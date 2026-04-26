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
with st.sidebar:
    st.header("Dashboard Controls")

    selected_year = st.select_slider(
        "Select Analysis Year",
        options=available_years,
        value="2020" if "2020" in available_years else available_years[-1]
    )

    selected_countries = st.multiselect(
        "Compare Countries",
        options=sorted(df["Country Name"].dropna().unique().tolist()),
        default=["Sri Lanka", "India", "Australia"]
    )

    top_n = st.slider(
        "Top Countries Ranking",
        min_value=5,
        max_value=20,
        value=10
    )

    st.markdown("---")
    st.markdown("### Dataset Information")
    st.markdown("""
**Source:** World Bank Open Data  
**Indicator:** ER.H2O.INTR.PC  

Renewable Internal Freshwater Resources per Capita
""")
    year_data = df[["Country Name", selected_year]].dropna()
year_data.columns = ["Country", "Freshwater"]
year_data = year_data[year_data["Freshwater"] > 0]

global_avg = year_data["Freshwater"].mean()
max_country = year_data.loc[year_data["Freshwater"].idxmax()]
min_country = year_data.loc[year_data["Freshwater"].idxmin()]
below_avg = (year_data["Freshwater"] < global_avg).sum()
