#!/usr/bin/env python3
"""Remove wind noise from Tilopa audio files without rebaking.

This script uses audio processing (highpass filter, noise reduction) to clean
wind noise from existing MP3 files while preserving voice quality.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent


def remove_wind_noise(input_file: Path, output_file: Path, severity: str = "medium") -> bool:
    """Remove wind noise from audio file using ffmpeg filters.
    
    Strategy:
    1. High-pass filter to remove low frequencies (wind noise is typically < 200 Hz)
    2. Noise reduction using afftdn filter
    3. Normalize volume
    4. Enhance voice frequencies
    
    Args:
        input_file: Path to input MP3 file
        output_file: Path to output cleaned MP3 file
        severity: Wind noise severity (low, medium, high)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Set filter parameters based on severity
        if severity == "high":
            highpass_freq = 150  # More aggressive
            nr_amount = 25  # Stronger noise reduction
        elif severity == "medium":
            highpass_freq = 120
            nr_amount = 20
        else:  # low
            highpass_freq = 100
            nr_amount = 15
        
        # Build complex ffmpeg filter chain:
        # 1. highpass: Remove low frequency wind noise
        # 2. afftdn: FFT-based denoising to remove residual noise
        # 3. equalizer: Boost voice frequencies (200-3000 Hz)
        # 4. compand: Dynamic range compression to even out volume
        # 5. loudnorm: Normalize loudness to standard levels
        
        filter_complex = (
            f"highpass=f={highpass_freq}:poles=2,"  # Remove low freq wind
            f"afftdn=nr={nr_amount}:nf=-20:tn=1,"  # Denoise
            "equalizer=f=300:width_type=h:width=500:g=3,"  # Boost low-mid voice
            "equalizer=f=1500:width_type=h:width=1000:g=2,"  # Boost mid voice
            "compand=attacks=0.3:decays=0.8:points=-80/-80|-45/-30|-25/-15|-10/-10|0/-5,"  # Compress
            "loudnorm=I=-16:LRA=11:TP=-1.5"  # Normalize loudness
        )
        
        cmd = [
            "ffmpeg",
            "-i", str(input_file),
            "-af", filter_complex,
            "-c:a", "libmp3lame",  # MP3 codec
            "-q:a", "2",  # High quality (VBR quality 2)
            "-y",  # Overwrite output
            str(output_file)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            text=True
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"    Error: {e}")
        if e.stderr:
            print(f"    ffmpeg stderr: {e.stderr[:200]}")
        return False
    except Exception as e:
        print(f"    Error: {e}")
        return False


def clean_all_tilopa_audio():
    """Clean all Tilopa audio files that have wind noise."""
    cache_dir = ROOT / ".cache" / "tilopa_audio"
    analysis_file = cache_dir / "analysis_results.json"
    
    if not analysis_file.exists():
        print("Error: No analysis results found. Run analyze_tilopa_audio.py first.")
        return
    
    # Load analysis results
    with open(analysis_file) as f:
        analysis = json.load(f)
    
    # Create output directory for cleaned files
    output_dir = cache_dir / "cleaned"
    output_dir.mkdir(exist_ok=True)
    
    # Find files with wind noise
    wind_noise_files = []
    for filename, metrics in analysis.items():
        if metrics.get("wind_noise_detected", False):
            severity = metrics.get("wind_noise_severity", "medium")
            wind_noise_files.append((filename, severity))
    
    if not wind_noise_files:
        print("No files with wind noise found. Nothing to clean!")
        return
    
    print(f"Cleaning {len(wind_noise_files)} files with wind noise...\n")
    
    success_count = 0
    failed_count = 0
    
    for filename, severity in wind_noise_files:
        input_file = cache_dir / filename
        output_file = output_dir / filename
        
        parts = filename.replace(".mp3", "").split("_")
        verse_num = parts[1]
        section = parts[2]
        
        print(f"Cleaning Verse {verse_num} ({section}) - {severity} severity...")
        
        if remove_wind_noise(input_file, output_file, severity):
            print(f"  ✓ Cleaned and saved to: {output_file.name}")
            success_count += 1
        else:
            print(f"  ✗ Failed to clean")
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"Cleaning complete:")
    print(f"  Success: {success_count} files")
    print(f"  Failed: {failed_count} files")
    print(f"\nCleaned files saved to: {output_dir}")
    
    # Also copy clean files (no wind noise) to the output directory
    clean_files = []
    for filename, metrics in analysis.items():
        if not metrics.get("wind_noise_detected", False) and "error" not in metrics:
            clean_files.append(filename)
    
    if clean_files:
        print(f"\nCopying {len(clean_files)} clean files (no wind noise)...")
        for filename in clean_files:
            input_file = cache_dir / filename
            output_file = output_dir / filename
            if input_file.exists():
                import shutil
                shutil.copy2(input_file, output_file)
        print(f"  ✓ Copied {len(clean_files)} files")


if __name__ == "__main__":
    # Check if ffmpeg is available with required filters
    try:
        result = subprocess.run(
            ["ffmpeg", "-filters"],
            capture_output=True,
            check=True,
            text=True
        )
        
        required_filters = ["highpass", "afftdn", "equalizer", "compand", "loudnorm"]
        missing_filters = []
        
        for filt in required_filters:
            if filt not in result.stdout:
                missing_filters.append(filt)
        
        if missing_filters:
            print(f"Error: ffmpeg is missing required filters: {', '.join(missing_filters)}")
            print("Please install a full version of ffmpeg with all filters enabled.")
            exit(1)
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is required but not found. Please install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        exit(1)
    
    clean_all_tilopa_audio()
