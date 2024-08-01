import pandas as pd
import streamlit as st

from hellocredit.helpers import COLOR_MAPPING, RATING_META

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.markdown("#### CreditWatch.")
st.title("Credit Rating Descriptions")

df = pd.DataFrame(RATING_META)
styled_df = df.style.applymap(lambda v: f"background-color: {COLOR_MAPPING.get(v, '')}", subset=["Rating"])
st.write(styled_df.to_html(index=False, escape=False), unsafe_allow_html=True)

st.caption("*Rating scale, Descriptions and Expected Loss percentages are \
    extrapolated from Moody's Loss Given Default for Speculative-Grade Companies (2015).")

if st.button("Back", type="primary", use_container_width=True):
  st.switch_page("pages/credit_watch.py")