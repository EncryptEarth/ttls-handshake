import json
import hashlib

# === Simulated Verification (Public Only) ===
def verify_fdsig_output(message: bytes, privkey: bytes, expected_signature: bytes) -> bool:
    simulated = hashlib.sha3_512(privkey + message + privkey).digest()
    return simulated == expected_signature

# === Load Test Vectors ===
with open("fdsig_test_vectors.json", "r") as f:
    vectors = json.load(f)

# === Run Tests ===
failures = 0
for i, vector in enumerate(vectors):
    msg = bytes.fromhex(vector["message_hex"])
    key = bytes.fromhex(vector["privkey_hex"])
    sig = bytes.fromhex(vector["signature_hex"])
    
    if verify_fdsig_output(msg, key, sig):
        print(f"[✅] Vector {i+1} passed")
    else:
        print(f"[❌] Vector {i+1} failed")
        failures += 1

if failures == 0:
    print("\n[✅] All FDSig test vectors verified successfully.")
else:
    print(f"\n[❌] {failures} test vector(s) failed.")
