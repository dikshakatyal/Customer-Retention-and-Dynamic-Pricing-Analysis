import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

# =========================
# PAGE CONFIG (BI STYLE)
# =========================
st.set_page_config(
    
    page_icon="📊",
    page_title= "Hotel Booking Analytics Dashboard",
    layout="wide"
)
# =========================
# CUSTOM STYLING
# =========================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #161A23;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD TITLE
# =========================
st.title("🏨 Hotel Booking Analytics & Revenue Intelligence Dashboard")
st.markdown("### Business Intelligence | Cancellation Insights | Revenue Optimization | ML Analytics")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("cleaned_hotel_booking.csv")


# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filters")

if "room_type" in df.columns:
    room_filter = st.sidebar.multiselect(
        "Room Type",
        df["room_type"].unique(),
        default=df["room_type"].unique()
    )
    df = df[df["room_type"].isin(room_filter)]

if "booking_channel" in df.columns:
    channel_filter = st.sidebar.multiselect(
        "Booking Channel",
        df["booking_channel"].unique(),
        default=df["booking_channel"].unique()
    )
    df = df[df["booking_channel"].isin(channel_filter)]

   

# Country Filter
if "country" in df.columns:
    country_filter = st.sidebar.multiselect(
        "🌍 Country",
        df["country"].unique(),
        default=df["country"].unique()
    )
    df = df[df["country"].isin(country_filter)]

# Booking Month Filter
if "booking_month" in df.columns:
    month_filter = st.sidebar.multiselect(
        "📅 Booking Month",
        df["booking_month"].unique(),
        default=df["booking_month"].unique()
    )
    df = df[df["booking_month"].isin(month_filter)]

# Customer Risk Category Filter
if "customer_risk_category" in df.columns:
    risk_filter = st.sidebar.multiselect(
        "⚠ Customer Risk Category",
        df["customer_risk_category"].unique(),
        default=df["customer_risk_category"].unique()
    )
    df = df[df["customer_risk_category"].isin(risk_filter)]



# =========================
# KPI CARDS (BI STYLE)

# KPI VALUES
total_bookings = len(df)
cancel_rate = df["is_cancelled"].mean() * 100
avg_adr = df["adr(average daily rate)"].mean()
avg_lead_time = df["lead_time"].mean()

# KPI ROW
col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Bookings", f"{total_bookings}")
col2.metric("❌ Cancellation Rate", f"{cancel_rate:.2f}%")
col3.metric("💰 Avg ADR", f"₹ {avg_adr:.2f}")
col4.metric("⏳ Avg Lead Time", f"{avg_lead_time:.1f}")

st.subheader("📌 Cancellation Distribution")

cancel_counts = df["is_cancelled"].value_counts()

fig1, ax1 = plt.subplots(figsize=(5,5))

ax1.pie(
    cancel_counts,
    labels=["Not Cancelled", "Cancelled"],
    autopct="%1.1f%%"
)

st.pyplot(fig1)




# DATA PREVIEW
# =========================
st.subheader("📁 Dataset Overview")
st.dataframe(df.head(10))

# =========================================
# 📈 BOOKING CHANNEL ANALYSIS
# =========================================

st.subheader("📈 Booking Channel Analysis")

channel_counts = df["booking_channel"].value_counts()

colors = [
    "royalblue",
    "crimson",
    "limegreen",
    "orange",
    "purple",
    "gold",
    "cyan"
]

fig, ax = plt.subplots(figsize=(8,4))

channel_counts.plot(
    kind="bar",
    color=colors,
    edgecolor="black",
    linewidth=1.5,
    ax=ax
)

ax.set_xlabel("Booking Channel")
ax.set_ylabel("Number of Bookings")

plt.xticks(rotation=0)

st.pyplot(fig)

st.markdown("---")


# =========================================
# 📊 CANCELLATION ANALYSIS
# =========================================

st.subheader("📊 Cancellation Analysis")

cancel_data = df["is_cancelled"].value_counts()

fig1, ax1 = plt.subplots(figsize=(6,4))

cancel_data.plot(
    kind="bar",
    color=["cyan", "crimson"],
    edgecolor="black",
    linewidth=1.5,
    ax=ax1
    
)

ax1.set_xticklabels(["Not Cancelled", "Cancelled"], rotation=0)
ax1.set_ylabel("Bookings")

st.pyplot(fig1)


# =========================================
# ⏳ LEAD TIME DISTRIBUTION
# =========================================

st.subheader("⏳ Lead Time Distribution")

fig2, ax2 = plt.subplots(figsize=(8,4))

sns.histplot(
    df["lead_time"],
    bins=30,
    kde=True,
    color="purple",
    ax=ax2
)

st.pyplot(fig2)


# =========================================
# 💰 ADR vs CANCELLATION
# =========================================

st.subheader("💰 ADR vs Cancellation")

fig3, ax3 = plt.subplots(figsize=(8,4))

sns.boxplot(
    x="is_cancelled",
    y="adr(average daily rate)",
    data=df,
    palette=["green", "orange"],
    ax=ax3
)

ax3.set_xticklabels(["Not Cancelled", "Cancelled"])

st.pyplot(fig3)

# =========================================
# 🌍 TOP COUNTRIES BY BOOKINGS
# =========================================

# =========================================
# 🌍 TOP COUNTRIES BY BOOKINGS
# =========================================

st.subheader("🌍 Top Countries by Bookings")

country_counts = df["country"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10,5))

country_counts.plot(
    kind="bar",
    color="lightgreen",      
    edgecolor="black",
    ax=ax
)

ax.set_xlabel("Country")
ax.set_ylabel("Bookings")

plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

# =========================================
# 📈 MONTHLY BOOKING TREND
# =========================================

st.subheader("📈 Monthly Booking Trend")

month_counts = df["booking_month"].value_counts()

fig5, ax5 = plt.subplots(figsize=(10,4))

month_counts.plot(
    kind="line",
    marker="o",
    linewidth=3,
    color="cyan",
    ax=ax5
)

st.pyplot(fig5)

# =========================================
# 🏨 REVENUE BY ROOM TYPE
# =========================================

st.subheader("🏨 Revenue by Room Type")

revenue_data = df.groupby("room_type")["total_revenue"].sum()

fig6, ax6 = plt.subplots(figsize=(8,4))

revenue_data.plot(
    kind="bar",
    color=["gold", "limegreen", "tomato", "deepskyblue"],
    ax=ax6
)

st.pyplot(fig6)

# =========================================
# 🔥 CORRELATION HEATMAP
# =========================================

st.subheader("🔥 Correlation Heatmap")

numeric_df = df.select_dtypes(include=np.number)

corr = numeric_df.corr()

fig7, ax7 = plt.subplots(figsize=(10,6))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=1,
    annot_kws={
        "size":10,
        "weight":"bold",
        "color":"black"
    },
    ax=ax7
)

st.pyplot(fig7)

# =========================================
# BOOKING CANCELLATION DISTRIBUTION
# =========================================

counts = df["is_cancelled"].value_counts()

plt.figure(figsize=(6,4))

cancel_colors = ["#85C1E9", "#F8C471"]

bars = plt.bar(
    ["Not Cancelled", "Cancelled"],
    counts.values,
    color=cancel_colors
)

# Add values
for bar in bars:
    yval = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        yval + 5,
        int(yval),
        ha='center'
    )

plt.title(
    "Booking Cancellation Distribution",
    fontsize=14,
    fontweight="bold"
)

plt.ylabel("Count")

plt.show()

# =========================================
# LEAD TIME VS CANCELLATION BOXPLOT
# =========================================

data = [
    df[df["is_cancelled"] == 0]["lead_time"],
    df[df["is_cancelled"] == 1]["lead_time"]
]

plt.figure(figsize=(8,6))

box = plt.boxplot(
    data,
    patch_artist=True,
    labels=["Not Cancelled", "Cancelled"]
)

box_colors = ["#85C1E9", "#F8C471"]

for patch, color in zip(box['boxes'], box_colors):
    patch.set_facecolor(color)

plt.title(
    "Lead Time vs Cancellation Status",
    fontsize=14,
    fontweight="bold"
)

plt.ylabel("Lead Time")

plt.grid(alpha=0.2)

plt.show()


# =========================
# MODEL BUILDING (BI INSIGHT LAYER)
# =========================
st.subheader("🤖 Cancellation Prediction Model")

# ENCODE ALL CATEGORICAL COLUMNS


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

# Find all object/string columns automatically
categorical_cols = df.select_dtypes(include=["object"]).columns

# Encode all categorical columns
for col in categorical_cols:
    df[col] = le.fit_transform(df[col].astype(str))
X = df.drop("is_cancelled", axis=1)
y = df["is_cancelled"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train, y_train)

y_proba = model.predict_proba(X_test)[:, 1]

auc = roc_auc_score(y_test, y_proba)

# =========================
# ROC CURVE (BI VISUAL)
# =========================
fpr, tpr, _ = roc_curve(y_test, y_proba)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Model Performance (ROC Curve)")
    fig2, ax2 = plt.subplots()
    ax2.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
    ax2.plot([0,1],[0,1],'--')
    ax2.legend()
    st.pyplot(fig2)

with col2:
    st.subheader("🏆 Model Score")
    st.success(f"ROC-AUC Score: {auc:.2f}")

# =========================
# BUSINESS INSIGHT SECTION
# =========================
st.markdown("---")
st.subheader("📌 Business Insights")

st.write("""
- Higher lead time increases cancellation risk  
- Certain booking channels show higher cancellations  
- Room type impacts booking stability  
- Model helps predict cancellations before arrival  
""")