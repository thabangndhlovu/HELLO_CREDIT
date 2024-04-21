import streamlit as st
import pandas as pd



# Initialize session state for page navigation and storing inputs
st.title("Page 2")

st.page_link("main.py", label="Home", icon="🏠")

data = pd.DataFrame([1, 2, 3, 4, 5])

data = r"C:\Users\Thabang Ndhlovu\Projects\HELLO_CREDIT\resources\Riskcalcu for private companies.pdf"
url = "www.google.com"

st.button("Click me")
st.download_button("Download file", data)
st.link_button("Go to gallery", url)
st.page_link("main.py", label="Home")
#st.data_editor("Edit data", data)
st.checkbox("I agree")
st.toggle("Enable")
st.radio("Pick one", ["cats", "dogs"])
st.selectbox("Pick one", ["cats", "dogs"])
st.multiselect("Buy", ["milk", "apples", "potatoes"])
st.slider("Pick a number", 0, 100)
st.select_slider("Pick a size", ["S", "M", "L"])
st.text_input("First name")
st.number_input("Pick a number", 0, 10)
st.text_area("Text to translate")
st.date_input("Your birthday")
st.time_input("Meeting time")
st.file_uploader("Upload a CSV")
st.camera_input("Take a picture")
st.color_picker("Pick a color")