import streamlit as st
from utils.auth import check_authentication
from utils.database import init_connection
import os
import shutil

st.set_page_config(
    page_title="ArcTecFox - Synthetic Data Platform",
    page_icon="❄️",
    layout="wide"
)

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("styles", exist_ok=True)

# Create custom.css if it doesn't exist
if not os.path.exists('styles/custom.css'):
    with open('styles/custom.css', 'w') as f:
        f.write("""
/* Arctic-inspired theme */
.stApp {
    background-color: #FFFFFF;
}

.stButton>button {
    background-color: #1E88E5;
    color: white;
    border-radius: 4px;
    border: none;
    padding: 0.5rem 1rem;
    transition: background-color 0.3s ease;
}
""")

# Apply custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def ensure_static_folder():
    os.makedirs("static", exist_ok=True)
    if not os.path.exists("static/logo.jpg") and os.path.exists("attached_assets/AF.jpg"):
        shutil.copy("attached_assets/AF.jpg", "static/logo.jpg")

def main():
    if not check_authentication():
        return

    ensure_static_folder()

    # Display logo
    if os.path.exists("static/logo.jpg"):
        st.image("static/logo.jpg", width=150)

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
        st.markdown("""
        #### Secure Data Processing
        Transform your sensitive data into valuable insights while maintaining privacy.
        """)

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