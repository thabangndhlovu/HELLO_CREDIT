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

tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs([
    "Financial Metrics", 
    "Factor Weights", 
    "Feature Importance", 
    "Rating Projections",
    "Executive Summary"
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
        if factor_weights['Financial Policy'] > 0:
            st.text_input(f"Why are you giving the {'company'} {policy_weight:.2%} weighting on financial policy?")
    
    factor_weights_tab2()


with tab_3:
    st.subheader("Rating Contributors")

    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # The provided data
    data = {
        'leverage_coverage_metrics': 4.0,
        'efficiency_metrics': 3.1,
        'profitability_metrics': 5.1
    }

    # Converting the data into a DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])

    # Creating the horizontal bar chart using Plotly
    fig = px.bar(df, y='Metric', x='Value', orientation='h', 
                labels={'Value': 'Rating Score (1 is highest, 9 is lowest)'},
                hover_data={'Value': True})

    st.plotly_chart(fig, use_container_width=True)





    # st.subheader("Credit Ratings (overtime)")
    # quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    # ratings = ['A', 'Baa', 'Baa', 'C']
    # rating_to_numeric = {'Aaa': 1, 'Aa': 2, 'A': 3, 'Baa': 4, 'Ba': 5, 'B': 6, 'Caa': 7, 'Ca': 8, 'C': 9, 'D': 10}

    # df = pd.DataFrame({'Timeseries': quarters, 'Rating': ratings})
    # df['Rating Numeric'] = df['Rating'].map(rating_to_numeric)

    # fig = px.line(df, x='Timeseries', y='Rating', markers=True, title='')
    # fig.update_yaxes(tickvals=list(rating_to_numeric.values()), ticktext=list(rating_to_numeric.keys()))
    # fig.update_traces(mode='lines+markers', line=dict(dash='dash'))
    # st.plotly_chart(fig)

    # # Optional: Display the DataFrame



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


with tab_5:
    col_1, col_2 = st.columns(2)

    st.markdown(
    """
    ### Executive Summary
    BANANA Capital Ltd. is a private investment and financial services company specializing in venture capital, private equity, and asset management. 
    The company has shown steady growth since its incorporation, with a diverse portfolio in technology, healthcare, and renewable energy sectors.

    ### Credit Rating
    
    Credit Rating: A (Stable)
    
    Rating Agency: ABC Credit Rating Agency

    ### Conclusion
    BANANA Capital Ltd. is a financially stable and well-managed company with a solid track record in the investment and financial services industry. 
    The company’s prudent financial practices and diverse investment portfolio position it well for continued growth and stable returns. 
    The current credit rating of A (Stable) reflects confidence in the company’s ability to meet its financial obligations and sustain its operational success.
    """
    )


re_run_button = st.button("Run Model", key="run_model")


# st.page_link("pages/page_2.py", label="Credit Description")


# st.page_link("main.py", label="Home", icon="🏠")
# st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.com", label="Google", icon="🌎")




