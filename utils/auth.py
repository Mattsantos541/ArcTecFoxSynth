import streamlit as st
import hashlib
import hmac
from utils.database import init_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash):
    return hmac.compare_digest(
        hash_password(password),
        hash
    )

def create_user(username, password):
    conn = init_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        cur.close()

def verify_user(username, password):
    conn = init_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password_hash FROM users WHERE username = %s",
        (username,)
    )
    result = cur.fetchone()
    cur.close()
    
    if result and verify_password(password, result[1]):
        return result[0]
    return None

def check_authentication():
    if 'user_id' not in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                user_id = verify_user(username, password)
                if user_id:
                    st.session_state['user_id'] = user_id
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
        
        with col2:
            st.subheader("Register")
            new_username = st.text_input("Username", key="register_username")
            new_password = st.text_input("Password", type="password", key="register_password")
            
            if st.button("Register"):
                if create_user(new_username, new_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")
        
        return False
    return True
