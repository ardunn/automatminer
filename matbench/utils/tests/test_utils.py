import unittest

import pandas as pd
from sklearn.exceptions import NotFittedError

from matbench.utils.utils import initialize_logger, initialize_null_logger, \
    is_greater_better, compare_columns, regression_or_classification, \
    check_fitted, set_fitted
from matbench.base import DataframeTransformer


class MyTransformer(DataframeTransformer):
    def __init__(self):
        self.is_fit = False

    @set_fitted
    def fit(self, df, target):
        return df

    @check_fitted
    def transform(self, df, target):
        return df


class TestUtils(unittest.TestCase):

    def test_logger_initialization(self):
        log = initialize_logger()
        log.info("Test logging.")
        log.debug("Test debug.")
        log.warning("Test warning.")

        null = initialize_null_logger()
        null.info("Test null log 1.")
        null.debug("Test null log 2.")
        null.warning("Test null log 3.")

    def test_is_greater_better(self):
        self.assertTrue(is_greater_better('accuracy'))
        self.assertTrue(is_greater_better('r2'))
        self.assertTrue(is_greater_better('neg_mean_squared_error'))
        self.assertFalse(is_greater_better('mean_squared_error'))

    def test_compare_columns(self):
        df1 = pd.DataFrame({"a": [1, 2], "b": [2, 3]})
        df2 = pd.DataFrame({"b": [3, 4], "c": [4, 5]})
        comparison = compare_columns(df1, df2)
        self.assertTrue(comparison["mismatch"])
        self.assertListEqual(comparison["df1_not_in_df2"], ["a"])
        self.assertListEqual(comparison["df2_not_in_df1"], ["c"])

        comparison2 = compare_columns(df1, df1)
        self.assertFalse(comparison2["mismatch"])

        comparison3 = compare_columns(df1, df2, ignore=["c"])
        self.assertTrue(comparison3["mismatch"])
        self.assertListEqual(comparison3["df1_not_in_df2"], ["a"])
        self.assertListEqual(comparison3["df2_not_in_df1"], [])

    def test_regression_or_classification(self):
        s = pd.Series(data=["4", "5", "6"])
        self.assertTrue(regression_or_classification(s) == "regression")

        s = pd.Series(data=[1, 2, 3])
        self.assertTrue(regression_or_classification(s) == "regression")

        s = pd.Series(data=["a", "b", "c"])
        self.assertTrue(regression_or_classification(s) == "classification")

        s = pd.Series(data=["a1", "b", "c"])
        self.assertTrue(regression_or_classification(s) == "classification")

    def test_fitting_decorations(self):
        df = pd.DataFrame({"a": [1, 2], "b": [2, 3]})
        mt = MyTransformer()

        self.assertFalse(mt.is_fit)
        mt.fit(df, "")
        self.assertTrue(mt.is_fit)
        df = mt.transform(df, "")

        mt2 = MyTransformer()
        self.assertRaises(NotFittedError, mt2.transform, [df, ""])


if __name__ == "__main__":
    unittest.main()
