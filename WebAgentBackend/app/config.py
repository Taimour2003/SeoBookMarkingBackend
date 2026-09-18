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
    def validate_json_structure(cls, raw_b64: str) -> str:
        try:
            decoded_bytes = base64.b64decode(raw_b64)
            parsed_json = json.loads(decoded_bytes.decode("utf-8"))
            if not isinstance(parsed_json, dict):
                raise TypeError("The provided JSON is not a valid dictionary.")
        except json.JSONDecodeError:
            raise ValueError("The provided string is not valid JSON.")
        return raw_b64

    # property
    @property
    def google_service_account_file_path(self) -> Dict[str, Any]:
        decoded_bytes = base64.b64decode(self.google_service_base64)
        return json.loads(decoded_bytes.decode("utf-8"))


settings = Settings()
