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

        
        
        #st.metric("", rating, 34)

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

        # The Factor Weights tab allows you to customise the importance of different \
        # financial metric categories. By tailoring these weights, you can align the 
        # analysis with your specific risk assessment criteria and industry focus, 
        # emphasising the metrics that matter most to you. This customisation \
        # feature ensures that the insights provided are highly relevant to your \
        # unique needs and preferences.
        # """)

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
    st.markdown("### Probabilistic Model")

    

    metrics = {
        'debt_to_equity': np.random.normal(1.5, 0.2, 10),
        'interest_coverage': np.random.normal(5, 1, 10),
        'asset_turnover': np.random.normal(0.8, 0.1, 10),
        'interest_expense': np.random.normal(0.05, 0.01, 10)
    }

    predictions = {
        'debt_to_equity': 1.4354540378906038,
        'interest_coverage': 5.010089759952652,
        'asset_turnover': 0.8138410863739253,
        'interest_expense': 0.05027357640453939
    }

    def generate_predictions(metrics: dict) -> dict:
        import pymc as pm
        import numpy as np
        
        with pm.Model() as model:
            priors = {
                metric: pm.Normal(f'{metric}_prior', mu=values[-1], sigma=np.std(values))
                for metric, values in metrics.items()
            }
            likelihoods = {
                metric: pm.Normal(f'{metric}_likelihood', mu=priors[metric], sigma=np.std(values), observed=values)
                for metric, values in metrics.items()
            }
            trace = pm.sample(1000, tune=1000)
        predictions = {metric: np.mean(trace.posterior[f'{metric}_prior'].values) for metric in metrics}
        return predictions








# st.page_link("pages/page_2.py", label="Credit Description")


# st.page_link("main.py", label="Home", icon="🏠")
# st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.com", label="Google", icon="🌎")




