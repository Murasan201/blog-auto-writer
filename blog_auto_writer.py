#!/usr/bin/env python3
"""
BlogAutoWriter - Automated blog post generation using OpenAI API
Author: Murasan
Version: 1.1
"""

import argparse
import sys
from pathlib import Path

from src.cli import CLIInterface
from src.config import ConfigManager
from src.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(
        description="Generate blog posts automatically using OpenAI API"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Configuration file path (default: config.json)"
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="./output",
        help="Output directory for generated markdown files (default: ./output)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    logger = setup_logger(args.log_level)
    
    try:
        config_manager = ConfigManager(args.config)
        cli = CLIInterface(config_manager, args.outdir, logger)
        cli.run()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()