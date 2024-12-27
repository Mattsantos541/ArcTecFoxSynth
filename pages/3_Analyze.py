import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import check_authentication
from utils.database import get_user_datasets
from utils.synthetic import get_data_profile

def main():
    if not check_authentication():
        return
        
    st.title("Data Analysis")
    
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
        
        st.subheader("Dataset Profile")
        profile = get_data_profile(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", profile['rows'])
            st.metric("Numeric Columns", profile['numeric_columns'])
        with col2:
            st.metric("Total Columns", profile['columns'])
            st.metric("Categorical Columns", profile['categorical_columns'])
        with col3:
            st.metric("Missing Values", profile['missing_values'])
        
        st.subheader("Data Visualization")
        
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("Select X axis", numeric_cols)
            y_col = st.selectbox("Select Y axis", numeric_cols)
            
            fig = px.scatter(df, x=x_col, y=y_col)
            st.plotly_chart(fig)
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column for distribution", numeric_cols)
            fig = px.histogram(df, x=selected_col)
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
