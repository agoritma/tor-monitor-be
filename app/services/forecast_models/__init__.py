"""Forecast models package - modules for time series prediction.

Modules:
    data_prep: Data preparation and feature engineering
    model: XGBoost model creation and training
    prediction: Future prediction generation
"""

from .data_prep import create_dataset
from .model import create_model, get_model_mae
from .prediction import generate_predictions

__all__ = [
    "create_dataset",
    "create_model",
    "get_model_mae",
    "generate_predictions",
]
