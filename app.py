"""
ABC Corp India — Smart Analytics Hub
Data & Analytics Transformation Demo
Author: Candidate Presentation Tool
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ABC Corp – Smart Analytics Hub",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0f1117; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #f97316; margin: 0; }
    .kpi-label { font-size: 0.78rem; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-delta { font-size: 0.75rem; margin-top: 6px; }
    .delta-up   { color: #22c55e; }
    .delta-down { color: #ef4444; }

    /* Section Headers */
    .section-header {
        font-size: 1.3rem; font-weight: 700;
        color: #f1f5f9;
        border-left: 4px solid #f97316;
        padding-left: 12px;
        margin: 28px 0 16px 0;
    }

    /* Insight Box */
    .insight-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #f97316;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .insight-title { color: #f97316; font-weight: 700; font-size: 0.9rem; }
    .insight-text  { color: #cbd5e1; font-size: 0.85rem; margin-top: 4px; }

    /* Alert Badge */
    .alert-critical { background: #450a0a; border-left: 4px solid #ef4444; border-radius: 6px; padding: 10px 14px; margin: 6px 0; color: #fca5a5; }
    .alert-warn     { background: #451a03; border-left: 4px solid #f97316; border-radius: 6px; padding: 10px 14px; margin: 6px 0; color: #fdba74; }
    .alert-ok       { background: #052e16; border-left: 4px solid #22c55e; border-radius: 6px; padding: 10px 14px; margin: 6px 0; color: #86efac; }

    /* Sidebar */
    .css-1d391kg { background-color: #0d1117 !important; }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { background: #1a1f2e; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8; border-radius: 8px; }
    .stTabs [aria-selected="true"] { background: #f97316 !important; color: white !important; }

    /* DataFrames */
    .dataframe { background: #1a1f2e !important; }

    /* Recommendation pill */
    .rec-pill {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #f97316;
        border-radius: 20px;
        padding: 4px 14px;
        color: #f97316;
        font-size: 0.8rem;
        margin: 4px 2px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.ExcelFile("ABC_Corp_India_CarRental_Data.xlsx")
    clicks   = pd.read_excel(xl, "Clickstream",    parse_dates=["Session_Date"])
    social   = pd.read_excel(xl, "Social_Media",   parse_dates=["Post_Date"])
    pos      = pd.read_excel(xl, "POS_Bookings",   parse_dates=["Booking_Date"])
    fleet    = pd.read_excel(xl, "Fleet_Telemetry",parse_dates=["Date"])
    inv      = pd.read_excel(xl, "Inventory",      parse_dates=["As_of_Date"])
    return clicks, social, pos, fleet, inv

clicks, social, pos, fleet, inv = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚗 ABC Corp India")
    st.markdown("**Smart Analytics Hub**")
    st.markdown("---")
    
    page = st.radio("Navigation", [
        "🏠 Executive Dashboard",
        "📊 Customer Journey Analytics",
        "📱 Social Media Intelligence",
        "🗓️ Booking & Revenue Analytics",
        "🛰️ Fleet Telemetry & Health",
        "📦 Inventory Intelligence",
        "🤖 AI Recommendations Engine",
        "📈 Predictive Insights (ML)",
    ])
    
    st.markdown("---")
    st.markdown("**Data Freshness**")
    st.caption(f"Bookings: {pos['Booking_Date'].max().strftime('%b %Y')}")
    st.caption(f"Fleet: {fleet['Date'].max().strftime('%b %Y')}")
    st.caption(f"Records: {len(pos)+len(clicks)+len(fleet)+len(inv):,}")


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────
def kpi(col, value, label, delta=None, delta_good=True):
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_good else "delta-down"
        arrow = "▲" if delta_good else "▼"
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {delta}</div>'
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def insight_box(title, text):
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 {title}</div>
        <div class="insight-text">{text}</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 1 — EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════
if page == "🏠 Executive Dashboard":
    st.markdown("# 🚗 ABC Corp India — Executive Dashboard")
    st.markdown("**Modern Data & Analytics Transformation · Real-time Business Intelligence**")
    st.markdown("---")

    # Top KPIs
    total_rev  = pos["Net_Revenue_INR"].sum()
    avg_rating = pos["Customer_Rating"].mean()
    fleet_util = fleet["Utilization_Pct"].mean()
    conv_rate  = clicks["Converted"].mean() * 100
    maintenance_due = fleet["Maintenance_Due"].eq("Yes").sum()
    idle_vehicles   = inv["Available"].sum()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    kpi(c1, f"₹{total_rev/1e6:.2f}M", "Total Net Revenue")
    kpi(c2, f"{avg_rating:.2f} ★", "Avg Customer Rating", "vs 4.0 target", True)
    kpi(c3, f"{fleet_util:.1f}%", "Fleet Utilization", "+2.3% MoM", True)
    kpi(c4, f"{conv_rate:.1f}%", "Booking Conversion", "-1.2% MoM", False)
    kpi(c5, f"{maintenance_due}", "Vehicles Due Maintenance", "Action needed", False)
    kpi(c6, f"{idle_vehicles}", "Available Vehicles Now", "Across all cities", True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue by City + Channel
    col1, col2 = st.columns(2)
    with col1:
        section("Revenue by City")
        city_rev = pos.groupby("City")["Net_Revenue_INR"].sum().sort_values(ascending=True)
        fig = px.bar(city_rev, orientation="h", color=city_rev.values,
                     color_continuous_scale=["#1e293b","#f97316"],
                     labels={"value":"Net Revenue (₹)","index":"City"})
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Revenue by Booking Channel")
        ch_rev = pos.groupby("Channel")["Net_Revenue_INR"].sum()
        fig = px.pie(values=ch_rev.values, names=ch_rev.index,
                     color_discrete_sequence=["#f97316","#fb923c","#fed7aa","#1e293b","#475569"])
        fig.update_layout(bg(), height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Revenue trend
    section("Monthly Revenue Trend")
    pos["Month"] = pos["Booking_Date"].dt.to_period("M").astype(str)
    monthly = pos.groupby("Month")["Net_Revenue_INR"].sum().reset_index()
    fig = px.line(monthly, x="Month", y="Net_Revenue_INR", markers=True,
                  color_discrete_sequence=["#f97316"])
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_layout(bg(), height=280)
    st.plotly_chart(fig, use_container_width=True)

    # Business Insights
    section("Automated Business Alerts")
    col1, col2, col3 = st.columns(3)
    with col1:
        top_city = pos.groupby("City")["Net_Revenue_INR"].sum().idxmax()
        st.markdown(f'<div class="alert-ok">✅ <b>Top Revenue City:</b> {top_city} — consider fleet expansion here</div>', unsafe_allow_html=True)
        low_conv_city = clicks.groupby("City")["Converted"].mean().idxmin()
        st.markdown(f'<div class="alert-warn">⚠️ <b>Lowest Conversion:</b> {low_conv_city} — UX/pricing review needed</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="alert-critical">🔴 <b>{maintenance_due} vehicles</b> overdue for maintenance — schedule immediately</div>', unsafe_allow_html=True)
        cancel_rate = (pos["Status"]=="Cancelled").mean()*100
        st.markdown(f'<div class="alert-warn">⚠️ <b>Cancellation Rate:</b> {cancel_rate:.1f}% — investigate root causes</div>', unsafe_allow_html=True)
    with col3:
        top_ch = pos.groupby("Channel")["Net_Revenue_INR"].sum().idxmax()
        st.markdown(f'<div class="alert-ok">✅ <b>Best Channel:</b> {top_ch} — prioritize for marketing budget</div>', unsafe_allow_html=True)
        low_fuel = (fleet["Fuel_Level_Pct"] < 20).sum()
        st.markdown(f'<div class="alert-warn">⚠️ <b>{low_fuel} vehicles</b> below 20% fuel — dispatch refueling team</div>', unsafe_allow_html=True)


def bg():
    return dict(plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
                font_color="#cbd5e1", margin=dict(l=10,r=10,t=30,b=10))


# ═══════════════════════════════════════════════
# PAGE 2 — CUSTOMER JOURNEY
# ═══════════════════════════════════════════════
elif page == "📊 Customer Journey Analytics":
    st.markdown("# 📊 Customer Journey Analytics")
    st.markdown("Clickstream funnel analysis · Abandoned booking recovery · UX optimization")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"{clicks['Session_Duration_Sec'].mean()/60:.1f} min", "Avg Session Duration")
    kpi(c2, f"{clicks['Converted'].mean()*100:.1f}%", "Overall Conversion Rate")
    kpi(c3, f"{clicks['Bounce'].mean()*100:.1f}%", "Bounce Rate", "High = UX issue", False)
    kpi(c4, f"{clicks['Repeat_Visitor'].mean()*100:.1f}%", "Repeat Visitors")

    col1, col2 = st.columns(2)
    with col1:
        section("Conversion by Device Type")
        dev = clicks.groupby("Device")["Converted"].mean().reset_index()
        dev["Conversion %"] = dev["Converted"] * 100
        fig = px.bar(dev, x="Device", y="Conversion %", color="Conversion %",
                     color_continuous_scale=["#1e293b","#f97316"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Conversion by Campaign Source")
        camp = clicks.groupby("Campaign_Source")["Converted"].mean().dropna().sort_values(ascending=False).reset_index()
        camp["Conversion %"] = camp["Converted"] * 100
        fig = px.bar(camp, x="Campaign_Source", y="Conversion %", color="Conversion %",
                     color_continuous_scale=["#1e293b","#f97316"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    section("Session Duration Distribution — Converted vs Not Converted")
    conv_y = clicks[clicks["Converted"]==1]["Session_Duration_Sec"]/60
    not_y  = clicks[clicks["Converted"]==0]["Session_Duration_Sec"]/60
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=conv_y, name="Converted", marker_color="#f97316", opacity=0.7, nbinsx=30))
    fig.add_trace(go.Histogram(x=not_y, name="Not Converted", marker_color="#3b82f6", opacity=0.7, nbinsx=30))
    fig.update_layout(bg(), barmode="overlay", xaxis_title="Session Duration (min)", height=280)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section("Booking Funnel")
        stages = ["Homepage Visit","Search","View Details","Add to Cart","Payment","Confirmed"]
        vals   = [300, 240, 180, 120, 80, int(clicks["Converted"].sum())]
        fig = go.Figure(go.Funnel(y=stages, x=vals,
            marker_color=["#f97316","#fb923c","#fed7aa","#fde68a","#a3e635","#22c55e"]))
        fig.update_layout(bg(), height=320)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Payment Drop-off", f"{100*(vals[3]-vals[4])/vals[3]:.0f}% users abandon at payment step — trigger real-time discount notification to recover bookings")

    with col2:
        section("Top Exit Pages")
        exit_pg = clicks["Exit_Page"].value_counts().head(8).reset_index()
        exit_pg.columns = ["Exit Page","Count"]
        fig = px.bar(exit_pg, y="Exit Page", x="Count", orientation="h",
                     color="Count", color_continuous_scale=["#1e293b","#ef4444"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=320)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("High /home Exit Rate", "Users exiting on /home indicate weak landing page — A/B test hero section with location search upfront")


# ═══════════════════════════════════════════════
# PAGE 3 — SOCIAL MEDIA
# ═══════════════════════════════════════════════
elif page == "📱 Social Media Intelligence":
    st.markdown("# 📱 Social Media Intelligence")
    st.markdown("Platform performance · Campaign ROI · Engagement insights")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"{social['Impressions'].sum()/1e6:.1f}M", "Total Impressions")
    kpi(c2, f"{social['Conversions'].sum():,}", "Total Conversions")
    kpi(c3, f"₹{social['Ad_Spend_INR'].sum()/1e6:.2f}M", "Total Ad Spend")
    kpi(c4, f"₹{(social['Ad_Spend_INR'].sum()/social['Conversions'].sum()):.0f}", "Cost per Conversion")

    col1, col2 = st.columns(2)
    with col1:
        section("Conversions by Platform")
        plat = social.groupby("Platform")["Conversions"].sum().reset_index()
        fig = px.pie(plat, values="Conversions", names="Platform",
                     color_discrete_sequence=["#f97316","#3b82f6","#a855f7","#22c55e"])
        fig.update_layout(bg(), height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Engagement Rate by Platform")
        eng = social.groupby("Platform")["Engagement_Rate_Pct"].mean().reset_index()
        fig = px.bar(eng, x="Platform", y="Engagement_Rate_Pct", color="Engagement_Rate_Pct",
                     color_continuous_scale=["#1e293b","#f97316"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300, yaxis_title="Engagement Rate %")
        st.plotly_chart(fig, use_container_width=True)

    section("Campaign ROI Analysis — Spend vs Conversions")
    camp = social.groupby("Campaign_Name").agg({"Ad_Spend_INR":"sum","Conversions":"sum","Impressions":"sum"}).reset_index()
    camp["CPConv"] = camp["Ad_Spend_INR"] / camp["Conversions"]
    fig = px.scatter(camp, x="Ad_Spend_INR", y="Conversions", size="Impressions",
                     color="Campaign_Name", text="Campaign_Name",
                     color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_traces(textposition="top center", textfont_size=10)
    fig.update_layout(bg(), height=350)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section("Post Type Performance")
        pt = social.groupby("Post_Type")[["Likes","Shares","Conversions"]].mean().reset_index()
        fig = px.bar(pt, x="Post_Type", y=["Likes","Shares","Conversions"], barmode="group",
                     color_discrete_sequence=["#f97316","#3b82f6","#22c55e"])
        fig.update_layout(bg(), height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Top Cities by Social Conversions")
        city_conv = social.groupby("City_Targeted")["Conversions"].sum().sort_values(ascending=False).head(8)
        fig = px.bar(city_conv, color=city_conv.values, color_continuous_scale=["#1e293b","#f97316"],
                     labels={"value":"Conversions","index":"City"})
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    insight_box("Facebook Dominates Conversions", "Reallocate 15% of LinkedIn budget to Facebook/Instagram for higher ROI — Facebook shows 2x conversion efficiency")
    insight_box("Diwali Campaign Best ROI", "Seasonal campaigns outperform always-on by 3x — plan dedicated campaign calendar for Holi, Summer, Diwali, New Year")


# ═══════════════════════════════════════════════
# PAGE 4 — BOOKING & REVENUE
# ═══════════════════════════════════════════════
elif page == "🗓️ Booking & Revenue Analytics":
    st.markdown("# 🗓️ Booking & Revenue Analytics")
    st.markdown("POS data across channels, cities, car types & location types")
    st.markdown("---")

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    sel_city = col_f1.multiselect("City", pos["City"].unique(), default=list(pos["City"].unique()))
    sel_ch   = col_f2.multiselect("Channel", pos["Channel"].unique(), default=list(pos["Channel"].unique()))
    sel_ct   = col_f3.multiselect("Car Type", pos["Car_Type"].unique(), default=list(pos["Car_Type"].unique()))

    filt = pos[pos["City"].isin(sel_city) & pos["Channel"].isin(sel_ch) & pos["Car_Type"].isin(sel_ct)]

    c1,c2,c3,c4,c5 = st.columns(5)
    kpi(c1, f"{len(filt):,}", "Total Bookings")
    kpi(c2, f"₹{filt['Net_Revenue_INR'].sum()/1e6:.2f}M", "Net Revenue")
    kpi(c3, f"₹{filt['Net_Revenue_INR'].mean():,.0f}", "Avg Booking Value")
    kpi(c4, f"{filt['Customer_Rating'].mean():.2f} ★", "Avg Rating")
    kpi(c5, f"{(filt['Status']=='Cancelled').mean()*100:.1f}%", "Cancellation Rate", "Target <10%", False)

    col1, col2 = st.columns(2)
    with col1:
        section("Revenue by Location Type")
        loc = filt.groupby("Location_Type")["Net_Revenue_INR"].sum().sort_values(ascending=True)
        fig = px.bar(loc, orientation="h", color=loc.values, color_continuous_scale=["#1e293b","#f97316"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Revenue by Car Type")
        ct = filt.groupby("Car_Type")["Net_Revenue_INR"].sum().sort_values(ascending=False)
        fig = px.bar(ct, color=ct.values, color_continuous_scale=["#1e293b","#f97316"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    section("Revenue Heatmap — City × Channel")
    pivot = filt.pivot_table(values="Net_Revenue_INR", index="City", columns="Channel", aggfunc="sum", fill_value=0)
    fig = px.imshow(pivot, color_continuous_scale=["#0f1117","#f97316"], aspect="auto",
                    labels=dict(color="Revenue ₹"))
    fig.update_layout(bg(), height=350)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section("Booking Status Breakdown")
        status = filt["Status"].value_counts()
        fig = px.pie(values=status.values, names=status.index,
                     color_discrete_sequence=["#22c55e","#f97316","#ef4444","#a855f7"])
        fig.update_layout(bg(), height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Rating Distribution by Car Type")
        fig = px.box(filt, x="Car_Type", y="Customer_Rating", color="Car_Type",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(bg(), showlegend=False, height=280)
        st.plotly_chart(fig, use_container_width=True)

    insight_box("Airport + Corporate = Highest Revenue", "Airport & Convention Centre locations + Corporate Partner channel yield 40% higher revenue per booking — prioritize fleet allocation here")
    insight_box("SUV Most Popular", "SUVs lead in revenue per booking — ensure 30%+ SUV stock at high-demand locations")


# ═══════════════════════════════════════════════
# PAGE 5 — FLEET TELEMETRY
# ═══════════════════════════════════════════════
elif page == "🛰️ Fleet Telemetry & Health":
    st.markdown("# 🛰️ Fleet Telemetry & Real-Time Vehicle Intelligence")
    st.markdown("GPS tracking · Predictive maintenance · Driver behaviour · Fleet health scoring")
    st.markdown("---")

    c1,c2,c3,c4,c5 = st.columns(5)
    kpi(c1, f"{fleet['Utilization_Pct'].mean():.1f}%", "Avg Fleet Utilization")
    kpi(c2, f"{fleet['Maintenance_Due'].eq('Yes').sum()}", "Maintenance Due", "Immediate action", False)
    kpi(c3, f"{fleet['Engine_Health_Score'].mean():.0f}/100", "Avg Engine Health")
    kpi(c4, f"{fleet['Harsh_Braking_Events'].sum()}", "Harsh Braking Events", "Driver training needed", False)
    kpi(c5, f"{fleet['Overspeeding_Events'].sum()}", "Overspeeding Events", "Safety alert", False)

    col1, col2 = st.columns(2)
    with col1:
        section("Vehicle Health Scores by Car Type")
        health = fleet.groupby("Car_Type")[["Engine_Health_Score","Brake_Health_Score","Tyre_Health_Score"]].mean()
        fig = px.bar(health, barmode="group", color_discrete_sequence=["#f97316","#3b82f6","#22c55e"])
        fig.update_layout(bg(), height=320, xaxis_title="Car Type", yaxis_title="Score /100")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Fleet Status Distribution")
        status_dist = fleet["Status"].value_counts()
        fig = px.pie(values=status_dist.values, names=status_dist.index,
                     color_discrete_sequence=["#22c55e","#f97316","#ef4444","#3b82f6"])
        fig.update_layout(bg(), height=320)
        st.plotly_chart(fig, use_container_width=True)

    section("Vehicle Maintenance Risk Map — Engine Health vs Last Service Days")
    fig = px.scatter(fleet, x="Last_Service_Days_Ago", y="Engine_Health_Score",
                     color="Maintenance_Due", size="Odometer_km",
                     hover_data=["Vehicle_ID","Car_Model","City","Status"],
                     color_discrete_map={"Yes":"#ef4444","No":"#22c55e"},
                     labels={"Last_Service_Days_Ago":"Days Since Last Service",
                             "Engine_Health_Score":"Engine Health Score"})
    fig.add_vline(x=60, line_dash="dash", line_color="#f97316", annotation_text="Service Threshold")
    fig.add_hline(y=60, line_dash="dash", line_color="#ef4444", annotation_text="Critical Health")
    fig.update_layout(bg(), height=380)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section("Fleet Utilization by City")
        util = fleet.groupby("City")["Utilization_Pct"].mean().sort_values(ascending=True)
        fig = px.bar(util, orientation="h", color=util.values,
                     color_continuous_scale=["#ef4444","#f97316","#22c55e"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Driver Behaviour — Harsh Events by City")
        drive = fleet.groupby("City")[["Harsh_Braking_Events","Overspeeding_Events"]].sum().reset_index()
        fig = px.bar(drive, x="City", y=["Harsh_Braking_Events","Overspeeding_Events"], barmode="stack",
                     color_discrete_sequence=["#f97316","#ef4444"])
        fig.update_layout(bg(), height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Critical vehicles table
    section("🔴 Vehicles Requiring Immediate Attention")
    critical = fleet[(fleet["Maintenance_Due"]=="Yes") & (fleet["Engine_Health_Score"] < 65)][
        ["Vehicle_ID","Car_Type","Car_Model","City","Status","Engine_Health_Score","Last_Service_Days_Ago","Fuel_Level_Pct"]
    ].sort_values("Engine_Health_Score").head(10)
    st.dataframe(critical.style.background_gradient(subset=["Engine_Health_Score"], cmap="RdYlGn"), use_container_width=True)

    insight_box("Predictive Maintenance Saves ₹2.1L/month", "Every avoided breakdown saves avg. ₹21,000 in repair + ₹8,000 in lost rental revenue. Scheduling maintenance for the 10 critical vehicles above saves an estimated ₹2.9L")


# ═══════════════════════════════════════════════
# PAGE 6 — INVENTORY
# ═══════════════════════════════════════════════
elif page == "📦 Inventory Intelligence":
    st.markdown("# 📦 Inventory Intelligence")
    st.markdown("Fleet allocation · Location gaps · Rebalancing recommendations")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"{inv['Total_Fleet'].sum():,}", "Total Fleet Size")
    kpi(c2, f"{inv['Available'].sum():,}", "Currently Available")
    kpi(c3, f"{inv['In_Repair'].sum():,}", "In Repair")
    kpi(c4, f"{inv['Utilization_Rate_Pct'].mean():.1f}%", "Avg Utilization Rate")

    col1, col2 = st.columns(2)
    with col1:
        section("Fleet Availability by City")
        city_inv = inv.groupby("City")[["Available","In_Repair","In_Transit","Booked"]].sum()
        fig = px.bar(city_inv, barmode="stack",
                     color_discrete_sequence=["#22c55e","#ef4444","#f97316","#3b82f6"])
        fig.update_layout(bg(), height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Fleet Distribution by Car Type")
        ct_inv = inv.groupby("Car_Type")["Total_Fleet"].sum().sort_values(ascending=False)
        fig = px.bar(ct_inv, color=ct_inv.values, color_continuous_scale=["#1e293b","#f97316"])
        fig.update_layout(bg(), showlegend=False, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    section("Utilization Heatmap — City × Location Type")
    pivot_inv = inv.pivot_table(values="Utilization_Rate_Pct", index="City",
                                columns="Location_Type", aggfunc="mean", fill_value=0)
    fig = px.imshow(pivot_inv, color_continuous_scale=["#0f1117","#22c55e"],
                    labels=dict(color="Utilization %"), aspect="auto")
    fig.update_layout(bg(), height=380)
    st.plotly_chart(fig, use_container_width=True)

    section("⚠️ Fleet Rebalancing Recommendations")
    # Cities with high available but low utilization → surplus
    city_util = inv.groupby("City").agg({"Available":"sum","Utilization_Rate_Pct":"mean","Total_Fleet":"sum"}).reset_index()
    surplus  = city_util[city_util["Utilization_Rate_Pct"] < 20].sort_values("Available", ascending=False)
    shortage = city_util[city_util["Utilization_Rate_Pct"] > 60].sort_values("Utilization_Rate_Pct", ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🟢 Surplus Cities (Move vehicles OUT)**")
        if len(surplus):
            st.dataframe(surplus[["City","Available","Utilization_Rate_Pct"]].rename(columns={"Utilization_Rate_Pct":"Util%"}), use_container_width=True)
        else:
            st.info("No surplus cities currently")

    with col2:
        st.markdown("**🔴 Demand Cities (Move vehicles IN)**")
        if len(shortage):
            st.dataframe(shortage[["City","Available","Utilization_Rate_Pct"]].rename(columns={"Utilization_Rate_Pct":"Util%"}), use_container_width=True)
        else:
            st.info("No shortage cities currently")


# ═══════════════════════════════════════════════
# PAGE 7 — AI RECOMMENDATIONS ENGINE
# ═══════════════════════════════════════════════
elif page == "🤖 AI Recommendations Engine":
    st.markdown("# 🤖 AI-Powered Recommendations Engine")
    st.markdown("Smart Hub Platform — Natural language insights, automated recommendations & GenAI integration")
    st.markdown("---")

    st.info("🔮 This page demonstrates ABC Corp's proposed GenAI Smart Hub — combining rule-based analytics with AI-generated recommendations in production, this would use Claude/GPT APIs for natural language query and automated reporting.")

    # Natural language query simulation
    section("💬 Natural Language Query Engine (Demo)")
    query = st.selectbox("Ask a business question:", [
        "Why did bookings drop last month?",
        "Which city has the most idle fleet?",
        "What is my best performing channel?",
        "Which vehicles need immediate maintenance?",
        "How can I improve my conversion rate?",
        "Which campaign has the best ROI?",
        "What is the revenue impact of fleet downtime?",
    ])

    nl_responses = {
        "Why did bookings drop last month?": {
            "answer": "Bookings declined by approximately 12% last month. Root causes identified: (1) Cancellation rate spiked to 18% in Chennai due to local event conflicts; (2) Online channel conversion dropped 2.3% — likely due to payment gateway friction detected in clickstream data; (3) 7 vehicles in Mumbai were in repair simultaneously, reducing availability during a peak weekend.",
            "action": "Immediate actions: Resolve payment gateway issues (Est. impact +8% conversion), reassign 3 surplus vehicles from Jaipur to Mumbai, investigate Chennai cancellation root cause.",
            "pills": ["Fix Payment UX","Rebalance Fleet","Investigate Chennai"]
        },
        "Which city has the most idle fleet?": {
            "answer": "Jaipur has the highest proportion of available (idle) vehicles at 78% availability rate with only 22% utilization — significantly below the 57% company average. This represents approximately ₹4.2L in potential lost monthly revenue.",
            "action": "Recommended: Transfer 8 SUVs and 4 Sedans from Jaipur to Mumbai (Airport) and Bengaluru (Corporate Hub) where demand is highest. Expected impact: +₹3.1L monthly revenue.",
            "pills": ["Transfer SUVs to Mumbai","Activate Jaipur Marketing","Dynamic Pricing Alert"]
        },
        "What is my best performing channel?": {
            "answer": "Corporate Partner channel delivers the highest revenue per booking (avg ₹18,200 vs overall avg ₹13,400), with a 91% completion rate and 4.7★ average rating. Online channel has the highest volume but lowest per-booking value.",
            "action": "Expand Corporate Partner agreements — target 5 new enterprise clients in Bengaluru and Hyderabad tech corridors. Each new corporate account estimated ₹8L annual revenue.",
            "pills": ["Expand Corporate Ties","Improve Online UX","Launch Corporate Loyalty"]
        },
        "Which vehicles need immediate maintenance?": {
            "answer": f"There are {fleet['Maintenance_Due'].eq('Yes').sum()} vehicles with maintenance due. Critical priority: 10 vehicles have engine health score below 65 AND are overdue by 60+ days. These vehicles have 3x higher breakdown risk.",
            "action": "Schedule maintenance for critical 10 vehicles immediately. Estimated cost: ₹2.1L. Expected savings from prevented breakdowns: ₹4.8L. ROI: 2.3x.",
            "pills": ["Schedule Maintenance","Alert Service Team","Update Vehicle SLA"]
        },
        "How can I improve my conversion rate?": {
            "answer": f"Current conversion rate is {clicks['Converted'].mean()*100:.1f}%. Key friction points: (1) 47% of users drop off at payment step; (2) Mobile users convert 8% less than desktop; (3) Users from 'None' campaign source convert at 31% — showing organic intent is high.",
            "action": "Quick wins: (1) Add saved payment method feature — est. +4% conversion; (2) Mobile UX audit — est. +3%; (3) Retargeting campaign for payment abandoners — est. +2%. Combined est. impact: +₹12L revenue/quarter.",
            "pills": ["Mobile UX Audit","Payment Optimization","Retargeting Campaign"]
        },
        "Which campaign has the best ROI?": {
            "answer": "Diwali Offer campaign has the best ROI with lowest Cost-per-Conversion. Summer Sale drives highest volume. Corporate Drive has highest quality conversions (repeat customers). New Year Offer underperforms significantly vs spend.",
            "action": "Increase Diwali/festive campaign budget by 40%. Reduce New Year budget by 50%, redirect to Holi campaign. Clone Diwali creative strategy for upcoming Eid and Independence Day.",
            "pills": ["Boost Diwali Budget","Cut New Year Spend","Clone Diwali Strategy"]
        },
        "What is the revenue impact of fleet downtime?": {
            "answer": f"Currently {inv['In_Repair'].sum()} vehicles are in repair. Average daily rate ₹1,850. Estimated daily revenue loss: ₹{inv['In_Repair'].sum()*1850:,}. Monthly impact: ₹{inv['In_Repair'].sum()*1850*30/1e5:.1f}L. Average repair duration is 4.2 days per vehicle.",
            "action": "Implement vendor SLA enforcement: Target <3 days repair turnaround (vs current 4.2 days). Negotiate priority service contracts with top 3 garages. Expected savings: ₹1.8L/month.",
            "pills": ["Enforce Vendor SLA","Add Spare Parts Buffer","Monitor Repair TAT"]
        }
    }

    resp = nl_responses[query]
    st.markdown(f"""
    <div class="insight-box" style="margin-top:16px;">
        <div class="insight-title">🤖 AI Analysis</div>
        <div class="insight-text" style="font-size:0.95rem; line-height:1.6;">{resp['answer']}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box" style="border-color:#22c55e;">
        <div class="insight-title" style="color:#22c55e;">✅ Recommended Actions</div>
        <div class="insight-text">{resp['action']}</div>
        <div style="margin-top:10px;">{"".join([f'<span class="rec-pill">{p}</span>' for p in resp["pills"]])}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section("🔄 Automated Daily Business Digest (GenAI Output Sample)")
    
    total_rev  = pos["Net_Revenue_INR"].sum()
    top_city   = pos.groupby("City")["Net_Revenue_INR"].sum().idxmax()
    maint_cnt  = fleet["Maintenance_Due"].eq("Yes").sum()
    conv_pct   = clicks["Converted"].mean()*100

    st.markdown(f"""
    <div style="background:#1a1f2e; border:1px solid #2d3748; border-radius:12px; padding:24px; font-family: 'Inter', monospace; line-height:1.9;">
        <div style="color:#f97316; font-weight:700; font-size:1.1rem; margin-bottom:12px;">📋 ABC Corp Daily Business Intelligence Report — Auto-Generated</div>
        <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:16px;">Generated: {pd.Timestamp.now().strftime('%B %d, %Y at %H:%M IST')} · Powered by GenAI Smart Hub</div>
        
        <div style="color:#e2e8f0; font-size:0.92rem;">
        <b style="color:#f97316;">REVENUE SUMMARY:</b> Portfolio net revenue stands at ₹{total_rev/1e6:.2f}M. 
        {top_city} continues to lead city-wise performance. Corporate Partner channel outperforms all others at ₹18,200 avg. booking value.<br><br>
        
        <b style="color:#ef4444;">ALERTS — ACTION REQUIRED:</b> {maint_cnt} vehicles have overdue maintenance, 
        with 10 in critical condition (Engine Health &lt;65). Fleet rebalancing opportunity identified: 
        Jaipur has surplus vehicles while Mumbai Airport shows demand pressure.<br><br>
        
        <b style="color:#22c55e;">OPPORTUNITIES:</b> Booking conversion at {conv_pct:.1f}% — 
        payment step drop-off represents ₹8L+ monthly revenue recovery opportunity. 
        Diwali campaign ROI outperforms all others — recommend budget increase.<br><br>
        
        <b style="color:#a855f7;">PREDICTED TODAY:</b> Weekend demand expected to peak at Airport locations. 
        Pre-position 12+ SUVs at Mumbai, Bengaluru, and Delhi airports by Friday 18:00.
        </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 8 — PREDICTIVE INSIGHTS
# ═══════════════════════════════════════════════
elif page == "📈 Predictive Insights (ML)":
    st.markdown("# 📈 Predictive Insights — Machine Learning Models")
    st.markdown("Demand forecasting · Churn prediction · Maintenance alerts · Dynamic pricing signals")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Demand Forecasting","⚠️ Maintenance Risk Score","💰 Dynamic Pricing Signal"])

    with tab1:
        section("Booking Volume Forecast — Next 30 Days")
        # Simple trend-based forecast
        pos["Month"] = pos["Booking_Date"].dt.to_period("M").astype(str)
        hist = pos.groupby("Month").size().reset_index(name="Bookings")
        hist["Period"] = range(len(hist))
        
        x = hist["Period"].values
        y = hist["Bookings"].values
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        
        future_x  = np.arange(len(hist), len(hist)+3)
        future_y  = p(future_x).astype(int)
        future_lb = (future_y * 0.85).astype(int)
        future_ub = (future_y * 1.15).astype(int)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist["Month"], y=hist["Bookings"], name="Historical", line_color="#3b82f6", line_width=2, mode="lines+markers"))
        future_months = ["Mar 2025","Apr 2025","May 2025"]
        fig.add_trace(go.Scatter(x=future_months, y=future_y, name="Forecast", line_color="#f97316", line_dash="dash", line_width=2, mode="lines+markers"))
        fig.add_trace(go.Scatter(x=future_months+future_months[::-1],
            y=list(future_ub)+list(future_lb[::-1]),
            fill="toself", fillcolor="rgba(249,115,22,0.15)", line_color="rgba(0,0,0,0)", name="Confidence Band"))
        fig.update_layout(bg(), height=380)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        for i, (m, v, lb, ub) in enumerate(zip(future_months, future_y, future_lb, future_ub)):
            [col1,col2,col3][i].markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{v}</div>
                <div class="kpi-label">{m} Forecast</div>
                <div class="kpi-delta" style="color:#94a3b8;">Range: {lb}–{ub}</div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        section("Predictive Maintenance Risk Scores")
        # Composite risk score
        fleet_risk = fleet.copy()
        fleet_risk["Risk_Score"] = (
            (100 - fleet_risk["Engine_Health_Score"]) * 0.35 +
            (100 - fleet_risk["Brake_Health_Score"])  * 0.25 +
            (fleet_risk["Last_Service_Days_Ago"] / 90 * 100).clip(0,100) * 0.25 +
            (100 - fleet_risk["Tyre_Health_Score"]) * 0.15
        ).round(1)
        fleet_risk["Risk_Level"] = pd.cut(fleet_risk["Risk_Score"],
            bins=[0,30,55,75,100], labels=["Low","Medium","High","Critical"])
        
        risk_dist = fleet_risk["Risk_Level"].value_counts()
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(values=risk_dist.values, names=risk_dist.index,
                         color_discrete_map={"Low":"#22c55e","Medium":"#f97316","High":"#ef4444","Critical":"#7f1d1d"},
                         title="Fleet Risk Distribution")
            fig.update_layout(bg(), height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            section("Top 10 High-Risk Vehicles")
            top_risk = fleet_risk.nlargest(10,"Risk_Score")[["Vehicle_ID","Car_Model","City","Risk_Score","Risk_Level","Maintenance_Due"]]
            st.dataframe(top_risk.style.background_gradient(subset=["Risk_Score"], cmap="RdYlGn_r"), use_container_width=True)

    with tab3:
        section("Dynamic Pricing Signal by Day of Week & City")
        pos["DayOfWeek"] = pos["Booking_Date"].dt.day_name()
        day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow_city = pos.groupby(["DayOfWeek","City"])["Net_Revenue_INR"].sum().reset_index()
        pivot_dow = dow_city.pivot(index="City", columns="DayOfWeek", values="Net_Revenue_INR").reindex(columns=day_order, fill_value=0)
        
        fig = px.imshow(pivot_dow, color_continuous_scale=["#0f1117","#f97316"],
                        labels=dict(color="Revenue ₹"), title="Revenue Intensity (Darker Orange = Higher Demand = Higher Price Signal)")
        fig.update_layout(bg(), height=380)
        st.plotly_chart(fig, use_container_width=True)

        insight_box("Dynamic Pricing Opportunity", "Weekends show 40-60% higher demand in Mumbai & Bengaluru. Applying +15% surge pricing on Fri-Sun at Airport locations estimated to generate +₹6.2L/quarter with minimal booking impact")
        insight_box("Off-Peak Discount Strategy", "Tuesday-Wednesday show lowest demand. Flash discount of 10% on these days can increase utilization by 8-12% with net positive revenue impact")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#475569; font-size:0.8rem; padding:12px 0;">
        ABC Corp India — Smart Analytics Hub · Modern Data & Analytics Transformation Proposal<br>
        Built with Python · Streamlit · Plotly · Pandas | Data: ABC Corp India Dummy Dataset
    </div>""", unsafe_allow_html=True)
