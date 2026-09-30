"""Run all eval cases and print accuracy. Usage: python -m tests.run_eval"""
import json
from pathlib import Path

from ai.triage import triage_incident
from scripts.try_one import load_attachments

cases = json.loads((Path(__file__).parent / "eval_cases.json").read_text(encoding="utf-8"))
type_ok = sev_ok = 0
for c in cases:
    try:
        inc = triage_incident(c["text"], load_attachments(c.get("files"))).incident
    except Exception as e:
        print(f"{c['id']}: ERROR {e}")
        continue
    t = inc.type == c["expected_type"]
    s = inc.severity == c["expected_severity"]
    type_ok += t
    sev_ok += s
    print(f"{c['id']}: type {'OK' if t else 'WRONG'} ({inc.type}), severity {'OK' if s else 'WRONG'} ({inc.severity})")
n = len(cases)
print(f"\nType accuracy: {type_ok}/{n}   Severity accuracy: {sev_ok}/{n}")
