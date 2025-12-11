"""
Career Pathway Recommender Dashboard

Interactive Streamlit dashboard for visualizing career pathway recommendations,
analyzing skill gaps, tracking development plans, and exploring career progression patterns.
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
    page_title="Career Pathway Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .employee-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .recommendation-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 3px solid #28a745;
        margin-bottom: 0.75rem;
    }
    .score-excellent {
        color: #28a745;
        font-weight: bold;
    }
    .score-good {
        color: #17a2b8;
        font-weight: bold;
    }
    .score-fair {
        color: #ffc107;
        font-weight: bold;
    }
    .skill-badge {
        display: inline-block;
        background-color: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        margin: 0.25rem;
        font-size: 0.85rem;
    }
    .plan-section {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 2rem;
    }
</style>
""", unsafe_allow_html=True)


def get_all_recommendations(rec: Dict) -> List[Dict]:
    """
    Extract all recommendations from a recommendation object.
    Handles both old format (list) and new format (dict with eligible_now/future_opportunities).
    """
    recs = rec.get('recommendations', [])
    
    # If it's already a list, return it
    if isinstance(recs, list):
        return recs
    
    # If it's a dict with the new structure, combine both lists
    if isinstance(recs, dict):
        all_recs = []
        all_recs.extend(recs.get('eligible_now', []))
        all_recs.extend(recs.get('future_opportunities', []))
        return all_recs
    
    return []


def load_career_pathway_results(results_dir: Path) -> List[Dict[str, Any]]:
    """Load career pathway recommendation results."""
    results = []
    
    for file in results_dir.glob('recommendations_*.json'):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                if 'recommendations' in data:
                    results.append({
                        'file': file.name,
                        'timestamp': file.name.split('_')[1] + '_' + file.name.split('_')[2].replace('.json', ''),
                        'data': data
                    })
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")
    
    return sorted(results, key=lambda x: x['timestamp'], reverse=True)


def format_similarity_score(score: float) -> str:
    """Format similarity score with color coding."""
    percentage = score * 100
    if score >= 0.8:
        return f'<span class="score-excellent">{percentage:.1f}%</span>'
    elif score >= 0.7:
        return f'<span class="score-good">{percentage:.1f}%</span>'
    else:
        return f'<span class="score-fair">{percentage:.1f}%</span>'


def create_overview_metrics(data: Dict[str, Any]) -> None:
    """Display overview metrics."""
    recommendations = data.get('recommendations', [])
    metrics_data = data.get('metrics', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Employees",
            metrics_data.get('total_employees', len(recommendations)),
            help="Number of employees analyzed"
        )
    
    with col2:
        success_rate = metrics_data.get('success_rate', 0) * 100
        st.metric(
            "Success Rate",
            f"{success_rate:.1f}%",
            help="Percentage of successful recommendations"
        )
    
    with col3:
        avg_score = metrics_data.get('average_similarity_score', 0) * 100
        st.metric(
            "Avg Match Score",
            f"{avg_score:.1f}%",
            help="Average similarity score across all recommendations"
        )
    
    with col4:
        st.metric(
            "Unique Roles",
            metrics_data.get('unique_roles_recommended', 0),
            help="Number of distinct roles recommended"
        )


def create_similarity_distribution(recommendations: List[Dict]) -> go.Figure:
    """Create similarity score distribution chart."""
    scores = []
    employee_names = []
    
    for rec in recommendations:
        for item in get_all_recommendations(rec):
            scores.append(item['similarity_score'] * 100)
            employee_names.append(rec['employee_name'])
    
    if not scores:
        return None
    
    fig = go.Figure()
    
    # Histogram
    fig.add_trace(go.Histogram(
        x=scores,
        nbinsx=20,
        name='Distribution',
        marker_color='rgba(102, 126, 234, 0.7)',
        hovertemplate='Score Range: %{x}<br>Count: %{y}<extra></extra>'
    ))
    
    # Add mean line
    mean_score = np.mean(scores)
    fig.add_vline(
        x=mean_score,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_score:.1f}%",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="Match Score Distribution",
        xaxis_title="Match Score (%)",
        yaxis_title="Frequency",
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig


def create_role_popularity_chart(recommendations: List[Dict]) -> go.Figure:
    """Create chart showing most recommended roles."""
    role_counts = {}
    
    for rec in recommendations:
        for item in get_all_recommendations(rec):
            role_title = item['role']['title']
            role_counts[role_title] = role_counts.get(role_title, 0) + 1
    
    if not role_counts:
        return None
    
    # Sort by count
    sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    roles, counts = zip(*sorted_roles)
    
    fig = go.Figure(go.Bar(
        y=roles,
        x=counts,
        orientation='h',
        marker_color='rgba(118, 75, 162, 0.7)',
        hovertemplate='%{y}<br>Count: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Top 10 Most Recommended Roles",
        xaxis_title="Number of Recommendations",
        yaxis_title="Role Title",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_job_family_breakdown(recommendations: List[Dict]) -> go.Figure:
    """Create pie chart of recommendations by job family."""
    family_counts = {}
    
    for rec in recommendations:
        for item in get_all_recommendations(rec):
            family = item['role']['job_family']
            family_counts[family] = family_counts.get(family, 0) + 1
    
    if not family_counts:
        return None
    
    fig = go.Figure(go.Pie(
        labels=list(family_counts.keys()),
        values=list(family_counts.values()),
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3,
        hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Recommendations by Job Family",
        height=400
    )
    
    return fig


def create_experience_level_chart(recommendations: List[Dict]) -> go.Figure:
    """Create chart showing experience level distribution."""
    current_exp = []
    recommended_exp = []
    employee_names = []
    
    for rec in recommendations:
        for item in get_all_recommendations(rec):
            # Parse years experience
            years_req = item['role']['years_experience']
            try:
                if '-' in years_req:
                    min_years, max_years = map(int, years_req.split('-'))
                    avg_years = (min_years + max_years) / 2
                elif '+' in years_req:
                    avg_years = int(years_req.replace('+', ''))
                else:
                    avg_years = int(years_req)
                
                recommended_exp.append(avg_years)
                # Note: We don't have current experience in this structure
                # Would need to enhance data structure
            except:
                continue
    
    if not recommended_exp:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=recommended_exp,
        nbinsx=10,
        name='Recommended Roles',
        marker_color='rgba(102, 126, 234, 0.7)',
        opacity=0.7
    ))
    
    fig.update_layout(
        title="Experience Level Distribution of Recommended Roles",
        xaxis_title="Years of Experience Required",
        yaxis_title="Count",
        height=400,
        barmode='overlay'
    )
    
    return fig


def create_skill_gap_analysis(recommendations: List[Dict]) -> pd.DataFrame:
    """Analyze common skill gaps."""
    skill_counts = {}
    
    for rec in recommendations:
        for item in get_all_recommendations(rec):
            for skill in item['role']['required_skills']:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    if not skill_counts:
        return None
    
    df = pd.DataFrame([
        {'Skill': skill, 'Frequency': count}
        for skill, count in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    ])
    
    return df


def display_employee_recommendations(employee_data: Dict[str, Any]) -> None:
    """Display detailed recommendations for a single employee."""
    st.markdown(f"""
    <div class="employee-card">
        <h3>👤 {employee_data['employee_name']}</h3>
        <p><strong>Employee ID:</strong> {employee_data['employee_id']}</p>
        <p><strong>Current Title:</strong> {employee_data['current_title']}</p>
        <p><strong>Recommendations Found:</strong> {len(employee_data.get('recommendations', []))}</p>
    </div>
    """, unsafe_allow_html=True)
    
    recommendations = employee_data.get('recommendations', [])
    
    if not recommendations:
        st.warning("No recommendations available for this employee.")
        return
    
    for idx, rec in enumerate(recommendations, 1):
        role = rec['role']
        
        with st.expander(f"🎯 Recommendation {idx}: {role['title']} - {role['job_family']}", expanded=(idx == 1)):
            # Match Score
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown(f"**Match Score:** {format_similarity_score(rec['similarity_score'])}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Experience Required:** {role['years_experience']} years")
            with col3:
                st.markdown(f"**Level:** {role['level']}")
            
            # Salary Range
            st.markdown(f"**💰 Salary Range:** {role['salary_range']}")
            
            # Key Responsibilities
            st.markdown("**📋 Key Responsibilities:**")
            for resp in role['responsibilities'][:3]:
                st.markdown(f"- {resp}")
            
            # Required Skills
            st.markdown("**🔧 Required Skills:**")
            skills_html = ''.join([f'<span class="skill-badge">{skill}</span>' for skill in role['required_skills'][:6]])
            st.markdown(skills_html, unsafe_allow_html=True)
            
            # Explanation
            st.markdown("**💡 Why This Role?**")
            st.info(rec['explanation'][:500] + "..." if len(rec['explanation']) > 500 else rec['explanation'])
            
            # Development Plan
            st.markdown("**📈 90-Day Development Plan**")
            plan = rec.get('development_plan', {})
            
            tabs = st.tabs(["Month 1", "Month 2", "Month 3"])
            
            for i, (tab, month_key) in enumerate(zip(tabs, ['month_1', 'month_2', 'month_3'])):
                with tab:
                    if month_key in plan:
                        month_data = plan[month_key]
                        
                        st.markdown(f"**Focus:** {month_data.get('focus', 'N/A')}")
                        
                        if 'objectives' in month_data:
                            st.markdown("**Objectives:**")
                            for obj in month_data['objectives']:
                                st.markdown(f"- {obj}")
                        
                        if 'activities' in month_data:
                            st.markdown("**Activities:**")
                            for activity in month_data['activities'][:3]:
                                st.markdown(f"- {activity}")
                        
                        if 'success_metrics' in month_data:
                            st.markdown("**Success Metrics:**")
                            for metric in month_data['success_metrics']:
                                st.markdown(f"✓ {metric}")
            
            if 'total_estimated_hours' in plan:
                st.markdown(f"**⏱️ Total Estimated Hours:** {plan['total_estimated_hours']}")


def create_career_pathway_network(recommendations: List[Dict]) -> go.Figure:
    """Create network visualization of career pathways."""
    # Build edges between current roles and recommended roles
    edges = []
    edge_counts = {}
    
    for rec in recommendations:
        current = rec.get('current_title', 'Unknown')
        for item in get_all_recommendations(rec):
            recommended = item['role']['title']
            edge_key = (current, recommended)
            edge_counts[edge_key] = edge_counts.get(edge_key, 0) + 1
    
    if not edge_counts:
        return None
    
    # Get unique nodes
    nodes = set()
    for (source, target) in edge_counts.keys():
        nodes.add(source)
        nodes.add(target)
    
    # Create node positions (circular layout)
    import math
    node_positions = {}
    nodes_list = list(nodes)
    n = len(nodes_list)
    
    for i, node in enumerate(nodes_list):
        angle = 2 * math.pi * i / n
        node_positions[node] = (math.cos(angle), math.sin(angle))
    
    # Create edge traces
    edge_traces = []
    for (source, target), count in edge_counts.items():
        x0, y0 = node_positions[source]
        x1, y1 = node_positions[target]
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=count * 2, color='rgba(125, 125, 125, 0.3)'),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_x = [node_positions[node][0] for node in nodes_list]
    node_y = [node_positions[node][1] for node in nodes_list]
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=nodes_list,
        textposition="top center",
        marker=dict(
            size=20,
            color='rgba(102, 126, 234, 0.8)',
            line=dict(width=2, color='white')
        ),
        hovertemplate='%{text}<extra></extra>',
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])
    
    fig.update_layout(
        title="Career Pathway Network",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600
    )
    
    return fig


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Career Pathway Recommender Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📁 Data Selection")
    
    # Load results - handle different execution contexts
    # Try multiple path resolution strategies
    possible_paths = [
        Path(__file__).parent.parent / 'career_pathway',  # Relative to script
        Path.cwd() / 'results' / 'career_pathway',  # From project root
        Path(__file__).resolve().parent.parent / 'career_pathway',  # Absolute resolution
    ]
    
    results_dir = None
    for path in possible_paths:
        if path.exists():
            results_dir = path
            break
    
    if results_dir is None:
        st.error("❌ Results directory not found")
        st.info("Searched in the following locations:")
        for path in possible_paths:
            st.code(str(path.absolute()))
        st.info("**To generate results, run:**")
        st.code("""
cd experiments/career_pathway_recommender
python run_career_pathway.py
        """)
        return
    
    # Show which path was used (for debugging)
    st.sidebar.info(f"📂 Using: `{results_dir.name}/`")
    
    results = load_career_pathway_results(results_dir)
    
    if not results:
        st.warning("No recommendation results found.")
        st.info("Run the experiment: `python run_career_pathway.py`")
        return
    
    # Select result file
    selected_result = st.sidebar.selectbox(
        "Select Results",
        options=range(len(results)),
        format_func=lambda i: f"{results[i]['timestamp']} ({results[i]['file']})"
    )
    
    data = results[selected_result]['data']
    recommendations = data.get('recommendations', [])
    
    # Display timestamp
    st.sidebar.markdown(f"**Generated:** {results[selected_result]['timestamp']}")
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.subheader("🔍 Filters")
    
    # Filter by minimum score
    min_score = st.sidebar.slider(
        "Minimum Match Score",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05,
        format="%.2f"
    )
    
    # Filter recommendations
    filtered_recommendations = []
    for rec in recommendations:
        all_recs = get_all_recommendations(rec)
        if not all_recs:
            continue
        
        filtered_recs = []
        for r in all_recs:
            # Handle case where r might not be a dict (data quality issue)
            if not isinstance(r, dict):
                st.warning(f"Skipping invalid recommendation data for {rec.get('employee_name', 'Unknown')}")
                continue
            if r.get('similarity_score', 0) >= min_score:
                filtered_recs.append(r)
        
        if filtered_recs:
            rec_copy = rec.copy()
            rec_copy['recommendations'] = filtered_recs
            filtered_recommendations.append(rec_copy)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 Employee Details", "📈 Analytics", "🔗 Career Pathways"])
    
    with tab1:
        st.header("Overview Metrics")
        create_overview_metrics(data)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_similarity_distribution(filtered_recommendations)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_job_family_breakdown(filtered_recommendations)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_role_popularity_chart(filtered_recommendations)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            fig = create_experience_level_chart(filtered_recommendations)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Employee Recommendations")
        
        if not filtered_recommendations:
            st.warning("No employees match the selected filters.")
        else:
            # Employee selector
            employee_names = [rec['employee_name'] for rec in filtered_recommendations]
            selected_employee = st.selectbox(
                "Select Employee",
                options=range(len(filtered_recommendations)),
                format_func=lambda i: f"{filtered_recommendations[i]['employee_name']} - {filtered_recommendations[i]['current_title']}"
            )
            
            st.markdown("---")
            
            # Display selected employee
            display_employee_recommendations(filtered_recommendations[selected_employee])
    
    with tab3:
        st.header("Advanced Analytics")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📚 Most In-Demand Skills")
            skill_df = create_skill_gap_analysis(filtered_recommendations)
            if skill_df is not None:
                fig = px.bar(
                    skill_df,
                    x='Frequency',
                    y='Skill',
                    orientation='h',
                    color='Frequency',
                    color_continuous_scale='Viridis',
                    height=500
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Summary Statistics")
            
            all_scores = []
            for rec in filtered_recommendations:
                for item in get_all_recommendations(rec):
                    all_scores.append(item['similarity_score'])
            
            if all_scores:
                st.metric("Mean Score", f"{np.mean(all_scores):.2%}")
                st.metric("Median Score", f"{np.median(all_scores):.2%}")
                st.metric("Std Dev", f"{np.std(all_scores):.2%}")
                st.metric("Total Recommendations", len(all_scores))
    
    with tab4:
        st.header("Career Pathway Network")
        st.markdown("Visualization of career transitions from current roles to recommended roles.")
        
        fig = create_career_pathway_network(filtered_recommendations)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to create network visualization.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Career Pathway Recommender Dashboard | HR AI Lab</p>
        <p>Powered by Google Gemini 2.5 Flash-Lite & sentence-transformers</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
