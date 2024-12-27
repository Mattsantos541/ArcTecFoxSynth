import streamlit as st
from auth import Auth
from data_processor import DataProcessor
from synthetic import SyntheticDataGenerator
from visualizations import DataVisualizer
from database import Database
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from utils import validate_file_extension, format_file_size, create_download_link
from styles import apply_custom_styles, display_logo
import pandas as pd

def initialize_session_state():
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'current_data' not in st.session_state:
        st.session_state['current_data'] = None
    if 'synthetic_data' not in st.session_state:
        st.session_state['synthetic_data'] = None

def login_page():
    st.header("Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            auth = Auth()
            if auth.login_user(email, password):
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    
    with col2:
        if st.button("Register"):
            auth = Auth()
            if auth.register_user(email, password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Registration failed")

def main_page():
    display_logo()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload Data", "Generate Synthetic Data", "Analysis", "Dashboard"])
    
    if page == "Upload Data":
        upload_data_page()
    elif page == "Generate Synthetic Data":
        generate_synthetic_data_page()
    elif page == "Analysis":
        analysis_page()
    elif page == "Dashboard":
        dashboard_page()
    
    if st.sidebar.button("Logout"):
        auth = Auth()
        auth.logout_user()
        st.experimental_rerun()

def upload_data_page():
    st.header("Upload Data")
    
    uploaded_file = st.file_uploader("Choose a file", type=[ext[1:] for ext in ALLOWED_EXTENSIONS])
    
    if uploaded_file is not None:
        if not validate_file_extension(uploaded_file.name, ALLOWED_EXTENSIONS):
            st.error("Invalid file format")
            return
        
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File too large. Maximum size: {format_file_size(MAX_FILE_SIZE)}")
            return
        
        data_processor = DataProcessor()
        df = data_processor.load_data(uploaded_file)
        
        if df is not None:
            validation_results = data_processor.validate_data(df)
            
            if validation_results["is_valid"]:
                st.session_state['current_data'] = df
                st.success("Data uploaded successfully!")
                
                st.subheader("Data Preview")
                st.write(df.head())
                
                summary = data_processor.get_data_summary(df)
                st.subheader("Data Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Rows", summary["rows"])
                with col2:
                    st.metric("Columns", summary["columns"])
                with col3:
                    st.metric("Size", f"{summary['memory_usage']:.2f} MB")
                
            else:
                st.error("Data validation failed:")
                for error in validation_results["errors"]:
                    st.write(f"- {error}")

def generate_synthetic_data_page():
    st.header("Generate Synthetic Data")
    
    if st.session_state['current_data'] is None:
        st.warning("Please upload data first")
        return
    
    model_type = st.selectbox("Select Model", ["GaussianCopula", "CTGAN"])
    num_rows = st.number_input("Number of synthetic rows to generate", 
                              min_value=1, 
                              max_value=100000, 
                              value=len(st.session_state['current_data']))
    
    if st.button("Generate Synthetic Data"):
        generator = SyntheticDataGenerator()
        
        with st.spinner("Training model..."):
            success = generator.train_model(st.session_state['current_data'], model_type)
        
        if success:
            with st.spinner("Generating synthetic data..."):
                synthetic_data = generator.generate_synthetic_data(num_rows)
                
                if synthetic_data is not None:
                    st.session_state['synthetic_data'] = synthetic_data
                    st.success("Synthetic data generated successfully!")
                    
                    st.subheader("Synthetic Data Preview")
                    st.write(synthetic_data.head())
                    
                    # Download options
                    format_option = st.selectbox("Download format", ["csv", "json"])
                    download_link = create_download_link(synthetic_data, format_option)
                    st.markdown(f'<a href="{download_link}" download="synthetic_data.{format_option}">Download Synthetic Data</a>', 
                              unsafe_allow_html=True)

def analysis_page():
    st.header("Analysis")
    
    if st.session_state['current_data'] is None or st.session_state['synthetic_data'] is None:
        st.warning("Please upload data and generate synthetic data first")
        return
    
    visualizer = DataVisualizer()
    
    # Distribution comparison
    st.subheader("Distribution Comparison")
    column = st.selectbox("Select column", st.session_state['current_data'].columns)
    
    dist_plot = visualizer.create_distribution_plot(
        st.session_state['current_data'],
        st.session_state['synthetic_data'],
        column
    )
    st.plotly_chart(dist_plot)
    
    # Correlation analysis
    st.subheader("Correlation Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        real_corr = visualizer.create_correlation_heatmap(
            st.session_state['current_data'],
            "Real Data Correlation"
        )
        st.plotly_chart(real_corr)
    
    with col2:
        synthetic_corr = visualizer.create_correlation_heatmap(
            st.session_state['synthetic_data'],
            "Synthetic Data Correlation"
        )
        st.plotly_chart(synthetic_corr)
    
    # Quality evaluation
    st.subheader("Quality Evaluation")
    generator = SyntheticDataGenerator()
    evaluation_results = generator.evaluate_synthetic_data(
        st.session_state['current_data'],
        st.session_state['synthetic_data']
    )
    
    if evaluation_results is not None:
        radar_chart = visualizer.create_evaluation_radar_chart(evaluation_results)
        st.plotly_chart(radar_chart)

def dashboard_page():
    st.header("Dashboard")
    
    db = Database()
    datasets = db.get_user_datasets(st.session_state['user']['id'])
    
    st.subheader("Your Datasets")
    if not datasets:
        st.info("No datasets found")
        return
    
    for dataset in datasets:
        with st.expander(f"{dataset['name']} - {dataset['created_at']}"):
            st.write(f"Description: {dataset['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Load Original", key=f"orig_{dataset['id']}"):
                    st.session_state['current_data'] = pd.read_json(dataset['original_data'])
                    st.success("Original data loaded")
            
            with col2:
                if dataset['synthetic_data'] and st.button("Load Synthetic", key=f"syn_{dataset['id']}"):
                    st.session_state['synthetic_data'] = pd.read_json(dataset['synthetic_data'])
                    st.success("Synthetic data loaded")

def main():
    apply_custom_styles()
    initialize_session_state()
    
    if st.session_state['user'] is None:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    main()
