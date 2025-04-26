# 🛡️ GI-AIC Project 5: Secure Data Encryption System

## 🎯 Objective  
Build a **Streamlit-based secure encryption app** that allows users to safely store and retrieve data using a passkey. The app:
- Stores encrypted data in memory 🧠  
- Hashes passkeys using SHA-256 🔐  
- Limits access after 3 failed attempts 🚫  
- Forces reauthorization via a login page 🔑

---

## 💡 Features
- 🔏 Encrypt & store data using a unique passkey  
- 🔓 Decrypt data only with the correct passkey  
- 🔃 Redirect to login after 3 failed attempts  
- 🧠 In-memory storage (no database)  
- 🖥️ Streamlit UI for ease of use  

---

## 🧰 Technologies Used
- 🐍 Python  
- 🌐 Streamlit  
- 🔐 `hashlib` for passkey hashing (SHA-256)  
- 🛡️ `cryptography.fernet` for encryption/decryption  

---

## 🗂️ Pages Overview

### 🏠 Home Page  
> Entry point with options to **store** or **retrieve** data  

### 📥 Store Data  
> Enter text and passkey to **encrypt & save** securely  

### 🔎 Retrieve Data  
> Enter encrypted text and correct passkey to decrypt  
> Fails after 3 wrong attempts ➡️ Login page  

### 🔑 Login Page  
> Enter master password (`admin123`) to reset access  

---

## 📦 Data Structure Example
```python
stored_data = {
    "encrypted_text_1": {
        "encrypted_text": "gAAAAABlZ...",
        "passkey": "hashed_passkey"
    }
}
