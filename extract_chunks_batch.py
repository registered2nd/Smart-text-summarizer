#!/usr/bin/env python3
"""
Extract specific chunks from the main chunks file and save as individual files
"""
import re
import sys

def extract_chunks(chunks_file, start_num, end_num):
    """Extract chunks from start_num to end_num"""
    with open(chunks_file, 'r') as f:
        content = f.read()
    
    for i in range(start_num, end_num + 1):
        # Find the chunk
        pattern = f"=== CHUNK {i}: Words \\d+-\\d+ ===\n(.*?)(?==== CHUNK {i+1}:|$)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            chunk_content = match.group(0).strip()
            output_file = f"output/book1_reprocessed/individual_chunks/chunk{i}.txt"
            
            with open(output_file, 'w') as out:
                out.write(chunk_content)
            print(f"Extracted chunk {i}")
        else:
            print(f"Could not find chunk {i}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_chunks_batch.py <chunks_file> <start_num> <end_num>")
        sys.exit(1)
    
    chunks_file = sys.argv[1]
    start_num = int(sys.argv[2])
    end_num = int(sys.argv[3])
    
    extract_chunks(chunks_file, start_num, end_num)