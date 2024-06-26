import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


st.title("Credit Risk Analysis Dashboard")

# Create two columns for layout


# # Key metrics in a single row
# metric1, metric2, metric3 = st.columns(3)
# metric1.metric("Rating", "A")
# metric2.metric("Score", "3.5")
# metric3.metric("Expected Loss", "0.10%")



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
