"""Data preparation utilities for forecasting models."""

import pandas as pd


def create_dataset(sales_history: list) -> pd.DataFrame:
    """Create feature-engineered dataset from sales history.

    Performs the following transformations:
    - Converts date to datetime
    - Extracts day of week and weekend indicator
    - Creates lagged features (1, 2, 3, and optionally 7 days)
    - Removes null values
    - Limits to last 30 records for recency bias

    Args:
        sales_history: List of dicts with 'date' and 'total_quantity' keys

    Returns:
        Processed pandas DataFrame ready for model training
    """
    df = pd.DataFrame(sales_history)

    df["date"] = pd.to_datetime(df["date"])
    df["dayofweek"] = df["date"].dt.dayofweek
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    # Create lag features based on data availability
    if len(df) >= 15:
        lags = [1, 2, 3, 7]
    else:
        lags = [1, 2, 3]
    for lag in lags:
        df[f"lag_{lag}"] = df["total_quantity"].shift(lag)

    # Drop rows with NaN values and reset index
    df = df.dropna().reset_index(drop=True)

    # Keep only recent data for recency bias
    if len(df) >= 30:
        df = df[-30:]

    return df
