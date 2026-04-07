import subprocess
import sys
import time
from pathlib import Path

# Add tests dir path to sys to import the generator
sys.path.append(str(Path(__file__).parent))
from generate_report import generate_reports

TEST_GROUPS = {
    # ================= UI TESTS =================
    "UI-1": [("tests/ui/test_dashboard_loads.py", "UI - Dashboard", "Verify dashboard charts and summary load")],
    "UI-2": [("tests/ui/test_revenue_recognition_ui.py", "UI - Revenue Recognition", "Verify global slicers (year/month) filter data")],
    
    # ================= API TESTS =================
    "API-1": [("tests/api/test_health_api.py", "API - Health & Base", "Dashboard main page resolves correctly")],
    "API-2": [("tests/api/test_revenue_recognition_api.py", "API - RR", "Slicer filters applied properly to endpoints")],
}


def run_test(file_path, label, description):
    print(f"\n🧪 Running: {label}")
    print(f"📌 What it checks: {description}\n")

    start_time = time.time()
    
    # ensure it runs properly from root project directory
    result = subprocess.run([sys.executable, file_path], capture_output=True, text=True)
    end_time = time.time()

    duration = round(end_time - start_time, 2)
    
    # For UI tests, maybe they generated a screenshot on failure in `reports/screenshots/`
    # Our scripts will print a specific token `SCREENSHOT:path/to/file.png` if they took a screenshot.
    screenshot_path = ""
    for line in result.stdout.split("\n"):
        if "SCREENSHOT:" in line:
            screenshot_path = line.split("SCREENSHOT:")[1].strip()

    if result.returncode == 0:
        print(f"✅ PASSED: {label}")
        print(f"✔ {description}")
        return {
            "name": label,
            "status": "PASS",
            "description": description,
            "time": duration,
            "screenshot": ""
        }
    else:
        print(f"❌ FAILED: {label}")
        print(f"✖ {description}")
        print(f"Stdout logs:\n{result.stdout}")
        print(f"Stderr logs:\n{result.stderr}")
        return {
            "name": label,
            "status": "FAIL",
            "description": description,
            "time": duration,
            "screenshot": screenshot_path
        }


def print_menu():
    print("\n===== SYKFINANCE TEST RUNNER =====")

    print("\n--- UI TESTS ---")
    for key, tests in TEST_GROUPS.items():
        if key.startswith("UI-"):
            label = tests[0][1]
            print(f"{key:<6} - {label}")

    print("\n--- API TESTS ---")
    for key, tests in TEST_GROUPS.items():
        if key.startswith("API-"):
            label = tests[0][1]
            print(f"{key:<6} - {label}")

    print("\n--- RUN GROUPS ---")
    print("ALL-UI - Run All UI Tests")
    print("ALL-API - Run All API Tests")
    print("ALL    - Run Complete Suite")


def run_group(prefix):
    results = []
    for key, tests in TEST_GROUPS.items():
        if key.startswith(prefix):
            for file_path, label, description in tests:
                results.append(run_test(file_path, label, description))
    return results


def run_all():
    results = []
    for tests in TEST_GROUPS.values():
        for file_path, label, description in tests:
            results.append(run_test(file_path, label, description))
    return results


def main():
    print_menu()

    choice = input("\nEnter your choice (e.g. ALL): ").strip().upper()

    if choice == "ALL-UI":
        results = run_group("UI")
    elif choice == "ALL-API":
        results = run_group("API")
    elif choice == "ALL":
        results = run_all()
    elif choice in TEST_GROUPS:
        tests = TEST_GROUPS[choice]
        results = []
        for file_path, label, description in tests:
            results.append(run_test(file_path, label, description))
    else:
        print("❌ Invalid choice")
        return

    print("\n========================")
    passed = all(r["status"] == "PASS" for r in results)

    if passed:
        print("🎉 ALL SELECTED TESTS PASSED")
    else:
        print("⚠️ SOME TESTS FAILED")
    print("========================")

    print("\n===== TEST SUMMARY =====")
    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"{icon} {r['name']} → {r['description']}")

    generate_reports(results)


if __name__ == "__main__":
    main()
