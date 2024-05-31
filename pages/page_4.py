import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define the data
scores = {'leverage_coverage_metrics': 4.0, 'efficiency_metrics': 5.1, 'profitability_metrics': 5.1}
credit_score = 4.733333333333333
credit_rating = 'Baa'

# Set page title and favicon
st.set_page_config(page_title='Credit Model Dashboard', page_icon=':money_with_wings:')

# Display header
st.header('Credit Model Dashboard')

# Display overall credit score and rating
st.subheader('Overall Credit Assessment')
col1, col2 = st.columns(2)
col1.metric('Credit Score', f'{credit_score:.2f}')
col2.metric('Credit Rating', credit_rating)

# Display category scores
st.subheader('Category Scores')
categories = list(scores.keys())
values = list(scores.values())

fig = go.Figure(data=[go.Bar(x=categories, y=values)])
fig.update_layout(xaxis_title='Category', yaxis_title='Score')
st.plotly_chart(fig)

# Display detailed category breakdown
st.subheader('Detailed Category Breakdown')
breakdown_data = {
    'Category': ['Leverage & Coverage Metrics', 'Efficiency Metrics', 'Profitability Metrics'],
    'Score': [scores['leverage_coverage_metrics'], scores['efficiency_metrics'], scores['profitability_metrics']],
    'Metrics': [
        '- Debt to Equity Ratio: 1.5\n- Interest Coverage: 3.2',
        '- Asset Turnover: 1.8\n- Inventory Turnover: 4.2',
        '- Return on Assets: 8.5%\n- Gross Profit Margin: 35%'
    ]
}
breakdown_df = pd.DataFrame(breakdown_data)
st.table(breakdown_df)

# Display insights and analysis
st.subheader('Insights and Analysis')
st.markdown('''
- The overall credit score of 4.73 indicates a moderate credit risk, corresponding to a Baa rating.
- The company demonstrates strong efficiency metrics, with an asset turnover of 1.8 and inventory turnover of 4.2.
- Profitability metrics are also robust, with a return on assets of 8.5% and a gross profit margin of 35%.
- However, the leverage and coverage metrics show room for improvement, particularly in the debt to equity ratio.
- Recommendation: Consider strategies to reduce debt levels and improve the company's financial leverage position.
''')