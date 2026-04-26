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