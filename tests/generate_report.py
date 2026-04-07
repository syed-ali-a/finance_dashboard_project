import csv
from datetime import datetime
from pathlib import Path
import openpyxl

REPORTS_DIR = Path("reports")
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

def generate_reports(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    html_file = REPORTS_DIR / f"test_report_{timestamp}.html"
    csv_file = REPORTS_DIR / f"test_report_{timestamp}.csv"
    xlsx_file = REPORTS_DIR / f"test_report_{timestamp}.xlsx"

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    # ========================== HTML GENERATION ============================
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Automation Report - SkyFinance</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            padding: 20px;
        }}
        .summary {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: #1e293b;
            padding: 20px;
            border-radius: 10px;
            width: 200px;
            text-align: center;
        }}
        .pass {{ color: #22c55e; }}
        .fail {{ color: #ef4444; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #1e293b;
            border-radius: 10px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            border-bottom: 1px solid #334155;
            text-align: left;
        }}
        th {{
            background: #020617;
        }}
        .PASS {{ color: #22c55e; font-weight: bold; }}
        .FAIL {{ color: #ef4444; font-weight: bold; }}
        img {{
            width: 150px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>

<h1>🚀 SkyFinance Automation Test Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<div class="summary">
    <div class="card">
        <h3>Total</h3>
        <p>{total}</p>
    </div>
    <div class="card">
        <h3 class="pass">Passed</h3>
        <p>{passed}</p>
    </div>
    <div class="card">
        <h3 class="fail">Failed</h3>
        <p>{failed}</p>
    </div>
</div>

<table>
<tr>
    <th>Test</th>
    <th>Status</th>
    <th>Description</th>
    <th>Time (s)</th>
    <th>Screenshot</th>
</tr>
"""

    for r in results:
        screenshot_html = "-"
        if r.get("status") == "FAIL" and r.get("screenshot"):
            # Using absolute or relative path to screenshot can be tricky, make it relative
            # Since HTML is in 'reports/', the screenshot relative path is 'screenshots/filename'
            img_name = Path(r["screenshot"]).name
            screenshot_html = f'<a href="screenshots/{img_name}" target="_blank"><img src="screenshots/{img_name}"></a>'

        html += f"""
<tr>
    <td>{r['name']}</td>
    <td class="{r['status']}">{r['status']}</td>
    <td>{r['description']}</td>
    <td>{r['time']}</td>
    <td>{screenshot_html}</td>
</tr>
"""

    html += """
</table>
</body>
</html>
"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)


    # ========================== CSV GENERATION ============================
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Test Name", "Status", "Description", "Time (s)", "Screenshot Path"])
        for r in results:
            writer.writerow([
                r["name"], 
                r["status"], 
                r["description"], 
                r["time"], 
                r.get("screenshot", "")
            ])

    # ========================== XLSX GENERATION ============================
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test Results"
        
        headers = ["Test Name", "Status", "Description", "Time (s)", "Screenshot Path"]
        ws.append(headers)

        for r in results:
            ws.append([
                r["name"],
                r["status"],
                r["description"],
                r["time"],
                r.get("screenshot", "N/A")
            ])
            
        wb.save(xlsx_file)
        print(f"🔥 XLSX Report generated: {xlsx_file}")
    except Exception as e:
        print(f"⚠️ Could not generate XLSX report: {e}")

    print(f"🔥 HTML Report generated: {html_file}")
    print(f"🔥 CSV Report generated:  {csv_file}")
