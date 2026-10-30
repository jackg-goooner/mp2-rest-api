def test_upload_csv(client, sample_csv_bytes):
    response = client.post(
        "/upload",
        files={"file": ("sample_data.csv", sample_csv_bytes, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["rows"] == 6
    assert payload["columns"] == 2
    assert isinstance(payload["id"], int) and payload["id"] > 0


def test_process_and_retrieve(client, uploaded_dataset_id, processing_body):
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body,
    )

    assert response.status_code == 200
    report = response.json()
    assert report["validation_rows_removed"] == 1
    assert report["cleaning_report"]["rows_before"] == 5
    assert report["cleaning_report"]["rows_after"] == 3

    retrieved = client.get(f"/datasets/{uploaded_dataset_id}")
    assert retrieved.status_code == 200
    payload = retrieved.json()
    assert payload["total_rows"] == 3
    assert payload["data"] == [
        {"student_id": 1, "score": 80.0},
        {"student_id": 2, "score": 90.0},
        {"student_id": 5, "score": 85.0},
    ]


def test_retrieve_missing_dataset(client):
    response = client.get("/datasets/999")
    assert response.status_code == 404


def test_failed_processing_does_not_update_dataset(
    client, uploaded_dataset_id, processing_body
):
    processing_body["validation"]["required_columns"] = ["missing_column"]
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body,
    )

    assert response.status_code == 400
    retrieved = client.get(f"/datasets/{uploaded_dataset_id}")
    assert retrieved.status_code == 200
    assert retrieved.json()["total_rows"] == 6


def test_responses_include_request_ids(client):
    first = client.get("/health")
    second = client.get("/datasets/999")

    first_id = first.headers["X-Request-ID"]
    second_id = second.headers["X-Request-ID"]
    assert len(first_id) == 8
    assert len(second_id) == 8
    assert first_id != second_id
