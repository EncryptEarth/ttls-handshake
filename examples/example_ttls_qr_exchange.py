import hashlib

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

# === Key Exchange Setup (Simulated) ===

print("\n[TTLS Offline QR Key Exchange]")

# Shared session entropy
session_phrase = "OPS_RELAY:7462"  # Can be exchanged via QR code or typed

# Simulate Alice and Bob both use the same session phrase
alice_secret = b"Alice_private_value_7"
bob_secret = b"Bob_private_value_3"

# Generate public exchange values (simulate QR encoding)
F0 = 5  # Fixed generator
p = 104729  # Example prime modulus (small for demo)

# Compute public components
alice_pub = pow(F0, int.from_bytes(alice_secret, "big"), p)
bob_pub = pow(F0, int.from_bytes(bob_secret, "big"), p)

print(f"Alice sends QR with public key: {hex(alice_pub)}")
print(f"Bob sends QR with public key:   {hex(bob_pub)}")

# === Shared Secret Agreement ===

alice_shared = pow(bob_pub, int.from_bytes(alice_secret, "big"), p)
bob_shared = pow(alice_pub, int.from_bytes(bob_secret, "big"), p)

assert alice_shared == bob_shared
print(f"\n[✓] Shared TTLS secret (hex): {hex(alice_shared)}")

# === Chaos key derived from shared secret ===

session_key = chaos_hash_512_dynamic(str(alice_shared), 64)
print(f"[✓] Derived chaos session key (64 bytes):\n{session_key.hex()[:64]}...")
