"""XGBoost utilities for loading and preparing sklearn datasets."""

from xgb_utils.get_data import (
    DATASET_CLASSES,
    BreastCancerDataset,
    DiabetesDataset,
    DigitsDataset,
    IrisDataset,
    LinnerudDataset,
    WineDataset,
    XGBDataset,
    get_dataset,
)

__all__ = [
    "DATASET_CLASSES",
    "BreastCancerDataset",
    "DiabetesDataset",
    "DigitsDataset",
    "IrisDataset",
    "LinnerudDataset",
    "WineDataset",
    "XGBDataset",
    "get_dataset",
]
