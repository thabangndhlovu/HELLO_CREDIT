import streamlit as st


st.title("Predictive Default Risk Assessor")

doc = """Expected to have extremely conservative financial policies; very stable metrics; public commitment to very strong credit profile over the long term."""
rating = "Aa"

st.page_link("pages/credit_description.py", label="Credit Description")

col_1, col_2 = st.columns(2)
with col_1:
    st.write(doc)

with col_2:
    with st.container(border=True, height=150):
        st.metric("", rating, -0)

st.write("---")


sector = st.selectbox("Select the sector of the company", ["Corporates", "Financial Institutions", "Funds & Asset Management", "Infrastructure & Project Finance", "Insurance", "Other"])


tab_1, tab_2, tab_3 = st.tabs(["Risk Calc", "Factor Weights", "Rating History"])


with tab_1:
    st.subheader("Financial Metrics")
    st.write(doc)

    col_1, col_2 = st.columns(2)

    with col_1:
        for metric in ["Debt/Equity", "Operational Margin", "Asset Turnover"]:
            st.number_input(metric)


 

with tab_2:
    st.subheader("Factor Weights")
    st.write(doc)

    col_1, col_2 = st.columns(2)

    with col_1:
        for metric in ["Profitability", "Leverage & Coverage", "Efficiency"]:
            st.number_input(metric)

    with col_2:
        st.write(doc)

with tab_3:
    st.subheader("Rating History")
    st.write(doc)




        
st.page_link("pages/page_2.py", label="Credit Description")


#st.page_link("main.py", label="Home", icon="🏠")
#st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.com", label="Google", icon="🌎")

