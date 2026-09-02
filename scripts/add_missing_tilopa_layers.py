#!/usr/bin/env python3
"""Add missing commentary and practice layers to Tilopa audio files.

This script identifies which Tilopa verses are missing commentary or practice
audio layers, generates them using the existing TTS system, and prepends them
to the translation audio (or creates standalone files).
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data_loader import get_all_verses  # noqa: E402
from app.tts import (  # noqa: E402
    SPEAKABLE_SECTIONS,
    build_script,
    resolve_voice,
    synthesize,
    synthesize_cue,
    voice_room_for,
)


def get_tilopa_verse_content(unit_id: str) -> Dict[str, str]:
    """Load content for a specific Tilopa verse."""
    verses = get_all_verses()
    
    for verse in verses:
        if verse.get("unit_id") == unit_id:
            content = {}
            
            # Extract content from pratibha_layers
            layers = verse.get("pratibha_layers", [])
            for layer in layers:
                kind = layer.get("kind", "")
                body = layer.get("body", "")
                
                if kind == "translation":
                    content["translation"] = body
                elif kind == "commentary":
                    content["commentary"] = body
                elif kind == "practice":
                    content["practice"] = body
            
            # Fallback to top-level fields
            if "translation" not in content and "translation" in verse:
                content["translation"] = verse["translation"]
            if "commentary" not in content and "commentary" in verse:
                content["commentary"] = verse["commentary"]
            if "practice" not in content and ("practice" in verse or "abhyasa" in verse):
                content["practice"] = verse.get("practice") or verse.get("abhyasa", "")
            
            return content
    
    return {}


async def generate_layer_audio(
    unit_id: str,
    section: str,
    text: str,
    work_id: str = "tilopa_mahamudra"
) -> bytes | None:
    """Generate audio for a specific layer using ElevenLabs TTS."""
    try:
        # Get voice configuration for Tilopa (Indic room)
        voice_room = voice_room_for(work_id)
        voice_id = resolve_voice(voice_room)
        
        # Clean and prepare text
        script = build_script(text, section)
        
        if not script.strip():
            print(f"    Warning: Empty script for {section}")
            return None
        
        print(f"    Generating {section} audio ({len(script)} chars)...")
        
        # Generate audio
        audio_data = await synthesize(voice_id, script, "indic")
        
        if audio_data and len(audio_data) > 0:
            print(f"    ✓ Generated {len(audio_data)} bytes")
            return audio_data
        else:
            print(f"    ✗ Generation failed (empty result)")
            return None
            
    except Exception as e:
        print(f"    ✗ Error generating audio: {e}")
        return None


async def generate_cue_audio(work_id: str = "tilopa_mahamudra") -> Tuple[bytes | None, bytes | None]:
    """Generate open and close cue audio for Tilopa verses."""
    try:
        voice_room = voice_room_for(work_id)
        
        print("  Generating tradition cue (open)...")
        open_cue = await synthesize_cue(voice_room, "open")
        
        print("  Generating tradition cue (close)...")
        close_cue = await synthesize_cue(voice_room, "close")
        
        return open_cue, close_cue
        
    except Exception as e:
        print(f"  ✗ Error generating cues: {e}")
        return None, None


def concatenate_audio_files(
    output_file: Path,
    *input_files: Path,
    include_silence: bool = True
) -> bool:
    """Concatenate multiple audio files into one using ffmpeg.
    
    Args:
        output_file: Path to output file
        input_files: Paths to input files (in order)
        include_silence: Whether to add brief silence between segments
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Filter out None/non-existent files
        valid_files = [f for f in input_files if f and f.exists()]
        
        if not valid_files:
            print(f"    ✗ No valid input files for concatenation")
            return False
        
        if len(valid_files) == 1:
            # Just copy the file
            import shutil
            shutil.copy2(valid_files[0], output_file)
            return True
        
        # Create a temp file list for ffmpeg concat
        file_list = output_file.parent / f"concat_{output_file.stem}.txt"
        
        with open(file_list, "w") as f:
            for input_file in valid_files:
                f.write(f"file '{input_file.absolute()}'\n")
                if include_silence and input_file != valid_files[-1]:
                    # Add 0.5 second silence between segments
                    f.write(f"file 'silence.mp3'\n")
        
        # Generate silence file if needed
        if include_silence:
            silence_file = output_file.parent / "silence.mp3"
            if not silence_file.exists():
                subprocess.run([
                    "ffmpeg",
                    "-f", "lavfi",
                    "-i", "anullsrc=r=44100:cl=mono",
                    "-t", "0.5",
                    "-c:a", "libmp3lame",
                    "-q:a", "2",
                    str(silence_file)
                ], capture_output=True, check=True)
        
        # Concatenate using ffmpeg
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(file_list),
            "-c", "copy",
            "-y",
            str(output_file)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        # Clean up
        file_list.unlink()
        
        return True
        
    except Exception as e:
        print(f"    ✗ Error concatenating audio: {e}")
        return False


async def add_missing_layers():
    """Add missing commentary and practice layers to Tilopa verses."""
    cache_dir = ROOT / ".cache" / "tilopa_audio"
    output_dir = cache_dir / "complete"
    output_dir.mkdir(exist_ok=True)
    
    # Create temp directory for generated layers
    temp_dir = cache_dir / "temp_layers"
    temp_dir.mkdir(exist_ok=True)
    
    print("Checking for missing layers in Tilopa verses...\n")
    
    # Check which files exist
    existing_files = set(f.name for f in cache_dir.glob("tilopa_*.mp3"))
    
    # Generate cues once for all verses
    print("Generating tradition cues...")
    open_cue_data, close_cue_data = await generate_cue_audio()
    
    if open_cue_data:
        open_cue_file = temp_dir / "cue_open.mp3"
        open_cue_file.write_bytes(open_cue_data)
    else:
        open_cue_file = None
    
    if close_cue_data:
        close_cue_file = temp_dir / "cue_close.mp3"
        close_cue_file.write_bytes(close_cue_data)
    else:
        close_cue_file = None
    
    # Process each verse
    for verse_num in range(1, 28):
        unit_id = f"tilopa_mahamudra.tilopa_mahamudra_{verse_num:03d}"
        
        print(f"\n{'='*60}")
        print(f"Processing Verse {verse_num}: {unit_id}")
        
        # Check which layers exist
        translation_file = f"tilopa_{verse_num:03d}_translation.mp3"
        commentary_file = f"tilopa_{verse_num:03d}_commentary.mp3"
        practice_file = f"tilopa_{verse_num:03d}_practice.mp3"
        
        has_translation = translation_file in existing_files
        has_commentary = commentary_file in existing_files
        has_practice = practice_file in existing_files
        
        print(f"  Existing layers:")
        print(f"    Translation: {'✓' if has_translation else '✗'}")
        print(f"    Commentary: {'✓' if has_commentary else '✗'}")
        print(f"    Practice: {'✓' if has_practice else '✗'}")
        
        # Load verse content
        content = get_tilopa_verse_content(unit_id)
        
        if not content:
            print(f"  ✗ Could not load content for {unit_id}")
            continue
        
        # Generate missing layers
        generated_files = []
        
        if not has_commentary and "commentary" in content and content["commentary"]:
            print(f"\n  Generating missing COMMENTARY layer...")
            commentary_audio = await generate_layer_audio(
                unit_id, "commentary", content["commentary"]
            )
            if commentary_audio:
                commentary_path = temp_dir / f"generated_{commentary_file}"
                commentary_path.write_bytes(commentary_audio)
                generated_files.append(("commentary", commentary_path))
        
        if not has_practice and "practice" in content and content["practice"]:
            print(f"\n  Generating missing PRACTICE layer...")
            practice_audio = await generate_layer_audio(
                unit_id, "practice", content["practice"]
            )
            if practice_audio:
                practice_path = temp_dir / f"generated_{practice_file}"
                practice_path.write_bytes(practice_audio)
                generated_files.append(("practice", practice_path))
        
        # Create complete audio file with all layers
        print(f"\n  Creating complete audio file...")
        
        audio_segments = []
        
        # Add opening cue
        if open_cue_file:
            audio_segments.append(open_cue_file)
        
        # Add translation
        if has_translation:
            audio_segments.append(cache_dir / translation_file)
        
        # Add commentary
        if has_commentary:
            audio_segments.append(cache_dir / commentary_file)
        else:
            for layer, path in generated_files:
                if layer == "commentary":
                    audio_segments.append(path)
        
        # Add practice
        if has_practice:
            audio_segments.append(cache_dir / practice_file)
        else:
            for layer, path in generated_files:
                if layer == "practice":
                    audio_segments.append(path)
        
        # Add closing cue
        if close_cue_file:
            audio_segments.append(close_cue_file)
        
        # Concatenate all segments
        complete_file = output_dir / f"tilopa_{verse_num:03d}_complete.mp3"
        if concatenate_audio_files(complete_file, *audio_segments):
            print(f"  ✓ Created complete audio: {complete_file.name}")
        else:
            print(f"  ✗ Failed to create complete audio")
        
        # Also save individual generated layers
        for layer, path in generated_files:
            layer_file = output_dir / f"tilopa_{verse_num:03d}_{layer}.mp3"
            import shutil
            shutil.copy2(path, layer_file)
            print(f"  ✓ Saved {layer} layer: {layer_file.name}")
    
    print(f"\n{'='*60}")
    print(f"Complete! Files saved to: {output_dir}")


if __name__ == "__main__":
    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is required but not found. Please install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        exit(1)
    
    asyncio.run(add_missing_layers())
