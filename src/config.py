"""Configuration management for BlogAutoWriter."""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration for BlogAutoWriter."""
    
    DEFAULT_CONFIG = {
        "prompt_settings": {
            "style": "丁寧で読みやすい文体",
            "stance": "中立的",
            "target_audience": "一般読者",
            "article_length": {
                "sections": 3,
                "words_per_section": 300
            }
        },
        "openai": {
            "model": "o4-mini",
            "temperature": 0.7,
            "max_tokens": 1000
        },
        "processing": {
            "max_threads": 10,
            "retry_attempts": 3,
            "retry_delay": 1.0
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if not self.config_path.exists():
            self._create_default_config()
            return self.DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                if self.config_path.suffix.lower() == '.yaml' or self.config_path.suffix.lower() == '.yml':
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            return self._merge_with_defaults(config)
        except Exception as e:
            raise ValueError(f"設定ファイルの読み込みに失敗しました: {e}")
    
    def _create_default_config(self):
        """Create default configuration file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with defaults."""
        merged = self.DEFAULT_CONFIG.copy()
        
        def deep_merge(default: dict, custom: dict):
            for key, value in custom.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    deep_merge(default[key], value)
                else:
                    default[key] = value
        
        deep_merge(merged, config)
        return merged
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by dot notation key."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save current configuration to file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            if self.config_path.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            else:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_prompt_template(self) -> str:
        """Generate prompt template based on configuration."""
        settings = self.config['prompt_settings']
        return f"""以下の設定に従って、与えられたタイトルについて記事を執筆してください。

文体・スタンス: {settings['style']}、{settings['stance']}
対象読者: {settings['target_audience']}
記事構成: {settings['article_length']['sections']}つの見出しで構成し、各セクション約{settings['article_length']['words_per_section']}文字

タイトル: {{title}}

Markdown形式で出力し、以下の構造を守ってください：
# タイトル
## 見出し1
内容...
## 見出し2
内容...
## 見出し3
内容..."""