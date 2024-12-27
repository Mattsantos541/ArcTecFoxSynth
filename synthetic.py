import streamlit as st
import pandas as pd
import numpy as np

class SyntheticDataGenerator:
    def __init__(self):
        self.models = {}
        self.current_model = None
        try:
            from sdv.tabular import GaussianCopula, CTGAN
            self.models = {
                'GaussianCopula': GaussianCopula,
                'CTGAN': CTGAN
            }
        except ImportError:
            st.warning("Advanced synthetic data generation models (SDV) are not available. Using basic simulation instead.")
            self.use_basic_simulation = True

    def train_model(self, data: pd.DataFrame, model_name: str = 'GaussianCopula', **kwargs):
        try:
            if hasattr(self, 'use_basic_simulation'):
                return self._train_basic_model(data)

            model_class = self.models[model_name]
            self.current_model = model_class(**kwargs)
            self.current_model.fit(data)
            return True
        except Exception as e:
            st.error(f"Error training model: {str(e)}")
            return False

    def _train_basic_model(self, data: pd.DataFrame):
        """Fallback method using basic statistical simulation"""
        self.data_summary = {
            'means': data.mean(),
            'stds': data.std(),
            'dtypes': data.dtypes,
            'categorical_columns': data.select_dtypes(include=['object']).columns,
            'numerical_columns': data.select_dtypes(include=[np.number]).columns
        }
        return True

    def generate_synthetic_data(self, num_rows: int) -> pd.DataFrame:
        try:
            if hasattr(self, 'use_basic_simulation'):
                return self._generate_basic_synthetic_data(num_rows)

            if self.current_model is None:
                raise ValueError("Model not trained. Please train the model first.")

            synthetic_data = self.current_model.sample(num_rows)
            return synthetic_data
        except Exception as e:
            st.error(f"Error generating synthetic data: {str(e)}")
            return None

    def _generate_basic_synthetic_data(self, num_rows: int) -> pd.DataFrame:
        """Generate synthetic data using basic statistical simulation"""
        synthetic_data = pd.DataFrame()

        for col in self.data_summary['numerical_columns']:
            mean = self.data_summary['means'][col]
            std = self.data_summary['stds'][col]
            synthetic_data[col] = np.random.normal(mean, std, num_rows)

            # Convert to original dtype
            synthetic_data[col] = synthetic_data[col].astype(self.data_summary['dtypes'][col])

        for col in self.data_summary['categorical_columns']:
            unique_values = self.data_summary['means'].index
            synthetic_data[col] = np.random.choice(unique_values, num_rows)

        return synthetic_data

    def evaluate_synthetic_data(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        try:
            if hasattr(self, 'use_basic_simulation'):
                return self._basic_evaluation(real_data, synthetic_data)

            from sdv.evaluation import evaluate
            evaluation_results = evaluate(
                real_data,
                synthetic_data,
                metrics=['CSTest', 'KSTest', 'ContinuousSimilarity']
            )
            return evaluation_results
        except Exception as e:
            st.error(f"Error evaluating synthetic data: {str(e)}")
            return None

    def _basic_evaluation(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        """Basic statistical evaluation when SDV is not available"""
        metrics = {}

        # Compare means
        real_means = real_data.mean()
        synthetic_means = synthetic_data.mean()
        mean_similarity = 1 - abs(real_means - synthetic_means).mean()
        metrics['MeanSimilarity'] = float(mean_similarity)

        # Compare standard deviations
        real_stds = real_data.std()
        synthetic_stds = synthetic_data.std()
        std_similarity = 1 - abs(real_stds - synthetic_stds).mean()
        metrics['StdSimilarity'] = float(std_similarity)

        # Overall score
        metrics['OverallScore'] = (metrics['MeanSimilarity'] + metrics['StdSimilarity']) / 2

        return metrics