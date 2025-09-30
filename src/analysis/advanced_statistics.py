# src/analysis/advanced_statistics.py
import numpy as np
from scipy import stats

class AdvancedStatistics:
    """Advanced statistical analysis for A/B testing"""
    
    @staticmethod
    def calculate_power_analysis(variant_a: np.ndarray, variant_b: np.ndarray, alpha: float = 0.05) -> dict:
        """Calculate statistical power for the A/B test"""
        effect_size = (np.mean(variant_b) - np.mean(variant_a)) / np.sqrt(
            (np.std(variant_a, ddof=1)**2 + np.std(variant_b, ddof=1)**2) / 2
        )
        
        n_obs = len(variant_a) + len(variant_b)
        
        # Simple power calculation (approximation)
        # For large samples, power ≈ 1 - β where β is from normal distribution
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_power = (effect_size * np.sqrt(n_obs/4)) - z_alpha
        power = stats.norm.cdf(z_power)
        
        # Required sample size for 80% power (approximation)
        z_beta = stats.norm.ppf(0.8)
        required_n = int(((z_alpha + z_beta) / effect_size) ** 2 * 4)
        
        return {
            'effect_size': effect_size,
            'current_power': max(0, min(power, 1)),  # Clamp between 0 and 1
            'required_sample_size_per_variant': required_n,
            'current_sample_size': n_obs
        }
    
    @staticmethod
    def bayesian_analysis(variant_a: np.ndarray, variant_b: np.ndarray) -> dict:
        """Bayesian analysis for probability of B being better than A"""
        # Simple Bayesian estimation using normal approximations
        mean_a, std_a = np.mean(variant_a), np.std(variant_a, ddof=1)
        mean_b, std_b = np.mean(variant_b), np.std(variant_b, ddof=1)
        
        # Probability that B > A
        delta_mean = mean_b - mean_a
        delta_std = np.sqrt(std_a**2/len(variant_a) + std_b**2/len(variant_b))
        prob_b_better = 1 - stats.norm.cdf(0, loc=delta_mean, scale=delta_std)
        
        return {
            'probability_b_better': prob_b_better,
            'credible_interval': stats.norm.interval(0.95, loc=delta_mean, scale=delta_std),
            'bayes_factor': prob_b_better / (1 - prob_b_better) if prob_b_better < 1 else float('inf')
        }