"""OpenAI API client for BlogAutoWriter."""

import os
import time
import logging
import openai
from typing import Optional, Dict, Any


class OpenAIClient:
    """OpenAI API client with retry logic and error handling."""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        
        oai_key = os.getenv('OPENAI_API_KEY')
        if not oai_key:
            raise RuntimeError("OPENAI_API_KEY環境変数が設定されていません")
        
        openai.api_key = oai_key
        self.model = config.get('openai', {}).get('model', 'o4-mini')
        self.temperature = config.get('openai', {}).get('temperature', 0.7)
        self.max_completion_tokens = config.get('openai', {}).get('max_tokens', 1000)
        self.max_retries = config.get('processing', {}).get('retry_attempts', 3)
        self.retry_delay = config.get('processing', {}).get('retry_delay', 1.0)
    
    def generate_article(self, prompt: str, title: str) -> Optional[str]:
        """Generate article content using OpenAI API."""
        formatted_prompt = prompt.format(title=title)
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.debug(f"OpenAI API呼び出し (試行 {attempt}): {title}")
                
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたは優秀なブログライターです。与えられたタイトルと設定に従って、読みやすく有益な記事を書いてください。"
                        },
                        {
                            "role": "user",
                            "content": formatted_prompt
                        }
                    ],
                    max_completion_tokens=self.max_completion_tokens
                )
                
                content = response.choices[0].message.content
                if content:
                    content = content.strip()
                    self.logger.debug(f"記事生成成功: {title} ({len(content)} 文字)")
                    return content
                else:
                    self.logger.warning(f"空の応答を受信: {title}")
                    return "No response generated."
                    
            except Exception as e:
                error_type = type(e).__name__
                self.logger.warning(
                    f"API呼び出し失敗 (試行 {attempt}/{self.max_retries}): {title} - {error_type}: {e}"
                )
                
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                    self.logger.info(f"{delay} 秒待機後に再試行します...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"最大試行回数に達しました。記事生成失敗: {title}")
                    return None
        
        return None
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection."""
        try:
            self.logger.info("OpenAI API接続テストを実行中...")
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_completion_tokens=10
            )
            
            if response.choices and response.choices[0].message.content:
                self.logger.info("OpenAI API接続テスト成功")
                return True
            else:
                self.logger.error("OpenAI API接続テスト失敗: 空の応答")
                return False
                
        except Exception as e:
            self.logger.error(f"OpenAI API接続テスト失敗: {e}")
            return False