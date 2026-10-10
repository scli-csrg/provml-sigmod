# ProvML

Reference implementation, policies, and evaluation datasets for
**ProvML: Policy-Enforced, Tamper-Evident Provenance for Machine-Learning Supply Chains**.

## Quick start
```bash
pip install -r requirements.txt
pip install -e .
pytest -q tests/
python -m eval.harness
python -m eval.scaling
