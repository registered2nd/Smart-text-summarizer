# Text Chunking & Summarization System v1.0

A comprehensive system for processing any text content - including EPUB books, plain text, markdown, and other formats - into manageable chunks with structured summaries.

## Overview

This system processes text content by:
1. Extracting sections from various sources (EPUB, TXT, MD, etc.)
2. Dividing text into 2000-word chunks with intelligent merging
3. Facilitating creation of 140-160 word summaries per chunk
4. Generating formatted output in HTML, Markdown, and plain text

## Key Features

- **Universal text processing**: Works with any text format - EPUB, TXT, MD, or pasted content
- **Content-based extraction**: Uses text markers for reliable section extraction
- **Smart chunking**: Automatically merges small final chunks to maintain consistency
- **Flexible output formats**: HTML with navigation, Markdown, and plain text
- **Large file handling**: Extracts individual chunks when files exceed tool limits
- **EPUB support**: Includes specialized script with proper numerical file sorting

## System Requirements

- Python 3.x
- BeautifulSoup4 for EPUB parsing
- Claude Code environment (recommended for optimal workflow)

## Core Scripts

### 1. `extract_book_section_fixed.py` (EPUB-specific)
Extracts specific sections from EPUB files with proper numerical file sorting.

```bash
python scripts/extract_book_section_fixed.py "book.epub" \
    --start-markers "Chapter 1" "Beginning text" \
    --end-markers "Chapter 2" "Ending text" \
    -o output.txt
```

**Note**: This is the only EPUB-specific script. All other scripts work with any text format.

### 2. `create_chunks.py` (Universal)
Splits any text file into chunks of specified word count.

```bash
python create_chunks.py input.txt -o output_chunks.txt -s 2000 -f standard
# Use -f numbered to create individual chunk files
# Works with .txt, .md, or any plain text file
```

### 3. `extract_chunks_batch.py`
Extracts specific chunks as individual files for easier processing.

```bash
python extract_chunks_batch.py all_chunks.txt 1 10
# Creates individual files: chunk1.txt through chunk10.txt
```

### 4. `format_output.py`
Generates formatted output from summaries.

```bash
python format_output.py -s summaries.txt -t "Book Title" \
    -a "Author Name" -o output_name -f all
```

## Recommended Workflow with Claude Code

The system is designed to work optimally with Claude Code, which provides:
- Parallel processing capabilities for reading multiple chunks
- Natural language interface for summary creation
- Built-in file management and validation
- Integrated todo tracking for complex multi-step processes

### Example Claude Code Workflow:

1. **Extract book section**:
   ```
   "Extract Book One from the EPUB using the fixed extraction script"
   ```

2. **Create chunks**:
   ```
   "Create 2000-word chunks from the extracted text"
   ```

3. **Generate summaries**:
   ```
   "Read chunks 1-10 and create 140-160 word summaries for each"
   ```

4. **Format output**:
   ```
   "Generate HTML, Markdown, and text output from the summaries"
   ```

## File Structure

```
text_summarizer/
├── scripts/
│   └── extract_book_section_fixed.py
├── create_chunks.py
├── extract_chunks_batch.py
├── format_output.py
├── process_book.py
├── output/              # Generated content (git-ignored)
├── books/               # Source EPUB files (git-ignored)
├── CLAUDE.md            # Project-specific configuration
└── README.md            # This file
```

## Summary Format

Summaries must follow this exact format:
```
=== SUMMARY [number]: Words [start]-[end] ===
Word count: [140-160]
[Summary text capturing key events, character developments, and themes]

```
(Note the blank line after each summary)

## Version History

- **v1.0** (2025): Initial release with core functionality
  - Fixed numerical sorting bug in EPUB extraction
  - Validated workflow for processing long texts
  - Integrated Claude Code optimization

## License

This project is designed for educational and personal use.

## Contributing

When contributing, please:
1. Focus on core system functionality, not specific book processing
2. Maintain the clean separation between system scripts and output
3. Update documentation for any new features
4. Test with various EPUB formats