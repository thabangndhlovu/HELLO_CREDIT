import plotly.graph_objects as go
import streamlit as st

COLOR_MAPPING = {
    "Aaa": "#6aa84f", "Aa": "#93c47d", "A": "#b6d7a8", "Baa": "#ffd966",
    "Ba": "#f6b26b", "B": "#e69138", "Caa": "#e06666", "Ca": "#cc0000",
    "C": "#990000",
}

RATINGS = ["C", "Ca", "Caa", "B", "Ba", "Baa", "A", "Aa", "Aaa"]

def create_credit_rating_gauge(credit_rating):
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=RATINGS.index(credit_rating),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Credit Rating: {credit_rating}", 'font': {'size': 24}},
        gauge={
            'axis': {
                'range': [0, len(RATINGS) - 1],
                'tickmode': 'array',
                'tickvals': list(range(len(RATINGS))),
                'ticktext': RATINGS,
                'tickwidth': 1,
                'tickcolor': "white",
            },
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [i, i+1], 'color': COLOR_MAPPING[rating]} 
                for i, rating in enumerate(RATINGS)
            ],
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="white",
    )
    
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title("Credit Rating Gauge")
    
    credit_rating = "B"
    fig = create_credit_rating_gauge(credit_rating)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})




import plotly.graph_objects as go
import numpy as np
import streamlit as st

def create_risk_assessment_chart(score, min_score=-200, max_score=1200):
    # Create color scale
    colors = ['red', 'orange', 'yellow', 'yellowgreen', 'green']
    n_colors = len(colors)
    color_scale = [(i/(n_colors-1), color) for i, color in enumerate(colors)]

    # Create the base chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Comprehensive Score", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [min_score, max_score], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue", 'thickness': 0.01},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [min_score, max_score], 'color': 'rgba(0,0,0,0)'}
            ],
            'threshold': {
                'line': {'color': "darkblue", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    # Add color gradient
    for i in range(100):
        fig.add_shape(
            type="line",
            x0=i/100, y0=0.05, x1=i/100, y1=0.15,
            line=dict(color=f"hsl({120-(i*1.2)},100%,50%)", width=4)
        )

    # Customize layout
    fig.update_layout(
        paper_bgcolor = "white",
        font = {'color': "darkblue", 'family': "Arial"},
        height=300,
        margin=dict(l=10, r=10, t=60, b=30)
    )

    # Add text annotations
    fig.add_annotation(x=0, y=-0.15, xref="paper", yref="paper",
                       text="Increased risk", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=1, y=-0.15, xref="paper", yref="paper",
                       text="Reduced risk", showarrow=False, font=dict(size=14))

    return fig

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Risk Assessment Chart")
    
    score = 942  # Example score
    fig = create_risk_assessment_chart(score)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

if __name__ == "__main__":
    main()

    
if __name__ == "__main__":
    main()