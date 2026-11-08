"""Run datacontract test against all per-schema contracts and summarize."""
import subprocess, json, os, sys

contracts = [
    "contracts/finserv_dw_core.odcs.yaml",
    "contracts/finserv_dw_analytics.odcs.yaml",
    "contracts/finserv_dw_insurance.odcs.yaml",
    "contracts/finserv_dw_risk.odcs.yaml",
    "contracts/finserv_dw_transactions.odcs.yaml",
]

env = os.environ.copy()
env["DATACONTRACT_SNOWFLAKE_USERNAME"] = "USER"
env["DATACONTRACT_SNOWFLAKE_AUTHENTICATOR"] = "oauth_authorization_code"
env["DATACONTRACT_SNOWFLAKE_ROLE"] = "ACCOUNTADMIN"
env["DATACONTRACT_SNOWFLAKE_WAREHOUSE"] = "COMPUTE_WH"
env["PYTHONIOENCODING"] = "utf-8"

all_results = {}
for contract in contracts:
    name = os.path.basename(contract).replace("finserv_dw_", "").replace(".odcs.yaml", "").upper()
    output_file = f"results_{name.lower()}.json"
    print(f"Testing {name}...", end=" ", flush=True)
    result = subprocess.run(
        ["datacontract", "test", contract, "--checks", "properties", "--metadata-only",
         "--output", output_file, "--output-format", "json"],
        env=env, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if os.path.exists(output_file):
        with open(output_file) as f:
            data = json.load(f)
        passed = sum(1 for c in data["checks"] if c["result"] == "passed")
        failed = sum(1 for c in data["checks"] if c["result"] == "failed")
        skipped = sum(1 for c in data["checks"] if c["result"] == "skipped")
        all_results[name] = {"passed": passed, "failed": failed, "skipped": skipped, "total": len(data["checks"])}
        print(f"passed={passed}, failed={failed}, skipped={skipped}")
    else:
        all_results[name] = {"error": "no output file"}
        print(f"ERROR - no output. stderr: {result.stderr[:200]}")

print("\n=== SUMMARY ===")
total_passed = sum(r.get("passed", 0) for r in all_results.values())
total_failed = sum(r.get("failed", 0) for r in all_results.values())
total_skipped = sum(r.get("skipped", 0) for r in all_results.values())
for name, r in all_results.items():
    status = "PASS" if r.get("failed", 0) == 0 and "error" not in r else "FAIL"
    print(f"  {status} {name}: {r}")
print(f"\nTOTAL: {total_passed} passed, {total_failed} failed, {total_skipped} skipped")
