import streamlit as st
from utils.auth import check_authentication
from utils.database import init_connection
import os

st.set_page_config(
    page_title="ArcTecFox - Synthetic Data Platform",
    page_icon="❄️",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    if not check_authentication():
        return
    
    st.title("ArcTecFox - Synthetic Data Platform")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to ArcTecFox
        Your secure platform for synthetic data generation and analysis.
        
        #### Key Features:
        - 🔒 Secure data handling
        - 🔄 Advanced synthetic data generation
        - 📊 Interactive analytics
        - 📈 Dataset comparison tools
        """)
        
    with col2:
        st.image("https://images.unsplash.com/photo-1572435555646-7ad9a149ad91",
                caption="Secure Data Processing",
                use_column_width=True)
    
    st.markdown("---")
    
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        st.metric(label="Active Projects", value="0")
    with metrics_col2:
        st.metric(label="Generated Datasets", value="0")
    with metrics_col3:
        st.metric(label="Data Quality Score", value="N/A")

if __name__ == "__main__":
    main()
