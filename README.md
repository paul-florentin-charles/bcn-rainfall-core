# bcn-rainfall-core

[![PyPI version](https://badge.fury.io/py/bcn-rainfall-core.svg)](https://badge.fury.io/py/bcn-rainfall-core)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Tools to load and manipulate rainfall data from the city of Barcelona, Catalunya; it is the core of the Barcelona Rainfall project and is exposed through the Barcelona Rainfall API.

## Requirements

- Python 3.12
- Pip

## Usage

```python
from bcn_rainfall_core import Rainfall
from bcn_rainfall_core.utils import DataSettings

# With configuration file in default path `config.yml`
rainfall = Rainfall.from_config()

# With configuration file in other path
rainfall_with_path = Rainfall.from_config(path="new/path/to/config.yml")

# With your own configuration
rainfall_with_cfg = Rainfall.from_config(
    cfg=DataSettings(file_url="http://...", start_year=1955, rainfall_precision=2)
)

# With your own configuration from local file
rainfall_with_cfg_from_file = Rainfall.from_config(
    cfg=DataSettings(local_file_path="/dir/my_rainfall_data.csv", start_year=1955, rainfall_precision=2),
    from_file=True,
)


# Have fun with class!
from bcn_rainfall_core.utils import TimeMode, Season

rainfall_avg = rainfall.get_rainfall_average(
    TimeMode.SEASONAL,
    begin_year=1975, 
    end_year=1998, 
    season=Season.WINTER
)
print(rainfall_avg)
...
```

## Tests & Coverage

```commandline
uv run coverage run -m pytest
uv run coverage report
```

## Code quality

```commandline
uv tool run mypy --check-untyped-defs .
uv tool run ruff check
uv tool run ruff format
```