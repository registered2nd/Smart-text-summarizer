# Text Summaries Project - CLAUDE.md

## Project Overview
This project processes EPUB books (specifically Neal Stephenson's Quicksilver trilogy) by extracting specific sections, creating 2000-word chunks, and generating 140-160 word summaries for each chunk.

## Current Task
Processing Quicksilver Book One: 237,612 words divided into 119 chunks
- Completed: Summaries 1-50
- In Progress: Summaries 51-119
- Output Directory: `/home/agentcode/text summaries/output/book1_reprocessed/`

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
python scripts/create_chunks.py input.txt output_chunks.txt --chunk-size 2000
```

### 3. extract_chunks_batch.py
**CRITICAL FOR LARGE FILES**: Extracts individual chunks when main file exceeds 256KB.
```python
python scripts/extract_chunks_batch.py quicksilver_book_one_chunks.txt 51 60
```

### 4. format_output.py
Generates HTML, Markdown, and text output files from summaries.
```python
python scripts/format_output.py -s summaries.txt -t "Quicksilver - Book One" \
    -a "Neal Stephenson" -o quicksilver_book_one_final -f all
```

## Handling Large Files (CRITICAL!)

When chunks file > 256KB (Read tool limit):

1. **Extract chunks in batches**:
   ```bash
   python scripts/extract_chunks_batch.py quicksilver_book_one_chunks.txt 51 60
   ```
   This creates: `individual_chunks/chunk51.txt` through `chunk60.txt`

2. **Read individually**:
   ```
   Read: /home/agentcode/text summaries/output/book1_reprocessed/individual_chunks/chunk51.txt
   ```

3. **Never use Bash to cat large files** - triggers approval prompts every ~2000 words

## Summary Format Requirements

Each summary MUST follow this exact format:
```
=== SUMMARY [number]: Words [start]-[end] ===
Word count: [140-160]
[Summary text capturing key events, character developments, and themes]

```
(Note the blank line after each summary)

## File Structure
```
text summaries/
├── books/                         # Source EPUB files
├── scripts/                       # Python processing scripts
├── output/
│   └── book1_reprocessed/        # Current working directory
│       ├── individual_chunks/     # Extracted chunk files
│       ├── quicksilver_book_one_chunks.txt    # All chunks (1.3MB - too large!)
│       ├── quicksilver_book_one_summaries.txt # Growing summaries file
│       └── quicksilver_book_one_final.*       # Final formatted outputs
└── CLAUDE.md                      # This file
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
- Book One ends: Before "BOOK TWO King of the Vagabonds"
- Total: 119 chunks, each ~2000 words
- Summaries must be 140-160 words each
- Read EVERY chunk before summarizing (no skipping!)
- The chunks file is too large for Read tool - MUST use individual extraction

## Next Steps
Continue with chunks 51-119 to complete Book One summaries.