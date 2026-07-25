<div align="center">

# 🔐 A Layered Encryption for Document Sharing

### Secure File Transfer Platform using Flask, Multi-Layer Encryption & Dual-Channel Key Delivery

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask">
<img src="https://img.shields.io/badge/Security-Cryptography-red?style=for-the-badge">
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">

---

**A secure document sharing platform implementing Fernet, AES, and Triple DES encryption with dual-channel SMTP key delivery, secure authentication, encrypted storage, and in-memory decryption.**

</div>

---

# 📖 Overview

Modern file-sharing platforms often expose sensitive information by transmitting encrypted files and their decryption keys through the same communication channel. This creates a single point of failure that attackers can exploit.

This project introduces a **Flask-based Secure File Transfer Platform** that separates encrypted files from their decryption keys using a **Dual-Channel Security Architecture**.

- 📁 Files are encrypted before storage.
- 🔑 Decryption keys are delivered separately through secure email (SMTP over TLS).
- 🔒 Only authenticated users can send or receive files.
- 💾 No decryption keys are stored on the server.
- 🛡️ Files are decrypted securely in memory without creating plaintext copies on disk.

---

# ✨ Features

### 🔐 Multi-LLayer Encryption

Supports multiple encryption algorithms:

- Fernet (Recommended)
- AES
- Triple DES (3DES)

---

### 👤 Secure Authentication

- User Registration
- Secure Login
- Password Hashing
- Session Management using Flask-Login
- Protected Routes

---

### 📂 Secure File Upload

- Upload Images & PDF Documents
- File Validation
- File Size Validation
- Random Encryption Key Generation
- Secure Ciphertext Storage

---

### 📧 Dual-Channel Security

Instead of sending both the encrypted file and the decryption key together:

✔ Encrypted File → Stored on Server

✔ Decryption Key → Sent separately through Gmail SMTP over TLS

This greatly improves confidentiality even if server storage is compromised.

---

### 🔓 Secure Decryption

Recipients can

- View received encrypted files
- Enter the received key
- Perform secure in-memory decryption
- Download original documents safely

---

### 📊 Performance Evaluation

Encryption performance comparison for:

- Fernet
- AES
- Triple DES

Across different file sizes.

---

# 🏗️ System Architecture

```
                User Login
                     │
                     ▼
          User Authentication
                     │
                     ▼
            Upload Secure File
                     │
                     ▼
        Select Encryption Algorithm
                     │
                     ▼
             Encryption Engine
        (Fernet / AES / Triple DES)
               │            │
               │            │
               ▼            ▼
     Encrypted File     Encryption Key
           │                  │
           ▼                  ▼
   Secure Server        Gmail SMTP (TLS)
       Storage          Secure Email Delivery
           │                  │
           └────────────┬─────┘
                        ▼
               Recipient Login
                        │
                        ▼
             Secure In-Memory Decryption
                        │
                        ▼
                Download Original File
```

---

# 🚀 Technologies Used

## Backend

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy

## Database

- SQLite

## Cryptography

- Fernet
- AES
- Triple DES (3DES)
- Cryptography Library
- PyCryptodome

## Communication

- Gmail SMTP
- TLS Encryption

## Frontend

- HTML
- CSS
- Bootstrap
- Jinja Templates

---

# 🔒 Encryption Algorithms

| Algorithm | Security | Performance |
|------------|----------|-------------|
| Fernet | High | ⭐ Fast |
| AES | Very High | ⭐⭐ Moderate |
| Triple DES | Medium | ⭐⭐⭐ Slow |

---

# 📈 Performance Results

| File Size | Fernet | AES | Triple DES |
|------------|---------|---------|------------|
| 1 MB | 0.15 s | 0.18 s | 0.25 s |
| 5 MB | 0.62 s | 0.75 s | 1.15 s |
| 10 MB | 1.20 s | 1.50 s | 2.30 s |

### Performance Summary

- ✅ Fernet achieved the fastest encryption and decryption.
- ✅ AES provides an excellent balance between security and speed.
- ✅ Triple DES offers stronger legacy compatibility but slower execution.

---

# 🔄 Workflow

1. User registers and logs in.
2. Sender searches for a recipient.
3. Uploads a file.
4. Selects an encryption algorithm.
5. File is encrypted.
6. Ciphertext is stored securely.
7. Random encryption key is generated.
8. Key is emailed securely using Gmail SMTP over TLS.
9. Recipient logs in.
10. Downloads encrypted file.
11. Enters the received key.
12. File is decrypted securely in memory.
13. Original file is downloaded.

---

# 📁 Project Structure

```
A-Layered-Encryption-for-Document-Sharing/
│
├── app.py
├── models.py
├── routes/
├── templates/
├── static/
├── uploads/
├── encrypted_files/
├── database/
├── utils/
├── requirements.txt
└── README.md
```

*(Project structure may vary depending on implementation.)*

---

# 🛡️ Security Features

- Multi-Layer Encryption
- Random Key Generation
- Secure Authentication
- Session Management
- Password Hashing
- SMTP over TLS
- Zero-Knowledge Storage
- Secure In-Memory Decryption
- Dual-Channel Key Distribution
- Ciphertext Storage Only

---

# 🎯 Applications

- Secure Document Sharing
- Enterprise File Transfer
- Academic Research Collaboration
- Government Organizations
- Healthcare Data Exchange
- Confidential Business Communication

---

# 🔮 Future Improvements

- RSA Hybrid Encryption
- Multi-Factor Authentication (MFA)
- Cloud Deployment (AWS / Azure / Render)
- Secure File Expiry
- Auto Delete Feature
- Digital Signature Verification
- Large File Streaming
- Role-Based Access Control

---

# 👨‍💻 Authors

### Teja Sai Y
B.Tech Electronics & Computer Engineering

### Kakarala Sai Ram
B.Tech Electronics & Computer Engineering

### P. Sumanth [Sumanth3036]
B.Tech Electronics & Computer Engineering

**Amrita Vishwa Vidyapeetham**
Bengaluru Campus

---


# ⭐ If you found this project useful

Please consider giving the repository a **⭐ Star**!

It motivates us to build more secure and impactful open-source projects.

---

<div align="center">

### 🔐 Secure • Reliable • Confidential

**Protecting Digital Documents with Layered Encryption**

</div>
