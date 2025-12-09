"""
Generate visualizations and reports for culture transformation results.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class CultureVisualizationGenerator:
    """Generate visualizations for culture transformation results."""
    
    def __init__(self, output_dir: str = "../../results/culture_transformation"):
        """Initialize visualization generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def generate_health_score_gauge(
        self,
        score: float,
        title: str = "Culture Health Score"
    ) -> go.Figure:
        """Generate a gauge chart for health score."""
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 24}},
            delta={'reference': 70, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 60], 'color': '#fee2e2'},
                    {'range': [60, 70], 'color': '#fef3c7'},
                    {'range': [70, 80], 'color': '#d9f99d'},
                    {'range': [80, 100], 'color': '#bbf7d0'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="white",
            font={'color': "darkblue", 'family': "Arial"},
            height=400
        )
        
        return fig
    
    def generate_dimension_heatmap(
        self,
        survey_data: List[Dict],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Generate heatmap of dimension scores by department."""
        
        # Extract data
        data_records = []
        
        for response in survey_data:
            dept = response.get("department", "Unknown")
            ratings = response.get("ratings", {})
            
            record = {"department": dept}
            for dim, data in ratings.items():
                record[dim] = data.get("score", 0)
            
            data_records.append(record)
        
        # Create dataframe
        df = pd.DataFrame(data_records)
        
        # Calculate mean by department
        dept_means = df.groupby("department").mean()
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.heatmap(
            dept_means.T,
            annot=True,
            fmt=".1f",
            cmap="RdYlGn",
            center=5,
            vmin=0,
            vmax=10,
            cbar_kws={'label': 'Score'},
            ax=ax
        )
        
        ax.set_title("Culture Dimension Scores by Department", fontsize=16, fontweight='bold')
        ax.set_xlabel("Department", fontsize=12)
        ax.set_ylabel("Culture Dimension", fontsize=12)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(self.output_dir / save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_trend_chart(
        self,
        historical_data: List[Dict],
        metric: str = "employee_engagement",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Generate trend line chart."""
        
        df = pd.DataFrame(historical_data)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(
            df['month'],
            df[metric],
            marker='o',
            linewidth=2,
            markersize=8,
            color='#6366f1'
        )
        
        # Add trend line
        x = np.arange(len(df))
        z = np.polyfit(x, df[metric], 1)
        p = np.poly1d(z)
        
        ax.plot(
            df['month'],
            p(x),
            "--",
            color='red',
            alpha=0.7,
            label='Trend'
        )
        
        ax.set_title(f"{metric.replace('_', ' ').title()} Trend", 
                     fontsize=16, fontweight='bold')
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Score", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(self.output_dir / save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_radar_chart(
        self,
        dimension_scores: Dict[str, float],
        title: str = "Culture Dimensions"
    ) -> go.Figure:
        """Generate radar chart for culture dimensions."""
        
        categories = [dim.replace('_', ' ').title() for dim in dimension_scores.keys()]
        values = list(dimension_scores.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current State',
            marker=dict(color='#6366f1', size=8),
            line=dict(color='#6366f1', width=2)
        ))
        
        # Add target line
        target_values = [8.0] * len(categories)
        fig.add_trace(go.Scatterpolar(
            r=target_values,
            theta=categories,
            fill='toself',
            name='Target',
            opacity=0.3,
            marker=dict(color='#10b981'),
            line=dict(color='#10b981', width=2, dash='dash')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            title=dict(text=title, x=0.5, xanchor='center'),
            height=500
        )
        
        return fig
    
    def generate_distribution_plot(
        self,
        survey_data: List[Dict],
        dimension: str,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Generate distribution plot for a specific dimension."""
        
        scores = []
        for response in survey_data:
            ratings = response.get("ratings", {})
            if dimension in ratings:
                scores.append(ratings[dimension].get("score", 0))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Histogram
        ax.hist(scores, bins=20, alpha=0.7, color='#6366f1', edgecolor='black')
        
        # Add mean line
        mean_score = np.mean(scores)
        ax.axvline(mean_score, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_score:.2f}')
        
        ax.set_title(f"{dimension.replace('_', ' ').title()} Score Distribution",
                     fontsize=16, fontweight='bold')
        ax.set_xlabel("Score", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(self.output_dir / save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_comprehensive_report(
        self,
        survey_data: List[Dict],
        assessment: Dict,
        plan: Optional[Dict] = None
    ) -> str:
        """Generate comprehensive HTML report."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"culture_report_{timestamp}.html"
        
        # Calculate statistics
        dimension_scores = self._calculate_dimension_averages(survey_data)
        overall_score = assessment.get("overall_health_score", 0)
        
        # Generate visualizations
        gauge_fig = self.generate_health_score_gauge(overall_score)
        radar_fig = self.generate_radar_chart(dimension_scores)
        
        # Build HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Culture Transformation Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .section {{
                    background: white;
                    padding: 25px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .metric-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    background: #f0f2f6;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #6366f1;
                }}
                .metric-value {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #6366f1;
                }}
                .metric-label {{
                    color: #666;
                    margin-top: 5px;
                }}
                .recommendation {{
                    background: #eff6ff;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 3px solid #3b82f6;
                    border-radius: 4px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #6366f1;
                    color: white;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <div class="header">
                <h1>🌟 Culture Transformation Report</h1>
                <p>Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            </div>
            
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-value">{overall_score:.1f}</div>
                        <div class="metric-label">Overall Health Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(survey_data)}</div>
                        <div class="metric-label">Survey Responses</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(dimension_scores)}</div>
                        <div class="metric-label">Dimensions Analyzed</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(assessment.get('risk_factors', []))}</div>
                        <div class="metric-label">Risk Factors</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Culture Health Score</h2>
                <div id="gauge-chart"></div>
                <script>
                    var gaugeData = {gauge_fig.to_json()};
                    Plotly.newPlot('gauge-chart', gaugeData.data, gaugeData.layout);
                </script>
            </div>
            
            <div class="section">
                <h2>🎯 Culture Dimensions</h2>
                <div id="radar-chart"></div>
                <script>
                    var radarData = {radar_fig.to_json()};
                    Plotly.newPlot('radar-chart', radarData.data, radarData.layout);
                </script>
                
                <h3>Dimension Scores</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Dimension</th>
                            <th>Score</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add dimension scores table
        for dim, score in sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True):
            status = "✅ Strong" if score >= 7.5 else "⚠️ Needs Work" if score >= 6 else "❌ Critical"
            html_content += f"""
                        <tr>
                            <td>{dim.replace('_', ' ').title()}</td>
                            <td>{score:.2f}/10</td>
                            <td>{status}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>⚠️ Risk Factors</h2>
        """
        
        risks = assessment.get("risk_factors", [])
        if risks:
            for risk in risks:
                html_content += f'<div class="recommendation">⚠️ {risk}</div>'
        else:
            html_content += '<p>No significant risk factors identified.</p>'
        
        html_content += """
            </div>
            
            <div class="section">
                <h2>💡 Recommendations</h2>
        """
        
        recommendations = assessment.get("recommended_interventions", [])
        if recommendations:
            for rec in recommendations:
                html_content += f'<div class="recommendation">💡 {rec}</div>'
        else:
            html_content += '<p>No specific recommendations at this time.</p>'
        
        html_content += """
            </div>
        """
        
        # Add transformation plan if available
        if plan:
            html_content += """
            <div class="section">
                <h2>🎯 Transformation Plan</h2>
            """
            
            phases = plan.get("phases", {})
            for phase_name, initiatives in phases.items():
                html_content += f"<h3>{phase_name.replace('_', ' ').title()}</h3><ul>"
                if isinstance(initiatives, list):
                    for initiative in initiatives:
                        html_content += f"<li>{initiative}</li>"
                html_content += "</ul>"
            
            html_content += """
            </div>
            """
        
        html_content += f"""
            <div class="footer">
                <p>Culture Transformation Report | Generated by HR AI Lab</p>
                <p>Report ID: {timestamp}</p>
            </div>
        </body>
        </html>
        """
        
        # Save report
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return str(report_path)
    
    def _calculate_dimension_averages(self, survey_data: List[Dict]) -> Dict[str, float]:
        """Calculate average scores for each dimension."""
        dimension_scores = {}
        
        for response in survey_data:
            ratings = response.get("ratings", {})
            for dimension, data in ratings.items():
                if dimension not in dimension_scores:
                    dimension_scores[dimension] = []
                dimension_scores[dimension].append(data.get("score", 0))
        
        return {
            dim: np.mean(scores)
            for dim, scores in dimension_scores.items()
        }


if __name__ == "__main__":
    # Example usage
    from experiments.culture_transformation_coach.generate_culture_data import CultureDataGenerator
    
    generator = CultureDataGenerator()
    viz_gen = CultureVisualizationGenerator()
    
    # Generate sample data
    survey_data = generator.generate_survey_responses(num_responses=100)
    
    assessment = {
        "overall_health_score": 72.5,
        "risk_factors": [
            "Leadership communication gaps",
            "Limited career development paths"
        ],
        "recommended_interventions": [
            "Implement quarterly town halls",
            "Launch career development framework"
        ]
    }
    
    # Generate report
    report_path = viz_gen.generate_comprehensive_report(survey_data, assessment)
    print(f"Report generated: {report_path}")
