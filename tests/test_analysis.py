import pandas as pd
from yelp_final_project.analysis import (
    reviews_vs_rating,
    delivery_vs_rating,
    price_vs_rating,
    city_vs_rating,
    second_most_common_category,
)
from yelp_final_project.cleaning import clean_data


def test_reviews_vs_rating_runs():
    df = clean_data()
    out = reviews_vs_rating(df)
    assert isinstance(out, pd.DataFrame)


def test_delivery_vs_rating_runs():
    df = clean_data()
    out = delivery_vs_rating(df)
    assert isinstance(out, pd.DataFrame)


def test_price_vs_rating_runs():
    df = clean_data()
    out = price_vs_rating(df)
    assert isinstance(out, pd.DataFrame)


def test_city_vs_rating_runs():
    df = clean_data()
    out = city_vs_rating(df)
    assert isinstance(out, pd.DataFrame)


def test_second_most_common_category_runs():
    df = clean_data()
    result = second_most_common_category(df)
    assert isinstance(result, str) or pd.isna(result)
