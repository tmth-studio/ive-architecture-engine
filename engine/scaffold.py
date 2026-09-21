#!/usr/bin/env python3
"""Create a deliberately incomplete architecture package from a valid JSON brief."""
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: scaffold.py INPUT.json OUTPUT.json", file=sys.stderr)
        return 2
    source = json.loads(Path(sys.argv[1]).read_text())
    artifact = {
        "schema_version": "0.1",
        "venture": source["venture"],
        "requirements": [],
        "components": [],
        "evidence": source.get("evidence", []),
        "financial_model": {"price_ceiling": None, "cost_floor": None, "fmos": None},
        "open_items": [
            {"id": "OPEN-1", "statement": "Complete requirements, components and financial model.", "status": "open"}
        ],
    }
    Path(sys.argv[2]).write_text(json.dumps(artifact, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
