import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from hellocredit import CreditRatingCalculator

def _determine_credit_rating(score):
    credit_ratings = [
        ("Aaa", 2.5), ("Aa", 3.5), ("A", 4.5), ("Baa", 5.5),
        ("Ba", 6.5), ("B", 7.5), ("Caa", 8.5), ("Ca", 9.5),
        ("C", float("inf")),
    ]
    for rating, threshold in credit_ratings:
        if score <= threshold:
            return rating

with open("output.json", "r") as f:
    output_dict = json.load(f)


st.markdown("#### CreditWatch.")




def main():
        
    ###########################################################################

    #policy_weight = output_dict["financial_policy_weight"]
    policy_weight = 0.0
    company_name = output_dict["company_name"]
    rating_description = output_dict["rating_description"]
    credit_score = output_dict["calculator_output"]["credit_score"] 

    if policy_weight > 0.01:
        credit_score *= policy_weight
    credit_rating = _determine_credit_rating(credit_score)


    st.title(company_name)
    st.write("")

    color_mapping = {
        "Aaa": "#6aa84f", "Aa": "#93c47d", "A": "#b6d7a8", "Baa": "#ffd966",
        "Ba": "#f6b26b", "B": "#e69138", "Caa": "#e06666", "Ca": "#cc0000", 
        "C": "#990000",
    }
    color = color_mapping.get(credit_rating)

    col_1, col_2 = st.columns(2)
    with col_1:
        st.write(rating_description)

    with col_2.container(border=True, height=150):
    
        sub_col_1, sub_col_2 = st.columns(2)
        sub_col_1.markdown("###### Credit Rating")
        sub_col_1.markdown(f'<h1 style="color:{"#052D3A"}">{credit_rating}</h1>', unsafe_allow_html=True)
        sub_col_2.markdown("###### Credit Score")
        sub_col_2.markdown(f'<h1 style="color:{"#052D3A"}">{credit_score:.2f}</h1>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: {color}; height: {8}px;"></div>
            """,
            unsafe_allow_html=True,
        )

    st.write("---")

    company_sector = st.selectbox("Select the sector of the company", [
        "Corporates", "Financial Institutions", "Funds & Asset Management", 
        "Infrastructure & Project Finance", "Insurance", "Other"
    ])

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
    company_size = st.radio("Company Size", ["Small", "Medium", "Large"])



    ################################### TABS ##################################

    tab_1, tab_2, tab_3, tab_4 = st.tabs([
        "Financial Metrics", "Factor Weights", "Probabilistic Model", "Overview"
    ])

    with tab_1:
        st.subheader("Financial Metrics")
        company_expected_metrics = output_dict["company_expected_metrics"]
        cols = st.columns(3)
        
        for i, (category, metrics) in enumerate(company_expected_metrics.items()):
            with cols[i]:
                st.markdown(f"<h4><b>{category.replace('_', ' ').title()}</b></h4>", unsafe_allow_html=True)
                for metric_, value in metrics.items():
                    st.metric(metric_.replace('_', ' ').title(), round(value, 2))

        st.caption("*The presented values above represent the expected (average) \
            metric values across time for given the timeseries.")

        # button CSS style
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
        rerun_model = st.button("Re-Run Model")


    with tab_2:
        metrics = output_dict["metrics"]
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
            ("Profitability", metrics['profitability_metrics']['class_weight']),
            ("Leverage & Coverage", metrics['leverage_coverage_metrics']['class_weight']),
            ("Efficiency", metrics['efficiency_metrics']['class_weight']),
            ("Financial Policy", 0)
        ]

        factor_weights = {}
        
        with col_1:
            for metric, default_weight in metrics_data:
                factor_weights[metric] = st.slider(
                    metric, 0, 100, value=int(default_weight), key=metric, 
                    disabled=(metric != "Financial Policy")
                )


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

        metrics["leverage_coverage_metrics"]["class_weight"] = factor_weights["Leverage & Coverage"]
        metrics["profitability_metrics"]["class_weight"] = factor_weights["Profitability"]
        metrics["efficiency_metrics"]["class_weight"] = factor_weights["Efficiency"]
        policy_weight += factor_weights["Financial Policy"]
        
        if factor_weights['Financial Policy'] > 0.0:
                st.markdown(
            """
            **Financial Policy**

            Management and board tolerance for financial risk is a rating determinant \
            because it directly affects debt levels, credit quality, and the risk of \
            adverse changes in financing and capital structure. Considerations include \
            a company’s public commitments in this area, its track record for adhering
            to commitments, and our views on the ability for the company to achieve its targets. 
            """
                )


    with tab_3:
        st.subheader("Probabilistic Model")
        st.write("""
        The Probabilistic Model enables you to predict various financial metrics and 
        credit ratings using Bayesian analysis. The Model Config tab allows you to 
        specify the number of periods, iterations, tolerance for convergence, and 
        hyperparameters for the precision of the Gaussian priors.
        """)

        rating_dict = {
            "Aaa": 2.5, "Aa": 3.5, "A": 4.5, "Baa": 5.5, "Ba": 6.5, 
            "B": 7.5, "Caa": 8.5, "Ca": 9.5, "C": float("inf")
        }

        periods_output = output_dict["calculator_periods_output"]
        bayesian_output = output_dict["bayesian_model_output"]

        bayesian_ratings = [bayesian_output[x]["credit_rating"] for x in bayesian_output]
        periods_ratings = [periods_output[x]["credit_rating"] for x in periods_output]

        time_periods = ['Q1', 'Q2', 'Q3', 'Q4']
        periods_ratings.extend(bayesian_ratings)
        time_periods.extend([f"Prediction {i+1}" for i in range(len(bayesian_ratings))])

        actual_values = [rating_dict[rating] for rating in periods_ratings]
        prediction_start_index = time_periods.index('Prediction 1')

        fig = go.Figure(data=[
            go.Scatter(
                x=time_periods, 
                y=actual_values + [actual_values[-1]], 
                mode='lines+markers+text', 
                name='Ratings',
                line=dict(color='#052D3A'), 
                text=[f'{rating}<br>({value})' for rating, value in zip(periods_ratings, actual_values)] + [f'{periods_ratings[-1]}<br>({actual_values[-1]})'],
                textposition='top center', 
                textfont=dict(size=12),
                marker=dict(
                    color=['#052D3A'] * prediction_start_index + ['#4CAF50'] * (len(actual_values) - prediction_start_index), 
                    size=[15] * prediction_start_index + [17] * (len(actual_values) - prediction_start_index)
                )
            )
        ])

        fig.add_vrect(
            x0=time_periods[prediction_start_index], 
            x1=time_periods[-1],
            fillcolor="gray", 
            opacity=0.2, 
            layer="below", 
            line_width=0
        )

        fig.update_layout(
            title='Credit Rating Over Time', 
            xaxis_title='Time Period', 
            yaxis_title='Credit Rating'
        )
        fig.update_yaxes(
            autorange="reversed", 
            tickvals=list(rating_dict.values()), 
            ticktext=list(rating_dict.keys())
        )

        st.plotly_chart(fig)

        with st.expander("Model Configs"):
            periods = st.number_input("Number of Periods: ", 1)
            col_1, col_2 = st.columns(2)
            with col_1:
                n_iter = st.number_input("Number of Iterations: ", 300)
            with col_2:
                tol = st.number_input("Tolerance for Convergence: ", 1e-3, format="%e")

            run_pro_model = st.button("Run Model")
        


    with tab_4:
        st.subheader("Overview")
        st.write("""
        """)

        tab_1, tab_2 = st.tabs(["Feature Contribution", "Summary Table"])
        
        with tab_2:
            summary_table = output_dict["calculator_output"]["metrics"]

            summary_table_df = pd.DataFrame.from_dict(summary_table, orient='index')
            summary_table_df.columns = [col.replace('_', ' ').title() for col in summary_table_df.columns]
            summary_table_df.index = summary_table_df.index.map(lambda x: x.replace('_', ' ').title())
            summary_table_df['Category'] = summary_table_df['Category'].apply(lambda x: x.replace('_', ' ').title().replace('Metrics', '').strip())
            st.dataframe(summary_table_df)

        with tab_1:
            class_scores = output_dict["calculator_output"]["scores"]
            class_scores.update({"financial_policy": policy_weight})
    
            def assign_credit_rating(value):
                credit_ratings = [
                    ("Aaa", 2.5), ("Aa", 3.5), ("A", 4.5), ("Baa", 5.5), ("Ba", 6.5), 
                    ("B", 7.5), ("Caa", 8.5), ("Ca", 9.5), ("C", float("inf"))
                ]
                return next(rating for rating, threshold in credit_ratings if value <= threshold)

            # Extracting data and assigning ratings
            categories, values = list(class_scores.keys()), list(class_scores.values())
            ratings = [assign_credit_rating(v) for v in values]

            total_value = sum(values)
            normalized_values = [(v / total_value) * 100 for v in values]

            # Adding each feature as a segment of the single bar
            fig = go.Figure()
            for category, original_value, normalized_value, rating in zip(categories, values, normalized_values, ratings):
                category = category.replace("_", " ").replace("metrics", "").title().strip()
                fig.add_trace(go.Bar(
                    y=[""],
                    x=[normalized_value],
                    name=category,
                    orientation='h',
                    text=f'{category}: \n{original_value:.2f} ({rating})',
                    textposition='inside',
                    insidetextanchor='middle',
                    hoverinfo='text'
                ))

            fig.update_layout(
                title='Credit Rating Contributions by Feature (less is better.)',
                barmode='stack',
                xaxis=dict(title='Value', range=[0, 100]),  # Set scale to 100
                yaxis=dict(title=''),
                legend_title_text='Features',
                margin=dict(l=20, r=20, t=40, b=20),
                width=1000, 
                height=200 
            )

            st.plotly_chart(fig)
            
            st.markdown(f"""
            This chart displays the key factors that determine the overall credit\
            rating and their relative importance. The rating is based on three main criteria:

            - **Profitability** ({metrics["profitability_metrics"]["class_weight"]:.2%}): Measures like profit margins and return on assets
            - **Leverage & Coverage** ({metrics["leverage_coverage_metrics"]["class_weight"]:.2%}): Debt and interest coverage ratios
            - **Efficiency** ({metrics["efficiency_metrics"]["class_weight"]:.2%}): Operational and asset use efficiency
            - **Financial Policy** ({policy_weight:.2%}): Measures efficient use of credit.
            
            """)

main()