import numpy as np
import pandas as pd


import streamlit as st


import matplotlib.pyplot as plt

# Set up the page layout
#st.set_page_config(layout="wide")


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

stocks = ["AAPL", "GOOG", "MSFT", "GME", "TSLA"]
options = st.selectbox("Stock Selection", stocks)



# Load your data - replace with the path to your dataset
# data = pd.read_csv('your_dataset.csv')

# Sample data to illustrate - you would use your actual data here
data = {
    "Metric": ["Market Cap", "Share Price", "Price Vol (1Yr)", "Total Debt", "Adj CFO (T12M)", "Interest Expn (T12M)"],
    "Value": [12236.67, 25917.00, 88.2, 920, 2075.1, 53.8],
    "Units": ["MM", "ZAR", "%", "MM", "MM", "MM"]
}


# Top-level metrics
col1, col2, col3 = st.columns(3)
col1.metric("1Yr Default Grade", "IG5")
col2.metric("2Yr Default Prob", "0.0193%")
col3.metric("5Yr Model CDS", "269.9 bps")

# Model Inputs Section

col1, col2 = st.columns(2)

with col2:
    model_inputs = pd.DataFrame(data)
    st.table(model_inputs)

with col1:
    data = pd.DataFrame(np.random.randn(10, 2), columns=['a', 'b'])
    st.line_chart(data)

# Sector Comparison
st.header("Sector Comparison | DRAM")

# Replace these with actual data calculations
sector_data = {
    "Credit Metric": ["Debt/Equity", "Int Coverage", "ROA", "Liab/EBITDA", "EBIT/Int Exp"],
    "GFI": [20.8, 27.6, 8.6, 2.6, 358.7],
    "10 Pctl": [0.4, -12.6, -19.5, -10.5, 117.1],
    "90 Pctl": [42.3, 16.8, 22.8, 78.5, 0.0]
}
sector_comparison = pd.DataFrame(sector_data)
st.table(sector_comparison)

st.dataframe(sector_comparison)
