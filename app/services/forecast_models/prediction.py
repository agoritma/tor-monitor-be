"""Prediction generation for time series forecasting."""

from itertools import repeat
from typing import List

import pandas as pd
from xgboost import XGBRegressor


def generate_predictions(
    model: XGBRegressor, dataset: pd.DataFrame, pred_range: int, day: int = 7
) -> List[dict]:
    """Generate future sales predictions using trained model.

    Creates rolling predictions by:
    1. Taking the last row as context
    2. Predicting next day
    3. Adding prediction to dataset
    4. Repeating for N days

    Args:
        model: Trained XGBoost model
        dataset: Feature-engineered dataset with training features
        pred_range: Range for confidence interval (min/max bounds)
        day: Number of days to forecast (default 7)

    Returns:
        List of dicts with date, total_sales, max_sales, min_sales
    """
    future_preds = []
    latest = dataset.copy()

    for _ in repeat(None, day):
        last_row = latest.iloc[-1:].copy()

        # Calculate next date
        next_date = last_row["date"].iloc[0] + pd.Timedelta(days=1)

        # Build feature row for prediction
        row = {
            "date": next_date,
            "dayofweek": next_date.dayofweek,
            "is_weekend": 1 if next_date.dayofweek in [5, 6] else 0,
            "lag_1": last_row["total_quantity"].iloc[0],
            "lag_2": last_row["lag_1"].iloc[0],
            "lag_3": last_row["lag_2"].iloc[0],
        }

        # Add lag_7 if available in training data
        if len(dataset) >= 15:
            row["lag_7"] = latest["total_quantity"].iloc[-7]

        row_df = pd.DataFrame([row])
        y_pred = round(model.predict(row_df.drop(columns=["date"]))[0])

        # Update row with prediction and add to dataset
        row["total_quantity"] = y_pred
        latest = pd.concat([latest, pd.DataFrame([row])], ignore_index=True)

        # Store prediction with confidence bounds
        future_preds.append(
            {
                "date": str(next_date.date()),
                "total_sales": y_pred,
                "max_sales": y_pred + pred_range,
                "min_sales": (y_pred - pred_range) if y_pred >= pred_range else 0,
            }
        )

    return future_preds
