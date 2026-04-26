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
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Countries with Data</div>
        <div class="metric-value">{len(year_data)}</div>
        <div class="metric-sub">for year {selected_year}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card teal">
        <div class="metric-label">Global Average</div>
        <div class="metric-value">{global_avg:,.0f} m³</div>
        <div class="metric-sub">per capita</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Highest Availability</div>
        <div class="metric-value">{max_country['Country']}</div>
        <div class="metric-sub">{max_country['Freshwater']:,.0f} m³</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Most Water Scarce</div>
        <div class="metric-value">{min_country['Country']}</div>
        <div class="metric-sub">{min_country['Freshwater']:,.0f} m³</div>
    </div>
    """, unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
    "Country Rankings",
    "Trend Analysis",
    "Global Map",
    "Strategic Insights"
])

with tab1:
    st.subheader(f"Top {top_n} Countries — {selected_year}")

    top_data = year_data.nlargest(top_n, "Freshwater")

    fig_top = px.bar(
        top_data,
        x="Freshwater",
        y="Country",
        orientation="h",
        color="Freshwater",
        color_continuous_scale=chart_theme,
        template="plotly_white"
    )

    st.plotly_chart(fig_top, use_container_width=True)

    st.subheader(f"Bottom {top_n} Water Scarce Countries — {selected_year}")

    bottom_data = year_data.nsmallest(top_n, "Freshwater")

    fig_bottom = px.bar(
        bottom_data,
        x="Freshwater",
        y="Country",
        orientation="h",
        color="Freshwater",
        color_continuous_scale="Reds",
        template="plotly_white"
    )

    st.plotly_chart(fig_bottom, use_container_width=True)
    with tab2:
    st.subheader("Freshwater Resource Trends Over Time")

    if selected_countries:
        trend_df = df[df["Country Name"].isin(selected_countries)][
            ["Country Name"] + available_years
        ].copy()

        trend_long = trend_df.melt(
            id_vars="Country Name",
            value_vars=available_years,
            var_name="Year",
            value_name="Freshwater"
        )

        trend_long["Year"] = trend_long["Year"].astype(int)
        trend_long = trend_long.dropna()

        fig_line = px.line(
            trend_long,
            x="Year",
            y="Freshwater",
            color="Country Name",
            markers=True,
            template="plotly_white"
        )

        st.plotly_chart(fig_line, use_container_width=True)

    else:
        st.info("Please select at least one country from the sidebar.")
        with tab3:
    st.subheader(f"Global Freshwater Distribution Map ({selected_year})")

    fig_map = px.choropleth(
        year_data,
        locations="Country",
        locationmode="country names",
        color="Freshwater",
        hover_name="Country",
        color_continuous_scale="Blues",
        template="plotly_white"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
    <div class='map-tip'>
    <strong>How to read this map:</strong> Darker blue indicates higher freshwater availability per person.
    Hover over any country to see the exact value.
    </div>
    """, unsafe_allow_html=True)
    with tab4:
    st.subheader("Strategic Insights and Sustainability Findings")

    insights = [
        f"In {selected_year}, the global average freshwater availability was {global_avg:,.0f} m³ per person.",
        f"{max_country['Country']} recorded the highest freshwater availability at {max_country['Freshwater']:,.0f} m³ per capita.",
        f"{min_country['Country']} showed the lowest freshwater availability at {min_country['Freshwater']:,.0f} m³ per capita.",
        f"{below_avg} countries fall below the global average freshwater availability.",
        "Climate change and population growth are major reasons for freshwater scarcity."
    ]

    for item in insights:
        st.markdown(
            f"<div class='insight-box'>• {item}</div>",
            unsafe_allow_html=True
        )

    st.success(
        "Conclusion: Sustainable water resource management is essential for long-term environmental balance and human wellbeing."
    )
    with st.expander("View Raw Dataset"):
    st.dataframe(df, use_container_width=True)

fig_pie = px.pie(
    values=[below_avg, len(year_data) - below_avg],
    names=["Below Global Average", "Above Global Average"],
    hole=0.4,
    template="plotly_white"
)

st.plotly_chart(fig_pie, use_container_width=True)
