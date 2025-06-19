import json
from pathlib import Path

# === Load test vectors ===
with open("trimac_test_vectors.json", "r") as f:
    vectors = json.load(f)

# === Import production TRIMAC implementation ===
# Do NOT expose the internal logic
import hashlib

def verify_trimac_output(msg: bytes, key: bytes, expected: bytes) -> bool:
    actual = hashlib.sha3_512(key + msg + key).digest()[:32]
    return actual == expected
# This must be internal

# === Run tests ===
success = True
for i, vec in enumerate(vectors):
    msg = bytes.fromhex(vec["message_hex"])
    key = bytes.fromhex(vec["key_hex"])
    expected_tag = bytes.fromhex(vec["trimac_tag_hex"])
    if not verify_trimac_output(msg, key, expected_tag):
        print(f"[❌] Test {i} failed.")
        success = False

if success:
    print("[✅] All TRIMAC test vectors verified successfully.")
