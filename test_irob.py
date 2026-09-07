import subprocess
from pathlib import Path

def run_test():
    print("=== STARTING IROB E2E TEST ===")
    
    # 1. Create test input file
    print("[1/4] Creating test input file: test_input.csv")
    with open("test_input.csv", "w", encoding="utf-8") as f:
        f.write("id,name,role\n1,Alice,Engineer\n2,Bob,Manager\n")
        
    # 2. Test CLI conversion: CSV -> JSON (positional arguments)
    print("[2/4] Testing CLI conversion: CSV -> JSON")
    res = subprocess.run(["irob", "convert", "test_input.csv", "test_output.json"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    assert res.returncode == 0, "CLI conversion failed"

    # 3. Test CLI conversion: JSON -> SQLite
    print("[3/4] Testing CLI conversion: JSON -> SQLite")
    res = subprocess.run(["irob", "convert", "test_output.json", "sqlite:///test_cli.db"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    assert res.returncode == 0, "SQLite conversion failed"

    print("[4/4] All tests passed successfully!")

if __name__ == "__main__":
    run_test()
