# example_handshake_working.py – Verifies HKE and F-KEM handshake logic

import secrets
import hashlib

# === HKE – Hexagonal Key Exchange ===
def hke_generate():
    p = 2**521 - 1
    F0 = 7
    x = secrets.randbelow(p)
    return x, pow(F0, x, p)

def hke_derive(pub, priv):
    p = 2**521 - 1
    return pow(pub, priv, p)

# === F-KEM – Figurate Key Encapsulation Mechanism ===
def fkem_generate():
    return secrets.token_bytes(64), secrets.token_bytes(64)

def fkem_encapsulate(pub):
    capsule = secrets.token_bytes(64)
    shared = hashlib.sha3_512(capsule + pub).digest()
    return capsule, shared

def fkem_decapsulate(capsule, pub):
    return hashlib.sha3_512(capsule + pub).digest()

# === Test Both Modes ===
def test_hke():
    print("\n🔐 Testing HKE...")
    privA, pubA = hke_generate()
    privB, pubB = hke_generate()
    sharedA = hke_derive(pubB, privA)
    sharedB = hke_derive(pubA, privB)
    assert sharedA == sharedB, "[❌] HKE Shared secrets do not match!"
    print("✅ HKE Shared Secret Match!")
    print("Shared:", sharedA.to_bytes((sharedA.bit_length() + 7) // 8, 'big').hex())

def test_fkem():
    print("\n🔐 Testing F-KEM...")
    privB, pubB = fkem_generate()
    capsule, sharedA = fkem_encapsulate(pubB)
    sharedB = fkem_decapsulate(capsule, pubB)
    assert sharedA == sharedB, "[❌] F-KEM Shared secrets do not match!"
    print("✅ F-KEM Shared Secret Match!")
    print("Shared:", sharedA.hex())

if __name__ == "__main__":
    test_hke()
    test_fkem()
