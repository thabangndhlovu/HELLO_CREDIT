import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from hellocredit import CreditRatingCalculator


with open("hellocredit/templete.json", "r") as f:
    metrics = json.load(f)

data = {
    'leverage_coverage_metrics': {
        'debt_to_equity': 1.175,
        'debt_to_ebitda': 3.5,
        'ebitda_to_interest_expense': 7.925,
        'debt_to_tangible_assets': 0.6
    },
    'efficiency_metrics': {
        'asset_turnover': 1.8,
        'inventory_to_cost_of_sales': 0.4,
        'cash_to_assets': 0.2
    },
    'profitability_metrics': {
        'ebitda_margin': 18.125,
        'total_assets': 50750000.0,
        'sales_growth': 12.125
    }
}



color_mapping = {
    "Aaa": "#6aa84f",  # Green for highest rating
    "Aa": "#93c47d",
    "A": "#b6d7a8",
    "Baa": "#ffd966",  # Yellow for middle rating
    "Ba": "#f6b26b",
    "B": "#e69138",
    "Caa": "#e06666",  # Red for lower rating
    "Ca": "#cc0000",
    "C": "#990000",
}

# Optimized coloring function using the dictionary
def color_rating_optimized(value):
    return f"background-color: {color_mapping.get(value)}"

col_1, col_2 = st.columns(2)
with col_1:
    st.markdown("#### CreditWatch.")



st.title("BANANA Capital Ltd")
st.write("")

doc = """Expected to have extremely conservative financial policies; very stable metrics; public commitment to very strong credit profile over the long term."""



# Define custom colors
credit_rating = "Baa"
credit_score = 3.43
credit_score_color = "#052D3A" #color_mapping.get(credit_rating, "#052D3A")



DOC = """
An AAA credit rating is the highest possible rating assigned to a company by 
credit rating agencies, indicating an exceptional level of creditworthiness and 
financial stability. Companies with an AAA rating are considered extremely low 
risk and are highly likely to meet their financial obligations in full and on 
time. 
"""

col_1, col_2 = st.columns(2)
with col_1:
    st.write(DOC)

with col_2:
    with st.container(border=True, height=150):
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("###### Credit Rating")
            st.markdown(f'<h1 style="color:{credit_score_color}">{credit_rating}</h1>', unsafe_allow_html=True)
        with col_2:
            st.markdown("###### Credit Score")
            st.markdown(f'<h1 style="color:{credit_score_color}">{credit_score}</h1>', unsafe_allow_html=True)

st.write("---")


sector = st.selectbox("Select the sector of the company", [
    "Corporates", 
    "Financial Institutions", 
    "Funds & Asset Management", 
    "Infrastructure & Project Finance", 
    "Insurance", 
    "Other"
])

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
company_size = st.radio("Company Size", ["Small", "Medium", "Large"])

  
tab_1, tab_2, tab_3 = st.tabs([
    "Financial Metrics", 
    "Factor Weights", 
    "Probabilistic Model", 
])


with tab_1:
    def financial_metrics_tab_1(data):
        st.subheader("Financial Metrics")
        cols = st.columns(3)
        
        for i, (category, metrics) in enumerate(data.items()):
            with cols[i]:
                st.markdown(f"<h4><b>{category.replace('_', ' ').title()}</b></h4>", unsafe_allow_html=True)
                for metric_, value in metrics.items():
                    st.metric(metric_.replace('_', ' ').title(), value)

        st.write("*The presented values below represent the expected (mean) metric values across time for given a timeseries.")
        
    financial_metrics_tab_1(data)
    
    # Define the button style using CSS
    button_style = """
    <style>
    .stButton > button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        display: inline-block;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)
    if st.button("Generate Report"):
        st.write("Model is running...")


with tab_2:
    def factor_weights_tab2():
        st.subheader("Factor Weights")
        st.write("""
        The Factor Weights tab enables customisation of the CreditWatch. by adjusting 
        the importance of various financial metrics class. Use the sliders to assign weights 
        to four metric categories: Profitability, Leverage & Coverage, Efficiency, 
        and Financial Policy. Tailoring these weights allows alignment with your 
        specific risk assessment criteria and industry focus, emphasising the most 
        relevant metrics for your needs.
        """)

        col_1, col_2 = st.columns(2)

        metrics_data = [
            ("Profitability", metrics['profitability_metrics']['class_weight'] * 1e2),
            ("Leverage & Coverage", metrics['leverage_coverage_metrics']['class_weight'] * 1e2),
            ("Efficiency", metrics['efficiency_metrics']['class_weight'] * 1e2),
            ("Financial Policy", 0)
        ]

        factor_weights = {}

        with col_1:
            for metric, default_weight in metrics_data:
                factor_weights[metric] = st.slider(metric, 0, 100, value=int(default_weight), key=metric)

        with col_2:
            fig = px.pie(values=list(factor_weights.values()), names=list(factor_weights.keys()))
            fig.update_layout(
                title="Factor Weight Distribution",
                legend_title="Factors",
                font=dict(size=14),
                width=500,
                height=500
            )
            st.plotly_chart(fig)

        total_weight = sum(factor_weights.values())
        factor_weights = {metric: weight / total_weight for metric, weight in factor_weights.items()}

        metrics['leverage_coverage_metrics']['class_weight'] = factor_weights["Leverage & Coverage"]
        metrics['profitability_metrics']['class_weight'] = factor_weights["Profitability"]
        metrics['efficiency_metrics']['class_weight'] = factor_weights["Efficiency"]
        policy_weight = factor_weights['Financial Policy']
    
    factor_weights_tab2()


with tab_3:
    st.subheader("Probabilistic Model")
    st.write("""
    The Probabilistic Model enables you to predict various financial metrics and 
    credit ratings using Bayesian analysis. The Model Config tab allows you to 
    specify the number of periods, iterations, tolerance for convergence, and 
    hyperparameters for the precision of the Gaussian priors.        
    """)

    def plot_tab3_probabilistic_model():
        pass

    credit_ratings = [("Aaa", 2.5), ("Aa", 3.5), ("A", 4.5), ("Baa", 5.5), ("Ba", 6.5), ("B", 7.5), ("Caa", 8.5), ("Ca", 9.5), ("C", float("inf"))]
    actual_ratings = ['Baa', 'Baa', 'Baa', 'Baa', 'Baa', 'B']
    time_periods = ['Q1', 'Q2', 'Q3', 'Q4', 'Prediction 1', 'Prediction 2']

    rating_dict = dict(credit_ratings)
    actual_values = [rating_dict[rating] for rating in actual_ratings]

    # Determine the index where predictions start
    prediction_start_index = time_periods.index('Prediction 1')

    fig = go.Figure(data=[
        go.Scatter(x=time_periods, y=actual_values + [actual_values[-1]], mode='lines+markers+text', name='Ratings',
                line=dict(color='#052D3A'), text=[f'{rating}<br>({value})' for rating, value in zip(actual_ratings, actual_values)] + [f'{actual_ratings[-1]}<br>({actual_values[-1]})'],
                textposition='top center', textfont=dict(size=12),
                marker=dict(color=['#052D3A'] * prediction_start_index + ['#4CAF50'] * (len(actual_values) - prediction_start_index), size=[15] * prediction_start_index + [17] * (len(actual_values) - prediction_start_index)))
    ])

    # Add gray shading for prediction periods
    fig.add_vrect(x0=time_periods[prediction_start_index], x1=time_periods[-1],
                fillcolor="gray", opacity=0.2, layer="below", line_width=0)

    fig.update_layout(title='Credit Rating Over Time', xaxis_title='Time Period', yaxis_title='Credit Rating')
    fig.update_yaxes(autorange="reversed", tickvals=list(rating_dict.values()), ticktext=list(rating_dict.keys()))

    st.plotly_chart(fig)
    
    with st.expander("Model Config"):
        periods = st.number_input("Number of Periods: ", 1)
        col_1, col_2 = st.columns(2)
        with col_1:
            n_iter = st.number_input("Number of Iterations: ", 300)
        with col_2:
            tol = st.number_input("Tolerance for Convergence: ", 1e-3, format="%e")

        if st.button("Re-Run Model"):
            st.write("Model is running...")





# st.page_link("pages/page_2.py", label="Credit Description")


# st.page_link("main.py", label="Home", icon="🏠")
# st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.com", label="Google", icon="🌎")




