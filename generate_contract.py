"""Generate ODCS v3.2.0 data contract for FINSERV_DW."""
import yaml
import uuid
import os
from datetime import date

# --- Metadata from FINSERV_DW.INFORMATION_SCHEMA ---
# (schema, table, type, row_count, column, position, data_type, nullable, char_max, num_prec, num_scale)
raw_metadata = [
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"CUSTOMER_ID",1,"NUMBER","YES",None,11,0),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"CUSTOMER_CODE",2,"TEXT","YES",16777216,None,None),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"FULL_NAME",3,"TEXT","YES",16777216,None,None),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"CUSTOMER_TIER",4,"TEXT","YES",8,None,None),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"CREDIT_SCORE",5,"NUMBER","YES",None,3,0),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"ANNUAL_INCOME",6,"NUMBER","YES",None,12,2),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"MEMBER_SINCE",7,"DATE","YES",None,None,None),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"IS_ACTIVE",8,"BOOLEAN","YES",None,None,None),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"COMPANY_NAME",9,"TEXT","YES",100,None,None),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"ACCOUNT_COUNT",10,"NUMBER","YES",None,18,0),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"TOTAL_BALANCE",11,"NUMBER","YES",None,26,2),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"TRANSACTION_COUNT",12,"NUMBER","YES",None,18,0),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"TOTAL_SPENT",13,"NUMBER","YES",None,26,2),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"RISK_SCORE",14,"NUMBER","YES",None,38,0),
    ("ANALYTICS","CUSTOMER_360","VIEW",None,"CREDIT_RISK",15,"TEXT","YES",8,None,None),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"POLICY_TYPE",1,"TEXT","YES",16777216,None,None),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"RISK_LEVEL",2,"TEXT","YES",8,None,None),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"TOTAL_POLICIES",3,"NUMBER","YES",None,18,0),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"TOTAL_CLAIMS",4,"NUMBER","YES",None,18,0),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"CLAIMS_RATIO",5,"FLOAT","YES",None,None,None),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"AVG_MONTHLY_PREMIUM",6,"NUMBER","YES",None,29,2),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"AVG_CLAIM_AMOUNT",7,"NUMBER","YES",None,33,2),
    ("ANALYTICS","POLICY_PERFORMANCE","VIEW",None,"TOTAL_CLAIM_AMOUNT",8,"NUMBER","YES",None,26,2),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"ACCOUNT_ID",1,"NUMBER","YES",None,18,0),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"CUSTOMER_ID",2,"NUMBER","YES",None,11,0),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"ACCOUNT_NUMBER",3,"TEXT","YES",16777216,None,None),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"ACCOUNT_TYPE",4,"TEXT","YES",12,None,None),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"OPENED_DATE",5,"DATE","YES",None,None,None),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"STATUS",6,"TEXT","YES",7,None,None),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"CURRENT_BALANCE",7,"NUMBER","YES",None,14,2),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"INTEREST_RATE",8,"NUMBER","YES",None,8,4),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"OVERDRAFT_PROTECTION",9,"BOOLEAN","YES",None,None,None),
    ("CORE","ACCOUNTS","BASE TABLE",83433,"LAST_TRANSACTION_DATE",10,"TIMESTAMP_NTZ","YES",None,None,None),
    ("CORE","COMPANIES","BASE TABLE",15,"COMPANY_ID",1,"TEXT","NO",4,None,None),
    ("CORE","COMPANIES","BASE TABLE",15,"COMPANY_NAME",2,"TEXT","NO",100,None,None),
    ("CORE","COMPANIES","BASE TABLE",15,"COMPANY_TYPE",3,"TEXT","YES",50,None,None),
    ("CORE","COMPANIES","BASE TABLE",15,"HQ_CITY",4,"TEXT","YES",50,None,None),
    ("CORE","COMPANIES","BASE TABLE",15,"HQ_STATE",5,"TEXT","YES",2,None,None),
    ("CORE","COMPANIES","BASE TABLE",15,"FOUNDED_YEAR",6,"NUMBER","YES",None,38,0),
    ("CORE","COMPANIES","BASE TABLE",15,"EMPLOYEE_COUNT",7,"NUMBER","YES",None,38,0),
    ("CORE","COMPANIES","BASE TABLE",15,"AUM_BILLIONS",8,"NUMBER","YES",None,12,2),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"CUSTOMER_ID",1,"NUMBER","YES",None,11,0),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"CUSTOMER_CODE",2,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"COMPANY_ID",3,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"FIRST_NAME",4,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"LAST_NAME",5,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"EMAIL",6,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"PHONE",7,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"DATE_OF_BIRTH",8,"DATE","YES",None,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"GENDER",9,"TEXT","YES",1,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"ADDRESS_LINE1",10,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"CITY",11,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"STATE_CODE",12,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"ZIP_CODE",13,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"CUSTOMER_TIER",14,"TEXT","YES",8,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"CREDIT_SCORE",15,"NUMBER","YES",None,3,0),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"ANNUAL_INCOME",16,"NUMBER","YES",None,12,2),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"EMPLOYMENT_STATUS",17,"TEXT","YES",16777216,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"MEMBER_SINCE",18,"DATE","YES",None,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"IS_ACTIVE",19,"BOOLEAN","YES",None,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"LAST_ACTIVITY_DATE",20,"TIMESTAMP_NTZ","YES",None,None,None),
    ("CORE","CUSTOMERS","BASE TABLE",50000,"ADVISOR_NOTES",21,"TEXT","YES",16777216,None,None),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"DOCUMENT_ID",1,"NUMBER","YES",None,11,0),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"CUSTOMER_ID",2,"NUMBER","YES",None,5,0),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"DOCUMENT_TYPE",3,"TEXT","YES",16777216,None,None),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"FILE_NAME",4,"TEXT","YES",16777216,None,None),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"FILE_PATH",5,"TEXT","YES",16777216,None,None),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"FILE_SIZE_BYTES",6,"NUMBER","YES",None,8,0),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"MIME_TYPE",7,"TEXT","YES",15,None,None),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"PAGE_COUNT",8,"NUMBER","YES",None,2,0),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"UPLOADED_DATE",9,"TIMESTAMP_NTZ","YES",None,None,None),
    ("CORE","DOCUMENTS","BASE TABLE",5000,"OCR_EXTRACTED_TEXT",10,"TEXT","YES",16777216,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"CLAIM_ID",1,"NUMBER","YES",None,18,0),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"POLICY_ID",2,"NUMBER","YES",None,11,0),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"CUSTOMER_ID",3,"NUMBER","YES",None,38,0),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"CLAIM_NUMBER",4,"TEXT","YES",16777216,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"INCIDENT_DATE",5,"DATE","YES",None,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"REPORTED_DATE",6,"DATE","YES",None,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"CLAIM_TYPE",7,"TEXT","YES",16777216,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"CLAIM_AMOUNT",8,"NUMBER","YES",None,14,2),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"STATUS",9,"TEXT","YES",12,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"ADJUSTER_NAME",10,"TEXT","YES",16777216,None,None),
    ("INSURANCE","CLAIMS","BASE TABLE",9847,"ADJUSTER_NOTES",11,"TEXT","YES",16777216,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"POLICY_ID",1,"NUMBER","YES",None,11,0),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"CUSTOMER_ID",2,"NUMBER","YES",None,38,0),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"COMPANY_ID",3,"TEXT","YES",16777216,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"POLICY_TYPE",4,"TEXT","YES",16777216,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"POLICY_NUMBER",5,"TEXT","YES",16777216,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"EFFECTIVE_DATE",6,"DATE","YES",None,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"EXPIRATION_DATE",7,"DATE","YES",None,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"PREMIUM_MONTHLY",8,"NUMBER","YES",None,10,2),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"COVERAGE_AMOUNT",9,"NUMBER","YES",None,14,2),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"DEDUCTIBLE_AMOUNT",10,"NUMBER","YES",None,10,2),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"RISK_LEVEL",11,"TEXT","YES",8,None,None),
    ("INSURANCE","POLICIES","BASE TABLE",35000,"STATUS",12,"TEXT","YES",9,None,None),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"ALERT_ID",1,"NUMBER","YES",None,18,0),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"CUSTOMER_ID",2,"NUMBER","YES",None,11,0),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"ACCOUNT_ID",3,"NUMBER","YES",None,18,0),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"ALERT_DATE",4,"TIMESTAMP_NTZ","YES",None,None,None),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"ALERT_TYPE",5,"TEXT","YES",16777216,None,None),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"SEVERITY",6,"TEXT","YES",8,None,None),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"FLAGGED_AMOUNT",7,"NUMBER","YES",None,12,2),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"STATUS",8,"TEXT","YES",15,None,None),
    ("RISK","FRAUD_ALERTS","BASE TABLE",8000,"RESOLUTION_DATE",9,"TIMESTAMP_NTZ","YES",None,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"ASSESSMENT_ID",1,"NUMBER","YES",None,11,0),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"CUSTOMER_ID",2,"NUMBER","YES",None,11,0),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"ASSESSMENT_DATE",3,"DATE","YES",None,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"RISK_SCORE",4,"NUMBER","YES",None,38,0),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"CREDIT_RISK",5,"TEXT","YES",8,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"MARKET_RISK",6,"TEXT","YES",16777216,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"OPERATIONAL_RISK",7,"TEXT","YES",16777216,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"AML_RISK",8,"TEXT","YES",8,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"NEXT_REVIEW_DATE",9,"DATE","YES",None,None,None),
    ("RISK","RISK_ASSESSMENTS","BASE TABLE",50000,"ASSESSMENT_DETAIL",10,"VARIANT","YES",None,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"TRANSACTION_ID",1,"NUMBER","YES",None,11,0),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"ACCOUNT_ID",2,"NUMBER","YES",None,38,0),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"TRANSACTION_DATE",3,"TIMESTAMP_NTZ","YES",None,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"POST_DATE",4,"DATE","YES",None,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"TRANSACTION_TYPE",5,"TEXT","YES",16777216,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"CATEGORY",6,"TEXT","YES",16777216,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"AMOUNT",7,"NUMBER","YES",None,14,2),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"MERCHANT_NAME",8,"TEXT","YES",16777216,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"CHANNEL",9,"TEXT","YES",16777216,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"STATUS",10,"TEXT","YES",9,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"REFERENCE_NUMBER",11,"TEXT","YES",16777216,None,None),
    ("TRANSACTIONS","TRANSACTIONS","BASE TABLE",200000,"TRANSACTION_METADATA",12,"VARIANT","YES",None,None,None),
]

# --- Group into tables ---
tables = {}
for schema, tbl, ttype, rows, col, pos, dtype, nullable, cmax, nprec, nscale in raw_metadata:
    key = (schema, tbl)
    if key not in tables:
        tables[key] = {"schema": schema, "table": tbl, "type": ttype, "row_count": rows, "columns": []}
    tables[key]["columns"].append({
        "name": col, "position": pos, "data_type": dtype,
        "nullable": nullable == "YES", "char_max_len": cmax,
        "num_precision": nprec, "num_scale": nscale,
    })

# --- Type mapping ---
def map_logical_type(col):
    dt = col["data_type"].upper()
    if dt in ("TEXT", "VARCHAR"):
        return "string"
    if dt == "NUMBER":
        if col["num_scale"] is not None and col["num_scale"] == 0:
            return "integer"
        return "number"
    if dt == "FLOAT":
        return "number"
    if dt == "DATE":
        return "date"
    if dt in ("TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ"):
        return "timestamp"
    if dt == "BOOLEAN":
        return "boolean"
    if dt == "VARIANT":
        return "object"
    return "string"

def build_physical_type(col):
    dt = col["data_type"].upper()
    if dt == "NUMBER" and col["num_precision"] is not None:
        scale = col["num_scale"] if col["num_scale"] is not None else 0
        return f"NUMBER({col['num_precision']},{scale})"
    if dt in ("TEXT", "VARCHAR") and col["char_max_len"] is not None:
        return f"VARCHAR({col['char_max_len']})"
    return dt

# --- Classification ---
PII_COLUMNS = {"EMAIL", "PHONE", "DATE_OF_BIRTH", "ADDRESS_LINE1", "ZIP_CODE", "GENDER"}
CONFIDENTIAL_COLUMNS = {"ADVISOR_NOTES", "ADJUSTER_NOTES", "OCR_EXTRACTED_TEXT", "ASSESSMENT_DETAIL", "TRANSACTION_METADATA"}

def classify_column(col_name):
    upper = col_name.upper()
    if upper in PII_COLUMNS:
        return "restricted"
    if upper in CONFIDENTIAL_COLUMNS:
        return "confidential"
    if upper.endswith("_ID") or upper.endswith("_CODE") or upper.endswith("_NUMBER"):
        return "internal"
    return "public"

def is_primary_key(col_name, table_name):
    singular = table_name.rstrip("S").upper()
    return col_name.upper() == f"{singular}_ID"

CDES = {"CUSTOMER_ID", "ACCOUNT_ID", "POLICY_ID", "CLAIM_ID", "TRANSACTION_ID",
        "COMPANY_ID", "DOCUMENT_ID", "ASSESSMENT_ID", "ALERT_ID"}

# --- Build contract ---
ACCOUNT = "SFSEHOL-DATA_IN_THE_D_HACKATHON_OCTOBER_GVKWCD"
HOST = f"{ACCOUNT}.snowflakecomputing.com"
DATABASE = "FINSERV_DW"
WAREHOUSE = "COMPUTE_WH"

DOMAIN_TAGS = {
    "CORE": ["finance", "core", "master-data"],
    "TRANSACTIONS": ["finance", "transactions"],
    "INSURANCE": ["finance", "insurance"],
    "RISK": ["finance", "risk", "compliance"],
    "ANALYTICS": ["finance", "analytics", "derived"],
}

DOMAIN_DESCRIPTIONS = {
    "CORE": "Core reference and master data for customers, accounts, companies, and documents.",
    "TRANSACTIONS": "Financial transaction records across all account types.",
    "INSURANCE": "Insurance policy and claims management data.",
    "RISK": "Risk assessments, fraud detection, and AML compliance data.",
    "ANALYTICS": "Pre-built analytical views combining data across domains.",
}

schema_objects = []
for (schema_name, table_name), tbl in sorted(tables.items()):
    pk_position = 1
    properties = []
    for col in tbl["columns"]:
        prop = {
            "name": col["name"].lower(),
            "logicalType": map_logical_type(col),
            "physicalType": build_physical_type(col),
            "classification": classify_column(col["name"]),
        }
        if not col["nullable"]:
            prop["required"] = True
        if is_primary_key(col["name"], table_name):
            prop["primaryKey"] = True
            prop["primaryKeyPosition"] = pk_position
            pk_position += 1
        if col["name"].upper() in CDES:
            prop["criticalDataElement"] = True
        properties.append(prop)

    physical_type = "table" if tbl["type"] == "BASE TABLE" else "view"
    obj = {
        "name": table_name.lower(),
        "logicalType": "object",
        "physicalType": physical_type,
        "physicalName": table_name,
        "description": DOMAIN_DESCRIPTIONS.get(schema_name, ""),
        "tags": DOMAIN_TAGS.get(schema_name, ["finance"]),
        "properties": properties,
    }
    if tbl["row_count"] is not None:
        obj["dataGranularityDescription"] = f"Approximately {tbl['row_count']:,} rows as of {date.today().isoformat()}"
    schema_objects.append(obj)

schemas_used = sorted(set(k[0] for k in tables))
servers = []
for schema_name in schemas_used:
    servers.append({
        "id": f"finserv-prod-{schema_name.lower()}",
        "server": f"snowflake-finserv-dw-{schema_name.lower()}",
        "type": "snowflake",
        "environment": "prod",
        "account": ACCOUNT,
        "host": HOST,
        "port": 443,
        "database": DATABASE,
        "schema": schema_name,
        "warehouse": WAREHOUSE,
    })

contract = {
    "apiVersion": "v3.2.0",
    "kind": "DataContract",
    "id": str(uuid.uuid4()),
    "name": "finserv_dw",
    "version": "1.0.0",
    "status": "active",
    "domain": "financial-services",
    "description": {
        "purpose": "Comprehensive financial services data warehouse covering customer management, transaction processing, insurance operations, risk assessment, and pre-built analytics.",
        "limitations": "Analytics views (CUSTOMER_360, POLICY_PERFORMANCE) are derived and may reflect stale data depending on upstream refresh schedules.",
        "usage": "Primary data source for BI dashboards, regulatory reporting, risk analytics, and customer insights.",
    },
    "tags": ["finance", "data-warehouse", "finserv", "regulated"],
    "schema": schema_objects,
    "servers": servers,
    "slaProperties": [
        {
            "id": "latency_sla",
            "property": "latency",
            "value": "1",
            "unit": "d",
            "description": "Placeholder - data should be no more than 1 day old.",
        }
    ],
    "team": [
        {
            "username": "data-engineering",
            "name": "Data Engineering",
            "description": "Placeholder - assign team ownership here.",
        }
    ],
}

# --- Write YAML ---
def clean_nones(d):
    if isinstance(d, dict):
        return {k: clean_nones(v) for k, v in d.items() if v is not None}
    if isinstance(d, list):
        return [clean_nones(i) for i in d]
    return d

output_dir = "contracts"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "finserv_dw.odcs.yaml")

cleaned = clean_nones(contract)
with open(output_path, "w", encoding="utf-8") as f:
    yaml.dump(cleaned, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

print(f"Contract written to: {output_path}")
print(f"File size: {os.path.getsize(output_path):,} bytes")
print(f"Objects: {len(schema_objects)}, Properties: {sum(len(o['properties']) for o in schema_objects)}, Servers: {len(servers)}")
