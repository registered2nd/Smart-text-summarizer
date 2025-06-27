#!/usr/bin/env python3
"""
Universal EPUB book section extractor
Works with any EPUB file to extract sections based on content markers
"""

import zipfile
import argparse
from bs4 import BeautifulSoup
import re
from pathlib import Path

def clean_text(text):
    """Clean extracted text from HTML and formatting artifacts"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove calibre markers
    text = re.sub(r'\bcalibre\d+\b', '', text)
    # Remove file position markers
    text = re.sub(r'filepos\d+', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove empty parentheses and brackets
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r'\[\s*\]', '', text)
    
    return text.strip()

def extract_section(epub_path, start_markers=None, end_markers=None, 
                   start_contains_all=False, end_contains_all=False,
                   verbose=False):
    """
    Extract a section from an EPUB file based on content markers
    
    Args:
        epub_path: Path to EPUB file
        start_markers: List of text markers that indicate section start
        end_markers: List of text markers that indicate section end
        start_contains_all: If True, all start markers must be present
        end_contains_all: If True, all end markers must be present
        verbose: Print progress information
        
    Returns:
        tuple: (extracted_text, word_count, metadata)
    """
    
    extracted_text = []
    found_start = False
    in_section = False
    metadata = {
        'start_file': None,
        'end_file': None,
        'total_files': 0
    }
    
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # Get all HTML files
        html_files = sorted([f for f in epub.namelist() if f.endswith('.html')])
        metadata['total_files'] = len(html_files)
        
        for html_file in html_files:
            if verbose:
                print(f"Processing {html_file}...")
                
            content = epub.read(html_file).decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for element in soup(["script", "style"]):
                element.extract()
            
            text = soup.get_text()
            
            # Check for start markers
            if not found_start and start_markers:
                if start_contains_all:
                    # All markers must be present
                    if all(marker in text for marker in start_markers):
                        found_start = True
                        in_section = True
                        metadata['start_file'] = html_file
                else:
                    # Any marker is sufficient
                    if any(marker in text for marker in start_markers):
                        found_start = True
                        in_section = True
                        metadata['start_file'] = html_file
            elif not start_markers:
                # No start markers specified, start from beginning
                found_start = True
                in_section = True
                metadata['start_file'] = html_files[0] if html_files else None
            
            # Process content if we're in the section
            if in_section:
                lines = text.split('\n')
                
                # If this is the start file, find exact start point
                if html_file == metadata['start_file'] and start_markers:
                    start_index = 0
                    for i, line in enumerate(lines):
                        if any(marker in line for marker in start_markers):
                            start_index = i
                            if verbose:
                                print(f"  Found start at line {i}: {line[:80]}...")
                            break
                    lines = lines[start_index:]
                
                # Check for end markers
                if end_markers:
                    end_index = None
                    for i, line in enumerate(lines):
                        if end_contains_all:
                            if all(marker in line for marker in end_markers):
                                end_index = i
                                metadata['end_file'] = html_file
                                if verbose:
                                    print(f"  Found end at line {i}: {line[:80]}...")
                                break
                        else:
                            if any(marker in line for marker in end_markers):
                                end_index = i
                                metadata['end_file'] = html_file
                                if verbose:
                                    print(f"  Found end at line {i}: {line[:80]}...")
                                break
                    
                    if end_index is not None:
                        lines = lines[:end_index]
                        in_section = False
                
                # Add cleaned lines
                for line in lines:
                    cleaned = line.strip()
                    if cleaned:
                        extracted_text.append(cleaned)
                
                # Stop if we found the end
                if not in_section:
                    break
    
    # Join and clean the full text
    full_text = ' '.join(extracted_text)
    full_text = clean_text(full_text)
    
    # Calculate word count
    word_count = len(full_text.split())
    
    return full_text, word_count, metadata

def main():
    parser = argparse.ArgumentParser(description='Extract sections from EPUB files')
    parser.add_argument('epub', help='Path to EPUB file')
    parser.add_argument('-s', '--start', nargs='+', help='Start marker(s)')
    parser.add_argument('-e', '--end', nargs='+', help='End marker(s)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--start-all', action='store_true', 
                       help='Require all start markers to be present')
    parser.add_argument('--end-all', action='store_true',
                       help='Require all end markers to be present')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print progress information')
    
    args = parser.parse_args()
    
    # Extract section
    text, word_count, metadata = extract_section(
        args.epub,
        start_markers=args.start,
        end_markers=args.end,
        start_contains_all=args.start_all,
        end_contains_all=args.end_all,
        verbose=args.verbose
    )
    
    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\nSaved to: {output_path}")
    
    # Print summary
    print(f"\nExtraction Summary:")
    print(f"- Words extracted: {word_count:,}")
    print(f"- Start file: {metadata['start_file']}")
    print(f"- End file: {metadata['end_file']}")
    print(f"- Files processed: {metadata['total_files']}")
    
    # Show preview
    words = text.split()
    if len(words) > 100:
        print(f"\nFirst 100 words:")
        print(' '.join(words[:100]) + '...')
        print(f"\nLast 100 words:")
        print('...' + ' '.join(words[-100:]))

if __name__ == "__main__":
    main()