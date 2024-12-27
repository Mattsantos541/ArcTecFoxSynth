import pandas as pd
import numpy as np
from typing import Dict, List, Union
import streamlit as st

class DataProcessor:
    @staticmethod
    def load_data(file) -> pd.DataFrame:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.json'):
                df = pd.read_json(file)
            else:
                raise ValueError("Unsupported file format")
            
            return df
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None

    @staticmethod
    def validate_data(df: pd.DataFrame) -> Dict[str, Union[bool, List[str]]]:
        validation_results = {
            "is_valid": True,
            "errors": []
        }

        # Check for empty dataframe
        if df.empty:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Dataset is empty")

        # Check for missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Missing values in columns: {', '.join(missing_cols)}")

        # Check for duplicate rows
        if df.duplicated().any():
            validation_results["is_valid"] = False
            validation_results["errors"].append("Dataset contains duplicate rows")

        return validation_results

    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict:
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict() if not df.empty else {},
            "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024)  # in MB
        }
        return summary

    @staticmethod
    def prepare_data_for_synthesis(df: pd.DataFrame) -> pd.DataFrame:
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
        
        return df
