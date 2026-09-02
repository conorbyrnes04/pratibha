#!/usr/bin/env python3
"""Master script to orchestrate the complete Tilopa audio cleanup process.

This script runs all steps in sequence:
1. Download existing audio from Supabase
2. Analyze for wind noise
3. Clean wind noise
4. Generate missing layers
5. Upload cleaned audio back to Supabase
"""
from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


async def run_step(step_name: str, script_path: Path, description: str) -> bool:
    """Run a processing step and report results."""
    print(f"\n{'='*60}")
    print(f"STEP: {step_name}")
    print(f"{description}")
    print(f"{'='*60}\n")
    
    try:
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=ROOT,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ {step_name} completed successfully")
            return True
        else:
            print(f"\n✗ {step_name} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n✗ {step_name} failed with error: {e}")
        return False


async def main():
    """Run the complete Tilopa audio cleanup process."""
    print("="*60)
    print("TILOPA AUDIO CLEANUP PIPELINE")
    print("="*60)
    print("\nThis script will:")
    print("  1. Download existing Tilopa audio from Supabase Storage")
    print("  2. Analyze audio files for wind noise")
    print("  3. Clean wind noise using audio processing")
    print("  4. Generate missing commentary and practice layers")
    print("  5. Upload cleaned and complete audio back to Supabase")
    print()
    
    response = input("Continue? [y/N]: ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    scripts_dir = ROOT / "scripts"
    steps = [
        (
            "Download Audio",
            scripts_dir / "download_tilopa_audio.py",
            "Download existing Tilopa audio files from Supabase Storage"
        ),
        (
            "Analyze Audio",
            scripts_dir / "analyze_tilopa_audio.py",
            "Analyze audio files for wind noise and quality issues"
        ),
        (
            "Clean Wind Noise",
            scripts_dir / "clean_tilopa_audio.py",
            "Remove wind noise using highpass filter and denoising"
        ),
        (
            "Add Missing Layers",
            scripts_dir / "add_missing_tilopa_layers.py",
            "Generate and add missing commentary and practice layers"
        ),
        (
            "Upload to Supabase",
            scripts_dir / "upload_tilopa_audio.py",
            "Upload cleaned and completed audio back to Supabase Storage"
        ),
    ]
    
    results = []
    
    for step_name, script_path, description in steps:
        if not script_path.exists():
            print(f"\n✗ Error: Script not found: {script_path}")
            results.append((step_name, False))
            break
        
        success = await run_step(step_name, script_path, description)
        results.append((step_name, success))
        
        if not success:
            print(f"\nPipeline stopped at: {step_name}")
            print("Fix the error and re-run to continue.")
            break
    
    # Final summary
    print(f"\n{'='*60}")
    print("PIPELINE SUMMARY")
    print(f"{'='*60}")
    
    for step_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {step_name}")
    
    all_success = all(success for _, success in results)
    
    if all_success:
        print(f"\n{'='*60}")
        print("✓ PIPELINE COMPLETE!")
        print(f"{'='*60}")
        print("\nAll Tilopa audio files have been processed:")
        print("  • Wind noise removed")
        print("  • Voice quality enhanced")
        print("  • Missing layers generated")
        print("  • Uploaded to Supabase Storage")
        print("  • listen_archive.json updated")
        print("\nThe Listen feature will now serve the cleaned audio.")
    else:
        print(f"\n{'='*60}")
        print("✗ PIPELINE INCOMPLETE")
        print(f"{'='*60}")
        print("\nSome steps failed. Please review the errors above.")


if __name__ == "__main__":
    # Check prerequisites
    print("Checking prerequisites...\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required")
        exit(1)
    print("✓ Python version OK")
    
    # Check ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✓ ffmpeg installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ffmpeg not found")
        print("  Install with: sudo apt-get install ffmpeg (Ubuntu/Debian)")
        print("           or: brew install ffmpeg (macOS)")
        exit(1)
    
    # Check numpy
    try:
        import numpy
        print("✓ numpy installed")
    except ImportError:
        print("✗ numpy not found")
        print("  Install with: pip install numpy")
        exit(1)
    
    # Check Supabase configuration
    from app import listen_store
    if listen_store.configured():
        print("✓ Supabase Storage configured")
    else:
        print("⚠ Supabase Storage not configured")
        print("  Some steps may fail. Set environment variables:")
        print("    SUPABASE_URL")
        print("    SUPABASE_SERVICE_ROLE_KEY")
    
    print()
    
    asyncio.run(main())
