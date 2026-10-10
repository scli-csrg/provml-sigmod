def local_witness(merkle_root: str) -> str:
    return f"local-witness:{merkle_root[:16]}"
