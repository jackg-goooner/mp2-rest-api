"""Shared command-line helpers for the data pipeline."""

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure console logging for the pipeline."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def validate_input(filepath):
    """Return whether filepath exists and refers to a file, logging the result."""
    path = Path(filepath)
    if not path.is_file():
        logger.error("Input file not found: %s", filepath)
        return False

    logger.info("Input file validated: %s", filepath)
    return True
