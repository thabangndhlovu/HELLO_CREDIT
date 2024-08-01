import plotly.graph_objects as go
import streamlit as st

MAPPED_RATINGS = [
    ("Aaa", 2.5),
    ("Aa", 3.5),
    ("A", 4.5),
    ("Baa", 5.5),
    ("Ba", 6.5),
    ("B", 7.5),
    ("Caa", 8.5),
    ("Ca", 9.5),
    ("C", float("inf")),
]

RATING_META = {
    "Score Range": ["≤ 2.5", "≤ 3.5", "≤ 4.5", "≤ 5.5", "≤ 6.5", "≤ 7.5", "≤ 8.5", "≤ 9.5", "> 9.5"],
    "Rating": ["Aaa", "Aa", "A", "Baa", "Ba", "B", "Caa", "Ca", "C"],
    "Description": [
        "Issuers assessed Aaa are judged to have the highest intrinsic, or standalone, financial strength, and thus subject to the lowest level of credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Aa are judged to have high intrinsic, or standalone, financial strength, and thus subject to very low credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed A are judged to have upper-medium-grade intrinsic, or standalone, financial strength, and thus subject to low credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Baa are judged to have medium-grade intrinsic, or standalone, financial strength, and thus subject to moderate credit risk and, as such, may possess certain speculative credit elements absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Ba are judged to have speculative intrinsic, or standalone, financial strength, and are subject to substantial credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed B are judged to have speculative intrinsic, or standalone, financial strength, and are subject to high credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Caa are judged to have speculative intrinsic, or standalone, financial strength, and are subject to very high credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Ca have highly speculative intrinsic, or standalone, financial strength, and are likely to be either in, or very near, default, with some prospect for recovery of principal and interest; or, these issuers have avoided default or are expected to avoid default through the provision of extraordinary support from an affiliate or a government.",
        "Issuers assessed C are typically in default, with little prospect for recovery of principal or interest; or, these issuers are benefiting from a government or affiliate support but are likely to be liquidated over time; without support there would be little prospect for recovery of principal or interest."
    ],
    "Probability of Default": ["0.00%", "0.01%", "0.10%", "0.46%", "2.31%", "7.62%", "17.86%", "50.00%", "100.00%"]
}

COLOR_MAPPING = {
    "Aaa": "#6aa84f", "Aa": "#93c47d", "A": "#b6d7a8", "Baa": "#ffd966", 
    "Ba": "#f6b26b", "B": "#e69138", "Caa": "#e06666", "Ca": "#cc0000", 
    "C": "#990000",
}

import plotly.graph_objects as go


import plotly.graph_objects as go

def create_credit_rating_chart(credit_rating, credit_score):
    fig = go.Figure()

    # Add colored rectangles for each rating
    shapes = []
    for i, (r, upper_bound) in enumerate(MAPPED_RATINGS):
        x0 = 0 if i == 0 else MAPPED_RATINGS[i-1][1]
        x1 = 10 #upper_bound if upper_bound != float("inf") else 10  # Set max to 10 for 'C' rating
        shapes.append(
            go.layout.Shape(
                type="rect",
                x0=x0,
                x1=x1,
                y0=0,
                y1=1,
                fillcolor=COLOR_MAPPING[r],
                line_width=0,
                layer="below"
            )
        )

    # Add vertical line for the score
    shapes.append(
        go.layout.Shape(
            type="line",
            x0=credit_score,
            x1=credit_score,
            y0=0,
            y1=1,
            line=dict(color="black", width=3)
        )
    )

    # Customize layout
    fig.update_layout(
        shapes=shapes,
        xaxis=dict(
            title="Score",
            title_standoff=25,
            range=[0, 10],
            tickvals=[r[1] for r in MAPPED_RATINGS[:-1]] + [10],
            ticktext=[r[0] for r in MAPPED_RATINGS],
            tickangle=0,
            tickmode='array',
            tickfont=dict(size=10),
            title_font=dict(size=12)
        ),
        yaxis=dict(visible=False),
        height=150,
        margin=dict(l=20, r=20, t=60, b=40),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def main():

    rating = "B"
    score = 5.1

    fig = create_credit_rating_chart(rating, score)
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()