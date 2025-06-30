#!/usr/bin/env python3
"""
Extract specific chunks from the main chunks file and save as individual files
with flexible output directory
"""
import re
import sys
import os

def extract_chunks(chunks_file, start_num, end_num, output_dir=None):
    """Extract chunks from start_num to end_num"""
    # Default output directory is next to the chunks file
    if output_dir is None:
        base_dir = os.path.dirname(chunks_file)
        output_dir = os.path.join(base_dir, 'individual_chunks')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    with open(chunks_file, 'r') as f:
        content = f.read()
    
    for i in range(start_num, end_num + 1):
        # Find the chunk
        pattern = f"=== CHUNK {i}: Words \\d+-\\d+ ===\n(.*?)(?==== CHUNK {i+1}:|$)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            chunk_content = match.group(0).strip()
            output_file = os.path.join(output_dir, f"chunk{i}.txt")
            
            with open(output_file, 'w') as out:
                out.write(chunk_content)
            print(f"Extracted chunk {i} to {output_file}")
        else:
            print(f"Could not find chunk {i}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python extract_chunks_flexible.py <chunks_file> <start_num> <end_num> [output_dir]")
        sys.exit(1)
    
    chunks_file = sys.argv[1]
    start_num = int(sys.argv[2])
    end_num = int(sys.argv[3])
    output_dir = sys.argv[4] if len(sys.argv) > 4 else None
    
    extract_chunks(chunks_file, start_num, end_num, output_dir)