# src/analysis/business_impact.py
import numpy as np

class BusinessImpactCalculator:
    """Calculate business impact of A/B test results"""
    
    def __init__(self, conversion_rate: float = 0.05, avg_order_value: float = 100, 
                 daily_users: int = 10000, test_duration_days: int = 30):
        self.conversion_rate = conversion_rate
        self.avg_order_value = avg_order_value
        self.daily_users = daily_users
        self.test_duration_days = test_duration_days
    
    def calculate_revenue_impact(self, analysis_results: dict, metric_type: str = 'session_duration') -> dict:
        """Calculate expected revenue impact of implementing Variant B"""
        
        # Estimate conversion rate improvement based on session duration increase
        duration_improvement = self._estimate_conversion_improvement(analysis_results)
        
        # Current metrics
        current_conversions = self.daily_users * self.conversion_rate
        current_revenue = current_conversions * self.avg_order_value
        
        # Improved metrics
        improved_conversion_rate = self.conversion_rate * (1 + duration_improvement)
        improved_conversions = self.daily_users * improved_conversion_rate
        improved_revenue = improved_conversions * self.avg_order_value
        
        # Annual impact
        daily_improvement = improved_revenue - current_revenue
        annual_improvement = daily_improvement * 365
        
        return {
            'current_metrics': {
                'conversion_rate': self.conversion_rate,
                'daily_conversions': current_conversions,
                'daily_revenue': current_revenue
            },
            'improved_metrics': {
                'conversion_rate': improved_conversion_rate,
                'daily_conversions': improved_conversions,
                'daily_revenue': improved_revenue
            },
            'improvement': {
                'conversion_rate_improvement': duration_improvement,
                'daily_revenue_improvement': daily_improvement,
                'annual_revenue_improvement': annual_improvement,
                'percentage_improvement': (improved_revenue / current_revenue - 1) * 100
            }
        }
    
    def _estimate_conversion_improvement(self, analysis_results: dict) -> float:
        """Estimate conversion rate improvement based on session duration increase"""
        # Empirical relationship: longer sessions → higher conversion rates
        median_a = analysis_results['percentiles']['variant_a'][2]  # 50th percentile
        median_b = analysis_results['percentiles']['variant_b'][2]
        
        # Simple model: 1% conversion improvement per 10% session duration increase
        duration_increase = (median_b - median_a) / median_a
        conversion_improvement = duration_increase * 0.1  # 10% of duration improvement
        
        return max(0, min(conversion_improvement, 0.5))  # Cap at 50% improvement