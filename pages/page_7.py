import streamlit as st
import pandas as pd
import json

# Set page title
st.set_page_config(page_title="Financial Metrics App")

# Function to load data from Excel file
def load_data_from_excel(file):
    try:
        df = pd.read_excel(file, sheet_name="Sheet1", engine="openpyxl")
        return df.to_dict(orient="records")[0]
    except Exception as e:
        st.error(f"Error loading Excel file: {str(e)}")
        return None

# Function to save data to JSON file
def save_data_to_json(data):
    with open("financial_metrics.json", "w") as file:
        json.dump(data, file, indent=2)

# Streamlit app
def main():
    st.title("Financial Metrics App")

    # File upload
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Load data from Excel file
        data = load_data_from_excel(uploaded_file)
    else:
        # Default data
        data = {
            "company_expected_metrics": {
                "leverage_coverage_metrics": {
                    "debt_to_equity": 1.175,
                    "debt_to_ebitda": 3.5,
                    "ebitda_to_interest_expense": 7.925,
                    "debt_to_tangible_assets": 0.6
                },
                "efficiency_metrics": {
                    "asset_turnover": 1.8,
                    "inventory_to_cost_of_sales": 0.4,
                    "cash_to_assets": 0.2
                },
                "profitability_metrics": {
                    "ebitda_margin": 18.125,
                    "total_assets": 50750000.0,
                    "sales_growth": 12.125
                }
            }
        }

    # Input fields for financial metrics
    st.subheader("Leverage & Coverage Metrics")
    data["company_expected_metrics"]["leverage_coverage_metrics"]["debt_to_equity"] = st.number_input("Debt to Equity", value=data["company_expected_metrics"]["leverage_coverage_metrics"]["debt_to_equity"], format="%.3f")
    data["company_expected_metrics"]["leverage_coverage_metrics"]["debt_to_ebitda"] = st.number_input("Debt to EBITDA", value=data["company_expected_metrics"]["leverage_coverage_metrics"]["debt_to_ebitda"], format="%.3f")
    data["company_expected_metrics"]["leverage_coverage_metrics"]["ebitda_to_interest_expense"] = st.number_input("EBITDA to Interest Expense", value=data["company_expected_metrics"]["leverage_coverage_metrics"]["ebitda_to_interest_expense"], format="%.3f")
    data["company_expected_metrics"]["leverage_coverage_metrics"]["debt_to_tangible_assets"] = st.number_input("Debt to Tangible Assets", value=data["company_expected_metrics"]["leverage_coverage_metrics"]["debt_to_tangible_assets"], format="%.3f")

    st.subheader("Efficiency Metrics")
    data["company_expected_metrics"]["efficiency_metrics"]["asset_turnover"] = st.number_input("Asset Turnover", value=data["company_expected_metrics"]["efficiency_metrics"]["asset_turnover"], format="%.3f")
    data["company_expected_metrics"]["efficiency_metrics"]["inventory_to_cost_of_sales"] = st.number_input("Inventory to Cost of Sales", value=data["company_expected_metrics"]["efficiency_metrics"]["inventory_to_cost_of_sales"], format="%.3f")
    data["company_expected_metrics"]["efficiency_metrics"]["cash_to_assets"] = st.number_input("Cash to Assets", value=data["company_expected_metrics"]["efficiency_metrics"]["cash_to_assets"], format="%.3f")

    st.subheader("Profitability Metrics")
    data["company_expected_metrics"]["profitability_metrics"]["ebitda_margin"] = st.number_input("EBITDA Margin", value=data["company_expected_metrics"]["profitability_metrics"]["ebitda_margin"], format="%.3f")
    data["company_expected_metrics"]["profitability_metrics"]["total_assets"] = st.number_input("Total Assets", value=data["company_expected_metrics"]["profitability_metrics"]["total_assets"], format="%.2f")
    data["company_expected_metrics"]["profitability_metrics"]["sales_growth"] = st.number_input("Sales Growth", value=data["company_expected_metrics"]["profitability_metrics"]["sales_growth"], format="%.3f")

    # Save data to JSON file
    if st.button("Save Data"):
        save_data_to_json(data)
        st.success("Data saved successfully!")

if __name__ == "__main__":
    main()