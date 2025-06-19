TTLS is fully testable and reproducible.
The core handshake and hash are open and source-available.
Our encryption and MAC layers are private IP designed for enterprise and post-quantum use.
Commercial access is available via Transformative Cryptography, LLC.

## 🛡️ TTLS: Transformative TLS

**TTLS** is a post-quantum-ready cryptographic handshake built for **secure, offline, certificate-free communication**.

It offers:

* 🔐 **No certificates**
* 📡️ **No clock sync**
* 🚀 **No internet required**
* ✅ **No external trust anchors**

TTLS works anywhere — from embedded devices to deep-space transmissions — with provable entropy, integrity, and tamper resistance.

---

## 📀 Who Should Use TTLS

* Developers building offline-first systems
* Privacy-focused platforms needing trustless crypto
* Satellite and mesh network engineers
* Zero-trust security architects
* Embedded and IoT device makers

---

## 🔍 What’s in This Repo

This repository includes the **open-source personal-use version** of TTLS:

* ✅ Public handshake logic
* ↻ Hexagonal figurate key exchange (HKE)
* 🤖 Chaos-based key derivation
* 🧪 Entropy & avalanche test vectors
* 📁 Functional usage examples

> The **core encryption (LiteFire), MAC (TRIMAC), and digital signature (FDSig)** systems are sealed and compiled, included as binaries only.

---

## 🚫 Personal Use License Only

This version is licensed for **personal, educational, and non-commercial** use only.

To use TTLS in:

* A commercial product
* Any monetized platform or enterprise environment

👉 You must purchase a license from **Transformative Cryptography, LLC**.

See: [`LICENSE.md`](LICENSE.md) | [`COMMERCIAL_LICENSE.md`](COMMERCIAL_LICENSE.md)

---

## 🧠 Why TTLS is Different

| Feature                  | TTLS                        | TLS / DTLS / Noise |
| ------------------------ | --------------------------- | ------------------ |
| Certificate-Free         | ✅ Yes                       | ❌ No               |
| Offline Key Exchange     | ✅ Yes                       | ❌ No               |
| Post-Quantum Ready       | ✅ Yes (no RSA/ECC)          | ⚠️ Some variants   |
| Encrypted Core Functions | ✅ Binary-only IP modules    | ❌ Fully exposed    |
| Avalanche-Verified MAC   | ✅ TRIMAC                    | ❌ Poly1305/HMAC    |
| Usable in Space / IoT    | ✅ Yes                       | ❌ Complex overhead |
| Replay-Proof             | ✅ Stateless & deterministic | ⚠️ Session-based   |

---

## 💼 Contact for Licensing

**Transformative Cryptography, LLC**
📧 [closedeyerony@gmail.com]
📞 1-423-488-8186

Let’s build trustless communication that works everywhere.
