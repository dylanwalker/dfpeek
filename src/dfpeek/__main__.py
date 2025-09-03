
import pandas as pd
import argparse
import sys

def load_df(path, delimiter=None, excel_sheet=None, excel_skiprows=None):
    if path.endswith('.feather'):
        return pd.read_feather(path)
    elif path.endswith('.csv'):
        return pd.read_csv(path, delimiter=delimiter)
    elif path.endswith('.tsv'):
        return pd.read_csv(path, delimiter='\t')
    elif path.endswith('.parquet'):
        return pd.read_parquet(path)
    elif path.endswith('.xlsx'):
        sheet = excel_sheet - 1 if excel_sheet is not None else 0  # Convert 1-based to 0-based indexing
        return pd.read_excel(path, sheet_name=sheet, skiprows=excel_skiprows)
    else:
        print("Unsupported file format.")
        sys.exit(1)


def print_head(df, n):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df.head(n))
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')

def print_tail(df, n):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df.tail(n))
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')

def print_range(df, start, end):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df.iloc[start:end])
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')

def print_unique(df, col):
    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return
    print(df[col].unique())


def print_colinfo(df, col):
    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return
    print(f"Column: {col}")
    print(f"Type: {df[col].dtype}")
    print(f"Nulls: {df[col].isnull().sum()} / {len(df)}")
    print(f"Unique: {df[col].nunique()}")
    print(f"Sample: {df[col].head(5).tolist()}")

def print_value_counts(df, col):
    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return
    print(df[col].value_counts())

def print_stats(df, col):
    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return
    print(df[col].describe())

def print_columns(df):
    print(list(df.columns))

def print_info(df):
    df.info()


def main():
    parser = argparse.ArgumentParser(description='Peek at tabular data files easily.')
    parser.add_argument('datafile', type=str, help='Path to data file')
    parser.add_argument('-d', type=str, default=None, help='Delimiter for CSV/TSV')
    parser.add_argument('-xs', type=int, default=None, help='Excel sheet number (1-based)')
    parser.add_argument('-xr', type=int, default=None, help='Excel number of rows to skip')
    parser.add_argument('-H', type=int, default=None, help='Show first N rows')
    parser.add_argument('-T', type=int, default=None, help='Show last N rows')
    parser.add_argument('-R', nargs=2, type=int, default=None, metavar=('START', 'END'), help='Show rows in range START to END (zero-based, END exclusive)')
    parser.add_argument('-u', type=str, default=None, help='Show unique values for column')
    parser.add_argument('-c', type=str, default=None, help='Show info about column')
    parser.add_argument('-v', type=str, default=None, help='Show value counts for column')
    parser.add_argument('-s', type=str, default=None, help='Show stats for numerical column')
    parser.add_argument('-l', action='store_true', help='List columns')
    parser.add_argument('-i', action='store_true', help='Show file info')
    args = parser.parse_args()

    df = load_df(args.datafile, delimiter=args.d, excel_sheet=args.xs, excel_skiprows=args.xr)

    if args.i:
        print_info(df)
    if args.l:
        print_columns(df)
    if args.H:
        print_head(df, args.H)
    if args.T:
        print_tail(df, args.T)
    if args.R:
        print_range(df, args.R[0], args.R[1])
    if args.u:
        print_unique(df, args.u)
    if args.c:
        print_colinfo(df, args.c)
    if args.v:
        print_value_counts(df, args.v)
    if args.s:
        print_stats(df, args.s)
    # Default: show info and head if no options
    if not any([args.i, args.l, args.H, args.T, args.R, args.u, args.c, args.v, args.s]):
        print_info(df)
        print_head(df, 5)

if __name__ == "__main__":
    main()
