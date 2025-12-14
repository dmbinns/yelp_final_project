from __future__ import annotations

import io
from contextlib import redirect_stdout

import pandas as pd
import streamlit as st
import plotly.express as px

from yelp_final_project.cleaning import clean_data
from yelp_final_project.analysis import (
    reviews_vs_rating,
    price_vs_rating,
    city_vs_rating,
    second_most_common_category,
    service_type_vs_rating,
)


def _sample_data() -> pd.DataFrame:
    """Small placeholder dataset for rapid UI feedback."""
    return pd.DataFrame(
        {
            "team": ["alpha", "beta", "gamma"],
            "metric_a": [0.72, 0.55, 0.91],
            "metric_b": [12, 9, 17],
        }
    )


def _run_with_capture(func) -> str:
    """Capture stdout from placeholder pipelines so Streamlit can display it."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()
    return buffer.getvalue().strip()


def main() -> None:
    st.set_page_config(
        page_title="Yelp Ice Cream Shop Ratings in Utah",
        layout="wide",
        page_icon="🍦",
    )
    st.title("🍦 Yelp Ice Cream Shop Ratings in Utah")
    st.write(
        "Welcome! This dashboard lets you explore Utah ice cream shop data pulled from Yelp. "
    "Use the tools on the left to filter shops by city, price level, or service type. "
    "Explore the graphs showing how these factors relate to customer ratings."
    )

    with st.sidebar:
        st.header("Controls")
        dataset_choice = st.selectbox("Dataset", ["Sample Data", "Upload CSV"])
        show_cleaning = st.checkbox("Show cleaned data")
        show_analysis = st.checkbox("Show analysis summaries")

    if dataset_choice == "Sample Data":
        df = _sample_data()
    else:
        uploaded = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.info("No file uploaded yet. Falling back to the sample data so the widgets stay live.")
            df = _sample_data()

    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    st.write("### Quick Dataset Summary")
    cleaned_for_summary = clean_data()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Shops", len(cleaned_for_summary))
    col2.metric("Cities Covered", cleaned_for_summary["city"].nunique())
    col3.metric("Service Types", cleaned_for_summary["service_type"].nunique())

    st.subheader("📋 Data Preview (Cleaned Sample)")

    clean_preview = clean_data()
    st.dataframe(
        clean_preview[["name", "city", "rating", "review_count", "price_level", "service_type"]]
        .head(20),
        use_container_width=True
    )


    if show_cleaning:
        st.subheader("Cleaned Data")
        cleaned = clean_data()
        st.dataframe(cleaned, use_container_width=True)
        st.caption("This is the cleaned dataset after processing.")

    enable_filters = st.sidebar.checkbox("Enable filters")

    if enable_filters:
        st.subheader("🔍 Filtered Results (Optional)")

        filtered = clean_data().copy()   # start with full cleaned dataset

        with st.expander("Filter Options"):
            city = st.selectbox("City", ["All"] + sorted(filtered["city"].dropna().unique()))
            price = st.multiselect(
                "Price Level ($–$$$$)",
                sorted(filtered["price_level"].dropna().unique())
            )
            service = st.multiselect(
                "Service Type (e.g., Takeout, Delivery, Dine-In)",
                sorted(filtered["service_type"].dropna().unique())
            )

        # APPLY FILTERS
        if city != "All":
            filtered = filtered[filtered["city"] == city]

        if price:
            filtered = filtered[filtered["price_level"].isin(price)]

        if service:
            filtered = filtered[filtered["service_type"].isin(service)]

        st.write("### Filtered Results")
        st.dataframe(filtered, use_container_width=True)


    if show_analysis:
        st.subheader("Analysis Summaries")
        cleaned = clean_data()

        st.write("### ⭐ Reviews vs Rating")
        summary_reviews = reviews_vs_rating(cleaned)
        st.dataframe(summary_reviews)

        st.write("#### Scatter Plot")
        fig1 = px.scatter(
            cleaned,
            x="review_count",
            y="rating",
            size="review_count",
            color="city",
            hover_name="name",
            title="Review Count vs Rating",
        )
        st.plotly_chart(fig1, use_container_width=True)


        st.write("### 🍦 Service Type vs Rating")
        service_summary = service_type_vs_rating(cleaned)
        st.dataframe(service_summary)

        fig2 = px.bar(
            service_summary,
            x="service_type",
            y="avg_rating",
            color="service_type",
            title="Average Rating by Service Type",
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.write("### 🥧 Service Type Distribution")

        service_counts = cleaned["service_type"].value_counts().reset_index()
        service_counts.columns = ["service_type", "count"]

        fig3 = px.bar(
            service_counts,
            x="count",
            y="service_type",
            orientation="h",
            text="count",
            color="service_type",
            title="Distribution of Service Types",
        )

        fig3.update_layout(
            yaxis_title="Service Type",
            xaxis_title="Number of Shops",
            showlegend=False
        )

        st.plotly_chart(fig3, use_container_width=True)


        st.write("### 💲 Price vs Rating")
        summary_price = price_vs_rating(cleaned)
        st.dataframe(summary_price)

        fig4 = px.line(
            summary_price,
            x="price_level",
            y="avg_rating",
            markers=True,
            title="Average Rating by Price Level",
        )
        st.plotly_chart(fig4, use_container_width=True)


        st.write("### 🏙️ City vs Rating")
        summary_city = city_vs_rating(cleaned)
        st.dataframe(summary_city)

        fig5 = px.bar(
            summary_city,
            x="city",
            y="avg_rating",
            title="Average Rating by City",
        )
        st.plotly_chart(fig5, use_container_width=True)


        st.write("### 🍪 Second Most Common Category (besides Ice Cream)")
        second_cat = second_most_common_category(cleaned)
        st.success(f"Second most common category: **{second_cat}**")

                # ---------------- MAP OF UTAH ----------------
        st.write("### 🗺️ Map of Utah Ice Cream Shops")

        if "coordinates.latitude" in cleaned.columns and "coordinates.longitude" in cleaned.columns:
            fig_map = px.scatter_mapbox(
                cleaned,
                lat="coordinates.latitude",
                lon="coordinates.longitude",
                color="rating",
                size="review_count",
                hover_name="name",
                hover_data={"city": True, "rating": True, "review_count": True},
                color_continuous_scale="Icefire",
                zoom=6.2,
                height=600,
                title="Utah Ice Cream Shop Locations",
            )

            fig_map.update_layout(mapbox_style="open-street-map")
            fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))

            st.plotly_chart(fig_map, use_container_width=True)

        else:
            st.error("No latitude/longitude columns found — cannot generate map.")

                
                

    st.info(
        "Try adjusting filters or switching datasets in the sidebar to explore trends more deeply!"
    )


if __name__ == "__main__":
    main()


## To run be in yelp_final_project main folder
## run in terminal run: streamlit run src/yelp_final_project/streamlit_app.py 