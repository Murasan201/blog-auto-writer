# BlogAutoWriter

A CLI tool for automated blog post generation using OpenAI API.

## Features

- **Title Input**: CLI-based title input line by line (terminate with empty line or 'END')
- **Custom Prompts**: Configurable writing style, target audience, and article length
- **Parallel Processing**: Efficient article generation with up to 10 threads
- **Markdown Output**: Save as `{YYYYMMDD}_{title_slug}.md` format
- **Error Handling**: Retry functionality and rate limit handling
- **Logging**: Detailed logging with text and JSON format support

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variable

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Configuration File (Optional)

A `config.json` file will be automatically generated on first run. Customize settings as needed.

```json
{
  "prompt_settings": {
    "style": "Polite and readable writing style",
    "stance": "Neutral",
    "target_audience": "General readers",
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

## Usage

### Basic Usage

```bash
python blog_auto_writer.py
```

### Usage with Options

```bash
python blog_auto_writer.py --config my_config.json --outdir ./my_articles --log-level DEBUG
```

### Example Session

```
$ python blog_auto_writer.py
=== BlogAutoWriter Configuration ===
Model: o4-mini
Style: Polite and readable writing style
Target Audience: General readers
Output Directory: output
==============================

Enter article titles one per line.
End input with empty line or 'END'.

Title 1: Learn Python Basics
  → Added: Learn Python Basics
Title 2: Introduction to Machine Learning
  → Added: Introduction to Machine Learning
Title 3: END

Total 2 titles entered.

=== Target Titles ===
 1. Learn Python Basics
 2. Introduction to Machine Learning
==============================

Start article generation? (y/N): y

=== Generation Results ===
✓ Learn Python Basics
  → output/20250614_Learn_Python_Basics.md
✓ Introduction to Machine Learning
  → output/20250614_Introduction_to_Machine_Learning.md
==============================
Success: 2 articles, Failed: 0 articles

Generated files are saved to output directory.
```

## Command Line Options

- `--config`: Configuration file path (default: config.json)
- `--outdir`: Output directory (default: ./output)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## File Structure

```
blog-auto-writer/
├── blog_auto_writer.py          # Main entry point
├── requirements.txt             # Python dependencies
├── config.json                  # Configuration file (auto-generated)
├── src/
│   ├── __init__.py
│   ├── cli.py                   # CLI interface
│   ├── config.py                # Configuration management
│   ├── generator.py             # Article generation logic
│   ├── openai_client.py         # OpenAI API client
│   ├── logger.py                # Logging setup
│   └── utils.py                 # Utility functions
├── output/                      # Generated markdown files
└── logs/                        # Log files
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection

## Developer

Created by [Murasan](https://murasan-net.com/)

## License

MIT License - See LICENSE file for details.