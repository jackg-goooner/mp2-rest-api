# MP2 REST API

This FastAPI application uploads CSV datasets, reports dataset metadata, retrieves stored rows, and validates and cleans datasets with reusable modules from MP1. The processing endpoint supports configurable required and numeric column validation, duplicate and missing-value handling, and outlier removal. Request middleware logs each request with a unique request ID, status, and duration, and returns the ID in the `X-Request-ID` response header.

Run the API from this directory with `uvicorn main:app --reload`, then open `/docs` to explore the endpoints. Install dependencies with `python -m pip install -r requirements.txt`. Run the API tests with `python -m pytest tests -v`.
