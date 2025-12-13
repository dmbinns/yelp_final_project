from __future__ import annotations

import io
from contextlib import redirect_stdout

import pandas as pd
import streamlit as st

from yelp_final_project.cleaning import clean_data, load_data
from yelp_final_project.analysis import (
    reviews_vs_rating,
    delivery_vs_rating,
    price_vs_rating,
    city_vs_rating,
    second_most_common_category,
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
    st.set_page_config(page_title="Yelp Ice Cream Shop Ratings in Utah", layout="wide")
    st.title("Yelp Ice Cream Shop Ratings in Utah")
    st.write(
        "This Streamlit app lets you explore the dataset, run the cleaning pipeline, "
        "and view analysis summaries for your STAT 386 final project."
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



    if show_cleaning:
        st.subheader("Cleaned Data")
        cleaned = clean_data()
        st.code(cleaned, use_container_width=True)
        st.caption("Replace clean_data with your real preprocessing logic.")

    if show_analysis:
        st.subheader("Analysis Summaries")
        cleaned = clean_data()

        st.write("### ⭐ Reviews vs Rating")
        st.dataframe(reviews_vs_rating(cleaned))

        st.write("### 🚚 Delivery vs Rating")
        st.dataframe(delivery_vs_rating(cleaned))

        st.write("### 💲 Price vs Rating")
        st.dataframe(price_vs_rating(cleaned))

        st.write("### 🏙️ City vs Rating")
        st.dataframe(city_vs_rating(cleaned))

        st.write("### 🍪 Second Most Common Category (besides Ice Cream)")
        second_cat = second_most_common_category(cleaned)
        st.success(f"Second most common category: **{second_cat}**")

    st.info(
        "Next steps: customize the sidebar controls, drop in Streamlit charts (st.bar_chart, st.map, etc.), "
        "and layer in explanations so stakeholders can self-serve results."
    )


if __name__ == "__main__":
    main()


## To run be in yelp_final_project main folder
## run in terminal run: streamlit run src\yelp_final_project\streamlit_app.py 