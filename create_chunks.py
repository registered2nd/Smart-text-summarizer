#!/usr/bin/env python3
"""
Universal text chunking script
Splits any text file into chunks of specified word count
"""

import argparse
from pathlib import Path

def create_chunks(text, chunk_size=2000, min_last_chunk=1000):
    """
    Split text into chunks of approximately chunk_size words
    
    Args:
        text: The text to chunk
        chunk_size: Target words per chunk
        min_last_chunk: Minimum words for last chunk (merge if less)
        
    Returns:
        List of chunk dictionaries with metadata
    """
    words = text.split()
    total_words = len(words)
    chunks = []
    
    for i in range(0, total_words, chunk_size):
        chunk_words = words[i:i + chunk_size]
        
        # Check if this is the last chunk and too small
        if i + chunk_size >= total_words and len(chunk_words) < min_last_chunk and chunks:
            # Merge with previous chunk
            prev_chunk = chunks.pop()
            combined_words = prev_chunk['text'].split() + chunk_words
            chunks.append({
                'number': len(chunks) + 1,
                'start': prev_chunk['start'],
                'end': total_words,
                'text': ' '.join(combined_words),
                'word_count': len(combined_words)
            })
        else:
            chunks.append({
                'number': len(chunks) + 1,
                'start': i + 1,
                'end': min(i + chunk_size, total_words),
                'text': ' '.join(chunk_words),
                'word_count': len(chunk_words)
            })
    
    return chunks

def save_chunks(chunks, output_file, format='standard'):
    """
    Save chunks to file in specified format
    
    Args:
        chunks: List of chunk dictionaries
        output_file: Output file path
        format: Output format ('standard', 'json', 'numbered')
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'json':
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    elif format == 'numbered':
        # Save each chunk as a separate numbered file
        base_name = output_path.stem
        output_dir = output_path.parent
        for chunk in chunks:
            chunk_file = output_dir / f"{base_name}_chunk_{chunk['number']:03d}.txt"
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(f"Chunk {chunk['number']}: Words {chunk['start']}-{chunk['end']}\n")
                f.write(f"Word count: {chunk['word_count']}\n\n")
                f.write(chunk['text'])
    
    else:  # standard format
        with open(output_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(f"=== CHUNK {chunk['number']}: Words {chunk['start']}-{chunk['end']} ===\n")
                f.write(chunk['text'])
                f.write("\n\n")

def main():
    parser = argparse.ArgumentParser(description='Chunk text files into specified word counts')
    parser.add_argument('input', help='Input text file')
    parser.add_argument('-o', '--output', help='Output file (default: input_chunks.txt)')
    parser.add_argument('-s', '--size', type=int, default=2000,
                       help='Words per chunk (default: 2000)')
    parser.add_argument('-m', '--min-last', type=int, default=1000,
                       help='Minimum words for last chunk (default: 1000)')
    parser.add_argument('-f', '--format', choices=['standard', 'json', 'numbered'],
                       default='standard', help='Output format')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print progress information')
    
    args = parser.parse_args()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        return
    
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create chunks
    chunks = create_chunks(text, args.size, args.min_last)
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        output_file = input_path.parent / f"{input_path.stem}_chunks.txt"
    
    # Save chunks
    save_chunks(chunks, output_file, args.format)
    
    # Print summary
    total_words = len(text.split())
    print(f"\nChunking Summary:")
    print(f"- Input file: {args.input}")
    print(f"- Total words: {total_words:,}")
    print(f"- Chunk size: {args.size:,} words")
    print(f"- Total chunks: {len(chunks)}")
    print(f"- Output: {output_file}")
    
    if args.verbose:
        print(f"\nChunk details:")
        for chunk in chunks:
            print(f"  Chunk {chunk['number']}: {chunk['word_count']:,} words "
                  f"(words {chunk['start']}-{chunk['end']})")

if __name__ == "__main__":
    main()