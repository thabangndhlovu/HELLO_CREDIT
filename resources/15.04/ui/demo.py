# import streamlit as st

# # Initialize session state for page navigation
# if 'page' not in st.session_state:
#     st.session_state.page = 'input_page'

# def go_to_model_page():
#     st.session_state.page = 'model_page'

# def go_back_to_input():
#     st.session_state.page = 'input_page'

# # Define the structure for the improved input page
# def input_page():
#     st.title("📈 Credit Default Prediction Model")
#     st.markdown("""
#     Welcome to the Credit Default Prediction Interface. 
#     Please input the necessary financial ratios below to assess the probability of bankruptcy. 
#                 Hover over the question marks next to each input field for more details on what to enter. 🚀
#     """)


    
#     income_statement_labels = {
#         "Revenue": "Total revenue generated from business activities.",
#         "Cost of Goods Sold": "Direct costs attributable to the production of the goods sold in the company.",
#         "Gross Profit": "Revenue minus the cost of goods sold.",
#         "Operating Expenses": "Expenses related to the operation of the business, excluding the cost of goods sold.",
#         "Operating Income": "Gross profit minus operating expenses.",
#         "Interest Expense": "The cost incurred by an entity for borrowed funds."
#     }

#     balance_sheet_labels = {
#         "Cash": "Amount of cash and cash equivalents.",
#         "Accounts Receivable": "Money owed to the company by its debtors.",
#         "Inventory": "Value of the company's inventory.",
#         "Total Current Assets": "Total value of all assets that can reasonably expect to be converted into cash within one year.",
#         "Total Assets": "Total value of all assets owned by the company.",
#         "Accounts Payable": "Money owed by the company to its creditors."
#     }

#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Income Statement")
#         for label, tooltip in income_statement_labels.items():
#             st.number_input(label, format="%f", help=tooltip, key=f"IS_{label}")

#     with col2:
#         st.subheader("Balance Sheet")
#         for label, tooltip in balance_sheet_labels.items():
#             st.number_input(label, format="%f", help=tooltip, key=f"BS_{label}")



#     liquidity_ratios = {
#         "Current Ratio": "Ability to pay off short-term liabilities with short-term assets. 🌊",
#         "Quick Ratio": "Ability to meet short-term liabilities with its most liquid assets. 💨"
#     }
    
#     efficiency_ratios = {
#         "Asset Turnover Ratio": "Sales generated for every dollar's worth of assets. 🔄",
#         "Inventory Turnover Ratio": "How quickly a company sells its inventory. 🛒"
#     }
    
#     probability_ratios = {
#         "Debt to Equity Ratio": "Company's financial leverage determined by dividing its total liabilities by stockholders' equity. ⚖️",
#         "Interest Coverage Ratio": "Ability to meet its interest expenses. 🔍"
#     }

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.subheader("Liquidity Ratios 💧")
#         for label, tooltip in liquidity_ratios.items():
#             st.number_input(label, format="%f", help=tooltip, key=f"LR_{label}")

#     with col2:
#         st.subheader("Efficiency Ratios ⚡")
#         for label, tooltip in efficiency_ratios.items():
#             st.number_input(label, format="%f", help=tooltip, key=f"ER_{label}")

#     with col3:
#         st.subheader("Probability Ratios 🎲")
#         for label, tooltip in probability_ratios.items():
#             st.number_input(label, format="%f", help=tooltip, key=f"PR_{label}")

#     st.write("---")
#     if st.button("Predict Default 🚀", on_click=go_to_model_page):
#         # This button will switch the page to the model output
#         pass

# # Define the structure for the model output page
# def model_page():
#     st.header("Model Output 📊")
#     st.write("Model results and bankruptcy probability will be displayed here.")

#     if st.button("Back to Input 🔙", on_click=go_back_to_input):
#         pass

# # Page routing
# if st.session_state.page == 'input_page':
#     input_page()
# elif st.session_state.page == 'model_page':
#     model_page()






# import streamlit as st

# # Initialize session state for page navigation
# if 'page' not in st.session_state:
#     st.session_state.page = 'input_page'

# def go_to_model_page():
#     st.session_state.page = 'model_page'

# def go_back_to_input():
#     st.session_state.page = 'input_page'

# # Define the structure for the improved input page
# def input_page():
#     # st.title("📈 Credit Default Prediction Model")
#     # st.markdown("""
#     # Welcome to the Credit Default Prediction Interface. 
#     # Please input the necessary financial ratios below to assess the Profitability of bankruptcy. 
#     # Hover over the question marks next to each input field for more details on what to enter. 🚀
#     # """)

#     # categories = {
#     #     "Income Statement": ["Revenue", "Cost of Goods Sold", "Operating Income", "EBITA (Earnings Before Interest, Taxes, and Amortization)", "Interest Expense", "Net Income"],
#     #     "Balance Sheet": ["Total Assets", "Total Debt"],
#     #     "Liquidity Ratios": ["Total Debt / EDITA", "Interest Coverage Ratio (EBITA / Interest Expense)"],
#     #     "Efficiency Ratios": ["Asset Turnover Ratio"],
#     #     "Profitability Ratios": ["Return on Assets", "Operating Margin Ratio", "Net Profit Margin"]
#     # }

#     # # Financial Statements input fields
#     # col1, col2 = st.columns(2)

#     # with col1:
#     #      st.subheader("Income Statement")
#     #      for label in categories["Income Statement"]:
#     #         st.number_input(label, format="%f", key=f"Income Statement_{label}")

#     # with col2:
#     #     st.subheader("Balance Sheet")
#     #     for label in categories["Balance Sheet"]:
#     #         st.number_input(label, format="%f", key=f"Balance Sheet_{label}")


#     # col1, col2, col3 = st.columns(3)
    
#     # with col1:
#     #     st.subheader("Profitability Ratios")
#     #     for label in categories["Profitability Ratios"]:
#     #         st.number_input(label, format="%f", key=f"Profitability Ratios_{label}")
   
#     # with col2:
#     #     st.subheader("Liquidity Ratios")
#     #     for label in categories["Liquidity Ratios"]:
#     #         st.number_input(label, format="%f", key=f"Liquidity Ratios_{label}")

#     # with col3:
#     #     st.subheader("Efficiency Ratios")
#     #     for label in categories["Efficiency Ratios"]:
#     #         st.number_input(label, format="%f", key=f"Efficiency Ratios_{label}")

# #     st.title("📈 Credit Default Prediction Model")
# #     st.markdown("""
# #     Welcome to the Credit Default Prediction Interface. 
# #     Please input the necessary financial figures below to assess the Profitability of bankruptcy. 
# #     Hover over the question marks next to each input field for more details on what to enter. 🚀
# #     """)

# #     categories = {
# #         "Income Statement": ["Revenue", "Cost of Goods Sold", "Operating Income", "EBITA (Earnings Before Interest, Taxes, and Amortization)", "Interest Expense", "Net Income"],
# #         "Balance Sheet": ["Total Assets", "Total Debt"]
# #     }

# #     # Financial Statements input fields
# #     col1, col2 = st.columns(2)

# #     income_statement_values = {}
# #     balance_sheet_values = {}

# #     with col1:
# #         st.subheader("Income Statement")
# #         for label in categories["Income Statement"]:
# #             income_statement_values[label] = st.number_input(label, format="%f", key=f"Income Statement_{label}")

# #     with col2:
# #         st.subheader("Balance Sheet")
# #         for label in categories["Balance Sheet"]:
# #             balance_sheet_values[label] = st.number_input(label, format="%f", key=f"Balance Sheet_{label}")

# #     # Calculate financial ratios if possible
# #     try:
# #         total_debt_edita_ratio = balance_sheet_values["Total Debt"] / income_statement_values["EBITA (Earnings Before Interest, Taxes, and Amortization)"]
# #         interest_coverage_ratio = income_statement_values["EBITA (Earnings Before Interest, Taxes, and Amortization)"] / income_statement_values["Interest Expense"]
# #         asset_turnover_ratio = income_statement_values["Revenue"] / balance_sheet_values["Total Assets"]
# #         return_on_assets = income_statement_values["Net Income"] / balance_sheet_values["Total Assets"]
# #         operating_margin_ratio = income_statement_values["Operating Income"] / income_statement_values["Revenue"]
# #         net_profit_margin = income_statement_values["Net Income"] / income_statement_values["Revenue"]
# #     except ZeroDivisionError:
# #         total_debt_edita_ratio, interest_coverage_ratio, asset_turnover_ratio, return_on_assets, operating_margin_ratio, net_profit_margin = (0, 0, 0, 0, 0, 0)

# #     # Display Calculated Ratios
# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         st.subheader("Profitability Ratios")
# #         st.metric("Return on Assets", f"{return_on_assets:.2f}")
# #         st.metric("Operating Margin Ratio", f"{operating_margin_ratio:.2f}")
# #         st.metric("Net Profit Margin", f"{net_profit_margin:.2f}")

# #     with col2:
# #         st.subheader("Liquidity Ratios")
# #         st.metric("Total Debt / EBITA", f"{total_debt_edita_ratio:.2f}")
# #         st.metric("Interest Coverage Ratio", f"{interest_coverage_ratio:.2f}")

# #     with col3:
# #         st.subheader("Efficiency Ratios")
# #         st.metric("Asset Turnover Ratio", f"{asset_turnover_ratio:.2f}")


# #     st.write("---")
# #     if st.button("Predict Default 🚀", on_click=go_to_model_page):
# #         pass

# # # Define the structure for the model output page
# # def model_page():
# #     st.header("Model Output 📊")
# #     st.write("Here are the inputs you provided for the prediction:")

# #     # Dynamically display the inputs based on session_state keys
# #     for category in ["Income Statement", "Balance Sheet", "Liquidity Ratios", "Efficiency Ratios", "Profitability Ratios"]:
# #         st.subheader(f"{category} Inputs")
# #         for key, value in st.session_state.items():
# #             if key.startswith(category):
# #                 label = key.split(f"{category}_")[1]  # Extract label from key
# #                 st.write(f"{label}: {value}")

# #     if st.button("Back to Input 🔙", on_click=go_back_to_input):
# #         pass

# # # Page routing
# # if st.session_state.page == 'input_page':
# #     input_page()
# # elif st.session_state.page == 'model_page':
# #     model_page()
