"""Split the single ODCS contract into per-schema contracts."""
import yaml, uuid, os

with open("contracts/finserv_dw.odcs.yaml", "r") as f:
    data = yaml.safe_load(f)

schema_to_server = {s["schema"]: s for s in data["servers"]}

schema_tags = {
    "ANALYTICS": ["finance", "analytics", "derived"],
    "CORE": ["finance", "core", "master-data"],
    "INSURANCE": ["finance", "insurance"],
    "RISK": ["finance", "risk", "compliance"],
    "TRANSACTIONS": ["finance", "transactions"],
}

domain_descs = {
    "ANALYTICS": "Pre-built analytical views combining data across domains.",
    "CORE": "Core reference and master data for customers, accounts, companies, and documents.",
    "INSURANCE": "Insurance policy and claims management data.",
    "RISK": "Risk assessments, fraud detection, and AML compliance data.",
    "TRANSACTIONS": "Financial transaction records across all account types.",
}

for schema_name in sorted(schema_to_server.keys()):
    server = schema_to_server[schema_name]
    expected_tags = set(schema_tags[schema_name])
    objects = [o for o in data["schema"] if set(o.get("tags", [])) == expected_tags]
    if not objects:
        continue

    contract = {
        "apiVersion": "v3.2.0",
        "kind": "DataContract",
        "id": str(uuid.uuid4()),
        "name": f"finserv_dw_{schema_name.lower()}",
        "version": "1.0.0",
        "status": "active",
        "domain": schema_name.lower(),
        "description": {
            "purpose": domain_descs[schema_name],
            "usage": data["description"]["usage"],
        },
        "tags": schema_tags[schema_name],
        "schema": objects,
        "servers": [server],
        "slaProperties": data.get("slaProperties", []),
        "team": data.get("team", []),
    }

    fname = f"finserv_dw_{schema_name.lower()}.odcs.yaml"
    fpath = os.path.join("contracts", fname)
    with open(fpath, "w", encoding="utf-8") as f:
        yaml.dump(contract, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
    print(f"  {fname}: {len(objects)} objects, server={server['server']}")

print("Done.")
