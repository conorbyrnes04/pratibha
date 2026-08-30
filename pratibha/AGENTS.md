## Read in Advance
- Lynx: https://lynxjs.org/llms.txt
  While dealing with a Lynx task, an agent MUST read this doc because it is an entry point of all available docs about Lynx.

## Pratibha-Specific Notes

### Architecture
- **Backend**: Convex (HTTP client only, not stock convex-js)
  - PrimJS (Lynx's JavaScript runtime) does not support BigInt
  - Use custom HTTP client in `src/convex/httpClient.ts`
  - Authentication via HTTP bearer tokens stored in localStorage (with guards for Lynx compatibility)

### Features
- Verse social layer: likes, nested comments (3-level depth), share to social platforms
- Daily verse rotation with full library browse
- Journal notes with tagging

### Development Target
- Primary: Lynx native (iOS/Android)
- Web preview: Use rspeedy's `/__web_preview?casename=index.web.bundle` URL during development
- Both environments configured in `lynx.config.ts`: `environments: { web: {}, lynx: {} }`

### ReactLynx Requirements
- Import only from `@lynx-js/react`
- Elements: `view`, `text`, `scroll-view`, `input` (not HTML div/span)
- Events: `bindtap`, `bindinput`, `bindfocus`, etc. (not onClick, onChange)
- Event data: `res.detail.value` not `e.target.value`
- Text content must be wrapped in `<text>` elements
- No `useLayoutEffect` (effects run background-only)
