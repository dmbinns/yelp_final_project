import pandas as pd
from yelp_final_project.cleaning import (
    load_data,
    clean_columns,
    convert_price,
    clean_delivery,
    drop_columns,
    sort_cities,
    clean_data,
)


def test_load_data_runs():
    df = load_data()
    assert isinstance(df, pd.DataFrame)


def test_clean_columns_lowercase():
    df = pd.DataFrame({"City Name": ["Provo"]})
    cleaned = clean_columns(df)
    assert "city_name" in cleaned.columns


def test_convert_price_creates_column():
    df = pd.DataFrame({"price": ["$", "$$", None]})
    cleaned = convert_price(df)
    assert "price_level" in cleaned.columns


def test_clean_delivery_creates_column():
    df = pd.DataFrame({"delivery": ["Yes", "No"]})
    cleaned = clean_delivery(df)
    assert "delivery_available" in cleaned.columns


def test_drop_columns_runs():
    df = pd.DataFrame(
        {
            "a": [1],
            "b": [2],
            "is_closed": [True],
            "attributes.business_temp_closed": ["No"],
            "attributes.menu_url": ["url"],
            "attributes.waitlist_reservation": ["yes"],
            "attributes.open24_hours": ["no"]
        }
    )
    cleaned = drop_columns(df)
    assert "is_closed" not in cleaned.columns
    assert "attributes.business_temp_closed" not in cleaned.columns
    assert "attributes.menu_url" not in cleaned.columns
    assert "attributes.waitlist_reservation" not in cleaned.columns
    assert "attributes.open24_hours" not in cleaned.columns


def test_sort_cities_runs():
    df = pd.DataFrame({"city": ["Provo", "Ogden", "Lehi"]})
    cleaned = sort_cities(df)
    assert list(cleaned["city"]) == ["Lehi", "Ogden", "Provo"]


def test_clean_data_runs():
    df = clean_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
