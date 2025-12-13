import pandas as pd


def check_columns(df, cols):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))


def reviews_vs_rating(df):
    check_columns(df, ["rating", "review_count", "city", "name"])
    result = (
        df.groupby("city")
        .agg(
            avg_rating=("rating", "mean"),
            avg_review_count=("review_count", "mean"),
            n_shops=("name", "count")
        )
        .reset_index()
        .sort_values("avg_rating", ascending=False)
    )
    return result


def delivery_vs_rating(df):
    check_columns(df, ["rating", "delivery_available", "name"])
    result = (
        df.groupby("delivery_available")
        .agg(
            avg_rating=("rating", "mean"),
            count=("name", "count")
        )
        .reset_index()
        .sort_values("avg_rating", ascending=False)
    )
    return result


def price_vs_rating(df):
    check_columns(df, ["rating", "price_level", "name"])
    result = (
        df.groupby("price_level")
        .agg(
            avg_rating=("rating", "mean"),
            count=("name", "count")
        )
        .reset_index()
        .sort_values("price_level")
    )
    return result


def city_vs_rating(df):
    check_columns(df, ["rating", "city", "name"])
    result = (
        df.groupby("city")
        .agg(
            avg_rating=("rating", "mean"),
            n_shops=("name", "count")
        )
        .reset_index()
        .sort_values("avg_rating", ascending=False)
    )
    return result


def second_most_common_category(df):
    check_columns(df, ["categories"])
    expanded = df["categories"].str.split(",", expand=False).explode()
    expanded = expanded.str.strip()
    counts = expanded.value_counts()
    if "Ice Cream & Frozen Yogurt" in counts.index:
        counts = counts.drop("Ice Cream & Frozen Yogurt")
    if len(counts) == 0:
        return None
    return counts.index[0]
