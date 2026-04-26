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
@st.cache_data
def load_data():
    df = pd.read_csv("freshwater.csv", skiprows=4)

    exclude = [
        "World", "OECD", "Arab World", "Africa", "Asia",
        "Europe", "income", "IDA", "IBRD", "blend", "Euro area"
    ]

    mask = df["Country Name"].apply(
        lambda x: not any(e.lower() in str(x).lower() for e in exclude)
    )

    df = df[mask].copy()

    year_cols = [col for col in df.columns if col.isdigit()]

    return df, year_cols


df, year_cols = load_data()
available_years = [y for y in year_cols if not df[y].isna().all()]
