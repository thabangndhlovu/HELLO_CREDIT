<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
=======
import os
import pandas as pd
import streamlit as st

def save_uploaded_file(uploaded_file):
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
>>>>>>> ba23da94d8bfcfd5aae80919534249ee04e336a8

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

<<<<<<< HEAD

st.title("Credit Risk Analysis Dashboard")

# Create two columns for layout


# # Key metrics in a single row
# metric1, metric2, metric3 = st.columns(3)
# metric1.metric("Rating", "A")
# metric2.metric("Score", "3.5")
# metric3.metric("Expected Loss", "0.10%")
=======
st.set_page_config(page_title="CreditWatch", page_icon="💳")
st.title("CreditWatch")
>>>>>>> ba23da94d8bfcfd5aae80919534249ee04e336a8

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
   with st.spinner("Loading and processing file..."):
      file_path = save_uploaded_file(uploaded_file)
      df = pd.read_excel(file_path)
   
   st.success("File successfully loaded!")
   st.session_state['excel_file_path'] = file_path

<<<<<<< HEAD
import plotly.graph_objects as go

def create_rating_gauge(score):
    ratings = ['Aaa', 'Aa', 'A', 'Baa', 'Ba', 'B', 'Caa', 'Ca', 'C']
    color_mapping = {
        "Aaa": "#6aa84f", "Aa": "#93c47d", "A": "#b6d7a8",
        "Baa": "#ffd966", "Ba": "#f6b26b", "B": "#e69138",
        "Caa": "#e06666", "Ca": "#cc0000", "C": "#990000",
    }
    
    # Create color steps based on the color mapping
    color_steps = [{'range': [i, i+1], 'color': color} for i, color in enumerate(color_mapping.values())]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 9], 'tickvals': list(range(9)), 'ticktext': ratings},
            'steps': color_steps,
            'threshold': {
                'line': {'color': "black", 'width': 6},
                'thickness': 1,
                'value': score
            },
            'bar': {
               'thickness': 1, 
               'color': "rgba(0,0,0,0.3)", # Set the gauge line to black with 30% opacity
               },  
        }
    ))
    
    
    fig.update_layout(
        height=400,
        font=dict(color="#052D3A"),
    )
    st.plotly_chart(fig, use_container_width=False)
    return fig

# # Example usage in Streamlit:
# score = 2.3  # This could be a variable or user input
# fig = create_rating_gauge(score)
# st.plotly_chart(fig, use_container_width=False)
=======
   st.subheader("Preview of the uploaded Excel file:")
   st.dataframe(df.head())

   if st.button("Load Model"):
      st.page_link("main.py", label="Home", icon="🏠")
>>>>>>> ba23da94d8bfcfd5aae80919534249ee04e336a8
