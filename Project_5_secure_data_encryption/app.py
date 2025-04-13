import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

# Constants
KEY_FILE = "secret.key"
DATA_FILE = "secure_data.json"
SALT = b'static_salt_here'
LOCKOUT_TIME = 60  # seconds

# Helper functions

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read()

KEY = load_key()
cipher = Fernet(KEY)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def hash_passkey_pbkdf2(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)
    return urlsafe_b64encode(key).decode()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text):
    try:
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        st.error(f"Decryption failed: {str(e)}")
        return None

# Load persistent data
if "stored_data" not in st.session_state:
    st.session_state.stored_data = load_data()

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = {}

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Sidebar Navigation with updated color
st.sidebar.markdown("""
    <style>
        /* Sidebar styling */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            background: #E80C31; /* Red color */
            color: #FFFFFF; /* White text */
            border-radius: 10px;
            margin: 4px 0;
            padding: 0.4rem 1rem;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
            background-color: #d11f2c; /* Slightly darker red for hover effect */
        }
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-selected="true"] {
            background-color: #b30c23; /* Darker red for selected item */
            font-weight: bold;
            box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05);
        }
        .sidebar .element-container:nth-child(n+2) {
            animation: slideIn 0.5s ease-in-out;
        }
        @keyframes slideIn {
            from { transform: translateX(-10px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .sidebar .css-1lcbmhc {
            padding-top: 10px;
        }
        .sidebar .css-14xtw13 {
            padding-top: 0;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🔐 Secure Data App")

menu = ["Home", "Login", "Store Data", "Retrieve Data"]
selected = st.sidebar.radio(
    "Navigation", menu, index=0, help="Select the action you want to perform")

# Home
if selected == "Home":
    st.title("🏠 Welcome")
    st.write("Multi-user secure storage with advanced security features.")
    st.info("If you are a new user, please register yourself below.")

    st.subheader("📝 Quick Register")
    username = st.text_input("Choose Username", key="home_register_username")
    password = st.text_input("Choose Password", type="password", key="home_register_password")

    if st.button("Register", key="home_register_button"):
        if username and password:
            if username in st.session_state.stored_data:
                st.error("Username already exists.")
            else:
                st.session_state.stored_data[username] = {
                    "password": hash_passkey_pbkdf2(password),
                    "entries": {}
                }
                st.session_state.current_user = username
                save_data(st.session_state.stored_data)
                st.success("User registered successfully and logged in!")
        else:
            st.error("Please fill both fields.")

# Login
elif selected == "Login":
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_data = st.session_state.stored_data.get(username)

        if not user_data:
            st.error("User not found")
        else:
            if username in st.session_state.lockout_time:
                if time.time() < st.session_state.lockout_time[username]:
                    st.warning("Too many failed attempts. Try again later.")
                    st.stop()

            if user_data["password"] == hash_passkey_pbkdf2(password):
                st.session_state.current_user = username
                st.session_state.failed_attempts[username] = 0
                st.success("Login successful!")
            else:
                st.session_state.failed_attempts[username] = st.session_state.failed_attempts.get(username, 0) + 1
                attempts_left = 3 - st.session_state.failed_attempts[username]
                if attempts_left <= 0:
                    st.session_state.lockout_time[username] = time.time() + LOCKOUT_TIME
                    st.warning("Too many failed attempts. Locked out for 1 minute.")
                else:
                    st.error(f"Incorrect password. Attempts left: {attempts_left}")

# Store Data
elif selected == "Store Data":
    if not st.session_state.current_user:
        st.warning("Please login first.")
        st.stop()

    st.title("📂 Store Data")
    user_data = st.text_area("Enter Data")
    passkey = st.text_input("Enter Passkey", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed = hash_passkey_pbkdf2(passkey)
            encrypted = encrypt_data(user_data)
            user_entries = st.session_state.stored_data[st.session_state.current_user]["entries"]
            user_entries[encrypted] = hashed
            save_data(st.session_state.stored_data)
            st.success(f"Encrypted Data: {encrypted}")
            st.code(hashed, language="text")
            st.caption("🔒 Passkey hash (copied to clipboard using right-click > copy)")
            st.text_input("Copy Hash", value=hashed, key="copy_hash", help="Select and copy the hash value")
        else:
            st.error("Please provide both data and passkey.")

# Retrieve Data
elif selected == "Retrieve Data":
    if not st.session_state.current_user:
        st.warning("Please login first.")
        st.stop()

    st.title("🔍 Retrieve Data")
    encrypted_text = st.text_area("Enter Encrypted Data")
    passkey = st.text_input("Enter Passkey", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            hashed_input = hash_passkey_pbkdf2(passkey)
            user_entries = st.session_state.stored_data[st.session_state.current_user]["entries"]
            stored_pass = user_entries.get(encrypted_text)

            if stored_pass and stored_pass == hashed_input:
                decrypted = decrypt_data(encrypted_text)
                if decrypted:
                    st.success(f"Decrypted Data: {decrypted}")
                else:
                    st.error("Decryption failed.")
            else:
                st.error("Incorrect passkey or entry not found.")
        else:
            st.error("Both fields required")
