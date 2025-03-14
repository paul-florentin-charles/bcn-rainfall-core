from pydantic import BaseModel, Field


class DataSettings(BaseModel):
    """Type definition for data settings."""

    file_url: str | None = Field(None)
    local_file_path: str | None = Field(None)
    start_year: int
    rainfall_precision: int = Field(1)
