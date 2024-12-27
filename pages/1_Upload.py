import streamlit as st
import pandas as pd
from utils.auth import check_authentication
from utils.database import save_dataset
import json

def main():
    if not check_authentication():
        return
        
    st.title("Upload Dataset")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'json'],
        help="Upload your dataset file (CSV, XLSX, or JSON format)"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_json(uploaded_file)
            
            st.write("Preview of your data:")
            st.dataframe(df.head())
            
            st.write("Dataset Statistics:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            if st.button("Save Dataset"):
                dataset_name = uploaded_file.name
                dataset_json = json.loads(df.to_json(orient='records'))
                dataset_id = save_dataset(
                    st.session_state['user_id'],
                    dataset_name,
                    dataset_json
                )
                st.success(f"Dataset saved successfully! ID: {dataset_id}")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
