import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Freshwater Sustainability Dashboard",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Global Freshwater Sustainability Dashboard")

st.markdown("""
This dashboard provides an interactive analysis of renewable internal freshwater
resources per capita across countries using World Bank Open Data.
""")
