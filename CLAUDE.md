# Text Summaries Project - CLAUDE.md

## Project Overview
This project processes EPUB books by extracting specific sections, creating 2000-word chunks, and generating 140-160 word summaries for each chunk. Optimized for use with Claude Code for efficient batch processing and summary generation.

## Current Status
Ready for processing any text content:
- Core system validated and functional
- All scripts optimized for Claude Code integration
- Documentation complete
- Example workflow tested and proven

## Key Scripts and Their Purposes

### 1. extract_book_section_fixed.py
Universal EPUB section extractor using content markers with proper file sorting.
```python
python scripts/extract_book_section_fixed.py "book.epub" \
    --start-markers "Chapter 1" "Beginning text" \
    --end-markers "Chapter 2" "Ending text" \
    -o extracted_text.txt
```

### 2. create_chunks.py
Splits text into 2000-word chunks with smart merging of small final chunks.
```python
python3 create_chunks.py input.txt output_chunks.txt --chunk-size 2000
```

### 3. extract_chunks_batch.py
**CRITICAL FOR LARGE FILES**: Extracts individual chunks when main file exceeds 256KB.
```python
python3 extract_chunks_batch.py all_chunks.txt 1 10
```

### 4. format_output.py
Generates HTML, Markdown, and text output files from summaries.
```python
python format_output.py -s summaries.txt -t "Book Title" \
    -a "Author Name" -o output_name -f all
```

## Handling Large Files (CRITICAL!)

### Recommended Process with Claude Code:
1. **Extract individual chunks when main file >256KB**:
   ```bash
   python3 extract_chunks_batch.py all_chunks.txt 1 50
   ```

2. **Process in batches with Claude Code Task tool**:
   - Read chunks in sequence using Task tool for parallel processing
   - Validate chunk numbers match expected sequence
   - Check for duplicates/gaps in summaries
   - Write to temporary file first
   - Only append after validation passes

3. **Always validate before appending to avoid duplicates!**

## Summary Format Requirements

Each summary MUST follow this exact format:
```
=== SUMMARY [number]: Words [start]-[end] ===
Word count: [140-160]
[Summary text capturing key events, character developments, and themes]

```
(Note the blank line after each summary)

## Claude Code Integration

This system is optimized for use with Claude Code, which provides:
- **Parallel Processing**: Read multiple chunks simultaneously using Task tool
- **Memory Management**: Handle files exceeding Read tool's 256KB limit
- **Workflow Automation**: Track progress with TodoWrite/TodoRead tools
- **Natural Language Interface**: Create summaries through conversation
- **Validation**: Built-in checking for duplicates and gaps

### Best Practices with Claude Code:
1. Use Task tool for batch operations (reading 10+ chunks)
2. Create individual chunk files when main file >256KB
3. Validate summaries before appending to avoid duplicates
4. Use TodoWrite to track multi-step processes
5. Let Claude Code handle the summarization while you review

## File Structure
```
text-summarizer/
├── scripts/
│   └── extract_book_section_fixed.py    # EPUB extraction with proper sorting
├── create_chunks.py                     # Universal text chunking
├── extract_chunks_batch.py              # Individual chunk extraction
├── format_output.py                     # Multi-format output generation
├── process_book.py                      # Workflow orchestrator
├── output/                              # Generated content (git-ignored)
│   └── [your_projects]/                 # Project-specific outputs
├── .gitignore                          # Excludes output and source files
├── README.md                           # System documentation
└── CLAUDE.md                           # Claude Code integration guide
```

## Example Workflow

### 1. Extract text from source
```bash
# For EPUB files
python scripts/extract_book_section_fixed.py book.epub \
    --start-markers "Chapter 1" --end-markers "Epilogue" -o extracted.txt

# For plain text, just use your .txt file directly
```

### 2. Create chunks
```bash
python create_chunks.py extracted.txt chunks.txt -s 2000 -f numbered
```

### 3. Generate summaries with Claude Code
```
"Read chunks 1-10 and create 140-160 word summaries for each"
```

### 4. Format final output
```bash
python format_output.py -s summaries.txt -t "Book Title" -a "Author" -o final_output -f all
```

## Tips for Success

- Always use Claude Code's Task tool for batch processing
- Create individual chunk files when main file exceeds 256KB
- Validate summaries before appending to avoid duplicates
- Use TodoWrite to track progress on large projects
- Test with small examples before processing entire books