#!/usr/bin/env python3
"""
Universal output formatter for book summaries
Creates HTML, Markdown, and formatted text from chunks and summaries
"""

import argparse
from pathlib import Path
from datetime import datetime
import re

def parse_chunks_file(chunks_file):
    """Parse a standard chunks file format"""
    chunks = []
    with open(chunks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by chunk markers
    parts = re.split(r'=== CHUNK (\d+): Words (\d+)-(\d+) ===', content)
    
    # Process chunks (skip first empty part)
    for i in range(1, len(parts), 4):
        if i + 3 < len(parts):
            chunk_num = int(parts[i])
            start_word = int(parts[i + 1])
            end_word = int(parts[i + 2])
            text = parts[i + 3].strip()
            
            chunks.append({
                'number': chunk_num,
                'start': start_word,
                'end': end_word,
                'text': text,
                'word_count': len(text.split())
            })
    
    return chunks

def parse_summaries_file(summaries_file):
    """Parse a summaries file format"""
    summaries = []
    with open(summaries_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by summary markers
    parts = re.split(r'=== SUMMARY (\d+): Words (\d+)-(\d+) ===', content)
    
    # Process summaries
    for i in range(1, len(parts), 4):
        if i + 3 < len(parts):
            summary_num = int(parts[i])
            start_word = int(parts[i + 1])
            end_word = int(parts[i + 2])
            
            # Extract word count and summary text
            text_part = parts[i + 3].strip()
            lines = text_part.split('\n')
            word_count_line = ""
            summary_text = ""
            
            for j, line in enumerate(lines):
                if line.strip().startswith('Word count:'):
                    word_count_line = line.strip()
                    # Rest is summary
                    summary_text = '\n'.join(lines[j+1:]).strip()
                    break
            
            summaries.append({
                'number': summary_num,
                'start': start_word,
                'end': end_word,
                'word_count_line': word_count_line,
                'text': summary_text
            })
    
    return summaries

def create_html(book_title, book_author, chunks, summaries, output_file):
    """Create HTML output with navigation and styling"""
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Summaries</title>
    <style>
        body {{
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
        }}
        .metadata {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .word-count {{
            font-style: italic;
            color: #7f8c8d;
            margin-bottom: 10px;
        }}
        .nav {{
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-decoration: none;
        }}
        .nav:hover {{
            background-color: #2980b9;
        }}
        @media print {{
            .nav {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <a href="#top" class="nav">↑ Top</a>
    <div class="container">
        <h1 id="top">{title}</h1>
        <div class="metadata">
            <p><strong>Author:</strong> {author}</p>
            <p><strong>Generated:</strong> {date}</p>
            <p><strong>Total Summaries:</strong> {total_summaries}</p>
        </div>
        
        {content}
    </div>
</body>
</html>"""
    
    content_parts = []
    for summary in summaries:
        content_parts.append(f"""
        <div class="summary">
            <h3>Summary {summary['number']}: Words {summary['start']}-{summary['end']}</h3>
            <p class="word-count">{summary['word_count_line']}</p>
            <p>{summary['text']}</p>
        </div>
        """)
    
    html_content = html_template.format(
        title=book_title,
        author=book_author,
        date=datetime.now().strftime('%Y-%m-%d'),
        total_summaries=len(summaries),
        content='\n'.join(content_parts)
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_markdown(book_title, book_author, chunks, summaries, output_file):
    """Create Markdown output"""
    
    output = []
    output.append(f"# {book_title}\n")
    output.append(f"**Author:** {book_author}\n")
    output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}\n")
    output.append(f"**Total Summaries:** {len(summaries)}\n")
    output.append("\n---\n")
    
    for summary in summaries:
        output.append(f"## Summary {summary['number']}: Words {summary['start']}-{summary['end']}\n")
        output.append(f"*{summary['word_count_line']}*\n")
        output.append(f"{summary['text']}\n")
        output.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

def create_text(book_title, book_author, chunks, summaries, output_file):
    """Create formatted text output"""
    
    output = []
    output.append(book_title.upper())
    output.append("=" * len(book_title))
    output.append(f"Author: {book_author}")
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    output.append(f"Total Summaries: {len(summaries)}")
    output.append("")
    output.append("=" * 60)
    output.append("")
    
    for summary in summaries:
        header = f"SUMMARY {summary['number']}: Words {summary['start']}-{summary['end']}"
        output.append(header)
        output.append("-" * len(header))
        output.append(summary['word_count_line'])
        output.append("")
        
        # Word wrap for readability
        import textwrap
        wrapped = textwrap.fill(summary['text'], width=80)
        output.append(wrapped)
        output.append("")
        output.append("-" * 60)
        output.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

def main():
    parser = argparse.ArgumentParser(description='Format book summaries into various outputs')
    parser.add_argument('-c', '--chunks', help='Chunks file')
    parser.add_argument('-s', '--summaries', required=True, help='Summaries file')
    parser.add_argument('-t', '--title', required=True, help='Book title')
    parser.add_argument('-a', '--author', required=True, help='Book author')
    parser.add_argument('-o', '--output', help='Output base name (default: book_summaries)')
    parser.add_argument('-f', '--formats', nargs='+', 
                       choices=['html', 'markdown', 'text', 'all'],
                       default=['all'], help='Output formats to generate')
    
    args = parser.parse_args()
    
    # Parse input files
    chunks = []
    if args.chunks:
        chunks = parse_chunks_file(args.chunks)
        print(f"Loaded {len(chunks)} chunks")
    
    summaries = parse_summaries_file(args.summaries)
    print(f"Loaded {len(summaries)} summaries")
    
    # Determine output base name
    output_base = args.output or 'book_summaries'
    
    # Generate requested formats
    formats = args.formats
    if 'all' in formats:
        formats = ['html', 'markdown', 'text']
    
    for fmt in formats:
        if fmt == 'html':
            output_file = f"{output_base}.html"
            create_html(args.title, args.author, chunks, summaries, output_file)
            print(f"Created: {output_file}")
        elif fmt == 'markdown':
            output_file = f"{output_base}.md"
            create_markdown(args.title, args.author, chunks, summaries, output_file)
            print(f"Created: {output_file}")
        elif fmt == 'text':
            output_file = f"{output_base}.txt"
            create_text(args.title, args.author, chunks, summaries, output_file)
            print(f"Created: {output_file}")

if __name__ == "__main__":
    main()