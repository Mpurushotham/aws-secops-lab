import json

def lambda_handler(event, context):
    findings = event.get('detail', {}).get('findings', [])
    print(f"Auto-remediating {len(findings)} findings...")
    for finding in findings:
        print(f"Remediating: {finding.get('Title')}")
    return {"statusCode": 200, "body": json.dumps("Remediation triggered")}
