#!/usr/bin/env python3
"""Check for duplicate or misplaced summaries"""

import re

# Read the summaries file
with open('output/book1_reprocessed/quicksilver_book_one_summaries.txt', 'r') as f:
    content = f.read()

# Split into individual summaries
summaries = content.split('\n\n\n')
summaries = [s.strip() for s in summaries if s.strip()]

print(f"Total summaries found: {len(summaries)}")
print("\nChecking for issues...")
print("=" * 80)

# Track summary texts to find duplicates
summary_texts = {}
issues_found = []

for i, summary in enumerate(summaries):
    lines = summary.split('\n')
    if len(lines) < 3:
        continue
        
    # Extract summary number and text
    header_match = re.match(r'=== SUMMARY (\d+):', lines[0])
    if not header_match:
        continue
        
    summary_num = int(header_match.group(1))
    summary_text = '\n'.join(lines[2:])  # Skip header and word count
    
    # Check if this exact text appears elsewhere
    if summary_text in summary_texts:
        issues_found.append(f"DUPLICATE TEXT: Summary {summary_num} has same text as Summary {summary_texts[summary_text]}")
    else:
        summary_texts[summary_text] = summary_num
    
    # Check for partial matches (first 200 characters)
    text_start = summary_text[:200].strip()
    for prev_num, prev_text in summary_texts.items():
        if prev_num != summary_text and text_start and text_start in prev_text:
            issues_found.append(f"PARTIAL MATCH: Beginning of Summary {summary_num} found in Summary {summary_texts.get(prev_text, '?')}")

# Check sequence
print("\nChecking summary sequence...")
for i in range(len(summaries)):
    if i > 0:
        lines = summaries[i].split('\n')
        if lines and '=== SUMMARY' in lines[0]:
            current_num = int(re.search(r'SUMMARY (\d+):', lines[0]).group(1))
            prev_lines = summaries[i-1].split('\n')
            if prev_lines and '=== SUMMARY' in prev_lines[0]:
                prev_num = int(re.search(r'SUMMARY (\d+):', prev_lines[0]).group(1))
                if current_num != prev_num + 1:
                    issues_found.append(f"SEQUENCE GAP: Summary {prev_num} followed by Summary {current_num}")

# Report issues
if issues_found:
    print("\nISSUES FOUND:")
    for issue in issues_found:
        print(f"  - {issue}")
else:
    print("\nNo obvious duplication or sequence issues found.")

# Show first 80 characters of each summary for manual review
print("\n\nFirst 80 characters of each summary for manual review:")
print("=" * 80)
for i, summary in enumerate(summaries[:30]):  # First 30 summaries
    lines = summary.split('\n')
    if len(lines) >= 3:
        header_match = re.match(r'=== SUMMARY (\d+):', lines[0])
        if header_match:
            num = header_match.group(1)
            text_preview = ' '.join(lines[2:])[:80].replace('\n', ' ')
            print(f"{num:3}: {text_preview}...")