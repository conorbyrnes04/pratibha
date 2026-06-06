# Pratibha: Sanskrit Text RAG System

A comprehensive Retrieval Augmented Generation (RAG) system for Sanskrit texts, featuring a FastAPI backend with PostgreSQL + pgvector, and a Next.js frontend for interactive chat with Sanskrit literature.

## 🎯 Overview

Pratibha enables intelligent querying and exploration of Sanskrit texts through:
- **RAG-powered chat interface** for contextual responses about Sanskrit literature
- **Vector database** for semantic search across texts
- **YAML-based text processing** for structured Sanskrit content
- **Multiple extraction tools** for PDF, EPUB, and plain text sources

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js Web   │    │   FastAPI       │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   + pgvector    │
│   (Chat UI)     │    │   (RAG Engine)  │    │   (Vector DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   (Embeddings)  │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API key
- Groq API key (optional)

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd pratibha

# Create environment file
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key
# GROQ_API_KEY=your_groq_key
# DEFAULT_MODEL=groq/llama-3.3-70b-versatile
# USE_RAG=true
```

### 2. Database Setup

```bash
# Start PostgreSQL with pgvector
docker-compose up -d

# The database will be initialized automatically with:
# - pgvector extension
# - chunks table for vector storage
```

### 3. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start both API + web (recommended)
./scripts/dev.sh

# Or API only — reload watches app/ only (not data/ or web/)
source .env && uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port 8000
```

### 4. Frontend Setup

```bash
cd web
npm install
npm run dev
```

### 5. Ingest Sanskrit Texts

```bash
# Ingest existing YAML files into the vector database
source .env && python scripts/ingest_pgvector.py data/yaml/
```

## 📁 Project Structure

```
pratibha/
├── app/                    # FastAPI backend
│   ├── main.py            # API endpoints (/chat, /chat.stream)
│   ├── config.py          # Configuration management
│   ├── llm.py             # LLM wrapper (Groq/OpenAI)
│   ├── rag.py             # RAG retrieval logic
│   └── data_loader.py     # Data loading utilities
├── web/                   # Next.js frontend
│   └── src/app/chat/      # Chat interface
├── scripts/               # Text processing tools
│   ├── ingest_pgvector.py # Vector database ingestion
│   ├── final_clean_yuktis.py # Clean yukti extraction
│   ├── pdf_to_yaml.py     # PDF text extraction
│   ├── epub_to_yaml.py    # EPUB text extraction
│   └── text_to_yaml.py    # Plain text processing
├── data/
│   ├── canonical/         # Canonical YAML units (see DATA.md)
│   ├── raw_texts/         # Source texts (PDF, EPUB, TXT)
│   └── yaml/              # Legacy / pipeline YAML files
├── db/init/               # Database initialization
└── docker-compose.yml     # PostgreSQL + pgvector setup
```

## 📊 Canonical Corpus & Translation Quality

The canonical corpus (`data/canonical/`, ~887 units) is **not** uniformly human-translated. See [DATA.md](DATA.md) for the full breakdown.

- **`editorial_maturity`** marks where each unit stands: `publishable` (human-revised, ~19 units), `strong_draft` (default for most collections), or `structural_draft` (PD-normalized or template-assembled scaffolding, ~145 units).
- **Translation layers** in `pratibha_layers` may be original Pratibha renderings, PD-normalized derivatives (regex word-modernization of Patrick 1889, Giles 1889, etc.), or absent entirely on legacy units.
- **Commentary, key terms, resonances, and practice** layers are similarly mixed: some are hand-authored to house standards; Heraclitus and Zhuangzi pilot batches use template-assembled drafts flagged `structural_draft`.
- Do **not** treat every `translation` layer as a finished, publishable Pratibha translation. Check `editorial_maturity` and `layer_provenance` before citing or shipping content.

```bash
# Validate corpus structure and provenance honesty
python scripts/validate_canonical.py
```

## 🔧 Core Features

### 1. RAG System
- **Vector Search**: Semantic similarity search using OpenAI embeddings
- **Context Retrieval**: Automatically finds relevant text passages
- **LLM Integration**: Supports both Groq and OpenAI models
- **Streaming Responses**: Real-time chat experience

### 2. Text Processing Pipeline
- **PDF Extraction**: Extract text from Sanskrit PDFs
- **EPUB Processing**: Handle digital Sanskrit books
- **YAML Structure**: Standardized format for Sanskrit texts
- **Verse Detection**: Automatic identification of verses and sutras

### 3. Data Formats

#### YAML Structure
```yaml
sutra_id: yukti_001
collection: Vijñāna Bhairava
section: meditation_technique
sanskrit: "संस्कृतम्"
transliteration: "saṃskṛtam"
translation: "YUKTI #1\nThe Supreme Goddess constantly articulates..."
commentary: ""
modes:
  bhasya: ""
  doctrinal: ""
  comparative: ""
  sadhana: "YUKTI #1\nThe Supreme Goddess constantly articulates..."
```

## 📚 Available Texts

### Shiva Sutra Collection
- **Location**: `data/yaml/siva_sutra/`
- **Content**: 60+ sutras from the Shiva Sutras
- **Format**: Sanskrit, transliteration, translation, commentary

### Vijñāna Bhairava Yuktis
- **Location**: `data/yaml/vijnana_bhairava_final/`
- **Content**: 15 meditation techniques (yuktis)
- **Format**: Clean, focused teachings without commentary

## 🛠️ Scripts & Tools

### Text Processing
```bash
# Extract from PDF
python scripts/pdf_to_yaml.py input.pdf output_dir

# Extract from EPUB
python scripts/epub_to_yaml.py input.epub output_dir

# Process plain text
python scripts/text_to_yaml.py input.txt output_dir

# Create clean yuktis (customizable)
python scripts/final_clean_yuktis.py
```

### Database Operations
```bash
# Ingest YAML files into vector database
python scripts/ingest_pgvector.py data/yaml/

# Check database status
docker-compose ps
```

## 🔍 API Endpoints

### Chat Endpoints
- `POST /chat` - Single response chat
- `POST /chat.stream` - Streaming chat response

### Request Format
```json
{
  "message": "What is the first yukti in Vijñāna Bhairava?",
  "use_rag": true
}
```

### Response Format
```json
{
  "response": "The first yukti teaches about the breath...",
  "sources": [
    {
      "text": "YUKTI #1\nThe Supreme Goddess...",
      "metadata": {"sutra_id": "yukti_001", "collection": "Vijñāna Bhairava"},
      "score": 0.95
    }
  ]
}
```

## 🎨 Web Interface

The Next.js frontend provides:
- **Real-time chat** with Sanskrit texts
- **Source citations** showing relevant passages
- **Responsive design** for all devices
- **Streaming responses** for better UX

## 🔧 Configuration

### Environment Variables
```bash
# API Keys
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Model Settings
DEFAULT_MODEL=groq/llama-3.3-70b-versatile
USE_RAG=true

# Database Settings
PG_USER=postgres
PG_PASSWORD=postgres
PG_DB=pratibha
PG_HOST=localhost
PG_PORT=5432
```

### RAG Settings
- **Embedding Model**: `text-embedding-3-small`
- **Vector Dimension**: 1536
- **Similarity Metric**: Cosine similarity
- **Retrieval Count**: 4 chunks per query

## 🚀 Deployment

### Development
```bash
# Both servers (stable reload scope)
./scripts/dev.sh

# API only (reload watches app/ — avoids reload storms from data/ or node_modules/)
source .env && uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port 8000

# Web only
cd web && npm run dev
```

### Production
```bash
# Build frontend
cd web && npm run build

# Run backend with production server
source .env && gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📖 Usage Examples

### 1. Querying Sanskrit Texts
```
User: "What are the different types of meditation in Vijñāna Bhairava?"
System: [Retrieves relevant yuktis and provides contextual response]
```

### 2. Adding New Texts
```bash
# 1. Place source file in data/raw_texts/
# 2. Extract using appropriate script
python scripts/pdf_to_yaml.py new_text.pdf data/yaml/new_collection/
# 3. Ingest into database
python scripts/ingest_pgvector.py data/yaml/new_collection/
```

### 3. Customizing Yuktis
```bash
# Edit the yukti definitions
vim scripts/final_clean_yuktis.py
# Regenerate YAML files
python scripts/final_clean_yuktis.py
# Re-ingest
python scripts/ingest_pgvector.py data/yaml/vijnana_bhairava_final/
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   # Restart if needed
   docker-compose restart
   ```

2. **API Key Errors**
   ```bash
   # Verify environment variables
   source .env && echo $OPENAI_API_KEY
   ```

3. **Vector Dimension Mismatch**
   ```bash
   # Recreate database with correct schema
   docker-compose down -v
   docker-compose up -d
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your Sanskrit texts to `data/raw_texts/`
4. Process using appropriate scripts
5. Test the RAG system
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for embedding models
- **Groq** for fast LLM inference
- **pgvector** for vector similarity search
- **Sanskrit scholars** whose translations make this possible

---

**Pratibha** - "Intelligence" in Sanskrit, enabling intelligent exploration of ancient wisdom through modern technology.