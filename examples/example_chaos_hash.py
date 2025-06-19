import hashlib
from collections import Counter

# === Public Chaos Hash ===

def chaos_hash_512_dynamic(data, length, cpn=None):
    if isinstance(data, str):
        data = data.encode("utf-8", errors="ignore")
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

# === Generate and Analyze ===

input_data = "TTLS_KEY_SEED"
stream_length = 4096
chaos_output = chaos_hash_512_dynamic(input_data, stream_length)

print(f"[✓] Chaos stream generated: {len(chaos_output)} bytes")
print(f"[ℹ] Unique byte values: {len(set(chaos_output))}/256")

# Basic byte frequency without NumPy
freqs = Counter(chaos_output)
top = freqs.most_common(10)
print("\n[🔍] Top 10 byte frequencies:")
for byte_val, count in top:
    print(f"Byte {byte_val:3}: {count} times")

print("\n[HEX] Preview of first 64 bytes:")
print(chaos_output[:64].hex())
