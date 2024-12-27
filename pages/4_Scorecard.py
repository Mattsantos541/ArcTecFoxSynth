import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import check_authentication
from utils.database import get_user_datasets
from utils.synthetic import evaluate_synthetic_data

def main():
    if not check_authentication():
        return
        
    st.title("Synthetic Data Scorecard")
    
    datasets = get_user_datasets(st.session_state['user_id'])
    
    if not datasets:
        st.warning("No datasets found. Please upload a dataset first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        original_dataset = st.selectbox(
            "Select Original Dataset",
            options=datasets,
            format_func=lambda x: x['name'],
            key="original"
        )
    
    with col2:
        synthetic_dataset = st.selectbox(
            "Select Synthetic Dataset",
            options=datasets,
            format_func=lambda x: x['name'],
            key="synthetic"
        )
    
    if original_dataset and synthetic_dataset:
        original_df = pd.DataFrame(original_dataset['data'])
        synthetic_df = pd.DataFrame(synthetic_dataset['data'])
        
        if st.button("Evaluate"):
            evaluation_results = evaluate_synthetic_data(
                original_df,
                synthetic_df
            )
            
            st.subheader("Evaluation Results")
            
            scores = evaluation_results.get_results()
            for metric, score in scores.items():
                st.metric(metric, f"{score:.2f}")
            
            st.subheader("Distribution Comparison")
            
            numeric_cols = original_df.select_dtypes(include=['int64', 'float64']).columns
            selected_col = st.selectbox("Select column", numeric_cols)
            
            fig = px.histogram(
                original_df,
                x=selected_col,
                title="Original vs Synthetic Distribution",
                opacity=0.7
            )
            fig.add_histogram(x=synthetic_df[selected_col])
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
