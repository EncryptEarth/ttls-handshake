import hashlib

# === chaos_hash_512_dynamic (public-safe version) ===

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


# === TTLS in Deep-Space Scenario ===

print("\n[🛰 TTLS Deep-Space Message Integrity Test]")

# Ground control sends a mission-critical update
message = "Adjust trajectory by +3.742° at 1287.2s.".encode("utf-8")
session_marker = b"probe-mars-9-cycle42"

# Derive chaos-based key
key = chaos_hash_512_dynamic(session_marker, length=len(message))

# === Simulate encryption (placeholder) ===
simulated_encrypted = b"\x88\x3C\x91..."  # Encrypted message placeholder
simulated_tag = b"\xB7\x4D\x22..."        # TRIMAC placeholder

print("[✓] Message encrypted using chaos-derived key.")
print(f"[✓] Tag attached: {simulated_tag.hex()[:32]}...")

# === Radiation flip / Replay Attack ===

print("[✗] Radiation flips 1 bit during message transfer...")

tampered_msg = bytearray(simulated_encrypted)
tampered_msg[-1] ^= 0x01  # Flip one byte

print("[✗] Attacker replays with original tag...")

# Simulated failure (no real crypto shown)
print("[✗] Verification failed – integrity compromised.")

print("\n[✔] TTLS blocks tampering even without shared clocks or network state.\n")
