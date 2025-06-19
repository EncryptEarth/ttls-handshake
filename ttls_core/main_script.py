import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import hashlib

# === Import sealed functions (compiled .pyd via sealed.py) ===
from sealed import (
    trimac_tag,
    sample_trimac_input,
    litefire_encrypt,
    litefire_decrypt,
    fdsig_sign,
    fdsig_verify
)

# === Public chaos_hash_512_dynamic ===
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

# === Hexagonal Key Exchange Utilities ===
def hexagonal(n):
    return n * (2 * n - 1)

def generate_public_key(base: int, private_exponent: int, prime: int) -> int:
    return pow(hexagonal(base), private_exponent, prime)

def compute_shared_secret(their_pub: int, my_private: int, prime: int) -> bytes:
    shared = pow(their_pub, my_private, prime)
    return chaos_hash_512_dynamic(str(shared).encode(), 64)

# === TTLS Handshake ===
def ttls_handshake(my_private: int, their_pub: int, base: int, prime: int, auth_data: bytes, passphrase: str):
    key_material = compute_shared_secret(their_pub, my_private, prime)
    signature = fdsig_sign(auth_data, key_material)
    tag = trimac_tag(auth_data, key_material)
    encrypted = litefire_encrypt(auth_data, key_material)
    return {
        'encrypted': encrypted,
        'tag': tag,
        'signature': signature
    }

def ttls_receive(my_private: int, their_pub: int, base: int, prime: int, packet: dict):
    key_material = compute_shared_secret(their_pub, my_private, prime)
    decrypted = litefire_decrypt(packet['encrypted'], key_material)
    if trimac_tag(decrypted, key_material) != packet['tag']:
        raise ValueError("TRIMAC verification failed")
    if not fdsig_verify(decrypted, packet['signature'], key_material):
        raise ValueError("FDSig verification failed")
    return decrypted

# === Quick test ===
if __name__ == "__main__":
    print("✅ TTLS core loaded and ready")
