"""
Common utilities for the Jotica Bible project.
"""

import os
import json
import logging
import yaml
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_logging(log_file: Optional[str] = None, level: str = "INFO") -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_file: Optional log file path
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger
    """
    log_level = getattr(logging, level.upper())
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def save_json(data: Any, file_path: str, indent: int = 2) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Output file path
        indent: JSON indentation
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)

def load_json(file_path: str) -> Any:
    """
    Load data from JSON file.
    
    Args:
        file_path: JSON file path
    
    Returns:
        Loaded data
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def ensure_dir(directory: str) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory: Directory path
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def get_env_var(var_name: str, default: Optional[str] = None, required: bool = True) -> Optional[str]:
    """
    Get environment variable with validation.
    
    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
    
    Returns:
        Environment variable value
    
    Raises:
        ValueError: If required variable is missing
    """
    value = os.getenv(var_name, default)
    
    if required and not value:
        raise ValueError(f"Required environment variable '{var_name}' is not set")
    
    return value

def format_bible_reference(book: str, chapter: int, verse: int) -> str:
    """
    Format biblical reference consistently.
    
    Args:
        book: Book name
        chapter: Chapter number
        verse: Verse number
    
    Returns:
        Formatted reference (e.g., "Génesis 1:1")
    """
    return f"{book} {chapter}:{verse}"

def parse_bible_reference(reference: str) -> tuple[str, int, int]:
    """
    Parse biblical reference string.
    
    Args:
        reference: Reference string (e.g., "Génesis 1:1")
    
    Returns:
        Tuple of (book, chapter, verse)
    
    Raises:
        ValueError: If reference format is invalid
    """
    try:
        # Split on last space to handle multi-word book names
        parts = reference.rsplit(' ', 1)
        if len(parts) != 2:
            raise ValueError("Invalid reference format")
        
        book = parts[0]
        chapter_verse = parts[1]
        
        # Split chapter and verse
        chapter_str, verse_str = chapter_verse.split(':')
        chapter = int(chapter_str)
        verse = int(verse_str)
        
        return book, chapter, verse
        
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid bible reference format: {reference}") from e

def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing.
    
    Args:
        text: Raw text
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep punctuation
    # This is basic - you might want more sophisticated cleaning
    
    return text.strip()

def chunk_text(text: str, max_length: int = 512, overlap: int = 50) -> List[str]:
    """
    Chunk text into smaller pieces with overlap.
    
    Args:
        text: Text to chunk
        max_length: Maximum chunk length in characters
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_length
        
        # Find the last space before max_length to avoid cutting words
        if end < len(text):
            while end > start and text[end] != ' ':
                end -= 1
            
            # If no space found, use max_length
            if end == start:
                end = start + max_length
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        
        # Prevent infinite loop
        if start <= 0:
            start = max(1, end - overlap)
    
    return chunks

def validate_model_path(model_path: str) -> bool:
    """
    Validate if model path exists and contains required files.
    
    Args:
        model_path: Path to model directory
    
    Returns:
        True if valid model path
    """
    path_obj = Path(model_path)
    
    if not path_obj.exists():
        return False
    
    # Check for common model files
    required_files = ['config.json', 'pytorch_model.bin']
    alternative_files = ['model.safetensors']
    
    has_required = all((path_obj / file).exists() for file in required_files)
    has_alternative = any((path_obj / file).exists() for file in alternative_files)
    
    return has_required or (path_obj / 'config.json').exists() and has_alternative

def get_device() -> str:
    """
    Get the best available device (CUDA, MPS, or CPU).
    
    Returns:
        Device string
    """
    try:
        import torch
        
        if torch.cuda.is_available():
            return f"cuda:{torch.cuda.current_device()}"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    except ImportError:
        return "cpu"

class ConfigManager:
    """Configuration manager for the project."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = {}
        
        # Load default environment-based config
        self._load_env_config()
        
        # Load file-based config if provided
        if config_path and os.path.exists(config_path):
            file_config = load_config(config_path)
            self.config.update(file_config)
    
    def _load_env_config(self):
        """Load configuration from environment variables."""
        self.config.update({
            'openai_api_key': get_env_var('OPENAI_API_KEY', required=False),
            'supabase_url': get_env_var('SUPABASE_URL', required=False),
            'supabase_service_key': get_env_var('SUPABASE_SERVICE_KEY', required=False),
            'wandb_api_key': get_env_var('WANDB_API_KEY', required=False),
            'base_model': get_env_var('BASE_MODEL', 'microsoft/DialoGPT-medium', required=False) or 'microsoft/DialoGPT-medium',
            'max_length': int(get_env_var('MAX_LENGTH', '512', required=False) or '512'),
            'batch_size': int(get_env_var('BATCH_SIZE', '4', required=False) or '4'),
            'learning_rate': float(get_env_var('LEARNING_RATE', '2e-4', required=False) or '2e-4'),
            'num_epochs': int(get_env_var('NUM_EPOCHS', '5', required=False) or '5'),
            'lora_rank': int(get_env_var('LORA_RANK', '32', required=False) or '32'),
            'lora_alpha': int(get_env_var('LORA_ALPHA', '64', required=False) or '64'),
            'lora_dropout': float(get_env_var('LORA_DROPOUT', '0.1', required=False) or '0.1'),
            'bible_data_path': get_env_var('BIBLE_DATA_PATH', 'data/bible_rva1909', required=False) or 'data/bible_rva1909',
            'output_model_path': get_env_var('OUTPUT_MODEL_PATH', 'models/jotica-bible-lora', required=False) or 'models/jotica-bible-lora',
        })
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return self.config.copy()