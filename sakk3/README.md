<div align="center">

# 🛡️ SAKK (صَكّ)
### Decentralized Cryptographic Document Verification Platform
> **Zero-Retention, Tamper-Proof Document Authentication for Sovereign Digital Governments.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Cryptography-ECDSA_SECP256R1-success.svg)](#)
[![Computer Vision](https://img.shields.io/badge/CV-OpenCV_%7C_PyMuPDF-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](#)

*An elite submission for the **Global SAFE Security and Innovation Competition** (Digital Government Solutions Track).*

</div>

---

## 🌟 Executive Summary

**SAKK** is a state-of-the-art cryptographic document verification platform designed for sovereign digital governance. In an era where physical and digital document forgery (land deeds, security clearances, academic certificates) poses severe national security and economic threats, SAKK provides absolute mathematical certainty.

By utilizing advanced **ECDSA (SECP256R1)** elliptic-curve cryptography combined with a strict **Zero-Retention architecture**, SAKK guarantees document integrity without ever storing sensitive data on centralized servers. The cryptographic proof travels with the document itself via a secure, transparent QR seal.

## 🚀 The Competitive Edge (Why SAKK?)

* 🔐 **Zero-Retention Privacy:** SAKK explicitly distrusts central data storage. It does not store uploaded documents or their metadata in any database. The data is cryptographically sealed directly into the physical/digital QR code. This ensures absolute compliance with strict data protection laws (e.g., PDPL, GDPR).
* 🛡️ **Cryptographic Tamper Detection:** If a malicious actor alters a single pixel, date, or character in the document, the cryptographic hash breaks instantly, and the system rejects the document.
* ⚡ **Decentralized Inter-Agency Verification:** A bank, foreign embassy, or court can instantly verify a government-issued document using only the issuer's public key. No complex API integrations or access to sensitive internal databases is required!
* 📄 **Multi-Page Intelligent Scanning:** Built-in AI/Computer Vision pipeline using `PyMuPDF` and `OpenCV` to automatically hunt and decode secure QR seals across large, multi-page PDFs.
* 🪄 **Transparent Aesthetic Seals:** Generates transparent, elegant QR codes that blend seamlessly into official documents without ruining their sovereign aesthetic or obscuring important text.
* 📱 **Multi-Engine Decoding Pipeline:** Engineered with a highly robust fallback chain (`pyzbar` → `cv2.wechat_qrcode` → `cv2.QRCodeDetector`) ensuring flawless scanning even on low-quality physical prints or dense digital codes.
* 🔑 **Multi-Factor Authentication (OTP):** Government issuers are protected by an OTP-based login system to prevent unauthorized document sealing.

---

## 🏗️ System Architecture & Cryptographic Workflow

SAKK operates on a **Zero-Trust** model. The server explicitly distrusts the uploaded file during verification and relies solely on mathematical proof.

### Phase 1: Document Issuance (The Cryptographic Binding)
1. **Hash Generation:** The system calculates a mathematically irreversible SHA-256 hash of the raw document file.
2. **Dynamic Metadata:** Custom key-value pairs (e.g., `Issuer: Ministry of Interior`, `Clearance Level: Top Secret`, `Date: 2026`) are canonically sorted and appended to the hash payload.
3. **ECDSA Signature:** The server signs the entire payload using its highly secure Elliptic Curve Private Key (`SECP256R1`).
4. **Seal Creation:** A transparent, branded QR code is generated containing the payload, hash, and signature. This seal is embedded into the document.

### Phase 2: Document Verification (Zero-Trust Proof)
1. **Upload / Scan:** A third party (e.g., a bank) uploads the physical scan or digital PDF to the portal.
2. **Extraction:** The AI vision pipeline scans the document, locates the QR code, and extracts the payload and signature.
3. **Re-Hashing:** The system automatically re-hashes the uploaded file (excluding the QR seal region) and compares it to the original hash in the payload.
4. **Mathematical Verification:** Using the Issuer's Public Key, the system cryptographically verifies that the signature was created by the trusted authority and that the document has not been tampered with.

---

## 📂 Repository Structure

```text
sakk3/
│
├── app.py                  # Core backend application (Flask, Cryptography, CV pipelines)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation (You are here)
│
├── templates/              # Frontend Glassmorphism UI
│   ├── index.html          # Main portal (Upload, Sign, Verify, Dashboard)
│   └── verify.html         # Public verification page
│
├── sakk.db                 # SQLite DB (Generated at runtime - Audit logs only)
├── private_key.pem         # ECDSA Private Key (Generated at runtime - DO NOT COMMIT!)
└── scratch/                # Development scratchpad and end-to-end tests
    └── test_meta.py        # Automated cryptographic binding tests
```

---

## 🛠️ Technology Stack

| Domain | Technology / Library |
|---|---|
| **Backend Framework** | Python 3.10+, Flask |
| **Cryptography** | `cryptography` (SECP256R1, SHA-256) |
| **Document Processing** | `PyMuPDF` (fitz), `Pillow` (PIL) |
| **Computer Vision** | `OpenCV` (cv2), `pyzbar` |
| **Frontend UI/UX** | HTML5, CSS3 (Glassmorphism), Vanilla JS |
| **Database** | SQLite (Strictly for Audit Logs & Public Keys) |

---

## ⚙️ Installation & Configuration

### Prerequisites
- Python 3.10 or higher
- Git

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/sakk.git
   cd sakk
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   *The system will automatically generate the SQLite database (`sakk.db`) and the ECDSA `private_key.pem` upon first execution.*

5. **Access the portal:**
   Open your browser and navigate to `http://127.0.0.1:5000`.

### ⚠️ Critical Security Notice
**NEVER commit `private_key.pem` or `sakk.db` to GitHub!** 
Ensure your `.gitignore` is properly configured to exclude these sensitive files. If the private key is compromised, the entire trust model of the system is broken.

---

## 🔌 API Reference (Core Endpoints)

- `POST /api/sign`: Accepts a file and dynamic metadata, hashes the content, signs it via ECDSA, and returns a secure transparent QR code seal.
- `POST /api/verify-qr`: Accepts a file (PDF/Image), uses OpenCV/PyMuPDF to locate the QR seal, extracts the payload, and cryptographically verifies document integrity.
- `POST /api/verify-qr-data`: Accepts raw QR payload data (e.g., from a mobile camera scan) for instant validation.
- `POST /api/login`: Secure issuer login utilizing Multi-Factor Authentication (OTP).

---

## 🗺️ Future Roadmap
- [ ] **Blockchain Anchoring:** Anchor daily Merkle roots of audit logs to a public blockchain (e.g., Ethereum/Polygon) for absolute historical immutability.
- [ ] **Hardware Security Module (HSM):** Integrate with physical HSMs or cloud KMS (AWS/GCP) to protect the private keys at a hardware level.
- [ ] **Mobile App:** Dedicated iOS/Android scanner application for on-the-go physical document verification by law enforcement or border control.

---

## 🏆 Global SAFE Competition Profile

* **Track:** Digital Government Solutions (الحلول الرقمية الحكومية)
* **Core Value Proposition:** 
  1. Eradicates physical and digital document forgery instantly.
  2. Eliminates centralized "honeypot" data breaches by utilizing Zero-Retention cryptography.
  3. Enables seamless, trustless interoperability between isolated government agencies and the private sector.

---
<div align="center">
<i>Architected with mathematical precision for a safer, trustless digital future.</i><br>
<b>Global SAFE Security and Innovation Competition</b>
</div>
