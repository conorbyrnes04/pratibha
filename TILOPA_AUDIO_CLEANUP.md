# Tilopa Audio Cleanup Process

This document describes the process and scripts for cleaning up the Tilopa Mahāmudrā audio files, removing wind noise, and adding missing commentary and practice layers.

## Problem Statement

The Tilopa Gaṅgā-mahāmudrā collection (27 verses) has text-to-speech audio files with the following issues:

1. **Wind noise**: Some audio files have background wind-like noise
2. **Missing layers**: Some verses are missing commentary or practice audio layers
3. **Quality**: Voice clarity could be enhanced

## Solution Overview

We've created a pipeline of scripts that:

1. **Download** existing audio from Supabase Storage
2. **Analyze** audio files to detect wind noise using spectral analysis
3. **Clean** wind noise using ffmpeg audio filters without regenerating TTS
4. **Generate** missing commentary and practice layers using ElevenLabs TTS
5. **Upload** cleaned and complete audio back to Supabase

## Scripts

### 1. `download_tilopa_audio.py`

Downloads all Tilopa audio files from Supabase Storage.

**Location**: `speech/{unit_id}/{section}.mp3`

**Sections**: translation, commentary, practice

**Output**: `.cache/tilopa_audio/tilopa_{verse_num}_{section}.mp3`

**Usage**:
```bash
python scripts/download_tilopa_audio.py
```

### 2. `analyze_tilopa_audio.py`

Analyzes audio files for wind noise using spectral analysis.

**Detection Method**:
- Wind noise typically has high energy in low frequencies (< 200 Hz)
- Analyzes frequency distribution using FFT
- Calculates low/mid/high frequency ratios
- Estimates signal-to-noise ratio

**Wind Noise Criteria**:
- Low severity: 25-40% low frequency content
- Medium severity: 40-60% low frequency content
- High severity: >60% low frequency content

**Output**: `.cache/tilopa_audio/analysis_results.json`

**Usage**:
```bash
python scripts/analyze_tilopa_audio.py
```

**Prerequisites**: ffmpeg, numpy

### 3. `clean_tilopa_audio.py`

Removes wind noise from audio files using ffmpeg filters.

**Processing Chain**:
1. **Highpass filter**: Remove low frequencies (wind noise < 150 Hz)
2. **FFT denoising**: Remove residual broadband noise
3. **Equalizer**: Boost voice frequencies (200-3000 Hz)
4. **Compressor**: Even out volume dynamics
5. **Loudness normalization**: Standardize output levels

**Severity-based filtering**:
- High: Aggressive filtering (150 Hz highpass, 25 dB noise reduction)
- Medium: Standard filtering (120 Hz highpass, 20 dB noise reduction)
- Low: Gentle filtering (100 Hz highpass, 15 dB noise reduction)

**Output**: `.cache/tilopa_audio/cleaned/tilopa_{verse_num}_{section}.mp3`

**Usage**:
```bash
python scripts/clean_tilopa_audio.py
```

**Prerequisites**: ffmpeg with filters: highpass, afftdn, equalizer, compand, loudnorm

### 4. `add_missing_tilopa_layers.py`

Generates missing commentary and practice layers and creates complete audio files.

**Process**:
1. Load verse content from canonical YAML files
2. Generate tradition cues (Indic room: singing bowl sound)
3. Generate missing layer audio using ElevenLabs TTS
4. Concatenate: cue + translation + commentary + practice + cue
5. Save individual layers and complete files

**Voice Configuration**:
- Tilopa → Indic voice room
- Voice: Anagh (Indian English)
- Model: eleven_multilingual_v2

**Output**: 
- `.cache/tilopa_audio/complete/tilopa_{verse_num}_{layer}.mp3` (individual)
- `.cache/tilopa_audio/complete/tilopa_{verse_num}_complete.mp3` (full)

**Usage**:
```bash
python scripts/add_missing_tilopa_layers.py
```

**Prerequisites**: ffmpeg, ElevenLabs API key (ELEVEN_API_KEY)

### 5. `upload_tilopa_audio.py`

Uploads cleaned and completed audio files back to Supabase Storage.

**Process**:
1. Upload individual cleaned layer files to `speech/{unit_id}/{section}.mp3`
2. Update `data/listen_archive.json` with available layers per verse
3. Report upload success/failure

**Output**: Updates Supabase Storage and listen_archive.json

**Usage**:
```bash
python scripts/upload_tilopa_audio.py
```

**Prerequisites**: Supabase configuration (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

### 6. `process_tilopa_audio_pipeline.py` (Master Script)

Orchestrates the entire pipeline in sequence.

**Usage**:
```bash
python scripts/process_tilopa_audio_pipeline.py
```

This runs all 5 steps automatically with progress reporting.

## Prerequisites

### System Requirements

- **Python 3.8+**
- **ffmpeg** with full filter support:
  ```bash
  # Ubuntu/Debian
  sudo apt-get update
  sudo apt-get install ffmpeg
  
  # macOS
  brew install ffmpeg
  ```

### Python Dependencies

Install required packages:
```bash
pip install numpy
```

The project dependencies (httpx, pydantic, etc.) are already in requirements.txt.

### Environment Configuration

Create a `.env` file or export environment variables:

```bash
# Required for generating missing layers
ELEVEN_API_KEY=your_elevenlabs_api_key

# Required for download/upload
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
LISTEN_BUCKET=listen  # optional, defaults to "listen"
```

## Usage

### Quick Start (Recommended)

Run the complete pipeline:

```bash
python scripts/process_tilopa_audio_pipeline.py
```

This will:
1. Check prerequisites
2. Run all 5 steps in sequence
3. Provide progress updates
4. Generate a summary report

### Manual Step-by-Step

If you prefer to run steps individually:

```bash
# 1. Download existing audio
python scripts/download_tilopa_audio.py

# 2. Analyze for wind noise
python scripts/analyze_tilopa_audio.py

# 3. Clean wind noise
python scripts/clean_tilopa_audio.py

# 4. Add missing layers
python scripts/add_missing_tilopa_layers.py

# 5. Upload to Supabase
python scripts/upload_tilopa_audio.py
```

## Output Structure

```
.cache/tilopa_audio/
├── tilopa_001_translation.mp3      # Downloaded originals
├── tilopa_001_commentary.mp3
├── tilopa_001_practice.mp3
├── ...
├── analysis_results.json           # Spectral analysis results
├── cleaned/                        # Cleaned audio (wind noise removed)
│   ├── tilopa_001_translation.mp3
│   ├── tilopa_001_commentary.mp3
│   └── ...
├── complete/                       # Complete files with all layers
│   ├── tilopa_001_commentary.mp3   # Generated missing layers
│   ├── tilopa_001_practice.mp3
│   ├── tilopa_001_complete.mp3     # Full verse (all layers + cues)
│   └── ...
└── temp_layers/                    # Temporary files (cues, etc.)
```

## Technical Details

### Wind Noise Detection Algorithm

1. **FFT Analysis**: Convert audio to frequency domain
2. **Frequency Bands**:
   - Low (20-200 Hz): Wind noise
   - Mid (200-3000 Hz): Speech
   - High (3000+ Hz): Sibilants
3. **Ratios**: Calculate energy distribution across bands
4. **Threshold**: Flag if low freq > 25% of total energy
5. **Severity**: Classify based on low freq percentage

### Audio Cleaning Strategy

The ffmpeg filter chain preserves voice quality while removing noise:

```
highpass → afftdn → equalizer → compand → loudnorm
```

- **Highpass**: Removes sub-speech frequencies
- **afftdn**: FFT-based noise gate
- **Equalizer**: Boosts vocal clarity
- **Compand**: Smooths dynamics
- **Loudnorm**: Standards-compliant loudness (EBU R128)

### TTS Layer Generation

For missing layers:
1. Extract text from canonical YAML (`pratibha_layers`)
2. Clean text (remove markdown, editorial notes)
3. Generate audio via ElevenLabs API
4. Cache and concatenate with appropriate silence gaps

## Troubleshooting

### "ffmpeg not found"

Install ffmpeg (see Prerequisites above).

### "numpy not found"

```bash
pip install numpy
```

### "Supabase Storage not configured"

Set environment variables:
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

### "ElevenLabs API error"

1. Check API key is set: `echo $ELEVEN_API_KEY`
2. Verify API quota at elevenlabs.io
3. Check rate limits (10 requests/minute on free tier)

### "No audio files found"

If download fails, check:
1. Supabase credentials are correct
2. Files exist in storage: `speech/tilopa_mahamudra.tilopa_mahamudra_001/translation.mp3`
3. Bucket name is correct (default: "listen")

### Partial pipeline failure

The pipeline can be resumed from any step. Previous steps' outputs are cached in `.cache/tilopa_audio/`.

## Results

After running the pipeline:

1. ✓ Wind noise removed from affected files
2. ✓ Voice clarity enhanced across all files
3. ✓ Missing commentary layers generated
4. ✓ Missing practice layers generated
5. ✓ All files uploaded to Supabase Storage
6. ✓ `listen_archive.json` updated with complete metadata

The Listen feature on the Pratibha web app will now serve the cleaned, complete audio.

## Maintenance

### Adding New Verses

If new Tilopa verses are added:

1. Add canonical YAML to `data/canonical/tilopa_mahamudra/`
2. Run the pipeline to generate audio
3. Upload to Supabase

### Re-processing

To re-process with different settings:

1. Edit filter parameters in `clean_tilopa_audio.py`
2. Delete `.cache/tilopa_audio/cleaned/`
3. Re-run step 3 (clean) and step 5 (upload)

### Bulk Collection Processing

These scripts can be adapted for other collections:
- Change `tilopa_mahamudra` → target collection
- Update voice room mapping if needed
- Adjust filter parameters based on audio characteristics

## See Also

- `app/tts.py`: TTS system configuration
- `app/listen_store.py`: Supabase Storage interface
- `data/listen_archive.json`: Audio availability index
- `scripts/bake_listen.py`: Original TTS generation script (if exists)

## License

These scripts are part of the Pratibha project (MIT License).
