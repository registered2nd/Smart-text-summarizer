# Text Summaries Project - CLAUDE.md

## Project Overview
This project processes EPUB books by extracting specific sections, creating 2000-word chunks, and generating 140-160 word summaries for each chunk. Optimized for use with Claude Code for efficient batch processing and summary generation.

## Current Status
Quicksilver Book One: COMPLETED ✓
- Total: 138,663 words divided into 69 chunks (corrected from initial parsing error)
- All 69 summaries completed
- Output Directory: `/home/agentcode/text summaries/output/books/quicksilver/book_one_corrected/`
- Note: Original extraction had file sorting error that scrambled narrative order - now fixed using natural_sort_key function

## Key Scripts and Their Purposes

### 1. extract_book_section.py
Universal EPUB section extractor using content markers instead of line numbers.
```python
python scripts/extract_book_section.py "Neal Stephenson - Quicksilver.epub" \
    --start-markers "Boston Common" "OCTOBER 12, 1713" \
    --end-markers "BOOK TWO" "King of the Vagabonds"
```

### 2. create_chunks.py
Splits text into 2000-word chunks with smart merging of small final chunks.
```python
python3 create_chunks.py input.txt output/books/[book_name]/chunks/all_chunks.txt --chunk-size 2000
```

### 3. extract_chunks_batch.py
**CRITICAL FOR LARGE FILES**: Extracts individual chunks when main file exceeds 256KB.
```python
python3 extract_chunks_batch.py output/books/quicksilver/book_one/chunks/all_chunks.txt 51 60
```

### 4. format_output.py
Generates HTML, Markdown, and text output files from summaries.
```python
python scripts/format_output.py -s summaries.txt -t "Quicksilver - Book One" \
    -a "Neal Stephenson" -o quicksilver_book_one_final -f all
```

## Handling Large Files (CRITICAL!)

⚠️ **WARNING: The old method led to duplicate summaries!** See UPDATED_PROCESSING_METHOD.md for the validated approach.

### Quick Reference - Validated Process:
1. **Extract ALL chunks first**:
   ```bash
   python3 extract_chunks_batch.py output/books/[book_name]/chunks/all_chunks.txt 1 119
   ```

2. **Process in batches with validation**:
   - Read chunks in sequence
   - Validate chunk numbers match
   - Check for duplicates/gaps
   - Write to temporary file first
   - Only append after validation passes

3. **Never append directly to main file without validation!**

### Book One Status: COMPLETED ✓
- All 69 summaries completed (corrected count)
- Files properly ordered using numerical sorting
- Complete formatted output available in book_one_corrected/formatted/

See `UPDATED_PROCESSING_METHOD.md` for the validated workflow used.

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
text summaries/
├── books/                         # Source EPUB files
├── scripts/                       # Python processing scripts (deprecated)
├── output/
│   └── books/                     # All processed books
│       ├── quicksilver/
│       │   ├── book_one/
│       │   │   ├── chunks/
│       │   │   │   └── all_chunks.txt      # Original 2000-word chunks
│       │   │   ├── summaries/
│       │   │   │   └── all_summaries.txt   # 140-160 word summaries
│       │   │   └── formatted/
│       │   │       ├── book_one.html       # Formatted HTML output
│       │   │       ├── book_one.md         # Formatted Markdown output
│       │   │       └── book_one.txt        # Formatted plain text output
│       │   ├── book_two/          # (Future)
│       │   └── book_three/        # (Future)
│       └── [other_books]/         # Same structure for other books
│   └── obsidian/                  # Obsidian-enhanced versions
│       ├── Book One.md            # Enhanced with wiki links
│       ├── Character Index.md     # Character frequency overview
│       └── characters/            # Individual character pages
└── CLAUDE.md                      # This file
```

## Obsidian Integration

Due to Windows file watching limitations with WSL paths, Obsidian files are maintained at:
- **Windows Path**: `C:\ObsidianVaults\Quicksilver`
- **WSL Access**: `/mnt/c/ObsidianVaults/Quicksilver`

This allows:
- Windows Obsidian to work with full file watching
- WSL scripts to read/write via `/mnt/c/` path
- No sync issues or EISDIR errors

To update Obsidian content from WSL:
```bash
cp -r output/obsidian/* /mnt/c/ObsidianVaults/Quicksilver/
```

## Workflow for Continuing Summaries

1. Extract next batch of chunks:
   ```bash
   python /home/agentcode/text summaries/scripts/extract_chunks_batch.py \
       quicksilver_book_one_chunks.txt 51 60
   ```

2. Read each chunk:
   ```
   Read: individual_chunks/chunk51.txt
   ```

3. Write summary to temporary file

4. Append to main summaries:
   ```bash
   cat new_summaries.txt >> quicksilver_book_one_summaries.txt
   ```

5. Every 10-20 summaries, generate progress output:
   ```bash
   python /home/agentcode/text summaries/scripts/format_output.py \
       -s quicksilver_book_one_summaries.txt \
       -t "Quicksilver - Book One" -a "Neal Stephenson" \
       -o quicksilver_book_one_progress -f all
   ```

## Important Notes

- Book One starts: "Boston Common OCTOBER 12, 1713" (Enoch meeting Ben Franklin)
- Book One ends: "sailing large before a quartering wind" (Minerva escaping Blackbeard)
- Total: 69 chunks, each ~2000 words = 138,663 words total
- Summaries must be 140-160 words each
- The fixed extraction script (extract_book_section_fixed.py) uses numerical sorting to maintain proper file order
- Use create_chunks.py with -f numbered option to create individual chunk files for easier reading

## Next Steps
Book One is complete. Ready to proceed with Book Two: "King of the Vagabonds"