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


def clean_delivery(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "transactions" in df.columns:
        def parse_list(x):
            if isinstance(x, list):
                return x
            if isinstance(x, str) and x.startswith("["):
                try:
                    return eval(x)
                except Exception:
                    return []
            return []

        df["transactions"] = df["transactions"].apply(parse_list)

        df["pickup_available"] = df["transactions"].apply(
            lambda x: "Yes" if "pickup" in x else "No"
        )

        def service_type(x):
            has_delivery = "delivery" in x
            has_pickup = "pickup" in x

            if has_delivery and has_pickup:
                return "Both"
            elif has_delivery:
                return "Delivery Only"
            elif has_pickup:
                return "Pickup Only"
            else:
                return "Neither"

        df["service_type"] = df["transactions"].apply(service_type)

    else:
        df["pickup_available"] = pd.NA
        df["service_type"] = pd.NA

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