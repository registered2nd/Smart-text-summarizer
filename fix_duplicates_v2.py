#!/usr/bin/env python3
"""Fix duplicate summaries - improved version"""

import re
import sys

def fix_summary_file(input_file, output_file):
    print(f"Reading {input_file}...")
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Remove EOF markers if any
    if 'EOF < /dev/null' in content:
        print("Found and removing EOF markers...")
        content = content.replace('EOF < /dev/null\n', '')
    
    # Parse all summaries - use a more flexible pattern
    summaries = {}
    duplicates = []
    
    # Split by summary headers and process each
    parts = re.split(r'(=== SUMMARY \d+: Words \d+-\d+ ===)', content)
    
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            header = parts[i]
            # Extract summary number from header
            match = re.search(r'=== SUMMARY (\d+):', header)
            if match:
                num = int(match.group(1))
                # Get the content (header + text until next summary or end)
                full_text = header + parts[i+1].rstrip()
                
                if num in summaries:
                    duplicates.append(num)
                    print(f"WARNING: Found duplicate summary {num}")
                else:
                    summaries[num] = full_text
    
    # Report findings
    print(f"\nFound {len(summaries)} unique summaries")
    if duplicates:
        print(f"Duplicates found: {sorted(set(duplicates))}")
    
    # Check for gaps
    if summaries:
        expected = set(range(1, max(summaries.keys()) + 1))
        missing = expected - set(summaries.keys())
        if missing:
            print(f"Missing summaries: {sorted(missing)}")
    
    # Write in correct order
    print(f"\nWriting cleaned file to {output_file}...")
    with open(output_file, 'w') as f:
        for i in sorted(summaries.keys()):
            if i > 1:
                f.write('\n\n')
            f.write(summaries[i])
    
    print(f"Done! Wrote {len(summaries)} summaries in order.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file + ".cleaned"
    else:
        input_file = "output/book1_reprocessed/quicksilver_book_one_summaries_fixed.txt"
        output_file = "output/book1_reprocessed/quicksilver_book_one_summaries_final.txt"
    
    fix_summary_file(input_file, output_file)