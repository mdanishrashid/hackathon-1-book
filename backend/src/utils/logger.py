import logging
from typing import Any, Dict
import json
from datetime import datetime

class AppLogger:
    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        log_data = self._format_log_data(message, extra)
        self.logger.info(log_data)
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        log_data = self._format_log_data(message, extra)
        self.logger.error(log_data)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        log_data = self._format_log_data(message, extra)
        self.logger.warning(log_data)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        log_data = self._format_log_data(message, extra)
        self.logger.debug(log_data)
    
    def _format_log_data(self, message: str, extra: Dict[str, Any] = None) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "extra": extra or {}
        }
        return json.dumps(log_entry)