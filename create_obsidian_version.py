#!/usr/bin/env python3
"""
Convert the compiled book_one.md to Obsidian format with wiki links
and create character index pages
"""

import re
import os

# Major characters to convert to wiki links
CHARACTERS = [
    "Daniel Waterhouse",
    "Isaac Newton",
    "Enoch Root",
    "Ben Franklin",
    "Robert Hooke", 
    "John Wilkins",
    "Roger Comstock",
    "Eliza",
    "Jack Shaftoe",
    "Bob Shaftoe",
    "Leibniz",
    "Samuel Pepys",
    "Princess Caroline",
    "Eleanor",
    "Drake Waterhouse",
    "Jeffreys",
    "William of Orange",
    "Louis XIV",
    "Charles II",
    "James II",
    "Oldenburg",
    "Rossignol",
    "Liselotte",
    "Madame",
    "Monsieur",
    "Étienne d'Arcachon",
    "Marie",
    "Brigitte",
    "Frau Heppner",
    "van Hoek",
    "Dappa",
    "Earl of Upnor",
    "Nicolas Fatio",
    "Christiaan Huygens",
    "Christopher Wren",
    "Robert Boyle",
    "Edmund Palling",
    "Wait Still Waterhouse",
    "Faith Waterhouse",
    "Godfrey Waterhouse",
    "Princess Eleanor",
    "Caroline",  # Sometimes called Princess Caroline, sometimes just Caroline
    "d'Avaux",
    "Father Édouard de Gex",
    "Count Fenil",
    "Dr. Alkmaar",
    "Bonaventure Rossignol"
]

# Key concepts/locations to link
CONCEPTS = [
    "Royal Society",
    "Trinity College",
    "Natural Philosophy",
    "Alchemy",
    "Massachusetts Bay Colony Institute of Technologickal Arts",
    "Gresham College",
    "Stourbridge Fair",
    "Great Fire of London",
    "Glorious Revolution",
    "Newton-Leibniz dispute",
    "Principia Mathematica",
    "Versailles",
    "The Hague",
    "Binnenhof",
    "Star Chamber",
    "Tower of London",
    "Bedlam",
    "V.O.C.",
    "Philosophical Language"
]

def extract_summaries_with_mentions(content):
    """Extract summaries and track which characters appear in each"""
    summaries = {}
    character_mentions = {char: [] for char in CHARACTERS}
    
    # Find all summaries
    pattern = r'## Summary (\d+): Words \d+-\d+\n\n\*Word count: \d+\*\n\n(.*?)(?=\n\n## Summary|\Z)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        num = int(match.group(1))
        text = match.group(2)
        summaries[num] = text
        
        # Track character mentions
        for char in CHARACTERS:
            if char.lower() in text.lower():
                character_mentions[char].append(num)
    
    return summaries, character_mentions

def add_wiki_links(content):
    """Add wiki links to character names and concepts"""
    # Create a copy to modify
    modified = content
    
    # Sort by length (longest first) to avoid partial replacements
    all_terms = CHARACTERS + CONCEPTS
    all_terms.sort(key=len, reverse=True)
    
    for term in all_terms:
        # Skip if already a wiki link
        if f"[[{term}]]" in modified:
            continue
            
        # Use word boundaries to avoid partial matches
        # But be flexible with possessives and plurals
        patterns = [
            (rf'\b{re.escape(term)}(?:\'s)?\b', f"[[{term}]]$1"),  # Handle possessives
            (rf'\b{re.escape(term)}s\b', f"[[{term}]]s"),  # Handle plurals
        ]
        
        for pattern, replacement in patterns:
            # Don't replace inside existing wiki links or headers
            # Use negative lookbehind and lookahead
            safe_pattern = rf'(?<!\[\[){pattern}(?![\]\|])'
            modified = re.sub(safe_pattern, lambda m: f"[[{term}]]" + m.group(0)[len(term):], modified, flags=re.IGNORECASE)
    
    return modified

def create_character_page(character, mentions, summaries):
    """Create a character index page"""
    content = f"# {character}\n\n"
    content += f"**Appears in {len(mentions)} summaries**\n\n"
    
    if mentions:
        for num in sorted(mentions):
            if num in summaries:
                # Get first 100 chars of summary for context
                preview = summaries[num][:100].replace('\n', ' ') + "..."
                content += f"- [[Book One#summary-{num}-words-{(num-1)*2000+1}-{num*2000}|Summary {num}]]: {preview}\n"
    else:
        content += "*No direct mentions found in the summaries.*\n"
    
    content += "\n---\n"
    content += "[[Book One]] | [[Character Index]]\n"
    
    return content

def create_character_index(character_mentions):
    """Create main character index page"""
    content = "# Character Index - Quicksilver Book One\n\n"
    
    # Group by frequency
    by_frequency = sorted([(char, len(mentions)) for char, mentions in character_mentions.items() if mentions], 
                         key=lambda x: x[1], reverse=True)
    
    content += "## Major Characters (by frequency)\n\n"
    for char, count in by_frequency[:10]:
        content += f"- [[{char}]] ({count} summaries)\n"
    
    content += "\n## All Characters\n\n"
    for char in sorted(CHARACTERS):
        if character_mentions[char]:
            content += f"- [[{char}]]\n"
    
    content += "\n---\n"
    content += "[[Book One]]\n"
    
    return content

def main():
    # Read the original compiled markdown
    with open('output/books/quicksilver/book_one/formatted/book_one.md', 'r') as f:
        content = f.read()
    
    # Extract summaries and character mentions
    print("Extracting summaries and character mentions...")
    summaries, character_mentions = extract_summaries_with_mentions(content)
    
    # Add wiki links
    print("Adding wiki links...")
    enhanced_content = add_wiki_links(content)
    
    # Add navigation at the end
    enhanced_content += "\n\n---\n\n"
    enhanced_content += "[[Character Index]] | [[Quicksilver Overview]]\n"
    
    # Write enhanced version
    output_path = 'output/obsidian/Book One.md'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(enhanced_content)
    print(f"Created: {output_path}")
    
    # Create character pages
    print("\nCreating character pages...")
    for char in CHARACTERS:
        if character_mentions[char]:  # Only create pages for characters that appear
            char_content = create_character_page(char, character_mentions[char], summaries)
            char_filename = char.replace(' ', '_').replace("'", "").replace(".", "")
            char_path = f'output/obsidian/characters/{char_filename}.md'
            with open(char_path, 'w') as f:
                f.write(char_content)
            print(f"Created: {char_path}")
    
    # Create character index
    index_content = create_character_index(character_mentions)
    with open('output/obsidian/Character Index.md', 'w') as f:
        f.write(index_content)
    print("\nCreated: output/obsidian/Character Index.md")
    
    print("\nDone! Copy the 'output/obsidian' folder to your Obsidian vault.")

if __name__ == "__main__":
    main()