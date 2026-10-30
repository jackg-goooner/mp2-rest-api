import logging

import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate required columns and remove rows with invalid numeric values."""
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        message = f"Missing required columns: {', '.join(missing_columns)}"
        logger.error(message)
        raise ValueError(message)

    result = df.copy()
    rows_before = len(result)
    for column in numeric_columns:
        if column not in result.columns:
            message = f"Numeric column is missing: {column}"
            logger.error(message)
            raise ValueError(message)

        invalid_positions = set()
        for position, value in enumerate(result[column].tolist()):
            if pd.notna(value):
                try:
                    float(value)
                except (TypeError, ValueError):
                    invalid_positions.add(position)

        if invalid_positions:
            logger.warning(
                "Removed %s rows with invalid numeric values in %s",
                len(invalid_positions),
                column,
            )
            keep = [position not in invalid_positions for position in range(len(result))]
            result = result.iloc[keep].copy()

        result[column] = pd.to_numeric(result[column])

    logger.debug("Validation: %s -> %s rows", rows_before, len(result))
    return result
