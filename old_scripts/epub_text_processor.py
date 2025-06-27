#!/usr/bin/env python3
"""
EPUB Text Processor - Extract, chunk, and summarize book content
Simplified version with best practices from the comprehensive prompt
"""

import os
import re
import json
import argparse
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional


class EPUBProcessor:
    """Process EPUB files: extract text, create chunks, generate summaries"""
    
    def __init__(self, epub_path: str, chunk_size: int = 2000):
        self.epub_path = Path(epub_path)
        self.chunk_size = chunk_size
        self.book = None
        self.extracted_text = ""
        self.chunks = []
        self.summaries = []
        
    def analyze_structure(self) -> Dict:
        """Analyze EPUB structure to identify books/parts/chapters"""
        self.book = epub.read_epub(self.epub_path)
        
        structure = {
            'title': self.book.get_metadata('DC', 'title')[0][0] if self.book.get_metadata('DC', 'title') else 'Unknown',
            'items': [],
            'toc': [],
            'book_markers': []
        }
        
        # Analyze table of contents
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_NAVIGATION:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                for link in soup.find_all('a'):
                    structure['toc'].append({
                        'title': link.get_text().strip(),
                        'href': link.get('href', '')
                    })
        
        # Analyze content items
        for item in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            # Look for book markers
            book_patterns = [
                r'BOOK\s+(ONE|TWO|THREE|FOUR|FIVE|1|2|3|4|5|I|II|III|IV|V)',
                r'PART\s+(ONE|TWO|THREE|1|2|3|I|II|III)'
            ]
            
            for pattern in book_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    structure['book_markers'].append({
                        'text': match.group(),
                        'item_id': item.get_id(),
                        'context': text[max(0, match.start()-100):match.end()+100]
                    })
            
            structure['items'].append({
                'id': item.get_id(),
                'name': item.get_name(),
                'word_count': len(text.split())
            })
        
        return structure
    
    def extract_text(self, start_marker: Optional[str] = None, end_marker: Optional[str] = None) -> str:
        """Extract text from EPUB with optional boundary markers"""
        if not self.book:
            self.book = epub.read_epub(self.epub_path)
        
        full_text = []
        in_range = start_marker is None
        
        for item in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            
            # Check for start marker
            if start_marker and not in_range:
                if start_marker.upper() in text.upper():
                    marker_pos = text.upper().find(start_marker.upper())
                    text = text[marker_pos:]
                    in_range = True
                else:
                    continue
            
            # Check for end marker
            if end_marker and in_range:
                if end_marker.upper() in text.upper():
                    marker_pos = text.upper().find(end_marker.upper())
                    text = text[:marker_pos]
                    full_text.append(text)
                    break
            
            if in_range:
                full_text.append(text)
        
        # Clean and join text
        self.extracted_text = ' '.join(full_text)
        self.extracted_text = re.sub(r'\s+', ' ', self.extracted_text).strip()
        
        # Remove common artifacts
        self.extracted_text = re.sub(r'calibre\d*', '', self.extracted_text)
        self.extracted_text = re.sub(r'filepos\d+', '', self.extracted_text)
        
        return self.extracted_text
    
    def validate_extraction(self) -> Dict:
        """Validate extracted text quality"""
        words = self.extracted_text.split()
        word_count = len(words)
        
        validation = {
            'word_count': word_count,
            'avg_word_length': sum(len(w) for w in words) / word_count if word_count > 0 else 0,
            'sentence_count': len(re.findall(r'[.!?]+', self.extracted_text)),
            'quality_checks': {
                'has_content': word_count > 1000,
                'has_sentences': len(re.findall(r'[.!?]+', self.extracted_text)) > word_count * 0.01,
                'has_narrative': any(word in self.extracted_text.lower() for word in ['said', 'was', 'were', 'had']),
                'low_artifacts': self.extracted_text.count('<') < 10 and self.extracted_text.count('>') < 10
            }
        }
        
        validation['passed'] = all(validation['quality_checks'].values())
        return validation
    
    def create_chunks(self) -> List[Dict]:
        """Create word-based chunks of specified size"""
        words = self.extracted_text.split()
        total_words = len(words)
        
        self.chunks = []
        chunk_num = 1
        
        for i in range(0, total_words, self.chunk_size):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            self.chunks.append({
                'number': chunk_num,
                'start_word': i + 1,
                'end_word': min(i + self.chunk_size, total_words),
                'word_count': len(chunk_words),
                'text': chunk_text
            })
            chunk_num += 1
        
        return self.chunks
    
    def create_summary(self, chunk_text: str, target_words: int = 150) -> str:
        """Create a summary of approximately target_words length"""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', chunk_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return chunk_text[:target_words * 5]  # Rough estimate of chars
        
        # Select key sentences based on position and keywords
        # First and last sentences often contain important info
        key_sentences = []
        
        # Add first sentence
        if sentences:
            key_sentences.append(sentences[0])
        
        # Add sentences with important keywords
        important_keywords = ['however', 'therefore', 'important', 'significant', 'concluded', 'discovered', 'revealed']
        for sentence in sentences[1:-1]:
            if any(keyword in sentence.lower() for keyword in important_keywords):
                key_sentences.append(sentence)
                if len(' '.join(key_sentences).split()) > target_words:
                    break
        
        # Add last sentence if room
        if sentences and len(' '.join(key_sentences).split()) < target_words:
            key_sentences.append(sentences[-1])
        
        # Build summary to target length
        summary = ' '.join(key_sentences)
        summary_words = summary.split()
        
        if len(summary_words) > target_words:
            summary = ' '.join(summary_words[:target_words])
            if not summary.endswith('.'):
                summary += '.'
        elif len(summary_words) < target_words * 0.8:
            # If too short, add more sentences
            for sentence in sentences:
                if sentence not in key_sentences:
                    key_sentences.insert(-1, sentence)
                    summary = ' '.join(key_sentences)
                    if len(summary.split()) >= target_words * 0.9:
                        break
        
        return summary
    
    def process_book_section(self, section_name: str = None, 
                           start_marker: str = None, 
                           end_marker: str = None) -> Dict:
        """Complete pipeline: extract, chunk, and summarize a book section"""
        
        # Step 1: Extract text
        print(f"Extracting text{f' for {section_name}' if section_name else ''}...")
        self.extract_text(start_marker, end_marker)
        
        # Step 2: Validate extraction
        print("Validating extraction...")
        validation = self.validate_extraction()
        print(f"  Word count: {validation['word_count']:,}")
        print(f"  Quality passed: {validation['passed']}")
        
        if not validation['passed']:
            print("WARNING: Quality validation failed. Review the extraction.")
        
        # Step 3: Create chunks
        print(f"Creating {self.chunk_size}-word chunks...")
        self.create_chunks()
        print(f"  Created {len(self.chunks)} chunks")
        
        # Step 4: Generate summaries
        print("Generating summaries...")
        self.summaries = []
        for chunk in self.chunks:
            summary = self.create_summary(chunk['text'])
            self.summaries.append({
                'chunk_number': chunk['number'],
                'summary': summary,
                'word_count': len(summary.split())
            })
        
        return {
            'section': section_name or 'Full book',
            'total_words': validation['word_count'],
            'chunks_created': len(self.chunks),
            'summaries_created': len(self.summaries),
            'validation': validation
        }
    
    def save_outputs(self, output_dir: str = "output"):
        """Save chunks and summaries to files"""
        output_path = Path(output_dir)
        chunks_dir = output_path / "chunks"
        summaries_dir = output_path / "summaries"
        
        # Create directories
        chunks_dir.mkdir(parents=True, exist_ok=True)
        summaries_dir.mkdir(parents=True, exist_ok=True)
        
        # Save chunks
        for chunk in self.chunks:
            chunk_file = chunks_dir / f"chunk_{chunk['number']:03d}.txt"
            chunk_file.write_text(chunk['text'], encoding='utf-8')
        
        # Save summaries
        for i, summary in enumerate(self.summaries):
            summary_file = summaries_dir / f"summary_{i+1:03d}.txt"
            summary_file.write_text(summary['summary'], encoding='utf-8')
        
        # Save metadata
        metadata = {
            'source_file': str(self.epub_path),
            'chunk_size': self.chunk_size,
            'total_chunks': len(self.chunks),
            'total_summaries': len(self.summaries),
            'word_count': len(self.extracted_text.split())
        }
        
        metadata_file = output_path / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
        print(f"\nOutputs saved to {output_path}")
        print(f"  Chunks: {chunks_dir}")
        print(f"  Summaries: {summaries_dir}")
        print(f"  Metadata: {metadata_file}")


def main():
    parser = argparse.ArgumentParser(description='Process EPUB files: extract, chunk, and summarize')
    parser.add_argument('epub_file', help='Path to EPUB file')
    parser.add_argument('--chunk-size', type=int, default=2000, help='Words per chunk (default: 2000)')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze structure, don\'t process')
    parser.add_argument('--start-marker', help='Text marker for extraction start (e.g., "BOOK ONE")')
    parser.add_argument('--end-marker', help='Text marker for extraction end (e.g., "BOOK TWO")')
    parser.add_argument('--output-dir', default='output', help='Output directory (default: output)')
    
    args = parser.parse_args()
    
    # Create processor
    processor = EPUBProcessor(args.epub_file, args.chunk_size)
    
    # Analyze structure
    print("Analyzing EPUB structure...")
    structure = processor.analyze_structure()
    
    print(f"\nTitle: {structure['title']}")
    print(f"Content items: {len(structure['items'])}")
    print(f"TOC entries: {len(structure['toc'])}")
    
    if structure['book_markers']:
        print("\nBook/Part markers found:")
        for marker in structure['book_markers']:
            print(f"  - {marker['text']}")
    
    if args.analyze_only:
        # Save structure analysis
        structure_file = Path(args.output_dir) / "structure_analysis.json"
        structure_file.parent.mkdir(exist_ok=True)
        structure_file.write_text(json.dumps(structure, indent=2))
        print(f"\nStructure analysis saved to {structure_file}")
        return
    
    # Process book
    print("\nProcessing book...")
    results = processor.process_book_section(
        section_name=args.start_marker,
        start_marker=args.start_marker,
        end_marker=args.end_marker
    )
    
    # Save outputs
    processor.save_outputs(args.output_dir)
    
    # Print summary
    print("\n" + "="*50)
    print("PROCESSING COMPLETE")
    print("="*50)
    print(f"Section: {results['section']}")
    print(f"Total words: {results['total_words']:,}")
    print(f"Chunks created: {results['chunks_created']}")
    print(f"Summaries created: {results['summaries_created']}")


if __name__ == "__main__":
    main()