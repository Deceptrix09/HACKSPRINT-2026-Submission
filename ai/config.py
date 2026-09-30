"""Settings for the AI module. Values come from the .env file."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
GCP_PROJECT = os.getenv("GCP_PROJECT", "")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
CRITICAL_MIN_CONFIDENCE = 0.8
PROMPT_PATH = ROOT / "ai" / "prompts" / "fuse_triage.txt"
SOP_PATH = ROOT / "data" / "sop" / "triage_rules.txt"
