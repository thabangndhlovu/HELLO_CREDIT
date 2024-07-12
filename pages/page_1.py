import os
import pandas as pd
import streamlit as st

def save_uploaded_file(uploaded_file):
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

st.set_page_config(page_title="CreditWatch", page_icon="💳")
st.title("CreditWatch")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
   with st.spinner("Loading and processing file..."):
      file_path = save_uploaded_file(uploaded_file)
      df = pd.read_excel(file_path)
   
   st.success("File successfully loaded!")
   st.session_state['excel_file_path'] = file_path

   st.subheader("Preview of the uploaded Excel file:")
   st.dataframe(df.head())

   if st.button("Load Model"):
      st.page_link("main.py", label="Home", icon="🏠")
