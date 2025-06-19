# example_message.py – Simulated Secure TTLS Message Exchange (Public Safe)

import secrets
import hashlib

print("[🔐] Simulated Secure Message via TTLS")
mode = "HKE"  # Set to "F-KEM" to switch modes manually

# === Placeholder Secure Modules ===
def litefire_encrypt(data, key):
    print("[🔒] Placeholder encryption with LiteFire")
    return b'ENCRYPTED_' + data

def litefire_decrypt(data, key):
    print("[🔓] Placeholder decryption with LiteFire")
    return data.replace(b'ENCRYPTED_', b'')

def generate_trimac(data, key):
    print("[🔏] Generating stand-in TRIMAC (not real logic)")
    return hashlib.sha3_512(key + data).digest()

def verify_trimac(data, key, tag):
    return tag == hashlib.sha3_512(key + data).digest()

def sign_data(data, key):
    print("[🖋️] Generating stand-in FDSig signature")
    return hashlib.sha3_512(key + b"FDSIG" + data).digest()

def verify_signature(data, key, sig):
    return sig == hashlib.sha3_512(key + b"FDSIG" + data).digest()

# === HKE Logic ===
def hke_generate():
    p = 2**521 - 1
    F0 = 7
    x = secrets.randbelow(p)
    return x, pow(F0, x, p)

def hke_derive(pub, priv):
    p = 2**521 - 1
    shared = pow(pub, priv, p)
    return shared.to_bytes((shared.bit_length() + 7) // 8, 'big').rjust(64, b'\x00')

# === F-KEM Logic ===
def fkem_generate():
    return secrets.token_bytes(64), secrets.token_bytes(64)

def fkem_encapsulate(pub):
    capsule = secrets.token_bytes(64)
    shared = hashlib.sha3_512(capsule + pub).digest()
    return capsule, shared

def fkem_decapsulate(capsule, pub):
    return hashlib.sha3_512(capsule + pub).digest()

# === Key Agreement ===
if mode == "HKE":
    print("[HKE] Generating TTLS keys...")
    privA, pubA = hke_generate()
    privB, pubB = hke_generate()
    sharedA = hke_derive(pubB, privA)
    sharedB = hke_derive(pubA, privB)
    assert sharedA == sharedB, "[❌] HKE shared secrets mismatch"
    shared = sharedA
    print("[✔] Shared Secret (HKE):", shared.hex())

elif mode == "F-KEM":
    print("[F-KEM] Encapsulating key exchange...")
    privB, pubB = fkem_generate()
    capsule, sharedA = fkem_encapsulate(pubB)
    sharedB = fkem_decapsulate(capsule, pubB)
    assert sharedA == sharedB, "[❌] F-KEM shared secrets mismatch"
    shared = sharedA
    print("[✔] Shared Secret (F-KEM):", shared.hex())

# === Secure Message Transmission ===
print("\n[✉️] Simulating Message Transmission")
plaintext = b"Confidential message payload via TTLS secure channel."
print("Original Message:", plaintext.decode())

ciphertext = litefire_encrypt(plaintext, shared)
tag = generate_trimac(ciphertext, shared)
sig = sign_data(ciphertext, shared[:32])

print("\n[📦] Transmitting...")
print("Encrypted (hex):", ciphertext.hex())
print("TRIMAC:", tag.hex())
print("Signature:", sig.hex())

print("\n[🔍] Verifying at receiver...")
if verify_trimac(ciphertext, shared, tag) and verify_signature(ciphertext, shared[:32], sig):
    print("[✅] Message integrity and authenticity verified.")
    decrypted = litefire_decrypt(ciphertext, shared)
    print("[📥] Decrypted Message:", decrypted.decode())
else:
    print("[❌] Verification failed. Message may be tampered.")
