"""
Provides custom Exceptions to be used within the project.
Raise them or catch them!
"""


class DataFormatError(Exception):
    """
    Customizable Exception for data that is not shaped as wished.
    """

    def __init__(self, data_format: str):
        self.data_format = data_format
        self.message = (
            f"Data given is incorrectly formatted. Should be: {self.data_format}"
        )

        super().__init__(self.message)
