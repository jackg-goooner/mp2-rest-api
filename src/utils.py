"""Shared logging helpers."""

import logging


def setup_logging(verbose=False):
    """Configure console logging with the MP1 logging format."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )
