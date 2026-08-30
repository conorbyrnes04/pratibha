# Pratibha Social Layer

## Product Design

Verse-centered social interaction without typical social network features. The focus is on contemplation and respectful discussion around sacred texts.

### What This Is NOT

- ❌ No Reddit-style homepage feed
- ❌ No public user profiles or karma
- ❌ No direct messages between users
- ❌ No leaderboards or gamification

### Core Features (First Slice)

#### 1. Like a Verse

- One like per user per verse
- Click again to unlike
- Display total like count
- Available on:
  - Read page (individual verse view)
  - Home page (daily passage)

#### 2. Comment on Verses

- Forum-style threaded discussions on each passage
- Nest up to 3 levels deep:
  - Level 0: Top-level comment on the verse
  - Level 1: Reply to a top-level comment
  - Level 2: Reply to a reply
  - Level 3: Final nesting level
- Reply functionality at all levels
- Comments are public (visible to signed-out users)
- Posting requires authentication

#### 3. Share to Social Platforms

Generate a verse card with deep link back to the specific verse in Pratibha.

**Platforms:**
- **X (Twitter):** Share intent with verse text + URL
- **Instagram:** Save/share verse card image + copy caption with URL
- **TikTok:** Save/share verse card image + copy caption with URL

**Card Content:**
- Original line (if available)
- Translation
- Pratibha branding mark
- Deep link URL to `/read/:verseId`

**Technical Approach:**
- Generate card in-app using HTML canvas (no paid screenshot APIs)
- Use Web Share API where available
- Fallback: download image + copy caption to clipboard
- Deep links open the specific verse in Pratibha app

#### 4. Content Moderation

Proactive filtering before content becomes visible. This is a spiritual study app requiring right-speech standards.

**NOT relying solely on user reports** — filtering runs on write.

---

## Data Schema (Convex)

### New Tables

#### `verse_likes`

| Field | Type | Description |
|-------|------|-------------|
| `userId` | `string` | User who liked |
| `verseId` | `string` | Verse being liked |
| `createdAt` | `number` | Timestamp |

**Indexes:**
- `by_user` on `[userId]` — likes by a user
- `by_verse` on `[verseId]` — likes for a verse
- `by_user_verse` on `[userId, verseId]` — uniqueness check

**Constraints:**
- Unique per `(userId, verseId)` pair

#### `verse_comments`

| Field | Type | Description |
|-------|------|-------------|
| `userId` | `string` | Comment author |
| `verseId` | `string` | Verse being commented on |
| `parentId` | `string \| null` | Parent comment ID (null = top-level) |
| `body` | `string` | Comment text |
| `depth` | `number` | Nesting level (0-3) |
| `status` | `"visible" \| "hidden" \| "pending"` | Moderation status |
| `createdAt` | `number` | Creation timestamp |
| `updatedAt` | `number` | Last edit timestamp |

**Indexes:**
- `by_verse_created` on `[verseId, createdAt]` — chronological comments
- `by_parent` on `[parentId]` — replies to a comment
- `by_user` on `[userId]` — user's comments
- `by_status` on `[status]` — moderation queue

#### `comment_reports`

| Field | Type | Description |
|-------|------|-------------|
| `commentId` | `string` | Comment being reported |
| `reporterUserId` | `string` | User who reported |
| `reason` | `string` | Report reason/category |
| `createdAt` | `number` | Report timestamp |

**Indexes:**
- `by_comment` on `[commentId]` — reports for a comment

---

## Moderation System

### Moderation on Write (Comment Insert/Update)

**Pre-checks (all must pass):**

1. **Authentication:** User must be logged in
2. **Length:** 
   - Min: 10 characters (trimmed)
   - Max: 2000 characters (trimmed)
3. **Rate limiting:** Max 10 comments per user per hour
4. **Depth cap:** Cannot exceed depth 3
5. **Reply limit:** Max 50 direct replies per parent comment

**Content Filtering:**

1. **Server-side blocklist** (case-insensitive):
   - Common slurs and profanity
   - Sexual vulgarity
   - Obvious hate speech patterns
   
2. **OpenAI Moderation API** (if `OPENAI_API_KEY` available):
   - Call from Convex action
   - Flag categories: `hate`, `harassment`, `sexual`
   - If flagged → reject
   - If no API key → blocklist still applies

**Default Status:**
- Pass all checks → `status: "visible"`
- Fail any check → throw error with calm message (never persisted as visible)

**Error Messages:**

Keep messages calm and in-register with a contemplative app:

- Too short: "Please share a more complete thought (at least 10 characters)."
- Too long: "Please keep comments concise (under 2000 characters)."
- Rate limit: "Please take time to reflect before commenting again."
- Depth limit: "Conversation thread is complete. Start a new top-level comment."
- Reply limit: "This thread has reached its capacity. Start a new discussion."
- Content filter: "This comment does not meet our community guidelines for respectful discourse."

### Report Handling

**User Reports:**
- Any authenticated user can report a comment
- Report includes `reason` (text field)
- After **3 reports**, comment automatically moves to `status: "hidden"`
- First report on a comment marks it as `status: "pending"` for moderator review

**Moderator View:**
- Admin can query `by_status` index for `"pending"` or `"hidden"` comments
- Review via Convex dashboard or simple admin page (if time permits)
- Query: `db.query("verse_comments").withIndex("by_status", q => q.eq("status", "pending"))`

### First-Time Commenter Reminder

When a user posts their first comment, show a one-line reminder in the UI:

> **Right speech:** Share insights with kindness and clarity.

Store `hasCommented` flag in user profile or check if user has any comments.

---

## Sharing System

### Deep Link Structure

**URL Format:** `/read/:verseId`

This should route to the verse detail view (either existing or new route in Read page).

**Example:** `https://pratibha.app/read/bhagavad_gita_2_47`

### Verse Card Generation

**Card Design:**
```
┌──────────────────────────────────────┐
│                                      │
│  [Original text in Sanskrit/etc]     │
│                                      │
│  "Translation text here..."          │
│                                      │
│  pratibha                            │
│  [Yantra mark]                       │
│                                      │
│  pratibha.app/read/verse_id          │
└──────────────────────────────────────┘
```

**Technical Implementation:**

1. **Canvas-based generation:**
   - Use HTML5 Canvas API
   - Render verse text + branding
   - Export as PNG or JPEG
   
2. **Alternative: DOM snapshot:**
   - Create hidden styled `<div>` with verse content
   - Use `html2canvas` library (if needed)
   - Convert to blob/dataURL

3. **No external APIs:** Don't depend on paid screenshot services

### Platform-Specific Sharing

#### X (Twitter)

```javascript
const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
  `${verseTitle}\n\n"${verseTranslation.slice(0, 200)}..."\n\n${deepLink}`
)}`;
window.open(tweetUrl, '_blank');
```

#### Instagram & TikTok

These platforms don't support web intents. Instead:

1. **Generate card image**
2. **Use Web Share API** (if available):
   ```javascript
   await navigator.share({
     files: [cardImageFile],
     text: caption,
   });
   ```

3. **Fallback:**
   - Download image as file
   - Copy caption to clipboard
   - Show instructions: "Image saved! Caption copied. Paste in Instagram/TikTok."

**Caption Format:**
```
[Verse Title]

"[First 200 chars of translation]..."

Read the full verse: [deep link URL]
```

### Open Graph Tags

For proper link previews when verse URLs are shared:

**Approach:**
- If Lynx web can serve meta tags: add OG tags to verse route
- If not: Create a minimal public HTML fallback for crawlers
- **Do NOT rebuild Next.js app** for this

**Tags needed:**
```html
<meta property="og:title" content="[Verse Title]" />
<meta property="og:description" content="[Translation excerpt]" />
<meta property="og:image" content="[Generated card image URL]" />
<meta property="og:url" content="[Deep link]" />
```

---

## HTTP / Convex Client

### Issue with Current Implementation

The current `httpClient.ts` uses:
```typescript
const url = `${CONVEX_URL}/api/${type}/${functionName}`;
```

**This is incorrect for Convex HTTP API.**

### Correct Convex HTTP API

Convex HTTP API endpoints:
- Query: `POST https://[deployment].convex.cloud/api/query`
- Mutation: `POST https://[deployment].convex.cloud/api/mutation`  
- Action: `POST https://[deployment].convex.cloud/api/action`

**Request body:**
```json
{
  "path": "moduleName:functionName",
  "args": { ... },
  "format": "json"
}
```

### Fix Required

Update `httpClient.ts` to match Convex's actual API format, or use `ConvexHttpClient` from `convex/browser` (recommended for web target).

Password auth must continue to work without requiring Google OAuth.

---

## UI Components (Lynx)

All UI built with official Lynx elements: `<view>`, `<text>`, `<scroll-view>`, `<input>`, `<image>`.

### Like Button Component

```tsx
<view onClick={handleLike} style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
  <text style={{ fontSize: 20 }}>{isLiked ? '♥' : '♡'}</text>
  <text style={{ color: '#999', fontSize: 14 }}>{likeCount}</text>
</view>
```

### Comment Section

**Layout:**
- Top-level comments shown chronologically
- Replies indented progressively (0 → 16px → 32px → 48px)
- "Reply" button on each comment (if depth < 3)
- "Report" link on each comment

**Comment Composition:**
- Text input area
- Character counter
- "Post Comment" / "Post Reply" button
- First-time user sees right-speech reminder

### Share Menu

Three platform buttons:
- X logo + "Share to X"
- Instagram logo + "Share to Instagram"  
- TikTok logo + "Share to TikTok"

On click:
1. Generate verse card
2. Execute platform-specific share flow
3. Show success/instruction message

---

## Out of Scope

- ❌ Merging this PR automatically
- ❌ Deleting `web/` directory
- ❌ Replacing `corpus/` FastAPI server
- ❌ Full Reddit clone with karma/awards
- ❌ User profiles and walls
- ❌ Following/followers
- ❌ Notifications system (v2 feature)
- ❌ Edit/delete comments (v2 feature)
- ❌ Real-time comment updates (HTTP client limitation)

---

## Testing Locally

### Prerequisites

1. **Convex backend running:**
   ```bash
   cd pratibha
   npx convex dev
   ```

2. **FastAPI corpus server:**
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. **Optional: OpenAI API key** for moderation
   ```bash
   # In pratibha/.env
   OPENAI_API_KEY=sk-...
   ```

### Try It Out

1. **Start the app:**
   ```bash
   cd pratibha
   npm run dev
   ```

2. **Create an account or sign in**

3. **Navigate to Home or Read page**

4. **Try features:**
   - Click heart to like a verse
   - Post a comment
   - Reply to your comment (nest up to 3 levels)
   - Click share buttons (test X intent, download cards)
   - Try posting profane/spammy content (should be blocked)

5. **Test moderation:**
   - Post 3+ reports on a comment → should hide it
   - Check Convex dashboard for comment statuses

---

## Implementation Checklist

- [x] Schema tables defined in `convex/schema.ts`
- [x] Convex queries/mutations for likes
- [x] Convex queries/mutations for comments (with moderation)
- [x] Convex queries/mutations for reports
- [x] Moderation action with OpenAI integration
- [x] Like button UI component
- [x] Comment section UI component
- [x] Comment composition UI with validation
- [x] Share button UI components
- [x] Verse card generation logic
- [x] Platform-specific share handlers
- [x] First-time commenter reminder
- [x] Integration into Read page
- [x] Integration into Home page
- [x] README update with social layer setup
- [x] Testing and type-checking

---

## Future Enhancements (Not in First Slice)

- Edit/delete own comments
- Real-time comment updates via WebSocket
- Push notifications for replies
- Moderator dashboard UI
- Comment search
- Saved verses collection
- Email digests of popular discussions
- Block/mute users
- Comment sorting (newest/oldest/most liked)
