"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from functools import cached_property
from typing import Optional

from bcn_rainfall_core.utils import BaseConfig, DataSettings


class Config(BaseConfig):
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["Config"] = None

    def __new__(cls, *, path: str):
        return super().__new__(cls, path=path)

    @cached_property
    def get_data_settings(self) -> DataSettings:
        """
        Return data settings to load and manipulate bcn_rainfall_core data.

        Example:
        {
            "file_url": "https://opendata-ajuntament.barcelona.cat/data/dataset/5334c15e-0d70-410b-85f3-d97740ffc1ed/resource/6f1fb778-0767-478b-b332-c64a833d26d2/download/precipitacionsbarcelonadesde1786.csv",
            "local_file_path": "resources/bcn_rainfall_1786_2024.csv",
            "start_year": 1971,
            "rainfall_precision": 1,
        }
        """
        return DataSettings(**self.yaml_config["data"])
