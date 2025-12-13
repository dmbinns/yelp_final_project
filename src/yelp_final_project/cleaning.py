import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "yelp_icecream_shops_utah.csv"


def load_data(path=DATA_PATH):
    return pd.read_csv(path)


def convert_price(df):
    if "price" in df.columns:
        df["price_level"] = (
            df["price"]
            .astype(str)
            .str.count(r"\$")  
            .replace(0, pd.NA)
        )
    else:
        df["price_level"] = pd.NA
    return df


def clean_delivery(df):
    df = df.copy()
    can_deliver = ["delivery"]
    delivery_col = None
    for col in can_deliver:
        if col in df.columns:
            delivery_col = col
            break
    if delivery_col is not None:
        df["delivery_available"] = (
            df[delivery_col]
            .astype(str)
            .str.lower()
            .str.contains("yes|true|delivery")
        ).map({True: "Yes", False: "No"})
    else:
        df["delivery_available"] = pd.NA
    return df


def clean_columns(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def drop_columns(df):
    df = df.copy()
    df = df.drop(columns=["is_closed", "attributes.business_temp_closed", "attributes.menu_url", "attributes.waitlist_reservation", "attributes.open24_hours"], errors="ignore")
    return df

def sort_cities(df):
    df = df.copy()
    if "city" in df.columns:
        df = df.sort_values("city")
    return df

def clean_data(path=DATA_PATH):
    df = load_data(path)
    df = clean_columns(df)
    if "location.city" in df.columns and "city" not in df.columns:
        df["city"] = df["location.city"]
    df = drop_columns(df)
    df = convert_price(df)
    df = clean_delivery(df)
    df = sort_cities(df)
    df = df.reset_index(drop=True)

    return df