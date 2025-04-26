import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import base64

# ---------------------------
# Session State Initialization
# ---------------------------
if "stored_data" not in st.session_state:
    st.session_state["stored_data"] = {}

if "failed_attempts" not in st.session_state:
    st.session_state["failed_attempts"] = {}

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# ---------------------------
# Key & Cipher Functions
# ---------------------------
def generate_key_from_passkey(passkey: str) -> bytes:
    hashed = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

# ---------------------------
# Encryption Functions
# ---------------------------
def encrypt_data(text: str, passkey: str) -> str:
    key = hashlib.sha256(passkey.encode()).digest()[:32]
    fernet = Fernet(base64.urlsafe_b64encode(key))
    return fernet.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str, passkey: str) -> str:
    try:
        key = hashlib.sha256(passkey.encode()).digest()[:32]
        fernet = Fernet(base64.urlsafe_b64encode(key))
        return fernet.decrypt(encrypted_text.encode()).decode()
    except:
        return None

# ---------------------------
# Styling Setup
# ---------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    .stApp {
        background: linear-gradient(to bottom right, #0d1b2a, #1b263b, #415a77);
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #1b263b !important;
        color: white !important;
    }
    .stButton>button {
        background-color: #415a77;
        color: white;
        border: none;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# UI Pages
# ---------------------------
def home():
    st.subheader("🏠 Welcome to Secure Data System")
    st.markdown("🔐 This app helps you **encrypt and store sensitive text** securely.")
    st.markdown("✅ Only *you* can decrypt it using your unique passkey.")
    st.markdown("➡️ Use the **Store Data** page to save encrypted data.")
    st.markdown("➡️ Use the **Retrieve Data** page to get it back when needed.")
    st.markdown("⚠️ After **3 wrong passkey attempts**, you'll need to reauthorize on the **Login** page.")

def store_data():
    st.subheader("📂 Store Data Securely")
    st.markdown("🧠 Use a *label* (username) to identify your data, then input your sensitive text and a passkey.")
    st.markdown("🔐 The passkey is used to encrypt your text — **don’t forget it!**")

    username = st.text_input("👤 Enter Username")
    user_data = st.text_area("📝 Enter Data to Encrypt")
    passkey = st.text_input("🔑 Enter Passkey", type="password")

    if st.button("🔒 Encrypt & Save"):
        if username and user_data and passkey:
            encrypted_text = encrypt_data(user_data, passkey)
            st.session_state["stored_data"][username] = {
                "encrypted_text": encrypted_text,
                "passkey": hash_passkey(passkey)
            }
            st.success("✅ Data stored securely!")
            st.code(encrypted_text, language="plaintext")
            st.markdown("📌 Copy this encrypted text and save it somewhere safe. It’s what you’ll get back.")
        else:
            st.error("⚠️ Please fill in all fields.")

def retrieve_data():
    st.subheader("🔍 Retrieve Your Data")
    st.markdown("🧠 Enter your username and the same passkey you used while storing.")
    st.markdown("🚨 After **3 failed attempts**, reauthorization via Login page will be needed.")

    username = st.text_input("👤 Enter Username")
    passkey = st.text_input("🔑 Enter Passkey", type="password")

    if username not in st.session_state["failed_attempts"]:
        st.session_state["failed_attempts"][username] = 0

    if st.session_state["failed_attempts"][username] >= 3:
        st.session_state["current_user"] = username
        st.warning("🔒 Too many failed attempts! Go to the Login page to reauthorize.")
        return

    if st.button("🔓 Decrypt"):
        if username in st.session_state["stored_data"]:
            stored = st.session_state["stored_data"][username]
            hashed_input = hash_passkey(passkey)

            if hashed_input == stored["passkey"]:
                decrypted = decrypt_data(stored["encrypted_text"], passkey)
                if decrypted:
                    st.success("✅ Decrypted Data:")
                    st.code(decrypted)
                    st.session_state["failed_attempts"][username] = 0
                else:
                    st.error("❌ Decryption failed!")
            else:
                st.session_state["failed_attempts"][username] += 1
                attempts = st.session_state["failed_attempts"][username]
                st.error(f"❌ Incorrect passkey! Attempts left: {3 - attempts}")
        else:
            st.error("⚠️ Username not found.")

def login():
    st.subheader("🔑 Reauthorization Required")
    st.markdown("⚠️ This page appears **after 3 failed attempts** on Retrieve Data.")
    st.markdown("🛡️ Only enter the master password to unlock attempts again.")

    password = st.text_input("🔐 Enter Admin Password", type="password")

    if st.button("🔓 Login"):
        if password == "admin123":
            username = st.session_state.get("current_user")
            if username:
                st.session_state["failed_attempts"][username] = 0
                st.success("✅ Reauthorized! Go back to Retrieve Data to try again.")
        else:
            st.error("❌ Incorrect admin password!")

# ---------------------------
# Main Navigation
# ---------------------------
st.title("🔒 Secure Data Encryption System")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("📁 Navigate", menu)

if choice == "Home":
    home()
elif choice == "Store Data":
    store_data()
elif choice == "Retrieve Data":
    retrieve_data()
elif choice == "Login":
    login()
