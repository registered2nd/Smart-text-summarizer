#!/usr/bin/env python3
import re

with open('output/book1_reprocessed/quicksilver_book_one_summaries_fixed.txt', 'r') as f:
    content = f.read()
    
numbers = sorted([int(m.group(1)) for m in re.finditer(r'=== SUMMARY (\d+):', content)])
print(f'Summary numbers: {numbers[0]} to {numbers[-1]}')
print(f'Total count: {len(numbers)}')

# Check if there are duplicates
if len(numbers) != len(set(numbers)):
    print("WARNING: Duplicate summaries found!")
    for n in set(numbers):
        if numbers.count(n) > 1:
            print(f"  Summary {n} appears {numbers.count(n)} times")