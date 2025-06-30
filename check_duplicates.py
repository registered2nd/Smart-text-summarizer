#!/usr/bin/env python3
"""Simple check for duplicate summaries"""

# Read the summaries file
with open('output/book1_reprocessed/quicksilver_book_one_summaries.txt', 'r') as f:
    content = f.read()

# Split by summary marker
parts = content.split('=== SUMMARY ')
summaries = []

for part in parts[1:]:  # Skip first empty part
    if ':' in part:
        num = part.split(':')[0].strip()
        # Get the actual summary text (skip header lines)
        lines = part.split('\n')
        if len(lines) > 2:
            text = '\n'.join(lines[2:]).strip()
            summaries.append((num, text[:300]))  # First 300 chars

print(f"Checking {len(summaries)} summaries for duplicates...\n")

# Compare each summary with others
duplicates_found = False
for i in range(len(summaries)):
    for j in range(i + 1, len(summaries)):
        if summaries[i][1] and summaries[j][1]:
            # Check if texts are very similar (first 200 chars match)
            if summaries[i][1][:200] == summaries[j][1][:200]:
                print(f"POSSIBLE DUPLICATE:")
                print(f"  Summary {summaries[i][0]} and Summary {summaries[j][0]}")
                print(f"  Text preview: {summaries[i][1][:100]}...")
                print()
                duplicates_found = True

if not duplicates_found:
    print("No exact duplicates found in first 200 characters.")

# Look for chronological issues
print("\nChecking for text that seems out of chronological order...")
print("(Looking for later events mentioned in earlier summaries)\n")

# Key events and their approximate locations
key_events = [
    ("Enoch meets Ben Franklin", 1, 5),
    ("Stourbridge Fair", 15, 20),
    ("Newton's telescope", 25, 30),
    ("Daniel imprisoned Tower", 51, 55),
    ("Jeffreys", 50, 75),
    ("Glorious Revolution", 65, 75),
    ("kidney stone surgery", 75, 80)
]

for event, expected_start, expected_end in key_events:
    print(f"\nSearching for '{event}' (expected around summaries {expected_start}-{expected_end}):")
    found_in = []
    for num, text in summaries:
        if event.lower() in text.lower():
            found_in.append(int(num))
    
    if found_in:
        found_in.sort()
        print(f"  Found in summaries: {found_in}")
        out_of_range = [n for n in found_in if n < expected_start - 5 or n > expected_end + 5]
        if out_of_range:
            print(f"  WARNING: Found in unexpected summaries: {out_of_range}")