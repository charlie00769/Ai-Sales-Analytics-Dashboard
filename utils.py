import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = {
    "Order ID",
    "Order Date",
    "Customer Name",
    "Segment",
    "Region",
    "State",
    "Category",
    "Sub-Category",
    "Product Name",
    "Sales",
    "Profit"
}


def load_csv(uploaded_file):
    attempts = [
        {},
        {"encoding": "latin1"},
        {"encoding": "latin1", "sep": ";"},
        {"encoding": "utf-8", "sep": ";"}
    ]

    last_error = None

    for options in attempts:
        uploaded_file.seek(0)

        try:
            return pd.read_csv(
                uploaded_file,
                **options
            )
        except Exception as error:
            last_error = error

    raise last_error


def validate_columns(df):
    return sorted(
        REQUIRED_COLUMNS.difference(df.columns)
    )


def prepare_data(df):
    clean_df = df.copy()

    original_rows = len(clean_df)
    duplicates = int(clean_df.duplicated().sum())
    missing_values = int(
        clean_df.isnull().sum().sum()
    )

    clean_df = clean_df.drop_duplicates().copy()

    for column in ["Sales", "Profit"]:
        clean_df[column] = pd.to_numeric(
            clean_df[column],
            errors="coerce"
        )

        median = clean_df[column].median()

        if pd.isna(median):
            median = 0

        clean_df[column] = clean_df[
            column
        ].fillna(median)

    clean_df["Order Date"] = pd.to_datetime(
        clean_df["Order Date"],
        errors="coerce"
    )

    text_columns = clean_df.select_dtypes(
        include=["object", "string"]
    ).columns

    clean_df[text_columns] = clean_df[
        text_columns
    ].fillna("Not Available")

    report = {
        "original_rows": original_rows,
        "clean_rows": len(clean_df),
        "duplicates_removed": duplicates,
        "missing_values": missing_values
    }

    return clean_df, report


def require_data():
    if "clean_df" not in st.session_state:
        st.warning(
            "⚠️ Upload a dataset from the Home page first."
        )
        st.stop()

    return st.session_state["clean_df"].copy()


def apply_sidebar_filters(df):
    st.sidebar.divider()
    st.sidebar.subheader("🔍 Filters")

    selections = {}

    for column in ["Region", "Category", "Segment"]:
        options = sorted(
            df[column].dropna().unique().tolist()
        )

        selections[column] = st.sidebar.multiselect(
            f"Select {column}",
            options=options,
            default=options
        )

    filtered_df = df[
        df["Region"].isin(selections["Region"])
        & df["Category"].isin(selections["Category"])
        & df["Segment"].isin(selections["Segment"])
    ].copy()

    return filtered_df