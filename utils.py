import streamlit as st
from typing import List, Dict
import pandas as pd
import json

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def format_file_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def create_download_link(df: pd.DataFrame, format: str = 'csv') -> str:
    if format == 'csv':
        data = df.to_csv(index=False)
        mime = 'text/csv'
        ext = 'csv'
    elif format == 'json':
        data = df.to_json(orient='records')
        mime = 'application/json'
        ext = 'json'
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return f'data:{mime};charset=utf-8,{data}'

def display_metric_card(title: str, value: str, delta: str = None):
    st.markdown(f"""
        <div class="metric-container">
            <h4>{title}</h4>
            <h2>{value}</h2>
            {f'<p>Δ {delta}</p>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)

def handle_error(error: Exception, message: str = "An error occurred"):
    st.error(f"{message}: {str(error)}")
    return None
