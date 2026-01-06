import numpy as np
import pandas as pd
import pytest
import xgboost as xgb

from xgb_utils.get_data import (
    DATASET_CLASSES,
    XGBDataset,
    _apply_mask,
    _create_split_masks,
    _load_sklearn_data,
    get_dataset,
)


# =============================================================================
# Test Helper Functions
# =============================================================================


class TestLoadSklearnData:
    """Tests for _load_sklearn_data helper."""

    @pytest.mark.parametrize(
        "name,expected_task",
        [
            ("iris", "classification"),
            ("wine", "classification"),
            ("breast_cancer", "classification"),
            ("digits", "classification"),
            ("diabetes", "regression"),
            ("linnerud", "regression"),
        ],
    )
    def test_load_all_datasets(self, name: str, expected_task: str):
        """Each dataset loads and returns correct task type."""
        X, y, task_type = _load_sklearn_data(name)

        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert task_type == expected_task
        assert len(X) == len(y)
        assert len(X) > 0

    def test_invalid_dataset_raises(self):
        """Unknown dataset name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown dataset"):
            _load_sklearn_data("not_a_dataset")

    def test_feature_names_preserved(self):
        """Feature names from sklearn are preserved as column names."""
        X, _, _ = _load_sklearn_data("iris")
        assert "sepal length (cm)" in X.columns


class TestCreateSplitMasks:
    """Tests for _create_split_masks helper."""

    def test_masks_are_mutually_exclusive(self):
        """No sample should be in multiple splits."""
        y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1, 2, 2])
        train, val, test = _create_split_masks(
            n_samples=10,
            y=y,
            train_ratio=0.6,
            val_ratio=0.2,
            test_ratio=0.2,
            stratify=True,
            random_state=42,
        )

        # No overlap between masks
        assert not np.any(train & val)
        assert not np.any(train & test)
        assert not np.any(val & test)

    def test_masks_cover_all_samples(self):
        """Every sample should be in exactly one split."""
        y = pd.Series(range(100))
        train, val, test = _create_split_masks(
            n_samples=100,
            y=y,
            train_ratio=0.7,
            val_ratio=0.15,
            test_ratio=0.15,
            stratify=False,
            random_state=42,
        )

        combined = train | val | test
        assert combined.all()

    def test_split_ratios_respected(self):
        """Split sizes should match requested ratios."""
        n = 1000
        y = pd.Series(range(n))
        train, val, test = _create_split_masks(
            n_samples=n,
            y=y,
            train_ratio=0.7,
            val_ratio=0.2,
            test_ratio=0.1,
            stratify=False,
            random_state=42,
        )

        assert train.sum() == 700
        assert val.sum() == 200
        assert test.sum() == 100

    def test_stratification_preserves_proportions(self):
        """Stratified split should maintain class proportions."""
        # Create imbalanced dataset: 80% class 0, 20% class 1
        y = pd.Series([0] * 80 + [1] * 20)

        train, val, test = _create_split_masks(
            n_samples=100,
            y=y,
            train_ratio=0.7,
            val_ratio=0.15,
            test_ratio=0.15,
            stratify=True,
            random_state=42,
        )

        # Check proportions in training set
        train_y = y[train]
        train_prop = (train_y == 0).sum() / len(train_y)
        assert 0.75 <= train_prop <= 0.85  # Should be ~0.80

    def test_invalid_ratios_raise(self):
        """Ratios not summing to 1.0 should raise."""
        y = pd.Series(range(10))
        with pytest.raises(ValueError, match="must sum to 1.0"):
            _create_split_masks(
                n_samples=10,
                y=y,
                train_ratio=0.5,
                val_ratio=0.3,
                test_ratio=0.3,  # Sum = 1.1
                stratify=False,
                random_state=42,
            )

    def test_reproducibility(self):
        """Same random_state should produce same masks."""
        y = pd.Series(range(100))
        masks1 = _create_split_masks(100, y, 0.7, 0.15, 0.15, False, 42)
        masks2 = _create_split_masks(100, y, 0.7, 0.15, 0.15, False, 42)

        for m1, m2 in zip(masks1, masks2):
            assert np.array_equal(m1, m2)


class TestApplyMask:
    """Tests for _apply_mask helper."""

    def test_mask_filters_correctly(self):
        """Mask should select only True indices."""
        X = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
        y = pd.Series([10, 20, 30, 40, 50])
        mask = np.array([True, False, True, False, True])

        X_filtered, y_filtered = _apply_mask(X, y, mask)

        assert len(X_filtered) == 3
        assert list(X_filtered["a"]) == [1, 3, 5]
        assert list(y_filtered) == [10, 30, 50]

    def test_index_reset(self):
        """Filtered data should have reset index."""
        X = pd.DataFrame({"a": range(10)})
        y = pd.Series(range(10))
        mask = np.array([False, True, False, True, False, True, False, True, False, True])

        X_filtered, y_filtered = _apply_mask(X, y, mask)

        assert list(X_filtered.index) == [0, 1, 2, 3, 4]
        assert list(y_filtered.index) == [0, 1, 2, 3, 4]


# =============================================================================
# Test XGBDataset Class
# =============================================================================


class TestXGBDataset:
    """Tests for XGBDataset dataclass."""

    @pytest.fixture
    def sample_dataset(self) -> XGBDataset:
        """Create a simple dataset for testing."""
        return get_dataset("iris", random_state=42)

    def test_dmatrix_creation(self, sample_dataset: XGBDataset):
        """DMatrix objects should be created lazily."""
        ds = sample_dataset

        # DMatrix not created yet
        assert ds._dtrain is None

        # Access triggers creation
        dtrain = ds.dtrain
        assert isinstance(dtrain, xgb.DMatrix)
        assert ds._dtrain is dtrain  # Cached

    def test_dmatrix_sizes(self, sample_dataset: XGBDataset):
        """DMatrix should have correct number of rows."""
        ds = sample_dataset

        assert ds.dtrain.num_row() == ds.n_train
        assert ds.dval.num_row() == ds.n_val
        assert ds.dtest.num_row() == ds.n_test

    def test_sample_counts(self, sample_dataset: XGBDataset):
        """Sample count properties should be accurate."""
        ds = sample_dataset

        assert ds.n_samples == ds.n_train + ds.n_val + ds.n_test
        assert ds.n_train == ds.train_mask.sum()
        assert ds.n_val == ds.val_mask.sum()
        assert ds.n_test == ds.test_mask.sum()

    def test_summary(self, sample_dataset: XGBDataset):
        """Summary should include key information."""
        summary = sample_dataset.summary()

        assert "iris" in summary
        assert "classification" in summary
        assert "train=" in summary
        assert "Features:" in summary


# =============================================================================
# Test Factory Function
# =============================================================================


class TestGetDataset:
    """Tests for get_dataset factory function."""

    @pytest.mark.parametrize("name", list(DATASET_CLASSES.keys()))
    def test_all_datasets_load(self, name: str):
        """Each dataset should load successfully via factory."""
        ds = get_dataset(name, random_state=42)

        assert isinstance(ds, XGBDataset)
        assert ds.name == name
        assert ds.n_samples > 0

    def test_correct_child_class_returned(self):
        """Factory should return the correct child class."""
        from xgb_utils.get_data import IrisDataset, DiabetesDataset

        iris = get_dataset("iris")
        diabetes = get_dataset("diabetes")

        assert type(iris) is IrisDataset
        assert type(diabetes) is DiabetesDataset

    def test_custom_split_ratios(self):
        """Custom split ratios should be applied."""
        ds = get_dataset(
            "iris",
            train_ratio=0.8,
            val_ratio=0.1,
            test_ratio=0.1,
            random_state=42,
        )

        total = ds.n_samples
        assert ds.n_train == int(total * 0.8)

    def test_processor_applied(self):
        """Processor callable should be applied to splits."""

        def double_features(X: pd.DataFrame, y: pd.Series):
            return X * 2, y

        ds = get_dataset("iris", processor=double_features, random_state=42)

        # Get raw data for comparison
        ds_raw = get_dataset("iris", random_state=42)

        # Check that processor was applied (values should be doubled)
        X_train_raw, _ = _apply_mask(ds_raw.X, ds_raw.y, ds_raw.train_mask)
        X_train_processed, _ = ds._get_split_data(ds.train_mask)

        assert np.allclose(X_train_processed.values, X_train_raw.values * 2)

    def test_invalid_dataset_raises(self):
        """Unknown dataset name should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown dataset"):
            get_dataset("not_a_real_dataset")

    def test_classification_is_stratified(self):
        """Classification datasets should have stratified splits."""
        ds = get_dataset("breast_cancer", random_state=42)

        # Get class proportions in full dataset
        full_prop = (ds.y == 0).sum() / len(ds.y)

        # Get class proportions in training set
        train_y = ds.y[ds.train_mask]
        train_prop = (train_y == 0).sum() / len(train_y)

        # Proportions should be similar (within 5%)
        assert abs(full_prop - train_prop) < 0.05


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """End-to-end integration tests."""

    def test_xgboost_training(self):
        """Dataset should work with xgboost.train()."""
        ds = get_dataset("iris", random_state=42)

        params = {
            "objective": "multi:softmax",
            "num_class": 3,
            "max_depth": 3,
            "eta": 0.1,
            "seed": 42,
        }

        model = xgb.train(
            params,
            ds.dtrain,
            num_boost_round=10,
            evals=[(ds.dval, "val")],
            verbose_eval=False,
        )

        # Model should be able to predict
        preds = model.predict(ds.dtest)
        assert len(preds) == ds.n_test
        assert all(p in [0, 1, 2] for p in preds)

    def test_regression_training(self):
        """Regression dataset should work with xgboost."""
        ds = get_dataset("diabetes", random_state=42)

        params = {
            "objective": "reg:squarederror",
            "max_depth": 3,
            "eta": 0.1,
            "seed": 42,
        }

        model = xgb.train(
            params,
            ds.dtrain,
            num_boost_round=10,
            evals=[(ds.dval, "val")],
            verbose_eval=False,
        )

        preds = model.predict(ds.dtest)
        assert len(preds) == ds.n_test
        assert all(isinstance(p, (float, np.floating)) for p in preds)
