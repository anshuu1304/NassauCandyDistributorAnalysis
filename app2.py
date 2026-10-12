import streamlit as st, pandas as pd, plotly.express as px

st.set_page_config(page_title="Nassau Shipping Analytics", layout="wide", page_icon="🚚")

# Professional Theme: Clean slate background with high-contrast readable metrics
st.markdown("""<style>
.stApp { background-color: #f1f5f9; }
.stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label { color: #1e293b !important; }
section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
section[data-testid="stSidebar"] div[data-testid="stMetric"] { border-left: 6px solid #0ea5e9; }
div[data-testid="stMetric"] { background-color: #ffffff !important; border: 1px solid #cbd5e1; border-left: 6px solid #2563eb; border-radius: 10px; padding: 12px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
div[data-testid="stMetricLabel"] p { color: #64748b !important; font-weight: 600 !important; }
div[data-testid="stMetricValue"] div { color: #0f172a !important; font-weight: 800 !important; }
div[data-testid="stDownloadButton"] button, div[data-testid="stDownloadButton"] button * { background-color: #2563eb !important; color: #ffffff !important; font-weight: 600 !important; border: none !important; }
div[data-testid="stDownloadButton"] button:hover { background-color: #1d4ed8 !important; }

/* Start and End Date Input styling: White text & placeholder */
div[data-testid="stDateInput"] div[data-baseweb="input"],
div[data-testid="stDateInput"] div[data-baseweb="base-input"] {
    background-color: #1e293b !important;
    border-radius: 8px !important;
    border: 1px solid #475569 !important;
}
div[data-testid="stDateInput"] input,
div[data-testid="stDateInput"] div[data-baseweb="input"] *,
div[data-testid="stDateInput"] input[type="text"] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: transparent !important;
}
div[data-testid="stDateInput"] input::placeholder,
div[data-testid="stDateInput"] input::-webkit-input-placeholder,
div[data-testid="stDateInput"] input::-moz-placeholder,
div[data-testid="stDateInput"] input:-ms-input-placeholder {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 0.9 !important;
}
div[data-testid="stDateInput"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}
</style>""", unsafe_allow_html=True)

st.title("🚚 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency")

# Load Data
df = pd.read_csv("data/processed_shipping_data.csv", parse_dates=["Order Date", "Ship Date"])

# Sidebar Filters & Control Panel
st.sidebar.markdown("### 🎛️ Control Panel")
region = st.sidebar.selectbox("Region", ["All"] + sorted(df["Region"].dropna().unique()))
mode = st.sidebar.selectbox("Ship Mode", ["All"] + sorted(df["Ship Mode"].dropna().unique()))
start = st.sidebar.date_input("Start Date", df["Order Date"].min().date())
end = st.sidebar.date_input("End Date", df["Order Date"].max().date())
threshold = st.sidebar.slider("Delay Threshold (days)", 1, 2000, 1274)

# Filter Data
d = df[df["Order Date"].dt.date.between(start, end)].copy()
if region != "All": d = d[d["Region"] == region]
if mode != "All": d = d[d["Ship Mode"] == mode]
d["Delayed"] = d["Lead Time"] > threshold

# Sidebar Live Status Card
st.sidebar.divider()
st.sidebar.metric("Filtered Shipments", f"{len(d):,}", f"{len(d)/len(df)*100:.1f}% active" if len(df) else "0% active")

# Top KPI Metric Cards
a, b, c = st.columns(3)
a.metric("Total Shipments", f"{len(d):,}")
b.metric("Avg Lead Time", f"{d['Lead Time'].mean():.1f} days" if len(d) else "N/A")
c.metric("Delayed Shipments", f"{d['Delayed'].mean():.1%}" if len(d) else "N/A")

# Helper for consistent full-width colorful charts
plot = lambda fig: st.plotly_chart(fig.update_layout(template="plotly_white", margin=dict(l=15, r=15, t=35, b=15)), use_container_width=True)

# Shipping Performance Charts
st.subheader("Shipping Performance")
p1, p2 = st.columns(2)
with p1: plot(px.bar(d.groupby("Ship Mode", as_index=False)["Lead Time"].mean(), x="Ship Mode", y="Lead Time", color="Ship Mode", color_discrete_sequence=px.colors.qualitative.Bold, title="Lead Time by Shipping Mode"))
with p2: plot(px.bar(d.groupby("Region", as_index=False)["Lead Time"].mean(), x="Region", y="Lead Time", color="Region", color_discrete_sequence=px.colors.qualitative.Safe, title="Lead Time by Region"))

p3, p4 = st.columns(2)
with p3: plot(px.histogram(d, x="Lead Time", color_discrete_sequence=["#3b82f6"], title="Lead Time Distribution"))
with p4: plot(px.pie(d, names="Delayed", color="Delayed", color_discrete_map={True: "#ef4444", False: "#10b981"}, hole=0.35, title="Delayed vs On-Time Shipments"))

# Shipment Records Table
st.subheader("Shipment Records")
st.dataframe(d, use_container_width=True)

# Route Analytics (Aggregated once)
route_agg = d.groupby("Route").agg(Shipments=("Order ID", "count"), Avg_Lead_Time=("Lead Time", "mean"), Delay_Rate=("Delayed", "mean")).reset_index()

st.subheader("Route Delay Analysis")
plot(px.bar(route_agg.assign(Delay_Pct=route_agg["Delay_Rate"]*100).nlargest(10, "Delay_Pct"), x="Delay_Pct", y="Route", orientation="h", color="Delay_Pct", color_continuous_scale="Reds", title="Top 10 Routes by Delay %"))

fast, slow = st.columns(2)
with fast: plot(px.bar(route_agg.nsmallest(10, "Avg_Lead_Time"), x="Avg_Lead_Time", y="Route", orientation="h", color="Avg_Lead_Time", color_continuous_scale="Tealgrn", title="Top 10 Fastest Routes"))
with slow: plot(px.bar(route_agg.nlargest(10, "Avg_Lead_Time"), x="Avg_Lead_Time", y="Route", orientation="h", color="Avg_Lead_Time", color_continuous_scale="OrRd", title="Top 10 Slowest Routes"))

st.subheader("Regional Bottlenecks")
plot(px.bar(d.groupby("State/Province", as_index=False)["Lead Time"].mean().nlargest(10, "Lead Time"), x="Lead Time", y="State/Province", orientation="h", color="Lead Time", color_continuous_scale="Burgyl", title="10 Slowest States"))

# Comparison & Summary Tables
st.subheader("Shipping Mode Comparison")
st.dataframe(d.groupby("Ship Mode").agg(Shipments=("Order ID", "count"), Avg_Lead_Time=("Lead Time", "mean"), Delay_Rate=("Delayed", "mean")).round(2), use_container_width=True)

st.subheader("Route KPI Summary")
st.dataframe(route_agg.sort_values("Avg_Lead_Time"), use_container_width=True)

st.caption(f"Showing {len(d):,} of {len(df):,} shipments | Delay threshold: {threshold} days")

# Route Drill-down
st.subheader("Route Drill-down")
if not d.empty:
    route = st.selectbox("Select Route", sorted(d["Route"].dropna().unique()))
    r = d[d["Route"] == route]
    r1, r2, r3 = st.columns(3)
    r1.metric("Shipments", len(r))
    r2.metric("Avg Lead Time", f"{r['Lead Time'].mean():.1f} days")
    r3.metric("Delay Rate", f"{r['Delayed'].mean():.1%}")
    st.dataframe(r, use_container_width=True)
else:
    st.info("No shipment records available for the selected filters. Please adjust the date range or filters to view data.")    

# Factory to Customer Geo Map
st.subheader("Factory-to-Customer Routes")
coords = {"Arizona": (34.3, -111.7), "Georgia": (32.7, -83.4), "Minnesota": (46.3, -94.3), "Tennessee": (35.8, -86.3), "Texas": (31.0, -99.9), "California": (36.8, -119.4), "Florida": (27.8, -81.7), "New York": (42.9, -75.0), "Illinois": (40.0, -89.2), "Ohio": (40.4, -82.8), "Washington": (47.4, -120.7), "Colorado": (39.0, -105.5)}
m = d[d["State/Province"].isin(coords)].drop_duplicates(["Factory", "State/Province"]).copy()
m["Lat"], m["Lon"] = m["State/Province"].map(lambda s: coords[s][0]), m["State/Province"].map(lambda s: coords[s][1])
plot(px.scatter_geo(m, lat="Lat", lon="Lon", color="Factory", hover_name="State/Province", title="Approximate Factory-to-Customer Locations", scope="usa"))

# Download Button
st.download_button("📥 Download Filtered Data", d.to_csv(index=False), "shipping_data.csv", "text/csv")



