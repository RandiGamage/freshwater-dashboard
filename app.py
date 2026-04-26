import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Global Freshwater Sustainability Dashboard",
    page_icon="💧",
    layout="wide",
)

# Header
st.title("💧 Global Freshwater Sustainability Dashboard")

st.markdown("""
This dashboard provides an interactive analysis of renewable internal freshwater 
resources per capita across countries using World Bank Open Data.

It helps identify water-rich nations, water-scarce regions, and supports 
sustainable development decision-making through data visualization.
""")

# Load Data
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

# Sidebar
with st.sidebar:
    st.header("Dashboard Controls")

    available_years = [y for y in year_cols if not df[y].isna().all()]

    selected_year = st.select_slider(
        "Select Analysis Year",
        options=available_years,
        value="2020" if "2020" in available_years else available_years[-1]
    )

# Selected Year Data
year_data = df[["Country Name", selected_year]].dropna()
year_data.columns = ["Country", "Freshwater"]
year_data = year_data[year_data["Freshwater"] > 0]

# Summary Metrics
global_avg = year_data["Freshwater"].mean()
max_country = year_data.loc[year_data["Freshwater"].idxmax()]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background:#ffffff;
        padding:20px;
        border-radius:15px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        border:1px solid #d6eaf8;
    ">
        <h4 style="color:#2e86c1;">Countries with Available Data</h4>
        <h1 style="color:#154360;">{len(year_data)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background:#ffffff;
        padding:20px;
        border-radius:15px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        border:1px solid #d6eaf8;
    ">
        <h4 style="color:#2e86c1;">Global Average</h4>
        <h1 style="color:#154360;">{global_avg:,.0f} m³</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background:#ffffff;
        padding:20px;
        border-radius:15px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        border:1px solid #d6eaf8;
    ">
        <h4 style="color:#2e86c1;">Highest Availability</h4>
        <h1 style="color:#154360;">{max_country['Country']}</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# Tabs
tab1, tab2 = st.tabs([
    "Country Rankings",
    "Trend Analysis"
])

# TAB 1 - Country Rankings
with tab1:
    st.subheader(f"Leading Countries in Freshwater Availability ({selected_year})")

    top_data = year_data.nlargest(10, "Freshwater")

    fig_top = px.bar(
        top_data,
        x="Freshwater",
        y="Country",
        orientation="h",
        color="Freshwater",
        color_continuous_scale="Blues",
        template="plotly_white"
    )

    st.plotly_chart(fig_top, use_container_width=True)

# TAB 2 - Trend Analysis
with tab2:
    st.subheader("Freshwater Resource Trends")

    st.info("Trend analysis section will be added in the next commit.")
