"""
CV Screening Results Dashboard

Interactive dashboard for visualizing and analyzing CV screening results.
Provides insights into candidate rankings, score distributions, and matching analysis.
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
    page_title="CV Screening Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .candidate-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .score-high {
        color: #28a745;
        font-weight: bold;
    }
    .score-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .score-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_screening_results(results_path: str) -> Optional[Dict[str, Any]]:
    """Load screening results from JSON file."""
    try:
        with open(results_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading results: {e}")
        return None


@st.cache_data
def load_metrics(metrics_path: str) -> Optional[Dict[str, Any]]:
    """Load metrics from JSON file."""
    try:
        with open(metrics_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading metrics: {e}")
        return None


def get_available_results() -> List[Path]:
    """Get list of available result files."""
    results_dir = Path("results/cv_screening")
    if not results_dir.exists():
        return []
    return sorted(results_dir.glob("screening_results_*.json"), reverse=True)


def create_candidate_dataframe(results: List[Dict]) -> pd.DataFrame:
    """Convert screening results to DataFrame."""
    data = []
    for result in results:
        matching = result.get('matching', {})
        qualifications = result.get('qualifications', {})
        
        data.append({
            'name': result.get('candidate_name', 'Unknown'),
            'score': matching.get('overall_score', 0),
            'recommendation': matching.get('recommendation', 'Unknown'),
            'interview': matching.get('interview_recommendation', False),
            'experience_years': qualifications.get('total_years_experience', 0),
            'education': qualifications.get('education_level', 'Unknown'),
            'technical_skills_count': len(qualifications.get('technical_skills', [])),
            'certifications_count': len(qualifications.get('relevant_certifications', [])),
        })
    
    return pd.DataFrame(data)


def plot_score_distribution(df: pd.DataFrame):
    """Plot score distribution histogram."""
    fig = px.histogram(
        df, 
        x='score',
        nbins=20,
        title='Score Distribution',
        labels={'score': 'Overall Score', 'count': 'Number of Candidates'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Overall Score (0-100)",
        yaxis_title="Number of Candidates"
    )
    return fig


def plot_recommendation_breakdown(df: pd.DataFrame):
    """Plot recommendation category breakdown."""
    recommendation_counts = df['recommendation'].value_counts()
    
    colors = {
        'Strong Match': '#28a745',
        'Good Match': '#17a2b8',
        'Possible Match': '#ffc107',
        'Weak Match': '#dc3545',
        'Error': '#6c757d'
    }
    
    fig = go.Figure(data=[
        go.Pie(
            labels=recommendation_counts.index,
            values=recommendation_counts.values,
            marker=dict(colors=[colors.get(cat, '#999') for cat in recommendation_counts.index]),
            hole=0.4
        )
    ])
    
    fig.update_layout(
        title='Recommendation Breakdown',
        showlegend=True
    )
    
    return fig


def plot_score_vs_experience(df: pd.DataFrame):
    """Plot score vs experience scatter plot."""
    fig = px.scatter(
        df,
        x='experience_years',
        y='score',
        color='recommendation',
        size='technical_skills_count',
        hover_data=['name', 'education'],
        title='Score vs Experience',
        labels={
            'experience_years': 'Years of Experience',
            'score': 'Overall Score',
            'technical_skills_count': 'Technical Skills'
        },
        color_discrete_map={
            'Strong Match': '#28a745',
            'Good Match': '#17a2b8',
            'Possible Match': '#ffc107',
            'Weak Match': '#dc3545'
        }
    )
    
    fig.update_layout(
        xaxis_title="Years of Experience",
        yaxis_title="Overall Score (0-100)"
    )
    
    return fig


def plot_skills_analysis(results: List[Dict]):
    """Plot skills distribution across candidates."""
    all_skills = []
    
    for result in results:
        qualifications = result.get('qualifications', {})
        skills = qualifications.get('technical_skills', [])
        all_skills.extend(skills)
    
    # Count skill frequency
    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = dict(skill_counts.most_common(15))
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(top_skills.values()),
            y=list(top_skills.keys()),
            orientation='h',
            marker=dict(color='#1f77b4')
        )
    ])
    
    fig.update_layout(
        title='Top 15 Technical Skills',
        xaxis_title='Number of Candidates',
        yaxis_title='Skill',
        height=500
    )
    
    return fig


def display_candidate_details(result: Dict):
    """Display detailed candidate information."""
    matching = result.get('matching', {})
    qualifications = result.get('qualifications', {})
    
    # Header
    name = result.get('candidate_name', 'Unknown')
    score = matching.get('overall_score', 0)
    recommendation = matching.get('recommendation', 'Unknown')
    
    # Score color
    if score >= 75:
        score_class = 'score-high'
    elif score >= 50:
        score_class = 'score-medium'
    else:
        score_class = 'score-low'
    
    st.markdown(f"""
    <div class="candidate-card">
        <h3>{name}</h3>
        <p><strong>Overall Score:</strong> <span class="{score_class}">{score}/100</span></p>
        <p><strong>Recommendation:</strong> {recommendation}</p>
        <p><strong>Interview Recommended:</strong> {'✅ Yes' if matching.get('interview_recommendation', False) else '❌ No'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Qualifications
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Experience", f"{qualifications.get('total_years_experience', 0)} years")
        st.metric("Education", qualifications.get('education_level', 'Unknown'))
    
    with col2:
        st.metric("Technical Skills", len(qualifications.get('technical_skills', [])))
        st.metric("Certifications", len(qualifications.get('relevant_certifications', [])))
    
    with col3:
        st.metric("Leadership Exp.", f"{qualifications.get('leadership_experience', 0)} years")
        st.metric("Domain Expertise", len(qualifications.get('domain_expertise', [])))
    
    # Detailed sections
    with st.expander("🎯 Strengths"):
        strengths = matching.get('strengths', [])
        if strengths:
            for strength in strengths:
                st.markdown(f"- {strength}")
        else:
            st.info("No strengths recorded")
    
    with st.expander("⚠️ Gaps"):
        gaps = matching.get('gaps', [])
        if gaps:
            for gap in gaps:
                st.markdown(f"- {gap}")
        else:
            st.info("No gaps recorded")
    
    with st.expander("💡 Reasoning"):
        st.write(matching.get('reasoning', 'No reasoning provided'))
    
    with st.expander("❓ Interview Questions"):
        questions = matching.get('key_questions', [])
        if questions:
            for i, question in enumerate(questions, 1):
                st.markdown(f"{i}. {question}")
        else:
            st.info("No questions provided")
    
    with st.expander("📋 Technical Skills"):
        skills = qualifications.get('technical_skills', [])
        if skills:
            st.write(", ".join(skills))
        else:
            st.info("No technical skills listed")


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 CV Screening Results Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    
    # Load available results
    available_results = get_available_results()
    
    if not available_results:
        st.error("No screening results found. Please run the CV screening experiment first.")
        st.info("Run: `python3 experiments/recruitment_cv_screening/cv_screener.py`")
        return
    
    # Select result file
    result_files = [f.name for f in available_results]
    selected_file = st.sidebar.selectbox(
        "Select Results File",
        result_files,
        help="Choose which screening results to display"
    )
    
    # Load data
    results_path = Path("results/cv_screening") / selected_file
    metrics_path = results_path.parent / selected_file.replace("screening_results_", "screening_metrics_")
    
    with st.spinner("Loading data..."):
        results_data = load_screening_results(str(results_path))
        metrics_data = load_metrics(str(metrics_path))
    
    if not results_data:
        st.error("Failed to load results data")
        return
    
    # Create DataFrame
    df = create_candidate_dataframe(results_data)
    
    # Metrics Overview
    st.header("📈 Overview Metrics")
    
    if metrics_data:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Candidates", metrics_data.get('total_candidates', 0))
        
        with col2:
            avg_score = metrics_data.get('average_score', 0)
            st.metric("Average Score", f"{avg_score:.1f}")
        
        with col3:
            st.metric("Strong Matches", metrics_data.get('strong_matches', 0))
        
        with col4:
            st.metric("Interview Ready", metrics_data.get('interview_recommended', 0))
        
        with col5:
            max_score = metrics_data.get('max_score', 0)
            st.metric("Highest Score", f"{max_score}")
    
    st.divider()
    
    # Visualizations
    st.header("📊 Analytics & Insights")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Detailed Analysis", "Skills Analysis", "Candidate Details"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_score_distribution(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_recommendation_breakdown(df), use_container_width=True)
        
        st.plotly_chart(plot_score_vs_experience(df), use_container_width=True)
    
    with tab2:
        st.subheader("Candidate Rankings")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_score = st.slider("Minimum Score", 0, 100, 0)
        
        with col2:
            rec_filter = st.multiselect(
                "Recommendation Type",
                options=df['recommendation'].unique(),
                default=df['recommendation'].unique()
            )
        
        with col3:
            interview_filter = st.selectbox(
                "Interview Recommendation",
                ["All", "Yes", "No"]
            )
        
        # Apply filters
        filtered_df = df[df['score'] >= min_score]
        filtered_df = filtered_df[filtered_df['recommendation'].isin(rec_filter)]
        
        if interview_filter == "Yes":
            filtered_df = filtered_df[filtered_df['interview'] == True]
        elif interview_filter == "No":
            filtered_df = filtered_df[filtered_df['interview'] == False]
        
        # Display table
        st.dataframe(
            filtered_df.sort_values('score', ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "name": "Candidate Name",
                "score": st.column_config.ProgressColumn(
                    "Score",
                    format="%d",
                    min_value=0,
                    max_value=100,
                ),
                "recommendation": "Recommendation",
                "interview": st.column_config.CheckboxColumn("Interview"),
                "experience_years": "Experience (years)",
                "education": "Education",
                "technical_skills_count": "Technical Skills",
                "certifications_count": "Certifications"
            }
        )
        
        # Export option
        if st.button("📥 Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"cv_screening_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with tab3:
        st.plotly_chart(plot_skills_analysis(results_data), use_container_width=True)
        
        # Additional skills insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Education Distribution")
            education_dist = df['education'].value_counts()
            fig = px.bar(
                x=education_dist.values,
                y=education_dist.index,
                orientation='h',
                labels={'x': 'Count', 'y': 'Education Level'},
                color_discrete_sequence=['#17a2b8']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Experience Distribution")
            fig = px.histogram(
                df,
                x='experience_years',
                nbins=10,
                labels={'experience_years': 'Years of Experience'},
                color_discrete_sequence=['#28a745']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Individual Candidate Analysis")
        
        # Select candidate
        candidate_names = [r['candidate_name'] for r in results_data]
        selected_candidate = st.selectbox("Select Candidate", candidate_names)
        
        # Find and display candidate details
        candidate_result = next(
            (r for r in results_data if r['candidate_name'] == selected_candidate),
            None
        )
        
        if candidate_result:
            display_candidate_details(candidate_result)
    
    # Footer
    st.divider()
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("Powered by Google Gemini 2.5 Flash-Lite • HR AI Lab Dashboard")


if __name__ == "__main__":
    main()
