import os
import json
import hashlib

import pandas as pd
import streamlit as st

from hellocredit import HelloCredit
from hellocredit.utils import validate_dataframe
from hellocredit.helpers import COMPANY_SECTOR_OPTIONS, COMPANY_SIZE_OPTIONS

BASE_PATH = os.getcwd()
API_KEY = ""


def create_download_button(file_path: str, label: str, file_name: str):
    with open(file_path, "rb") as template_file:
        st.download_button(
            label=label,
            data=template_file.read(),
            file_name=file_name,
            mime="application/vnd.ms-excel",
        )


def get_work_directory(filepath: str) -> str:
    with open(filepath, "rb") as f:
        hash_value = hashlib.sha256(f.read()).hexdigest()[:16]
    abs_path = os.path.join(BASE_PATH, os.path.abspath(f"public/work_directory/{hash_value}"))
    return abs_path


def load_config(company_sector: str, company_size: str) -> dict:
    size = company_size.lower()

    file_path = (
        "public/metrics_large.json" if size == "large" else "public/metrics_small.json"
    )
    with open(file_path, "r") as f:
        return json.load(f)


def save_uploaded_file(folder: str, uploaded_file) -> str:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def process_uploaded_file(uploaded_file: str, company_size: str):
    work_directory = get_work_directory(uploaded_file.name)
    excel_file_path = save_uploaded_file(work_directory, uploaded_file)

    df = pd.read_excel(excel_file_path, index_col=[0, 1])
    df.columns = pd.to_datetime(df.columns)
    validated_df = validate_dataframe(df, company_size)

    return work_directory, excel_file_path, validated_df


def get_input_dict(
    work_directory, excel_file_path, company_name, company_size, company_sector
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
            "tol": 1e-3,
        },
        "configuration": configuration,
        "financial_policy": 0,
    }


def main():
    st.set_page_config(
        page_title="Upload Data", layout="centered", initial_sidebar_state="collapsed"
    )
    st.markdown("#### CreditWatch.")
    st.title("Upload Company Metrics")
    st.markdown("##")

    api_key = st.sidebar.text_input(
        "Enter your API Key (used for AI response)", value=API_KEY, type="password"
    )

    # Initialize session state
    if "company_name" not in st.session_state:
        st.session_state.company_name = ""
    if "company_size" not in st.session_state:
        st.session_state.company_size = "Small"
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "validated_df" not in st.session_state:
        st.session_state.validated_df = None
    if "work_directory" not in st.session_state:
        st.session_state.work_directory = None
    if "excel_file_path" not in st.session_state:
        st.session_state.excel_file_path = None
    if "api_key" not in st.session_state:
        st.session_state.api_key = api_key

    st.session_state.company_name = st.text_input(
        "Enter Company Name", st.session_state.company_name
    )
    company_sector = st.selectbox(
        "Select the sector of the company",
        COMPANY_SECTOR_OPTIONS,
        index=0,
        disabled=True,
    )

    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>",
        unsafe_allow_html=True,
    )
    st.session_state.company_size = st.radio(
        "Company Size",
        COMPANY_SIZE_OPTIONS,
        index=COMPANY_SIZE_OPTIONS.index(st.session_state.company_size),
    )

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        save_uploaded_file(".", uploaded_file)

    if st.session_state.uploaded_file is not None:
        try:
            if st.session_state.validated_df is None:
                (
                    st.session_state.work_directory,
                    st.session_state.excel_file_path,
                    st.session_state.validated_df,
                ) = process_uploaded_file(
                    st.session_state.uploaded_file,
                    st.session_state.company_size,
                )

            st.success("File successfully loaded")
            st.markdown("### Preview of the dataset file:")
            st.dataframe(st.session_state.validated_df)

        except Exception as error:
            st.error(f"An error occurred while processing the file. \
                Please make sure you're using the correct file template and try again.\n{error}")

        if st.button("Load Model", type="primary", use_container_width=True):
            if not st.session_state.company_name:
                st.error("Please enter the company name")
                st.stop()

            input_dict = get_input_dict(
                st.session_state.work_directory,
                st.session_state.excel_file_path,
                st.session_state.company_name,
                st.session_state.company_size,
                company_sector,
            )

            model = HelloCredit(api_key, input_dict)
            st.session_state.output_dict = model.run_function()
            st.session_state.input_dict = input_dict
            st.session_state.run_progress_bar = True
            st.session_state.toast = True

            st.switch_page("pages/4_Credit_Watch.py")

    else:
        with st.expander("Metric Descriptions"):
            st.caption(
                "The model expects an Excel template with the following metrics.\
                Ensure the data is adjusted based on the company's size for accurate analysis by the model:"
            )

            metrics_info = {
                "Ebitda Margin": "Measures operational profitability as a percentage of revenue. EBITDA / Revenue * 100",
                "Total Assets": "Sum of all current and non-current assets owned by the company. Sum of all assets",
                "Sales Growth": "Year-over-year percentage increase in sales or revenue. (Current Sales - Prior Sales) / Prior Sales * 100",
                "Debt To Equity": "Ratio of total debt to shareholders' equity, indicating leverage. Total Debt / Shareholders' Equity * 100",
                "Debt To Ebitda": "Ratio of total debt to EBITDA, indicating ability to pay off debt. Total Debt / EBITDA",
                "Ebitda To Interest Expense": "Ratio of EBITDA to interest expense, showing ability to cover interest payments. EBITDA / Interest Expense",
                "Debt To Tangible Assets": "Ratio of total debt to tangible assets, showing leverage relative to physical assets. Total Debt / Tangible Assets",
                "Asset Turnover": "Ratio of revenue to average total assets, indicating efficiency of asset usage. Revenue / Average Total Assets",
                "Inventory To Cost Of Sales": "Ratio of average inventory to cost of goods sold, showing inventory management efficiency. Average Inventory / Cost of Goods Sold",
                "Cash To Assets": "Ratio of cash and cash equivalents to total assets, indicating liquidity. Cash and Cash Equivalents / Total Assets",
            }
            df = pd.DataFrame.from_dict(
                metrics_info, orient="index", columns=["Description"]
            )
            st.info("For optimal results, it is recommended to use data from the most recent 5 to 10 years/periods.")
            st.table(df)

            col_1, _, col_2 = st.columns(3)
            with col_1:
                create_download_button(
                    "public/creditwatch_small_medium_company_template.xlsx",
                    "Download Template\n\n(Small & Medium Company)",
                    "creditwatch_small_medium_company_template.xlsx",
                )
            with col_2:
                create_download_button(
                    "public/creditwatch_large_company_template.xlsx",
                    "Download Template\n\n(Large Company)",
                    "creditwatch_large_company_template.xlsx",
                )


if __name__ == "__main__":
    main()
