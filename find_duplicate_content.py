#!/usr/bin/env python3
"""Find summaries that contain content from wrong chunks"""

import re

# Read all summaries
with open('output/book1_reprocessed/quicksilver_book_one_summaries.txt', 'r') as f:
    content = f.read()

# Extract summaries with their numbers
summaries = []
parts = content.split('=== SUMMARY ')
for part in parts[1:]:
    if ':' in part:
        match = re.match(r'(\d+): Words (\d+)-(\d+)', part)
        if match:
            num = int(match.group(1))
            start_word = int(match.group(2))
            end_word = int(match.group(3))
            lines = part.split('\n')
            if len(lines) > 2:
                text = '\n'.join(lines[2:]).strip()
                summaries.append({
                    'num': num,
                    'start': start_word,
                    'end': end_word,
                    'text': text
                })

print(f"Analyzing {len(summaries)} summaries...\n")

# Check if summary content matches its word range
issues = []
for s in summaries:
    expected_start = (s['num'] - 1) * 2000 + 1
    expected_end = s['num'] * 2000
    
    if s['start'] != expected_start or s['end'] != expected_end:
        issues.append(f"Summary {s['num']}: Word range mismatch - shows {s['start']}-{s['end']}, expected {expected_start}-{expected_end}")

# Check for summaries mentioning wrong chunk numbers
for s in summaries:
    # Look for mentions of "chunk" followed by a number
    chunk_mentions = re.findall(r'chunk[s]?\s*(\d+)', s['text'], re.IGNORECASE)
    for chunk_num in chunk_mentions:
        if int(chunk_num) != s['num']:
            issues.append(f"Summary {s['num']}: Mentions 'chunk {chunk_num}' but should be about chunk {s['num']}")
            print(f"\nSummary {s['num']} text preview:")
            print(s['text'][:200] + "...")

# Look for summaries that seem to be about different parts of the book
print("\nChecking for chronological inconsistencies...")

# Define key events and where they should appear
timeline = [
    ("Enoch", "Ben Franklin", "Boston", 1, 10),  # Opening scene
    ("Cambridge", "Trinity", "Newton", 10, 20),   # Daniel at Cambridge
    ("Stourbridge Fair", "prism", None, 17, 19), # Specific scene
    ("plague", "Cambridge", None, 20, 25),        # Plague years
    ("Fire of London", None, None, 25, 30),       # Great Fire
    ("Royal Society", "Hooke", None, 30, 40),     # RS meetings
    ("Tower of London", "prisoner", None, 50, 60), # Daniel imprisoned
    ("Eliza", "cipher", "embroidery", 55, 65),    # Eliza's story
    ("Glorious Revolution", "William", None, 65, 75), # Revolution
    ("surgery", "kidney stone", "Hooke", 75, 80)  # Surgery
]

for keywords in timeline:
    event_keys = [k for k in keywords[:-2] if k]  # Get non-None keywords
    expected_start, expected_end = keywords[-2:]
    
    found_in = []
    for s in summaries:
        if all(key.lower() in s['text'].lower() for key in event_keys):
            found_in.append(s['num'])
    
    if found_in:
        out_of_range = [n for n in found_in if n < expected_start - 2 or n > expected_end + 2]
        if out_of_range:
            event_desc = " + ".join(event_keys)
            issues.append(f"Chronology: '{event_desc}' found in summaries {out_of_range}, expected {expected_start}-{expected_end}")

if issues:
    print("\nISSUES FOUND:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\nNo major issues found.")