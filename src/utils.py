"""Utility functions for BlogAutoWriter."""

import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional


def validate_title(title: str) -> Optional[str]:
    """Validate article title.
    
    Returns:
        None if valid, error message string if invalid.
    """
    if not title or not title.strip():
        return "タイトルが空です"
    
    if len(title) > 200:
        return "タイトルが200文字を超えています"
    
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in invalid_chars:
        if char in title:
            return f"無効な文字が含まれています: {char}"
    
    return None


def create_title_slug(title: str) -> str:
    """Create a URL-safe slug from title."""
    slug = title.strip()
    
    slug = unicodedata.normalize('NFKC', slug)
    
    slug = re.sub(r'[<>:"/\\|?*]', '', slug)
    
    slug = re.sub(r'[\s\u3000]+', '_', slug)
    
    slug = slug.strip('_')
    
    if len(slug) > 50:
        slug = slug[:50].rstrip('_')
    
    if not slug:
        slug = "untitled"
    
    return slug


def create_output_filename(title: str, date: Optional[datetime] = None) -> str:
    """Create output filename following the specified format."""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y%m%d")
    slug = create_title_slug(title)
    
    return f"{date_str}_{slug}.md"


def sanitize_markdown_content(content: str) -> str:
    """Sanitize and format markdown content."""
    lines = content.split('\n')
    sanitized_lines = []
    
    for line in lines:
        line = line.rstrip()
        
        if line.startswith('#'):
            if not line.startswith('# ') and not line.startswith('## '):
                if line.startswith('#'):
                    line = '# ' + line[1:].strip()
                elif line.startswith('##'):
                    line = '## ' + line[2:].strip()
        
        sanitized_lines.append(line)
    
    content = '\n'.join(sanitized_lines)
    
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()


def ensure_directory_exists(path: Path) -> bool:
    """Ensure directory exists, create if necessary."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def is_valid_output_directory(path: str) -> bool:
    """Check if output directory path is valid and writable."""
    try:
        output_path = Path(path)
        
        if output_path.exists() and not output_path.is_dir():
            return False
        
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        
        test_file = output_path / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        
        return True
    except Exception:
        return False