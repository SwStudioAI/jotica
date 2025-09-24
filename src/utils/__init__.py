"""
Utility modules for the Jotica Bible project.
"""

from .common import (
    setup_logging,
    load_config,
    save_json,
    load_json,
    ensure_dir,
    get_env_var,
    format_bible_reference,
    parse_bible_reference,
    clean_text,
    chunk_text,
    validate_model_path,
    get_device,
    ConfigManager
)

from .bible import (
    BibleVerse,
    BiblePassage,
    BibleProcessor
)

__all__ = [
    # Common utilities
    'setup_logging',
    'load_config',
    'save_json',
    'load_json',
    'ensure_dir',
    'get_env_var',
    'format_bible_reference',
    'parse_bible_reference',
    'clean_text',
    'chunk_text',
    'validate_model_path',
    'get_device',
    'ConfigManager',
    
    # Bible processing
    'BibleVerse',
    'BiblePassage',
    'BibleProcessor',
]