import streamlit as st
import pandas as pd
import json
from utils.auth import check_authentication
from utils.database import get_user_datasets
from utils.synthetic import generate_synthetic_data

def main():
    if not check_authentication():
        return
        
    st.title("Generate Synthetic Data")
    
    datasets = get_user_datasets(st.session_state['user_id'])
    
    if not datasets:
        st.warning("No datasets found. Please upload a dataset first.")
        return
    
    selected_dataset = st.selectbox(
        "Select Dataset",
        options=datasets,
        format_func=lambda x: x['name']
    )
    
    if selected_dataset:
        df = pd.DataFrame(selected_dataset['data'])
        st.write("Original Data Preview:")
        st.dataframe(df.head())
        
        num_rows = st.number_input(
            "Number of synthetic rows to generate",
            min_value=1,
            max_value=10000,
            value=len(df)
        )
        
        if st.button("Generate Synthetic Data"):
            with st.spinner("Generating synthetic data..."):
                synthetic_df = generate_synthetic_data(df, num_rows)
                
                st.write("Synthetic Data Preview:")
                st.dataframe(synthetic_df.head())
                
                st.download_button(
                    label="Download Synthetic Data",
                    data=synthetic_df.to_csv(index=False),
                    file_name="synthetic_data.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
