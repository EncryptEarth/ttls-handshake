# TTLS Cryptographic Test Vectors

This folder contains verified, reproducible test vectors for components of the TTLS (Transformative TLS) protocol stack, developed by **Transformative Cryptography, LLC**.

## 📦 Included Vectors

| Component     | Description                          | Test Script                  | Public Logic? |
|---------------|--------------------------------------|------------------------------|----------------|
| ChaosHash     | 512-bit entropy-rich keystreams      | `test_chaos_hash_vectors.py` | ✅ Yes         |
| TRIMAC        | Triangular MAC (32-byte integrity)   | `test_trimac_vectors.py`     | ❌ Proprietary |
| FDSig         | Figurate Digital Signature           | `test_fdsig_vectors.py`      | ❌ Proprietary |
| LiteFire      | Figurate-based encryption cipher     | `test_litefire_vectors.py`   | ❌ Proprietary |
| TTLS Handshake| Public key exchange using hexagonal figurate base | `test_ttls_handshake_vectors.py` | ✅ Yes |

## ✅ Test Policy
All vectors pass verification with fully deterministic logic. Random seeds are included for cryptographic reproducibility and fuzz resistance.

## 🔒 Licensing
- ChaosHash and TTLS handshake logic are published for review and interoperability.
- TRIMAC, FDSig, and LiteFire are protected components under the commercial license below.
