import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
import streamlit as st

class DataVisualizer:
    @staticmethod
    def create_distribution_plot(real_data: pd.DataFrame, synthetic_data: pd.DataFrame, column: str):
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=real_data[column],
            name='Real Data',
            opacity=0.75
        ))
        
        fig.add_trace(go.Histogram(
            x=synthetic_data[column],
            name='Synthetic Data',
            opacity=0.75
        ))
        
        fig.update_layout(
            title=f'Distribution Comparison: {column}',
            xaxis_title=column,
            yaxis_title='Count',
            barmode='overlay'
        )
        
        return fig

    @staticmethod
    def create_correlation_heatmap(df: pd.DataFrame, title: str):
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_df.corr()
        
        fig = px.imshow(
            correlation_matrix,
            labels=dict(color="Correlation"),
            title=title
        )
        
        fig.update_layout(
            width=700,
            height=700
        )
        
        return fig

    @staticmethod
    def create_evaluation_radar_chart(evaluation_metrics: Dict):
        categories = list(evaluation_metrics.keys())
        values = list(evaluation_metrics.values())
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            title="Synthetic Data Quality Evaluation"
        )
        
        return fig

    @staticmethod
    def create_completeness_chart(df: pd.DataFrame):
        completeness = (df.count() / len(df) * 100).sort_values()
        
        fig = px.bar(
            x=completeness.index,
            y=completeness.values,
            labels={'x': 'Columns', 'y': 'Completeness (%)'},
            title='Data Completeness by Column'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        
        return fig
