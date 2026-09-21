#!/usr/bin/env python3
"""Dependency-free Tier-1 verifier for IVE Architecture Engine artifacts."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "rules" / "policy.json").read_text())


def check(artifact):
    findings = []
    required = {"schema_version", "venture", "requirements", "components", "evidence", "financial_model", "open_items"}
    missing = sorted(required - set(artifact))
    if missing:
        return [{"rule": "artifact-shape", "status": "FAIL", "detail": f"Missing fields: {', '.join(missing)}"}]
    if artifact["schema_version"] != POLICY["version"]:
        findings.append({"rule": "schema-version", "status": "FAIL", "detail": "Unsupported schema version."})

    component_ids = {item.get("id") for item in artifact["components"]}
    evidence = {item.get("id"): item for item in artifact["evidence"]}
    if not artifact["requirements"]:
        findings.append({"rule": "requirements", "status": "FAIL", "detail": "At least one requirement is required."})
    for requirement in artifact["requirements"]:
        rid = requirement.get("id", "unidentified")
        for field in ("statement", "bottleneck", "intervention", "verification"):
            if not isinstance(requirement.get(field), str) or not requirement[field].strip():
                findings.append({"rule": "requirement-completeness", "status": "FAIL", "detail": f"{rid} lacks {field}."})
        refs = requirement.get("component_ids", [])
        if not refs or any(ref not in component_ids for ref in refs):
            findings.append({"rule": "component-trace", "status": "FAIL", "detail": f"{rid} has missing component trace."})
        eids = requirement.get("evidence_ids", [])
        if not eids or any(ref not in evidence for ref in eids):
            findings.append({"rule": "evidence-trace", "status": "FAIL", "detail": f"{rid} has missing evidence trace."})

    for eid, record in evidence.items():
        if not record.get("source_or_test"):
            findings.append({"rule": "evidence-provenance", "status": "FAIL", "detail": f"{eid} lacks source or test."})
        if record.get("status") not in {"evidenced", "assumption"}:
            findings.append({"rule": "evidence-status", "status": "FAIL", "detail": f"{eid} has invalid status."})
        if record.get("status") == "assumption" and not record.get("falsification_test"):
            findings.append({"rule": "assumption-test", "status": "FAIL", "detail": f"{eid} needs a falsification test."})

    model = artifact["financial_model"]
    try:
        price, cost, supplied = float(model["price_ceiling"]), float(model["cost_floor"]), float(model["fmos"])
        calculated = (price - cost) / cost
        if cost <= 0 or abs(calculated - supplied) > 0.001:
            findings.append({"rule": "fmos-arithmetic", "status": "FAIL", "detail": "FMOS calculation is invalid."})
        elif supplied < POLICY["minimum_fmos"]:
            findings.append({"rule": "fmos-gate", "status": "FAIL", "detail": f"FMOS {supplied:.1%} is below {POLICY['minimum_fmos']:.0%}."})
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        findings.append({"rule": "fmos-arithmetic", "status": "FAIL", "detail": "Financial model must contain valid numeric values."})

    for item in artifact["open_items"]:
        if item.get("status") == "resolved":
            findings.append({"rule": "open-item-integrity", "status": "FAIL", "detail": f"{item.get('id', 'open item')} is listed as resolved; remove it or use open/blocked."})
    if not findings:
        findings.append({"rule": "all-tier-1-checks", "status": "PASS", "detail": "All published mechanical checks passed."})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--report", default=None)
    args = parser.parse_args()
    findings = check(json.loads(Path(args.artifact).read_text()))
    verdict = "PASS" if all(row["status"] == "PASS" for row in findings) else "FAIL"
    report = {"policy_version": POLICY["version"], "verdict": verdict, "findings": findings,
              "scope": "Mechanical verification only; not market validation or expert sign-off."}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.report:
        Path(args.report).write_text(rendered)
    print(rendered, end="")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
