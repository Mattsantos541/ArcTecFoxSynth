import hashlib
import secrets
import streamlit as st
from database import Database

class Auth:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def _hash_password(self, password):
        salt = secrets.token_hex(16)
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest() + salt

    def _verify_password(self, password, hash_salt):
        stored_hash = hash_salt[:-32]
        salt = hash_salt[-32:]
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest() == stored_hash

    def login_user(self, email, password):
        query = "SELECT * FROM users WHERE email = %s"
        self.db.cursor.execute(query, (email,))
        user = self.db.cursor.fetchone()
        
        if user and self._verify_password(password, user['password_hash']):
            st.session_state['user'] = {
                'id': user['id'],
                'email': user['email']
            }
            return True
        return False

    def register_user(self, email, password):
        try:
            password_hash = self._hash_password(password)
            query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
            self.db.cursor.execute(query, (email, password_hash))
            self.db.conn.commit()
            return True
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")
            return False

    def logout_user(self):
        st.session_state['user'] = None
