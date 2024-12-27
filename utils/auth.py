import streamlit as st
from typing import Optional
import os
import hashlib
import psycopg2
from datetime import datetime

def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOST'],
        port=os.environ['PGPORT']
    )

def init_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        hashed_password = hash_password(password)
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        return True
    except psycopg2.Error:
        return False
    finally:
        cur.close()
        conn.close()

def authenticate(username: str, password: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (username,)
        )
        result = cur.fetchone()
        if result and result[0] == hash_password(password):
            return True
        return False
    finally:
        cur.close()
        conn.close()

def login_form():
    if st.session_state.authenticated:
        st.sidebar.write(f"Logged in as: {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.experimental_rerun()
    else:
        with st.sidebar.form("login"):
            st.write("## Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("Login")
            with col2:
                signup_submitted = st.form_submit_button("Sign Up")

            if login_submitted and username and password:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")

            if signup_submitted and username and password:
                if create_user(username, password):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists")
