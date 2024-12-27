import pandas as pd
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.evaluation import evaluate
import streamlit as st

def generate_synthetic_data(df, num_rows):
    synthesizer = GaussianCopulaSynthesizer()
    synthesizer.fit(df)
    synthetic_data = synthesizer.sample(num_rows)
    return synthetic_data

def evaluate_synthetic_data(real_data, synthetic_data):
    evaluation_results = evaluate(
        real_data,
        synthetic_data,
        metrics=['CSTest', 'KSTest']
    )
    return evaluation_results

def get_data_profile(df):
    profile = {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'numeric_columns': len(df.select_dtypes(include=['int64', 'float64']).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns)
    }
    return profile
