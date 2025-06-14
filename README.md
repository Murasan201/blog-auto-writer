# BlogAutoWriter

OpenAI APIを活用してブログ記事を自動生成するCLIツールです。

## 機能

- **タイトル入力**: CLIでタイトルを1行ずつ入力（空行またはENDで終了）
- **カスタムプロンプト**: 文体、対象読者、記事長さを設定可能
- **並列処理**: 最大10スレッドで効率的に記事生成
- **Markdown出力**: `{YYYYMMDD}_{タイトルスラッグ}.md`形式で保存
- **エラーハンドリング**: リトライ機能、レートリミット対応
- **ログ管理**: 詳細なログ出力とJSON形式対応

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. 設定ファイル（オプション）

初回実行時に `config.json` が自動生成されます。必要に応じて設定をカスタマイズしてください。

```json
{
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
```

## 使用方法

### 基本的な使用

```bash
python blog_auto_writer.py
```

### オプション付き実行

```bash
python blog_auto_writer.py --config my_config.json --outdir ./my_articles --log-level DEBUG
```

### 実行例

```
$ python blog_auto_writer.py
=== BlogAutoWriter 設定 ===
モデル: o4-mini
文体: 丁寧で読みやすい文体
対象読者: 一般読者
出力先: output
==============================

記事タイトルを1行ずつ入力してください。
空行または 'END' で入力を終了します。

タイトル 1: Pythonの基礎を学ぼう
  → 追加されました: Pythonの基礎を学ぼう
タイトル 2: 機械学習入門
  → 追加されました: 機械学習入門
タイトル 3: END

合計 2 件のタイトルが入力されました。

=== 生成対象タイトル ===
 1. Pythonの基礎を学ぼう
 2. 機械学習入門
==============================

記事生成を開始しますか？ (y/N): y

=== 生成結果 ===
✓ Pythonの基礎を学ぼう
  → output/20250614_Pythonの基礎を学ぼう.md
✓ 機械学習入門
  → output/20250614_機械学習入門.md
==============================
成功: 2 件, 失敗: 0 件

生成されたファイルは output に保存されました。
```

## コマンドラインオプション

- `--config`: 設定ファイルのパス（デフォルト: config.json）
- `--outdir`: 出力ディレクトリ（デフォルト: ./output）
- `--log-level`: ログレベル（DEBUG, INFO, WARNING, ERROR）

## ファイル構成

```
blog-auto-writer/
├── blog_auto_writer.py          # メインエントリーポイント
├── requirements.txt             # Python 依存関係
├── config.json                  # 設定ファイル（自動生成）
├── src/
│   ├── __init__.py
│   ├── cli.py                   # CLI インターフェース
│   ├── config.py                # 設定管理
│   ├── generator.py             # 記事生成ロジック
│   ├── openai_client.py         # OpenAI API クライアント
│   ├── logger.py                # ログ設定
│   └── utils.py                 # ユーティリティ関数
├── output/                      # 生成されたMarkdownファイル
└── logs/                        # ログファイル
```

## 要件

- Python 3.8以上
- OpenAI API キー
- インターネット接続

## ライセンス

MIT License - 詳細は LICENSE ファイルを参照してください。