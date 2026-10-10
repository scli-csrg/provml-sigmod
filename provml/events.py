from __future__ import annotations
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from .canon import canon_event, REQUIRED_CERTS, DOMAIN_TAGS
from .commitment import event_commitment

@dataclass
class Artifact:
    hash: str
    type: str
    role: str
    size: int = 0

@dataclass
class Event:
    type: str
    actor: str
    inputs: List[Artifact]
    outputs: List[Artifact]
    env: Dict[str, Any] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    policy_context: Dict[str, Any] = field(default_factory=dict)
    certificates: List[Dict[str, Any]] = field(default_factory=list)
    parents: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    seq: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sig: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["inputs"]  = [asdict(a) for a in self.inputs]
        d["outputs"] = [asdict(a) for a in self.outputs]
        return d

    def validate_schema(self) -> None:
        if self.type not in DOMAIN_TAGS:
            raise ValueError(f"Unknown event type: {self.type}")
        required = REQUIRED_CERTS.get(self.type, set())
        provided = {c.get("kind") for c in self.certificates}
        missing = required - provided
        if missing:
            raise ValueError(f"{self.type} missing certificates: {missing}")

    def sign(self, sk: Ed25519PrivateKey) -> None:
        self.sig = sk.sign(canon_event(self.to_dict())).hex()

    def verify(self, pk: Ed25519PublicKey) -> bool:
        if self.sig is None or pk is None:
            return False
        try:
            pk.verify(bytes.fromhex(self.sig), canon_event(self.to_dict()))
        except Exception:
            return False
        return True

    @property
    def commitment(self) -> str:
        return event_commitment(self.to_dict())
