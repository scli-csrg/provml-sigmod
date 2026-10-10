from __future__ import annotations
from typing import Iterable, List
from .canon import canon_event, sha256, hexdigest

def _merkle_root(leaves: List[bytes]) -> bytes:
    if not leaves:
        return sha256(b"")
    layer = list(leaves)
    while len(layer) > 1:
        if len(layer) % 2:
            layer.append(layer[-1])
        layer = [sha256(layer[i] + layer[i+1]) for i in range(0, len(layer), 2)]
    return layer[0]

def hash_list(items: Iterable[bytes]) -> bytes:
    return _merkle_root(list(items))

def event_commitment(event: dict) -> str:
    canon = canon_event(event)
    h_in  = hash_list(bytes.fromhex(a["hash"]) for a in event["inputs"])
    h_out = hash_list(bytes.fromhex(a["hash"]) for a in event["outputs"])
    h_par = hash_list(bytes.fromhex(p) for p in event["parents"])
    return hexdigest(canon + h_in + h_out + h_par)

def batch_merkle_root(commitments: List[str]) -> str:
    return hexdigest(_merkle_root([bytes.fromhex(c) for c in commitments]))
