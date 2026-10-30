import logging

import pandas as pd


logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Return ``df`` without duplicate rows."""
    result = df.drop_duplicates()
    logger.debug("remove_duplicates: %s → %s rows", len(df), len(result))
    return result


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis not in {"rows", "columns"}:
        logger.error("Unsupported missing-value axis: %s", axis)
        raise ValueError(f"Unsupported missing-value axis: {axis}")

    result = df.dropna(axis=0 if axis == "rows" else 1)
    removed = len(df) - len(result) if axis == "rows" else len(df.columns) - len(result.columns)
    logger.debug("handle_missing (%s): removed %s", axis, removed)
    return result


def remove_outliers(df, columns, method, threshold):
    """Remove rows with outliers in configured numeric columns."""
    if method not in {"iqr", "zscore"}:
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    result = df.copy()
    for column in columns:
        if column not in result.columns:
            logger.warning("Column not found: %s", column)
            continue
        if not pd.api.types.is_numeric_dtype(result[column]):
            logger.warning("Column is not numeric: %s", column)
            continue

        values = result[column]
        if method == "iqr":
            q1, q3 = values.quantile([0.25, 0.75])
            spread = q3 - q1
            lower = q1 - threshold * spread
            upper = q3 + threshold * spread
            keep = values.between(lower, upper)
        else:
            mean = values.mean()
            standard_deviation = values.std(ddof=0)
            if standard_deviation == 0 or pd.isna(standard_deviation):
                keep = pd.Series(True, index=values.index)
            else:
                zscores = (values - mean).abs() / standard_deviation
                keep = zscores <= threshold
            lower = mean - threshold * standard_deviation
            upper = mean + threshold * standard_deviation

        # Outlier handling should not implicitly change the missing-value policy.
        keep = keep | values.isna()
        before = len(result)
        result = result.loc[keep]
        logger.debug("%s: lower=%s, upper=%s, removed=%s", column, lower, upper, before - len(result))

    return result


def process_data(df, config):
    """Apply enabled cleaning steps in the configured order."""
    processing = config["processing"]
    result = df

    if processing.get("remove_duplicates", False):
        result = remove_duplicates(result)

    missing = processing.get("missing", {})
    if missing.get("enabled", False):
        result = handle_missing(result, axis=missing["axis"])

    outliers = processing.get("outliers", {})
    if outliers.get("enabled", False):
        result = remove_outliers(
            result,
            columns=outliers["columns"],
            method=outliers["method"],
            threshold=outliers["threshold"],
        )

    return result


def create_cleaning_report(df_before, df_after):
    """Summarize row and column counts before and after cleaning."""
    rows_before, rows_after = len(df_before), len(df_after)
    columns_before, columns_after = len(df_before.columns), len(df_after.columns)
    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_before - rows_after,
        "columns_before": columns_before,
        "columns_after": columns_after,
        "columns_removed": columns_before - columns_after,
    }
