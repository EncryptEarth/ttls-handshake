import json
import hashlib

def chaos_hash_512_dynamic(data, length, cpn=None):
    if isinstance(data, str):
        data = data.encode('utf-8', errors='ignore')
    base = hashlib.sha3_512(data).digest()
    chaotic = bytearray(base)
    if cpn:
        for i in range(min(len(cpn), len(chaotic))):
            chaotic[i] ^= cpn[i]
    while len(chaotic) < length:
        i = len(chaotic)
        feedback = chaotic[i - 1] if i > 0 else chaotic[-1]
        new_byte = (base[i % 64] ^ (i * 13 % 251) ^ ((i * i + feedback) % 251)) & 0xFF
        chaotic.append(new_byte)
    return bytes(chaotic[:length])

# Load JSON test vectors
with open("chaos_hash_test_vectors.json", "r") as f:
    vectors = json.load(f)

# Verify
for i, vec in enumerate(vectors):
    msg = bytes.fromhex(vec["input_hex"])
    cpn = bytes.fromhex(vec["cpn_hex"])
    expected = bytes.fromhex(vec["output_hex"])
    actual = chaos_hash_512_dynamic(msg, 128, cpn)
    if actual != expected:
        print(f"[❌] Mismatch at index {i}")
        break
else:
    print("[✅] All chaos hash test vectors verified successfully.")
