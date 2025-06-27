import os
import shutil
from pathlib import Path

def copy_to_windows_structure():
    """Copy all output files to Windows-friendly directory structure"""
    
    # Define source and destination paths
    source_base = "/home/agentcode/text summaries"
    
    # Windows destination path (will work in WSL)
    # In WSL, Windows C: drive is mounted at /mnt/c/
    windows_base = "/mnt/c/OneDrive/Documents/Texts/Fiction/output-quicksilver"
    
    # Create the output directory if it doesn't exist
    os.makedirs(windows_base, exist_ok=True)
    
    # Create subdirectories
    chunks_dir = os.path.join(windows_base, "chunks")
    summaries_dir = os.path.join(windows_base, "summaries")
    os.makedirs(chunks_dir, exist_ok=True)
    os.makedirs(summaries_dir, exist_ok=True)
    
    print(f"Creating Windows directory structure at: C:\\OneDrive\\Documents\\Texts\\Fiction\\output-quicksilver")
    print("-" * 60)
    
    # Copy the main formatted files
    main_files = [
        ("output/Quicksilver_Book_Summaries.html", "Quicksilver_Book_Summaries.html"),
        ("output/Quicksilver_Book_Summaries.md", "Quicksilver_Book_Summaries.md"),
        ("output/Quicksilver_Book_Summaries_Formatted.txt", "Quicksilver_Book_Summaries_Formatted.txt")
    ]
    
    for src_file, dest_file in main_files:
        src_path = os.path.join(source_base, src_file)
        dest_path = os.path.join(windows_base, dest_file)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"✓ Copied: {dest_file}")
    
    # Copy chunk files
    chunk_files = [
        "quicksilver_book_one_all_chunks.txt",
        "quicksilver_book_two_all_chunks.txt",
        "quicksilver_book_three_all_chunks.txt"
    ]
    
    print("\nCopying chunk files...")
    for chunk_file in chunk_files:
        src_path = os.path.join(source_base, "output/chunks", chunk_file)
        dest_path = os.path.join(chunks_dir, chunk_file)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"✓ Copied: chunks/{chunk_file}")
    
    # Copy summary files
    summary_files = [
        "quicksilver_book_one_all_summaries.txt",
        "quicksilver_book_two_all_summaries.txt",
        "quicksilver_book_three_all_summaries.txt"
    ]
    
    print("\nCopying summary files...")
    for summary_file in summary_files:
        src_path = os.path.join(source_base, "output/summaries", summary_file)
        dest_path = os.path.join(summaries_dir, summary_file)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"✓ Copied: summaries/{summary_file}")
    
    print("\n" + "=" * 60)
    print("All files copied successfully!")
    print("\nWindows directory structure:")
    print("C:\\OneDrive\\Documents\\Texts\\Fiction\\output-quicksilver\\")
    print("├── Quicksilver_Book_Summaries.html    (Best for viewing)")
    print("├── Quicksilver_Book_Summaries.md      (Great for documentation)")
    print("├── Quicksilver_Book_Summaries_Formatted.txt")
    print("├── chunks\\")
    print("│   ├── quicksilver_book_one_all_chunks.txt")
    print("│   ├── quicksilver_book_two_all_chunks.txt")
    print("│   └── quicksilver_book_three_all_chunks.txt")
    print("└── summaries\\")
    print("    ├── quicksilver_book_one_all_summaries.txt")
    print("    ├── quicksilver_book_two_all_summaries.txt")
    print("    └── quicksilver_book_three_all_summaries.txt")
    
    # Create a simple README file
    readme_content = """Quicksilver - Processed Text Summaries
=====================================

This folder contains processed summaries of Neal Stephenson's "Quicksilver" (The Baroque Cycle, Vol. 1).

Files:
------
- Quicksilver_Book_Summaries.html - Open this in a web browser for the best reading experience
- Quicksilver_Book_Summaries.md - Markdown format, great for GitHub or documentation
- Quicksilver_Book_Summaries_Formatted.txt - Plain text with formatting

Folders:
--------
- chunks/ - Contains the 2000-word text chunks for each book
- summaries/ - Contains the 140-160 word summaries for each chunk

Processing Details:
------------------
- Book One: Quicksilver - 29 chunks
- Book Two: King of the Vagabonds - 29 chunks  
- Book Three: Odalisque - 29 chunks

Total: 87 summaries covering the entire book

Generated using the EPUB processing workflow.
"""
    
    readme_path = os.path.join(windows_base, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("\n✓ Created README.txt")

if __name__ == "__main__":
    copy_to_windows_structure()