# src/visualization/advanced_dashboard.py
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class AdvancedDashboard:
    """Create comprehensive A/B test dashboard"""
    
    @staticmethod
    def create_comprehensive_dashboard(analysis_results: dict, business_impact: dict, 
                                     segment_results: dict, metric_name: str):
        """Create a comprehensive dashboard with multiple visualizations"""
        
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'CDF Comparison', 'Probability Difference',
                'Business Impact Analysis', 'Statistical Summary',
                'Segment Analysis', 'Bayesian Probability'
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"colspan": 2}, None],
                [{"colspan": 2}, None]
            ],
            vertical_spacing=0.08,
            horizontal_spacing=0.08
        )
        
        # 1. CDF Comparison
        fig.add_trace(
            go.Scatter(
                x=analysis_results['variant_a']['sorted'],
                y=analysis_results['variant_a']['cdf'],
                name='Variant A',
                line=dict(color='blue', width=3)
            ), row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=analysis_results['variant_b']['sorted'],
                y=analysis_results['variant_b']['cdf'],
                name='Variant B',
                line=dict(color='red', width=3)
            ), row=1, col=1
        )
        
        # 2. Probability Difference
        fig.add_trace(
            go.Scatter(
                x=analysis_results['probability_differences']['x_values'],
                y=analysis_results['probability_differences']['differences'],
                name='Probability Difference (B - A)',
                line=dict(color='green', width=2)
            ), row=1, col=2
        )
        
        # 3. Business Impact
        revenue_data = [
            business_impact['current_metrics']['daily_revenue'],
            business_impact['improved_metrics']['daily_revenue']
        ]
        
        fig.add_trace(
            go.Bar(
                x=['Current (A)', 'Improved (B)'],
                y=revenue_data,
                name='Daily Revenue',
                marker_color=['blue', 'red']
            ), row=2, col=1
        )
        
        # 4. Statistical Summary
        p_values = [
            analysis_results['statistical_tests']['ks_test']['p_value'],
            analysis_results['statistical_tests']['mann_whitney']['p_value']
        ]
        
        fig.add_trace(
            go.Bar(
                x=['KS Test', 'Mann-Whitney'],
                y=p_values,
                name='P-values',
                marker_color=['orange', 'purple']
            ), row=3, col=1
        )
        
        fig.update_layout(
            height=1200,
            title_text=f"Advanced A/B Test Analysis: {metric_name.title()}",
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_segment_comparison_plot(segment_results: dict):
        """Create visualization comparing results across segments"""
        segments = list(segment_results.keys())
        improvements = [segment_results[seg]['median_improvement'] * 100 for seg in segments]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=segments,
            y=improvements,
            marker_color=['red' if imp < 0 else 'green' for imp in improvements],
            text=[f"{imp:.1f}%" for imp in improvements],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Session Duration Improvement by User Segment",
            xaxis_title="User Segments",
            yaxis_title="Improvement (%)",
            showlegend=False
        )
        
        return fig