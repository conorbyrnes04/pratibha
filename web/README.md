# Pratibhā Web Frontend

Next.js application providing the study interface for the Pratibhā corpus.

## Pages

| Route | Page | Description |
|---|---|---|
| `/` | Home | Landing page with navigation cards |
| `/read` | Library | Browse all collections and passages |
| `/read/[id]` | Passage | Single passage with all annotation layers |
| `/daily` | Daily | One selected passage per day |
| `/random` | Random | Serendipitous passage discovery |
| `/chat` | Study Chat | RAG-grounded Q&A with source citations |
| `/learn` | Learning Paths | Guided tracks with progress tracking |
| `/journal` | Journal | Contemplative reflection tied to passages |

## Components

- **`LayerBlock`** — renders a single annotation layer (translation, commentary, key terms, etc.)
- **`SiteNav`** — top navigation bar
- **`JournalPanel`** — inline journal for reflection during reading
- **`learn/`** — learning path components:
  - `DailySitCard` — daily practice card
  - `JourneyMandala` — visual progress mandala
  - `PassageMaturityBadge` — mastery indicator
  - `StepIntegrationGate` — progression gate between learning steps
  - `ThreadsConstellation` — visual map of cross-tradition threads
  - `YantraBreath` — breath-synchronized animation

## Stack

- **Next.js 16** with App Router
- **React 19**
- **Tailwind CSS 3**
- **TypeScript**

## Development

```bash
npm install
npm run dev
```

The frontend expects the FastAPI backend running on `http://localhost:8000`. See the [root README](../README.md) for full setup.

## Local storage

Journal entries and learning progress are persisted in the browser's `localStorage` — no account or server-side storage required.
