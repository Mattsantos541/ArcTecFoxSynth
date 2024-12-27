import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import os
import pandas as pd

@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )

def init_tables():
    conn = init_connection()
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Datasets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            name VARCHAR(255) NOT NULL,
            data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Synthetic datasets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS synthetic_datasets (
            id SERIAL PRIMARY KEY,
            original_dataset_id INTEGER REFERENCES datasets(id),
            data JSONB NOT NULL,
            parameters JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()

def save_dataset(user_id, name, data):
    conn = init_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO datasets (user_id, name, data) VALUES (%s, %s, %s) RETURNING id",
        (user_id, name, data)
    )
    dataset_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return dataset_id

def get_user_datasets(user_id):
    conn = init_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM datasets WHERE user_id = %s", (user_id,))
    datasets = cur.fetchall()
    cur.close()
    return datasets
