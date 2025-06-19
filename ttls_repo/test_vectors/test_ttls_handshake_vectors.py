import json

# === Load Test Vectors ===
with open("ttls_handshake_test_vectors.json", "r") as f:
    vectors = json.load(f)

# === Run Test ===
passed = 0
for i, v in enumerate(vectors):
    p = int(v["p_hex"], 16)
    F0 = v["F0"]
    x = int(v["private_a_hex"], 16)
    y = int(v["private_b_hex"], 16)
    P_a = pow(F0, x, p)
    P_b = pow(F0, y, p)
    S_a = pow(P_b, x, p)
    S_b = pow(P_a, y, p)

    if S_a == S_b:
        print(f"[✅] Vector {i} passed")
        passed += 1
    else:
        print(f"[❌] Vector {i} failed")

print(f"\n[🏁] {passed} / {len(vectors)} vectors passed")
