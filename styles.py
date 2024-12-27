import streamlit as st
from config import COLORS

def apply_custom_styles():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {COLORS['background']};
            color: {COLORS['text']};
        }}
        
        .stButton>button {{
            background-color: {COLORS['primary']};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
        }}
        
        .stTextInput>div>div>input {{
            border-radius: 5px;
            border: 1px solid {COLORS['secondary']};
        }}
        
        .stHeader {{
            background-color: {COLORS['primary']};
            padding: 1rem;
            border-radius: 5px;
            color: white;
        }}
        
        .stAlert {{
            background-color: {COLORS['accent']};
            border: 1px solid {COLORS['secondary']};
            border-radius: 5px;
            padding: 1rem;
        }}
        
        .metric-container {{
            background-color: white;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        </style>
    """, unsafe_allow_html=True)

def display_logo():
    st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="color: {COLORS['primary']};">ArcTecFox</h1>
            <p style="color: {COLORS['text']};">Secure Synthetic Data Platform</p>
        </div>
    """, unsafe_allow_html=True)
