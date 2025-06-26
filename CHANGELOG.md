## Changelog

### v1.0.6
_26/06/2025_

- Customize pie chart percentages of normal via `percentages_of_normal` parameter.
- Shorten some figure labels and default margins.

### v1.0.5
_19/06/2025_

- Allow displaying of x-axis range slider for *Plotly* graphs.
- Add a new bar graphic depicting standard deviations of rainfall.
- Clean up some docstrings.
- Increase default `round_precision` value from 1 to 2 in `config.yml`.

### v1.0.4
_17/06/2025_

- Remove a lot of unused code, notably used to add/remove columns to `DataFrame`.
- Add function to compute and get K-Means directly for given time frame.
- Lighten `Label` enum class by removing unused attributes.
- Integrate display by K-Means clusters in rainfall bar graphic.

### v1.0.3
_14/03/2025_

- Various modifications of comments & type hints, nothing really crucial.
- Make `rainfall_precision` optional in `config.yml` and default to 1.

### v1.0.2
_14/02/2025_

- Reset dependencies version to working conditions to ensure compatibility.

### v1.0.1
_14/02/2025_

- Fix typo in many files
- Make some keywords compulsory

### v1.0.0 
_14/02/2025_

- Initial release.
- Code is taken from [this repository](https://github.com/paul-florentin-charles/bcn-rainfall-models).