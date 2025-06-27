import os
from datetime import datetime

def create_markdown_summaries():
    """Create a well-structured Markdown file with all summaries"""
    output = []
    
    # Add header
    output.append("# Quicksilver - Book Summaries\n")
    output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}\n")
    output.append("**Book:** Neal Stephenson - Quicksilver (The Baroque Cycle, Vol. 1)\n")
    output.append("\n---\n")
    
    # Add table of contents
    output.append("## Table of Contents\n")
    output.append("- [Book One: Quicksilver](#book-one-quicksilver)")
    output.append("- [Book Two: King of the Vagabonds](#book-two-king-of-the-vagabonds)")
    output.append("- [Book Three: Odalisque](#book-three-odalisque)\n")
    output.append("\n---\n")
    
    # Process each book
    books = [
        ('Book One: Quicksilver', 'book-one-quicksilver', '/home/agentcode/text summaries/output/summaries/quicksilver_book_one_all_summaries.txt'),
        ('Book Two: King of the Vagabonds', 'book-two-king-of-the-vagabonds', '/home/agentcode/text summaries/output/summaries/quicksilver_book_two_all_summaries.txt'),
        ('Book Three: Odalisque', 'book-three-odalisque', '/home/agentcode/text summaries/output/summaries/quicksilver_book_three_all_summaries.txt')
    ]
    
    for book_title, book_id, file_path in books:
        # Add book section
        output.append(f"## {book_title}\n")
        
        # Read summaries
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse summaries - split by "=== SUMMARY"
        parts = content.split('=== SUMMARY')
        chunk_count = 0
        
        for part in parts[1:]:  # Skip first empty element
            if part.strip():
                # Extract the summary number and content
                lines = part.strip().split('\n')
                
                # Find the header line
                header_line = None
                for i, line in enumerate(lines):
                    if 'Words' in line and '===':
                        header_line = 'SUMMARY' + line
                        break
                
                # Find word count line
                word_count_line = None
                summary_start = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('Word count:'):
                        word_count_line = line.strip()
                        # Summary text starts after word count line (skip empty lines)
                        for j in range(i+1, len(lines)):
                            if lines[j].strip():
                                summary_start = j
                                break
                        break
                
                # Extract summary text
                if header_line and word_count_line and summary_start > 0:
                    summary_text = '\n'.join(lines[summary_start:]).strip()
                    
                    if summary_text:
                        chunk_count += 1
                        # Add summary
                        output.append(f"### {header_line.replace(' ===', '')}\n")
                        output.append(f"*{word_count_line}*\n")
                        output.append(f"{summary_text}\n")
        
        output.append(f"\n**Total chunks in {book_title}: {chunk_count}**\n")
        output.append("\n---\n")
    
    # Save markdown file
    with open('/home/agentcode/text summaries/output/Quicksilver_Book_Summaries.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Created: Quicksilver_Book_Summaries.md")

def create_html_summaries():
    """Create an HTML file with navigation and styling"""
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quicksilver - Book Summaries</title>
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
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 30px;
        }}
        .metadata {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        .toc {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 20px;
        }}
        .toc a {{
            color: #3498db;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .summary {{
            text-align: justify;
            margin-bottom: 20px;
        }}
        .word-count {{
            font-style: italic;
            color: #7f8c8d;
            margin-bottom: 10px;
        }}
        .chunk-count {{
            font-weight: bold;
            color: #34495e;
            margin: 20px 0;
        }}
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            display: none;
        }}
        @media print {{
            .back-to-top {{
                display: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 id="top">Quicksilver - Book Summaries</h1>
        <div class="metadata">
            <p><strong>Generated:</strong> {date}</p>
            <p><strong>Book:</strong> Neal Stephenson - Quicksilver (The Baroque Cycle, Vol. 1)</p>
        </div>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#book-one">Book One: Quicksilver</a></li>
                <li><a href="#book-two">Book Two: King of the Vagabonds</a></li>
                <li><a href="#book-three">Book Three: Odalisque</a></li>
            </ul>
        </div>
        
        {content}
        
        <a href="#top" class="back-to-top">↑ Top</a>
    </div>
    
    <script>
        // Show/hide back to top button
        window.onscroll = function() {{
            if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {{
                document.querySelector('.back-to-top').style.display = "block";
            }} else {{
                document.querySelector('.back-to-top').style.display = "none";
            }}
        }};
    </script>
</body>
</html>"""
    
    content_parts = []
    
    # Process each book
    books = [
        ('Book One: Quicksilver', 'book-one', '/home/agentcode/text summaries/output/summaries/quicksilver_book_one_all_summaries.txt'),
        ('Book Two: King of the Vagabonds', 'book-two', '/home/agentcode/text summaries/output/summaries/quicksilver_book_two_all_summaries.txt'),
        ('Book Three: Odalisque', 'book-three', '/home/agentcode/text summaries/output/summaries/quicksilver_book_three_all_summaries.txt')
    ]
    
    for book_title, book_id, file_path in books:
        content_parts.append(f'<h2 id="{book_id}">{book_title}</h2>')
        
        # Read summaries
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse summaries
        parts = content.split('=== SUMMARY')
        chunk_count = 0
        
        for part in parts[1:]:
            if part.strip():
                lines = part.strip().split('\n')
                
                # Find header
                header_line = None
                for i, line in enumerate(lines):
                    if 'Words' in line and '===':
                        header_line = 'SUMMARY' + line.replace(' ===', '')
                        break
                
                # Find word count and summary
                word_count_line = None
                summary_text = None
                for i, line in enumerate(lines):
                    if line.strip().startswith('Word count:'):
                        word_count_line = line.strip()
                        # Get all non-empty lines after word count
                        remaining_lines = []
                        for j in range(i+1, len(lines)):
                            if lines[j].strip():
                                remaining_lines.append(lines[j].strip())
                        if remaining_lines:
                            summary_text = ' '.join(remaining_lines)
                        break
                
                if header_line and word_count_line and summary_text:
                    chunk_count += 1
                    content_parts.append(f'<h3>{header_line}</h3>')
                    content_parts.append(f'<p class="word-count">{word_count_line}</p>')
                    content_parts.append(f'<p class="summary">{summary_text}</p>')
        
        content_parts.append(f'<p class="chunk-count">Total chunks in {book_title}: {chunk_count}</p>')
    
    # Generate final HTML
    html_content = html_template.format(
        date=datetime.now().strftime('%Y-%m-%d'),
        content='\n'.join(content_parts)
    )
    
    # Save HTML file
    with open('/home/agentcode/text summaries/output/Quicksilver_Book_Summaries.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Created: Quicksilver_Book_Summaries.html")

def create_structured_text():
    """Create a well-formatted text file with proper structure"""
    output = []
    
    # Add header
    output.append("QUICKSILVER - BOOK SUMMARIES")
    output.append("=" * 50)
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    output.append("Book: Neal Stephenson - Quicksilver (The Baroque Cycle, Vol. 1)")
    output.append("=" * 50)
    output.append("")
    
    # Add table of contents
    output.append("TABLE OF CONTENTS")
    output.append("-" * 30)
    output.append("1. Book One: Quicksilver")
    output.append("2. Book Two: King of the Vagabonds")
    output.append("3. Book Three: Odalisque")
    output.append("")
    output.append("=" * 50)
    output.append("")
    
    # Process each book
    books = [
        ('BOOK ONE: QUICKSILVER', '/home/agentcode/text summaries/output/summaries/quicksilver_book_one_all_summaries.txt'),
        ('BOOK TWO: KING OF THE VAGABONDS', '/home/agentcode/text summaries/output/summaries/quicksilver_book_two_all_summaries.txt'),
        ('BOOK THREE: ODALISQUE', '/home/agentcode/text summaries/output/summaries/quicksilver_book_three_all_summaries.txt')
    ]
    
    for book_title, file_path in books:
        # Add book section
        output.append(book_title)
        output.append("=" * len(book_title))
        output.append("")
        
        # Read summaries
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse summaries
        parts = content.split('=== SUMMARY')
        chunk_count = 0
        
        for part in parts[1:]:
            if part.strip():
                lines = part.strip().split('\n')
                
                # Find header
                header_line = None
                for i, line in enumerate(lines):
                    if 'Words' in line and '===':
                        header_line = 'SUMMARY' + line.replace(' ===', '')
                        break
                
                # Find word count and summary
                word_count_line = None
                summary_text = None
                for i, line in enumerate(lines):
                    if line.strip().startswith('Word count:'):
                        word_count_line = line.strip()
                        # Collect all non-empty lines after word count
                        text_lines = []
                        for j in range(i+1, len(lines)):
                            if lines[j].strip():
                                text_lines.append(lines[j].strip())
                        if text_lines:
                            summary_text = ' '.join(text_lines)
                        break
                
                if header_line and word_count_line and summary_text:
                    chunk_count += 1
                    # Add summary with proper formatting
                    output.append(header_line)
                    output.append("-" * len(header_line))
                    output.append(word_count_line)
                    output.append("")
                    
                    # Word wrap the summary text for better readability
                    import textwrap
                    wrapped_text = textwrap.fill(summary_text, width=80)
                    output.append(wrapped_text)
                    output.append("")
                    output.append("-" * 50)
                    output.append("")
        
        output.append(f"Total chunks in {book_title}: {chunk_count}")
        output.append("")
        output.append("=" * 50)
        output.append("")
    
    # Save structured text file
    with open('/home/agentcode/text summaries/output/Quicksilver_Book_Summaries_Formatted.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Created: Quicksilver_Book_Summaries_Formatted.txt")

if __name__ == "__main__":
    print("Creating readable formats with fixed parsing...")
    
    # Create all three formats
    create_markdown_summaries()
    create_html_summaries()
    create_structured_text()
    
    print("\nAll formats created successfully with actual content!")