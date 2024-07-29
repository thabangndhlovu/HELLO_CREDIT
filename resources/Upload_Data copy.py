import os
import json
import hashlib
from datetime import datetime

import pandas as pd
import streamlit as st
import pandera as pa



def get_work_directory(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    timestamp = datetime.now().strftime("%Y%m%d")
    
    with open(filepath, 'rb') as f:
        file_content = f.read()
        
    hash_value = hashlib.sha256(file_content).hexdigest()[:16]
    return os.path.abspath(f"temp/{hash_value}")


def load_config(company_sector, company_size):
    sector = company_sector.lower()
    file_path = "metrics.json" if sector == "large" else "metrics.json"
    
    with open(file_path, "r") as f:
        return json.load(f)
    

def save_uploaded_file(folder, uploaded_file):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def create_download_button(file_path: str, label: str, file_name: str):
    with open(file_path, "rb") as template_file:
        template_bytes = template_file.read()
            
        st.download_button(
            label=label,
            data=template_bytes,
            file_name=file_name,
            mime="application/vnd.ms-excel"
        )


st.set_page_config(
    page_title="Upload Data", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("#### CreditWatch.")
st.title("Upload Company Metrics")
st.write("")

company_name = st.text_input("Enter Company Name", "")
company_sector = st.selectbox("Select the sector of the company", [
    "Corporates", "Financial Institutions", "Funds & Asset Management", 
    "Infrastructure & Project Finance", "Insurance", "Other"
    ], disabled=True)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
company_size = st.radio("Company Size", ["Small", "Medium", "Large"])
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    with st.spinner("Loading and processing file..."):
        work_directory = get_work_directory(uploaded_file.name)
        excel_file_path = save_uploaded_file(work_directory, uploaded_file)
        
        try:
            df = pd.read_excel(excel_file_path, index_col=[0, 1])
            df.columns = pd.to_datetime(df.columns)

            # Validate the dataset
            expected_categories = [
                "leverage_coverage_metrics", 
                "efficiency_metrics", 
                "profitability_metrics"
            ]

            if company_size in ("Small", "Medium"):
                small_expected_metrics = [
                    "debt_to_equity", "debt_to_ebitda", "ebitda_to_interest_expense",
                    "debt_to_tangible_assets", "asset_turnover", "inventory_to_cost_of_sales",
                    "cash_to_assets", "ebitda_margin", "total_assets", "sales_growth"
                ]
                column_schema = {col: pa.Column(float) for col in df.columns}
                schema = pa.DataFrameSchema(
                    columns=column_schema,
                    index=pa.MultiIndex([
                        pa.Index(str, name="Metric Category"),
                        pa.Index(str, name="Metric Name", checks=[
                            pa.Check.isin(small_expected_metrics),
                            pa.Check(lambda x: set(x) == set(small_expected_metrics), 
                            error="DataFrame contains unexpected or missing metrics")
                        ])
                    ]),
                strict=True)

            if company_size == "Large":
                large_expected_metrics = [
                    "debt_to_equity", "debt_to_ebitda", "ebitda_to_interest_expense",
                    "asset_turnover", "ebitda_margin"
                ]
                column_schema = {col: pa.Column(float) for col in df.columns}
                schema = pa.DataFrameSchema(
                    columns=column_schema,
                    index=pa.MultiIndex([
                        pa.Index(str, name="Metric Category"),
                        pa.Index(str, name="Metric Name", checks=[
                            pa.Check.isin(large_expected_metrics),
                            pa.Check(lambda x: set(x) == set(large_expected_metrics), 
                            error="DataFrame contains unexpected or missing metrics")
                        ])
                    ]),
                strict=True)

            validated_df = schema.validate(df)
            
            st.success("File successfully loaded")
            st.markdown("### Preview of the dataset file:")
            st.dataframe(validated_df)
            

            if st.button("Load Model", type="primary", use_container_width=True):
                
                if not company_name:
                    st.error("Please enter the company name")
                    st.stop()
                
                st.session_state["work_directory"] = work_directory
                configuration = load_config(company_sector, company_size)
                
                input_dict = {
                    "work_directory": work_directory,
                    "file_path": excel_file_path,
                    "company_meta": {
                        "company_name": company_name,
                        "company_size": company_size,
                        "company_sector": company_sector,
                    },
                    "probabilistic_model": {
                        "periods": 1, 
                        "look_back_periods": 5, 
                        "max_iter": 300, 
                        "tol": 1e-3
                    },
                    "configuration": configuration
                }

                
                st.switch_page("pages/credit_watch.py")
                

        except pa.errors.SchemaError as error:
            st.error(
        f"""
        An error occurred while processing the file.
        Please make sure you're using the correct file template and try again.\n
        {error}
        """
        )
        
        except Exception as error:
            st.error(
        f"""
        An error occurred while processing the file.
        Please make sure you're using the correct file template and try again.\n
        {error}
        """
        )


if not uploaded_file:
    with st.expander("Metric Descriptions"):
        st.caption("""
        The model expects an Excel template with the following metrics. 
        Ensure the data is adjusted based on the company's size for accurate analysis by the model:
        """)
            
        metrics_info = {
            "Ebitda Margin": "Measures operational profitability as a percentage of revenue. EBITDA / Revenue",
            "Total Assets": "Sum of all current and non-current assets owned by the company. Sum of all assets",
            "Sales Growth": "Year-over-year percentage increase in sales or revenue. (Current Sales - Prior Sales) / Prior Sales",
            "Debt To Equity": "Ratio of total debt to shareholders' equity, indicating leverage. Total Debt / Shareholders' Equity",
            "Debt To Ebitda": "Ratio of total debt to EBITDA, indicating ability to pay off debt. Total Debt / EBITDA",
            "Ebitda To Interest Expense": "Ratio of EBITDA to interest expense, showing ability to cover interest payments. EBITDA / Interest Expense",
            "Debt To Tangible Assets": "Ratio of total debt to tangible assets, showing leverage relative to physical assets. Total Debt / Tangible Assets",
            "Asset Turnover": "Ratio of revenue to average total assets, indicating efficiency of asset usage. Revenue / Average Total Assets",
            "Inventory To Cost Of Sales": "Ratio of average inventory to cost of goods sold, showing inventory management efficiency. Average Inventory / Cost of Goods Sold",
            "Cash To Assets": "Ratio of cash and cash equivalents to total assets, indicating liquidity. Cash and Cash Equivalents / Total Assets"
            }

        df = pd.DataFrame.from_dict(metrics_info, orient="index").reset_index()
        df.columns = ['Metric', 'Description']
        st.table(df)


        # Helper Templates
        base_path = r"C:\Users\103763\Projects\HELLO_CREDIT"
        small_company_template = f"{base_path}\creditwatch_small_medium_company_template.xlsx"
        large_company_template = f"{base_path}\creditwatch_large_company_template.xlsx"

        col_1, _, col_2 = st.columns(3)
        with col_1:
            create_download_button(
                small_company_template,
                "Download Template\n\n(Small & Medium Company)",
                "creditwatch_small_medium_company_template.xlsx"
            )

        with col_2:
            create_download_button(
                large_company_template,
                "Download Template\n\n(Large Company)",
                "creditwatch_large_company_template.xlsx"
            )