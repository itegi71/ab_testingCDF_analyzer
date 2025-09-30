# src/data/data_generator.py
import numpy as np
import pandas as pd
from typing import Dict

class ABTestDataGenerator:
    """Generate realistic A/B testing data for demonstration"""
    
    @staticmethod
    def generate_session_durations(variant: str, n_samples: int = 1000) -> np.ndarray:
        """Generate realistic session duration data"""
        if variant == 'A':
            # Shorter sessions with some long tails
            base = np.random.exponential(120, n_samples)
            outliers = np.random.exponential(600, n_samples // 10)
            data = np.concatenate([base, outliers])
        else:  # variant B - hopefully better!
            base = np.random.exponential(180, n_samples)
            outliers = np.random.exponential(800, n_samples // 10)
            data = np.concatenate([base, outliers])
            
        return np.random.choice(data, n_samples, replace=False)
    
    @staticmethod
    def generate_conversion_times(variant: str, n_samples: int = 500) -> np.ndarray:
        """Generate conversion time data"""
        if variant == 'A':
            return np.random.lognormal(4.5, 0.8, n_samples)  # Slower conversions
        else:
            return np.random.lognormal(4.2, 0.7, n_samples)  # Faster conversions
    
    @staticmethod
    def create_sample_dataset() -> Dict:
        """Create a complete sample dataset for demonstration"""
        return {
            'session_duration': {
                'A': ABTestDataGenerator.generate_session_durations('A', 1500),
                'B': ABTestDataGenerator.generate_session_durations('B', 1500)
            },
            'conversion_time': {
                'A': ABTestDataGenerator.generate_conversion_times('A', 800),
                'B': ABTestDataGenerator.generate_conversion_times('B', 800)
            },
            'page_load_time': {
                'A': np.random.exponential(2.5, 2000),
                'B': np.random.exponential(2.0, 2000)
            }
        }