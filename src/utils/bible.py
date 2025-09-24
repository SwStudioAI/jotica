"""
Bible text processing utilities for the Jotica Bible project.
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass

from .common import setup_logging, clean_text, format_bible_reference

# Setup logging
logger = setup_logging()

@dataclass
class BibleVerse:
    """Represents a single Bible verse."""
    book: str
    chapter: int
    verse: int
    text: str
    reference: str = ""
    
    def __post_init__(self):
        """Generate reference after initialization."""
        if not self.reference:
            self.reference = format_bible_reference(self.book, self.chapter, self.verse)

@dataclass
class BiblePassage:
    """Represents a Bible passage with multiple verses."""
    verses: List[BibleVerse]
    book: str
    chapter: int
    start_verse: int
    end_verse: int
    
    @property
    def reference(self) -> str:
        """Get formatted reference for the passage."""
        if self.start_verse == self.end_verse:
            return format_bible_reference(self.book, self.chapter, self.start_verse)
        else:
            return f"{self.book} {self.chapter}:{self.start_verse}-{self.end_verse}"
    
    @property
    def text(self) -> str:
        """Get combined text of all verses."""
        return " ".join(verse.text for verse in self.verses)

class BibleProcessor:
    """Process and manage Bible text data."""
    
    def __init__(self, data_path: str = "data/bible_rva1909"):
        """
        Initialize Bible processor.
        
        Args:
            data_path: Path to Bible data directory
        """
        self.data_path = Path(data_path)
        self.verses: List[BibleVerse] = []
        self.books: Dict[str, List[BibleVerse]] = {}
        self.chapters: Dict[str, Dict[int, List[BibleVerse]]] = {}
        
        # Spanish Bible book mappings
        self.book_names = {
            "genesis": "Génesis",
            "exodo": "Éxodo", 
            "levitico": "Levítico",
            "numeros": "Números",
            "deuteronomio": "Deuteronomio",
            "josue": "Josué",
            "jueces": "Jueces",
            "rut": "Rut",
            "1samuel": "1 Samuel",
            "2samuel": "2 Samuel",
            "1reyes": "1 Reyes",
            "2reyes": "2 Reyes",
            "1cronicas": "1 Crónicas",
            "2cronicas": "2 Crónicas",
            "esdras": "Esdras",
            "nehemias": "Nehemías",
            "ester": "Ester",
            "job": "Job",
            "salmos": "Salmos",
            "proverbios": "Proverbios",
            "eclesiastes": "Eclesiastés",
            "cantares": "Cantares",
            "isaias": "Isaías",
            "jeremias": "Jeremías",
            "lamentaciones": "Lamentaciones",
            "ezequiel": "Ezequiel",
            "daniel": "Daniel",
            "oseas": "Oseas",
            "joel": "Joel",
            "amos": "Amós",
            "abdias": "Abdías",
            "jonas": "Jonás",
            "miqueas": "Miqueas",
            "nahum": "Nahum",
            "habacuc": "Habacuc",
            "sofonias": "Sofonías",
            "hageo": "Hageo",
            "zacarias": "Zacarías",
            "malaquias": "Malaquías",
            "mateo": "Mateo",
            "marcos": "Marcos",
            "lucas": "Lucas",
            "juan": "Juan",
            "hechos": "Hechos",
            "romanos": "Romanos",
            "1corintios": "1 Corintios",
            "2corintios": "2 Corintios",
            "galatas": "Gálatas",
            "efesios": "Efesios",
            "filipenses": "Filipenses",
            "colosenses": "Colosenses",
            "1tesalonicenses": "1 Tesalonicenses",
            "2tesalonicenses": "2 Tesalonicenses",
            "1timoteo": "1 Timoteo",
            "2timoteo": "2 Timoteo",
            "tito": "Tito",
            "filemon": "Filemón",
            "hebreos": "Hebreos",
            "santiago": "Santiago",
            "1pedro": "1 Pedro",
            "2pedro": "2 Pedro",
            "1juan": "1 Juan",
            "2juan": "2 Juan",
            "3juan": "3 Juan",
            "judas": "Judas",
            "apocalipsis": "Apocalipsis"
        }
        
        # Book categories
        self.old_testament = [
            "Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio",
            "Josué", "Jueces", "Rut", "1 Samuel", "2 Samuel", 
            "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas",
            "Esdras", "Nehemías", "Ester", "Job", "Salmos",
            "Proverbios", "Eclesiastés", "Cantares", "Isaías",
            "Jeremías", "Lamentaciones", "Ezequiel", "Daniel",
            "Oseas", "Joel", "Amós", "Abdías", "Jonás", "Miqueas",
            "Nahum", "Habacuc", "Sofonías", "Hageo", "Zacarías", "Malaquías"
        ]
        
        self.new_testament = [
            "Mateo", "Marcos", "Lucas", "Juan", "Hechos", "Romanos",
            "1 Corintios", "2 Corintios", "Gálatas", "Efesios",
            "Filipenses", "Colosenses", "1 Tesalonicenses", "2 Tesalonicenses",
            "1 Timoteo", "2 Timoteo", "Tito", "Filemón", "Hebreos",
            "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan",
            "3 Juan", "Judas", "Apocalipsis"
        ]
    
    def load_bible_data(self, file_pattern: str = "*.json") -> None:
        """
        Load Bible data from JSON files.
        
        Args:
            file_pattern: Pattern to match data files
        """
        logger.info(f"Loading Bible data from {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Bible data directory not found: {self.data_path}")
        
        # Find all JSON files
        json_files = list(self.data_path.glob(file_pattern))
        
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {self.data_path}")
        
        for json_file in json_files:
            self._load_json_file(json_file)
        
        logger.info(f"Loaded {len(self.verses)} verses from {len(json_files)} files")
        self._organize_data()
    
    def _load_json_file(self, file_path: Path) -> None:
        """Load verses from a single JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                self._process_verse_list(data)
            elif isinstance(data, dict):
                self._process_book_dict(data)
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
    
    def _process_verse_list(self, verses: List[Dict[str, Any]]) -> None:
        """Process a list of verse dictionaries."""
        for verse_data in verses:
            verse = self._create_verse_from_dict(verse_data)
            if verse:
                self.verses.append(verse)
    
    def _process_book_dict(self, book_data: Dict[str, Any]) -> None:
        """Process book dictionary structure."""
        for book_key, book_content in book_data.items():
            book_name = self.book_names.get(book_key.lower(), book_key)
            
            if isinstance(book_content, dict):
                for chapter_key, chapter_content in book_content.items():
                    try:
                        chapter_num = int(chapter_key)
                        
                        if isinstance(chapter_content, dict):
                            for verse_key, verse_text in chapter_content.items():
                                try:
                                    verse_num = int(verse_key)
                                    verse = BibleVerse(
                                        book=book_name,
                                        chapter=chapter_num,
                                        verse=verse_num,
                                        text=clean_text(str(verse_text))
                                    )
                                    self.verses.append(verse)
                                except ValueError:
                                    continue
                    except ValueError:
                        continue
    
    def _create_verse_from_dict(self, verse_data: Dict[str, Any]) -> Optional[BibleVerse]:
        """Create BibleVerse from dictionary data."""
        try:
            # Handle different key naming conventions
            book = verse_data.get('book') or verse_data.get('libro')
            chapter = verse_data.get('chapter') or verse_data.get('capitulo')
            verse = verse_data.get('verse') or verse_data.get('versiculo')
            text = verse_data.get('text') or verse_data.get('texto')
            
            if not all([book, chapter, verse, text]):
                return None
            
            # Ensure we have string for book name lookup
            book_str = str(book) if book else ""
            chapter_int = int(chapter) if chapter else 0
            verse_int = int(verse) if verse else 0
            text_str = str(text) if text else ""
            
            # Normalize book name
            book_name = self.book_names.get(book_str.lower(), book_str)
            
            return BibleVerse(
                book=book_name,
                chapter=chapter_int,
                verse=verse_int,
                text=clean_text(text_str)
            )
        
        except (ValueError, KeyError) as e:
            logger.warning(f"Error processing verse data: {e}")
            return None
    
    def _organize_data(self) -> None:
        """Organize verses by book and chapter."""
        self.books.clear()
        self.chapters.clear()
        
        for verse in self.verses:
            # Group by book
            if verse.book not in self.books:
                self.books[verse.book] = []
            self.books[verse.book].append(verse)
            
            # Group by book and chapter
            if verse.book not in self.chapters:
                self.chapters[verse.book] = {}
            if verse.chapter not in self.chapters[verse.book]:
                self.chapters[verse.book][verse.chapter] = []
            self.chapters[verse.book][verse.chapter].append(verse)
        
        # Sort verses within each group
        for book in self.books.values():
            book.sort(key=lambda v: (v.chapter, v.verse))
        
        for book_chapters in self.chapters.values():
            for chapter_verses in book_chapters.values():
                chapter_verses.sort(key=lambda v: v.verse)
    
    def get_verse(self, book: str, chapter: int, verse: int) -> Optional[BibleVerse]:
        """
        Get a specific verse.
        
        Args:
            book: Book name
            chapter: Chapter number
            verse: Verse number
        
        Returns:
            BibleVerse or None if not found
        """
        if book in self.chapters and chapter in self.chapters[book]:
            for v in self.chapters[book][chapter]:
                if v.verse == verse:
                    return v
        return None
    
    def get_passage(self, book: str, chapter: int, start_verse: int, end_verse: int) -> Optional[BiblePassage]:
        """
        Get a passage of verses.
        
        Args:
            book: Book name
            chapter: Chapter number
            start_verse: Starting verse number
            end_verse: Ending verse number
        
        Returns:
            BiblePassage or None if not found
        """
        if book not in self.chapters or chapter not in self.chapters[book]:
            return None
        
        verses = []
        for v in self.chapters[book][chapter]:
            if start_verse <= v.verse <= end_verse:
                verses.append(v)
        
        if not verses:
            return None
        
        return BiblePassage(
            verses=verses,
            book=book,
            chapter=chapter,
            start_verse=start_verse,
            end_verse=end_verse
        )
    
    def get_chapter(self, book: str, chapter: int) -> List[BibleVerse]:
        """
        Get all verses from a chapter.
        
        Args:
            book: Book name
            chapter: Chapter number
        
        Returns:
            List of verses
        """
        if book in self.chapters and chapter in self.chapters[book]:
            return self.chapters[book][chapter].copy()
        return []
    
    def search_text(self, query: str, books: Optional[List[str]] = None) -> List[BibleVerse]:
        """
        Search for verses containing specific text.
        
        Args:
            query: Search query
            books: Optional list of books to search in
        
        Returns:
            List of matching verses
        """
        query_lower = query.lower()
        results = []
        
        search_verses = self.verses
        if books:
            search_verses = [v for v in self.verses if v.book in books]
        
        for verse in search_verses:
            if query_lower in verse.text.lower():
                results.append(verse)
        
        return results
    
    def get_context(self, book: str, chapter: int, verse: int, before: int = 2, after: int = 2) -> List[BibleVerse]:
        """
        Get verses with context around a specific verse.
        
        Args:
            book: Book name
            chapter: Chapter number
            verse: Verse number
            before: Number of verses before
            after: Number of verses after
        
        Returns:
            List of verses including context
        """
        start_verse = max(1, verse - before)
        end_verse = verse + after
        
        passage = self.get_passage(book, chapter, start_verse, end_verse)
        return passage.verses if passage else []
    
    def get_random_verses(self, count: int = 10, books: Optional[List[str]] = None) -> List[BibleVerse]:
        """
        Get random verses for training.
        
        Args:
            count: Number of verses to return
            books: Optional list of books to sample from
        
        Returns:
            List of random verses
        """
        import random
        
        sample_verses = self.verses
        if books:
            sample_verses = [v for v in self.verses if v.book in books]
        
        if len(sample_verses) < count:
            return sample_verses.copy()
        
        return random.sample(sample_verses, count)
    
    def export_to_text(self, output_path: str, format_type: str = "reference") -> None:
        """
        Export Bible data to text format.
        
        Args:
            output_path: Output file path
            format_type: Format type ('reference', 'plain', 'structured')
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for verse in self.verses:
                if format_type == "reference":
                    f.write(f"{verse.reference}: {verse.text}\n")
                elif format_type == "plain":
                    f.write(f"{verse.text}\n")
                elif format_type == "structured":
                    f.write(f"[{verse.book}|{verse.chapter}|{verse.verse}] {verse.text}\n")
        
        logger.info(f"Exported {len(self.verses)} verses to {output_file}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the loaded Bible data."""
        stats = {
            'total_verses': len(self.verses),
            'total_books': len(self.books),
            'old_testament_books': len([b for b in self.books.keys() if b in self.old_testament]),
            'new_testament_books': len([b for b in self.books.keys() if b in self.new_testament]),
            'books': {}
        }
        
        for book, verses in self.books.items():
            chapters = set(v.chapter for v in verses)
            stats['books'][book] = {
                'verses': len(verses),
                'chapters': len(chapters),
                'testament': 'Old' if book in self.old_testament else 'New'
            }
        
        return stats