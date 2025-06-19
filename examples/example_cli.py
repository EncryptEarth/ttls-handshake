# example_cli.py – Interactive TTLS Handshake Simulator (Public Demo)

import sys
import secrets
import hashlib

print("[🔐] Starting TTLS Handshake Simulator...")
mode = input("[⚙️] Select mode (HKE or F-KEM): ").strip().upper()
if mode not in ("HKE", "F-KEM"):
    print("[❌] Invalid mode. Choose 'HKE' or 'F-KEM'.")
    sys.exit(1)

# === NOTE: Proprietary modules replaced with placeholders ===
def litefire_encrypt(data, key):
    print("[🔒] Placeholder: Encrypting with proprietary LiteFire")
    return b'ENCRYPTED_' + data

def litefire_decrypt(data, key):
    print("[🔒] Placeholder: Decrypting with proprietary LiteFire")
    return data.replace(b'ENCRYPTED_', b'')

def generate_trimac(data, key):
    print("[🔒] Placeholder: Generating TRIMAC")
    return b'TRIMAC_TAG_64_BYTES'.ljust(64, b'\x00')

def verify_trimac(data, key, tag):
    print("[🔒] Placeholder: Verifying TRIMAC")
    return tag.startswith(b'TRIMAC_TAG')

def sign_data(data, key):
    print("[🔒] Placeholder: Signing data with FDSig")
    return b'FDSIG_SIGNATURE_64_BYTES'.ljust(64, b'\x00')

def verify_signature(data, key, signature):
    print("[🔒] Placeholder: Verifying FDSig")
    return signature.startswith(b'FDSIG_SIGNATURE')

# === HKE Functions ===
def hke_generate():
    p = 2**521 - 1
    F0 = 7
    x = secrets.randbelow(p)
    return x, pow(F0, x, p)

def hke_derive(pub, priv):
    p = 2**521 - 1
    s = pow(pub, priv, p)
    return s.to_bytes((s.bit_length() + 7) // 8, 'big').rjust(64, b'\x00')

# === F-KEM (Deterministic Placeholder) ===
def fkem_generate():
    return secrets.token_bytes(64), secrets.token_bytes(64)

def fkem_encapsulate(pub):
    capsule = secrets.token_bytes(64)
    shared = hashlib.sha3_512(capsule + pub).digest()
    return capsule, shared

def fkem_decapsulate(capsule, pub):
    return hashlib.sha3_512(capsule + pub).digest()

# === Handshake ===
if mode == "HKE":
    print("[1️⃣] Using Hexagonal Key Exchange")
    print("[🔑] Generating key pairs for Party A and B...")
    privA, pubA = hke_generate()
    privB, pubB = hke_generate()
    print("  A Public Key:", hex(pubA))
    print("  B Public Key:", hex(pubB))
    print("[🔄] Deriving shared secret...")
    sharedA = hke_derive(pubB, privA)
    sharedB = hke_derive(pubA, privB)
    assert sharedA == sharedB, "[❌] Shared secrets do not match!"
    shared = sharedA

elif mode == "F-KEM":
    print("[1️⃣] Using Figurate KEM")
    print("[🔐] Generating recipient's key pair...")
    privB, pubB = fkem_generate()
    print("  Public Key:", pubB.hex())
    print("[📦] Encapsulating shared secret for transmission...")
    capsule, sharedA = fkem_encapsulate(pubB)
    print("  Capsule:", capsule.hex())
    print("[🔓] Recipient decapsulating shared secret...")
    sharedB = fkem_decapsulate(capsule, pubB)
    assert sharedA == sharedB, "[❌] Shared secrets do not match!"
    shared = sharedA

print("[✔] Shared Secret Established:", shared.hex())

# === Secure Message Exchange ===
print("\n[✉️ ] Secure Message Exchange Begins")
message = input("Enter message to encrypt: ").encode()
print("[🔐] Encrypting message...")
encrypted = litefire_encrypt(message, shared)
print("[🔏] Generating TRIMAC...")
tag = generate_trimac(encrypted, shared)
print("[✍️ ] Signing with FDSig...")
sig = sign_data(encrypted, shared[:32])

print("\n--- Transmission Payload ---")
print("Encrypted Message (hex):", encrypted.hex())
print("TRIMAC Tag:", tag.hex())
print("FDSig Signature:", sig.hex())

# === Decryption & Verification ===
print("\n[🔎] Verifying TRIMAC and Signature before decrypting...")
if verify_trimac(encrypted, shared, tag) and verify_signature(encrypted, shared[:32], sig):
    print("[✅] Integrity and authenticity verified.")
    decrypted = litefire_decrypt(encrypted, shared)
    print("[📥] Decrypted Message:", decrypted.decode())
else:
    print("[❌] Verification failed. Message may have been tampered with.")
