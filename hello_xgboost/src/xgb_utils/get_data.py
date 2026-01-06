from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.datasets import (
    load_breast_cancer,
    load_diabetes,
    load_digits,
    load_iris,
    load_linnerud,
    load_wine,
)


# =============================================================================
# Helper Functions
# =============================================================================


def _load_sklearn_data(name: str) -> tuple[pd.DataFrame, pd.Series, str]:
    """Load sklearn dataset by name, return X, y, and task_type."""
    loaders = {
        "iris": (load_iris, "classification"),
        "wine": (load_wine, "classification"),
        "breast_cancer": (load_breast_cancer, "classification"),
        "digits": (load_digits, "classification"),
        "diabetes": (load_diabetes, "regression"),
        "linnerud": (load_linnerud, "regression"),
    }

    if name not in loaders:
        valid = ", ".join(loaders.keys())
        raise ValueError(f"Unknown dataset: {name}. Valid options: {valid}")

    loader_fn, task_type = loaders[name]
    data = loader_fn()

    X = pd.DataFrame(data.data, columns=data.feature_names)

    # Linnerud has multiple targets - use first one
    if name == "linnerud":
        y = pd.Series(data.target[:, 0], name=data.target_names[0])
    else:
        y = pd.Series(data.target)

    return X, y, task_type


def _create_split_masks(
    n_samples: int,
    y: pd.Series,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    stratify: bool,
    random_state: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create binary mask vectors for train/val/test splits.

    Args:
        n_samples: Total number of samples
        y: Target values (used for stratification)
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
        stratify: Whether to stratify by target values
        random_state: Random seed for reproducibility

    Returns:
        Three boolean arrays (train_mask, val_mask, test_mask)
    """
    if not np.isclose(train_ratio + val_ratio + test_ratio, 1.0):
        raise ValueError("Split ratios must sum to 1.0")

    rng = np.random.default_rng(random_state)

    if stratify:
        # Stratified sampling: maintain class proportions in each split
        train_mask = np.zeros(n_samples, dtype=bool)
        val_mask = np.zeros(n_samples, dtype=bool)
        test_mask = np.zeros(n_samples, dtype=bool)

        for class_val in y.unique():
            class_indices = np.where(y == class_val)[0]
            n_class = len(class_indices)

            # Shuffle indices within this class
            shuffled = rng.permutation(class_indices)

            # Calculate split points
            n_train = int(n_class * train_ratio)
            n_val = int(n_class * val_ratio)

            # Assign to splits
            train_mask[shuffled[:n_train]] = True
            val_mask[shuffled[n_train : n_train + n_val]] = True
            test_mask[shuffled[n_train + n_val :]] = True
    else:
        # Random sampling without stratification
        indices = rng.permutation(n_samples)

        n_train = int(n_samples * train_ratio)
        n_val = int(n_samples * val_ratio)

        train_mask = np.zeros(n_samples, dtype=bool)
        val_mask = np.zeros(n_samples, dtype=bool)
        test_mask = np.zeros(n_samples, dtype=bool)

        train_mask[indices[:n_train]] = True
        val_mask[indices[n_train : n_train + n_val]] = True
        test_mask[indices[n_train + n_val :]] = True

    return train_mask, val_mask, test_mask


def _apply_mask(
    X: pd.DataFrame, y: pd.Series, mask: np.ndarray
) -> tuple[pd.DataFrame, pd.Series]:
    """Apply a boolean mask to extract a subset of data."""
    return X.loc[mask].reset_index(drop=True), y.loc[mask].reset_index(drop=True)


# =============================================================================
# Parent Dataclass
# =============================================================================


@dataclass
class XGBDataset:
    """Base class for XGBoost-ready datasets.

    Attributes:
        X: Feature data as DataFrame
        y: Target data as Series
        train_mask: Boolean mask for training samples
        val_mask: Boolean mask for validation samples
        test_mask: Boolean mask for test samples
        processor: Optional callable to transform (X, y) before DMatrix creation
        name: Dataset name
        task_type: Either "classification" or "regression"
    """

    X: pd.DataFrame
    y: pd.Series
    train_mask: np.ndarray
    val_mask: np.ndarray
    test_mask: np.ndarray
    processor: Callable[[pd.DataFrame, pd.Series], tuple[pd.DataFrame, pd.Series]] | None
    name: str
    task_type: Literal["classification", "regression"]

    # Cache for DMatrix objects
    _dtrain: xgb.DMatrix | None = field(default=None, repr=False)
    _dval: xgb.DMatrix | None = field(default=None, repr=False)
    _dtest: xgb.DMatrix | None = field(default=None, repr=False)

    def _get_split_data(
        self, mask: np.ndarray
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Get data for a split, applying processor if present."""
        X_split, y_split = _apply_mask(self.X, self.y, mask)
        if self.processor is not None:
            X_split, y_split = self.processor(X_split, y_split)
        return X_split, y_split

    @property
    def dtrain(self) -> xgb.DMatrix:
        """DMatrix for training data (lazily created)."""
        if self._dtrain is None:
            X_train, y_train = self._get_split_data(self.train_mask)
            self._dtrain = xgb.DMatrix(X_train, label=y_train)
        return self._dtrain

    @property
    def dval(self) -> xgb.DMatrix:
        """DMatrix for validation data (lazily created)."""
        if self._dval is None:
            X_val, y_val = self._get_split_data(self.val_mask)
            self._dval = xgb.DMatrix(X_val, label=y_val)
        return self._dval

    @property
    def dtest(self) -> xgb.DMatrix:
        """DMatrix for test data (lazily created)."""
        if self._dtest is None:
            X_test, y_test = self._get_split_data(self.test_mask)
            self._dtest = xgb.DMatrix(X_test, label=y_test)
        return self._dtest

    @property
    def n_samples(self) -> int:
        """Total number of samples."""
        return len(self.X)

    @property
    def n_features(self) -> int:
        """Number of features."""
        return self.X.shape[1]

    @property
    def n_train(self) -> int:
        """Number of training samples."""
        return self.train_mask.sum()

    @property
    def n_val(self) -> int:
        """Number of validation samples."""
        return self.val_mask.sum()

    @property
    def n_test(self) -> int:
        """Number of test samples."""
        return self.test_mask.sum()

    def summary(self) -> str:
        """Return a summary string of the dataset."""
        return (
            f"{self.name} ({self.task_type})\n"
            f"  Samples: {self.n_samples} (train={self.n_train}, "
            f"val={self.n_val}, test={self.n_test})\n"
            f"  Features: {self.n_features}"
        )


# =============================================================================
# Child Dataclasses
# =============================================================================


@dataclass
class IrisDataset(XGBDataset):
    """Iris dataset - 3-class classification."""

    name: str = "iris"
    task_type: Literal["classification", "regression"] = "classification"


@dataclass
class WineDataset(XGBDataset):
    """Wine dataset - 3-class classification."""

    name: str = "wine"
    task_type: Literal["classification", "regression"] = "classification"


@dataclass
class BreastCancerDataset(XGBDataset):
    """Breast Cancer Wisconsin dataset - binary classification."""

    name: str = "breast_cancer"
    task_type: Literal["classification", "regression"] = "classification"


@dataclass
class DigitsDataset(XGBDataset):
    """Digits dataset - 10-class classification."""

    name: str = "digits"
    task_type: Literal["classification", "regression"] = "classification"


@dataclass
class DiabetesDataset(XGBDataset):
    """Diabetes dataset - regression."""

    name: str = "diabetes"
    task_type: Literal["classification", "regression"] = "regression"


@dataclass
class LinnerudDataset(XGBDataset):
    """Linnerud dataset - regression (first target only)."""

    name: str = "linnerud"
    task_type: Literal["classification", "regression"] = "regression"


# =============================================================================
# Factory Function
# =============================================================================

DATASET_CLASSES = {
    "iris": IrisDataset,
    "wine": WineDataset,
    "breast_cancer": BreastCancerDataset,
    "digits": DigitsDataset,
    "diabetes": DiabetesDataset,
    "linnerud": LinnerudDataset,
}


def get_dataset(
    name: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    processor: Callable[[pd.DataFrame, pd.Series], tuple[pd.DataFrame, pd.Series]]
    | None = None,
    random_state: int = 42,
) -> XGBDataset:
    """Factory function to get a prepared dataset by name.

    Args:
        name: Dataset name (iris, wine, breast_cancer, digits, diabetes, linnerud)
        train_ratio: Proportion for training set (default 0.7)
        val_ratio: Proportion for validation set (default 0.15)
        test_ratio: Proportion for test set (default 0.15)
        processor: Optional callable to transform (X, y) before DMatrix creation
        random_state: Random seed for reproducibility (default 42)

    Returns:
        XGBDataset instance with data loaded and splits created

    Example:
        >>> ds = get_dataset("iris")
        >>> print(ds.summary())
        >>> model = xgb.train(params, ds.dtrain, evals=[(ds.dval, "val")])
    """
    X, y, task_type = _load_sklearn_data(name)

    # Auto-detect stratification based on task type
    stratify = task_type == "classification"

    train_mask, val_mask, test_mask = _create_split_masks(
        n_samples=len(X),
        y=y,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        stratify=stratify,
        random_state=random_state,
    )

    dataset_class = DATASET_CLASSES[name]

    return dataset_class(
        X=X,
        y=y,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        processor=processor,
    )
