"""
Create embeddings for Bible verses using OpenAI API.
"""

import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
import logging

import openai
from supabase import create_client

from ..utils import setup_logging, ConfigManager, ensure_dir, BibleProcessor

# Setup logging
logger = setup_logging()

class EmbeddingGenerator:
    """Generate and manage embeddings for Bible verses."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize embedding generator.
        
        Args:
            config_path: Optional configuration file path
        """
        self.config = ConfigManager(config_path)
        
        # Setup OpenAI client
        api_key = self.config.get('openai_api_key')
        if not api_key:
            raise ValueError("OpenAI API key not found in configuration")
        
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        
        # Setup Supabase client (optional)
        self.supabase_client = None
        supabase_url = self.config.get('supabase_url')
        supabase_key = self.config.get('supabase_service_key')
        
        if supabase_url and supabase_key:
            try:
                self.supabase_client = create_client(supabase_url, supabase_key)
                logger.info("Supabase client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Supabase client: {e}")
        
        # Embedding configuration
        self.model = "text-embedding-ada-002"
        self.max_batch_size = 100
        self.rate_limit_delay = 1.0  # seconds between API calls
        
        # Load Bible processor
        bible_data_path = self.config.get('bible_data_path', 'data/bible_rva1909')
        self.bible = BibleProcessor(bible_data_path)
        self.bible.load_bible_data()
        
        logger.info(f"Loaded {len(self.bible.verses)} verses for embedding generation")
    
    def generate_embeddings(self, verses: Optional[List] = None, output_dir: str = "data/embeddings") -> Dict[str, Any]:
        """
        Generate embeddings for Bible verses.
        
        Args:
            verses: Optional list of verses to embed (defaults to all verses)
            output_dir: Directory to save embeddings
        
        Returns:
            Dictionary with embedding statistics
        """
        if verses is None:
            verses = self.bible.verses
        
        ensure_dir(output_dir)
        output_path = Path(output_dir)
        
        logger.info(f"Generating embeddings for {len(verses)} verses")
        
        embeddings = {}
        texts = []
        verse_keys = []
        
        # Prepare texts and keys
        for verse in verses:
            text = f"{verse.reference}: {verse.text}"
            texts.append(text)
            verse_key = f"{verse.book}_{verse.chapter}_{verse.verse}"
            verse_keys.append(verse_key)
        
        # Generate embeddings in batches
        batch_size = min(self.max_batch_size, len(texts))
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_keys = verse_keys[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch_texts)} texts)")
            
            try:
                # Generate embeddings for batch
                response = self.client.embeddings.create(
                    input=batch_texts,
                    model=self.model
                )
                
                # Store embeddings
                for j, embedding_data in enumerate(response.data):
                    verse_key = batch_keys[j]
                    embeddings[verse_key] = {
                        'verse': verses[i + j],
                        'embedding': embedding_data.embedding,
                        'text': batch_texts[j]
                    }
                
                # Rate limiting
                if batch_num < total_batches:
                    time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"Error processing batch {batch_num}: {e}")
                continue
        
        # Save embeddings to file
        embeddings_file = output_path / "bible_embeddings.pkl"
        with open(embeddings_file, 'wb') as f:
            pickle.dump(embeddings, f)
        
        logger.info(f"Saved embeddings to {embeddings_file}")
        
        # Save to Supabase if available
        if self.supabase_client:
            self._save_embeddings_to_supabase(embeddings)
        
        # Save metadata
        metadata = {
            'total_verses': len(verses),
            'successful_embeddings': len(embeddings),
            'model': self.model,
            'embedding_dimension': len(list(embeddings.values())[0]['embedding']) if embeddings else 0
        }
        
        metadata_file = output_path / "embedding_metadata.pkl"
        with open(metadata_file, 'wb') as f:
            pickle.dump(metadata, f)
        
        return metadata
    
    def _save_embeddings_to_supabase(self, embeddings: Dict[str, Any]) -> None:
        """Save embeddings to Supabase vector database."""
        if not self.supabase_client:
            logger.warning("Supabase client not available")
            return
            
        try:
            logger.info("Saving embeddings to Supabase...")
            
            # Prepare data for batch insert
            records = []
            for verse_key, data in embeddings.items():
                verse = data['verse']
                record = {
                    'id': verse_key,
                    'book': verse.book,
                    'chapter': verse.chapter,
                    'verse': verse.verse,
                    'text': verse.text,
                    'reference': verse.reference,
                    'embedding': data['embedding']
                }
                records.append(record)
            
            # Insert in batches to avoid size limits
            batch_size = 100
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                try:
                    self.supabase_client.table('bible_embeddings').insert(batch).execute()
                    logger.info(f"Inserted batch {i // batch_size + 1} ({len(batch)} records)")
                
                except Exception as e:
                    logger.error(f"Error inserting batch {i // batch_size + 1}: {e}")
                    continue
            
            logger.info(f"Successfully saved {len(embeddings)} embeddings to Supabase")
        
        except Exception as e:
            logger.error(f"Error saving embeddings to Supabase: {e}")
    
    def load_embeddings(self, embeddings_path: str = "data/embeddings/bible_embeddings.pkl") -> Dict[str, Any]:
        """
        Load embeddings from file.
        
        Args:
            embeddings_path: Path to embeddings file
        
        Returns:
            Dictionary of embeddings
        """
        embeddings_file = Path(embeddings_path)
        
        if not embeddings_file.exists():
            raise FileNotFoundError(f"Embeddings file not found: {embeddings_path}")
        
        with open(embeddings_file, 'rb') as f:
            embeddings = pickle.load(f)
        
        logger.info(f"Loaded {len(embeddings)} embeddings from {embeddings_path}")
        return embeddings
    
    def search_similar_verses(self, query: str, top_k: int = 10, embeddings_path: str = "data/embeddings/bible_embeddings.pkl") -> List[Dict[str, Any]]:
        """
        Search for verses similar to a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
            embeddings_path: Path to embeddings file
        
        Returns:
            List of similar verses with scores
        """
        # Load embeddings
        embeddings = self.load_embeddings(embeddings_path)
        
        # Generate query embedding
        try:
            response = self.client.embeddings.create(
                input=[query],
                model=self.model
            )
            query_embedding = response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            return []
        
        # Calculate similarities
        similarities = []
        
        for verse_key, data in embeddings.items():
            verse_embedding = data['embedding']
            
            # Cosine similarity
            similarity = np.dot(query_embedding, verse_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(verse_embedding)
            )
            
            similarities.append({
                'verse': data['verse'],
                'text': data['text'],
                'similarity': similarity,
                'key': verse_key
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    
    def export_embeddings_csv(self, output_path: str = "data/embeddings/bible_embeddings.csv", embeddings_path: str = "data/embeddings/bible_embeddings.pkl") -> None:
        """
        Export embeddings to CSV format.
        
        Args:
            output_path: Output CSV file path
            embeddings_path: Path to embeddings file
        """
        import pandas as pd
        
        embeddings = self.load_embeddings(embeddings_path)
        
        rows = []
        for verse_key, data in embeddings.items():
            verse = data['verse']
            embedding = data['embedding']
            
            row = {
                'key': verse_key,
                'book': verse.book,
                'chapter': verse.chapter,
                'verse': verse.verse,
                'reference': verse.reference,
                'text': verse.text,
                'embedding_dim': len(embedding),
            }
            
            # Add embedding dimensions as separate columns
            for i, val in enumerate(embedding):
                row[f'emb_{i}'] = val
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        
        logger.info(f"Exported embeddings to {output_path} ({len(rows)} rows)")

def create_embeddings(config_path: Optional[str] = None) -> None:
    """
    Create embeddings for Bible verses.
    
    Args:
        config_path: Optional configuration file path
    """
    try:
        generator = EmbeddingGenerator(config_path)
        metadata = generator.generate_embeddings()
        
        logger.info("Embedding generation completed successfully")
        logger.info(f"Generated {metadata['successful_embeddings']}/{metadata['total_verses']} embeddings")
        logger.info(f"Embedding dimension: {metadata['embedding_dimension']}")
        
    except Exception as e:
        logger.error(f"Error creating embeddings: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    config_file = sys.argv[1] if len(sys.argv) > 1 else None
    create_embeddings(config_file)