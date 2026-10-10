from __future__ import annotations
import hashlib, json
from typing import Any

DOMAIN_TAGS = {
    "Acquire":  "provml:v1:acquire",
    "Train":    "provml:v1:train",
    "Compile":  "provml:v1:compile",
    "Package":  "provml:v1:package",
    "Load":     "provml:v1:load",
    "Deploy":   "provml:v1:deploy",
    "Ingest":   "provml:v1:ingest",
    "Embed":    "provml:v1:embed",
    "Index":    "provml:v1:index",
    "Retrieve": "provml:v1:retrieve",
    "Generate": "provml:v1:generate",
}

REQUIRED_CERTS = {
    "Compile":  {"compiler_hash", "flags", "post_compile_equivalence"},
    "Load":     {"safe_loader_contract", "import_trace"},
    "Deploy":   {"policy_version"},
    "Ingest":   {"corpus_manifest"},
    "Retrieve": {"index_version"},
    "Generate": {"retrieved_chunks", "model_commitment"},
}

def canonicalize(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")

def canon_event(event: dict) -> bytes:
    tag = DOMAIN_TAGS[event["type"]]
    body = {k: v for k, v in event.items() if k != "id"}
    return tag.encode("utf-8") + b"\x00" + canonicalize(body)

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def hexdigest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
