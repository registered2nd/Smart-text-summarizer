import zipfile
from bs4 import BeautifulSoup
import re

def extract_book_one_properly():
    """Extract Book One from the EPUB using content markers, not line numbers"""
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
            
            # Look for the start of Book One - multiple possible markers
            if not found_start:
                if ('Boston Common' in text and 'OCTOBER 12, 1713' in text) or \
                   ('ENOCH ROUNDS THE CORNER' in text) or \
                   ('BOOK ONE' in text and 'Quicksilver' in text and 'Boston' in text):
                    found_start = True
                    in_book_one = True
                    
                    # Find the exact starting point
                    lines = text.split('\n')
                    start_index = None
                    
                    # Look for different possible starting points
                    for i, line in enumerate(lines):
                        # Primary marker: ENOCH ROUNDS THE CORNER
                        if 'ENOCH ROUNDS THE CORNER' in line:
                            start_index = i
                            break
                        # Alternative: Boston Common header
                        elif 'Boston Common' in line and i < len(lines) - 1:
                            # Check if next lines contain the date
                            next_few_lines = ' '.join(lines[i:i+3])
                            if 'OCTOBER 12, 1713' in next_few_lines:
                                start_index = i
                                break
                    
                    if start_index is not None:
                        book_one_text.extend(lines[start_index:])
                        print(f"Found Book One start in {html_file} at line {start_index}")
                        print(f"First line: {lines[start_index][:100]}...")
                    else:
                        # If we can't find the exact start, include the whole file
                        book_one_text.extend(lines)
                        print(f"Including full content from {html_file} (couldn't find exact start)")
                        
            elif in_book_one:
                # Check if we've reached Book Two
                if 'BOOK TWO' in text and 'King of the Vagabonds' in text:
                    lines = text.split('\n')
                    end_index = None
                    
                    for i, line in enumerate(lines):
                        if 'BOOK TWO' in line:
                            end_index = i
                            print(f"Found Book Two start in {html_file} at line {i}")
                            break
                    
                    if end_index is not None:
                        # Add content up to Book Two
                        book_one_text.extend(lines[:end_index])
                    
                    in_book_one = False
                    break
                else:
                    # Continue collecting Book One content
                    book_one_text.extend(text.split('\n'))
    
    # Clean the text
    cleaned_lines = []
    for line in book_one_text:
        line = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
        line = re.sub(r'filepos\d+', '', line)  # Remove filepos markers
        line = re.sub(r'calibre\d+', '', line)  # Remove calibre markers
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    # Join text
    full_text = ' '.join(cleaned_lines)
    full_text = re.sub(r'\s+', ' ', full_text)  # Normalize whitespace
    
    # Verify we got the right content
    words = full_text.split()
    word_count = len(words)
    first_500_words = ' '.join(words[:500])
    last_500_words = ' '.join(words[-500:])
    
    print(f"\nExtraction complete!")
    print(f"Total words: {word_count:,}")
    print(f"\nFirst 500 words:")
    print("-" * 80)
    print(first_500_words)
    print("-" * 80)
    print(f"\nLast 500 words:")
    print("-" * 80)
    print(last_500_words)
    print("-" * 80)
    
    # Check for expected content
    if 'ENOCH' in first_500_words.upper() and 'BOSTON' in first_500_words.upper():
        print("\n✓ Verified: Found Enoch in Boston at the beginning")
    else:
        print("\n⚠ WARNING: Expected to find Enoch in Boston at the beginning")
    
    if 'MINERVA' in last_500_words:
        print("✓ Verified: Found Minerva near the end")
    else:
        print("⚠ WARNING: Expected to find Minerva near the end")
    
    return full_text, word_count

def create_chunks(text, chunk_size=2000):
    """Split text into chunks of approximately chunk_size words"""
    words = text.split()
    total_words = len(words)
    chunks = []
    
    for i in range(0, total_words, chunk_size):
        chunk_words = words[i:i + chunk_size]
        
        # If this is the last chunk and it's less than 1000 words, merge with previous
        if i + chunk_size >= total_words and len(chunk_words) < 1000 and chunks:
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

def save_chunks(chunks, output_file):
    """Save chunks to a single file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(f"=== CHUNK {chunk['number']}: Words {chunk['start']}-{chunk['end']} ===\n")
            f.write(chunk['text'])
            f.write("\n\n")
    
    print(f"\nSaved {len(chunks)} chunks to {output_file}")

def main():
    print("Extracting Book One from Quicksilver EPUB...")
    print("=" * 80)
    
    # Extract Book One
    book_one_text, word_count = extract_book_one_properly()
    
    # Save full text
    full_text_file = "/home/agentcode/text summaries/output/book_one_full_corrected.txt"
    with open(full_text_file, 'w', encoding='utf-8') as f:
        f.write(book_one_text)
    print(f"\nSaved full text to: {full_text_file}")
    
    # Create chunks
    chunks = create_chunks(book_one_text)
    
    # Save chunks
    chunks_file = "/home/agentcode/text summaries/output/chunks/quicksilver_book_one_all_chunks_corrected.txt"
    save_chunks(chunks, chunks_file)
    
    # Print summary
    print(f"\nSummary:")
    print(f"- Total words: {word_count:,}")
    print(f"- Total chunks: {len(chunks)}")
    print(f"- Average words per chunk: {word_count // len(chunks):,}")
    
    return book_one_text, chunks

if __name__ == "__main__":
    main()