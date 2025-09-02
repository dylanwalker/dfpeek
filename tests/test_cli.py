import os
import subprocess
import pytest

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'sample.csv')

@pytest.mark.parametrize("args,expected", [
    ("-H 2", "Alice"),
    ("-T 2", "Evan"),
    ("-R 1 4", "Charlie"),
    ("-u city", "San Diego"),
    ("-c age", "Type:"),
    ("-v status", "active"),
    ("-s age", "mean"),
    ("-l", "name"),
    ("-i", "RangeIndex"),
    ("", "Alice"),
])
def test_cli(args, expected):
    cmd = f"dfpeek {SAMPLE} {args}".strip()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert expected in result.stdout
