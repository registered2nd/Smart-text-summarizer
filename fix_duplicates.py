#!/usr/bin/env python3
"""Fix duplicate summaries and EOF markers in summaries file"""

import re
import sys

def fix_summary_file(input_file, output_file):
    print(f"Reading {input_file}...")
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Remove EOF markers
    if 'EOF < /dev/null' in content:
        print("Found and removing EOF markers...")
        content = content.replace('EOF < /dev/null\n', '')
    
    # Parse all summaries
    summaries = {}
    duplicates = []
    
    # Find all summaries
    pattern = r'(=== SUMMARY (\d+): Words \d+-\d+ ===\nWord count: \d+\n.*?)(?=\n\n\n=== SUMMARY|\n\n\n?$)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        full_text = match.group(1)
        num = int(match.group(2))
        
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
    
    # Validate the output
    with open(output_file, 'r') as f:
        check_content = f.read()
    
    # Final checks
    if 'EOF < /dev/null' in check_content:
        print("ERROR: EOF markers still present!")
    else:
        print("✓ No EOF markers")
    
    # Check sequence
    numbers = [int(m.group(1)) for m in re.finditer(r'=== SUMMARY (\d+):', check_content)]
    if numbers == sorted(numbers):
        print("✓ Summaries are in correct order")
    else:
        print("ERROR: Summaries are not in order!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file + ".fixed"
    else:
        input_file = "output/book1_reprocessed/quicksilver_book_one_summaries.txt"
        output_file = "output/book1_reprocessed/quicksilver_book_one_summaries_fixed.txt"
    
    fix_summary_file(input_file, output_file)