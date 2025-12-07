"""Forecast service - orchestrates data preparation and model prediction."""

from typing import List

from .forecast_models.data_prep import create_dataset
from .forecast_models.model import create_model, get_model_mae
from .forecast_models.prediction import generate_predictions


def forecast(dataset: List[dict], day_forecast: int = 7) -> dict:
    """Generate sales forecast from historical data.

    Pipeline:
    1. Prepare data with feature engineering
    2. Create and train XGBoost model
    3. Evaluate model with MAE
    4. Generate future predictions
    5. Calculate aggregate metrics

    Args:
        dataset: List of dicts with historical sales (date, total_quantity)
        day_forecast: Number of days to forecast (default 7)

    Returns:
        Dict with:
            - predictions: List of daily forecasts
            - total_sales: Aggregate forecast
            - max_restock_quantity: Upper confidence bound
            - min_restock_quantity: Lower confidence bound
            - restock_quantity: Recommended restock quantity
            - goods_mae: Model mean absolute error
    """
    # Step 1: Prepare data with feature engineering
    df = create_dataset(dataset)

    # Step 2: Create training features
    X_train = df.drop(columns=["date", "total_quantity"]).reset_index(drop=True)
    y_train = df["total_quantity"]

    # Step 3: Create and train model
    model = create_model()
    goods_mae = get_model_mae(model, X_train, y_train)

    # Fit on full training data
    model.fit(X_train, y_train)

    # Step 4: Generate predictions
    future_preds = generate_predictions(
        model, df, pred_range=goods_mae, day=day_forecast
    )

    # Step 5: Calculate aggregate metrics
    total_sales_forecast = sum(pred["total_sales"] for pred in future_preds)
    max_restock_quantity = total_sales_forecast + goods_mae
    min_restock_quantity = max(0, total_sales_forecast - goods_mae)

    return {
        "predictions": future_preds,
        "total_sales": total_sales_forecast,
        "max_restock_quantity": max_restock_quantity,
        "min_restock_quantity": min_restock_quantity,
        "restock_quantity": total_sales_forecast,
        "goods_mae": goods_mae,
    }
