import streamlit as st

from utils import (
    load_csv,
    prepare_data,
    validate_columns
)


st.set_page_config(
    page_title="AI Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def home_page():
    st.title("📊 AI Sales Analytics Platform")

    st.write(
        """
        Upload your sales dataset and explore:

        - Business KPIs
        - Interactive dashboards
        - Data-cleaning results
        - Product, customer and regional insights
        - AI-style business questions
        """
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "📂 Upload Sales CSV",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            raw_df = load_csv(uploaded_file)

            missing_columns = validate_columns(
                raw_df
            )

            if missing_columns:
                st.error(
                    "The dataset is missing these columns: "
                    + ", ".join(missing_columns)
                )
                st.stop()

            clean_df, report = prepare_data(
                raw_df
            )

            # Save data so every page can access it
            st.session_state["raw_df"] = raw_df
            st.session_state["clean_df"] = clean_df

            st.session_state[
                "cleaning_report"
            ] = report

            st.session_state[
                "uploaded_filename"
            ] = uploaded_file.name

            st.success(
                "✅ Dataset uploaded and cleaned successfully!"
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

            st.subheader("Dataset Preview")

            st.dataframe(
                clean_df.head(10),
                use_container_width=True
            )

            st.info(
                "👈 Select Dashboard, Data Cleaning, "
                "Business Insights or AI Assistant "
                "from the sidebar."
            )

        except Exception as error:
            st.error(
                f"Could not process this dataset: {error}"
            )

    elif "clean_df" in st.session_state:
        filename = st.session_state.get(
            "uploaded_filename",
            "Dataset"
        )

        st.success(
            f"✅ {filename} is currently loaded."
        )

        st.dataframe(
            st.session_state["clean_df"].head(10),
            use_container_width=True
        )

        if st.button("🗑️ Remove Current Dataset"):
            keys_to_remove = [
                "raw_df",
                "clean_df",
                "cleaning_report",
                "uploaded_filename"
            ]

            for key in keys_to_remove:
                st.session_state.pop(
                    key,
                    None
                )

            st.rerun()

    else:
        st.info(
            "Upload your sales CSV file to begin."
        )

        st.subheader(
            "Required Dataset Columns"
        )

        st.code(
            """
Order ID
Order Date
Customer Name
Segment
Region
State
Category
Sub-Category
Product Name
Sales
Profit
            """
        )


# Create the navigation menu
navigation = st.navigation(
    {
        "Main": [
            st.Page(
                home_page,
                title="Home",
                icon="🏠",
                default=True
            )
        ],
        "Analytics": [
            st.Page(
                "pages/Dashboard.py",
                title="Dashboard",
                icon="📊"
            ),
            st.Page(
                "pages/Data_cleaning.py",
                title="Data Cleaning",
                icon="🧹"
            ),
            st.Page(
                "pages/Business_Insights.py",
                title="Business Insights",
                icon="💡"
            ),
            st.Page(
                "pages/AI_Assistant.py",
                title="AI Assistant",
                icon="🤖"
            )
        ]
    },
    position="sidebar"
)


# Run the selected page
navigation.run()