# from __future__ import annotations

# import os
# from dataclasses import dataclass
# from pathlib import Path

# from dotenv import load_dotenv

# BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv(
#     BASE_DIR / ".env",
#     override=False,
# )


# @dataclass(frozen=True)
# class Settings:
#     google_service_account_file: Path
#     bookmarking_sheet_id: str
#     bookmarking_sheet_name: str

#     groq_api_key: str
#     groq_model: str

#     web_agent_token: str


# def get_settings() -> Settings:
#     return Settings(
#         google_service_account_file=(
#             BASE_DIR / os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"]
#         ),
#         bookmarking_sheet_id=os.environ["BookmarkingSitesSheetId"],
#         bookmarking_sheet_name=os.getenv(
#             "BookmarkingSitesSheetName",
#             "BookmarkingSites",
#         ),
#         groq_api_key=os.environ["GROQ_API_KEY"],
#         groq_model=os.getenv(
#             "GROQ_MODEL",
#             "llama-3.3-70b-versatile",
#         ),
#         web_agent_token=os.environ["WEBAGENT_API_TOKEN"],
#     )


# settings = get_settings()
import base64
import json
from typing import Any, Dict

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_service_base64: str = Field(..., alias="GOOGLE_CREDENTIALS_BASE64")

    bookmarking_sheet_id: str = Field(..., alias="BookmarkingSitesSheetId")
    bookmarking_sheet_name: str = Field(
        default="BookmarkingSites",
        alias="BookmarkingSitesSheetName",
    )

    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    groq_model: str = Field(alias="GROQ_MODEL", default="llama-3.3-70b-versatile")
    web_agent_token: str = Field(..., alias="WEBAGENT_API_TOKEN")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @field_validator("google_service_base64", mode="after")
    @classmethod
    def validate_json_structure(cls, raw_json: str) -> str:
        try:
            parsed_json = json.loads(raw_json)
            if not isinstance(parsed_json, dict):
                raise TypeError("The provided JSON is not a valid dictionary.")
            if "type" not in parsed_json:
                raise ValueError("Missing 'type' key in Google Service Account JSON.")
        except json.JSONDecodeError:
            raise ValueError("The provided string is not valid JSON.")
        return raw_json

    # property
    @property
    def google_service_account_file_path(self) -> Dict[str, Any]:
        decoded_bytes = base64.b64decode(self.google_credentials_base64)
        return json.loads(decoded_bytes.decode("utf-8"))


settings = Settings()
