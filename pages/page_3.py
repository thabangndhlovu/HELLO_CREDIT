import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define the data
data = {
    'metrics': {
        'debt_to_equity': {'category': 'leverage_coverage_metrics', 'value': 1.2, 'score': 5, 'weight': 0.2, 'weighted_score': 1.0, 'rating': 'Baa'},
        'debt_to_ebitda': {'category': 'leverage_coverage_metrics', 'value': 3.5, 'score': 5, 'weight': 0.2, 'weighted_score': 1.0, 'rating': 'Baa'},
        'ebitda_to_interest_expense': {'category': 'leverage_coverage_metrics', 'value': 8.0, 'score': 4, 'weight': 0.2, 'weighted_score': 0.8, 'rating': 'A'},
        'debt_to_tangible_assets': {'category': 'leverage_coverage_metrics', 'value': 0.6, 'score': 3, 'weight': 0.4, 'weighted_score': 1.2, 'rating': 'Aa'},
        'asset_turnover': {'category': 'efficiency_metrics', 'value': 1.8, 'score': 6, 'weight': 0.4, 'weighted_score': 2.4, 'rating': 'Ba'},
        'inventory_to_cost_of_sales': {'category': 'efficiency_metrics', 'value': 0.4, 'score': 4, 'weight': 0.3, 'weighted_score': 1.2, 'rating': 'A'},
        'cash_to_assets': {'category': 'efficiency_metrics', 'value': 0.2, 'score': 5, 'weight': 0.3, 'weighted_score': 1.5, 'rating': 'Baa'},
        'ebitda_margin': {'category': 'profitability_metrics', 'value': 18.0, 'score': 6, 'weight': 0.4, 'weighted_score': 2.4, 'rating': 'Ba'},
        'total_assets': {'category': 'profitability_metrics', 'value': 50000000, 'score': 3, 'weight': 0.3, 'weighted_score': 0.9, 'rating': 'Aa'},
        'sales_growth': {'category': 'profitability_metrics', 'value': 12.0, 'score': 6, 'weight': 0.3, 'weighted_score': 1.8, 'rating': 'Ba'}
    },
    'scores': {'leverage_coverage_metrics': 4.0, 'efficiency_metrics': 5.1, 'profitability_metrics': 5.1},
    'credit_score': 4.733333333333333,
    'credit_rating': 'Baa'
}

# Set page title and layout
st.set_page_config(page_title="Credit Analysis Dashboard", layout="wide")

# Display header and overall credit score
st.title("Credit Analysis Dashboard")
st.header(f"Overall Credit Score: {data['credit_score']:.2f} ({data['credit_rating']})")

# Create four columns for the main content
col1, col2, col3, col4 = st.columns(4)

# Display metrics table in the first column
with col1:
    st.subheader("Metrics Table")
    metrics_data = []
    for metric, values in data['metrics'].items():
        metrics_data.append([metric.replace('_', ' ').title(), values['value'], values['score'], values['rating']])
    metrics_df = pd.DataFrame(metrics_data, columns=['Metric', 'Value', 'Score', 'Rating'])
    st.dataframe(metrics_df, height=400)

# Display category scores in the second column
with col2:
    st.subheader("Category Scores")
    categories = list(data['scores'].keys())
    scores = list(data['scores'].values())
    fig = go.Figure(data=[go.Bar(x=categories, y=scores, text=scores, textposition='auto')])
    fig.update_layout(xaxis_title="Category", yaxis_title="Score", yaxis=dict(range=[0, 6]))
    st.plotly_chart(fig)

# Display weighted scores in the third column
with col3:
    st.subheader("Weighted Scores")
    weighted_scores_data = []
    for metric, values in data['metrics'].items():
        weighted_scores_data.append([metric.replace('_', ' ').title(), values['weighted_score']])
    weighted_scores_df = pd.DataFrame(weighted_scores_data, columns=['Metric', 'Weighted Score'])
    fig = go.Figure(data=[go.Pie(labels=weighted_scores_df['Metric'], values=weighted_scores_df['Weighted Score'], hole=0.4)])
    fig.update_layout(title="Weighted Scores Distribution")
    st.plotly_chart(fig)

# Display additional insights in the fourth column
with col4:
    st.subheader("Additional Insights")
    st.write("- The company has a moderate credit score of {:.2f}, indicating a '{}' credit rating.".format(data['credit_score'], data['credit_rating']))
    st.write("- The leverage & coverage metrics show a balanced debt profile, with room for improvement in the debt-to-tangible-assets ratio.")
    st.write("- Efficiency metrics highlight strong asset turnover, while inventory management could be optimized further.")
    st.write("- Profitability metrics demonstrate healthy EBITDA margin and sales growth, but the total assets score suggests potential for asset utilization improvements.")
    
# Display the radar chart at the bottom
st.subheader("Category Scores Radar Chart")
fig = go.Figure(data=go.Scatterpolar(
    r=scores,
    theta=categories,
    fill='toself'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 6]
        )),
    showlegend=False
)

st.plotly_chart(fig)