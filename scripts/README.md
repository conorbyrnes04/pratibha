# Scripts

Text processing, corpus validation, and ingestion tools. **Getting started:** root [README](../README.md).

## Script overview

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `ingest_pgvector.py` | Ingest YAML files into vector database | YAML directory | PostgreSQL chunks table |
| `final_clean_yuktis.py` | Generate clean yukti YAML files | None (hardcoded) | Clean yukti YAML files |
| `pdf_to_yaml.py` | Extract text from PDF files | PDF file | YAML files |
| `epub_to_yaml.py` | Extract text from EPUB files | EPUB file | YAML files |
| `text_to_yaml.py` | Process plain text files | TXT file | YAML files |

## 🔧 Script Details

### 1. `ingest_pgvector.py`
**Purpose**: Ingest YAML files into the PostgreSQL vector database for RAG retrieval.

**Usage**:
```bash
source .env && python scripts/ingest_pgvector.py data/yaml/
```

**Features**:
- Generates OpenAI embeddings for all text content
- Handles long text by chunking into smaller pieces
- Supports multiple YAML fields (sanskrit, transliteration, translation, commentary, modes)
- Converts Python objects to JSON for database storage
- Error handling for API rate limits and large texts

**Input Format**: YAML files with structured Sanskrit content
**Output**: Vector embeddings stored in PostgreSQL `chunks` table

### 2. `final_clean_yuktis.py`
**Purpose**: Generate clean, focused yukti (meditation technique) YAML files.

**Usage**:
```bash
python scripts/final_clean_yuktis.py
```

**Features**:
- Creates 15 clean yuktis in exact format: "YUKTI #X + core teaching"
- No commentary or extra text
- Easily customizable by editing the script
- Consistent YAML structure for all yuktis

**Output**: `data/yaml/vijnana_bhairava_final/yukti_XXX.yml`

**Customization**:
```python
# Edit the yuktis list in the script
yuktis = [
    {
        'verse_number': '16',
        'content': 'YUKTI #16\nYour new yukti content here...'
    },
    # Add more yuktis...
]
```

### 3. `pdf_to_yaml.py`
**Purpose**: Extract text from PDF files and create YAML stubs.

**Usage**:
```bash
python scripts/pdf_to_yaml.py input.pdf output_directory
```

**Features**:
- Uses pdfminer for text extraction
- Handles complex PDF layouts
- Creates basic YAML structure
- Preserves page information

**Input**: PDF file
**Output**: YAML files with extracted text

### 4. `epub_to_yaml.py`
**Purpose**: Extract text from EPUB files and create YAML stubs.

**Usage**:
```bash
python scripts/epub_to_yaml.py input.epub output_directory
```

**Features**:
- Parses EPUB structure
- Extracts chapter content
- Creates YAML files per chapter
- Handles metadata

**Input**: EPUB file
**Output**: YAML files with chapter content

### 5. `text_to_yaml.py`
**Purpose**: Process plain text files and extract verses into structured YAML.

**Usage**:
```bash
python scripts/text_to_yaml.py input.txt output_directory
```

**Features**:
- Detects verse patterns using regex
- Handles Sanskrit and transliterated text
- Creates structured YAML output
- Supports multiple verse formats

**Input**: Plain text file
**Output**: YAML files with detected verses

## 🚀 Workflow Examples

### Adding New Sanskrit Texts

1. **PDF Source**:
   ```bash
   # Place PDF in data/raw_texts/
   cp new_text.pdf data/raw_texts/
   
   # Extract to YAML
   python scripts/pdf_to_yaml.py data/raw_texts/new_text.pdf data/yaml/new_collection/
   
   # Ingest into database
   source .env && python scripts/ingest_pgvector.py data/yaml/new_collection/
   ```

2. **EPUB Source**:
   ```bash
   # Place EPUB in data/raw_texts/
   cp new_book.epub data/raw_texts/
   
   # Extract to YAML
   python scripts/epub_to_yaml.py data/raw_texts/new_book.epub data/yaml/new_collection/
   
   # Ingest into database
   source .env && python scripts/ingest_pgvector.py data/yaml/new_collection/
   ```

3. **Plain Text Source**:
   ```bash
   # Place text file in data/raw_texts/
   cp new_text.txt data/raw_texts/
   
   # Process to YAML
   python scripts/text_to_yaml.py data/raw_texts/new_text.txt data/yaml/new_collection/
   
   # Ingest into database
   source .env && python scripts/ingest_pgvector.py data/yaml/new_collection/
   ```

### Customizing Yuktis

1. **Edit the yukti definitions**:
   ```bash
   vim scripts/final_clean_yuktis.py
   ```

2. **Add new yuktis to the list**:
   ```python
   yuktis = [
       # Existing yuktis...
       {
           'verse_number': '16',
           'content': 'YUKTI #16\nYour new meditation technique here...'
       }
   ]
   ```

3. **Regenerate YAML files**:
   ```bash
   python scripts/final_clean_yuktis.py
   ```

4. **Re-ingest into database**:
   ```bash
   source .env && python scripts/ingest_pgvector.py data/yaml/vijnana_bhairava_final/
   ```

## 🔍 YAML Structure

All scripts produce YAML files with this structure:

```yaml
sutra_id: unique_identifier
collection: "Collection Name"
section: "text_type"
sanskrit: "संस्कृतम्"
transliteration: "saṃskṛtam"
translation: "English translation"
commentary: "Additional commentary"
modes:
  bhasya: "Traditional commentary"
  doctrinal: "Doctrinal analysis"
  comparative: "Comparative study"
  sadhana: "Practice instructions"
```

## ⚠️ Important Notes

### Environment Variables
Always source the environment file before running ingestion scripts:
```bash
source .env
```

### API Rate Limits
The ingestion script includes error handling for OpenAI API rate limits. If you encounter rate limit errors:
- Wait a few minutes before retrying
- Consider processing smaller batches of files

### Text Chunking
Long texts are automatically chunked to avoid embedding model limits. The script splits text at sentence boundaries to maintain coherence.

### Database Schema
The scripts expect a PostgreSQL database with pgvector extension and a `chunks` table with this structure:
```sql
CREATE TABLE chunks (
  id SERIAL PRIMARY KEY,
  body TEXT NOT NULL,
  embedding VECTOR(1536) NOT NULL,
  metadata JSONB DEFAULT '{}'::jsonb
);
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Connection**:
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   ```

3. **API Key Issues**:
   ```bash
   # Verify environment variables
   source .env && echo $OPENAI_API_KEY
   ```

4. **File Permission Errors**:
   ```bash
   # Ensure write permissions
   chmod 755 data/yaml/
   ```

## 📚 Dependencies

All scripts require these Python packages:
- `yaml` - YAML file processing
- `asyncpg` - PostgreSQL async driver
- `openai` - OpenAI API client
- `pdfminer` - PDF text extraction
- `beautifulsoup4` - HTML/XML parsing (for EPUB)
- `pathlib` - File path handling

Install with:
```bash
pip install -r requirements.txt
```