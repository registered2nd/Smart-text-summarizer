#!/usr/bin/env python3
"""
Helper script to process remaining chunks systematically
"""

import os
from pathlib import Path

def count_words(text):
    return len(text.split())

def adjust_to_150_words(text):
    """Adjust text to be exactly 150 words"""
    words = text.split()
    if len(words) > 150:
        return ' '.join(words[:150])
    elif len(words) < 150:
        # This shouldn't happen with properly written summaries
        return text
    return text

# Check which summaries have been completed
summaries_dir = Path("/home/agentcode/text summaries/output/summaries")
chunks_dir = Path("/home/agentcode/text summaries/output/chunks")

completed = []
remaining = []

for i in range(1, 55):
    summary_file = summaries_dir / f"summary_{i:03d}.txt"
    chunk_file = chunks_dir / f"chunk_{i:03d}.txt"
    
    if summary_file.exists():
        # Check if it's a real summary or placeholder
        with open(summary_file, 'r') as f:
            content = f.read()
            if "NEEDS MANUAL SUMMARY" not in content:
                completed.append(i)
            else:
                remaining.append(i)
    else:
        remaining.append(i)

print(f"Completed summaries: {len(completed)}")
print(f"Remaining summaries: {len(remaining)}")
print(f"\nCompleted: {completed}")
print(f"\nRemaining: {remaining[:10]}...")  # Show first 10 remaining

# Create a template for batch processing
print("\n\nNext chunks to process:")
for i in remaining[:5]:
    print(f"- chunk_{i:03d}.txt")