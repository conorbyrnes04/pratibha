#!/usr/bin/env python3
"""Download existing Tilopa audio files from Supabase Storage for analysis and cleanup.

This script downloads all Tilopa Mahāmudrā audio files from the Listen archive
so we can analyze them for wind noise and missing layers.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import listen_store  # noqa: E402


async def download_tilopa_audio():
    """Download all Tilopa audio files from the Listen archive."""
    output_dir = ROOT / ".cache" / "tilopa_audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the listen archive to see what's been baked
    archive_path = ROOT / "data" / "listen_archive.json"
    if archive_path.exists():
        with open(archive_path) as f:
            archive = json.load(f)
    else:
        archive = {}
    
    # List all 27 Tilopa verses
    tilopa_units = []
    for i in range(1, 28):
        unit_id = f"tilopa_mahamudra.tilopa_mahamudra_{i:03d}"
        tilopa_units.append(unit_id)
    
    downloaded = []
    missing = []
    
    print("Downloading Tilopa audio files...")
    for unit_id in tilopa_units:
        verse_num = int(unit_id.split("_")[-1])
        print(f"\nVerse {verse_num}: {unit_id}")
        
        # Check which layers exist in the archive
        layers = archive.get(unit_id, ["translation", "commentary", "practice"])
        
        for section in layers:
            # Try to download the audio file
            key = f"speech/{unit_id}/{section}.mp3"
            print(f"  Checking {section}...", end=" ")
            
            try:
                audio_data = await listen_store.get_object(key)
                if audio_data:
                    output_file = output_dir / f"tilopa_{verse_num:03d}_{section}.mp3"
                    output_file.write_bytes(audio_data)
                    downloaded.append((verse_num, section, output_file))
                    print(f"✓ Downloaded ({len(audio_data)} bytes)")
                else:
                    missing.append((verse_num, section))
                    print("✗ Not found in storage")
            except Exception as e:
                missing.append((verse_num, section))
                print(f"✗ Error: {e}")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Downloaded: {len(downloaded)} audio files")
    print(f"  Missing: {len(missing)} files")
    
    if downloaded:
        print(f"\nDownloaded files saved to: {output_dir}")
    
    if missing:
        print(f"\nMissing files:")
        for verse_num, section in missing:
            print(f"  Verse {verse_num}: {section}")
    
    return downloaded, missing


if __name__ == "__main__":
    asyncio.run(download_tilopa_audio())
