# src/analysis/segmentation.py
import numpy as np
import pandas as pd

class SegmentationAnalyzer:
    """Analyze A/B test results across different user segments"""
    
    def __init__(self):
        self.segments = ['new_users', 'returning_users', 'mobile_users', 'desktop_users']
    
    def create_segmented_data(self, base_data: dict, segment_sizes: dict) -> dict:
        """Create segmented data for analysis"""
        segmented_data = {}
        
        for segment in self.segments:
            size = segment_sizes.get(segment, 500)
            segmented_data[segment] = {
                'A': self._generate_segment_data(base_data['session_duration']['A'], size, segment),
                'B': self._generate_segment_data(base_data['session_duration']['B'], size, segment)
            }
        
        return segmented_data
    
    def _generate_segment_data(self, base_data: np.ndarray, size: int, segment: str) -> np.ndarray:
        """Generate data for specific segments with different characteristics"""
        if len(base_data) == 0:
            return np.array([])
            
        if segment == 'new_users':
            # New users typically have shorter sessions
            filtered_data = base_data[base_data < np.percentile(base_data, 40)]
            return filtered_data[:size] if len(filtered_data) > 0 else base_data[:size]
        elif segment == 'returning_users':
            # Returning users have longer sessions
            filtered_data = base_data[base_data > np.percentile(base_data, 60)]
            return filtered_data[:size] if len(filtered_data) > 0 else base_data[:size]
        elif segment == 'mobile_users':
            # Mobile users might have different patterns - FIXED BROADCASTING
            multiplier = np.random.uniform(0.8, 1.2, size)
            return base_data[:size] * multiplier
        else:  # desktop_users
            return base_data[:size]
    
    def analyze_segments(self, segmented_data: dict, analyzer) -> dict:
        """Analyze each segment separately"""
        segment_results = {}
        
        for segment, data in segmented_data.items():
            if len(data['A']) > 0 and len(data['B']) > 0:
                results = analyzer.compare_variants(data['A'], data['B'])
                
                # Calculate segment-specific metrics
                improvement = (np.median(data['B']) - np.median(data['A'])) / np.median(data['A'])
                
                segment_results[segment] = {
                    'analysis': results,
                    'median_improvement': improvement,
                    'sample_size': len(data['A'])
                }
        
        return segment_results