# Book Processing Method for Large EPUB Files

## Problem
When processing large books (like Quicksilver Book One with 237,612 words), the chunks file exceeds Claude's Read tool limit of 256KB, making it impossible to read the entire file at once.

## Solution: Individual Chunk Extraction

### Step 1: Extract Individual Chunks
Use the `extract_chunks_batch.py` script to extract specific chunks into individual files:

```bash
cd /home/agentcode/text summaries/output/book1_reprocessed
python /home/agentcode/text summaries/scripts/extract_chunks_batch.py quicksilver_book_one_chunks.txt 51 60
```

This creates:
- `individual_chunks/chunk51.txt`
- `individual_chunks/chunk52.txt`
- ... up to `chunk60.txt`

### Step 2: Read Each Chunk
Use the Read tool on individual chunk files:
```
Read: /home/agentcode/text summaries/output/book1_reprocessed/individual_chunks/chunk51.txt
```

### Step 3: Write Summaries
For each chunk, write a 140-160 word summary in this format:
```
=== SUMMARY 51: Words 100001-102000 ===
Word count: 155
[Your summary text here capturing key events, character developments, and important themes]
```

### Step 4: Append to Main File
Add summaries to the main summaries file:
```bash
cat new_summaries.txt >> quicksilver_book_one_summaries.txt
```

## Why This Method?
1. **Avoids Read tool's 256KB limit** - Individual chunks are always small enough
2. **Avoids Bash approval prompts** - No need to cat large files through Bash
3. **Allows systematic progress** - Can process chunks in batches
4. **Maintains quality** - Each chunk is fully read before summarizing

## Current Progress
- Book One: 237,612 words = 119 chunks
- Summaries completed: 1-50
- Remaining: 51-119

## Scripts Location
- Extract script: `/home/agentcode/text summaries/scripts/extract_chunks_batch.py`
- Format script: `/home/agentcode/text summaries/scripts/format_output.py`
- Process script: `/home/agentcode/text summaries/scripts/process_book.py`