"""Article generation logic for BlogAutoWriter."""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from .config import ConfigManager
from .openai_client import OpenAIClient
from .utils import create_output_filename, sanitize_markdown_content
from .logger import log_title_processing


class ArticleGenerator:
    """Handles article generation with parallel processing."""
    
    def __init__(self, config_manager: ConfigManager, logger: logging.Logger):
        self.config_manager = config_manager
        self.logger = logger
        self.openai_client = OpenAIClient(config_manager.config, logger)
        self.max_threads = config_manager.get('processing.max_threads', 10)
    
    def generate_articles(self, titles: List[str], output_dir: Path) -> Dict[str, Dict[str, Any]]:
        """Generate articles for multiple titles in parallel."""
        results = {}
        
        if not self.openai_client.test_connection():
            raise RuntimeError("OpenAI API接続に失敗しました")
        
        prompt_template = self.config_manager.get_prompt_template()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_title = {
                executor.submit(
                    self._generate_single_article, 
                    title, 
                    prompt_template, 
                    output_dir
                ): title 
                for title in titles
            }
            
            for future in as_completed(future_to_title):
                title = future_to_title[future]
                
                try:
                    result = future.result()
                    results[title] = result
                    
                    if result['success']:
                        log_title_processing(
                            self.logger, 
                            title, 
                            'completed',
                            output_file=result['output_file']
                        )
                    else:
                        log_title_processing(
                            self.logger, 
                            title, 
                            'failed',
                            error=result['error']
                        )
                        
                except Exception as e:
                    error_msg = f"予期しないエラー: {e}"
                    results[title] = {
                        'success': False,
                        'error': error_msg,
                        'output_file': None
                    }
                    log_title_processing(
                        self.logger, 
                        title, 
                        'failed',
                        error=error_msg
                    )
        
        return results
    
    def _generate_single_article(
        self, 
        title: str, 
        prompt_template: str, 
        output_dir: Path
    ) -> Dict[str, Any]:
        """Generate a single article."""
        log_title_processing(self.logger, title, 'started')
        
        try:
            content = self.openai_client.generate_article(prompt_template, title)
            
            if not content:
                return {
                    'success': False,
                    'error': 'OpenAI APIから有効な応答を取得できませんでした',
                    'output_file': None
                }
            
            sanitized_content = sanitize_markdown_content(content)
            
            filename = create_output_filename(title)
            output_file = output_dir / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)
            
            return {
                'success': True,
                'error': None,
                'output_file': str(output_file)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output_file': None
            }