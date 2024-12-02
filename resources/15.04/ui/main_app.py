import pandas as pd
import streamlit as st


# Initialize session state for page navigation and storing inputs
if 'page' not in st.session_state:
    st.session_state.page = 'input_page'
if 'input_values' not in st.session_state:
    st.session_state.input_values = {}

def go_to_model_page():
    st.session_state.page = 'model_page'

def go_back_to_input():
    st.session_state.page = 'input_page'

# Define the structure for the input page
def input_page():
    st.title("📈 Credit Default Prediction Model")
    st.markdown("""
    Welcome to the Credit Default Prediction Interface.
    Please input the necessary financial figures below to assess the Profitability of bankruptcy.
    Hover over the question marks next to each input field for more details on what to enter. 🚀
    """)


    sector = st.selectbox("Select the sector of the company", ["Corporates", "Financial Institutions", "Funds & Asset Management", "Infrastructure & Project Finance", "Insurance", "Other"])

    ratios = {
        "Profitability 💰": ["Return on Assets", "Operating Margin Ratio", "Net Profit Margin"],
        "Liquidity 💧": ["Total Debt / EBITA", "Interest Coverage Ratio"],
        "Efficiency ⚡": ["Asset Turnover Ratio"]
    }

    
    columns = st.columns(len(ratios))
    for col, (section, labels) in zip(columns, ratios.items()):
        with col:
            st.subheader(section)
            for label in labels:
                # Store the input values in session state
                st.session_state.input_values[label] = st.number_input(label, format="%.2f")
                
    st.write("---")
    if st.button("Predict Default 🚀", on_click=go_to_model_page):
        pass

# Define the structure for the model output page
def model_page():
    st.header("Model Output 📊")
    st.write("Here are the inputs you provided for the prediction:")

    # Display the input values stored in session state
    for label, value in st.session_state.input_values.items():
        st.write(f"{label}: {value}")

    if st.button("Back to Input 🔙", on_click=go_back_to_input):
        pass



# Page routing
if st.session_state.page == 'input_page':
    input_page()
elif st.session_state.page == 'model_page':
    model_page()
