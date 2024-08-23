import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def _determine_credit_rating(credit_score):
    # Implement the logic to determine credit rating based on credit score
    # This is a placeholder implementation
    if credit_score > 90:
        return "Aaa"
    elif credit_score > 80:
        return "Aa"
    # ... add more conditions as needed
    else:
        return "C"

def input_phase():
    st.title("CreditWatch - Input Data")
    
    company_name = st.text_input("Company Name")
    company_sector = st.selectbox("Select the sector of the company", [
        "Corporates", "Financial Institutions", "Funds & Asset Management", 
        "Infrastructure & Project Finance", "Insurance", "Other"
    ])
    company_size = st.radio("Company Size", ["Small", "Medium", "Large"])
    
    st.header("Financial Metrics")
    profitability = st.number_input("Profitability Score", 0.0, 100.0, 50.0)
    leverage_coverage = st.number_input("Leverage & Coverage Score", 0.0, 100.0, 50.0)
    efficiency = st.number_input("Efficiency Score", 0.0, 100.0, 50.0)
    financial_policy = st.number_input("Financial Policy Score", 0.0, 100.0, 50.0)
    
    if st.button("Calculate Credit Rating"):
        st.session_state.input_complete = True
        st.session_state.company_name = company_name
        st.session_state.company_sector = company_sector
        st.session_state.company_size = company_size
        st.session_state.profitability = profitability
        st.session_state.leverage_coverage = leverage_coverage
        st.session_state.efficiency = efficiency
        st.session_state.financial_policy = financial_policy

def main():
    st.title(f"CreditWatch - {st.session_state.company_name}")
    
    # Calculate credit score (this is a simplified example)
    credit_score = (st.session_state.profitability + 
                    st.session_state.leverage_coverage + 
                    st.session_state.efficiency + 
                    st.session_state.financial_policy) / 4
    
    # Determine credit rating
    credit_rating = _determine_credit_rating(credit_score)
    
    # Simulate the output_dict structure
    output_dict = {
        "company_name": st.session_state.company_name,
        "rating_description": f"Credit rating for {st.session_state.company_name}",
        "calculator_output": {"credit_score": credit_score},
        "metrics": {
            "profitability_metrics": {"class_weight": 0.25},
            "leverage_coverage_metrics": {"class_weight": 0.25},
            "efficiency_metrics": {"class_weight": 0.25},
        }
    }
    
    policy_weight = 0.25  # Assuming equal weight for simplicity
    
    # Display results as in the original code
    col_1, col_2 = st.columns(2)
    with col_1:
        st.write(output_dict["rating_description"])

    color_mapping = {
        "Aaa": "#6aa84f", "Aa": "#93c47d", "A": "#b6d7a8", "Baa": "#ffd966",
        "Ba": "#f6b26b", "B": "#e69138", "Caa": "#e06666", "Ca": "#cc0000", 
        "C": "#990000",
    }
    color = color_mapping.get(credit_rating)

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

    st.write(f"Company Sector: {st.session_state.company_sector}")
    st.write(f"Company Size: {st.session_state.company_size}")

    # Add the tabs and other visualizations as in the original code
    # For brevity, I'll just add the Factor Weights tab as an example

    tab_1, tab_2, tab_3, tab_4 = st.tabs([
        "Financial Metrics", "Factor Weights", "Probabilistic Model", "Overview"
    ])

    with tab_2:
        st.subheader("Factor Weights")
        
        factor_weights = {
            "Profitability": st.session_state.profitability,
            "Leverage & Coverage": st.session_state.leverage_coverage,
            "Efficiency": st.session_state.efficiency,
            "Financial Policy": st.session_state.financial_policy
        }
        
        col_1, col_2 = st.columns(2)
        
        with col_1:
            for metric, weight in factor_weights.items():
                st.slider(metric, 0, 100, int(weight), key=metric, disabled=True)

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

    # Add more tabs and visualizations as needed

if __name__ == "__main__":
    if 'input_complete' not in st.session_state:
        st.session_state.input_complete = False

    if not st.session_state.input_complete:
        input_phase()
    else:
        main()