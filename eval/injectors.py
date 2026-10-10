import copy, hashlib, random
from typing import Dict

def inject_missing(run):
    out = copy.deepcopy(run)
    if len(out["events"]) > 1:
        out["events"].pop(random.randrange(len(out["events"])))
    out["injected"] = "missing"; out["expected"] = "REJECT"; return out

def inject_mismatched(run):
    out = copy.deepcopy(run)
    for ev in out["events"]:
        if ev["inputs"]:
            ev["inputs"][0]["hash"] = hashlib.sha256(b"tampered").hexdigest(); break
    out["injected"] = "mismatched"; out["expected"] = "REJECT"; return out

def inject_replayed(run):
    out = copy.deepcopy(run)
    if out["events"]: out["events"].append(copy.deepcopy(out["events"][0]))
    out["injected"] = "replayed"; out["expected"] = "REJECT"; return out

def inject_forged(run):
    out = copy.deepcopy(run)
    for ev in out["events"]:
        if ev["certificates"]:
            ev["certificates"][0]["issuer"] = "unlisted-ca"; break
    out["injected"] = "forged"; out["expected"] = "REJECT"; return out

INJECTORS = {"missing": inject_missing, "mismatched": inject_mismatched,
             "replayed": inject_replayed, "forged": inject_forged}
