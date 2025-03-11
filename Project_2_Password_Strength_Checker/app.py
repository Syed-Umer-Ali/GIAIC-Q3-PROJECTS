import streamlit as st
import random
import string
from zxcvbn import zxcvbn

def generate_strong_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))

def main():
    # Sidebar Settings
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        theme_option = st.selectbox("🎨 Choose Theme:", ["Dark", "Light"])
        if theme_option == "Light":
            st.markdown('<style> .stApp { background-color: white; color: black; } </style>', unsafe_allow_html=True)

    # Apply custom styles using CSS
    st.markdown(
        """
        <style>
            .stApp {
                background-color: black;
                color: white;
            }
            header[data-testid="stHeader"] {
                background-color: #1E1E1E;
            }
            .animated-title {
                font-size: 40px;
                font-weight: bold;
                text-align: center;
                color: red;
            }
            .password-box input {
                background-color: black;
                color: white;
                border: 2px solid red;
                padding: 10px;
                font-size: 18px;
                width: 100%;
                text-align: center;
            }
            .result-box {
                color: white;
                background-color: black;
                padding: 10px;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                border-radius: 10px;
                margin-top: 20px;
            }
            .suggestion-box {
                background-color: #FFD700;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                border-radius: 10px;
                margin-top: 20px;
                color: black;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page Title
    st.markdown("<h1 class='animated-title'>🔐 Password Strength Meter</h1>", unsafe_allow_html=True)

    password = st.text_input("", placeholder="Enter your password", type="password")

    st.markdown("""
    **A strong password should:**
    ✅ Be at least 8 characters long  
    ✅ Contain uppercase & lowercase letters  
    ✅ Include at least one digit (0-9)  
    ✅ Have one special character (!@#$%^&*)  
    """)

    if password:
        result = zxcvbn(password)
        score = result['score']

        strength_levels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
        st.markdown(f'<div class="result-box">🔒 Password Strength: {strength_levels[score]}</div>', unsafe_allow_html=True)

        # Password strength meter
        st.progress((score + 1) / 5)

        if score < 3:
            suggested_password = generate_strong_password()
            st.markdown(f'<div class="suggestion-box">⚠️ Your password is weak! Try using: `{suggested_password}`</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
