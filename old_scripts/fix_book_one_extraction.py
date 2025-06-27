import zipfile
from bs4 import BeautifulSoup
import re

def extract_book_one_properly():
    """Extract the actual Book One starting with Enoch in Boston"""
    epub_path = "/home/agentcode/text summaries/books/Neal Stephenson - Quicksilver (The Baroque Cycle, Vol. 1) (2003).epub"
    
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # Get all HTML files
        html_files = sorted([f for f in epub.namelist() if f.endswith('.html')])
        
        book_one_text = []
        found_start = False
        in_book_one = False
        
        for html_file in html_files:
            content = epub.read(html_file).decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for element in soup(["script", "style"]):
                element.extract()
            
            text = soup.get_text()
            
            # Look for the actual Book One start - Boston Common scene
            if 'Boston Common' in text and 'OCTOBER 12, 1713' in text and 'ENOCH ROUNDS THE CORNER' in text:
                found_start = True
                in_book_one = True
                lines = text.split('\n')
                
                # Find where this scene starts
                for i, line in enumerate(lines):
                    if 'Boston Common' in line:
                        # Start collecting from here
                        book_one_text.extend(lines[i:])
                        break
                        
            elif in_book_one:
                # Check if we've reached Book Two
                if 'BOOK TWO' in text and 'King of the Vagabonds' in text:
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if 'BOOK TWO' in line:
                            # Add content up to this point
                            book_one_text.extend(lines[:i])
                            in_book_one = False
                            break
                else:
                    # Continue collecting Book One content
                    book_one_text.extend(text.split('\n'))
    
    # Clean the text
    cleaned_lines = []
    for line in book_one_text:
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'filepos\d+', '', line)
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    # Join text
    full_text = ' '.join(cleaned_lines)
    full_text = re.sub(r'\s+', ' ', full_text)
    
    # Save the corrected full text
    with open('/home/agentcode/text summaries/output/book_one_corrected.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"Book One extracted properly")
    print(f"Total words: {len(full_text.split())}")
    print(f"\nFirst 300 words:")
    print(' '.join(full_text.split()[:300]))
    
    return full_text

if __name__ == "__main__":
    extract_book_one_properly()