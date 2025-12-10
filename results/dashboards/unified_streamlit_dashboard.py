"""
HR AI Lab - Interactive Streamlit Dashboard

An interactive, real-time dashboard for viewing and analyzing results from all HR AI Lab experiments.

Run with:
    streamlit run results/dashboards/unified_streamlit_dashboard.py
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import glob


# Page configuration
st.set_page_config(
    page_title="HR AI Lab Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_results():
    """Load all experiment results."""
    results_dir = Path(__file__).parent.parent
    
    data = {
        'cv_screening': load_experiment_results(results_dir / 'cv_screening', '*.json'),
        'bias_testing': load_experiment_results(results_dir / 'bias_testing', '*.json'),
        'hris_data_quality': load_experiment_results(results_dir / 'hris_data_quality', 'quality_report_*.json'),
        'interview_summarization': load_experiment_results(results_dir / 'interview_summarization', '*.json'),
        'culture_transformation': load_experiment_results(results_dir / 'culture_transformation', '*.json'),
    }
    
    return data


def load_experiment_results(results_path, pattern):
    """Load results for a specific experiment."""
    if not results_path.exists():
        return {'available': False, 'message': 'Directory not found'}
    
    json_files = list(results_path.glob(pattern))
    
    if not json_files:
        return {'available': False, 'message': 'No data files found'}
    
    # Load most recent file
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    
    try:
        with open(latest_file) as f:
            data = json.load(f)
        
        return {
            'available': True,
            'file': str(latest_file),
            'data': data,
            'timestamp': datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat(),
            'total_files': len(json_files)
        }
    except Exception as e:
        return {'available': False, 'message': f'Error: {e}'}


def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">🧪 HR AI Lab</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2em; color: #666; margin-bottom: 30px;">Unified Experiments Dashboard</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading experiment results...'):
        data = load_results()
    
    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "Data Quality", "Bias Testing", "CV Screening", "Interviews", "Culture", "Comparisons"]
    )
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Display timestamp
    st.sidebar.markdown("---")
    st.sidebar.info(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Route to appropriate page
    if page == "Overview":
        show_overview(data)
    elif page == "Data Quality":
        show_data_quality(data)
    elif page == "Bias Testing":
        show_bias_testing(data)
    elif page == "CV Screening":
        show_cv_screening(data)
    elif page == "Interviews":
        show_interviews(data)
    elif page == "Culture":
        show_culture(data)
    elif page == "Comparisons":
        show_comparisons(data)


def show_overview(data):
    """Display overview of all experiments."""
    
    st.header("📊 Experiments Overview")
    
    # Calculate metrics
    available_experiments = sum([
        1 if data['cv_screening'].get('available') else 0,
        1 if data['bias_testing'].get('available') else 0,
        1 if data['hris_data_quality'].get('available') else 0,
        1 if data['interview_summarization'].get('available') else 0,
        1 if data['culture_transformation'].get('available') else 0,
    ])
    
    total_experiments = 5
    completion_pct = (available_experiments / total_experiments) * 100
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Experiments Run", f"{available_experiments}/{total_experiments}", 
                 delta=f"{completion_pct:.0f}% Complete")
    
    with col2:
        if data['hris_data_quality'].get('available'):
            score = data['hris_data_quality']['data'].get('quality_score', 0)
            st.metric("Data Quality Score", f"{score:.1f}/100",
                     delta="Good" if score >= 75 else "Needs Improvement")
        else:
            st.metric("Data Quality Score", "N/A", delta="Not Run")
    
    with col3:
        bias_reports = data['bias_testing'].get('total_files', 0) if data['bias_testing'].get('available') else 0
        st.metric("Bias Reports", bias_reports,
                 delta="Active" if bias_reports > 0 else None)
    
    with col4:
        total_reports = sum([
            data['cv_screening'].get('total_files', 0),
            data['bias_testing'].get('total_files', 0),
            data['hris_data_quality'].get('total_files', 0),
            data['interview_summarization'].get('total_files', 0),
            data['culture_transformation'].get('total_files', 0),
        ])
        st.metric("Total Reports", total_reports)
    
    st.markdown("---")
    
    # Experiment status grid
    st.subheader("Experiment Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status table
        status_data = {
            'Experiment': [
                '📄 CV Screening',
                '⚖️ Bias Testing',
                '🔍 Data Quality',
                '🎙️ Interviews',
                '🌟 Culture'
            ],
            'Status': [
                '✅ Available' if data['cv_screening'].get('available') else '⏳ Pending',
                '✅ Available' if data['bias_testing'].get('available') else '⏳ Pending',
                '✅ Available' if data['hris_data_quality'].get('available') else '⏳ Pending',
                '✅ Available' if data['interview_summarization'].get('available') else '⏳ Pending',
                '✅ Available' if data['culture_transformation'].get('available') else '⏳ Pending',
            ],
            'Reports': [
                data['cv_screening'].get('total_files', 0),
                data['bias_testing'].get('total_files', 0),
                data['hris_data_quality'].get('total_files', 0),
                data['interview_summarization'].get('total_files', 0),
                data['culture_transformation'].get('total_files', 0),
            ]
        }
        
        df = pd.DataFrame(status_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with col2:
        # Completion pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'Pending'],
            values=[available_experiments, total_experiments - available_experiments],
            hole=0.4,
            marker=dict(colors=['#10b981', '#e5e7eb'])
        )])
        
        fig.update_layout(
            title="Experiment Completion",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)


def show_data_quality(data):
    """Display data quality experiment results."""
    
    st.header("🔍 HRIS Data Quality Analysis")
    
    if not data['hris_data_quality'].get('available'):
        st.warning("No data quality results available yet.")
        st.info("Run the HRIS Data Quality Agent to generate results.")
        return
    
    dq_data = data['hris_data_quality']['data']
    
    # Quality score
    score = dq_data.get('quality_score', 0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Quality Score", f"{score:.1f}/100")
        
        # Score gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Quality"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 60], 'color': "#fee2e2"},
                    {'range': [60, 75], 'color': "#fef3c7"},
                    {'range': [75, 90], 'color': "#dbeafe"},
                    {'range': [90, 100], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total Records", dq_data.get('total_records', 0))
        st.metric("Records with Issues", dq_data.get('records_with_issues', 0))
        st.metric("Total Issues Found", dq_data.get('total_issues', 0))
    
    with col3:
        issues_by_severity = dq_data.get('issues_by_severity', {})
        st.metric("🔴 Critical", issues_by_severity.get('critical', 0))
        st.metric("🟠 High", issues_by_severity.get('high', 0))
        st.metric("🟡 Medium", issues_by_severity.get('medium', 0))
        st.metric("🟢 Low", issues_by_severity.get('low', 0))
    
    st.markdown("---")
    
    # Issues breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Issues by Type")
        
        issues_by_type = dq_data.get('issues_by_type', {})
        
        if issues_by_type:
            df = pd.DataFrame({
                'Issue Type': [k.replace('_', ' ').title() for k in issues_by_type.keys()],
                'Count': list(issues_by_type.values())
            })
            
            fig = px.bar(df, x='Count', y='Issue Type', orientation='h',
                        color='Count', color_continuous_scale='Reds')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Severity Distribution")
        
        if issues_by_severity:
            fig = go.Figure(data=[go.Pie(
                labels=[k.title() for k in issues_by_severity.keys()],
                values=list(issues_by_severity.values()),
                marker=dict(colors=['#ef4444', '#f59e0b', '#fbbf24', '#10b981'])
            )])
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("📋 Recommendations")
    
    recommendations = dq_data.get('recommendations', [])
    
    for i, rec in enumerate(recommendations, 1):
        st.info(f"**{i}.** {rec}")
    
    # Summary
    with st.expander("📊 Executive Summary"):
        st.write(dq_data.get('summary', 'No summary available'))


def show_bias_testing(data):
    """Display bias testing results."""
    
    st.header("⚖️ Bias Testing Results")
    
    if not data['bias_testing'].get('available'):
        st.warning("No bias testing results available yet.")
        st.info("Run the Bias Testing Agent to generate results.")
        return
    
    bt_data = data['bias_testing']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("JSON Reports", bt_data.get('total_files', 0))
    
    with col2:
        st.metric("HTML Dashboards", len(list(Path(bt_data['file']).parent.glob('*.html'))))
    
    with col3:
        st.metric("Status", "✅ Active")
    
    st.success("Bias testing framework is operational. Regular testing recommended for all experiments.")
    
    st.info("💡 **Best Practice**: Run bias tests on all candidate screening and evaluation experiments to ensure fairness.")


def show_cv_screening(data):
    """Display CV screening results."""
    
    st.header("📄 CV Screening Results")
    
    if not data['cv_screening'].get('available'):
        st.warning("No CV screening results available yet.")
        st.info("Run the CV Screening experiment to generate results.")
        return
    
    st.success("CV screening pipeline is operational and ready for candidate evaluation.")


def show_interviews(data):
    """Display interview summarization results."""
    
    st.header("🎙️ Interview Summarization")
    
    if not data['interview_summarization'].get('available'):
        st.warning("No interview results available yet.")
        st.info("Run the Interview Summarization experiment to generate results.")
        return
    
    st.metric("Total Reports", data['interview_summarization'].get('total_files', 0))


def show_culture(data):
    """Display culture transformation results."""
    
    st.header("🌟 Culture Transformation")
    
    if not data['culture_transformation'].get('available'):
        st.warning("No culture transformation results available yet.")
        st.info("Run the Culture Transformation experiment to generate results.")
        return
    
    st.metric("Total Reports", data['culture_transformation'].get('total_files', 0))


def show_comparisons(data):
    """Display comparative analysis across experiments."""
    
    st.header("📊 Cross-Experiment Comparisons")
    
    # Experiment availability comparison
    st.subheader("Experiment Availability")
    
    availability_data = {
        'Experiment': [
            'CV Screening',
            'Bias Testing',
            'Data Quality',
            'Interviews',
            'Culture'
        ],
        'Available': [
            1 if data['cv_screening'].get('available') else 0,
            1 if data['bias_testing'].get('available') else 0,
            1 if data['hris_data_quality'].get('available') else 0,
            1 if data['interview_summarization'].get('available') else 0,
            1 if data['culture_transformation'].get('available') else 0,
        ],
        'Reports': [
            data['cv_screening'].get('total_files', 0),
            data['bias_testing'].get('total_files', 0),
            data['hris_data_quality'].get('total_files', 0),
            data['interview_summarization'].get('total_files', 0),
            data['culture_transformation'].get('total_files', 0),
        ]
    }
    
    df = pd.DataFrame(availability_data)
    
    fig = px.bar(df, x='Experiment', y='Reports', color='Available',
                 color_discrete_map={0: '#e5e7eb', 1: '#10b981'},
                 title="Reports Generated per Experiment")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Timeline (if multiple reports available)
    st.subheader("Activity Timeline")
    st.info("Timeline visualization will show experiment runs over time once multiple reports are generated.")


if __name__ == '__main__':
    main()
