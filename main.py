import json

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


# Set page title and theme
st.set_page_config(page_title="Home Page", page_icon=":guardsman:", layout="wide", initial_sidebar_state="auto")


col_1, col_2 = st.columns(2)
with col_1:
    st.title("CreditWatch.")

with col_2:
    st.image("logo.png")




uploaded_file = st.sidebar.file_uploader("Upload Company Financials")

    

doc = """Expected to have extremely conservative financial policies; very stable metrics; public commitment to very strong credit profile over the long term."""
rating = "Aa"

st.page_link("pages/credit_description.py", label="Credit Description")



DOC = """
An AAA credit rating is the highest possible rating assigned to a company by 
credit rating agencies, indicating an exceptional level of creditworthiness and 
financial stability. Companies with an AAA rating are considered extremely low 
risk and are highly likely to meet their financial obligations in full and on 
time. This rating reflects strong financial health, prudent management practices, 
and a robust track record of performance and profitability. Investors view 
companies with an AAA rating as safe havens, offering a high degree of security 
and stability. Overall, an AAA credit rating signals confidence in the company's 
ability to weather economic uncertainties and maintain a superior financial standing.
"""

col_1, col_2 = st.columns(2)
with col_1:
    st.write(DOC)

with col_2:
    with st.container(border=True, height=150):
        st.metric("", rating, -0)

st.write("---")


sector = st.selectbox("Select the sector of the company", [
    "Corporates", 
    "Financial Institutions", 
    "Funds & Asset Management", 
    "Infrastructure & Project Finance", 
    "Insurance", 
    "Other"
])
small_company_toggle = st.toggle("Small Company")

tab_1, tab_2, tab_3, tab_4 = st.tabs([
    "Financial Metrics", 
    "Factor Weights", 
    "Rating History", 
    "Rating Projections"
])


with tab_1:
    def financial_metrics_tab_1(data):
        st.subheader("Financial Metrics")
        st.write("The presented values below represent the expected (mean) metric values across time.")
        cols = st.columns(3)
        
        for i, (category, metrics) in enumerate(data.items()):
            with cols[i]:
                st.markdown(f"<h4><b>{category.replace('_', ' ').title()}</b></h4>", unsafe_allow_html=True)
                for metric_, value in metrics.items():
                    st.metric(metric_.replace('_', ' ').title(), value)
    financial_metrics_tab_1(data)
 

with tab_2:
    def factor_weights_tab2():
        st.subheader("Factor Weights")
        st.write("""
        The Factor Weights tab enables customisation of the CreditWatch by adjusting 
        the importance of various financial metrics. Use the sliders to assign weights 
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
    
    factor_weights_tab2()


with tab_3:
    st.subheader("Rating History")
    st.write(doc)

    # Sample credit rating data
    rating_data = {
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "Rating": ["A", "A-", "A-", "BBB", "BBB+", "A-"]
    }

    # Create a line chart using plotly
    fig = px.line(rating_data, x="Year", y="Rating", markers=True)

    # Update the chart layout
    fig.update_layout(
        title="Credit Rating History",
        xaxis_title="Year",
        yaxis_title="Rating",
        yaxis=dict(
            autorange="reversed",
            tickvals=["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C"],
            ticktext=["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C"]
        ),
        font=dict(size=14),
        width=800,
        height=500,
    )

    st.plotly_chart(fig)


with tab_4:
    st.subheader("Credit Rating Projection")
    st.write(doc)

    # Sample projected credit rating probabilities
    projected_probabilities = {
        "Year": [2024, 2025, 2026, 2027, 2028],
        "AAA": [0.05, 0.08, 0.12, 0.15, 0.20],
        "AA+": [0.10, 0.15, 0.20, 0.25, 0.30],
        "AA": [0.20, 0.25, 0.30, 0.35, 0.40],
        "AA-": [0.30, 0.35, 0.40, 0.45, 0.50],
        "A+": [0.25, 0.30, 0.35, 0.40, 0.45],
        "A": [0.20, 0.25, 0.30, 0.35, 0.40],
        "A-": [0.15, 0.20, 0.25, 0.30, 0.35],
        "BBB+": [0.10, 0.15, 0.20, 0.25, 0.30],
        "BBB": [0.05, 0.10, 0.15, 0.20, 0.25],
        "BBB-": [0.02, 0.05, 0.10, 0.15, 0.20],
    }

    # Create traces for each credit rating
    traces = []
    for rating in ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-"]:
        trace = go.Scatter(
            x=projected_probabilities["Year"],
            y=projected_probabilities[rating],
            mode="lines",
            name=rating,
            fill="tonexty",
            opacity=0.7,
        )
        traces.append(trace)

    # Create the layout for the chart
    layout = go.Layout(
        title="Credit Rating Projection (Probabilistic)",
        xaxis=dict(title="Year", tickmode="linear"),
        yaxis=dict(title="Probability", range=[0, 1], tickformat=".0%"),
        showlegend=True,
        hovermode="x",
    )

    # Create the figure and add the traces
    fig = go.Figure(data=traces, layout=layout)

    # Display the chart in Streamlit
    st.plotly_chart(fig)

#if st.button("Run Model"):
    # Code to run when the button is clicked

re_run_button = st.button("Re-Run Model", key="run_model")


# st.page_link("pages/page_2.py", label="Credit Description")


# st.page_link("main.py", label="Home", icon="🏠")
# st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.com", label="Google", icon="🌎")




