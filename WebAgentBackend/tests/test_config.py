import json

import pytest
from app.config import Settings
from pydantic import ValidationError


def test_validator_valid_json(monkeypatch):
    """Test karein ke valid JSON string bina kisi error ke pass ho jati hai."""
    valid_json = json.dumps({"type": "service_account", "project_id": "test-project"})

    monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_FILE", valid_json)
    monkeypatch.setenv("BookmarkingSitesSheetId", "dummy_id")
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    monkeypatch.setenv("WEBAGENT_API_TOKEN", "dummy_token")

    settings = Settings()
    assert settings.google_service_account_file == valid_json


def test_validator_invalid_json(monkeypatch):
    """Test karein ke agar string valid JSON na ho, toh custom ValueError aye."""
    monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_FILE", "plain-text-not-json")
    monkeypatch.setenv("BookmarkingSitesSheetId", "dummy_id")
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    monkeypatch.setenv("WEBAGENT_API_TOKEN", "dummy_token")

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    assert "The provided string is not valid JSON." in str(exc_info.value)


def test_validator_missing_type_key(monkeypatch):
    """Test karein ke agar JSON mein 'type' key missing ho, toh error raise ho."""
    invalid_json = json.dumps({"project_id": "no-type-field"})

    monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_FILE", invalid_json)
    monkeypatch.setenv("BookmarkingSitesSheetId", "dummy_id")
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    monkeypatch.setenv("WEBAGENT_API_TOKEN", "dummy_token")

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    assert "Missing 'type' key in Google Service Account JSON" in str(exc_info.value)
