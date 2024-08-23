import json
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from hellocredit import HelloCredit
from hellocredit.helpers import MAPPED_RATINGS, MAPPED_RATINGS_DICT, COLOR_MAPPING, COMPANY_SECTOR_OPTIONS, COMPANY_SIZE_OPTIONS
from hellocredit.utils import get_credit_rating, percentage_to_rating, get_rating_meta

st.set_page_config(layout="centered", page_title="Credit Watch.", initial_sidebar_state="collapsed")
st.markdown('#### <a href="../Welcome_Page.py" target="_self" style="text-decoration: none; color: inherit;">CreditWatch.</a>', unsafe_allow_html=True)


def main():
            
    try:
        WORK_DIR = st.session_state.input_dict["work_directory"]

        with open(f"{WORK_DIR}/output_dict.json", "r") as f:
            output_dict = json.load(f)

        with open(f"{WORK_DIR}/input_dict.json", "r") as f:
            input_dict = json.load(f)
    except:
        st.switch_page("main.py")

    if st.session_state.run_progress_bar:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()


    ###########################################################################

    financial_policy_rating, financial_policy_score = percentage_to_rating(input_dict["financial_policy"])

    total_weight = sum(list(map(abs, [
        input_dict['financial_policy'],
        input_dict["configuration"]['profitability_metrics']['class_weight'],
        input_dict["configuration"]['leverage_coverage_metrics']['class_weight'],
        input_dict["configuration"]['efficiency_metrics']['class_weight']
    ])))


    financial_policy_percentage = input_dict['financial_policy'] / total_weight
    financial_policy_contribution = financial_policy_score * financial_policy_percentage
    financial_policy_percentage_weighted = -1 * financial_policy_contribution 

    company_name = input_dict["company_meta"]["company_name"].upper()
    selected_company_size = input_dict["company_meta"]["company_size"]
    selected_company_sector = input_dict["company_meta"]["company_sector"]
    credit_score = output_dict["calculator_output"]["credit_score"] + financial_policy_percentage_weighted
    credit_rating = get_credit_rating(credit_score)
    rating_meta = get_rating_meta("Rating", credit_rating)
    probability_of_default = rating_meta["probability_of_default"]
    
    st.title(company_name)
    st.markdown("##")

    col_1, col_2 = st.columns(2)
    with col_1:
        st.write(rating_meta["description"])

    with col_2.container(border=True, height=150):
        sub_col_1, sub_col_2 = st.columns(2)
        sub_col_1.markdown("###### Credit Rating")
        sub_col_1.markdown(f'<h1 style="color:{"#052D3A"}">{credit_rating}</h1>', unsafe_allow_html=True)
        sub_col_2.markdown("###### Credit Score")
        sub_col_2.markdown(f'<h1 style="color:{"#052D3A"}">{credit_score:.2f}</h1>', unsafe_allow_html=True)
        st.markdown(f"""<div style="background-color: {COLOR_MAPPING.get(credit_rating)}; height: {8}px;"></div>""", unsafe_allow_html=True)

    st.write("---")
    company_sector = st.selectbox(
        "Select the sector of the company", 
        COMPANY_SECTOR_OPTIONS,
        index=COMPANY_SECTOR_OPTIONS.index(selected_company_sector),
        disabled=True)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
    company_size = st.radio(
        "Company Size", 
        COMPANY_SIZE_OPTIONS, 
        index=COMPANY_SIZE_OPTIONS.index(selected_company_size), 
        disabled=True
    )

    ################################### TABS ##################################

    tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs([
        "Financial Metrics", "Credit Assessment", "Factor Weights", 
        "Probabilistic Model", "Rating Factors"
    ])

    with tab_1:
        st.subheader("Financial Metrics")
        company_expected_metrics = output_dict["company_expected_metrics"]
        cols = st.columns(3)
        
        for i, (category, metrics) in enumerate(company_expected_metrics.items()):
            with cols[i]:
                st.markdown(f"#### {category.replace('_', ' ').replace('metrics', '').title()}", unsafe_allow_html=True)
                for metric, value in metrics.items():
                    st.metric(metric.replace('_', ' ').title(), round(value, 2))

        st.caption("*The presented values above represent the expected (average) \
            metric values across time for given the timeseries.")

        rerun_model = st.button("Run Model", type="primary", use_container_width=True)


    with tab_2:
        st.header("Credit Assessment")

        st.markdown(rating_meta['meaning'])

        col_1, col_2 = st.columns([0.8, 0.2])

        scaled_credit_score = max(1.5, min(credit_score, 10.5))

        with col_1:
            fig = go.Figure()
            
            shapes = [
                go.layout.Shape(
                    type="rect",
                    x0=1.5 if i == 0 else MAPPED_RATINGS[i-1][1],
                    x1=upper_bound if upper_bound != float("inf") else 10.5,
                    y0=0,
                    y1=1,
                    fillcolor=COLOR_MAPPING[r],
                    line_width=0,
                    layer="below"
                )
                for i, (r, upper_bound) in enumerate(MAPPED_RATINGS)
            ]

            # Add vertical line for the score
            shapes.append(
                go.layout.Shape(
                    type="line",
                    x0=scaled_credit_score,
                    x1=scaled_credit_score,
                    y0=-2,
                    y1=2,
                    line=dict(color="rgba(0,0,0,0.5)", width=5)
                )
            )

            # Customize layout
            fig.update_layout(
                shapes=shapes,
                xaxis=dict(
                    title="Credit Rating",
                    title_standoff=25,
                    range=[1.5, 10.5],  # Keep this range to match your shapes
                    tickvals=[1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5],  # Adjusted to start at 1.5
                    ticktext=[r[0] for r in MAPPED_RATINGS],
                    tickangle=0,
                    tickmode='array',
                    tickfont=dict(size=10),
                    title_font=dict(size=10)
                ),
                yaxis=dict(visible=False),
                height=150,
                margin=dict(l=40, r=20, t=20, b=50),
                showlegend=False,
        )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


        with col_2:
            st.markdown("#### ")
            st.metric("Probability of Default", f"{probability_of_default}%")
        
        if output_dict['llm_response'].get('response'):
            st.markdown("##### Summary Analysis")
            st.markdown(output_dict['llm_response']['overall_analysis'])

            with st.expander("Highlights"):
                col_1, col_2 = st.columns(2)
                with col_1:
                    st.markdown("##### Key Strengths")
                    for strength in output_dict['llm_response']["key_strengths"]:
                        st.markdown(f"- {strength}")

                with col_2:
                    st.markdown("##### Potential Risks")
                    for risk in output_dict['llm_response']["potential_risks"]:
                        st.markdown(f"- {risk}")

            st.caption("Generated with AI.")
        else:
            st.error(output_dict['llm_response']['overall_analysis'])


    with tab_3:
        metrics = input_dict["configuration"]
        st.subheader("Factor Weights")
        st.write("""
        The Factor Weights tab enables customisation of the CreditWatch. by adjusting 
        the importance of various financial metrics class. Use the sliders to assign weights 
        to four metric categories: Profitability, Leverage & Coverage, Efficiency, 
        and Financial Policy. Tailoring these weights allows alignment with your 
        specific risk assessment criteria and industry focus, emphasising the most 
        relevant metrics for your analysis.
        """)

        col_1, col_2 = st.columns(2)

        metrics_data = [
            ("Profitability", metrics['profitability_metrics']['class_weight']),
            ("Leverage & Coverage", metrics['leverage_coverage_metrics']['class_weight']),
            ("Efficiency", metrics['efficiency_metrics']['class_weight']),
            ("Financial Policy", input_dict["financial_policy"])
        ]

        factor_weights = {}
        
        with col_1:
            for metric, default_weight in metrics_data:
                is_financial_policy = metric == "Financial Policy"
                factor_weights[metric] = st.slider(
                    metric,
                    min_value=-100 if is_financial_policy else 0,
                    max_value=100,
                    value=int(default_weight),
                    key=metric,
                    disabled=not is_financial_policy
            )

        with col_2:
            fig = px.pie(
                values=list(map(abs, factor_weights.values())), 
                names=list(factor_weights.keys())
            )
            fig.update_layout(
                title="Factor Weight Distribution",
                legend_title="Factors",
                font=dict(size=14),
                width=500,
                height=500
            )
            st.plotly_chart(fig)

        input_dict["configuration"]["leverage_coverage_metrics"]["class_weight"] = factor_weights["Leverage & Coverage"]
        input_dict["configuration"]["profitability_metrics"]["class_weight"] = factor_weights["Profitability"]
        input_dict["configuration"]["efficiency_metrics"]["class_weight"] = factor_weights["Efficiency"]
        input_dict["financial_policy"] = factor_weights["Financial Policy"]

        
        if abs(factor_weights['Financial Policy']) > 0.0:
            st.markdown(
            """
            **Financial Policy**

            This factor assesses the management and board's tolerance for financial risk, \
            which directly impacts debt levels, credit quality, and the potential \
            for adverse changes in financing and capital structure. The evaluation \
            takes into account the company's public commitments regarding financial \
            policy, its history of adhering to these commitments, and the analyst's \
            perspective on the company's capability to achieve its stated targets.
            """
        )


    with tab_4:
        st.subheader("Probabilistic Model")
        st.write("""
        The Probabilistic Model enables you to predict various financial metrics and 
        credit ratings using Bayesian analysis.
        """)

        periods_output = output_dict["calculator_periods_output"]
        bayesian_output = output_dict["bayesian_model_output"]['computed_rating']

        bayesian_ratings = [bayesian_output[x]["credit_rating"] for x in bayesian_output]
        periods_ratings = [periods_output[x]["credit_rating"] for x in periods_output]

        time_periods = [f"T{t + 1}" for t in range(len(periods_output))]
        periods_ratings.extend(bayesian_ratings)
        time_periods.extend([f"Prediction {i+1}" for i in range(len(bayesian_ratings))])

        actual_values = [MAPPED_RATINGS_DICT[rating] for rating in periods_ratings]
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
            tickvals=list(MAPPED_RATINGS_DICT.values()), 
            ticktext=list(MAPPED_RATINGS_DICT.keys())
        )

        st.plotly_chart(fig)

        with st.expander("Model Configuration"):
            prob_model = input_dict["probabilistic_model"]
            col1, col2 = st.columns(2)
            
            prob_inputs = [
                ("Number of Periods:", "periods", {"min_value": 1, "max_value": 10}),
                ("Number of Look back Periods:", "look_back_periods", {"min_value": 1, "max_value": 100}),
                ("Number of Iterations:", "max_iter", {"min_value": 0, "max_value": 1000}),
                ("Tolerance for Convergence:", "tol", {"format": "%e"})
            ]
            
            for i, (label, key, kwargs) in enumerate(prob_inputs):
                with col1 if i % 2 == 0 else col2:
                    input_dict["probabilistic_model"][key] = st.number_input(
                        label, 
                        value=prob_model[key], 
                        key=key, 
                        **kwargs
                    )

    
    with tab_5:
        st.subheader("Rating Factors")
        tab_1, tab_2 = st.tabs(["Feature Contribution", "Summary Table"])

        with tab_1:
            class_scores = output_dict["calculator_output"]["scores"]
            
            if abs(factor_weights['Financial Policy']) > 0.0:
                class_scores.update({"financial_policy": financial_policy_score})

            # Extracting data and assigning ratings
            categories, values = list(class_scores.keys()), list(class_scores.values())
            ratings = [get_credit_rating(v) for v in values]

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
                width=700, 
                height=200 
            )

            st.plotly_chart(fig)

            total_weight = sum(map(abs, factor_weights.values()))
            normalised_weights = {metric: (abs(weight) / total_weight) for metric, weight in factor_weights.items()}
            
            st.markdown(f"""
            This chart displays the key factors that determine the overall credit rating and their relative importance. The rating is based on four main criteria:

            - **Profitability** ({normalised_weights["Profitability"]:.2%}): Measures like profit margins and return on assets
            - **Leverage & Coverage** ({normalised_weights["Leverage & Coverage"]:.2%}): Debt and interest coverage ratios
            - **Efficiency** ({normalised_weights["Efficiency"]:.2%}): Operational and asset use efficiency
            - **Financial Policy** ({normalised_weights["Financial Policy"]:.2%}): Evaluates management's risk tolerance and impact on debt, credit quality, and capital structure
            """)
        
        with tab_2:
            clean_string =  lambda s: s.replace('_', ' ').title().replace('Metrics', '').strip()

            summary_table_df = pd.DataFrame.from_dict(output_dict["calculator_output"]["metrics"], orient='index')        
            summary_table_df.columns = summary_table_df.columns.map(clean_string)
            summary_table_df.index = summary_table_df.index.map(clean_string)        
            summary_table_df['Category'] = summary_table_df['Category'].apply(clean_string)
            
            if abs(factor_weights['Financial Policy']) > 0.0:
                fin_policy_sum = pd.DataFrame({
                    "Category": ["Financial Policy"],
                    "Value": [factor_weights['Financial Policy']],
                    "Score": [""],
                    "Weight": [financial_policy_percentage],
                    "Weighted Score": [financial_policy_percentage_weighted],
                    "Rating": [financial_policy_rating]
                }, index=["Financial Policy"])
                
                summary_table_df = pd.concat([summary_table_df, fin_policy_sum])
            
            st.dataframe(summary_table_df.round(2))
            st.caption("*The presented values above represent the expected (average) "
                    "metric values across time for the given timeseries.")

    if rerun_model:
        API_KEY = ""
        model = HelloCredit(API_KEY, input_dict)
        model.run_function()
        st.rerun()

    st.session_state.run_progress_bar = False
main()