import streamlit as st
import plotly.express as px

from utils import require_data, apply_sidebar_filters


st.title("💡 Business Insights")

df = require_data()
df = apply_sidebar_filters(df)

if df.empty:
    st.warning("No rows match the selected filters.")
    st.stop()


product_performance = (
    df.groupby("Product Name", as_index=False)
    .agg({
        "Sales": "sum",
        "Profit": "sum"
    })
)

best_product = product_performance.loc[
    product_performance["Sales"].idxmax()
]

worst_product = product_performance.loc[
    product_performance["Profit"].idxmin()
]


customer_performance = (
    df.groupby("Customer Name", as_index=False)["Sales"]
    .sum()
)

best_customer = customer_performance.loc[
    customer_performance["Sales"].idxmax()
]


state_performance = (
    df.groupby("State", as_index=False)["Sales"]
    .sum()
)

best_state = state_performance.loc[
    state_performance["Sales"].idxmax()
]


col1, col2 = st.columns(2)

col1.success(
    f"🏆 Best-selling product: "
    f"{best_product['Product Name']} — "
    f"${best_product['Sales']:,.2f}"
)

col2.error(
    f"⚠️ Lowest-profit product: "
    f"{worst_product['Product Name']} — "
    f"${worst_product['Profit']:,.2f}"
)

col3, col4 = st.columns(2)

col3.info(
    f"👤 Top customer: "
    f"{best_customer['Customer Name']} — "
    f"${best_customer['Sales']:,.2f}"
)

col4.info(
    f"🗺️ Best state: "
    f"{best_state['State']} — "
    f"${best_state['Sales']:,.2f}"
)


st.divider()
st.subheader("👥 Top 10 Customers")

top_customers = customer_performance.nlargest(
    10,
    "Sales"
)

customer_figure = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    color="Sales",
    title="Top Customers by Sales"
)

customer_figure.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    customer_figure,
    use_container_width=True
)


st.divider()
st.subheader("📦 Product Performance")

product_figure = px.scatter(
    product_performance,
    x="Sales",
    y="Profit",
    hover_name="Product Name",
    color="Profit",
    size="Sales",
    title="Product Sales vs Profit"
)

st.plotly_chart(
    product_figure,
    use_container_width=True
)


st.divider()
st.subheader("✅ Recommendations")

unprofitable_products = product_performance[
    product_performance["Profit"] < 0
]

st.write(
    f"- Review {len(unprofitable_products)} "
    "products currently generating losses."
)

st.write(
    f"- Maintain inventory for "
    f"{best_product['Product Name']}."
)

st.write(
    f"- Prioritize marketing in "
    f"{best_state['State']}."
)

st.write(
    f"- Create a loyalty offer for "
    f"{best_customer['Customer Name']}."
)