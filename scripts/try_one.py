"""Try one case from the command line.
Example: python -m scripts.try_one --text "Water above knee height" --files data/samples/flood.jpg
"""
import argparse
import json
import mimetypes
from pathlib import Path

from ai.triage import Attachment, triage_incident


def load_attachments(paths):
    out = []
    for p in paths or []:
        path = Path(p)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        out.append(Attachment(path.name, path.read_bytes(), mime))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--files", nargs="*")
    args = ap.parse_args()
    result = triage_incident(args.text, load_attachments(args.files))
    print(json.dumps(result.incident.model_dump(), indent=2, ensure_ascii=False))
    print("\nReview reasons:", result.review_reasons or "none")
