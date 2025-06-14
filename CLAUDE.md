# BlogAutoWriter - Claude Code Configuration

## Project Overview
- **Name**: BlogAutoWriter
- **Version**: 1.1
- **Language**: Python 3.8+
- **Purpose**: CLI tool for automated blog post generation using OpenAI API
- **Requirements**: All development must follow the specifications in `BlogAutoWriter-Requirements-Specification.md`

## Development Rules
- **IMPORTANT**: Always refer to `BlogAutoWriter-Requirements-Specification.md` for requirements and specifications
- All features and implementations must comply with the requirements document
- Any changes or additions should align with the defined functional and non-functional requirements
- Follow the specified CLI interface, file formats, and system architecture as documented
- **OpenAI API Reference**: Use the implementation pattern from https://github.com/Murasan201/openai-text-generator/blob/main/generate_text.py as reference for API calls
- Use `o4-mini` model and follow the established error handling and response processing patterns

## Development Commands
```bash
# Run the application
python blog_auto_writer.py [--config config.json] [--outdir ./output]

# Install dependencies
pip install -r requirements.txt

# Run tests (when implemented)
python -m pytest tests/

# Code formatting
black src/ blog_auto_writer.py
flake8 src/ blog_auto_writer.py

# Type checking
mypy src/ blog_auto_writer.py
```

## Project Structure
```
blog-auto-writer/
├── blog_auto_writer.py          # Main entry point
├── requirements.txt             # Python dependencies
├── config.json                  # Default configuration
├── src/
│   ├── __init__.py
│   ├── cli.py                   # CLI interface
│   ├── config.py                # Configuration management
│   ├── generator.py             # Article generation logic
│   ├── openai_client.py         # OpenAI API client
│   ├── logger.py                # Logging setup
│   └── utils.py                 # Utility functions
├── output/                      # Generated markdown files
├── logs/                        # Log files
└── tests/                       # Unit tests
```

## Key Features
1. CLI-based title input with validation
2. Customizable prompt templates (JSON/YAML)
3. OpenAI API integration (o4-mini, gpt-3.5-turbo, gpt-4)
4. Parallel processing (max 10 threads)
5. Markdown output with proper formatting
6. Comprehensive logging and error handling
7. Resume functionality for interrupted processes

## Configuration
- API key: Set `OPENAI_API_KEY` environment variable
- Default model: o4-mini
- Output format: `{YYYYMMDD}_{title_slug}.md`
- Log levels: DEBUG, INFO, WARNING, ERROR

## Dependencies
- openai
- pyyaml
- click or argparse
- python-dotenv
- concurrent.futures (built-in)
- pathlib (built-in)

## Error Handling
- API retry logic (max 3 attempts)
- Rate limit handling with backoff
- Input validation and sanitization
- Graceful shutdown on interruption