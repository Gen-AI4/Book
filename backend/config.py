from pydantic_settings import BaseSettings as Settings
from pydantic import Field
from typing import Optional
import os


class Settings(Settings):
    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")

    # Qdrant settings
    qdrant_url: Optional[str] = Field(default="https://16b332a7-4011-462d-a698-10f2e3df8e6e.europe-west3-0.gcp.cloud.qdrant.io:6333", alias="QDRANT_HOST")  # Default local Qdrant instance
    qdrant_host: Optional[str] = Field(default="https://16b332a7-4011-462d-a698-10f2e3df8e6e.europe-west3-0.gcp.cloud.qdrant.io:6333", alias="QDRANT_HOST")  # For backward compatibility
    qdrant_api_key: Optional[str] = Field(default=None, alias="QDRANT_API_KEY")
    qdrant_collection_name: str = Field(default="textbook_content", alias="QDRANT_COLLECTION_NAME")

    # OpenAI settings
    openai_api_key: str = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", alias="OPENAI_MODEL")  # Default model, can be gpt-4o as well

    # Cohere settings
    cohere_api_key: str = Field(alias="COHERE_API_KEY")

    class Config:
        env_file = ".env"
        env_prefix = ""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


settings = Settings()