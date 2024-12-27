from sdv.tabular import GaussianCopula, CTGAN
from sdv.evaluation import evaluate
import pandas as pd
import streamlit as st

class SyntheticDataGenerator:
    def __init__(self):
        self.models = {
            'GaussianCopula': GaussianCopula,
            'CTGAN': CTGAN
        }
        self.current_model = None

    def train_model(self, data: pd.DataFrame, model_name: str = 'GaussianCopula', **kwargs):
        try:
            model_class = self.models[model_name]
            self.current_model = model_class(**kwargs)
            self.current_model.fit(data)
            return True
        except Exception as e:
            st.error(f"Error training model: {str(e)}")
            return False

    def generate_synthetic_data(self, num_rows: int) -> pd.DataFrame:
        if self.current_model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        try:
            synthetic_data = self.current_model.sample(num_rows)
            return synthetic_data
        except Exception as e:
            st.error(f"Error generating synthetic data: {str(e)}")
            return None

    def evaluate_synthetic_data(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        try:
            evaluation_results = evaluate(
                real_data,
                synthetic_data,
                metrics=['CSTest', 'KSTest', 'ContinuousSimilarity']
            )
            return evaluation_results
        except Exception as e:
            st.error(f"Error evaluating synthetic data: {str(e)}")
            return None
