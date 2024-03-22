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

# import streamlit as st
# 
# st.header("Model Inputs")
# st.subheader("Financial Metrics")
# 
# income_statement_labels = [
#     "Revenue", 
#     "Cost of Goods Sold", 
#     "Gross Profit", 
#     "Operating Expenses", 
#     "Operating Income", 
#     "Interest Expense"
# ]
# 
# balance_sheet_labels = [
#     "Cash", 
#     "Accounts Receivable", 
#     "Inventory", 
#     "Total Current Assets", 
#     "Total Assets", 
#     "Accounts Payable"]
# 
# col1, col2 = st.columns(2)
# 
# with col1:
#     st.markdown("### Income Statement")
#     for label in income_statement_labels:
#         st.number_input(label, key=f"IS_{label}", format="%f")
# 
# with col2:
#     st.markdown("### Balance Sheet")
#     for label in balance_sheet_labels:
#         st.number_input(label, key=f"BS_{label}", format="%f")


import streamlit as st

# Function to display the model input form
def show_input_form():
    st.header("Model Inputs")
    st.subheader("Financial Metrics")

    income_statement_labels = ["Revenue", "Cost of Goods Sold", "Gross Profit", "Operating Expenses", "Operating Income", "Interest Expense"]
    balance_sheet_labels = ["Cash", "Accounts Receivable", "Inventory", "Total Current Assets", "Total Assets", "Accounts Payable"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Income Statement")
        for label in income_statement_labels:
            st.number_input(label, key=f"IS_{label}", format="%f")

    with col2:
        st.markdown("### Balance Sheet")
        for label in balance_sheet_labels:
            st.number_input(label, key=f"BS_{label}", format="%f")
    
    if st.button("Generate Model"):
        # Set a session state variable to navigate to the results page
        st.session_state.page = "results"

# Function to display the results page
def show_results_page():
    st.header("Model Results")
    # Example content - adapt based on your actual model results
    st.write("Model generated successfully. Display results or further actions here.")

# Main app logic
if 'page' not in st.session_state:
    st.session_state.page = "input_form"

if st.session_state.page == "input_form":
    show_input_form()
elif st.session_state.page == "results":
    show_results_page()
