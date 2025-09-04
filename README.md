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
| `-f FORMAT`    | Force file format (csv, tsv, excel, parquet, feather)   |
| `-d DELIM`     | Set delimiter for CSV/TSV files (e.g., `,` or `\t`)      |
| `-xs N`        | Select Excel sheet N (1-based indexing)                  |
| `-xr N`        | Skip first N rows in Excel files                        |
| `-H N`         | Show first N rows                                        |
| `-T N`         | Show last N rows                                         |
| `-R START END` | Show rows in range START to END (zero-based, END excl.)  |
| `-L EXPR`      | Perform df.loc[expression] for flexible row/column selection |
| `-I EXPR`      | Perform df.iloc[expression] for position-based selection |
| `-u COL`       | Show unique values for column COL                        |
| `-c COL`       | Show info about column COL (type, nulls, etc.)           |
| `-v COL`       | Show value counts for column COL                         |
| `-s COL`       | Show stats for numerical column COL                      |
| `-l`           | List column names                                        |
| `-i`           | Show file info (rows, columns, memory usage)             |

All options can be chained in any order.

## Examples

### Basic Operations
Show first 10 rows:
```powershell
dfpeek data.feather -H 10
```

Show last 5 rows:
```powershell
dfpeek data.feather -T 5
```

Show rows 20 to 30:
```powershell
dfpeek data.feather -R 20 30
```

### Column Analysis
Show unique values for column `city`:
```powershell
dfpeek data.feather -u city
```

Show info about column `city`:
```powershell
dfpeek data.feather -c city
```

Show value counts for column `status`:
```powershell
dfpeek data.feather -v status
```

Show stats for column `age`:
```powershell
dfpeek data.feather -s age
```

### File Information
List columns:
```powershell
dfpeek data.feather -l
```

Show file info:
```powershell
dfpeek data.feather -i
```

### Advanced Indexing
Use loc for label-based selection:
```powershell
# Rows only
dfpeek data.feather -L "0:5"                        # First 5 rows
dfpeek data.feather -L "df.age > 30"                # Rows where age > 30

# Columns only  
dfpeek data.feather -L ":, 'name'"                  # All rows, name column
dfpeek data.feather -L ":, ['name', 'age']"         # All rows, name and age columns

# Both rows and columns
dfpeek data.feather -L "0:5, 'name':'city'"         # First 5 rows, name to city columns
dfpeek data.feather -L "df.age > 25, ['name', 'status']"  # Age > 25, name and status columns
```

Use iloc for position-based selection:
```powershell
# Rows only
dfpeek data.feather -I "0:5"                        # First 5 rows
dfpeek data.feather -I "[0,2,4]"                    # Rows at positions 0, 2, 4

# Columns only
dfpeek data.feather -I ":, 0"                       # All rows, first column
dfpeek data.feather -I ":, [0,2]"                   # All rows, columns 0 and 2

# Both rows and columns  
dfpeek data.feather -I "0:5, 0:3"                   # First 5 rows, first 3 columns
dfpeek data.feather -I "[0,2,4], [1,3]"            # Specific rows and columns
```

### Format and Delimiter Options
Force CSV format for files without .csv extension:
```powershell
dfpeek mydata.txt -f csv
```

Use custom delimiter:
```powershell
dfpeek data.tsv -d "\t" -H 5
```

### Default Behavior
Show info and first 5 rows (default if no options):
```powershell
dfpeek data.feather
```

Use a specific Excel sheet (e.g., the 3rd sheet):
```powershell
dfpeek data.xlsx -xs 3 -h 10
```

Skip the first 2 rows of an excel file:
```powershell
dfpeek data.xlsx -xr 2 
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
