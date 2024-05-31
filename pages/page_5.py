import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Sample Data
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
    'scores': {
        'leverage_coverage_metrics': 4.0,
        'efficiency_metrics': 5.1,
        'profitability_metrics': 5.1
    },
    'credit_score': 4.73,
    'credit_rating': 'Baa'
}

# Function to convert data to DataFrame
def get_metrics_df(data):
    metrics = data['metrics']
    df = pd.DataFrame(metrics).T
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'metric'}, inplace=True)
    return df

# Dashboard Overview
def dashboard_overview(data):
    st.title("Credit Model Dashboard")
    st.header("Overview")
    st.metric("Credit Score", data['credit_score'])
    st.metric("Credit Rating", data['credit_rating'])

    scores = data['scores']
    st.subheader("Category-wise Scores")
    for category, score in scores.items():
        st.write(f"**{category.replace('_', ' ').title()}:** {score}")

    # Pie Chart for Weighted Scores
    metrics_df = get_metrics_df(data)
    fig = px.pie(metrics_df, names='metric', values='weighted_score', title='Weighted Scores Distribution')
    st.plotly_chart(fig)

# Detailed Metrics
def detailed_metrics(data, category):
    st.header(f"{category.replace('_', ' ').title()} Metrics")
    metrics_df = get_metrics_df(data)
    category_metrics = metrics_df[metrics_df['category'] == category]

    st.dataframe(category_metrics)

    # Bar Chart for Metric Values
    fig = px.bar(category_metrics, x='metric', y='value', title=f"{category.replace('_', ' ').title()} Metrics")
    st.plotly_chart(fig)

    # Bar Chart for Scores
    fig = px.bar(category_metrics, x='metric', y='score', title=f"{category.replace('_', ' ').title()} Scores")
    st.plotly_chart(fig)

    # Bar Chart for Weighted Scores
    fig = px.bar(category_metrics, x='metric', y='weighted_score', title=f"{category.replace('_', ' ').title()} Weighted Scores")
    st.plotly_chart(fig)

    # Bar Chart for Ratings
    fig = px.bar(category_metrics, x='metric', y='rating', title=f"{category.replace('_', ' ').title()} Ratings", 
                 labels={'rating': 'Rating'}, color='rating')
    st.plotly_chart(fig)

    # Radar Chart for Scores
    fig = px.line_polar(category_metrics, r='score', theta='metric', line_close=True, title=f"{category.replace('_', ' ').title()} Scores Radar Chart")
    st.plotly_chart(fig)

# Additional Charts
def additional_charts(data):
    st.header("Additional Visualizations")

    # Heatmap for Scores
    metrics_df = get_metrics_df(data)
    heatmap_data = metrics_df.pivot_table(index='metric', columns='category', values='score').fillna(0)
    st.subheader("Heatmap of Scores")
    fig, ax = plt.subplots()
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

    # Correlation Matrix
    st.subheader("Correlation Matrix")
    correlation_data = metrics_df[['value', 'score', 'weighted_score']]
    correlation_matrix = correlation_data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Dashboard", "Leverage Coverage Metrics", "Efficiency Metrics", "Profitability Metrics", "Additional Charts"])

# Page Routing
if page == "Dashboard":
    dashboard_overview(data)
elif page == "Leverage Coverage Metrics":
    detailed_metrics(data, 'leverage_coverage_metrics')
elif page == "Efficiency Metrics":
    detailed_metrics(data, 'efficiency_metrics')
elif page == "Profitability Metrics":
    detailed_metrics(data, 'profitability_metrics')
elif page == "Additional Charts":
    additional_charts(data)
