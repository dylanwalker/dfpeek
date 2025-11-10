
import shutil
import pandas as pd
import argparse
import sys

def load_df(path, delimiter=None, excel_sheet=None, excel_skiprows=None, force_format=None):
    # Use forced format if specified, otherwise infer from extension
    if force_format:
        format_type = force_format.lower()
    elif path.endswith('.feather'):
        format_type = 'feather'
    elif path.endswith('.csv'):
        format_type = 'csv'
    elif path.endswith('.tsv'):
        format_type = 'tsv'
    elif path.endswith('.parquet'):
        format_type = 'parquet'
    elif path.endswith('.xlsx'):
        format_type = 'excel'
    else:
        print("Unsupported file format. Use -f to specify format explicitly.")
        sys.exit(1)
    
    # Load based on format type
    if format_type == 'feather':
        return pd.read_feather(path)
    elif format_type == 'csv':
        return pd.read_csv(path, delimiter=delimiter)
    elif format_type == 'tsv':
        return pd.read_csv(path, delimiter='\t')
    elif format_type == 'parquet':
        return pd.read_parquet(path)
    elif format_type in ['excel', 'xlsx']:
        sheet = excel_sheet - 1 if excel_sheet is not None else 0  # Convert 1-based to 0-based indexing
        return pd.read_excel(path, sheet_name=sheet, skiprows=excel_skiprows)
    else:
        print(f"Unsupported format: {format_type}. Supported: csv, tsv, excel, parquet, feather")
        sys.exit(1)


def print_head(df, n):
    print(df.head(n))


def print_tail(df, n):
    print(df.tail(n))

def print_range(df, start, end):
    print(df.iloc[start:end])

def apply_loc(df, locstring):
    """Apply df.loc[locstring] and return the subset"""
    try:
        namespace = {'df': df}
        code = f"df.loc[{locstring}]"
        return eval(code, {"__builtins__": {}}, namespace)
    except Exception as e:
        print(f"Error in loc expression '{locstring}': {e}")
        print("Examples:")
        print("  Rows: '0:5', 'df.age > 25', 'df.name == \"Alice\"'")
        print("  Columns: ':, \"name\"', ':, [\"name\", \"age\"]'")
        print("  Both: ':, \"name\":\"city\"', 'df.age > 25, [\"name\", \"status\"]'")
        sys.exit(1)

def apply_iloc(df, ilocstring):
    """Apply df.iloc[ilocstring] and return the subset"""
    try:
        if ':' in ilocstring and not ilocstring.startswith('[') and ',' not in ilocstring:
            parts = ilocstring.split(':')
            if len(parts) == 2:
                start = int(parts[0]) if parts[0] else None
                end = int(parts[1]) if parts[1] else None
                return df.iloc[start:end]
            else:
                return df.iloc[eval(ilocstring)]
        else:
            return df.iloc[eval(ilocstring)]
    except Exception as e:
        print(f"Error in iloc expression '{ilocstring}': {e}")
        print("Examples:")
        print("  Rows: '0:5', '[0,2,4]', '0:10:2'")
        print("  Columns: ':, 0', ':, [0,2]', ':, 0:3'")
        print("  Both: '0:5, 0:3', '[0,2,4], [1,3]'")
        sys.exit(1)

def print_loc(df, locstring):
    """Execute df.loc[locstring] safely"""
    subset = apply_loc(df, locstring)
    print(subset)

def print_iloc(df, ilocstring):
    """Execute df.iloc[ilocstring] safely"""
    subset = apply_iloc(df, ilocstring)
    print(subset)

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
    parser.add_argument('-f', type=str, default=None, help='Force file format (csv, tsv, excel, parquet, feather)')
    parser.add_argument('-d', type=str, default=None, help='Delimiter for CSV/TSV')
    parser.add_argument('-xs', type=int, default=None, help='Excel sheet number (1-based)')
    parser.add_argument('-xr', type=int, default=None, help='Excel number of rows to skip')
    parser.add_argument('-H', type=int, default=None, help='Show first N rows')
    parser.add_argument('-T', type=int, default=None, help='Show last N rows')
    parser.add_argument('-R', nargs=2, type=int, default=None, metavar=('START', 'END'), help='Show rows in range START to END (zero-based, END exclusive)')
    parser.add_argument('-L', type=str, default=None, help='Perform df.loc[expression] (e.g., "0:5", "df.age > 25")')
    parser.add_argument('-I', type=str, default=None, help='Perform df.iloc[expression] (e.g., "0:5", "[0,2,4]")')
    parser.add_argument('-u', type=str, default=None, help='Show unique values for column')
    parser.add_argument('-c', type=str, default=None, help='Show info about column')
    parser.add_argument('-v', type=str, default=None, help='Show value counts for column')
    parser.add_argument('-s', type=str, default=None, help='Show stats for numerical column')
    parser.add_argument('-l', action='store_true', help='List columns')
    parser.add_argument('-i', action='store_true', help='Show file info')
    args = parser.parse_args()

    terminal_size = shutil.get_terminal_size((80, 24))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', terminal_size.columns)

    df = load_df(args.datafile, delimiter=args.d, excel_sheet=args.xs, excel_skiprows=args.xr, force_format=args.f)

    # Chain loc and iloc operations in the order they appear in sys.argv
    loc_iloc_ops = []
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == '-L' and i + 1 < len(sys.argv):
            loc_iloc_ops.append(('loc', sys.argv[i + 1]))
            i += 2
        elif sys.argv[i] == '-I' and i + 1 < len(sys.argv):
            loc_iloc_ops.append(('iloc', sys.argv[i + 1]))
            i += 2
        else:
            i += 1
    
    # Apply loc/iloc operations in order
    for op_type, op_value in loc_iloc_ops:
        if op_type == 'loc':
            df = apply_loc(df, op_value)
        else:
            df = apply_iloc(df, op_value)

    # Track if any operation was performed
    any_operation = any([args.i, args.l, args.H, args.T, args.R, args.L, args.I, args.u, args.c, args.v, args.s])

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
    if loc_iloc_ops:
        print(df)  # Print the final result of chained operations
    elif args.L:
        print_loc(df, args.L)
    elif args.I:
        print_iloc(df, args.I)
    if args.u:
        print_unique(df, args.u)
    if args.c:
        print_colinfo(df, args.c)
    if args.v:
        print_value_counts(df, args.v)
    if args.s:
        print_stats(df, args.s)
    # Default: show info and head if no options
    if not any_operation:
        print_info(df)
        print_head(df, 5)

if __name__ == "__main__":
    main()
