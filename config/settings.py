# config/settings.py
import os
from dataclasses import dataclass

@dataclass
class Settings:
    PROJECT_NAME: str = "AB Testing CDF Analyzer"
    VERSION: str = "1.0.0"
    DEFAULT_SAMPLE_SIZE: int = 1000
    CONFIDENCE_LEVEL: float = 0.95
    KEY_THRESHOLDS: dict = None
    
    def __post_init__(self):
        if self.KEY_THRESHOLDS is None:
            self.KEY_THRESHOLDS = {
                'session_duration': [30, 60, 180, 300],  # seconds
                'conversion_time': [60, 120, 300, 600],
                'page_load_time': [1, 3, 5]  # seconds
            }

settings = Settings()