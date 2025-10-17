# 🚦 NVDB Traffic Insights

Comprehensive analysis of Norwegian road traffic patterns, COVID-19 impact assessment, and recovery trends using official NVDB (National Road Database) data.

## 🌟 Features

- **🦠 COVID-19 Impact Analysis**: Detailed pandemic effect assessment with recovery tracking
- **🏙️ Regional Traffic Comparison**: Oslo vs Bergen traffic patterns  
- **🛣️ Road Category Analysis**: Highway vs regional road performance
- **📊 Seasonal Patterns**: Monthly and seasonal traffic variations
- **📈 Interactive Visualizations**: Professional charts with traffic-themed styling

## 🚀 Live Demo

[View Live Dashboard on Streamlit Cloud](https://nvdb-traffic-insights.streamlit.app)

## 📊 Dashboard Sections

1. **Main Traffic Trends**: Time series visualization with rolling averages
2. **COVID Impact Metrics**: Before/during/after pandemic analysis  
3. **Regional Performance**: Comparative analysis by region
4. **Road Infrastructure**: Traffic patterns by road category
5. **Seasonal Analysis**: Monthly heatmaps and seasonal patterns

## 🛠️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/Semir-Harun/nvdb-traffic-insights.git
cd nvdb-traffic-insights

# Install dependencies  
pip install -r requirements.txt

# Process raw data (optional - processed data included)
python -m src.analysis.prepare --verbose

# Run dashboard locally
streamlit run src/app/streamlit_app.py
```

## 📁 Project Structure

```
nvdb-traffic-insights/
├── src/
│   ├── app/
│   │   └── streamlit_app.py      # Main Streamlit dashboard
│   ├── analysis/
│   │   └── prepare.py            # Data processing pipeline
│   └── data/
│       └── download.py           # NVDB API data collection
├── data/
│   ├── raw/                      # Raw NVDB traffic data
│   └── processed/                # Analytics-ready datasets
├── tests/
│   └── test_metrics.py           # Unit tests
└── requirements.txt              # Python dependencies
```

## 📈 Key Insights

### 🦠 COVID-19 Impact Findings
- **Immediate Impact**: 25-40% traffic reduction during lockdowns
- **Regional Variation**: Oslo showed faster recovery than Bergen  
- **Road Category Effects**: Highways recovered faster than local roads
- **Recovery Timeline**: Near pre-pandemic levels by late 2021

### 📊 Traffic Pattern Insights
- **Seasonal Trends**: Summer peaks align with tourism patterns
- **Urban vs Rural**: Different recovery trajectories observed
- **Infrastructure Impact**: Road category influences traffic resilience
- **Policy Effectiveness**: Mobility restrictions clearly visible in data

## 🔧 Technical Stack

- **Python 3.11**: Core programming language
- **Streamlit**: Interactive web dashboard framework
- **Plotly**: Advanced data visualizations
- **Pandas**: Data manipulation and analysis
- **NVDB API**: Official Norwegian road database

## 📊 Data Source

**NVDB (National Road Database)**
- Official Norwegian road database
- Automated traffic counting stations  
- Real-time data collection and validation
- Comprehensive coverage of road network

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Related Projects

- [EV Insights Dashboard](https://github.com/Semir-Harun/ev-insights-dashboard)
- [Entur Punctuality Insights](https://github.com/Semir-Harun/entur-punctuality-insights)  
- [Norway Open Data Portfolio](https://github.com/Semir-Harun/norway-open-data-insights)

---

**🚦 NVDB Traffic Insights** - Norwegian road traffic analytics for evidence-based transportation planning