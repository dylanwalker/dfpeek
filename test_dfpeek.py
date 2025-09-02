import subprocess
import sys

def run(cmd):
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

sample = "sample.csv"

# Test all options
run(f"dfpeek {sample} -H 2")
run(f"dfpeek {sample} -T 2")
run(f"dfpeek {sample} -R 1 4")
run(f"dfpeek {sample} -u city")
run(f"dfpeek {sample} -c age")
run(f"dfpeek {sample} -v status")
run(f"dfpeek {sample} -s age")
run(f"dfpeek {sample} -l")
run(f"dfpeek {sample} -i")
run(f"dfpeek {sample}")
