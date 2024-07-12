import os
import pandas as pd
import streamlit as st
import pandera as pa

def save_uploaded_file(uploaded_file):
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def _get_download_button():
    template_path = r"C:\Users\103763\Projects\HELLO_CREDIT\stienhoff_data.xlsx"

    with open(template_path, "rb") as template_file:
        template_bytes = template_file.read()

    st.download_button(
        label="Download Template",
        data=template_bytes,
        file_name="creditwatch_template.xlsx",
        mime="application/vnd.ms-excel"
    )


st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

st.markdown("#### CreditWatch.")
st.title("Upload Metrics")
st.write("")

company_name = st.text_input("Enter Company Name", "")
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    with st.spinner("Loading and processing file..."):
        file_path = save_uploaded_file(uploaded_file)
        
        try:
            df = pd.read_excel(file_path, index_col=[0, 1])
            df.columns = pd.to_datetime(df.columns)

            # Validate the dataset
            expected_entries = {
                "metrics":[
                    "debt_to_equity", "debt_to_ebitda", "ebitda_to_interest_expense",
                    "debt_to_tangible_assets", "asset_turnover", "inventory_to_cost_of_sales",
                    "cash_to_assets", "ebitda_margin", "total_assets", "sales_growth"
                ],
                "categories": [
                    "leverage_coverage_metrics", "efficiency_metrics", 
                    "profitability_metrics"
                ]
            }

            column_schema = {col: pa.Column(float) for col in df.columns}
            schema = pa.DataFrameSchema(
                columns=column_schema,
                index=pa.MultiIndex([
                    pa.Index(str, name="Metric Category"),
                    pa.Index(str, name="Metric Name", checks=[pa.Check.isin(expected_entries["metrics"])])
                ])
            )

            validated_df = schema.validate(df)
            
            st.success("File successfully loaded")
            st.session_state["excel_file_path"] = file_path
            #st.session_state["company_name"] = company_name.upper()
            
            st.markdown("### Preview of the dataset file:")
            st.dataframe(validated_df.head())
            
            if st.button("Load Model"):
                st.page_link("main.py", label="Home")

        except pa.errors.SchemaError as error:
            _get_download_button()
            st.error(
        f"""
        An error occurred while processing the file.
        Please make sure you're using the correct file format and try again.\n
        {error}
        """
        )
        
        except Exception as error:
            _get_download_button()
            st.error(
        f"""
        An error occurred while processing the file.
        Please make sure you're using the correct file format and try again.\n
        {error}
        """
        )


if not uploaded_file:
    with st.expander("Metric Descriptions"):
            
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

        df = pd.DataFrame.from_dict(metrics_info, orient='index').reset_index()
        df.columns = ['Metric', 'Description']
        st.table(df)

        _get_download_button()
        
     