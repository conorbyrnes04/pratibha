#!/usr/bin/env python3
"""Upload cleaned and completed Tilopa audio files back to Supabase Storage.

This script uploads the processed audio files (cleaned of wind noise, with complete
layers) back to the Listen archive in Supabase Storage and updates the listen_archive.json.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import listen_store  # noqa: E402


async def upload_tilopa_audio():
    """Upload all processed Tilopa audio files to Supabase Storage."""
    
    # Check which directories exist
    cache_dir = ROOT / ".cache" / "tilopa_audio"
    cleaned_dir = cache_dir / "cleaned"
    complete_dir = cache_dir / "complete"
    
    if not cache_dir.exists():
        print("Error: Cache directory not found. Process audio files first.")
        return
    
    print("Uploading processed Tilopa audio files to Supabase Storage...\n")
    
    # Track what we're uploading
    upload_tasks = []
    
    # 1. Upload individual cleaned layers (for verse pages)
    if cleaned_dir.exists():
        print("Uploading cleaned individual layers...")
        for audio_file in sorted(cleaned_dir.glob("tilopa_*.mp3")):
            if "_complete" in audio_file.name:
                continue  # Skip complete files for now
            
            # Parse filename: tilopa_001_translation.mp3
            parts = audio_file.stem.split("_")
            if len(parts) >= 3:
                verse_num = int(parts[1])
                section = parts[2]
                
                unit_id = f"tilopa_mahamudra.tilopa_mahamudra_{verse_num:03d}"
                storage_key = f"speech/{unit_id}/{section}.mp3"
                
                upload_tasks.append((audio_file, storage_key, verse_num, section, "layer"))
    
    # 2. Upload generated missing layers from complete directory
    if complete_dir.exists():
        print("Uploading generated missing layers...")
        for audio_file in sorted(complete_dir.glob("tilopa_*_commentary.mp3")):
            parts = audio_file.stem.split("_")
            if len(parts) >= 3:
                verse_num = int(parts[1])
                section = parts[2]
                
                unit_id = f"tilopa_mahamudra.tilopa_mahamudra_{verse_num:03d}"
                storage_key = f"speech/{unit_id}/{section}.mp3"
                
                # Check if we didn't already add this from cleaned_dir
                if not any(t[1] == storage_key for t in upload_tasks):
                    upload_tasks.append((audio_file, storage_key, verse_num, section, "layer"))
        
        for audio_file in sorted(complete_dir.glob("tilopa_*_practice.mp3")):
            parts = audio_file.stem.split("_")
            if len(parts) >= 3:
                verse_num = int(parts[1])
                section = parts[2]
                
                unit_id = f"tilopa_mahamudra.tilopa_mahamudra_{verse_num:03d}"
                storage_key = f"speech/{unit_id}/{section}.mp3"
                
                if not any(t[1] == storage_key for t in upload_tasks):
                    upload_tasks.append((audio_file, storage_key, verse_num, section, "layer"))
    
    # Execute uploads
    uploaded = []
    failed = []
    
    for audio_file, storage_key, verse_num, section, upload_type in upload_tasks:
        print(f"\nVerse {verse_num} ({section}): {audio_file.name}")
        print(f"  → {storage_key}")
        
        try:
            audio_data = audio_file.read_bytes()
            success = await listen_store.put_object(storage_key, audio_data, "audio/mpeg")
            
            if success:
                print(f"  ✓ Uploaded ({len(audio_data)} bytes)")
                uploaded.append((verse_num, section))
            else:
                print(f"  ✗ Upload failed")
                failed.append((verse_num, section))
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed.append((verse_num, section))
    
    # Update listen_archive.json
    print(f"\n{'='*60}")
    print("Updating listen_archive.json...")
    
    archive_path = ROOT / "data" / "listen_archive.json"
    
    if archive_path.exists():
        with open(archive_path) as f:
            archive = json.load(f)
    else:
        archive = {}
    
    # Add Tilopa entries
    for verse_num in range(1, 28):
        unit_id = f"tilopa_mahamudra.tilopa_mahamudra_{verse_num:03d}"
        
        # Check which layers were uploaded for this verse
        layers = []
        for v, section in uploaded:
            if v == verse_num:
                layers.append(section)
        
        if layers:
            # Remove duplicates and sort
            layers = sorted(set(layers))
            archive[unit_id] = layers
            print(f"  {unit_id}: {layers}")
    
    # Save updated archive
    with open(archive_path, "w") as f:
        json.dump(archive, f, indent=2, sort_keys=True)
    
    print(f"\n✓ Updated {archive_path}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Upload Summary:")
    print(f"  Uploaded: {len(uploaded)} layer files")
    print(f"  Failed: {len(failed)} files")
    print(f"  Updated archive with {len([v for v in range(1, 28) if any(uv[0] == v for uv in uploaded)])} verses")
    
    if failed:
        print(f"\nFailed uploads:")
        for verse_num, section in failed:
            print(f"  Verse {verse_num}: {section}")
    
    # 3. Optionally upload complete files (full verse with all layers)
    if complete_dir.exists():
        complete_files = list(complete_dir.glob("tilopa_*_complete.mp3"))
        if complete_files:
            print(f"\n{'='*60}")
            print(f"Found {len(complete_files)} complete verse files.")
            print("These contain all layers (translation + commentary + practice + cues).")
            print("They can be uploaded as standalone files for full playback.")
            print("\nTo upload complete files, run with --upload-complete flag.")


if __name__ == "__main__":
    import sys
    
    if not listen_store.configured():
        print("Error: Supabase Storage is not configured.")
        print("Please set the following environment variables:")
        print("  SUPABASE_URL")
        print("  SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_SERVICE_KEY)")
        print("  LISTEN_BUCKET (optional, defaults to 'listen')")
        exit(1)
    
    asyncio.run(upload_tilopa_audio())
