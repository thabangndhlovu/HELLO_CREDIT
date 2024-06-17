import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.markdown("""
### BANANA Capital Ltd. Credit Report

#### Company Overview
- **Name**: BANANA Capital Ltd.
- **Type**: Private Limited Company
- **Incorporation Date**: January 15, 2015
- **Registered Office**: 123 Fruit Street, London, UK
- **Industry**: Investment and Financial Services
- **Company Registration Number**: 0987654321

#### Executive Summary
BANANA Capital Ltd. is a private investment and financial services company specializing in venture capital, private equity, and asset management. The company has shown steady growth since its incorporation, with a diverse portfolio in technology, healthcare, and renewable energy sectors.

#### Financial Performance
- **Revenue (2023)**: £50 million
- **Net Income (2023)**: £7.5 million
- **Total Assets**: £200 million
- **Total Liabilities**: £100 million
- **Shareholder's Equity**: £100 million

#### Key Financial Ratios
- **Current Ratio**: 2.5
- **Debt-to-Equity Ratio**: 1.0
- **Return on Equity (ROE)**: 7.5%
- **Net Profit Margin**: 15%

#### Credit Rating
- **Credit Rating**: A (Stable)
- **Rating Agency**: ABC Credit Rating Agency

#### Credit History
BANANA Capital Ltd. has maintained a positive credit history with no significant defaults or late payments reported. The company has a history of prudent financial management, reflected in its strong financial ratios and stable credit rating.

#### Key Management
- **CEO**: John Smith
- **CFO**: Jane Doe
- **COO**: Michael Brown

#### Operational Highlights
- **Key Investments**: Technology startups, green energy projects, healthcare innovations
- **Recent Acquisitions**: Acquired a 20% stake in GreenTech Innovations Ltd. (2022)
- **Strategic Partnerships**: Partnered with XYZ Bank for co-investment opportunities

#### Risk Factors
- **Market Risk**: Exposure to market volatility, particularly in the tech sector
- **Credit Risk**: Moderate, due to a diversified portfolio and stable financial performance
- **Regulatory Risk**: Compliance with financial regulations in multiple jurisdictions

#### Conclusion
BANANA Capital Ltd. is a financially stable and well-managed company with a solid track record in the investment and financial services industry. The company’s prudent financial practices and diverse investment portfolio position it well for continued growth and stable returns. The current credit rating of A (Stable) reflects confidence in the company’s ability to meet its financial obligations and sustain its operational success.

""")

import pandas as pd
import streamlit as st



import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
    }
)

data = st.data_editor(
    data_df,
    column_config={
        "widgets": st.column_config.TextColumn(
            "Widgets",
            help="Streamlit **widget** commands 🎈",
            default="st.",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
    },
    hide_index=True,
)

import streamlit as st
import pandas as pd
import random


# Create a sample DataFrame with financial ratios
data_df = pd.DataFrame({
    "Ratio": ["Current Ratio", "Quick Ratio", "Debt-to-Equity Ratio", "Return on Equity"],
    "Value": [0.0, 0.0, 0.0, 0.0]
})

# Function to generate random values for the ratios
def generate_random_values():
    data_df["Value"] = [random.uniform(0.5, 2.0) for _ in range(len(data_df))]

st.title("Financial Ratios App")

# Display the data editor
edited_df = st.data_editor(
    data_df,
    column_config={
        "Value": st.column_config.NumberColumn(
            "Value",
            help="Enter the value for the financial ratio",
            format="{:.2f}",
            min_value=0.0,
            step=0.01,
        )
    },
    hide_index=True,
)

# Button to generate random values
if st.button("Generate Random Values"):
    generate_random_values()

# Display the updated DataFrame
st.write("Updated Financial Ratios:")
st.dataframe(edited_df)