import streamlit as st

from utils import require_data


st.title("🤖 Business Analytics Assistant")

st.caption(
    "Ask about sales, profit, products, customers, "
    "regions, states or orders."
)

df = require_data()


def answer_question(question):
    question = question.lower().strip()

    if "total sales" in question:
        return (
            f"Total sales are "
            f"${df['Sales'].sum():,.2f}."
        )

    if "total profit" in question:
        return (
            f"Total profit is "
            f"${df['Profit'].sum():,.2f}."
        )

    if (
        "highest profit product" in question
        or "most profitable product" in question
    ):
        profits = df.groupby(
            "Product Name"
        )["Profit"].sum()

        product = profits.idxmax()

        return (
            f"The most profitable product is "
            f"{product}, with "
            f"${profits.max():,.2f} in profit."
        )

    if (
        "best selling product" in question
        or "highest sales product" in question
    ):
        sales = df.groupby(
            "Product Name"
        )["Sales"].sum()

        product = sales.idxmax()

        return (
            f"The best-selling product is "
            f"{product}, with "
            f"${sales.max():,.2f} in sales."
        )

    if "top customer" in question:
        customers = df.groupby(
            "Customer Name"
        )["Sales"].sum()

        customer = customers.idxmax()

        return (
            f"The top customer is {customer}, "
            f"with ${customers.max():,.2f} "
            f"in purchases."
        )

    if "best region" in question:
        regions = df.groupby(
            "Region"
        )["Sales"].sum()

        region = regions.idxmax()

        return (
            f"The best region is {region}, "
            f"with ${regions.max():,.2f} in sales."
        )

    if "best state" in question:
        states = df.groupby(
            "State"
        )["Sales"].sum()

        state = states.idxmax()

        return (
            f"The best state is {state}, "
            f"with ${states.max():,.2f} in sales."
        )

    if "profit margin" in question:
        sales = df["Sales"].sum()
        profit = df["Profit"].sum()

        margin = (
            profit / sales * 100
            if sales != 0
            else 0
        )

        return (
            f"The overall profit margin is "
            f"{margin:.2f}%."
        )

    if "orders" in question:
        orders = df["Order ID"].nunique()

        return f"There are {orders:,} unique orders."

    if "customers" in question:
        customers = df[
            "Customer Name"
        ].nunique()

        return (
            f"There are {customers:,} "
            f"unique customers."
        )

    return (
        "I do not understand that question yet. "
        "Try asking about total sales, total profit, "
        "best product, top customer, best region, "
        "best state, profit margin or orders."
    )


examples = [
    "",
    "What are the total sales?",
    "What is the total profit?",
    "Which is the highest profit product?",
    "Which is the best selling product?",
    "Who is the top customer?",
    "Which is the best region?",
    "Which is the best state?",
    "What is the profit margin?",
    "How many orders are there?"
]

selected_example = st.selectbox(
    "Example questions",
    examples
)

question = st.text_input(
    "Ask your question",
    value=selected_example
)

if st.button(
    "Ask Assistant",
    type="primary"
):
    if question.strip():
        st.success(
            answer_question(question)
        )
    else:
        st.warning("Enter a question first.")