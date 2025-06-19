import json
import hashlib

# === Simulated LiteFire Verifier (public-facing only) ===
def verify_litefire_output(plaintext: bytes, key: bytes, expected_ciphertext: bytes) -> bool:
    # Simulated transformation (not real encryption logic)
    combined = bytearray()
    for i in range(len(plaintext)):
        b = plaintext[i]
        k = key[i % len(key)]
        fake = (b + k + (i * 17 % 251)) % 256
        combined.append(fake)
    return bytes(combined) == expected_ciphertext

# === Load Test Vectors ===
with open("litefire_test_vectors.json", "r") as f:
    vectors = json.load(f)

# === Run Tests ===
failures = 0
for i, vector in enumerate(vectors):
    msg = bytes.fromhex(vector["plaintext_hex"])
    key = bytes.fromhex(vector["key_hex"])
    cipher = bytes.fromhex(vector["ciphertext_hex"])
    
    if verify_litefire_output(msg, key, cipher):
        print(f"[✅] Vector {i+1} passed")
    else:
        print(f"[❌] Vector {i+1} failed")
        failures += 1

if failures == 0:
    print("\n[✅] All LiteFire test vectors verified successfully.")
else:
    print(f"\n[❌] {failures} test vector(s) failed.")
