import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG
import pandas as pd

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port']
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            self._create_tables()
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")

    def _create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS datasets (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                name VARCHAR(255) NOT NULL,
                description TEXT,
                original_data JSONB,
                synthetic_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        for command in commands:
            self.cursor.execute(command)
        self.conn.commit()

    def save_dataset(self, user_id, name, description, original_data, synthetic_data=None):
        query = """
        INSERT INTO datasets (user_id, name, description, original_data, synthetic_data)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        self.cursor.execute(query, (user_id, name, description, 
                                  original_data.to_json(), 
                                  synthetic_data.to_json() if synthetic_data is not None else None))
        self.conn.commit()
        return self.cursor.fetchone()['id']

    def get_user_datasets(self, user_id):
        query = "SELECT * FROM datasets WHERE user_id = %s ORDER BY created_at DESC"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
