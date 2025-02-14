from pytest import fixture, raises
from yaml.parser import ParserError  # type: ignore

from bcn_rainfall_core.config import Config

CONFIG = Config(path="config.yml")


@fixture(autouse=True)
def reset_config():
    Config._instance = None

    yield


class TestConfig:
    @staticmethod
    def test_config_file_not_found():
        with raises(FileNotFoundError):
            Config(path="/there/is/no/config/file/there/dude.yaml")

    @staticmethod
    def test_config_file_invalid():
        with raises(ParserError):
            Config(path="README.md")

    @staticmethod
    def test_get_data_settings():
        data_settings = CONFIG.get_data_settings

        assert isinstance(data_settings.file_url, str)

        if data_settings.local_file_path is not None:
            assert isinstance(data_settings.local_file_path, str)

        assert isinstance(data_settings.start_year, int)
        assert isinstance(data_settings.rainfall_precision, int)
