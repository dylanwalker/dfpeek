# dfpeek

A fast command-line tool for peeking at tabular data files (CSV, TSV, Parquet, Feather, Excel) with concise, chainable options inspired by Unix tools like `ls`.

## Installation

Install from PyPI (recommended):

```powershell
pip install dfpeek
```

Or, for Excel/Parquet support:

```powershell
pip install dfpeek[excel,parquet]
```

## Usage

Run from the command line:

```powershell
dfpeek <datafile> [options]
```

## Options

| Option         | Description                                              |
|----------------|---------------------------------------------------------|
| `-h N`         | Show first N rows                                        |
| `-t N`         | Show last N rows                                         |
| `-r START END` | Show rows in range START to END (zero-based, END excl.)  |
| `-u COL`       | Show unique values for column COL                        |
| `-c COL`       | Show info about column COL (type, nulls, etc.)           |
| `-v COL`       | Show value counts for column COL                         |
| `-s COL`       | Show stats for numerical column COL                      |
| `-l`           | List column names                                        |
| `-i`           | Show file info (rows, columns, memory usage)             |
| `-d DELIM`     | Set delimiter for CSV/TSV files (e.g., `,` or `\t`)      |
| `-xs N`        | Select Excel sheet N (1-based indexing)                  |

All options can be chained in any order.

## Examples

Show first 10 rows:
```powershell
dfpeek data.csv -h 10
```

Show last 5 rows:
```powershell
dfpeek data.csv -t 5
```

Show rows 20 to 30:
```powershell
dfpeek data.csv -r 20 30
```

Show unique values for column `city`:
```powershell
dfpeek data.csv -u city
```

Show info about column `city`:
```powershell
dfpeek data.csv -c city
```

Show value counts for column `status`:
```powershell
dfpeek data.csv -v status
```

Show stats for column `age`:
```powershell
dfpeek data.csv -s age
```

List columns:
```powershell
dfpeek data.csv -l
```

Show file info:
```powershell
dfpeek data.csv -i
```

Show info and first 5 rows (default if no options):
```powershell
dfpeek data.csv
```

Use a custom delimiter (e.g., tab):
```powershell
dfpeek data.tsv -d "\t" -h 5
```

Use a specific Excel sheet (e.g., the 3rd sheet):
```powershell
dfpeek data.xlsx -xs 3 -h 10
```

## Supported Formats
- CSV (.csv)
- TSV (.tsv)
- Parquet (.parquet)
- Feather (.feather)
- Excel (.xlsx)

## Notes
- For very large files, output may be slow if printing many rows.
- All rows/columns are shown in full (no abbreviation).
- Requires Python 3.7+

## License
MIT
