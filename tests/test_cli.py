import os
import subprocess
import pytest

# Sample files in the root directory
SAMPLE_CSV = os.path.join(os.path.dirname(__file__), '..', 'sample.csv')
SAMPLE_FEATHER = os.path.join(os.path.dirname(__file__), '..', 'sample.feather')
SAMPLE_XLSX = os.path.join(os.path.dirname(__file__), '..', 'sample.xlsx')

def run_dfpeek(args, sample_file=SAMPLE_FEATHER):
    """Helper function to run dfpeek command"""
    cmd = f"dfpeek {sample_file} {args}".strip()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

@pytest.mark.parametrize("sample_file", [SAMPLE_CSV, SAMPLE_FEATHER, SAMPLE_XLSX])
@pytest.mark.parametrize("args,expected", [
    ("-H 2", "Alice"),
    ("-T 2", "Evan"),
    ("-R 1 3", "Charlie"),
    ("-u city", "San Diego"),
    ("-c age", "Type:"),
    ("-v status", "active"),
    ("-s age", "mean"),
    ("-l", "name"),
    ("-i", "RangeIndex"),
    ("", "Alice"),
])
def test_cli_basic_options(sample_file, args, expected):
    """Test basic CLI options with different file formats"""
    result = run_dfpeek(args, sample_file)
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert expected in result.stdout, f"Expected '{expected}' not found in output"

@pytest.mark.parametrize("args,expected", [
    ("-L 0:2", "Alice"),
    ("-L \"df.age > 30\"", "Charlie"),
    ("-I 0:2", "Alice"),
    ("-I [0,2]", "Charlie"),
])
def test_cli_advanced_indexing(args, expected):
    """Test advanced indexing options (loc and iloc)"""
    result = run_dfpeek(args)
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert expected in result.stdout, f"Expected '{expected}' not found in output"

def test_cli_force_format():
    """Test forcing file format"""
    # Test forcing CSV format on a file with different extension
    result = run_dfpeek("-f csv -H 2", SAMPLE_CSV)
    assert result.returncode == 0
    assert "Alice" in result.stdout

def test_cli_excel_options():
    """Test Excel-specific options"""
    # Test Excel sheet selection (should work with sheet 1)
    result = run_dfpeek("-xs 1 -H 2", SAMPLE_XLSX)
    assert result.returncode == 0
    assert "Alice" in result.stdout

def test_cli_delimiter():
    """Test custom delimiter option"""
    # Create a TSV-like file and test delimiter
    result = run_dfpeek("-d ',' -H 2", SAMPLE_CSV)
    assert result.returncode == 0
    assert "Alice" in result.stdout

def test_cli_chained_options():
    """Test chaining multiple options"""
    result = run_dfpeek("-i -l -H 2")
    assert result.returncode == 0
    assert "RangeIndex" in result.stdout  # from -i
    assert "name" in result.stdout        # from -l
    assert "Alice" in result.stdout       # from -H 2

def test_cli_error_handling():
    """Test error handling for invalid options"""
    # Test non-existent column
    result = run_dfpeek("-u nonexistent_column")
    assert "not found" in result.stdout.lower() or result.returncode != 0

    # Test invalid loc expression
    result = run_dfpeek("-L 'invalid_expression'")
    assert "error" in result.stdout.lower() or result.returncode != 0
