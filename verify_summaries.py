#!/usr/bin/env python3
"""Verify that summaries actually match their labeled chunks"""

import re

def extract_key_phrases(text, num_phrases=5):
    """Extract distinctive phrases from text"""
    # Look for proper nouns, unique phrases
    words = text.split()
    # Get capitalized words (likely names/places)
    capitals = [w for w in words if w and w[0].isupper() and len(w) > 3]
    # Return first few unique ones
    seen = set()
    unique = []
    for w in capitals:
        if w not in seen and not w in ['Word', 'The', 'This', 'Summary']:
            seen.add(w)
            unique.append(w)
        if len(unique) >= num_phrases:
            break
    return unique

print("Verifying summaries match their chunks...\n")

# Read summaries
with open('output/book1_reprocessed/quicksilver_book_one_summaries_fixed.txt', 'r') as f:
    summaries_content = f.read()

# Parse summaries
summaries = {}
for match in re.finditer(r'=== SUMMARY (\d+): Words (\d+)-(\d+) ===\nWord count: \d+\n(.*?)(?=\n\n|$)', 
                        summaries_content, re.DOTALL):
    num = int(match.group(1))
    start_word = int(match.group(2))
    end_word = int(match.group(3))
    text = match.group(4).strip()
    summaries[num] = {
        'start': start_word,
        'end': end_word,
        'text': text,
        'key_phrases': extract_key_phrases(text)
    }

# Check a sample of summaries against their chunks
mismatches = []
checked = []

for num in [10, 15, 20, 25, 30, 35, 40, 45, 50]:  # Sample check
    if num not in summaries:
        continue
        
    chunk_file = f'output/book1_reprocessed/individual_chunks/chunk{num}.txt'
    try:
        with open(chunk_file, 'r') as f:
            chunk_content = f.read()
        
        # Check if key phrases from summary appear in chunk
        summary_phrases = summaries[num]['key_phrases']
        chunk_lower = chunk_content.lower()
        
        found = 0
        not_found = []
        for phrase in summary_phrases[:3]:  # Check first 3 key phrases
            if phrase.lower() in chunk_lower:
                found += 1
            else:
                not_found.append(phrase)
        
        checked.append(num)
        
        if found < 2 and len(summary_phrases) >= 3:  # Less than 2/3 found
            mismatches.append({
                'num': num,
                'summary_phrases': summary_phrases[:3],
                'not_found': not_found
            })
            print(f"❌ Summary {num}: Only {found}/3 key phrases found in chunk")
            print(f"   Missing: {not_found}")
        else:
            print(f"✓ Summary {num}: {found}/3 key phrases match")
            
    except FileNotFoundError:
        print(f"⚠️  Summary {num}: No chunk file found")

# Also check word ranges
print("\n\nChecking word ranges...")
for num in sorted(summaries.keys())[:20]:  # Check first 20
    expected_start = (num - 1) * 2000 + 1
    expected_end = num * 2000
    actual_start = summaries[num]['start']
    actual_end = summaries[num]['end']
    
    if actual_start != expected_start or actual_end != expected_end:
        print(f"❌ Summary {num}: Word range mismatch")
        print(f"   Expected: {expected_start}-{expected_end}")
        print(f"   Actual: {actual_start}-{actual_end}")

# Check for shifted content
print("\n\nChecking for shifted content after summary 18...")
if 17 in summaries and 19 in summaries:
    # Get key phrases from what's labeled as summary 19
    s19_phrases = summaries[19]['key_phrases']
    
    # Check if they appear in chunk 21 instead
    try:
        with open('output/book1_reprocessed/individual_chunks/chunk21.txt', 'r') as f:
            chunk21 = f.read().lower()
        
        found_in_21 = sum(1 for p in s19_phrases[:3] if p.lower() in chunk21)
        if found_in_21 >= 2:
            print("⚠️  WARNING: Summary 19 content appears to match chunk 21!")
            print("   This suggests all summaries after 18 are shifted by 2")
    except:
        pass

print(f"\n\nSummary: Checked {len(checked)} summaries")
if mismatches:
    print(f"Found {len(mismatches)} potential mismatches")
    print("\nRecommendation: Summaries after #18 may be shifted and need regeneration")
else:
    print("All checked summaries appear to match their chunks")