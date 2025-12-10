"""
HR AI Lab - Unified Results Dashboard Generator

This script generates a comprehensive, interactive HTML dashboard that displays
results from all HR AI Lab experiments in one unified view.

Features:
- Overview of all experiment results
- Individual experiment deep dives
- Model performance leaderboard
- Interactive charts and visualizations
- Responsive design for all devices
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import glob


class DashboardGenerator:
    """Generate unified HTML dashboard for all HR AI Lab experiments."""
    
    def __init__(self, results_dir: Path):
        """
        Initialize dashboard generator.
        
        Args:
            results_dir: Path to results directory
        """
        self.results_dir = Path(results_dir)
        self.data = self._load_all_results()
        
    def _load_all_results(self) -> Dict[str, Any]:
        """Load results from all experiments."""
        data = {
            'cv_screening': self._load_cv_screening_results(),
            'bias_testing': self._load_bias_testing_results(),
            'hris_data_quality': self._load_data_quality_results(),
            'interview_summarization': self._load_interview_results(),
            'culture_transformation': self._load_culture_results(),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }
        return data
    
    def _load_cv_screening_results(self) -> Dict[str, Any]:
        """Load CV screening experiment results."""
        results_path = self.results_dir / 'cv_screening'
        
        if not results_path.exists():
            return {'available': False, 'message': 'No CV screening results found'}
        
        # Look for JSON result files
        json_files = list(results_path.glob('*.json'))
        
        if not json_files:
            return {'available': False, 'message': 'No CV screening data files'}
        
        # Load most recent
        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
        
        try:
            with open(latest_file) as f:
                data = json.load(f)
            
            return {
                'available': True,
                'file': str(latest_file),
                'data': data,
                'timestamp': datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
            }
        except Exception as e:
            return {'available': False, 'message': f'Error loading: {e}'}
    
    def _load_bias_testing_results(self) -> Dict[str, Any]:
        """Load bias testing experiment results."""
        results_path = self.results_dir / 'bias_testing'
        
        if not results_path.exists():
            return {'available': False, 'message': 'No bias testing results found'}
        
        # Look for JSON result files
        json_files = list(results_path.glob('*.json'))
        html_files = list(results_path.glob('*.html'))
        
        results = {
            'available': len(json_files) > 0 or len(html_files) > 0,
            'json_reports': len(json_files),
            'html_reports': len(html_files),
            'reports': []
        }
        
        # Load latest JSON if available
        if json_files:
            latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
            try:
                with open(latest_file) as f:
                    data = json.load(f)
                results['data'] = data
                results['file'] = str(latest_file)
            except Exception as e:
                results['message'] = f'Error loading: {e}'
        
        return results
    
    def _load_data_quality_results(self) -> Dict[str, Any]:
        """Load HRIS data quality experiment results."""
        results_path = self.results_dir / 'hris_data_quality'
        
        if not results_path.exists():
            return {'available': False, 'message': 'No data quality results found'}
        
        # Look for quality report JSON files
        json_files = list(results_path.glob('quality_report_*.json'))
        
        if not json_files:
            return {'available': False, 'message': 'No quality reports found'}
        
        # Load most recent
        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
        
        try:
            with open(latest_file) as f:
                data = json.load(f)
            
            return {
                'available': True,
                'file': str(latest_file),
                'data': data,
                'timestamp': datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat(),
                'total_reports': len(json_files)
            }
        except Exception as e:
            return {'available': False, 'message': f'Error loading: {e}'}
    
    def _load_interview_results(self) -> Dict[str, Any]:
        """Load interview summarization results."""
        results_path = self.results_dir / 'interview_summarization'
        
        if not results_path.exists():
            return {'available': False, 'message': 'No interview results found'}
        
        json_files = list(results_path.glob('*.json'))
        
        return {
            'available': len(json_files) > 0,
            'total_reports': len(json_files),
            'message': f'Found {len(json_files)} interview summaries' if json_files else 'No data'
        }
    
    def _load_culture_results(self) -> Dict[str, Any]:
        """Load culture transformation results."""
        results_path = self.results_dir / 'culture_transformation'
        
        if not results_path.exists():
            return {'available': False, 'message': 'No culture results found'}
        
        json_files = list(results_path.glob('*.json'))
        
        return {
            'available': len(json_files) > 0,
            'total_reports': len(json_files),
            'message': f'Found {len(json_files)} culture reports' if json_files else 'No data'
        }
    
    def generate_html(self) -> str:
        """Generate complete HTML dashboard."""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR AI Lab - Results Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .timestamp {{
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-bottom: 30px;
        }}
        
        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .metric-card h3 {{
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-top: 10px;
        }}
        
        .status-available {{
            background: #10b981;
            color: white;
        }}
        
        .status-unavailable {{
            background: #ef4444;
            color: white;
        }}
        
        .status-partial {{
            background: #f59e0b;
            color: white;
        }}
        
        .experiments-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .experiment-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .experiment-card h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        
        .experiment-stats {{
            margin: 20px 0;
        }}
        
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .stat-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .stat-value {{
            color: #333;
            font-weight: bold;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .chart-title {{
            color: #667eea;
            font-size: 1.3em;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        canvas {{
            max-height: 400px;
        }}
        
        .quality-score {{
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }}
        
        .quality-excellent {{ color: #10b981; }}
        .quality-good {{ color: #3b82f6; }}
        .quality-fair {{ color: #f59e0b; }}
        .quality-poor {{ color: #ef4444; }}
        
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e5e7eb;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .issue-breakdown {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .issue-item {{
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .issue-critical {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .issue-high {{
            background: #fed7aa;
            color: #9a3412;
        }}
        
        .issue-medium {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .issue-low {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .recommendations {{
            background: #f0f9ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        
        .recommendations h4 {{
            color: #1e40af;
            margin-bottom: 10px;
        }}
        
        .recommendations ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .recommendations li {{
            padding: 8px 0;
            color: #1e3a8a;
        }}
        
        .recommendations li:before {{
            content: "→ ";
            font-weight: bold;
            margin-right: 10px;
        }}
        
        .issues-section {{
            margin: 30px 0;
        }}
        
        .issues-section h4 {{
            color: #1f2937;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        
        .issues-table {{
            width: 100%;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .issues-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .issues-table th {{
            background: #f3f4f6;
            color: #374151;
            font-weight: 600;
            padding: 12px;
            text-align: left;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .issues-table td {{
            padding: 12px;
            border-top: 1px solid #e5e7eb;
            font-size: 0.9em;
            color: #4b5563;
        }}
        
        .issues-table tr:hover {{
            background: #f9fafb;
        }}
        
        .severity-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .severity-critical {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .severity-high {{
            background: #fed7aa;
            color: #9a3412;
        }}
        
        .severity-medium {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .severity-low {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .issue-type-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.75em;
            background: #e0e7ff;
            color: #3730a3;
            font-weight: 500;
        }}
        
        .auto-fix-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.7em;
            background: #d1fae5;
            color: #065f46;
            font-weight: 600;
        }}
        
        .manual-fix-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.7em;
            background: #fef3c7;
            color: #92400e;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .experiments-grid {{
                grid-template-columns: 1fr;
            }}
            
            .overview-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 HR AI Lab</h1>
            <p>Unified Experiments Dashboard</p>
        </div>
        
        <div class="timestamp">
            📅 Generated: {self.data['metadata']['generated_at'][:19].replace('T', ' ')}
        </div>
        
        {self._generate_overview_section()}
        
        {self._generate_experiments_sections()}
        
        {self._generate_charts_section()}
    </div>
    
    <script>
        {self._generate_chart_scripts()}
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_overview_section(self) -> str:
        """Generate overview metrics section."""
        
        # Count available experiments
        available_count = sum([
            1 if self.data['cv_screening'].get('available') else 0,
            1 if self.data['bias_testing'].get('available') else 0,
            1 if self.data['hris_data_quality'].get('available') else 0,
            1 if self.data['interview_summarization'].get('available') else 0,
            1 if self.data['culture_transformation'].get('available') else 0,
        ])
        
        total_experiments = 5
        completion_pct = (available_count / total_experiments) * 100
        
        # Get data quality score if available
        dq_score = "N/A"
        if self.data['hris_data_quality'].get('available'):
            dq_score = f"{self.data['hris_data_quality']['data'].get('quality_score', 0):.1f}"
        
        html = f"""
        <div class="overview-grid">
            <div class="metric-card">
                <h3>Experiments Run</h3>
                <div class="metric-value">{available_count}/{total_experiments}</div>
                <div class="metric-label">Active Experiments</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_pct}%">{completion_pct:.0f}%</div>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Data Quality Score</h3>
                <div class="metric-value">{dq_score}</div>
                <div class="metric-label">HRIS Data Health</div>
                {'<span class="status-badge status-available">Available</span>' if dq_score != "N/A" else '<span class="status-badge status-unavailable">Not Run</span>'}
            </div>
            
            <div class="metric-card">
                <h3>Bias Testing</h3>
                <div class="metric-value">{self.data['bias_testing'].get('json_reports', 0)}</div>
                <div class="metric-label">Reports Generated</div>
                {'<span class="status-badge status-available">Active</span>' if self.data['bias_testing'].get('available') else '<span class="status-badge status-unavailable">No Data</span>'}
            </div>
            
            <div class="metric-card">
                <h3>CV Screening</h3>
                <div class="metric-value">{"✓" if self.data['cv_screening'].get('available') else "✗"}</div>
                <div class="metric-label">Screening Pipeline</div>
                {'<span class="status-badge status-available">Operational</span>' if self.data['cv_screening'].get('available') else '<span class="status-badge status-unavailable">Pending</span>'}
            </div>
        </div>
        """
        
        return html
    
    def _generate_experiments_sections(self) -> str:
        """Generate detailed sections for each experiment."""
        
        sections = []
        
        # HRIS Data Quality Section
        if self.data['hris_data_quality'].get('available'):
            sections.append(self._generate_data_quality_section())
        
        # Bias Testing Section
        if self.data['bias_testing'].get('available'):
            sections.append(self._generate_bias_testing_section())
        
        # CV Screening Section
        if self.data['cv_screening'].get('available'):
            sections.append(self._generate_cv_screening_section())
        
        return f'<div class="experiments-grid">{"".join(sections)}</div>'
    
    def _generate_data_quality_section(self) -> str:
        """Generate HRIS data quality section."""
        
        data = self.data['hris_data_quality']['data']
        
        score = data.get('quality_score', 0)
        quality_class = (
            'quality-excellent' if score >= 90 else
            'quality-good' if score >= 75 else
            'quality-fair' if score >= 60 else
            'quality-poor'
        )
        
        issues_by_severity = data.get('issues_by_severity', {})
        
        html = f"""
        <div class="experiment-card">
            <h2>🔍 HRIS Data Quality</h2>
            <p style="color: #666; margin-bottom: 20px;">
                Comprehensive data quality analysis and validation
            </p>
            
            <div class="quality-score {quality_class}">
                {score:.1f}/100
            </div>
            
            <div class="experiment-stats">
                <div class="stat-row">
                    <span class="stat-label">Total Records</span>
                    <span class="stat-value">{data.get('total_records', 0)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Records with Issues</span>
                    <span class="stat-value">{data.get('records_with_issues', 0)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Total Issues</span>
                    <span class="stat-value">{data.get('total_issues', 0)}</span>
                </div>
            </div>
            
            <div class="issue-breakdown">
                <div class="issue-item issue-critical">
                    <div style="font-size: 2em; font-weight: bold;">{issues_by_severity.get('critical', 0)}</div>
                    <div style="font-size: 0.85em;">Critical</div>
                </div>
                <div class="issue-item issue-high">
                    <div style="font-size: 2em; font-weight: bold;">{issues_by_severity.get('high', 0)}</div>
                    <div style="font-size: 0.85em;">High</div>
                </div>
                <div class="issue-item issue-medium">
                    <div style="font-size: 2em; font-weight: bold;">{issues_by_severity.get('medium', 0)}</div>
                    <div style="font-size: 0.85em;">Medium</div>
                </div>
                <div class="issue-item issue-low">
                    <div style="font-size: 2em; font-weight: bold;">{issues_by_severity.get('low', 0)}</div>
                    <div style="font-size: 0.85em;">Low</div>
                </div>
            </div>
            
            <div class="recommendations">
                <h4>📋 Top Recommendations</h4>
                <ul>
                    {"".join([f"<li>{rec[:100]}</li>" for rec in data.get('recommendations', [])[:3]])}
                </ul>
            </div>
            
            {self._generate_issues_table(data.get('issues', []))}
        </div>
        """
        
        return html
    
    def _generate_issues_table(self, issues: List[Dict[str, Any]]) -> str:
        """Generate detailed issues table."""
        
        if not issues:
            return ""
        
        # Sort issues by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.get('severity', 'low'), 3))
        
        # Generate table rows
        rows = []
        for issue in sorted_issues:
            severity = issue.get('severity', 'low')
            issue_type = issue.get('issue_type', 'unknown').replace('_', ' ').title()
            record_id = issue.get('record_id', 'N/A')
            field_name = issue.get('field_name', 'N/A')
            description = issue.get('description', '')[:100]  # Truncate long descriptions
            auto_fixable = issue.get('auto_fixable', False)
            
            fix_badge = '<span class="auto-fix-badge">AUTO-FIX</span>' if auto_fixable else '<span class="manual-fix-badge">MANUAL</span>'
            
            rows.append(f"""
                <tr>
                    <td><span class="severity-badge severity-{severity}">{severity.upper()}</span></td>
                    <td><span class="issue-type-badge">{issue_type}</span></td>
                    <td><strong>{record_id}</strong></td>
                    <td>{field_name}</td>
                    <td>{description}</td>
                    <td>{fix_badge}</td>
                </tr>
            """)
        
        html = f"""
        <div class="issues-section">
            <h4>🔍 Detailed Issues List ({len(issues)} issues found)</h4>
            <div class="issues-table">
                <table>
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Issue Type</th>
                            <th>Record ID</th>
                            <th>Field</th>
                            <th>Description</th>
                            <th>Fix Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html
    
    def _generate_bias_testing_section(self) -> str:
        """Generate bias testing section."""
        
        data = self.data['bias_testing']
        
        html = f"""
        <div class="experiment-card">
            <h2>⚖️ Bias Testing</h2>
            <p style="color: #666; margin-bottom: 20px;">
                Ethical AI fairness and bias detection
            </p>
            
            <div class="experiment-stats">
                <div class="stat-row">
                    <span class="stat-label">JSON Reports</span>
                    <span class="stat-value">{data.get('json_reports', 0)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">HTML Dashboards</span>
                    <span class="stat-value">{data.get('html_reports', 0)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Status</span>
                    <span class="stat-value">✓ Active</span>
                </div>
            </div>
            
            <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <p style="color: #166534; font-weight: 500;">
                    Bias testing framework is operational. Regular testing recommended for all experiments.
                </p>
            </div>
        </div>
        """
        
        return html
    
    def _generate_cv_screening_section(self) -> str:
        """Generate CV screening section."""
        
        html = f"""
        <div class="experiment-card">
            <h2>📄 CV Screening</h2>
            <p style="color: #666; margin-bottom: 20px;">
                AI-powered candidate screening and ranking
            </p>
            
            <div class="experiment-stats">
                <div class="stat-row">
                    <span class="stat-label">Status</span>
                    <span class="stat-value">✓ Operational</span>
                </div>
            </div>
            
            <div style="background: #eff6ff; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <p style="color: #1e40af; font-weight: 500;">
                    CV screening pipeline configured and ready for candidate evaluation.
                </p>
            </div>
        </div>
        """
        
        return html
    
    def _generate_charts_section(self) -> str:
        """Generate charts section."""
        
        html = ""
        
        # Data quality issues by type chart
        if self.data['hris_data_quality'].get('available'):
            html += """
        <div class="chart-container">
            <h3 class="chart-title">Data Quality Issues by Type</h3>
            <canvas id="issuesChart"></canvas>
        </div>
        """
        
        # Experiment completion chart
        html += """
        <div class="chart-container">
            <h3 class="chart-title">Experiment Completion Status</h3>
            <canvas id="completionChart"></canvas>
        </div>
        """
        
        return html
    
    def _generate_chart_scripts(self) -> str:
        """Generate JavaScript for charts."""
        
        scripts = []
        
        # Data quality issues chart
        if self.data['hris_data_quality'].get('available'):
            issues_by_type = self.data['hris_data_quality']['data'].get('issues_by_type', {})
            
            labels = list(issues_by_type.keys())
            values = list(issues_by_type.values())
            
            scripts.append(f"""
        // Issues by Type Chart
        new Chart(document.getElementById('issuesChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps([l.replace('_', ' ').title() for l in labels])},
                datasets: [{{
                    label: 'Number of Issues',
                    data: {json.dumps(values)},
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgba(239, 68, 68, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(139, 92, 246, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
        """)
        
        # Completion status chart
        experiments = ['CV Screening', 'Bias Testing', 'Data Quality', 'Interviews', 'Culture']
        statuses = [
            1 if self.data['cv_screening'].get('available') else 0,
            1 if self.data['bias_testing'].get('available') else 0,
            1 if self.data['hris_data_quality'].get('available') else 0,
            1 if self.data['interview_summarization'].get('available') else 0,
            1 if self.data['culture_transformation'].get('available') else 0,
        ]
        
        scripts.append(f"""
        // Completion Status Chart
        new Chart(document.getElementById('completionChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Completed', 'Pending'],
                datasets: [{{
                    data: [{sum(statuses)}, {len(statuses) - sum(statuses)}],
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(229, 231, 235, 0.8)'
                    ],
                    borderColor: [
                        'rgba(16, 185, 129, 1)',
                        'rgba(229, 231, 235, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        """)
        
        return "\n".join(scripts)
    
    def save_dashboard(self, output_path: Optional[Path] = None) -> Path:
        """
        Save dashboard to HTML file.
        
        Args:
            output_path: Optional custom output path
            
        Returns:
            Path to saved dashboard
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.results_dir / 'dashboards' / f'unified_dashboard_{timestamp}.html'
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        html = self.generate_html()
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"✓ Dashboard saved to: {output_path}")
        return output_path


def main():
    """Generate and save unified dashboard."""
    
    # Get project root
    script_dir = Path(__file__).parent
    results_dir = script_dir.parent
    
    print("=" * 80)
    print("HR AI LAB - UNIFIED DASHBOARD GENERATOR")
    print("=" * 80)
    print()
    
    print("Loading results from all experiments...")
    generator = DashboardGenerator(results_dir)
    
    print(f"\nExperiment Status:")
    print(f"  • CV Screening: {'✓' if generator.data['cv_screening'].get('available') else '✗'}")
    print(f"  • Bias Testing: {'✓' if generator.data['bias_testing'].get('available') else '✗'}")
    print(f"  • Data Quality: {'✓' if generator.data['hris_data_quality'].get('available') else '✗'}")
    print(f"  • Interviews: {'✓' if generator.data['interview_summarization'].get('available') else '✗'}")
    print(f"  • Culture: {'✓' if generator.data['culture_transformation'].get('available') else '✗'}")
    print()
    
    print("Generating unified dashboard...")
    dashboard_path = generator.save_dashboard()
    
    print()
    print("=" * 80)
    print("DASHBOARD GENERATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Open the dashboard:")
    print(f"  {dashboard_path}")
    print()
    print("Or run:")
    print(f"  open {dashboard_path}")
    print()


if __name__ == '__main__':
    main()
