# src/data/real_world_importers.py
import pandas as pd
import numpy as np
import json
from typing import Dict, List, Optional, Union
from pathlib import Path
import warnings

class DataImporters:
    """
    Import and convert real-world A/B testing data from various sources
    to our standardized format for CDF analysis.
    """
    
    def __init__(self):
        self.supported_sources = ['google_analytics', 'optimizely', 'amplitude', 'mixpanel', 'csv']
    
    def validate_data_structure(self, data: Dict, source: str) -> bool:
        """Validate that imported data has the correct structure"""
        required_keys = ['variant_a', 'variant_b', 'metric_name']
        
        if not all(key in data for key in required_keys):
            raise ValueError(f"Missing required keys. Expected: {required_keys}")
        
        if len(data['variant_a']) == 0 or len(data['variant_b']) == 0:
            raise ValueError("Variant data cannot be empty")
            
        return True
    
    def get_supported_sources(self) -> List[str]:
        """Return list of supported data sources"""
        return self.supported_sources

    def import_from_csv(self, file_path: str, 
                      variant_column: str,
                      metric_column: str,
                      control_value: str = 'A',
                      treatment_value: str = 'B') -> Dict:
        """
        Import A/B test data from CSV file
        """
        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            df = pd.read_csv(file_path)
            
            # Validate required columns
            required_columns = [variant_column, metric_column]
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing columns in CSV: {missing_cols}")
            
            # Extract variant data
            control_data = df[df[variant_column] == control_value][metric_column].dropna().values
            treatment_data = df[df[variant_column] == treatment_value][metric_column].dropna().values
            
            if len(control_data) == 0:
                raise ValueError(f"No data found for control variant '{control_value}'")
            if len(treatment_data) == 0:
                raise ValueError(f"No data found for treatment variant '{treatment_value}'")
            
            # Clean the data
            control_data = self._clean_metric_data(control_data)
            treatment_data = self._clean_metric_data(treatment_data)
            
            result = {
                'variant_a': control_data,
                'variant_b': treatment_data,
                'metric_name': metric_column,
                'source': 'csv',
                'file_path': file_path,
                'sample_sizes': {
                    'control': len(control_data),
                    'treatment': len(treatment_data)
                },
                'data_quality': {
                    'control_missing_removed': len(df[df[variant_column] == control_value]) - len(control_data),
                    'treatment_missing_removed': len(df[df[variant_column] == treatment_value]) - len(treatment_data)
                }
            }
            
            self.validate_data_structure(result, 'csv')
            return result
            
        except Exception as e:
            raise ValueError(f"Error importing CSV data: {str(e)}")

    def _clean_metric_data(self, data: np.ndarray, 
                         outlier_threshold: float = 3.0) -> np.ndarray:
        """
        Clean metric data by handling outliers and extreme values
        """
        if len(data) == 0:
            return data
        
        # Remove NaN values
        clean_data = data[~np.isnan(data)]
        
        # Remove extreme outliers using IQR method
        if len(clean_data) > 10:  # Only if we have enough data
            Q1 = np.percentile(clean_data, 25)
            Q3 = np.percentile(clean_data, 75)
            IQR = Q3 - Q1
            lower_bound = Q1 - outlier_threshold * IQR
            upper_bound = Q3 + outlier_threshold * IQR
            
            clean_data = clean_data[(clean_data >= lower_bound) & (clean_data <= upper_bound)]
        
        return clean_data

    def get_import_summary(self, imported_data: Dict) -> str:
        """Generate a summary of imported data"""
        control_mean = np.mean(imported_data['variant_a']) if len(imported_data['variant_a']) > 0 else 0
        treatment_mean = np.mean(imported_data['variant_b']) if len(imported_data['variant_b']) > 0 else 0
        
        summary = f"""
 Data Import Summary
────────────────────
Source: {imported_data.get('source', 'unknown')}
Metric: {imported_data.get('metric_name', 'unknown')}
Sample Sizes: 
  - Control (A): {len(imported_data['variant_a']):,}
  - Treatment (B): {len(imported_data['variant_b']):,}
Data Quality:
  - Control Mean: {control_mean:.2f}
  - Treatment Mean: {treatment_mean:.2f}
  - Control Missing Removed: {imported_data.get('data_quality', {}).get('control_missing_removed', 0)}
  - Treatment Missing Removed: {imported_data.get('data_quality', {}).get('treatment_missing_removed', 0)}
────────────────────
"""
        return summary
