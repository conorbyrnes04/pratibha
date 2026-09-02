# Pratibhā

**A multi-tradition contemplative corpus with RAG-powered study tools.**

*Pratibhā* (प्रतिभा) — "luminous intelligence," the flash of recognition by which consciousness knows itself. In the Pratyabhijñā tradition, *pratibhā* is not acquired learning but the innate brilliance that makes understanding possible at all.

This project is two things at once:

1. **A structured corpus** of 583 annotated units spanning 17 philosophical and contemplative traditions — Sanskrit, Greek, Chinese, Arabic, Persian, Senegambian, Pulaar — each processed through a seven-layer scholarly format (original text, transliteration, translation, commentary, key terms, cross-tradition resonances, practice).

2. **A study application** — FastAPI backend + Next.js frontend + PostgreSQL/pgvector — that makes the corpus queryable, browsable, and livable through RAG-powered chat, daily practice passages, a contemplative journal, and guided learning paths.

---

## The Corpus

| Collection | Tradition | Units | Source |
|---|---|---|---|
| **Śiva Sūtra** | Nondual Śaiva Tantra | 47 | Vasugupta |
| **Vijñāna Bhairava Tantra** | Nondual Śaiva Tantra | 112 | 112 dhāraṇās (yuktis) |
| **Yoga Spanda-kārikā** | Spanda school | 52 | Vasugupta / Kallaṭa |
| **Pratyabhijñāhṛdayam** | Pratyabhijñā | 21 | Kṣemarāja |
| **Aṣṭāvakra Gītā** | Advaita | 31 | — |
| **Bhagavad Gītā** | Vedānta / Yoga | 12 | Selected passage-units |
| **Īśāvāsya Upaniṣad** | Upanishadic | 24 | — |
| **Śvetāśvatara Upaniṣad** | Upanishadic | 22 | — |
| **Māṇḍūkya Upaniṣad + Gauḍapāda Kārikā** | Advaita / Ajātivāda | 16 | Gauḍapāda |
| **Heraclitus Fragments** | Pre-Socratic Greek | 128 | Diels-Kranz numbering |
| **Epictetus: Enchiridion** | Stoic | 3 | Carter/Higginson |
| **Phaedo** | Platonic | 7 | Plato |
| **Dào Dé Jīng** | Daoist | 4 | Lǎozǐ |
| **The Book of Chuang Tzu** | Daoist | 48 | Zhuāngzǐ |
| **Know Yourself** | Sufi (Ibn ʿArabī / al-Balayānī) | 36 | — |
| **Senegalese Animism** | Serer / Senegambian | 10 | Lasnet 1900; Bérenger-Féraud 1879; Delafosse 1925 |
| **Pulaar Tradition** | Fulɓe / Pulaar (pre-Islamic remnants) | 10 | Reclus 1887; Crozals 1883; Lasnet 1900; Delafosse 1925 |

**583 units total.** Each unit carries up to seven annotated layers — see [DATA.md](DATA.md) for the full schema and pipeline.

### The Seven Layers (Pratibhā Format)

Every canonical unit passes through this structure:

1. **Original / Devanāgarī** — source script (Devanāgarī, Greek, Traditional Chinese, Arabic)
2. **IAST / Transliteration** — full diacritics, compound resolution at morpheme boundaries
3. **Pratibhā Translation** — present-tense, active-voice, philosophically precise; no archaisms
4. **Pratibhā Commentary** — opens with an explicit philosophical claim, names the counterintuitive move, ≥150 words
5. **Key Terms** — etymology → tradition-specific meaning → why the default translation fails
6. **Cross-Tradition Resonances** — structural (not thematic) parallels across traditions, with divergence notes
7. **Practice (Abhyāsa)** — second-person, present-tense, derived from *this specific passage*

---

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js Web   │    │   FastAPI        │    │  PostgreSQL     │
│   Frontend      │◄──►│   Backend        │◄──►│  + pgvector     │
│                 │    │   (RAG Engine)   │    │  (Vector DB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       │                        │
       │  Pages:                ▼
       │  · Library       ┌─────────────────┐
       │  · Daily         │   LLM Provider  │
       │  · Random        │   (Groq/OpenAI) │
       │  · Study Chat    └─────────────────┘
       │  · Journal
       │  · Learning Paths
```

The backend serves the corpus via REST endpoints and streams RAG-grounded responses. The frontend provides five study modes:

- **Library** — browse all collections and passages
- **Daily** — one selected passage per day
- **Random** — serendipitous discovery
- **Study Chat** — ask questions in plain language, get RAG-grounded answers with source citations
- **Learning Paths** — guided tracks from concept to practice, with a journal integration
- **Journal** — contemplative reflection tied to passages

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Docker & Docker Compose
- API key for at least one LLM provider (OpenAI, Groq, or OpenRouter)

### 1. Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 2. Database

```bash
docker-compose up -d
```

### 3. Backend

```bash
pip install -r requirements.txt
source .env && uvicorn app.main:app --reload --port 8000
```

### 4. Ingest the Corpus

```bash
source .env && python scripts/ingest_pgvector.py data/canonical/
```

### 5. Frontend

```bash
cd web && npm install && npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Project Structure

```
pratibha/
├── app/                        # FastAPI backend
│   ├── main.py                 #   API endpoints (health, verses, chat, stream)
│   ├── rag.py                  #   RAG retrieval logic (pgvector similarity search)
│   ├── llm.py                  #   LLM wrapper (Groq / OpenAI / OpenRouter)
│   ├── data_loader.py          #   Loads canonical YAML at startup
│   ├── collection_aliases.py   #   Human-readable collection labels
│   └── config.py               #   Settings from environment
├── web/                        # Next.js frontend
│   └── src/
│       ├── app/                #   Pages: home, chat, daily, learn, journal, read, random
│       ├── components/         #   LayerBlock, SiteNav, JournalPanel, learn/*
│       ├── hooks/              #   useLearnProgress
│       └── lib/                #   API client, types, learning paths, journal storage
├── scripts/                    # Text processing pipeline (31 scripts)
│   ├── *_md_to_yaml.py         #   Markdown → structured YAML
│   ├── *_epub_to_yaml.py       #   EPUB → structured YAML
│   ├── canonicalize_texts.py   #   YAML → canonical format
│   ├── enrich_yaml_*.py        #   LLM-powered enrichment
│   ├── ingest_pgvector.py      #   Canonical YAML → pgvector embeddings
│   └── validate_canonical.py   #   Schema validation for canonical units
├── data/
│   ├── raw_texts/              #   Source manuscripts (Pratibhā MD format)
│   ├── yaml/                   #   Intermediate YAML (per-script output)
│   ├── canonical/              #   Final validated units (source of truth)
│   └── reports/                #   Enrichment quality reports
├── db/init/                    # PostgreSQL initialization (pgvector extension)
├── docker-compose.yml          # PostgreSQL + pgvector + Adminer
└── requirements.txt            # Python dependencies
```

See [DATA.md](DATA.md) for a detailed explanation of the data pipeline.

---

## API

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Status + loaded item count |
| `/verses` | GET | All loaded passages |
| `/verse/{id}` | GET | Single passage by ID |
| `/daily` | GET | Today's selected passage |
| `/random` | GET | Random passage |
| `/chat` | POST | Single RAG-grounded response |
| `/chat.stream` | POST | Streaming RAG-grounded response |

---

## Configuration

Key settings in `.env`:

| Variable | Default | Notes |
|---|---|---|
| `OPENAI_API_KEY` | — | Required for embeddings (text-embedding-3-small) |
| `GROQ_API_KEY` | — | Optional: fast inference via Groq |
| `DEFAULT_MODEL` | `groq/llama-3.3-70b-versatile` | LLM for chat responses |
| `USE_RAG` | `true` | Enable/disable vector retrieval |
| `RAG_FETCH_K` | `20` | Candidates to retrieve before reranking |
| `RAG_MIN_SCORE` | `0.2` | Cosine similarity threshold |

---

## Contributing

The corpus is the heart of this project. Contributions that add new texts, improve translations, deepen commentaries, or extend cross-tradition resonances are especially welcome. See [DATA.md](DATA.md) for the schema and quality standards.

---

## License

[MIT](LICENSE)

---

*Pratibhā* — प्रतिभा — luminous intelligence, the flash of recognition.
