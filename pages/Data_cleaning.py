import pandas as pd
import streamlit as st

from utils import require_data


st.title("🧹 Data Cleaning Report")

clean_df = require_data()

raw_df = st.session_state.get(
    "raw_df",
    clean_df
)

report = st.session_state.get(
    "cleaning_report",
    {
        "original_rows": len(raw_df),
        "clean_rows": len(clean_df),
        "duplicates_removed": 0,
        "missing_values": 0
    }
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Original Rows",
    report["original_rows"]
)

col2.metric(
    "Clean Rows",
    report["clean_rows"]
)

col3.metric(
    "Duplicates Removed",
    report["duplicates_removed"]
)

col4.metric(
    "Missing Values Found",
    report["missing_values"]
)


st.divider()
st.subheader("Missing Values Before Cleaning")

missing_df = pd.DataFrame({
    "Column": raw_df.columns,
    "Missing Values": raw_df.isnull().sum().values,
    "Missing Percentage": (
        raw_df.isnull().mean().values * 100
    ).round(2)
})

st.dataframe(
    missing_df,
    use_container_width=True
)


st.divider()
st.subheader("Cleaned Column Types")

types_df = pd.DataFrame({
    "Column": clean_df.columns,
    "Data Type": clean_df.dtypes.astype(str)
})

st.dataframe(
    types_df,
    use_container_width=True
)


st.divider()
st.subheader("Cleaned Dataset")

st.dataframe(
    clean_df,
    use_container_width=True
)


csv_data = clean_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Cleaned Dataset",
    data=csv_data,
    file_name="cleaned_sales_dataset.csv",
    mime="text/csv"
)