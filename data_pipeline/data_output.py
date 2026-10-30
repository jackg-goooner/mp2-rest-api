import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_data(df, filepath):
    """Save a DataFrame as a CSV file and return its path."""
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.debug("Saved %s rows to %s", len(df), output_path)
    return output_path
