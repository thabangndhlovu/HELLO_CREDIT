import streamlit as st
import pandas as pd

st.page_link("main.py", label="Back")

st.title("Credit Descriptions")


# Define the data
data = {
    "Score Range": ["≤ 1.5", "≤ 2.5", "≤ 3.5", "≤ 4.5", "≤ 5.5", "≤ 6.5", "≤ 7.5", "≤ 8.5", "> 8.5"],
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
    ]
}

# Define the color mapping dictionary
color_mapping = {
    "Aaa": "#6aa84f",  # Green for highest rating
    "Aa": "#93c47d",
    "A": "#b6d7a8",
    "Baa": "#ffd966",  # Yellow for middle rating
    "Ba": "#f6b26b",
    "B": "#e69138",
    "Caa": "#e06666",  # Red for lower rating
    "Ca": "#cc0000",
    "C": "#990000",
}

# Optimized coloring function using the dictionary
def color_rating_optimized(value):
    return f"background-color: {color_mapping.get(value)}"

# Apply the coloring function to the DataFrame
credit_ratings_df = pd.DataFrame(data)
styled_df = credit_ratings_df.style.applymap(color_rating_optimized, subset=["Rating"])
st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

