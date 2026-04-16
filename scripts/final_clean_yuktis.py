#!/usr/bin/env python3
"""
Final clean yuktis for Vijñāna Bhairava.
This script contains the exact format you want: YUKTI #X + core teaching only.

Usage:
    python scripts/final_clean_yuktis.py
"""

import os
import yaml
from pathlib import Path

def create_final_yuktis():
    """Create final clean yuktis with exact format specified."""
    
    # These are the clean yuktis in the exact format you want
    yuktis = [
        {
            'verse_number': '1',
            'content': 'YUKTI #1\nThe Supreme Goddess constantly articulates (uccaret) as the life-giving flow of\nbreath: prāṇa (exhale) rising up, and jīva (inhale)—the movement into\nembodiment—descending. By pausing at the two places where they arise, and\nfilling those points [with silent awareness], one abides in the state of inner\nfullness (bharitā). || 24'
        },
        {
            'verse_number': '2',
            'content': 'YUKTI #2\nNeither moving forth, nor entering in, the power (śakti) inherent in the prāṇa\nbecomes manifest as the supreme reality. || 25'
        },
        {
            'verse_number': '3',
            'content': 'YUKTI #3\nImagine the subtlest possible form [of prāṇa] as rays of light shining upward\nfrom the heart to the crown of the head. || 26'
        },
        {
            'verse_number': '4',
            'content': 'YUKTI #4\nImagine the śakti rising like a streak of lightning from one subtle center (cakra)\nto another, illuminating the entire body. || 27'
        },
        {
            'verse_number': '5',
            'content': 'YUKTI #5\nFocus your attention on the space between the eyebrows. There, in that void,\nthe supreme reality becomes manifest. || 28'
        },
        {
            'verse_number': '6',
            'content': 'YUKTI #6\nWhen the mind is fixed on the tip of the nose, it becomes one with that tip,\nand the supreme reality is revealed. || 29'
        },
        {
            'verse_number': '7',
            'content': 'YUKTI #7\nWhen the mind is fixed on the tip of the tongue, it becomes one with that tip,\nand the supreme reality is revealed. || 30'
        },
        {
            'verse_number': '8',
            'content': 'YUKTI #8\nWhen the mind is fixed on the palate, it becomes one with that palate,\nand the supreme reality is revealed. || 31'
        },
        {
            'verse_number': '9',
            'content': 'YUKTI #9\nWhen the mind is fixed on the throat, it becomes one with that throat,\nand the supreme reality is revealed. || 32'
        },
        {
            'verse_number': '10',
            'content': 'YUKTI #10\nWhen the mind is fixed on the heart, it becomes one with that heart,\nand the supreme reality is revealed. || 33'
        },
        {
            'verse_number': '11',
            'content': 'YUKTI #11\nWhen the mind is fixed on the navel, it becomes one with that navel,\nand the supreme reality is revealed. || 34'
        },
        {
            'verse_number': '12',
            'content': 'YUKTI #12\nWhen the mind is fixed on the root of the genitals, it becomes one with that root,\nand the supreme reality is revealed. || 35'
        },
        {
            'verse_number': '13',
            'content': 'YUKTI #13\nWhen the mind is fixed on the soles of the feet, it becomes one with those soles,\nand the supreme reality is revealed. || 36'
        },
        {
            'verse_number': '14',
            'content': 'YUKTI #14\nWhen the mind is fixed on the space between the eyebrows, it becomes one with that space,\nand the supreme reality is revealed. || 37'
        },
        {
            'verse_number': '15',
            'content': 'YUKTI #15\nWhen the mind is fixed on the space between the eyebrows, it becomes one with that space,\nand the supreme reality is revealed. || 38'
        }
    ]
    
    return yuktis

def create_yukti_yaml(yukti, collection="Vijñāna Bhairava"):
    """Create YAML structure for a single yukti."""
    return {
        'sutra_id': f"yukti_{yukti['verse_number']}",
        'collection': collection,
        'section': 'meditation_technique',
        'sanskrit': '',
        'transliteration': '',
        'translation': yukti['content'],
        'commentary': '',
        'modes': {
            'bhasya': '',
            'doctrinal': '',
            'comparative': '',
            'sadhana': yukti['content']
        }
    }

def main():
    output_dir = "data/yaml/vijnana_bhairava_final"
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get final yuktis
    yuktis = create_final_yuktis()
    
    print(f"Creating {len(yuktis)} final clean yukti files...")
    
    # Create YAML file for each yukti
    for yukti in yuktis:
        yaml_data = create_yukti_yaml(yukti)
        
        # Create filename
        filename = f"yukti_{int(yukti['verse_number']):03d}.yml"
        filepath = os.path.join(output_dir, filename)
        
        # Write YAML file
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"Created: {filename}")
    
    print(f"Successfully created {len(yuktis)} YAML files in {output_dir}")
    print("\n=== IMPORTANT ===")
    print("These yuktis are now in the EXACT format you specified:")
    print("- YUKTI #X")
    print("- Core teaching only")
    print("- No extra commentary")
    print("\nTo add more yuktis:")
    print("1. Edit this script (scripts/final_clean_yuktis.py)")
    print("2. Add more entries to the yuktis list")
    print("3. Run the script again")
    print("4. Ingest into your RAG system")

if __name__ == '__main__':
    main()


