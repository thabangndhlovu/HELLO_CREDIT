import numpy as np
import pandas as pd


import streamlit as st


import matplotlib.pyplot as plt



st.title("Credit Default Assessor Dashboard 💳🔍📉")
st.write(
"""
The KMV model is a credit risk assessment tool that predicts the likelihood of a company defaulting on its debt. 
It calculates the distance to default by comparing the firm's asset value and volatility with its debt level, 
offering a market-based view of credit risk. 
This model is widely used for its accuracy in assessing default probabilities, 
making it a valuable tool for investors and financial analysts.
"""
)


ASSETS = pd.read_excel("resources/stock_universe_sectors.xlsx", index_col=0)
PRICES = pd.read_csv("resources/stock_prices.csv", index_col=0, parse_dates=True).resample("M").last()
DEFAULT_PROB = pd.read_excel("resources/stock_universe_default_prob.xlsx", index_col=0)
METRICS = pd.read_excel("resources/stock_universe_key_metrics.xlsx", index_col=0)

options = st.selectbox("Stock Selection", ASSETS.security_name)

SECURITY_CLASS = ASSETS.query(f"security_name == '{options}'")




data = METRICS[SECURITY_CLASS.security]

default_prob = DEFAULT_PROB.loc[SECURITY_CLASS.security].bb_1yr_default_prob[0]
default_grade = DEFAULT_PROB.loc[SECURITY_CLASS.security].rsk_bb_issuer_default[0]


# Top-level metrics
col1, col2, col3 = st.columns(3)
col2.metric(f"1Yr Default Prob", default_prob)
col1.metric(f"1Yr Default Grade", default_grade, "-" if "H" in default_grade else "+")
with col3:
    st.markdown(f"### {options}")


# Model Inputs Section
col1, col2 = st.columns(2)

with col2:
    st.write("Financial Metrics")
    st.table(METRICS[SECURITY_CLASS.security].dropna())

with col1:
    st.write("Share Price")
    st.line_chart(PRICES[SECURITY_CLASS.security].dropna())



# # Sector Comparison
st.header(f"Sector Comparison | {list(SECURITY_CLASS.industry_sector)[0]}")




import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Metrics for comparison
metrics = ['Profitability', 'Market Value', 'Leverage', 'Size', 'Liquidity']

# Generate random data to simulate sector range, median, weighted average, and BYIT (selected stock)
#np.random.seed(42)  # For reproducible random results
sector_range_start = np.random.uniform(low=10, high=50, size=len(metrics))
sector_range_end = sector_range_start + np.random.uniform(low=50, high=100, size=len(metrics))
median_values = np.random.uniform(low=sector_range_start, high=sector_range_end, size=len(metrics))
weighted_avg_values = np.random.uniform(low=sector_range_start, high=sector_range_end, size=len(metrics))
byit_values = np.random.uniform(low=sector_range_start, high=sector_range_end, size=len(metrics))

# Create the figure
fig = go.Figure()

# Add the sector range as lines
for i, metric in enumerate(metrics):
    fig.add_trace(go.Scatter(
        x=[sector_range_start[i], sector_range_end[i]],
        y=[metric, metric],
        mode='lines',
        line=dict(color='grey', width=2),
        showlegend=False
    ))

# Add median values as cyan dots
fig.add_trace(go.Scatter(
    x=median_values,
    y=metrics,
    mode='markers',
    marker=dict(color='cyan', size=10),
    name='Median'
))

# Add weighted average values as magenta diamonds
fig.add_trace(go.Scatter(
    x=weighted_avg_values,
    y=metrics,
    mode='markers',
    marker=dict(color='magenta', size=10, symbol='diamond'),
    name='Wtd Avg'
))

# Add BYIT values as orange dots
fig.add_trace(go.Scatter(
    x=byit_values,
    y=metrics,
    mode='markers',
    marker=dict(color='orange', size=10),
    name=list(SECURITY_CLASS.security)[0]
))

# Update the layout
fig.update_layout(
    xaxis=dict(title='Value'),
    yaxis=dict(title='', automargin=True),
    margin=dict(l=20, r=20, t=30, b=20),
)

# Display the figure in the Streamlit app

st.plotly_chart(fig, use_container_width=True)




np.random.seed()

# Metrics from the previous chart
metrics = ['Profitability', 'Market Value', 'Leverage', 'Size', 'Liquidity']

# Generate random data for the table
byit_values = np.random.uniform(low=0, high=100, size=len(metrics)).round(1)
tenth_percentile_values = np.random.uniform(low=-50, high=byit_values, size=len(metrics)).round(1)
ninetieth_percentile_values = np.random.uniform(low=byit_values, high=150, size=len(metrics)).round(1)

# Create a DataFrame
df = pd.DataFrame({
    'Credit Metric': metrics,
    list(SECURITY_CLASS.security)[0]: byit_values,
    '10 Pctl': tenth_percentile_values,
    '90 Pctl': ninetieth_percentile_values
})

# Set the 'Credit Metric' as the index for display purposes
df.set_index('Credit Metric', inplace=True)

# Display the DataFrame as a table in Streamlit

st.table(df)