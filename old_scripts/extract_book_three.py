import zipfile
import os
from bs4 import BeautifulSoup
import re

def extract_book_three():
    epub_path = "/home/agentcode/text summaries/books/Neal Stephenson - Quicksilver (The Baroque Cycle, Vol. 1) (2003).epub"
    
    # Extract and process Book Three
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # Get all HTML files
        html_files = [f for f in epub.namelist() if f.endswith('.html')]
        html_files.sort()
        
        book_three_text = []
        in_book_three = False
        
        for html_file in html_files:
            content = epub.read(html_file).decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            # Check if we've reached Book Three
            if 'BOOK THREE' in text and 'Odalisque' in text:
                in_book_three = True
                # Start collecting from this point
                lines = text.split('\n')
                book_start_index = None
                for i, line in enumerate(lines):
                    if 'BOOK THREE' in line:
                        book_start_index = i
                        break
                if book_start_index:
                    book_three_text.extend(lines[book_start_index:])
            elif in_book_three:
                # Check for end markers (Dramatis Personae, Acknowledgments, etc.)
                if any(marker in text for marker in ['DRAMATIS PERSONAE', 'Acknowledgments', 'About the Author']):
                    # Stop before these sections
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if any(marker in line for marker in ['DRAMATIS PERSONAE', 'Acknowledgments', 'About the Author']):
                            book_three_text.extend(lines[:i])
                            in_book_three = False
                            break
                else:
                    # Continue collecting Book Three content
                    book_three_text.extend(text.split('\n'))
    
    # Clean the text
    cleaned_lines = []
    for line in book_three_text:
        # Remove calibre markers and clean up
        line = re.sub(r'filepos\d+', '', line)
        line = re.sub(r'<[^>]+>', '', line)
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    # Join and normalize whitespace
    full_text = ' '.join(cleaned_lines)
    full_text = re.sub(r'\s+', ' ', full_text)
    
    # Save the full text
    output_path = "/home/agentcode/text summaries/output/summaries/quicksilver_book_three_full.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Count words
    word_count = len(full_text.split())
    
    # Verify extraction by showing first and last 200 words
    words = full_text.split()
    first_200 = ' '.join(words[:200])
    last_200 = ' '.join(words[-200:])
    
    print(f"Book Three extracted successfully!")
    print(f"Total word count: {word_count}")
    print(f"\nFirst 200 words:\n{first_200}")
    print(f"\nLast 200 words:\n{last_200}")
    
    return full_text, word_count

if __name__ == "__main__":
    text, count = extract_book_three()