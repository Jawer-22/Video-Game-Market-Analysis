# 🎮 Video Game Market Analysis

An exploratory data analysis (EDA) project that uncovers patterns and trends in the global video game market using sales data for **16,000+ games** spanning 1980–2016.

## 📌 Project Overview

This project analyzes the **VGChartz** video game sales dataset to answer questions like:

- Which genres and platforms dominate the market?
- How did the gaming industry evolve across decades?
- How do regional markets (NA, EU, JP) differ in taste?
- Which publishers control the most market share?
- What makes a game a mega-hit?

The focus is **EDA and business insights**, not machine learning.

## 📁 Project Structure

```
video-game-market-analysis/
│
├── Data/
│   ├── raw/vgsales.csv              # Original dataset
│   └── processed/cleaned_vgsales.csv # Cleaned + feature-engineered
│
├── Notebooks/
│   ├── 01_data_understanding.ipynb   # Dataset exploration & overview
│   ├── 02_data_cleaning.ipynb        # Handling missing values, types
│   ├── 03_feature_engineering.ipynb   # Creating analytical features
│   └── 04_exploratory_data_analysis.ipynb  # Deep EDA & insights
│
├── WebApp/
│   └── streamlit_app.py              # Interactive dashboard
│
├── README.md
├── requirements.txt
└── .gitignore
```

## 📊 Dataset

| Column | Description |
|---|---|
| `Rank` | Overall sales ranking |
| `Name` | Game title |
| `Platform` | Platform (PS4, Wii, X360, etc.) |
| `Year` | Release year |
| `Genre` | Genre (Action, Sports, RPG, etc.) |
| `Publisher` | Publisher name |
| `NA_Sales` | North America sales (millions) |
| `EU_Sales` | Europe sales (millions) |
| `JP_Sales` | Japan sales (millions) |
| `Other_Sales` | Rest of world sales (millions) |
| `Global_Sales` | Total worldwide sales (millions) |

**Source**: https://www.kaggle.com/datasets/gregorut/videogamesales

## 🎮 Platform Reference

| Abbreviation | Full Form |
|---|---|
| **2600** | Atari 2600 |
| **3DO** | 3DO Interactive Multiplayer |
| **3DS** | Nintendo 3DS |
| **DC** | Sega Dreamcast |
| **DS** | Nintendo DS |
| **GB** | Game Boy |
| **GBA** | Game Boy Advance |
| **GC** | Nintendo GameCube |
| **GEN** | Sega Genesis |
| **GG** | Sega Game Gear |
| **N64** | Nintendo 64 |
| **NES** | Nintendo Entertainment System |
| **NG** | Neo Geo |
| **PC** | Personal Computer |
| **PCFX** | PC-FX |
| **PS** | PlayStation |
| **PS2** | PlayStation 2 |
| **PS3** | PlayStation 3 |
| **PS4** | PlayStation 4 |
| **PSP** | PlayStation Portable |
| **PSV** | PlayStation Vita |
| **SAT** | Sega Saturn |
| **SCD** | Sega CD |
| **SNES** | Super Nintendo Entertainment System |
| **TG16** | TurboGrafx-16 |
| **WS** | WonderSwan |
| **Wii** | Nintendo Wii |
| **WiiU** | Nintendo Wii U |
| **X360** | Xbox 360 |
| **XB** | Xbox |
| **XOne** | Xbox One |

## 🔍 Key Insights

### Genre
- **Action** dominates in both volume and revenue
- **Platform** games have the highest average sales per title
- Genre preferences vary by region: Shooters → NA, RPGs → Japan, Sports → EU

### Platforms
- **PS2** is the all-time sales leader
- Each platform follows a ~6–8 year lifecycle
- The **Wii** had the most dramatic rise and fall

### Market Trends
- The market peaked around **2008–2009** and declined after
- Average sales per game dropped as the market became more crowded
- The 2000s were the **golden age** of console gaming

### Regional Patterns
- **North America** accounts for ~49% of global sales
- NA and EU are highly correlated; **Japan** is a distinct market
- Japan uniquely favors RPGs and Nintendo franchises

### Publishers
- Top 5 publishers control **~50%+ of total sales**
- **Nintendo** leads with the strongest first-party catalog

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- pip
- Run the following website to view the dashboard:
https://video-game-market-analysis-wkpjt3la7xcp7urmtcufms.streamlit.app/
## 🛠️ Technologies Used

| Tool | Purpose |
|---|---|
| **Python** | Core language |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical operations |
| **Matplotlib** | Static visualizations |
| **Seaborn** | Statistical visualizations |
| **Plotly** | Interactive charts |
| **Streamlit** | Web dashboard |
| **Jupyter** | Notebook environment |

## 📝 Notebook Workflow

1. **Data Understanding** — Explore dataset structure, types, statistics, and formulate questions
2. **Data Cleaning** — Handle missing values, fix types, validate data integrity
3. **Feature Engineering** — Create Game Age, Release Decade, Top Region, Platform Era, Sales Category
4. **Exploratory Data Analysis** — 8 sections of deep analysis with visualizations and insights
