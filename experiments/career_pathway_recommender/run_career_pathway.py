#!/usr/bin/env python3
"""
Run Career Pathway Recommender Experiment

This script executes the career pathway recommendation experiment with
various test scenarios and generates detailed reports.

Usage:
    python run_career_pathway.py [--employees DATASET] [--top-k N] [--output DIR]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from scripts.utils import load_json_data, save_results, logger, timestamp
from career_recommender import CareerPathwayRecommender


def load_employee_profiles(dataset_path: str) -> List[Dict[str, Any]]:
    """
    Load employee profiles from dataset.
    
    Args:
        dataset_path: Path to employee profiles JSON or directory
        
    Returns:
        List of employee profile dictionaries
    """
    path = Path(dataset_path)
    
    if path.is_file():
        # Single JSON file
        data = load_json_data(str(path))
        if isinstance(data, list):
            return data
        else:
            return [data]
    
    elif path.is_dir():
        # Directory of JSON files
        profiles = []
        for file in path.glob('*.json'):
            try:
                data = load_json_data(str(file))
                if isinstance(data, list):
                    profiles.extend(data)
                else:
                    profiles.append(data)
            except Exception as e:
                logger.error(f"Error loading {file}: {e}")
        return profiles
    
    else:
        logger.error(f"Path not found: {dataset_path}")
        return []


def create_sample_employees() -> List[Dict[str, Any]]:
    """Create sample employee profiles for testing."""
    return [
        {
            'employee_id': 'EMP001',
            'name': 'Alex Johnson',
            'current_title': 'Software Engineer',
            'years_experience': 4,
            'skills': [
                'Python', 'JavaScript', 'React', 'Node.js',
                'PostgreSQL', 'Docker', 'Git', 'REST APIs',
                'System Design', 'Agile Development'
            ],
            'education_level': 'Bachelor of Science in Computer Science',
            'certifications': ['AWS Certified Developer'],
            'career_interests': [
                'Technical Leadership',
                'System Architecture',
                'Team Mentoring'
            ],
            'strengths': [
                'Problem Solving',
                'Technical Communication',
                'Cross-team Collaboration'
            ]
        },
        {
            'employee_id': 'EMP002',
            'name': 'Maria Rodriguez',
            'current_title': 'Senior Software Engineer',
            'years_experience': 7,
            'skills': [
                'Java', 'Python', 'Kubernetes', 'Microservices',
                'AWS', 'Terraform', 'CI/CD', 'System Architecture',
                'Team Leadership', 'Technical Mentoring'
            ],
            'education_level': 'Master of Science in Computer Science',
            'certifications': ['AWS Solutions Architect', 'Kubernetes Administrator'],
            'career_interests': [
                'Engineering Management',
                'Technical Strategy',
                'Organization Building'
            ],
            'strengths': [
                'Technical Leadership',
                'Strategic Thinking',
                'Stakeholder Management'
            ]
        },
        {
            'employee_id': 'EMP003',
            'name': 'David Chen',
            'current_title': 'Junior Data Analyst',
            'years_experience': 1.5,
            'skills': [
                'Python', 'SQL', 'Pandas', 'Matplotlib',
                'Excel', 'Tableau', 'Statistics',
                'Data Visualization', 'A/B Testing'
            ],
            'education_level': 'Bachelor of Science in Statistics',
            'certifications': ['Google Data Analytics Certificate'],
            'career_interests': [
                'Machine Learning',
                'Data Science',
                'Advanced Analytics'
            ],
            'strengths': [
                'Analytical Thinking',
                'Attention to Detail',
                'Quick Learner'
            ]
        },
        {
            'employee_id': 'EMP004',
            'name': 'Sarah Kim',
            'current_title': 'Product Manager',
            'years_experience': 5,
            'skills': [
                'Product Strategy', 'User Research', 'Roadmap Planning',
                'Agile/Scrum', 'Stakeholder Management', 'Data Analysis',
                'A/B Testing', 'SQL', 'Jira', 'Figma'
            ],
            'education_level': 'MBA',
            'certifications': ['Certified Scrum Product Owner', 'Product Management Certificate'],
            'career_interests': [
                'Senior Product Leadership',
                'Product Strategy',
                'Team Management'
            ],
            'strengths': [
                'Strategic Vision',
                'Cross-functional Leadership',
                'User Empathy'
            ]
        }
    ]


def generate_report(
    recommendations: List[Dict[str, Any]],
    metrics: Dict[str, Any],
    output_path: Path
) -> None:
    """
    Generate a human-readable report from recommendations.
    
    Args:
        recommendations: List of recommendation results
        metrics: Evaluation metrics
        output_path: Path to save report
    """
    report_lines = []
    
    report_lines.append("="*80)
    report_lines.append("CAREER PATHWAY RECOMMENDATION REPORT")
    report_lines.append("="*80)
    report_lines.append(f"\nGenerated: {timestamp()}")
    report_lines.append(f"Total Employees Analyzed: {metrics['total_employees']}")
    report_lines.append(f"Successful Recommendations: {metrics['successful_recommendations']}")
    report_lines.append(f"Success Rate: {metrics['success_rate']:.1%}")
    report_lines.append(f"Average Match Score: {metrics['average_similarity_score']:.2%}")
    report_lines.append(f"Unique Roles Recommended: {metrics['unique_roles_recommended']}")
    report_lines.append("\n" + "="*80 + "\n")
    
    for i, rec in enumerate(recommendations, 1):
        if 'error' in rec:
            report_lines.append(f"\n{i}. Employee: {rec.get('employee_id', 'Unknown')} - ERROR")
            report_lines.append(f"   {rec['error']}")
            continue
        
        report_lines.append(f"\n{i}. EMPLOYEE: {rec['employee_name']} ({rec['employee_id']})")
        report_lines.append(f"   Current Role: {rec['current_title']}")
        
        # Get all recommendations (eligible now + future)
        all_recs = []
        if isinstance(rec.get('recommendations'), dict):
            all_recs.extend(rec['recommendations'].get('eligible_now', []))
            all_recs.extend(rec['recommendations'].get('future_opportunities', []))
        elif isinstance(rec.get('recommendations'), list):
            all_recs = rec['recommendations']
        
        if not all_recs:
            report_lines.append(f"\n   No suitable career pathways identified.")
            continue
            
        report_lines.append(f"\n   RECOMMENDED CAREER PATHS:")
        
        for j, path in enumerate(all_recs, 1):
            role = path.get('role', {})
            status = path.get('status', 'ELIGIBLE_NOW')
            report_lines.append(f"\n   {j}. {role.get('title', 'Unknown')} - {role.get('job_family', 'Unknown')} [{status}]")
            report_lines.append(f"      Match Score: {path.get('similarity_score', 0):.2%}")
            report_lines.append(f"      Experience Required: {role.get('years_experience', 'N/A')}")
            report_lines.append(f"      Salary Range: {role.get('salary_range', 'N/A')}")
            
            # Show eligibility details if available
            if 'eligibility' in path:
                eligibility = path['eligibility']
                if eligibility.get('readiness_score') is not None:
                    report_lines.append(f"      Readiness Score: {eligibility['readiness_score']:.1f}%")
            
            report_lines.append(f"\n      WHY THIS ROLE:")
            # Wrap explanation text
            explanation = path.get('explanation', 'No explanation provided')
            for line in explanation.split('\n'):
                if line.strip():
                    report_lines.append(f"      {line}")
            
            report_lines.append(f"\n      90-DAY DEVELOPMENT PLAN:")
            plan = path.get('development_plan', '')
            
            # Handle both structured and text-based plans
            if isinstance(plan, dict):
                for month in ['month_1', 'month_2', 'month_3']:
                    if month in plan:
                        month_data = plan[month]
                        month_num = month.split('_')[1]
                        report_lines.append(f"\n      Month {month_num}: {month_data.get('focus', 'N/A')}")
                        
                        if 'objectives' in month_data:
                            report_lines.append(f"      Objectives:")
                            for obj in month_data['objectives']:
                                report_lines.append(f"        • {obj}")
                        
                        if 'activities' in month_data:
                            report_lines.append(f"      Activities:")
                            for activity in month_data['activities'][:2]:  # Show first 2
                                report_lines.append(f"        • {activity}")
            else:
                # Text-based plan
                for line in str(plan).split('\n'):
                    if line.strip():
                        report_lines.append(f"      {line}")
            
            if 'total_estimated_hours' in plan:
                report_lines.append(f"\n      Total Estimated Hours: {plan['total_estimated_hours']}")
        
        report_lines.append("\n" + "-"*80)
    
    # Write report
    report_text = "\n".join(report_lines)
    with open(output_path, 'w') as f:
        f.write(report_text)
    
    logger.info(f"Report saved to {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Run Career Pathway Recommender Experiment'
    )
    parser.add_argument(
        '--employees',
        type=str,
        help='Path to employee profiles JSON file or directory'
    )
    parser.add_argument(
        '--top-k',
        type=int,
        default=3,
        help='Number of recommendations per employee (default: 3)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for results (default: results/career_pathway)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / 'config.json'
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    career_config = config['experiments']['career_pathway']
    career_config['llm_provider'] = config['default_experiment_config']['llm_provider']
    
    # Initialize recommender
    logger.info("Initializing Career Pathway Recommender...")
    recommender = CareerPathwayRecommender(career_config)
    
    # Load job families
    job_families_dir = project_root / 'datasets' / 'job_families'
    job_family_files = list(job_families_dir.glob('job_family_*.json'))
    
    if not job_family_files:
        logger.error("No job family files found!")
        return 1
    
    logger.info(f"Loading {len(job_family_files)} job families...")
    recommender.load_job_families([str(f) for f in job_family_files])
    
    # Load or create employee profiles
    if args.employees:
        logger.info(f"Loading employee profiles from {args.employees}")
        employees = load_employee_profiles(args.employees)
    else:
        logger.info("Using sample employee profiles")
        employees = create_sample_employees()
    
    if not employees:
        logger.error("No employee profiles loaded!")
        return 1
    
    logger.info(f"Processing {len(employees)} employees...")
    
    # Generate recommendations
    recommendations = recommender.batch_recommend(employees, top_k=args.top_k)
    
    # Evaluate results
    metrics = recommender.evaluate_recommendations(recommendations)
    
    # Setup output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = project_root / 'results' / 'career_pathway'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save results
    ts = timestamp()
    
    # Save JSON results
    json_output = output_dir / f'recommendations_{ts}.json'
    save_results({
        'recommendations': recommendations,
        'metrics': metrics,
        'config': career_config
    }, str(json_output))
    logger.info(f"JSON results saved to {json_output}")
    
    # Save metrics
    metrics_output = output_dir / f'metrics_{ts}.json'
    save_results(metrics, str(metrics_output))
    logger.info(f"Metrics saved to {metrics_output}")
    
    # Generate human-readable report
    report_output = output_dir / f'report_{ts}.txt'
    generate_report(recommendations, metrics, report_output)
    
    # Print summary
    print("\n" + "="*80)
    print("EXPERIMENT COMPLETE")
    print("="*80)
    print(f"\nTotal Employees: {metrics['total_employees']}")
    print(f"Successful Recommendations: {metrics['successful_recommendations']}")
    print(f"Success Rate: {metrics['success_rate']:.1%}")
    print(f"Average Match Score: {metrics['average_similarity_score']:.2%}")
    print(f"Unique Roles Recommended: {metrics['unique_roles_recommended']}")
    print(f"\nOutputs:")
    print(f"  - JSON: {json_output}")
    print(f"  - Metrics: {metrics_output}")
    print(f"  - Report: {report_output}")
    print("="*80 + "\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
