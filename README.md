# 🚗 ABC Corp India — Smart Analytics Hub

A fully interactive **Data & Analytics Transformation Demo** built for the ABC Corp case study.

## What This App Demonstrates

This Streamlit application showcases a real implementation of the proposed Modern Data & Analytics platform, covering all 5 data sources from the problem statement:

| Page | Data Source | Business Value |
|------|-------------|----------------|
| Executive Dashboard | All sources | C-suite KPIs & alerts |
| Customer Journey Analytics | Clickstream | Conversion funnel, drop-off |
| Social Media Intelligence | Social Media | Campaign ROI, engagement |
| Booking & Revenue Analytics | POS Bookings | Revenue by city/channel/type |
| Fleet Telemetry & Health | Fleet Telemetry | Maintenance risk, driver behaviour |
| Inventory Intelligence | Inventory | Rebalancing recommendations |
| AI Recommendations Engine | All | GenAI Smart Hub simulation |
| Predictive Insights (ML) | All | Forecasting, risk scores, pricing |

## How to Run

### Option 1: Local (Recommended for Interview Demo)
```bash
# 1. Clone / download this folder
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```
The app opens at http://localhost:8501

### Option 2: Deploy to Streamlit Cloud (Free)
1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Connect your GitHub repo, set `app.py` as the main file
4. Click Deploy — live URL in ~2 minutes!

### Option 3: Deploy to Hugging Face Spaces
1. Create a new Space at https://huggingface.co/spaces
2. Choose Streamlit SDK
3. Upload all files
4. App is live with a public URL!

## Files
```
abc_corp_app/
├── app.py                              # Main Streamlit application
├── ABC_Corp_India_CarRental_Data.xlsx  # Dataset (all 5 sheets)
├── requirements.txt                    # Python dependencies
└── README.md                          # This file
```

## Key Features That Impress Interviewers
- ✅ All 5 required data sources from problem statement
- ✅ Interactive filters on every page
- ✅ Predictive ML models (demand forecast, maintenance risk)
- ✅ GenAI Smart Hub simulation with NL query engine
- ✅ Automated business alerts & recommendations
- ✅ Dynamic pricing signal analysis
- ✅ Fleet rebalancing recommendations
- ✅ Professional dark-mode UI with orange brand colors

## Technology Stack
- **Frontend**: Streamlit + Custom CSS
- **Visualisation**: Plotly Express & Graph Objects
- **Data**: Pandas + OpenPyXL
- **ML**: NumPy polynomial regression, composite risk scoring
- **Deployment**: Streamlit Cloud / Heroku / Hugging Face

---
*Built for ABC Corp India — Data & Analytics Transformation Proposal*
