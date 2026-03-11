"""
🎮 Video Game Market Analysis — Interactive Dashboard
=====================================================
An interactive analytics tool to explore the global video game market.
Built with Streamlit + Plotly.

Run: streamlit run WebApp/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────── Page Config ───────────────────────
st.set_page_config(
    page_title="Video Game Market Analysis",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────── Custom CSS ───────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        padding: 0.5rem 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: white;
        text-align: center;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────── Load Data ───────────────────────
@st.cache_data
def load_data():
    """Load the cleaned dataset."""
    # Try multiple paths for flexibility
    paths = [
        Path(__file__).parent.parent / "Data" / "processed" / "cleaned_vgsales.csv",
        Path("Data/processed/cleaned_vgsales.csv"),
        Path("../Data/processed/cleaned_vgsales.csv"),
    ]
    for p in paths:
        if p.exists():
            df = pd.read_csv(p)
            return df
    
    # Fallback: generate cleaned data from raw
    raw_paths = [
        Path(__file__).parent.parent / "Data" / "raw" / "vgsales.csv",
        Path(__file__).parent.parent / "Data" / "vgsales.csv",
        Path("Data/raw/vgsales.csv"),
        Path("Data/vgsales.csv"),
    ]
    for p in raw_paths:
        if p.exists():
            df = pd.read_csv(p)
            df = df.dropna(subset=["Year"])
            df["Year"] = df["Year"].astype(int)
            df["Publisher"] = df["Publisher"].fillna("Unknown")
            return df
    
    st.error("Dataset not found. Please ensure vgsales.csv is in the Data folder.")
    st.stop()


df = load_data()

# ─────────────────────── Sidebar Filters ───────────────────────
st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown("Use these filters to explore the dataset interactively.")

# Year range
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider(
    "📅 Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
)

# Genre
all_genres = sorted(df["Genre"].unique())
selected_genres = st.sidebar.multiselect(
    "🎯 Genre",
    options=all_genres,
    default=all_genres,
)

# Platform
all_platforms = sorted(df["Platform"].unique())
selected_platforms = st.sidebar.multiselect(
    "🕹️ Platform",
    options=all_platforms,
    default=all_platforms,
)

# Publisher (top 30 + 'Other')
top_publishers = df["Publisher"].value_counts().head(30).index.tolist()
publisher_options = ["All"] + top_publishers
selected_publisher = st.sidebar.selectbox("🏢 Publisher", options=publisher_options)

# ─────────────────────── Apply Filters ───────────────────────
mask = (
    (df["Year"] >= year_range[0])
    & (df["Year"] <= year_range[1])
    & (df["Genre"].isin(selected_genres))
    & (df["Platform"].isin(selected_platforms))
)
if selected_publisher != "All":
    mask &= df["Publisher"] == selected_publisher

filtered = df[mask].copy()

# ─────────────────────── Header ───────────────────────
st.markdown('<p class="main-header">🎮 Video Game Market Analysis</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Explore the global video game market through interactive visualizations</p>',
    unsafe_allow_html=True,
)

# ─────────────────────── KPI Metrics ───────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🎮 Games", f"{len(filtered):,}")
col2.metric("💰 Total Sales", f"${filtered['Global_Sales'].sum():,.0f}M")
col3.metric("📊 Avg Sales", f"${filtered['Global_Sales'].mean():.2f}M")
col4.metric("🕹️ Platforms", f"{filtered['Platform'].nunique()}")
col5.metric("🏢 Publishers", f"{filtered['Publisher'].nunique()}")

st.markdown("---")

# ─────────────────────── Row 1: Genre & Platform ───────────────────────
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("🎯 Genre Sales Distribution")
    genre_sales = (
        filtered.groupby("Genre")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_genre = px.bar(
        genre_sales,
        x="Global_Sales",
        y="Genre",
        orientation="h",
        color="Global_Sales",
        color_continuous_scale="Viridis",
        labels={"Global_Sales": "Sales (M)", "Genre": ""},
    )
    fig_genre.update_layout(
        height=400, showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_genre, use_container_width=True)

with row1_col2:
    st.subheader("🕹️ Platform Sales Comparison")
    plat_sales = (
        filtered.groupby("Platform")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )
    fig_plat = px.bar(
        plat_sales,
        x="Platform",
        y="Global_Sales",
        color="Global_Sales",
        color_continuous_scale="Magma",
        labels={"Global_Sales": "Sales (M)", "Platform": ""},
    )
    fig_plat.update_layout(
        height=400, showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_plat, use_container_width=True)

st.markdown("---")

# ─────────────────────── Row 2: Regional & Trends ───────────────────────
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🌍 Regional Sales Breakdown")
    regional = pd.DataFrame({
        "Region": ["North America", "Europe", "Japan", "Other"],
        "Sales": [
            filtered["NA_Sales"].sum(),
            filtered["EU_Sales"].sum(),
            filtered["JP_Sales"].sum(),
            filtered["Other_Sales"].sum(),
        ],
    })
    fig_reg = px.pie(
        regional,
        values="Sales",
        names="Region",
        color="Region",
        color_discrete_map={
            "North America": "#3498db",
            "Europe": "#2ecc71",
            "Japan": "#e74c3c",
            "Other": "#f39c12",
        },
        hole=0.4,
    )
    fig_reg.update_traces(textposition="outside", textinfo="percent+label")
    fig_reg.update_layout(
        height=400, showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_reg, use_container_width=True)

with row2_col2:
    st.subheader("📈 Sales Trends Over Time")
    trend = (
        filtered.groupby("Year")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]]
        .sum()
        .reset_index()
    )
    fig_trend = go.Figure()
    colors = {"NA_Sales": "#3498db", "EU_Sales": "#2ecc71",
              "JP_Sales": "#e74c3c", "Other_Sales": "#f39c12"}
    names = {"NA_Sales": "North America", "EU_Sales": "Europe",
             "JP_Sales": "Japan", "Other_Sales": "Other"}
    for col in ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]:
        fig_trend.add_trace(go.Scatter(
            x=trend["Year"], y=trend[col],
            mode="lines+markers", name=names[col],
            line=dict(color=colors[col], width=2),
            marker=dict(size=4),
            stackgroup="one",
        ))
    fig_trend.update_layout(
        height=400,
        xaxis_title="Year", yaxis_title="Sales (Millions)",
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# ─────────────────────── Row 3: Top Games Leaderboard ───────────────────────
st.subheader("🏆 Top Selling Games Leaderboard")

leaderboard_count = st.slider("Number of games to show", 10, 50, 20)
top_games = filtered.nlargest(leaderboard_count, "Global_Sales")[
    ["Rank", "Name", "Platform", "Year", "Genre", "Publisher",
     "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
].reset_index(drop=True)
top_games.index += 1
top_games.index.name = "#"

# Color the top game
fig_lb = px.bar(
    top_games.head(20),
    x="Global_Sales",
    y="Name",
    orientation="h",
    color="Genre",
    hover_data=["Platform", "Year", "Publisher"],
    labels={"Global_Sales": "Global Sales (M)", "Name": ""},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_lb.update_layout(
    height=500, yaxis=dict(autorange="reversed"),
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", y=-0.12),
)
st.plotly_chart(fig_lb, use_container_width=True)

# Table
with st.expander("📋 View Full Leaderboard Table"):
    st.dataframe(
        top_games.style.format({
            "NA_Sales": "{:.2f}M",
            "EU_Sales": "{:.2f}M",
            "JP_Sales": "{:.2f}M",
            "Other_Sales": "{:.2f}M",
            "Global_Sales": "{:.2f}M",
        }),
        use_container_width=True,
        height=400,
    )

st.markdown("---")

# ─────────────────────── Row 4: Genre by Region Heatmap ───────────────────────
st.subheader("🗺️ Genre Popularity by Region")

genre_region = filtered.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum()
genre_region.columns = ["North America", "Europe", "Japan", "Other"]

fig_heat = px.imshow(
    genre_region,
    color_continuous_scale="YlOrRd",
    aspect="auto",
    labels=dict(x="Region", y="Genre", color="Sales (M)"),
)
fig_heat.update_layout(
    height=450,
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig_heat, use_container_width=True)

# ─────────────────────── Footer ───────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#aaa; font-size:0.85rem;'>"
    "📊 Video Game Market Analysis | Data Source: VGChartz | "
    "Built with Streamlit & Plotly"
    "</p>",
    unsafe_allow_html=True,
)
