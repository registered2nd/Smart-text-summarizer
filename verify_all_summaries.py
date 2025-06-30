#!/usr/bin/env python3
"""Thoroughly verify that ALL summaries match their labeled chunks"""

import re
import os

def extract_key_phrases(text, num_phrases=5):
    """Extract distinctive phrases from text"""
    # Look for proper nouns, unique phrases
    words = text.split()
    # Get capitalized words (likely names/places)
    capitals = [w for w in words if w and len(w) > 3 and w[0].isupper()]
    
    # Filter out common words
    common_words = {'Word', 'The', 'This', 'That', 'These', 'Those', 'Summary', 
                    'After', 'Before', 'During', 'Through', 'Chapter', 'Book'}
    
    seen = set()
    unique = []
    for w in capitals:
        # Clean punctuation
        clean_w = w.strip('.,!?;:"')
        if clean_w not in seen and clean_w not in common_words:
            seen.add(clean_w)
            unique.append(clean_w)
        if len(unique) >= num_phrases:
            break
    return unique

print("Comprehensive verification of ALL summaries...\n")

# Read summaries
with open('output/books/quicksilver/book_one/summaries/all_summaries.txt', 'r') as f:
    summaries_content = f.read()

# Parse ALL summaries
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

print(f"Found {len(summaries)} summaries to verify\n")

# Check EVERY summary
total_checked = 0
total_mismatches = 0
word_range_errors = []
content_mismatches = []
missing_chunks = []

for num in sorted(summaries.keys()):
    total_checked += 1
    
    # Check word range
    expected_start = (num - 1) * 2000 + 1
    expected_end = num * 2000
    
    if summaries[num]['start'] != expected_start or summaries[num]['end'] != expected_end:
        word_range_errors.append({
            'num': num,
            'expected': f"{expected_start}-{expected_end}",
            'actual': f"{summaries[num]['start']}-{summaries[num]['end']}"
        })
    
    # First extract the chunk if needed
    os.system(f'cd "/home/agentcode/text summaries" && python3 extract_chunks_flexible.py output/books/quicksilver/book_one/chunks/all_chunks.txt {num} {num} >/dev/null 2>&1')
    
    # Check if chunk file exists in the correct location
    chunk_file = f'output/books/quicksilver/book_one/chunks/individual_chunks/chunk{num}.txt'
    
    # Now check content match
    if os.path.exists(chunk_file):
        try:
            with open(chunk_file, 'r') as f:
                chunk_content = f.read().lower()
            
            # Check if key phrases from summary appear in chunk
            summary_phrases = summaries[num]['key_phrases']
            
            if len(summary_phrases) >= 3:
                found = 0
                not_found = []
                for phrase in summary_phrases[:5]:  # Check up to 5 key phrases
                    if phrase.lower() in chunk_content:
                        found += 1
                    else:
                        not_found.append(phrase)
                
                # Flag if less than 40% of key phrases found
                if found < len(summary_phrases[:5]) * 0.4:
                    content_mismatches.append({
                        'num': num,
                        'summary_phrases': summary_phrases[:5],
                        'not_found': not_found,
                        'match_rate': f"{found}/{min(5, len(summary_phrases))}"
                    })
                    total_mismatches += 1
                    print(f"❌ Summary {num}: Only {found}/{min(5, len(summary_phrases))} key phrases found")
                else:
                    print(f"✓ Summary {num}: {found}/{min(5, len(summary_phrases))} key phrases match")
            else:
                print(f"⚠️  Summary {num}: Too few key phrases to verify effectively")
                
        except Exception as e:
            print(f"⚠️  Summary {num}: Error reading chunk - {e}")
    else:
        missing_chunks.append(num)
        print(f"⚠️  Summary {num}: Chunk file not found")

# Summary report
print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
print(f"Total summaries checked: {total_checked}")
print(f"Word range errors: {len(word_range_errors)}")
print(f"Content mismatches: {len(content_mismatches)}")
print(f"Missing chunk files: {len(missing_chunks)}")

if word_range_errors:
    print("\n❌ WORD RANGE ERRORS:")
    for err in word_range_errors[:5]:  # Show first 5
        print(f"  Summary {err['num']}: Expected {err['expected']}, got {err['actual']}")
    if len(word_range_errors) > 5:
        print(f"  ... and {len(word_range_errors) - 5} more")

if content_mismatches:
    print("\n❌ CONTENT MISMATCHES (possible shifted summaries):")
    for mis in content_mismatches[:5]:  # Show first 5
        print(f"  Summary {mis['num']}: {mis['match_rate']} matches")
        print(f"    Missing phrases: {', '.join(mis['not_found'][:3])}")
    if len(content_mismatches) > 5:
        print(f"  ... and {len(content_mismatches) - 5} more")

if missing_chunks:
    print(f"\n⚠️  MISSING CHUNKS: {missing_chunks[:10]}")
    if len(missing_chunks) > 10:
        print(f"  ... and {len(missing_chunks) - 10} more")

# Check for shift pattern
if content_mismatches:
    print("\n🔍 CHECKING FOR SYSTEMATIC SHIFT...")
    # Check if mismatches follow a pattern
    mismatch_nums = [m['num'] for m in content_mismatches]
    if all(n > 18 for n in mismatch_nums):
        print("  ⚠️  All mismatches occur after summary 18 - suggests shift due to duplicates")
    else:
        print("  Mismatches appear random, not following a clear pattern")

# Final verdict
print("\n" + "="*60)
if total_mismatches == 0 and len(word_range_errors) == 0:
    print("✅ VERDICT: All summaries appear to be correctly matched!")
else:
    print("❌ VERDICT: Issues detected - some summaries may need regeneration")
    print(f"   Total issues: {total_mismatches + len(word_range_errors)}")