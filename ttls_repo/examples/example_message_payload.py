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

# === TTLS Message Creation ===

print("\n[TTLS One-Way Encrypted Message Demo]")

message = b"Transmit backup codes via secure drop at 0400Z."
passphrase = b"paradigm7"

# Derive a chaos-based encryption key
key = chaos_hash_512_dynamic(passphrase, length=len(message))

# === Simulate encryption ===
# We do not reveal LiteFire internals, so we fake this step
simulated_encrypted = b"\xB7\x2C\x14..."  # Example placeholder

# Simulate TRIMAC tag generation
simulated_trimac = b"\x8E\x51\xA0..."  # Placeholder

# Simulate optional signature
simulated_signature = b"\xDF\xC4\x32..."  # Placeholder

# Package message blob
print("[✓] Message encrypted.")
print(f"[✓] Encrypted (hex): {simulated_encrypted.hex()[:48]}...")
print(f"[✓] TRIMAC tag: {simulated_trimac.hex()[:32]}...")
print(f"[✓] Signature: {simulated_signature.hex()[:32]}...")

# (Optional) Save to disk or send via QR, NFC, or text
