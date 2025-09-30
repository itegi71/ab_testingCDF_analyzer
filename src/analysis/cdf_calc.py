# src/analysis/cdf_calculator.py
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union
from scipy import stats
import warnings

class CDFAnalyzer:
    """
    Comprehensive CDF analysis for A/B testing data
    """
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        
    def calculate_cdf(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate CDF for a given dataset
        
        Args:
            data: Array of numerical values
            
        Returns:
            sorted_data: Sorted values
            cdf_values: Corresponding CDF values
        """
        if len(data) == 0:
            raise ValueError("Data cannot be empty")
            
        sorted_data = np.sort(data)
        cdf_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        
        return sorted_data, cdf_values
    
    def compare_variants(self, variant_a: np.ndarray, variant_b: np.ndarray) -> Dict:
        """
        Comprehensive comparison of two variants using CDF analysis
        """
        # Calculate CDFs
        sorted_a, cdf_a = self.calculate_cdf(variant_a)
        sorted_b, cdf_b = self.calculate_cdf(variant_b)
        
        # Statistical tests
        ks_stat, ks_pvalue = stats.ks_2samp(variant_a, variant_b)
        mw_stat, mw_pvalue = stats.mannwhitneyu(variant_a, variant_b, alternative='two-sided')
        
        # Key percentiles
        percentiles = [10, 25, 50, 75, 90]
        perc_a = np.percentile(variant_a, percentiles)
        perc_b = np.percentile(variant_b, percentiles)
        
        # Probability differences at key thresholds
        prob_differences = {}
        common_range = np.linspace(
            max(min(variant_a), min(variant_b)),
            min(max(variant_a), max(variant_b)),
            1000
        )
        
        cdf_a_interp = np.interp(common_range, sorted_a, cdf_a)
        cdf_b_interp = np.interp(common_range, sorted_b, cdf_b)
        prob_diff = cdf_b_interp - cdf_a_interp
        
        return {
            'variant_a': {'sorted': sorted_a, 'cdf': cdf_a, 'size': len(variant_a)},
            'variant_b': {'sorted': sorted_b, 'cdf': cdf_b, 'size': len(variant_b)},
            'statistical_tests': {
                'ks_test': {'statistic': ks_stat, 'p_value': ks_pvalue},
                'mann_whitney': {'statistic': mw_stat, 'p_value': mw_pvalue}
            },
            'percentiles': {
                'values': percentiles,
                'variant_a': perc_a,
                'variant_b': perc_b
            },
            'probability_differences': {
                'x_values': common_range,
                'differences': prob_diff
            },
            'effect_size': self._calculate_effect_size(variant_a, variant_b)
        }
    
    def _calculate_effect_size(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate Cohen's d effect size"""
        return (np.mean(b) - np.mean(a)) / np.sqrt((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2)