# example_entropy_avalanche.py – Test Entropy and Avalanche of Chaos Hash

import hashlib
import secrets
from collections import Counter
import math

# === Chaos Hash Reference ===
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

# === Entropy Calculation ===
def calculate_entropy(byte_stream):
    length = len(byte_stream)
    freqs = Counter(byte_stream)
    probs = [count / length for count in freqs.values()]
    entropy = -sum(p * math.log2(p) for p in probs)
    return entropy

# === Avalanche Test ===
def avalanche_score(hash_func, base_input, length=512):
    original = hash_func(base_input, length)
    total_bits = len(original) * 8
    total_flips = 0
    trials = 0

    for i in range(len(base_input) * 8):  # Flip each bit
        flipped = bytearray(base_input)
        byte_index = i // 8
        bit_index = i % 8
        flipped[byte_index] ^= (1 << bit_index)

        new_output = hash_func(bytes(flipped), length)
        flips = sum(
            bin(b1 ^ b2).count('1') for b1, b2 in zip(original, new_output)
        )
        total_flips += flips
        trials += 1

    avg_flips = total_flips / trials
    return avg_flips, total_bits

# === Run Tests ===
if __name__ == "__main__":
    print("=== Chaos Hash: Entropy and Avalanche ===")
    test_input = secrets.token_bytes(64)
    output = chaos_hash_512_dynamic(test_input, 512)

    entropy = calculate_entropy(output)
    print(f"Entropy: {entropy:.5f} bits/byte (ideal is 8.0)")

    avg_flips, total_bits = avalanche_score(chaos_hash_512_dynamic, test_input, 512)
    print(f"Avalanche: {avg_flips:.2f} bit flips out of {total_bits} (~{(avg_flips/total_bits)*100:.2f}%)")
