import streamlit as st


st.set_page_config(
    page_title="Welcome Page", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
# CreditWatch.
#
""")

if st.button("Get Started", key="upload_data_button", help="Upload your data and start credit-watching!", type="primary", use_container_width=True):
    st.switch_page("pages/3_Upload_Data.py")

if st.button("Documentation", key="documentation_button", help="View the documentation", use_container_width=True):
    st.switch_page("pages/2_Documentation.py")

st.markdown("""
---
### Need Help?
If you have any questions or need assistance, please don't hesitate to \
[contact me](mailto:thabang.ndhlovu@sasfin.com).- always happy to chat and help out! 😊
""", 
)