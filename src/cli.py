"""CLI interface for BlogAutoWriter."""

import sys
from pathlib import Path
from typing import List, Set
import logging

from .config import ConfigManager
from .generator import ArticleGenerator
from .utils import validate_title, create_title_slug


class CLIInterface:
    """Command-line interface for BlogAutoWriter."""
    
    def __init__(self, config_manager: ConfigManager, output_dir: str, logger: logging.Logger):
        self.config_manager = config_manager
        self.output_dir = Path(output_dir)
        self.logger = logger
        self.generator = ArticleGenerator(config_manager, logger)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self):
        """Run the CLI application."""
        self.logger.info("BlogAutoWriter を開始します")
        
        try:
            self._display_config()
            titles = self._collect_titles()
            
            if not titles:
                self.logger.warning("タイトルが入力されませんでした")
                return
            
            self._confirm_generation(titles)
            self._generate_articles(titles)
            
        except KeyboardInterrupt:
            self.logger.info("ユーザーによって中断されました")
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"予期しないエラーが発生しました: {e}")
            sys.exit(1)
    
    def _display_config(self):
        """Display current configuration."""
        print("=== BlogAutoWriter 設定 ===")
        print(f"モデル: {self.config_manager.get('openai.model')}")
        print(f"文体: {self.config_manager.get('prompt_settings.style')}")
        print(f"対象読者: {self.config_manager.get('prompt_settings.target_audience')}")
        print(f"出力先: {self.output_dir}")
        print("=" * 30)
        print()
    
    def _collect_titles(self) -> List[str]:
        """Collect article titles from user input."""
        print("記事タイトルを1行ずつ入力してください。")
        print("空行または 'END' で入力を終了します。")
        print()
        
        titles = []
        seen_titles: Set[str] = set()
        line_count = 0
        empty_line_count = 0
        
        while True:
            try:
                line = input(f"タイトル {len(titles) + 1}: ").strip()
                line_count += 1
                
                if not line:
                    empty_line_count += 1
                    if empty_line_count >= 2:
                        print("警告: 連続する空行が検出されました。入力を終了します。")
                        break
                    continue
                
                if line.upper() == 'END':
                    break
                
                empty_line_count = 0
                
                validation_error = validate_title(line)
                if validation_error:
                    print(f"エラー: {validation_error}")
                    continue
                
                if line in seen_titles:
                    print("警告: このタイトルは既に入力されています。別のタイトルを入力してください。")
                    continue
                
                titles.append(line)
                seen_titles.add(line)
                print(f"  → 追加されました: {line}")
                
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n入力が中断されました。")
                raise
        
        print(f"\n合計 {len(titles)} 件のタイトルが入力されました。")
        return titles
    
    def _confirm_generation(self, titles: List[str]):
        """Confirm article generation with user."""
        print("\n=== 生成対象タイトル ===")
        for i, title in enumerate(titles, 1):
            print(f"{i:2d}. {title}")
        print("=" * 30)
        
        while True:
            try:
                response = input("\n記事生成を開始しますか？ (y/N): ").strip().lower()
                if response in ['y', 'yes']:
                    break
                elif response in ['n', 'no', '']:
                    print("記事生成をキャンセルしました。")
                    sys.exit(0)
                else:
                    print("'y' または 'n' で答えてください。")
            except (EOFError, KeyboardInterrupt):
                print("\n記事生成をキャンセルしました。")
                sys.exit(0)
    
    def _generate_articles(self, titles: List[str]):
        """Generate articles for all titles."""
        self.logger.info(f"{len(titles)} 件の記事生成を開始します")
        
        try:
            results = self.generator.generate_articles(titles, self.output_dir)
            
            print("\n=== 生成結果 ===")
            successful = 0
            failed = 0
            
            for title, result in results.items():
                if result['success']:
                    successful += 1
                    print(f"✓ {title}")
                    print(f"  → {result['output_file']}")
                else:
                    failed += 1
                    print(f"✗ {title}")
                    print(f"  → エラー: {result['error']}")
            
            print("=" * 30)
            print(f"成功: {successful} 件, 失敗: {failed} 件")
            
            if successful > 0:
                print(f"\n生成されたファイルは {self.output_dir} に保存されました。")
            
            self.logger.info(f"記事生成完了: 成功 {successful} 件, 失敗 {failed} 件")
            
        except Exception as e:
            self.logger.error(f"記事生成中にエラーが発生しました: {e}")
            print(f"エラー: {e}")
            sys.exit(1)