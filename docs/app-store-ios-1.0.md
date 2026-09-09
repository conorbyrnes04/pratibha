# App Store Connect — Pratibha iOS 1.0

Bundle `com.pratibha.app`. Version `1.0.0`. Submit **Friday 11 Sep 2026** (Saturday 12 is backup). Privacy URL must match production after web deploy.

## Listing

**Name** (30): Pratibha

**Subtitle** (30): A walk through world wisdom

**Promotional text** (170, optional):
A daily gate into public-domain wisdom texts. Walk a path, read the library, keep a journal. Sign in with email to carry notes and progress to the website.

**Description:**
Pratibha is a guided walk through world wisdom — not a pile of books.

Each day opens one gate: a teaching, a canonical passage, and one practice. Finish the gate, and tomorrow names itself. The Path, the Library, and your notes live on this phone. Sign in with email and password to keep a journal and carry your walk to pratibha.agniagama.com.

The library is public-domain contemplative texts: Yoga, the Gītā, Buddhist, Sufi, Christian mystical, Yoruba, and other lineages we have permission to host. Listen audio is on the website. Study chat is on the website.

No ads. No tracking. No Google sign-in in the app. Delete your account any time from Settings.

**Keywords** (100 chars, comma-separated, no spaces after commas if tight):
wisdom,philosophy,yoga,meditation,gita,buddhist,sufi,journal,sanskrit,contemplation

**Support URL:** https://pratibha.agniagama.com
**Marketing URL:** https://pratibha.agniagama.com
**Privacy Policy URL:** https://pratibha.agniagama.com/privacy
**Copyright:** 2026 Agni Agama

**Age rating:** 4+ (no unrestricted web, no violence, no medical claims). Do not tick “Made for Kids”.

**Category:** Education (primary). Lifestyle (secondary, optional).

## Review notes

Sign in is email and password only (minimum 10 characters), same Convex account as the website. There is no Google button and no Sign in with Apple.

Demo account: use any existing password account, or create one in-app. Library, Path, and Today work signed out.

Account deletion: Settings → Delete account. That removes journal notes, path progress, circle offerings, and the login. The public library stays. Same action exists on the website at /account.

Contact: conor@agniagama.com

## Privacy nutrition labels

Data linked to identity (when the user signs in):

| Data type | Purpose | Linked to identity | Used for tracking |
|---|---|---|---|
| Email address | Account | Yes | No |
| User content (journal notes, path progress) | App functionality | Yes | No |

Not collected: location, contacts, browsing history, search history, identifiers for ads, purchases, health, sensitive info, diagnostics (unless Apple’s crash reports — leave off if we do not use them), other user content beyond journal/progress.

Tracking: **No**. We do not use the App Tracking Transparency prompt.

Third parties named in the privacy policy: Convex (accounts and sync), Render (public library API). ElevenLabs and OpenRouter are used on the **website**, not in this iOS 1.0 binary. Google OAuth is website-only.

## Screenshots (6.7" iPhone required)

1. Today — the day’s gate
2. Path — a trail with a few steps done
3. Library — a collection cover
4. Passage — original + translation
5. Mine — a journal note
6. Settings — signed-in account + Delete account visible

Dark UI. Do not show chat as a tab. Do not show Google.

## Build

```bash
cd mobile
eas build --platform ios --profile production
eas submit --platform ios --latest
```
