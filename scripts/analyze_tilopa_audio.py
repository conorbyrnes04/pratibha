#!/usr/bin/env python3
"""Analyze Tilopa audio files for wind noise and quality issues.

This script uses spectral analysis to detect wind noise and other audio issues
in the downloaded Tilopa MP3 files.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def analyze_audio_spectrum(audio_file: Path) -> Dict:
    """Analyze audio file for wind noise and quality metrics.
    
    Wind noise typically shows:
    - High energy in low frequencies (< 200 Hz)
    - Broadband noise across the spectrum
    - Irregular amplitude variations
    """
    try:
        # Use ffmpeg to extract audio data
        cmd = [
            "ffmpeg",
            "-i", str(audio_file),
            "-f", "f32le",
            "-ac", "1",  # mono
            "-ar", "22050",  # sample rate
            "-"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True
        )
        
        # Convert to numpy array
        audio_data = np.frombuffer(result.stdout, dtype=np.float32)
        
        if len(audio_data) == 0:
            return {"error": "No audio data"}
        
        # Calculate various metrics
        metrics = {}
        
        # 1. RMS (overall volume)
        rms = np.sqrt(np.mean(audio_data ** 2))
        metrics["rms"] = float(rms)
        
        # 2. Low frequency energy (potential wind noise indicator)
        # Use FFT to analyze frequency content
        fft = np.fft.rfft(audio_data)
        freqs = np.fft.rfftfreq(len(audio_data), 1/22050)
        power = np.abs(fft) ** 2
        
        # Low freq band (20-200 Hz) - wind noise range
        low_freq_mask = (freqs >= 20) & (freqs <= 200)
        low_freq_power = np.sum(power[low_freq_mask])
        
        # Mid freq band (200-3000 Hz) - speech range
        mid_freq_mask = (freqs >= 200) & (freqs <= 3000)
        mid_freq_power = np.sum(power[mid_freq_mask])
        
        # High freq band (3000+ Hz)
        high_freq_mask = freqs >= 3000
        high_freq_power = np.sum(power[high_freq_mask])
        
        total_power = low_freq_power + mid_freq_power + high_freq_power
        
        if total_power > 0:
            metrics["low_freq_ratio"] = float(low_freq_power / total_power)
            metrics["mid_freq_ratio"] = float(mid_freq_power / total_power)
            metrics["high_freq_ratio"] = float(high_freq_power / total_power)
        else:
            metrics["low_freq_ratio"] = 0.0
            metrics["mid_freq_ratio"] = 0.0
            metrics["high_freq_ratio"] = 0.0
        
        # 3. Detect if low frequency content is excessive (wind noise indicator)
        # Normal speech should have most energy in mid frequencies
        # Wind noise has high low-frequency content
        if metrics["low_freq_ratio"] > 0.4:  # > 40% low freq = likely wind
            metrics["wind_noise_detected"] = True
            metrics["wind_noise_severity"] = "high" if metrics["low_freq_ratio"] > 0.6 else "medium"
        elif metrics["low_freq_ratio"] > 0.25:
            metrics["wind_noise_detected"] = True
            metrics["wind_noise_severity"] = "low"
        else:
            metrics["wind_noise_detected"] = False
            metrics["wind_noise_severity"] = "none"
        
        # 4. Signal-to-noise ratio estimate
        # Use quiet parts to estimate noise floor
        quiet_threshold = rms * 0.3
        noise_samples = audio_data[np.abs(audio_data) < quiet_threshold]
        if len(noise_samples) > 0:
            noise_level = np.std(noise_samples)
            if noise_level > 0:
                snr = 20 * np.log10(rms / noise_level)
                metrics["snr_db"] = float(snr)
            else:
                metrics["snr_db"] = float('inf')
        else:
            metrics["snr_db"] = None
        
        # 5. Duration
        duration = len(audio_data) / 22050
        metrics["duration_seconds"] = float(duration)
        
        return metrics
        
    except subprocess.CalledProcessError as e:
        return {"error": f"ffmpeg error: {e}"}
    except Exception as e:
        return {"error": str(e)}


def analyze_all_tilopa_audio():
    """Analyze all downloaded Tilopa audio files."""
    cache_dir = ROOT / ".cache" / "tilopa_audio"
    
    if not cache_dir.exists():
        print("Error: No audio files found. Run download_tilopa_audio.py first.")
        return
    
    audio_files = sorted(cache_dir.glob("tilopa_*.mp3"))
    
    if not audio_files:
        print("Error: No audio files found in cache directory.")
        return
    
    print(f"Analyzing {len(audio_files)} audio files...\n")
    
    results = {}
    wind_noise_files = []
    
    for audio_file in audio_files:
        print(f"Analyzing: {audio_file.name}...", end=" ")
        
        metrics = analyze_audio_spectrum(audio_file)
        results[audio_file.name] = metrics
        
        if "error" in metrics:
            print(f"✗ {metrics['error']}")
        else:
            wind_detected = metrics.get("wind_noise_detected", False)
            severity = metrics.get("wind_noise_severity", "none")
            
            if wind_detected:
                print(f"⚠ WIND NOISE ({severity}) - Low freq: {metrics['low_freq_ratio']:.1%}")
                wind_noise_files.append((audio_file.name, severity, metrics))
            else:
                print(f"✓ Clean - Low freq: {metrics['low_freq_ratio']:.1%}")
    
    # Save results
    output_file = cache_dir / "analysis_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Analysis complete. Results saved to: {output_file}")
    
    if wind_noise_files:
        print(f"\n⚠ WIND NOISE DETECTED in {len(wind_noise_files)} files:")
        for filename, severity, metrics in wind_noise_files:
            parts = filename.replace(".mp3", "").split("_")
            verse_num = parts[1]
            section = parts[2]
            print(f"  Verse {verse_num} ({section}): {severity} severity")
            print(f"    Low freq: {metrics['low_freq_ratio']:.1%}, "
                  f"Mid freq: {metrics['mid_freq_ratio']:.1%}, "
                  f"SNR: {metrics.get('snr_db', 'N/A'):.1f} dB")
    else:
        print("\n✓ No wind noise detected in any files!")
    
    return results, wind_noise_files


if __name__ == "__main__":
    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is required but not found. Please install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        exit(1)
    
    try:
        import numpy
    except ImportError:
        print("Error: numpy is required. Install with: pip install numpy")
        exit(1)
    
    analyze_all_tilopa_audio()
