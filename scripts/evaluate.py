"""
Evaluation and benchmarking framework for HR AI Lab.

This module provides tools to evaluate experiment results,
calculate metrics, and generate benchmark comparisons.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
import statistics
from datetime import datetime

from utils import (
    load_dataset,
    save_results,
    calculate_accuracy,
    get_results_path,
    logger
)


class Evaluator:
    """Base evaluator class for experiments."""
    
    def __init__(self, experiment_name: str):
        """
        Initialize evaluator.
        
        Args:
            experiment_name: Name of the experiment
        """
        self.experiment_name = experiment_name
        self.metrics = {}
    
    def evaluate(
        self,
        results_path: str,
        ground_truth_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate experiment results.
        
        Args:
            results_path: Path to results file
            ground_truth_path: Path to ground truth data (optional)
            
        Returns:
            Dictionary of evaluation metrics
        """
        raise NotImplementedError("Subclasses must implement evaluate()")
    
    def calculate_basic_metrics(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate basic metrics common to all experiments."""
        if not results:
            return {}
        
        total_items = len(results)
        
        # Token usage metrics
        tokens = [
            r.get("metadata", {}).get("tokens_used", 0)
            for r in results
        ]
        
        return {
            "total_items": total_items,
            "total_tokens": sum(tokens),
            "avg_tokens_per_item": statistics.mean(tokens) if tokens else 0,
            "min_tokens": min(tokens) if tokens else 0,
            "max_tokens": max(tokens) if tokens else 0,
        }


class CVScreeningEvaluator(Evaluator):
    """Evaluator for CV screening experiments."""
    
    def __init__(self):
        super().__init__("cv_screening")
    
    def evaluate(
        self,
        results_path: str,
        ground_truth_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Evaluate CV screening results."""
        # Load results
        with open(results_path, 'r') as f:
            results = json.load(f)
        
        metrics = self.calculate_basic_metrics(results)
        
        # Extraction completeness
        required_fields = ["skills", "experience_years", "certifications", "projects", "education"]
        field_extraction_rates = {field: 0 for field in required_fields}
        
        for result in results:
            output = result.get("output", {})
            for field in required_fields:
                if field in output and output[field]:
                    field_extraction_rates[field] += 1
        
        # Convert to percentages
        for field in required_fields:
            field_extraction_rates[field] = (
                field_extraction_rates[field] / len(results) * 100
                if results else 0
            )
        
        metrics["extraction_rates"] = field_extraction_rates
        metrics["avg_extraction_rate"] = statistics.mean(field_extraction_rates.values())
        
        # Successful parses
        successful = sum(1 for r in results if r.get("output"))
        metrics["successful_parses"] = successful
        metrics["parse_success_rate"] = (successful / len(results) * 100) if results else 0
        
        return metrics


class BiasEvaluator:
    """Evaluator for bias testing across experiments."""
    
    def __init__(self):
        self.bias_metrics = {}
    
    def evaluate_bias(
        self,
        original_results: List[Dict],
        modified_results: List[Dict],
        modification_type: str
    ) -> Dict[str, Any]:
        """
        Evaluate bias by comparing original and modified results.
        
        Args:
            original_results: Results from original data
            modified_results: Results from modified data (e.g., name-swapped)
            modification_type: Type of modification (name_swap, gender_swap, etc.)
            
        Returns:
            Bias metrics
        """
        if len(original_results) != len(modified_results):
            logger.error("Results lists must have the same length")
            return {}
        
        # Calculate score differences
        score_diffs = []
        for orig, mod in zip(original_results, modified_results):
            orig_score = self._extract_score(orig)
            mod_score = self._extract_score(mod)
            if orig_score is not None and mod_score is not None:
                score_diffs.append(abs(orig_score - mod_score))
        
        if not score_diffs:
            return {}
        
        return {
            "modification_type": modification_type,
            "avg_score_difference": statistics.mean(score_diffs),
            "max_score_difference": max(score_diffs),
            "std_score_difference": statistics.stdev(score_diffs) if len(score_diffs) > 1 else 0,
            "pairs_evaluated": len(score_diffs),
            "bias_threshold_violations": sum(1 for d in score_diffs if d > 0.05),
            "bias_acceptable": statistics.mean(score_diffs) < 0.05
        }
    
    def _extract_score(self, result: Dict) -> Optional[float]:
        """Extract numerical score from result."""
        output = result.get("output", {})
        
        # Try common score fields
        for field in ["fit_score", "score", "rating", "confidence"]:
            if field in output:
                try:
                    return float(output[field])
                except (ValueError, TypeError):
                    pass
        
        return None


class BenchmarkComparator:
    """Compare multiple experiment runs or models."""
    
    def __init__(self):
        self.comparisons = []
    
    def compare_models(
        self,
        results_paths: Dict[str, str],
        metrics_to_compare: List[str]
    ) -> Dict[str, Any]:
        """
        Compare results from different models.
        
        Args:
            results_paths: Dict mapping model names to result file paths
            metrics_to_compare: List of metric names to compare
            
        Returns:
            Comparison results
        """
        all_metrics = {}
        
        # Load metrics for each model
        for model_name, path in results_paths.items():
            evaluator = self._get_evaluator(path)
            metrics = evaluator.evaluate(path)
            all_metrics[model_name] = metrics
        
        # Build comparison table
        comparison = {
            "models": list(results_paths.keys()),
            "metrics": {}
        }
        
        for metric in metrics_to_compare:
            comparison["metrics"][metric] = {
                model: all_metrics[model].get(metric, None)
                for model in results_paths.keys()
            }
            
            # Determine winner
            values = [
                all_metrics[model].get(metric, float('-inf'))
                for model in results_paths.keys()
            ]
            if values:
                best_idx = values.index(max(values))
                comparison["metrics"][metric]["winner"] = list(results_paths.keys())[best_idx]
        
        return comparison
    
    def _get_evaluator(self, results_path: str) -> Evaluator:
        """Get appropriate evaluator based on results file."""
        # Simple heuristic: check filename
        if "cv_screening" in results_path:
            return CVScreeningEvaluator()
        # Default to base evaluator
        return Evaluator("unknown")


def generate_leaderboard(results_dir: str, output_path: str = None):
    """
    Generate leaderboard from all experiment results.
    
    Args:
        results_dir: Directory containing result files
        output_path: Path to save leaderboard (optional)
    """
    results_path = Path(results_dir)
    if not results_path.exists():
        logger.error(f"Results directory not found: {results_dir}")
        return
    
    leaderboard_data = []
    
    # Process all JSON result files
    for result_file in results_path.glob("*.json"):
        try:
            with open(result_file, 'r') as f:
                results = json.load(f)
            
            # Extract key information
            if isinstance(results, list) and len(results) > 0:
                first_result = results[0]
                metadata = first_result.get("metadata", {})
                
                leaderboard_data.append({
                    "experiment": result_file.stem,
                    "model": metadata.get("model", "unknown"),
                    "provider": metadata.get("provider", "unknown"),
                    "items_processed": len(results),
                    "avg_tokens": statistics.mean([
                        r.get("metadata", {}).get("tokens_used", 0)
                        for r in results
                    ]) if results else 0,
                    "file": result_file.name
                })
        except Exception as e:
            logger.warning(f"Failed to process {result_file}: {str(e)}")
    
    # Sort by experiment and model
    leaderboard_data.sort(key=lambda x: (x["experiment"], x["avg_tokens"]))
    
    # Save leaderboard
    if output_path is None:
        output_path = str(get_results_path() / "leaderboard.csv")
    
    if leaderboard_data:
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=leaderboard_data[0].keys())
            writer.writeheader()
            writer.writerows(leaderboard_data)
        
        logger.info(f"Leaderboard saved to {output_path}")
        return leaderboard_data
    else:
        logger.warning("No results found to generate leaderboard")
        return []


def print_evaluation_report(metrics: Dict[str, Any]):
    """Print formatted evaluation report."""
    print("\n" + "=" * 70)
    print("EVALUATION REPORT")
    print("=" * 70)
    
    for key, value in metrics.items():
        if isinstance(value, dict):
            print(f"\n{key.upper().replace('_', ' ')}:")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, float):
                    print(f"  {sub_key}: {sub_value:.2f}")
                else:
                    print(f"  {sub_key}: {sub_value}")
        elif isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        results_path = sys.argv[1]
        
        # Determine evaluator type
        if "cv_screening" in results_path:
            evaluator = CVScreeningEvaluator()
        else:
            evaluator = Evaluator("generic")
        
        try:
            metrics = evaluator.evaluate(results_path)
            print_evaluation_report(metrics)
        except Exception as e:
            print(f"Evaluation failed: {str(e)}")
    else:
        # Generate leaderboard
        results_dir = get_results_path()
        leaderboard = generate_leaderboard(str(results_dir))
        print(f"Generated leaderboard with {len(leaderboard)} entries")
