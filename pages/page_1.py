import streamlit as st

# Initialize session state for page navigation and storing inputs
st.title("Page 1")

st.page_link("main.py", label="Home", icon="🏠")

import streamlit as st
import pandas as pd
import plotly.express as px


output = {'metrics': {'debt_to_equity': {'category': 'leverage_coverage_metrics',
   'value': 1.2,
   'score': 5,
   'weight': 0.2,
   'weighted_score': 1.0,
   'rating': 'Baa'},
  'debt_to_ebitda': {'category': 'leverage_coverage_metrics',
   'value': 3.5,
   'score': 5,
   'weight': 0.2,
   'weighted_score': 1.0,
   'rating': 'Baa'},
  'ebitda_to_interest_expense': {'category': 'leverage_coverage_metrics',
   'value': 8.0,
   'score': 4,
   'weight': 0.2,
   'weighted_score': 0.8,
   'rating': 'A'},
  'debt_to_tangible_assets': {'category': 'leverage_coverage_metrics',
   'value': 0.6,
   'score': 3,
   'weight': 0.4,
   'weighted_score': 1.2000000000000002,
   'rating': 'Aa'},
  'asset_turnover': {'category': 'efficiency_metrics',
   'value': 1.8,
   'score': 6,
   'weight': 0.4,
   'weighted_score': 2.4000000000000004,
   'rating': 'Ba'},
  'inventory_to_cost_of_sales': {'category': 'efficiency_metrics',
   'value': 0.4,
   'score': 4,
   'weight': 0.3,
   'weighted_score': 1.2,
   'rating': 'A'},
  'cash_to_assets': {'category': 'efficiency_metrics',
   'value': 0.2,
   'score': 5,
   'weight': 0.3,
   'weighted_score': 1.5,
   'rating': 'Baa'},
  'ebitda_margin': {'category': 'profitability_metrics',
   'value': 18.0,
   'score': 6,
   'weight': 0.4,
   'weighted_score': 2.4000000000000004,
   'rating': 'Ba'},
  'total_assets': {'category': 'profitability_metrics',
   'value': 50000000,
   'score': 3,
   'weight': 0.3,
   'weighted_score': 0.8999999999999999,
   'rating': 'Aa'},
  'sales_growth': {'category': 'profitability_metrics',
   'value': 12.0,
   'score': 6,
   'weight': 0.3,
   'weighted_score': 1.7999999999999998,
   'rating': 'Ba'}}}



# Add a title and introduction
st.title('Credit Risk Assessment Dashboard')
st.write('Welcome to the Credit Risk Assessment Dashboard! This app provides insights into various financial metrics and their impact on credit risk.')

# Assuming the output is stored in a variable called 'output'
metrics_data = output['metrics']

# Convert the metrics data to a DataFrame
metrics_df = pd.DataFrame.from_dict(metrics_data, orient='index')

# Display the metrics as a table
st.subheader('Metrics Table')
st.write('The following table provides a detailed view of the financial metrics and their corresponding scores, weights, and ratings.')
styled_table = metrics_df.style.background_gradient(cmap='RdYlGn', subset=['score', 'weighted_score'])
st.dataframe(styled_table)

# Create a bar chart for the weighted scores
st.subheader('Weighted Scores by Metric')
st.write('This bar chart visualizes the weighted scores for each financial metric, categorized by their respective categories.')
fig1 = px.bar(metrics_df, x=metrics_df.index, y='weighted_score', color='category',
              labels={'x': 'Metric', 'y': 'Weighted Score', 'category': 'Category'},
              title='Weighted Scores by Metric')
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1)

# Create a bar chart for the ratings
st.subheader('Scores and Ratings by Metric')
st.write('This bar chart displays the scores for each financial metric, with color-coding representing the assigned ratings.')
fig2 = px.bar(metrics_df, x=metrics_df.index, y='score', color='rating',
              labels={'x': 'Metric', 'y': 'Score', 'rating': 'Rating'},
              title='Scores and Ratings by Metric',
              color_discrete_sequence=px.colors.qualitative.Pastel)
fig2.update_layout(showlegend=True)
st.plotly_chart(fig2)

# Add a summary and conclusion
st.subheader('Summary')
st.write('Based on the analysis of the financial metrics, the key insights are:')
st.write('- The company has a strong performance in the Profitability and Efficiency categories.')
st.write('- The Leverage & Coverage metrics indicate a moderate risk profile.')
st.write('- The overall credit rating of the company is Baa, suggesting a moderate credit risk.')

st.subheader('Conclusion')
st.write('The Credit Risk Assessment Dashboard provides a comprehensive view of the company\'s financial health and creditworthiness. By considering various metrics across different categories, stakeholders can make informed decisions regarding credit risk management and investment strategies.')