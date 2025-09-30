# src/visualization/cdf_plots.py
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from typing import Dict

class CDFVisualizer:
    """Create CDF visualizations for A/B testing results"""
    
    @staticmethod
    def plot_matplotlib_cdf(analysis_results: Dict, metric_name: str, save_path: str = None):
        """Create matplotlib CDF plot"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Main CDF plot
        ax1.plot(analysis_results['variant_a']['sorted'], 
                analysis_results['variant_a']['cdf'], 
                label='Variant A', linewidth=2)
        ax1.plot(analysis_results['variant_b']['sorted'], 
                analysis_results['variant_b']['cdf'], 
                label='Variant B', linewidth=2)
        ax1.set_xlabel(metric_name.title())
        ax1.set_ylabel('Cumulative Probability')
        ax1.set_title(f'CDF Comparison: {metric_name.title()}')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Probability difference plot
        ax2.plot(analysis_results['probability_differences']['x_values'],
                analysis_results['probability_differences']['differences'],
                color='red', linewidth=2)
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax2.set_xlabel(metric_name.title())
        ax2.set_ylabel('Probability Difference (B - A)')
        ax2.set_title('CDF Difference')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def create_interactive_plot(analysis_results: Dict, metric_name: str):
        """Create interactive Plotly visualization"""
        fig = go.Figure()
        
        # CDF traces
        fig.add_trace(go.Scatter(
            x=analysis_results['variant_a']['sorted'],
            y=analysis_results['variant_a']['cdf'],
            name='Variant A',
            line=dict(color='blue', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=analysis_results['variant_b']['sorted'],
            y=analysis_results['variant_b']['cdf'],
            name='Variant B', 
            line=dict(color='red', width=3)
        ))
        
        fig.update_layout(
            title=f'A/B Test CDF Analysis: {metric_name.title()}',
            xaxis_title=metric_name.title(),
            yaxis_title='Cumulative Probability',
            hovermode='x unified',
            width=1000,
            height=600
        )
        
        return fig