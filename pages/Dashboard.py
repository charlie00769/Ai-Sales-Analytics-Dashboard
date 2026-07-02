import streamlit as st
import plotly.express as px

from utils import require_data, apply_sidebar_filters


st.title("📊 Executive Dashboard")

df = require_data()
df = apply_sidebar_filters(df)

if df.empty:
    st.warning("No rows match the selected filters.")
    st.stop()


total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer Name"].nunique()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Orders", f"{total_orders:,}")

col4, col5, col6 = st.columns(3)

col4.metric("👥 Customers", f"{total_customers:,}")
col5.metric(
    "🛒 Average Order Value",
    f"${average_order_value:,.2f}"
)
col6.metric(
    "💹 Profit Margin",
    f"{profit_margin:.2f}%"
)


st.divider()
st.subheader("📈 Monthly Sales Trend")

monthly = df.dropna(subset=["Order Date"]).copy()

monthly["Month"] = (
    monthly["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    monthly
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)

figure = px.line(
    monthly,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    figure,
    use_container_width=True
)


left, right = st.columns(2)

category_sales = (
    df.groupby("Category", as_index=False)["Sales"]
    .sum()
)

category_figure = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Sales",
    title="Sales by Category"
)

left.plotly_chart(
    category_figure,
    use_container_width=True
)


region_sales = (
    df.groupby("Region", as_index=False)["Sales"]
    .sum()
)

region_figure = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    hole=0.4,
    title="Sales by Region"
)

right.plotly_chart(
    region_figure,
    use_container_width=True
)


st.divider()
st.subheader("🏆 Top 10 Products")

top_products = (
    df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .nlargest(10, "Sales")
)

product_figure = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top Products by Sales"
)

product_figure.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    product_figure,
    use_container_width=True
)


st.divider()
st.subheader("💹 Profit by Sub-Category")

profit_data = (
    df.groupby("Sub-Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

profit_figure = px.bar(
    profit_data,
    x="Sub-Category",
    y="Profit",
    color="Profit",
    color_continuous_scale="RdYlGn",
    title="Profit by Sub-Category"
)

st.plotly_chart(
    profit_figure,
    use_container_width=True
)


st.divider()
st.subheader("🗺️ Sales by State")

state_sales = (
    df.groupby("State", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

state_figure = px.bar(
    state_sales,
    x="State",
    y="Sales",
    color="Sales",
    title="Sales by State"
)

state_figure.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    state_figure,
    use_container_width=True
)