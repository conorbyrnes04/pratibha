# Remaining upgrades — execution order

Web is the product. The essential spine (`RECOMMENDED_SPINE`) was not changed.

## Wave 1 — Finish the walk loop (done)

One gate a day. Finish it, and tomorrow names itself.

## Wave 2 — Real tradition trails (done)

Yoga (Patañjali), Buddhism, and Yoruba are walkable from Paths. They are **not** on The Path spine. Sufi and Christian mysticism remain coming soon.

## Wave 3 — Living tradition into the house (done)

Layer-split into the live corpus (commentary, key terms, resonances, practice). English-source works keep Original only; Ellis òwe keep Translation only. Public domain ≠ cultural permission — provenance notes stay, and ceremonial/secret material is not ingested. Do not ingest `data/staging/` into pgvector.

| Collection | Tradition | Units |
|---|---|---|
| Yoruba Proverbs (Òwe) | Yoruba | 130 |
| The Yoruba Faith (Johnson) | Yoruba | 8 |
| The Soul of the Indian (Eastman) | Dakota | 30 |
| Old Indian Legends (Zitkála-Šá) | Dakota | 12 |

The Yoruba trail is their Path seat. Living-tradition tomes sit on the default Library shelf (drafts off).

## Wave 4 — Chat serves the gate (done)

Chat opened from Today / a gate is framed as this gate and pinned to the verse.

## Wave 5 — Circle and manuscript as a book (done)

Public `/m/[slug]` reads as a chapbook (leaves, page numbers, colophon). Circle stays one reading each, with a write-yours link. Share folio tries the OS sheet first (IG/TikTok included).

## Wave 6 — Native is the same walk (done)

Lynx primary nav is Today → Path → Library → Mine; Today sits on the essential gate. Expo tabs match; Mine is a chapbook seat. Chat/Journal are secondary.

## Wave 7 — Production (reader errors done)

Auth no longer blanks protected routes with “Checking session…”. Read-page Convex hooks do not run when Convex is off. Sign-in CTAs wait for session. Raw Convex messages stay out of production `error.tsx`. Deploy still needs `web/.env.production` + Cloudflare/Convex secrets — run `cd web && npm run deploy` when those are present. Light theme stays deferred.

## Wave 8 — Library and Sources by tradition (done)

Library default grouping and `/sources` use the same shelf order: Vedānta → Yoga → Kashmir Śaiva → Buddhist → Daoist → Confucian → Yoruba → Dakota → Hebrew → Greek → Christian → Sufi (`TRADITION_ORDER` in `web/src/lib/libraryTomes.ts`). No leftover Other bucket. Sources cards drop the redundant tradition subtitle; coming-soon items stay inside their tradition.

Corpus collections that were on the Library shelf but missing from the Sources registry were added (Kaṭha, Bṛhadāraṇyaka, Muṇḍaka, Dhammapada, Marcus Aurelius, Parmenides, Cloud of Unknowing, Pseudo-Dionysius). A Course in Miracles sits on the Christian shelf. Kabbalah — Sefer Yetzirah & the Zohar is in the live corpus with its own named shelf until that label folds into Hebrew.
