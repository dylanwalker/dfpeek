import pandas as pd
import pytest
from dfpeek.__main__ import (print_head, print_tail, print_range, print_loc, print_iloc, 
                            print_unique, print_colinfo, print_value_counts, print_stats, 
                            print_columns, print_info, load_df)

@pytest.fixture
def df():
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan', 'Fay'],
        'age': [30, 25, 35, 28, 40, 22],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'San Diego'],
        'status': ['active', 'inactive', 'active', 'active', 'inactive', 'active']
    }
    return pd.DataFrame(data)

def test_print_head(df, capsys):
    print_head(df, 2)
    out = capsys.readouterr().out
    assert 'Alice' in out and 'Bob' in out

def test_print_tail(df, capsys):
    print_tail(df, 2)
    out = capsys.readouterr().out
    assert 'Evan' in out and 'Fay' in out

def test_print_range(df, capsys):
    print_range(df, 1, 4)
    out = capsys.readouterr().out
    assert 'Bob' in out and 'Charlie' in out and 'Diana' in out

def test_print_unique(df, capsys):
    print_unique(df, 'city')
    out = capsys.readouterr().out
    assert 'New York' in out and 'San Diego' in out

def test_print_colinfo(df, capsys):
    print_colinfo(df, 'age')
    out = capsys.readouterr().out
    assert 'Type:' in out and 'Nulls:' in out

def test_print_value_counts(df, capsys):
    print_value_counts(df, 'status')
    out = capsys.readouterr().out
    assert 'active' in out and 'inactive' in out

def test_print_stats(df, capsys):
    print_stats(df, 'age')
    out = capsys.readouterr().out
    assert 'mean' in out or 'count' in out
