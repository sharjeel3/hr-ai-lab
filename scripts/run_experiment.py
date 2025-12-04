"""
Main experiment runner for HR AI Lab.

This script provides a unified interface to run any experiment in the lab.
Usage:
    python run_experiment.py --experiment cv_screening --config config.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any
import logging

from utils import (
    LLMClient,
    load_dataset,
    save_results,
    timestamp,
    get_experiment_path,
    get_dataset_path,
    get_results_path,
    logger
)


class ExperimentRunner:
    """Base class for running experiments."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize experiment runner.
        
        Args:
            config: Experiment configuration
        """
        self.config = config
        self.experiment_name = config.get("experiment_name", "unknown")
        self.llm_client = LLMClient(
            provider=config.get("llm_provider", "openai"),
            model=config.get("llm_model", "gpt-4")
        )
        self.results = []
        
    def run(self) -> Dict[str, Any]:
        """
        Run the experiment.
        
        Returns:
            Experiment results
        """
        logger.info(f"Starting experiment: {self.experiment_name}")
        
        try:
            # Load data
            data = self.load_data()
            logger.info(f"Loaded {len(data)} items")
            
            # Process each item
            for idx, item in enumerate(data):
                logger.info(f"Processing item {idx + 1}/{len(data)}")
                result = self.process_item(item)
                self.results.append(result)
            
            # Save results
            self.save_results()
            
            # Calculate metrics
            metrics = self.calculate_metrics()
            
            return {
                "experiment": self.experiment_name,
                "status": "success",
                "items_processed": len(data),
                "metrics": metrics,
                "results_path": self.get_output_path()
            }
            
        except Exception as e:
            logger.error(f"Experiment failed: {str(e)}")
            return {
                "experiment": self.experiment_name,
                "status": "failed",
                "error": str(e)
            }
    
    def load_data(self) -> list:
        """Load experiment data. Override in subclasses."""
        dataset_name = self.config.get("dataset", "")
        dataset_path = get_dataset_path(dataset_name)
        return load_dataset(str(dataset_path))
    
    def process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single data item. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement process_item()")
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate experiment metrics. Override in subclasses."""
        return {
            "total_items": len(self.results)
        }
    
    def save_results(self):
        """Save experiment results."""
        output_path = self.get_output_path()
        save_results(self.results, output_path, format="json")
    
    def get_output_path(self) -> str:
        """Get output file path."""
        results_dir = get_results_path()
        results_dir.mkdir(parents=True, exist_ok=True)
        ts = timestamp()
        return str(results_dir / f"{self.experiment_name}_{ts}.json")


class CVScreeningExperiment(ExperimentRunner):
    """CV Screening benchmark experiment."""
    
    def __init__(self, config: Dict[str, Any]):
        config["experiment_name"] = "cv_screening"
        config["dataset"] = "synthetic_cvs"
        super().__init__(config)
    
    def process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single CV."""
        cv_text = item.get("text", "")
        
        prompt = f"""Extract the following fields from this CV:
- Skills (mapped to standard ontology)
- Years of experience
- Certifications
- Projects with outcomes
- Education

Return ONLY valid JSON in this format:
{{
    "name": "...",
    "skills": [...],
    "experience_years": 0,
    "certifications": [...],
    "projects": [...],
    "education": [...]
}}

CV:
{cv_text}
"""
        
        response = self.llm_client.call(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1000
        )
        
        try:
            # Try to parse JSON from response
            parsed = json.loads(response.get("response", "{}"))
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response for {item.get('filename', 'unknown')}")
            parsed = {}
        
        return {
            "input": item.get("filename", "unknown"),
            "output": parsed,
            "metadata": response.get("metadata", {})
        }
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate CV screening metrics."""
        successful_parses = sum(1 for r in self.results if r.get("output"))
        total_tokens = sum(
            r.get("metadata", {}).get("tokens_used", 0)
            for r in self.results
        )
        
        return {
            "total_items": len(self.results),
            "successful_parses": successful_parses,
            "parse_rate": successful_parses / len(self.results) if self.results else 0,
            "total_tokens_used": total_tokens,
            "avg_tokens_per_cv": total_tokens / len(self.results) if self.results else 0
        }


# Experiment registry
EXPERIMENTS = {
    "cv_screening": CVScreeningExperiment,
    # Add more experiments as they're implemented
}


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run HR AI Lab experiments")
    parser.add_argument(
        "--experiment",
        type=str,
        required=True,
        choices=list(EXPERIMENTS.keys()),
        help="Experiment to run"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (optional)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="LLM model to use"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "anthropic", "azure"],
        help="LLM provider"
    )
    
    args = parser.parse_args()
    
    # Load or create config
    if args.config:
        config = load_config(args.config)
    else:
        config = {
            "llm_model": args.model,
            "llm_provider": args.provider
        }
    
    # Get experiment class and run
    experiment_class = EXPERIMENTS[args.experiment]
    runner = experiment_class(config)
    results = runner.run()
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Experiment: {results['experiment']}")
    print(f"Status: {results['status']}")
    if results['status'] == 'success':
        print(f"Items processed: {results['items_processed']}")
        print(f"\nMetrics:")
        for key, value in results['metrics'].items():
            print(f"  {key}: {value}")
        print(f"\nResults saved to: {results['results_path']}")
    else:
        print(f"Error: {results.get('error', 'Unknown error')}")
    print("=" * 60)
    
    return 0 if results['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
