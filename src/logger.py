"""Logging setup for BlogAutoWriter."""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'title'):
            log_entry['title'] = record.title
        if hasattr(record, 'status'):
            log_entry['status'] = record.status
        if hasattr(record, 'error_type'):
            log_entry['error_type'] = record.error_type
            
        return json.dumps(log_entry, ensure_ascii=False)


def setup_logger(level: str = "INFO", enable_json: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger("BlogAutoWriter")
    logger.setLevel(getattr(logging, level.upper()))
    
    if logger.handlers:
        return logger
    
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    text_handler = logging.FileHandler(
        logs_dir / f"blog_auto_writer_{timestamp}.log",
        encoding='utf-8'
    )
    text_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    text_handler.setFormatter(text_formatter)
    logger.addHandler(text_handler)
    
    if enable_json:
        json_handler = logging.FileHandler(
            logs_dir / f"blog_auto_writer_{timestamp}.json",
            encoding='utf-8'
        )
        json_handler.setFormatter(JSONFormatter())
        logger.addHandler(json_handler)
    
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_title_processing(logger: logging.Logger, title: str, status: str, **kwargs):
    """Log title processing with structured data."""
    extra = {'title': title, 'status': status}
    extra.update(kwargs)
    
    if status == 'started':
        logger.info(f"記事生成開始: {title}", extra=extra)
    elif status == 'completed':
        logger.info(f"記事生成完了: {title}", extra=extra)
    elif status == 'failed':
        error_msg = kwargs.get('error', '不明なエラー')
        logger.error(f"記事生成失敗: {title} - {error_msg}", extra=extra)
    elif status == 'retrying':
        attempt = kwargs.get('attempt', 1)
        logger.warning(f"記事生成再試行 ({attempt}回目): {title}", extra=extra)