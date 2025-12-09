"""
Run complete Culture Transformation Coach experiment and save results.

This script runs the full experiment pipeline:
1. Generate synthetic survey data
2. Analyze culture survey
3. Assess culture health
4. Generate transformation plan
5. Provide coaching guidance
6. Save all results to results folder
7. Generate visualizations and reports
"""

import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import experiment modules
import sys
sys.path.append(str(Path(__file__).parent))

from culture_coach import CultureTransformationCoach
from generate_culture_data import CultureDataGenerator


class CultureExperimentRunner:
    """Run complete culture transformation experiment."""
    
    def __init__(self, output_dir: str = None):
        """Initialize experiment runner."""
        # Get project root directory
        project_root = Path(__file__).parent.parent.parent
        
        if output_dir is None:
            self.output_dir = project_root / "results" / "culture_transformation"
        else:
            self.output_dir = Path(output_dir)
            if not self.output_dir.is_absolute():
                self.output_dir = project_root / output_dir
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {}
        
    def generate_test_data(self, num_responses: int = 100):
        """Generate synthetic survey data."""
        print("\n" + "="*60)
        print("Step 1: Generating Synthetic Survey Data")
        print("="*60)
        
        generator = CultureDataGenerator()
        
        # Generate survey responses
        responses = generator.generate_survey_responses(
            num_responses=num_responses,
            culture_profile="mixed"
        )
        
        # Generate organization context
        context = generator.generate_organization_context()
        
        print(f"✓ Generated {len(responses)} survey responses")
        print(f"✓ Organization: {context['company_size']} {context['industry']} company")
        
        # Save to datasets folder as well
        project_root = Path(__file__).parent.parent.parent
        datasets_dir = project_root / "datasets" / "culture_surveys"
        datasets_dir.mkdir(parents=True, exist_ok=True)
        
        with open(datasets_dir / f"survey_responses_{self.timestamp}.json", "w") as f:
            json.dump(responses, f, indent=2)
        
        with open(datasets_dir / f"organization_context_{self.timestamp}.json", "w") as f:
            json.dump(context, f, indent=2)
        
        self.results['survey_responses'] = responses
        self.results['organization_context'] = context
        
        return responses, context
    
    def run_culture_analysis(self, responses, context):
        """Run culture survey analysis."""
        print("\n" + "="*60)
        print("Step 2: Analyzing Culture Survey")
        print("="*60)
        
        coach = CultureTransformationCoach()
        
        print("Analyzing survey responses with AI...")
        analysis = coach.analyze_culture_survey(responses, context)
        
        if analysis.get("parsed", True):
            print("✓ Culture analysis completed")
            if "key_themes" in analysis:
                print(f"  - Key themes: {len(analysis.get('key_themes', []))} identified")
            if "strengths" in analysis:
                print(f"  - Strengths: {len(analysis.get('strengths', []))} identified")
            if "areas_for_improvement" in analysis:
                print(f"  - Areas for improvement: {len(analysis.get('areas_for_improvement', []))} identified")
        else:
            print("✓ Culture analysis completed (raw format)")
        
        self.results['culture_analysis'] = analysis
        
        # Save individual result
        with open(self.output_dir / f"culture_analysis_{self.timestamp}.json", "w") as f:
            json.dump(analysis, f, indent=2)
        
        return analysis
    
    def run_health_assessment(self):
        """Run culture health assessment."""
        print("\n" + "="*60)
        print("Step 3: Assessing Culture Health")
        print("="*60)
        
        coach = CultureTransformationCoach()
        
        # Calculate metrics from survey data
        responses = self.results['survey_responses']
        
        # Calculate average scores
        all_scores = []
        dimension_scores = {}
        
        for response in responses:
            ratings = response.get("ratings", {})
            for dim, data in ratings.items():
                score = data.get("score", 0)
                all_scores.append(score)
                
                if dim not in dimension_scores:
                    dimension_scores[dim] = []
                dimension_scores[dim].append(score)
        
        avg_engagement = sum(all_scores) / len(all_scores) if all_scores else 0
        
        # Create metrics
        metrics = {
            "employee_engagement": round(avg_engagement, 2),
            "retention_rate": 0.85,
            "innovation_index": round(sum(dimension_scores.get('innovation', [0])) / len(dimension_scores.get('innovation', [1])), 2),
            "collaboration_score": round(sum(dimension_scores.get('collaboration', [0])) / len(dimension_scores.get('collaboration', [1])), 2),
            "leadership_trust": round(sum(dimension_scores.get('leadership', [0])) / len(dimension_scores.get('leadership', [1])), 2)
        }
        
        # Historical data (simulated)
        historical_data = [
            {"month": "2024-09", "employee_engagement": avg_engagement - 0.2},
            {"month": "2024-10", "employee_engagement": avg_engagement - 0.1},
            {"month": "2024-11", "employee_engagement": avg_engagement}
        ]
        
        print("Assessing culture health with AI...")
        assessment = coach.assess_culture_health(metrics, historical_data)
        
        print("✓ Health assessment completed")
        if isinstance(assessment.get("overall_health_score"), (int, float)):
            print(f"  - Overall health score: {assessment['overall_health_score']:.1f}/100")
        
        self.results['health_assessment'] = assessment
        self.results['metrics'] = metrics
        self.results['historical_data'] = historical_data
        
        # Save individual result
        with open(self.output_dir / f"health_assessment_{self.timestamp}.json", "w") as f:
            json.dump(assessment, f, indent=2)
        
        return assessment
    
    def generate_transformation_plan(self, analysis):
        """Generate transformation plan."""
        print("\n" + "="*60)
        print("Step 4: Generating Transformation Plan")
        print("="*60)
        
        coach = CultureTransformationCoach()
        
        # Define goals based on analysis
        goals = [
            "Improve overall employee engagement",
            "Enhance leadership transparency",
            "Foster innovation culture",
            "Strengthen cross-department collaboration"
        ]
        
        constraints = {
            "budget": "moderate",
            "timeline": "12 months",
            "leadership_support": "high",
            "change_capacity": "medium"
        }
        
        print("Generating transformation plan with AI...")
        plan = coach.generate_transformation_plan(analysis, goals, constraints)
        
        print("✓ Transformation plan generated")
        if "phases" in plan:
            phases = plan.get('phases', {})
            print(f"  - Planning phases: {len(phases)}")
        
        self.results['transformation_plan'] = plan
        
        # Save individual result
        with open(self.output_dir / f"transformation_plan_{self.timestamp}.json", "w") as f:
            json.dump(plan, f, indent=2)
        
        return plan
    
    def provide_coaching_guidance(self):
        """Provide coaching guidance for common scenarios."""
        print("\n" + "="*60)
        print("Step 5: Generating Coaching Guidance")
        print("="*60)
        
        coach = CultureTransformationCoach()
        
        # Common scenarios
        scenarios = [
            {
                "name": "Remote Work Resistance",
                "scenario": "Middle managers are resisting the new hybrid work policy",
                "context": {
                    "company_size": self.results['organization_context']['company_size'],
                    "industry": self.results['organization_context']['industry'],
                    "policy": "3 days remote, 2 days office"
                }
            },
            {
                "name": "Innovation Stagnation",
                "scenario": "Team members are not proposing new ideas or taking initiative",
                "context": {
                    "company_size": self.results['organization_context']['company_size'],
                    "recent_changes": self.results['organization_context'].get('recent_changes', [])
                }
            }
        ]
        
        all_guidance = {}
        
        for scenario_data in scenarios:
            print(f"Generating guidance for: {scenario_data['name']}...")
            guidance = coach.provide_coaching_guidance(
                scenario_data['scenario'],
                scenario_data['context']
            )
            all_guidance[scenario_data['name']] = guidance
            print(f"✓ {scenario_data['name']} guidance generated")
        
        self.results['coaching_guidance'] = all_guidance
        
        # Save individual result
        with open(self.output_dir / f"coaching_guidance_{self.timestamp}.json", "w") as f:
            json.dump(all_guidance, f, indent=2)
        
        return all_guidance
    
    def save_comprehensive_results(self):
        """Save all results to a single comprehensive file."""
        print("\n" + "="*60)
        print("Step 6: Saving Comprehensive Results")
        print("="*60)
        
        comprehensive_results = {
            "experiment_metadata": {
                "timestamp": self.timestamp,
                "experiment": "Culture Transformation Coach",
                "num_responses": len(self.results['survey_responses']),
                "organization": self.results['organization_context']
            },
            "survey_data": {
                "responses": self.results['survey_responses'],
                "context": self.results['organization_context']
            },
            "analysis": self.results['culture_analysis'],
            "health_assessment": self.results['health_assessment'],
            "metrics": self.results['metrics'],
            "historical_data": self.results['historical_data'],
            "transformation_plan": self.results['transformation_plan'],
            "coaching_guidance": self.results['coaching_guidance']
        }
        
        # Save comprehensive results
        output_file = self.output_dir / f"experiment_results_{self.timestamp}.json"
        with open(output_file, "w") as f:
            json.dump(comprehensive_results, f, indent=2)
        
        print(f"✓ Comprehensive results saved to: {output_file}")
        
        # Create summary file
        summary = {
            "timestamp": self.timestamp,
            "experiment": "Culture Transformation Coach",
            "files_generated": [
                f"experiment_results_{self.timestamp}.json",
                f"culture_analysis_{self.timestamp}.json",
                f"health_assessment_{self.timestamp}.json",
                f"transformation_plan_{self.timestamp}.json",
                f"coaching_guidance_{self.timestamp}.json"
            ],
            "summary_statistics": {
                "total_responses": len(self.results['survey_responses']),
                "overall_health_score": comprehensive_results['health_assessment'].get('overall_health_score', 'N/A'),
                "organization_type": f"{self.results['organization_context']['company_size']} {self.results['organization_context']['industry']}"
            }
        }
        
        summary_file = self.output_dir / f"experiment_summary_{self.timestamp}.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"✓ Summary saved to: {summary_file}")
        
        return output_file
    
    def generate_visualizations(self):
        """Generate visualizations and HTML report."""
        print("\n" + "="*60)
        print("Step 7: Generating Visualizations")
        print("="*60)
        
        try:
            # Try to import visualization generator
            project_root = Path(__file__).parent.parent.parent
            dashboards_path = project_root / "results" / "dashboards"
            sys.path.insert(0, str(dashboards_path))
            from generate_culture_report import CultureVisualizationGenerator
            
            viz_gen = CultureVisualizationGenerator(
                output_dir=str(self.output_dir)
            )
            
            print("Generating comprehensive HTML report...")
            report_path = viz_gen.generate_comprehensive_report(
                survey_data=self.results['survey_responses'],
                assessment=self.results['health_assessment'],
                plan=self.results['transformation_plan']
            )
            
            print(f"✓ HTML report generated: {report_path}")
            
            # Generate individual charts
            print("Generating dimension heatmap...")
            viz_gen.generate_dimension_heatmap(
                self.results['survey_responses'],
                save_path=f"dimension_heatmap_{self.timestamp}.png"
            )
            print(f"✓ Heatmap saved")
            
            # Generate trend chart if historical data available
            if self.results.get('historical_data'):
                print("Generating trend chart...")
                viz_gen.generate_trend_chart(
                    self.results['historical_data'],
                    metric="employee_engagement",
                    save_path=f"engagement_trend_{self.timestamp}.png"
                )
                print(f"✓ Trend chart saved")
            
        except ImportError as e:
            print(f"⚠️  Visualization generation skipped: {e}")
            print("   Install required packages: pip install matplotlib seaborn plotly pandas numpy")
        except Exception as e:
            print(f"⚠️  Error generating visualizations: {e}")
    
    def run_complete_experiment(self, num_responses: int = 100):
        """Run the complete experiment pipeline."""
        print("\n" + "="*70)
        print("CULTURE TRANSFORMATION COACH - FULL EXPERIMENT")
        print("="*70)
        print(f"Timestamp: {self.timestamp}")
        print(f"Output directory: {self.output_dir}")
        
        # Check for API key
        if not os.environ.get("GOOGLE_API_KEY"):
            print("\n❌ ERROR: GOOGLE_API_KEY not set!")
            print("Please set your API key: export GOOGLE_API_KEY='your-key-here'")
            return None
        
        try:
            # Step 1: Generate data
            responses, context = self.generate_test_data(num_responses)
            
            # Step 2: Analyze culture
            analysis = self.run_culture_analysis(responses, context)
            
            # Step 3: Assess health
            assessment = self.run_health_assessment()
            
            # Step 4: Generate plan
            plan = self.generate_transformation_plan(analysis)
            
            # Step 5: Provide guidance
            guidance = self.provide_coaching_guidance()
            
            # Step 6: Save all results
            output_file = self.save_comprehensive_results()
            
            # Step 7: Generate visualizations
            self.generate_visualizations()
            
            # Final summary
            print("\n" + "="*70)
            print("EXPERIMENT COMPLETED SUCCESSFULLY! ✓")
            print("="*70)
            print(f"\n📁 Results saved to: {self.output_dir}")
            print(f"📊 Main results file: {output_file.name}")
            print(f"\n📈 View results:")
            print(f"   - Open HTML report: open {self.output_dir}/culture_report_*.html")
            print(f"   - View JSON results: cat {output_file}")
            print(f"\n🎯 Next steps:")
            print(f"   - Launch dashboard: streamlit run results/dashboards/culture_transformation_dashboard.py")
            print(f"   - Review transformation plan in: transformation_plan_{self.timestamp}.json")
            
            return output_file
            
        except Exception as e:
            print(f"\n❌ Experiment failed: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run Culture Transformation Coach experiment"
    )
    parser.add_argument(
        "--responses",
        type=int,
        default=100,
        help="Number of survey responses to generate (default: 100)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for results (default: results/culture_transformation)"
    )
    
    args = parser.parse_args()
    
    # Run experiment
    runner = CultureExperimentRunner(output_dir=args.output_dir)
    runner.run_complete_experiment(num_responses=args.responses)


if __name__ == "__main__":
    main()
