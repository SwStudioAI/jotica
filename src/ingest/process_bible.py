"""
Process raw Bible texts and prepare for training.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

from ..utils import setup_logging, ensure_dir, save_json, BibleProcessor, ConfigManager

# Setup logging
logger = setup_logging()

def process_rva1909_text(input_path: str, output_dir: str) -> None:
    """
    Process raw RVA 1909 Bible text files.
    
    Args:
        input_path: Path to raw text files
        output_dir: Output directory for processed JSON
    """
    logger.info(f"Processing RVA 1909 text from {input_path}")
    
    input_dir = Path(input_path)
    output_path = Path(output_dir)
    ensure_dir(str(output_path))
    
    if not input_dir.exists():
        logger.warning(f"Input directory does not exist: {input_path}")
        return
    
    # Process text files
    text_files = list(input_dir.glob("*.txt"))
    
    for text_file in text_files:
        logger.info(f"Processing {text_file.name}")
        verses = parse_bible_text_file(str(text_file))
        
        if verses:
            output_file = output_path / f"{text_file.stem}.json"
            save_json(verses, str(output_file))
            logger.info(f"Saved {len(verses)} verses to {output_file}")

def parse_bible_text_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a Bible text file and extract verses.
    
    Args:
        file_path: Path to text file
    
    Returns:
        List of verse dictionaries
    """
    verses = []
    current_book = ""
    current_chapter = 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Try to parse different formats
            verse_data = None
            
            # Format: "Genesis 1:1 En el principio..."
            if ':' in line and any(char.isdigit() for char in line):
                verse_data = parse_reference_format(line)
            
            # Format: "1:1 En el principio..." (book set separately)
            elif line.startswith(tuple('123456789')):
                verse_data = parse_chapter_verse_format(line, current_book, current_chapter)
            
            # Format: "GENESIS" (book header)
            elif line.isupper() and not any(char.isdigit() for char in line):
                current_book = normalize_book_name(line)
                current_chapter = 1
                continue
            
            # Format: "Capítulo 1" (chapter header)
            elif line.lower().startswith('capítulo') or line.lower().startswith('chapter'):
                try:
                    # Update current chapter for subsequent verse parsing
                    chapter_num = int(line.split()[-1])
                    current_chapter = chapter_num
                except ValueError:
                    pass
                continue
            
            if verse_data:
                verses.append(verse_data)
                if verse_data['book']:
                    current_book = verse_data['book']
        
    except Exception as e:
        logger.error(f"Error parsing {file_path}: {e}")
    
    return verses

def parse_reference_format(line: str) -> Dict[str, Any]:
    """Parse line in format 'Book Chapter:Verse Text'."""
    try:
        # Find the first colon
        colon_idx = line.find(':')
        if colon_idx == -1:
            return {}
        
        # Find the last space before the colon (should be chapter number)
        space_before_colon = line.rfind(' ', 0, colon_idx)
        if space_before_colon == -1:
            return {}
        
        book = line[:space_before_colon].strip()
        chapter = int(line[space_before_colon:colon_idx].strip())
        
        # Find the verse number and text
        after_colon = line[colon_idx + 1:].strip()
        verse_end = 0
        
        for i, char in enumerate(after_colon):
            if not char.isdigit():
                break
            verse_end = i + 1
        
        if verse_end == 0:
            return {}
        
        verse = int(after_colon[:verse_end])
        text = after_colon[verse_end:].strip()
        
        return {
            'book': normalize_book_name(book),
            'chapter': chapter,
            'verse': verse,
            'text': text
        }
        
    except (ValueError, IndexError):
        return {}

def parse_chapter_verse_format(line: str, current_book: str, fallback_chapter: int = 1) -> Dict[str, Any]:
    """Parse line in format 'Chapter:Verse Text'."""
    try:
        colon_idx = line.find(':')
        if colon_idx == -1:
            return {}
        
        chapter = int(line[:colon_idx].strip())
        
        after_colon = line[colon_idx + 1:].strip()
        verse_end = 0
        
        for i, char in enumerate(after_colon):
            if not char.isdigit():
                break
            verse_end = i + 1
        
        if verse_end == 0:
            return {}
        
        verse = int(after_colon[:verse_end])
        text = after_colon[verse_end:].strip()
        
        return {
            'book': current_book,
            'chapter': chapter,
            'verse': verse,
            'text': text
        }
        
    except (ValueError, IndexError):
        return {}

def normalize_book_name(book: str) -> str:
    """
    Normalize book name to standard Spanish names.
    
    Args:
        book: Raw book name
    
    Returns:
        Normalized book name
    """
    book_mappings = {
        'GENESIS': 'Génesis',
        'GÉNESIS': 'Génesis',
        'EXODO': 'Éxodo',
        'ÉXODO': 'Éxodo',
        'EXODUS': 'Éxodo',
        'LEVITICO': 'Levítico',
        'LEVÍTICO': 'Levítico',
        'LEVITICUS': 'Levítico',
        'NUMEROS': 'Números',
        'NÚMEROS': 'Números',
        'NUMBERS': 'Números',
        'DEUTERONOMIO': 'Deuteronomio',
        'DEUTERONOMY': 'Deuteronomio',
        'JOSUE': 'Josué',
        'JOSUÉ': 'Josué',
        'JOSHUA': 'Josué',
        'JUECES': 'Jueces',
        'JUDGES': 'Jueces',
        'RUT': 'Rut',
        'RUTH': 'Rut',
        '1 SAMUEL': '1 Samuel',
        '1SAMUEL': '1 Samuel',
        '2 SAMUEL': '2 Samuel',
        '2SAMUEL': '2 Samuel',
        '1 REYES': '1 Reyes',
        '1REYES': '1 Reyes',
        '1 KINGS': '1 Reyes',
        '2 REYES': '2 Reyes',
        '2REYES': '2 Reyes',
        '2 KINGS': '2 Reyes',
        '1 CRONICAS': '1 Crónicas',
        '1CRONICAS': '1 Crónicas',
        '1 CRÓNICAS': '1 Crónicas',
        '1 CHRONICLES': '1 Crónicas',
        '2 CRONICAS': '2 Crónicas',
        '2CRONICAS': '2 Crónicas',
        '2 CRÓNICAS': '2 Crónicas',
        '2 CHRONICLES': '2 Crónicas',
        'ESDRAS': 'Esdras',
        'EZRA': 'Esdras',
        'NEHEMIAS': 'Nehemías',
        'NEHEMÍAS': 'Nehemías',
        'NEHEMIAH': 'Nehemías',
        'ESTER': 'Ester',
        'ESTHER': 'Ester',
        'JOB': 'Job',
        'SALMOS': 'Salmos',
        'PSALMS': 'Salmos',
        'PROVERBIOS': 'Proverbios',
        'PROVERBS': 'Proverbios',
        'ECLESIASTES': 'Eclesiastés',
        'ECCLESIASTES': 'Eclesiastés',
        'CANTARES': 'Cantares',
        'SONG OF SOLOMON': 'Cantares',
        'SONG OF SONGS': 'Cantares',
        'ISAIAS': 'Isaías',
        'ISAÍAS': 'Isaías',
        'ISAIAH': 'Isaías',
        'JEREMIAS': 'Jeremías',
        'JEREMÍAS': 'Jeremías',
        'JEREMIAH': 'Jeremías',
        'LAMENTACIONES': 'Lamentaciones',
        'LAMENTATIONS': 'Lamentaciones',
        'EZEQUIEL': 'Ezequiel',
        'EZEKIEL': 'Ezequiel',
        'DANIEL': 'Daniel',
        'OSEAS': 'Oseas',
        'HOSEA': 'Oseas',
        'JOEL': 'Joel',
        'AMOS': 'Amós',
        'AMÓS': 'Amós',
        'ABDIAS': 'Abdías',
        'ABDÍAS': 'Abdías',
        'OBADIAH': 'Abdías',
        'JONAS': 'Jonás',
        'JONÁS': 'Jonás',
        'JONAH': 'Jonás',
        'MIQUEAS': 'Miqueas',
        'MICAH': 'Miqueas',
        'NAHUM': 'Nahum',
        'HABACUC': 'Habacuc',
        'HABAKKUK': 'Habacuc',
        'SOFONIAS': 'Sofonías',
        'SOFONÍAS': 'Sofonías',
        'ZEPHANIAH': 'Sofonías',
        'HAGEO': 'Hageo',
        'HAGGAI': 'Hageo',
        'ZACARIAS': 'Zacarías',
        'ZACARÍAS': 'Zacarías',
        'ZECHARIAH': 'Zacarías',
        'MALAQUIAS': 'Malaquías',
        'MALAQUÍAS': 'Malaquías',
        'MALACHI': 'Malaquías',
        'MATEO': 'Mateo',
        'MATTHEW': 'Mateo',
        'MARCOS': 'Marcos',
        'MARK': 'Marcos',
        'LUCAS': 'Lucas',
        'LUKE': 'Lucas',
        'JUAN': 'Juan',
        'JOHN': 'Juan',
        'HECHOS': 'Hechos',
        'ACTS': 'Hechos',
        'ROMANOS': 'Romanos',
        'ROMANS': 'Romanos',
        '1 CORINTIOS': '1 Corintios',
        '1CORINTIOS': '1 Corintios',
        '1 CORINTHIANS': '1 Corintios',
        '2 CORINTIOS': '2 Corintios',
        '2CORINTIOS': '2 Corintios',
        '2 CORINTHIANS': '2 Corintios',
        'GALATAS': 'Gálatas',
        'GÁLATAS': 'Gálatas',
        'GALATIANS': 'Gálatas',
        'EFESIOS': 'Efesios',
        'EPHESIANS': 'Efesios',
        'FILIPENSES': 'Filipenses',
        'PHILIPPIANS': 'Filipenses',
        'COLOSENSES': 'Colosenses',
        'COLOSSIANS': 'Colosenses',
        '1 TESALONICENSES': '1 Tesalonicenses',
        '1TESALONICENSES': '1 Tesalonicenses',
        '1 THESSALONIANS': '1 Tesalonicenses',
        '2 TESALONICENSES': '2 Tesalonicenses',
        '2TESALONICENSES': '2 Tesalonicenses',
        '2 THESSALONIANS': '2 Tesalonicenses',
        '1 TIMOTEO': '1 Timoteo',
        '1TIMOTEO': '1 Timoteo',
        '1 TIMOTHY': '1 Timoteo',
        '2 TIMOTEO': '2 Timoteo',
        '2TIMOTEO': '2 Timoteo',
        '2 TIMOTHY': '2 Timoteo',
        'TITO': 'Tito',
        'TITUS': 'Tito',
        'FILEMON': 'Filemón',
        'FILEMÓN': 'Filemón',
        'PHILEMON': 'Filemón',
        'HEBREOS': 'Hebreos',
        'HEBREWS': 'Hebreos',
        'SANTIAGO': 'Santiago',
        'JAMES': 'Santiago',
        '1 PEDRO': '1 Pedro',
        '1PEDRO': '1 Pedro',
        '1 PETER': '1 Pedro',
        '2 PEDRO': '2 Pedro',
        '2PEDRO': '2 Pedro',
        '2 PETER': '2 Pedro',
        '1 JUAN': '1 Juan',
        '1JUAN': '1 Juan',
        '1 JOHN': '1 Juan',
        '2 JUAN': '2 Juan',
        '2JUAN': '2 Juan',
        '2 JOHN': '2 Juan',
        '3 JUAN': '3 Juan',
        '3JUAN': '3 Juan',
        '3 JOHN': '3 Juan',
        'JUDAS': 'Judas',
        'JUDE': 'Judas',
        'APOCALIPSIS': 'Apocalipsis',
        'REVELATION': 'Apocalipsis',
        'REVELATIONS': 'Apocalipsis'
    }
    
    return book_mappings.get(book.upper().strip(), book.title())

def create_training_data(config_path: Optional[str] = None) -> None:
    """
    Create processed training data from Bible texts.
    
    Args:
        config_path: Optional configuration file path
    """
    config = ConfigManager(config_path)
    
    input_path = config.get('raw_text_path', 'data/raw_text')
    output_path = config.get('bible_data_path', 'data/bible_rva1909')
    
    logger.info("Starting Bible text processing pipeline")
    
    # Process raw text files
    process_rva1909_text(input_path, output_path)
    
    # Load and validate processed data
    bible = BibleProcessor(output_path)
    try:
        bible.load_bible_data()
        stats = bible.get_statistics()
        
        logger.info("Bible processing completed successfully")
        logger.info(f"Total verses: {stats['total_verses']}")
        logger.info(f"Total books: {stats['total_books']}")
        logger.info(f"Old Testament books: {stats['old_testament_books']}")
        logger.info(f"New Testament books: {stats['new_testament_books']}")
        
        # Export to text format for inspection
        text_output = Path(output_path) / "bible_complete.txt"
        bible.export_to_text(str(text_output), "reference")
        logger.info(f"Exported complete Bible to {text_output}")
        
    except Exception as e:
        logger.error(f"Error loading processed Bible data: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    config_file = sys.argv[1] if len(sys.argv) > 1 else None
    create_training_data(config_file)