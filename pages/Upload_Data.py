
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd
import pandera as pa
import streamlit as st

from hellocredit import HelloCredit
from hellocredit.utils import validate_dataframe
from hellocredit.helpers import COMPANY_SECTOR_OPTIONS, COMPANY_SIZE_OPTIONS

BASE_PATH = r"C:\Users\103763\Projects\HELLO_CREDIT"


def create_download_button(file_path: str, label: str, file_name: str):
    with open(file_path, "rb") as template_file:
        st.download_button(
            label=label,
            data=template_file.read(),
            file_name=file_name,
            mime="application/vnd.ms-excel"
        )

def get_work_directory(company_name: str, filepath: str) -> str:
    company_name = company_name.lower().replace(" ", "_").strip()
    filename = os.path.splitext(os.path.basename(filepath))[0]
    with open(filepath, "rb") as f:
        hash_value = hashlib.sha256(f.read()).hexdigest()[:16]
    return os.path.abspath(f"temp/{hash_value}")


def load_config(company_sector: str, company_size: str) -> Dict:
    sector = company_sector.lower()
    file_path = "metrics.json" if sector == "large" else "metrics.json"
    with open(file_path, "r") as f:
        return json.load(f)


def save_uploaded_file(folder: str, uploaded_file) -> str:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def process_uploaded_file(uploaded_file: str, company_name: str, company_size: str):
    work_directory = get_work_directory(company_name, uploaded_file.name)
    excel_file_path = save_uploaded_file(work_directory, uploaded_file)
    
    df = pd.read_excel(excel_file_path, index_col=[0, 1])
    df.columns = pd.to_datetime(df.columns)
    validated_df = validate_dataframe(df, company_size)
    
    return work_directory, excel_file_path, validated_df


def get_input_dict(
    work_directory, 
    excel_file_path, 
    company_name, 
    company_size, 
    company_sector
):
    configuration = load_config(company_sector, company_size)
    
    return {
        "work_directory": work_directory,
        "file_path": excel_file_path,
        "company_meta": {
            "company_name": company_name,
            "company_size": company_size,
            "company_sector": company_sector,
        },
        "probabilistic_model": {
            "periods": 2, 
            "look_back_periods": 5, 
            "max_iter": 300, 
            "tol": 1e-3
        },
        "configuration": configuration,
        "financial_policy": 0
    }

def main():
    st.set_page_config(page_title="Upload Data", layout="centered", initial_sidebar_state="collapsed")
    st.markdown("#### CreditWatch.")
    st.title("Upload Company Metrics")
    st.markdown("##")

    # Initialize session state
    if 'company_name' not in st.session_state:
        st.session_state.company_name = ""
    if 'company_size' not in st.session_state:
        st.session_state.company_size = "Small"
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'validated_df' not in st.session_state:
        st.session_state.validated_df = None
    if 'work_directory' not in st.session_state:
        st.session_state.work_directory = None
    if 'excel_file_path' not in st.session_state:
        st.session_state.excel_file_path = None

    st.session_state.company_name = st.text_input("Enter Company Name", st.session_state.company_name)
    company_sector = st.selectbox("Select the sector of the company", COMPANY_SECTOR_OPTIONS, index=0, disabled=True)
    
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
    st.session_state.company_size = st.radio("Company Size", COMPANY_SIZE_OPTIONS, index=COMPANY_SIZE_OPTIONS.index(st.session_state.company_size))
    
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
    
    if st.session_state.uploaded_file is not None:
        try:
            if st.session_state.validated_df is None:
                st.session_state.work_directory, st.session_state.excel_file_path, st.session_state.validated_df = \
                    process_uploaded_file(
                        st.session_state.uploaded_file, st.session_state.company_name, 
                        st.session_state.company_size
                    )
            
            st.success("File successfully loaded")
            st.markdown("### Preview of the dataset file:")
            st.dataframe(st.session_state.validated_df)

            if st.button("Load Model", type="primary", use_container_width=True):
                if not st.session_state.company_name:
                    st.error("Please enter the company name")
                    st.stop()
                
                input_dict = get_input_dict(
                    st.session_state.work_directory, 
                    st.session_state.excel_file_path, 
                    st.session_state.company_name, 
                    st.session_state.company_size, 
                    company_sector
                )
            
                model = HelloCredit(input_dict)
                st.session_state.output_dict = model.run_function()
                st.session_state.input_dict = input_dict
                st.switch_page("pages/credit_watch.py")
        
        
        except Exception as error:
            st.error(f"An error occurred while processing the file. \
                Please make sure you're using the correct file template and try again.\n{error}")
    
    else:
        with st.expander("Metric Descriptions"):
            st.caption("The model expects an Excel template with the following metrics.\
                Ensure the data is adjusted based on the company's size for accurate analysis by the model:")
            
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
            df = pd.DataFrame.from_dict(metrics_info, orient="index", columns=["Description"])
            st.table(df)

            small_company_template = f"{BASE_PATH}\creditwatch_small_medium_company_template.xlsx"
            large_company_template = f"{BASE_PATH}\creditwatch_large_company_template.xlsx"

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

if __name__ == "__main__":
    main()