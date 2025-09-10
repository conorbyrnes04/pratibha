#!/usr/bin/env python3
"""
Intelligent Sanskrit Text → YAML Converter
Parses Sanskrit texts and extracts verses into structured YAML files.

Usage:
    python scripts/text_to_yaml.py input.txt output_dir --collection "Collection Name" --section "Section Name"
    
Example:
    python scripts/text_to_yaml.py bhagavad_gita.txt data/yaml/bhagavad_gita --collection "Bhagavad Gita" --section "Karma Yoga"
"""

import argparse
import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

def detect_verse_patterns(text: str) -> List[Tuple[str, str, str]]:
    """
    Intelligently detect verse patterns in Sanskrit text.
    Returns list of (verse_id, sanskrit, translation) tuples.
    """
    verses = []
    
    # Common verse patterns
    patterns = [
        # Pattern: "1.1" or "1:1" followed by Sanskrit text
        r'(\d+\.\d+)[\s:]+([^\n]+?)(?:\n|$)(.*?)(?=\d+\.\d+|$)',
        # Pattern: "Verse 1" or "Sloka 1" followed by text
        r'(?:verse|sloka|śloka)\s+(\d+)[\s:]+([^\n]+?)(?:\n|$)(.*?)(?=(?:verse|sloka|śloka)\s+\d+|$)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            verse_id, sanskrit, translation = match.groups()
            
            # Clean up text
            sanskrit = sanskrit.strip()
            translation = translation.strip()
            
            if sanskrit and len(sanskrit) > 10:  # Minimum length for Sanskrit
                verses.append((verse_id, sanskrit, translation))
    
    # If no patterns found, try to split by lines and group
    if not verses:
        lines = text.split('\n')
        current_verse = []
        verse_num = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line contains Sanskrit (Devanagari script)
            if re.search(r'[\u0900-\u097F]', line):
                if current_verse:
                    # Save previous verse
                    sanskrit = '\n'.join(current_verse)
                    verses.append((f"auto-{verse_num}", sanskrit, ""))
                    verse_num += 1
                    current_verse = []
                current_verse.append(line)
            else:
                if current_verse:
                    current_verse.append(line)
        
        # Don't forget the last verse
        if current_verse:
            sanskrit = '\n'.join(current_verse)
            verses.append((f"auto-{verse_num}", sanskrit, ""))
    
    return verses

def create_yaml_structure(verse_id: str, sanskrit: str, translation: str, 
                         collection: str, section: str) -> Dict:
    """Create a properly structured YAML object for a verse."""
    
    # Try to extract Sanskrit and transliteration
    sanskrit_lines = sanskrit.split('\n')
    sanskrit_text = sanskrit_lines[0] if sanskrit_lines else ""
    
    # Create transliteration (basic - you might want to enhance this)
    transliteration = ""
    if sanskrit_text:
        # This is a placeholder - you might want to use a proper Sanskrit transliteration library
        transliteration = f"Transliteration of {verse_id}"
    
    # Split translation into commentary if it's long
    translation_lines = translation.split('\n') if translation else []
    translation_text = translation_lines[0] if translation_lines else ""
    commentary_text = '\n'.join(translation_lines[1:]) if len(translation_lines) > 1 else ""
    
    return {
        "sutra_id": verse_id,
        "collection": collection,
        "section": section,
        "sanskrit": sanskrit_text,
        "transliteration": transliteration,
        "translation": translation_text,
        "commentary": commentary_text,
        "modes": {
            "bhasya": "",
            "doctrinal": "",
            "comparative": "",
            "sadhana": ""
        }
    }

def process_text_file(input_path: str, output_dir: str, collection: str, section: str):
    """Process a text file and convert it to YAML files."""
    
    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Detect verses
    verses = detect_verse_patterns(text)
    
    if not verses:
        print("Warning: No verses detected. Creating a single YAML file with the entire text.")
        # Create a single YAML file with the entire text
        yaml_obj = create_yaml_structure(
            "complete", text[:100] + "...", text, collection, section
        )
        output_path = os.path.join(output_dir, "complete.yml")
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(yaml_obj, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"Created single YAML file: {output_path}")
        return
    
    # Create YAML files for each verse
    for i, (verse_id, sanskrit, translation) in enumerate(verses, 1):
        yaml_obj = create_yaml_structure(verse_id, sanskrit, translation, collection, section)
        
        # Create filename
        safe_id = re.sub(r'[^\w\-_.]', '_', str(verse_id))
        filename = f"{safe_id}.yml"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(yaml_obj, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
        print(f"Created: {filename}")
    
    print(f"\nSuccessfully created {len(verses)} YAML files in {output_dir}")
    print(f"Collection: {collection}")
    print(f"Section: {section}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert Sanskrit text files to structured YAML format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument("input_path", help="Path to input text file")
    parser.add_argument("output_dir", help="Output directory for YAML files")
    parser.add_argument("--collection", default="Unknown Collection", 
                       help="Name of the collection (e.g., 'Bhagavad Gita')")
    parser.add_argument("--section", default="", 
                       help="Section name (e.g., 'Karma Yoga')")
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_path):
        print(f"Error: Input file '{args.input_path}' not found.")
        return 1
    
    try:
        process_text_file(args.input_path, args.output_dir, args.collection, args.section)
        return 0
    except Exception as e:
        print(f"Error processing file: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
