"""
Culture Transformation Coach Dashboard

Interactive dashboard for visualizing culture analysis, health assessments,
and transformation plans.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Culture Transformation Dashboard",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #6366f1;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #6366f1;
    }
    .health-excellent {
        color: #10b981;
        font-weight: bold;
    }
    .health-good {
        color: #22c55e;
        font-weight: bold;
    }
    .health-fair {
        color: #eab308;
        font-weight: bold;
    }
    .health-poor {
        color: #ef4444;
        font-weight: bold;
    }
    .dimension-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .recommendation-box {
        background-color: #eff6ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 3px solid #3b82f6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


class CultureDashboard:
    """Dashboard for culture transformation insights."""
    
    CULTURE_DIMENSIONS = [
        "collaboration", "innovation", "accountability",
        "transparency", "work_life_balance", "leadership",
        "diversity_inclusion", "learning_development"
    ]
    
    def __init__(self):
        """Initialize dashboard."""
        self.results_dir = Path("../../results/culture_transformation")
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def load_results(self, file_path: str) -> Optional[Dict]:
        """Load results from JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading results: {e}")
            return None
    
    def get_health_status(self, score: float) -> tuple[str, str]:
        """Get health status label and color based on score."""
        if score >= 80:
            return "Excellent", "#10b981"
        elif score >= 70:
            return "Good", "#22c55e"
        elif score >= 60:
            return "Fair", "#eab308"
        else:
            return "Poor", "#ef4444"
    
    def render_header(self):
        """Render dashboard header."""
        st.markdown('<div class="main-header">🌟 Culture Transformation Dashboard</div>', 
                   unsafe_allow_html=True)
        st.markdown("---")
    
    def render_culture_health_overview(self, assessment: Dict):
        """Render overall culture health metrics."""
        st.subheader("📊 Culture Health Overview")
        
        # Extract overall score
        overall_score = assessment.get("overall_health_score", 0)
        if isinstance(overall_score, dict):
            overall_score = overall_score.get("score", 0)
        
        status, color = self.get_health_status(overall_score)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Overall Health Score",
                value=f"{overall_score:.1f}/100",
                delta=f"{status}"
            )
        
        with col2:
            retention = assessment.get("metrics", {}).get("retention_rate", 0.85) * 100
            st.metric(
                label="Retention Rate",
                value=f"{retention:.1f}%"
            )
        
        with col3:
            engagement = assessment.get("metrics", {}).get("employee_engagement", 7.2)
            st.metric(
                label="Engagement Score",
                value=f"{engagement:.1f}/10"
            )
        
        with col4:
            risk_count = len(assessment.get("risk_factors", []))
            st.metric(
                label="Risk Factors",
                value=risk_count,
                delta="Identified" if risk_count > 0 else "None"
            )
    
    def render_dimension_scores(self, survey_data: List[Dict]):
        """Render culture dimension scores chart."""
        st.subheader("📈 Culture Dimension Scores")
        
        # Calculate average scores per dimension
        dimension_scores = {}
        
        for response in survey_data:
            ratings = response.get("ratings", {})
            for dimension, data in ratings.items():
                if dimension not in dimension_scores:
                    dimension_scores[dimension] = []
                dimension_scores[dimension].append(data.get("score", 0))
        
        # Calculate averages
        avg_scores = {
            dim: np.mean(scores) 
            for dim, scores in dimension_scores.items()
        }
        
        # Create radar chart
        dimensions = list(avg_scores.keys())
        scores = list(avg_scores.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=[d.replace("_", " ").title() for d in dimensions],
            fill='toself',
            name='Current State',
            marker=dict(color='#6366f1')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            title="Culture Dimensions Radar Chart",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Top dimensions
            sorted_dims = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
            st.markdown("**🌟 Top Strengths**")
            for dim, score in sorted_dims[:3]:
                st.markdown(f"- **{dim.replace('_', ' ').title()}**: {score:.1f}/10")
        
        with col2:
            # Bottom dimensions
            st.markdown("**⚠️ Areas for Improvement**")
            for dim, score in sorted_dims[-3:]:
                st.markdown(f"- **{dim.replace('_', ' ').title()}**: {score:.1f}/10")
    
    def render_sentiment_distribution(self, survey_data: List[Dict]):
        """Render sentiment distribution across departments."""
        st.subheader("🏢 Sentiment by Department")
        
        # Extract department data
        dept_data = {}
        
        for response in survey_data:
            dept = response.get("department", "Unknown")
            ratings = response.get("ratings", {})
            
            if dept not in dept_data:
                dept_data[dept] = []
            
            # Calculate average score for this response
            scores = [r.get("score", 0) for r in ratings.values()]
            avg_score = np.mean(scores) if scores else 0
            dept_data[dept].append(avg_score)
        
        # Create dataframe
        dept_df = pd.DataFrame([
            {"Department": dept, "Average Score": np.mean(scores)}
            for dept, scores in dept_data.items()
        ])
        
        # Create bar chart
        fig = px.bar(
            dept_df,
            x="Department",
            y="Average Score",
            color="Average Score",
            color_continuous_scale="RdYlGn",
            title="Average Culture Score by Department"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_trend_analysis(self, historical_data: List[Dict]):
        """Render trend analysis over time."""
        st.subheader("📉 Trend Analysis")
        
        if not historical_data:
            st.info("No historical data available for trend analysis.")
            return
        
        # Create dataframe
        df = pd.DataFrame(historical_data)
        
        # Plot trends
        fig = px.line(
            df,
            x="month",
            y="employee_engagement",
            title="Employee Engagement Trend",
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Engagement Score",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_transformation_plan(self, plan: Dict):
        """Render transformation plan details."""
        st.subheader("🎯 Transformation Plan")
        
        # Executive summary
        if "executive_summary" in plan:
            st.markdown("**Executive Summary**")
            st.info(plan["executive_summary"])
        
        # Phases
        phases = plan.get("phases", {})
        if phases:
            tabs = st.tabs(["Short-term", "Medium-term", "Long-term"])
            
            phase_keys = ["short_term", "medium_term", "long_term"]
            
            for i, tab in enumerate(tabs):
                with tab:
                    phase_key = phase_keys[i]
                    initiatives = phases.get(phase_key, [])
                    
                    if isinstance(initiatives, list):
                        for initiative in initiatives:
                            st.markdown(f"- {initiative}")
                    elif isinstance(initiatives, dict):
                        for key, value in initiatives.items():
                            st.markdown(f"**{key}**: {value}")
        
        # Success metrics
        if "metrics" in plan or "success_metrics" in plan:
            st.markdown("---")
            st.markdown("**📊 Success Metrics**")
            metrics = plan.get("metrics", plan.get("success_metrics", []))
            
            if isinstance(metrics, list):
                for metric in metrics:
                    st.markdown(f"- {metric}")
            elif isinstance(metrics, dict):
                for key, value in metrics.items():
                    st.markdown(f"- **{key}**: {value}")
    
    def render_risk_factors(self, assessment: Dict):
        """Render identified risk factors."""
        st.subheader("⚠️ Risk Factors")
        
        risks = assessment.get("risk_factors", [])
        
        if not risks:
            st.success("No significant risk factors identified!")
            return
        
        for i, risk in enumerate(risks, 1):
            if isinstance(risk, str):
                st.warning(f"{i}. {risk}")
            elif isinstance(risk, dict):
                # Handle different dict structures - try multiple field names
                risk_title = risk.get('risk', risk.get('factor', risk.get('title', f'Risk {i}')))
                risk_desc = risk.get('description', risk.get('impact', risk.get('desc', '')))
                severity = risk.get('severity', '')
                
                # Build severity badge if present
                severity_html = ""
                if severity:
                    severity_color = {
                        'High': '#dc3545',
                        'Medium': '#ffc107', 
                        'Low': '#28a745'
                    }.get(severity, '#6c757d')
                    severity_html = f'<span style="background-color: {severity_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 0.25rem; font-size: 0.85rem; margin-left: 0.5rem;">{severity}</span>'
                
                # Use container with warning to ensure visibility
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107; margin-bottom: 0.5rem;">
                        <strong style="color: #856404;">{i}. {risk_title}</strong>{severity_html}<br>
                        <span style="color: #856404; margin-top: 0.5rem; display: block;">{risk_desc}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_recommendations(self, assessment: Dict):
        """Render recommendations."""
        st.subheader("💡 Recommendations")
        
        recommendations = assessment.get("recommended_interventions", 
                                        assessment.get("recommendations", []))
        
        if not recommendations:
            st.info("No specific recommendations available.")
            return
        
        for i, rec in enumerate(recommendations, 1):
            if isinstance(rec, str):
                st.markdown(f"""
                <div style="background-color: #eff6ff; padding: 1rem; border-radius: 0.5rem; border-left: 3px solid #3b82f6; margin-bottom: 0.5rem;">
                    <strong>{i}.</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
            elif isinstance(rec, dict):
                # Handle structured recommendations with dimension
                if "dimension" in rec and "recommendations" in rec:
                    dimension = rec.get("dimension", f"Area {i}")
                    sub_recs = rec.get("recommendations", [])
                    
                    # Display dimension header
                    st.markdown(f"<div style='margin-top: 0.5rem; margin-bottom: 0.5rem;'><strong>{i}. {dimension}</strong></div>", unsafe_allow_html=True)
                    
                    # Display each sub-recommendation
                    for j, sub_rec in enumerate(sub_recs, 1):
                        st.markdown(f"""
                        <div style="background-color: #eff6ff; padding: 0.8rem; border-radius: 0.5rem; border-left: 3px solid #3b82f6; margin: 0.3rem 0 0.3rem 1rem;">
                            <span style="color: #333;">{sub_rec}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Handle simple dict structure
                    title = rec.get("title", f"Recommendation {i}")
                    description = rec.get("description", "")
                    st.markdown(f"""
                    <div style="background-color: #eff6ff; padding: 1rem; border-radius: 0.5rem; border-left: 3px solid #3b82f6; margin-bottom: 0.5rem;">
                        <strong>{title}</strong><br>
                        <span style="color: #333;">{description}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_coaching_guidance(self, guidance: Dict):
        """Render coaching guidance."""
        st.subheader("🎓 Coaching Guidance")
        
        # Check if guidance is a dictionary of scenarios
        if isinstance(guidance, dict) and not any(key in guidance for key in ["analysis", "recommended_approaches", "scenario"]):
            # Multiple scenarios format (scenario name as key)
            for scenario_name, scenario_data in guidance.items():
                with st.expander(f"📋 {scenario_name}", expanded=True):
                    self._render_single_guidance(scenario_data)
        else:
            # Single guidance format
            self._render_single_guidance(guidance)
    
    def _render_single_guidance(self, guidance: Dict):
        """Render a single guidance scenario."""
        # Scenario description
        if "scenario" in guidance:
            st.markdown("**Scenario**")
            st.info(guidance["scenario"])
        
        # Context
        if "context" in guidance:
            st.markdown("**Context**")
            context = guidance["context"]
            if isinstance(context, dict):
                for key, value in context.items():
                    st.write(f"- **{key.replace('_', ' ').title()}**: {value}")
            else:
                st.write(context)
        
        # Analysis
        if "analysis" in guidance:
            st.markdown("**Cultural Implications**")
            analysis = guidance["analysis"]
            if isinstance(analysis, dict):
                if "cultural_implications" in analysis:
                    for implication in analysis["cultural_implications"]:
                        st.markdown(f"- {implication}")
                else:
                    st.write(analysis)
            else:
                st.write(analysis)
        
        # Approaches
        if "recommended_approaches" in guidance:
            st.markdown("**Recommended Approaches**")
            approaches = guidance["recommended_approaches"]
            if isinstance(approaches, list):
                for approach_item in approaches:
                    if isinstance(approach_item, dict):
                        approach_name = approach_item.get("approach", "Approach")
                        st.markdown(f"**{approach_name}**")
                        actions = approach_item.get("actions", [])
                        if isinstance(actions, list):
                            for action in actions:
                                st.markdown(f"  - {action}")
                        else:
                            st.write(f"  {actions}")
                    else:
                        st.markdown(f"- {approach_item}")
            else:
                st.write(approaches)
        
        # Challenges
        if "potential_challenges" in guidance:
            st.markdown("**Potential Challenges**")
            challenges = guidance["potential_challenges"]
            if isinstance(challenges, list):
                for challenge in challenges:
                    if isinstance(challenge, dict):
                        challenge_name = challenge.get("challenge", "")
                        description = challenge.get("description", "")
                        mitigation = challenge.get("mitigation", "")
                        st.markdown(f"- **{challenge_name}**: {description}")
                        if mitigation:
                            st.markdown(f"  - *Mitigation*: {mitigation}")
                    else:
                        st.markdown(f"- {challenge}")
            else:
                st.write(challenges)
        
        # Success metrics
        if "success_metrics" in guidance:
            st.markdown("**Success Metrics**")
            metrics = guidance["success_metrics"]
            if isinstance(metrics, list):
                for metric in metrics:
                    st.markdown(f"- {metric}")
            else:
                st.write(metrics)
        
        # Timeline
        if "timeline_expectations" in guidance:
            st.markdown("**Timeline Expectations**")
            timeline = guidance["timeline_expectations"]
            if isinstance(timeline, dict):
                for key, value in timeline.items():
                    st.markdown(f"- **{key}**: {value}")
            else:
                st.info(timeline)
    
    def export_results(self, data: Dict, filename: str):
        """Export results to JSON."""
        output_path = self.results_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(data, indent=2, fp=f)
        
        st.success(f"Results exported to {output_path}")
        
        # Download button
        st.download_button(
            label="Download Results",
            data=json.dumps(data, indent=2),
            file_name=filename,
            mime="application/json"
        )
    
    def run(self):
        """Run the dashboard."""
        self.render_header()
        
        # Sidebar
        st.sidebar.title("📂 Data Source")
        
        data_source = st.sidebar.radio(
            "Select data source:",
            ["Upload Files", "Use Sample Data", "Load from Results"]
        )
        
        survey_data = None
        assessment_data = None
        plan_data = None
        guidance_data = None
        
        if data_source == "Upload Files":
            st.sidebar.markdown("### Upload Data Files")
            
            survey_file = st.sidebar.file_uploader(
                "Survey Responses (JSON)",
                type=['json'],
                key="survey"
            )
            
            assessment_file = st.sidebar.file_uploader(
                "Health Assessment (JSON)",
                type=['json'],
                key="assessment"
            )
            
            plan_file = st.sidebar.file_uploader(
                "Transformation Plan (JSON)",
                type=['json'],
                key="plan"
            )
            
            guidance_file = st.sidebar.file_uploader(
                "Coaching Guidance (JSON)",
                type=['json'],
                key="guidance"
            )
            
            if survey_file:
                survey_data = json.load(survey_file)
            if assessment_file:
                assessment_data = json.load(assessment_file)
            if plan_file:
                plan_data = json.load(plan_file)
            if guidance_file:
                guidance_data = json.load(guidance_file)
        
        elif data_source == "Use Sample Data":
            # Generate sample data
            from experiments.culture_transformation_coach.generate_culture_data import CultureDataGenerator
            
            generator = CultureDataGenerator()
            survey_data = generator.generate_survey_responses(num_responses=100)
            
            assessment_data = {
                "overall_health_score": 72.5,
                "metrics": {
                    "employee_engagement": 7.2,
                    "retention_rate": 0.85,
                    "innovation_index": 6.5
                },
                "risk_factors": [
                    "Leadership communication gaps",
                    "Limited career development paths"
                ],
                "recommended_interventions": [
                    "Implement quarterly town halls",
                    "Launch career development framework"
                ]
            }
        
        elif data_source == "Load from Results":
            st.sidebar.markdown("### Select Results File")
            
            results_files = list(self.results_dir.glob("*.json"))
            
            if results_files:
                selected_file = st.sidebar.selectbox(
                    "Choose file:",
                    [f.name for f in results_files]
                )
                
                if selected_file:
                    file_path = self.results_dir / selected_file
                    data = self.load_results(file_path)
                    
                    if data:
                        st.sidebar.success(f"✓ Loaded: {selected_file}")
                        
                        # Check if it's a comprehensive experiment results file
                        if "experiment_results" in str(selected_file) or "survey_data" in data:
                            # This is a comprehensive results file
                            if "survey_data" in data:
                                survey_data = data["survey_data"].get("responses", [])
                            if "health_assessment" in data:
                                assessment_data = data["health_assessment"]
                            if "transformation_plan" in data:
                                plan_data = data["transformation_plan"]
                                # Handle double nesting if present
                                if isinstance(plan_data, dict) and "transformation_plan" in plan_data:
                                    plan_data = plan_data["transformation_plan"]
                            if "coaching_guidance" in data:
                                guidance_data = data["coaching_guidance"]
                        # Otherwise check individual file types
                        elif "survey" in str(selected_file) or "responses" in str(selected_file):
                            survey_data = data
                        elif "assessment" in str(selected_file) or "health" in str(selected_file):
                            assessment_data = data
                        elif "plan" in str(selected_file) or "transformation" in str(selected_file):
                            plan_data = data
                        elif "guidance" in str(selected_file) or "coaching" in str(selected_file):
                            guidance_data = data
                        
                        # Show what was loaded
                        loaded_items = []
                        if survey_data:
                            loaded_items.append("Survey Data")
                        if assessment_data:
                            loaded_items.append("Health Assessment")
                        if plan_data:
                            loaded_items.append("Transformation Plan")
                        if guidance_data:
                            loaded_items.append("Coaching Guidance")
                        
                        if loaded_items:
                            st.sidebar.info(f"📊 Loaded: {', '.join(loaded_items)}")
            else:
                st.sidebar.info("No results files found.")
        
        # Main content
        if survey_data or assessment_data:
            
            # Health overview
            if assessment_data:
                self.render_culture_health_overview(assessment_data)
                st.markdown("---")
            
            # Dimension scores
            if survey_data:
                self.render_dimension_scores(survey_data)
                st.markdown("---")
                
                self.render_sentiment_distribution(survey_data)
                st.markdown("---")
            
            # Transformation plan
            if plan_data:
                self.render_transformation_plan(plan_data)
                st.markdown("---")
            
            # Risk factors and recommendations
            if assessment_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    self.render_risk_factors(assessment_data)
                
                with col2:
                    self.render_recommendations(assessment_data)
                
                st.markdown("---")
            
            # Coaching guidance
            if guidance_data:
                self.render_coaching_guidance(guidance_data)
                st.markdown("---")
            
            # Export options
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 💾 Export")
            
            if st.sidebar.button("Export Dashboard Data"):
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "survey_data": survey_data,
                    "assessment": assessment_data,
                    "plan": plan_data,
                    "guidance": guidance_data
                }
                
                filename = f"culture_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.export_results(export_data, filename)
        
        else:
            st.info("👆 Please select a data source from the sidebar to view the dashboard.")


if __name__ == "__main__":
    dashboard = CultureDashboard()
    dashboard.run()
