# Pratibha iOS App Store Submission Guide

## Current Status
✅ App configured with bundle ID: `com.pratibha.app`  
✅ EAS project ID: `7051a79c-f704-4c73-9672-e170d31f0aaf`  
✅ Production API defaults set  
✅ Convex Auth with Google OAuth via expo-web-browser  
✅ App Transport Security enabled (NSAllowsArbitraryLoads removed)  
✅ Dark splash screen and icon configured  

## Prerequisites

### 1. Apple Developer Program Enrollment ($99/year)
- Enroll at [developer.apple.com/programs](https://developer.apple.com/programs)
- Decide whether to enroll as:
  - **Individual**: Conor Byrnes (personal account)
  - **Organization**: Agni Agama (if business entity exists)
- Complete enrollment and wait for approval (~24-48 hours)
- Note your **Team ID** once approved

### 2. Google Cloud OAuth Configuration
The mobile app uses the existing Web application client (ID starts with `999545287985`) for Google sign-in.

**Action needed:**
- Go to [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials
- Select the existing Web client
- Verify authorized redirect URIs include:
  - `https://energized-armadillo-158.convex.site/api/auth/callback/google` (already configured)
- **Add iOS bundle ID** (optional but recommended):
  - Create a new iOS OAuth client with bundle ID: `com.pratibha.app`
  - Add custom URL scheme: `pratibha://`
  - Keep both Web and iOS clients active

## Build Configuration

### Update eas.json
Before building, update the placeholder values in `mobile/eas.json`:

\`\`\`json
"submit": {
  "production": {
    "ios": {
      "appleId": "conor@agniagama.com",
      "ascAppId": "YOUR_APP_STORE_CONNECT_APP_ID",
      "appleTeamId": "YOUR_APPLE_TEAM_ID"
    }
  }
}
\`\`\`

### Build Commands

**Build for TestFlight/App Store:**
\`\`\`bash
cd mobile
eas build --platform ios --profile production
\`\`\`

This will:
- Auto-increment build number
- Create a production-signed IPA
- Upload to EAS servers

**Submit to App Store:**
\`\`\`bash
eas submit --platform ios --profile production
\`\`\`

## App Store Connect Setup

### 1. Create App Record
- Go to [App Store Connect](https://appstoreconnect.apple.com)
- Navigate to **My Apps** → **+** → **New App**
- Fill in:
  - **Platform**: iOS
  - **Name**: Pratibha
  - **Primary Language**: English (U.S.)
  - **Bundle ID**: Select `com.pratibha.app` (from your certificate)
  - **SKU**: `pratibha-ios` (or any unique identifier)
  - **User Access**: Full Access

### 2. App Information
- **Subtitle** (30 chars): "Wisdom texts for contemplation"
- **Category**: Education (Primary), Lifestyle (Secondary)
- **Content Rights**: You own or have rights to use
- **Age Rating**: 4+ (no objectionable content)

### 3. Privacy & URLs
- **Privacy Policy URL**: `https://pratibha.agniagama.com/privacy`
- **Support URL**: `https://pratibha.agniagama.com`
- **Marketing URL** (optional): `https://pratibha.agniagama.com`

### 4. App Privacy Details
When prompted, answer Apple's privacy questionnaire:
- **Data Collection**:
  - Email address (for account creation)
  - Optional: Name (from Google OAuth)
  - Journal notes (stored in Convex, linked to user account)
- **Data Use**:
  - App functionality (authentication, saving user content)
  - NOT used for tracking, advertising, or analytics
- **Data Sharing**: None (we do not sell or share data with third parties)
- **Account Required**: Yes (for journal and progress tracking)

## App Store Listing

### Promotional Text (170 chars)
> Explore timeless wisdom from Buddhism, Taoism, Hinduism, and mystical traditions. Read verses, reflect with AI guidance, and journal your contemplative practice.

### Description
\`\`\`
Pratibha is a contemplative companion for studying world wisdom texts.

EXPLORE SACRED TEXTS
• Verses from the Dhammapada, Tao Te Ching, Upanishads, Bhagavad Gita
• Sufi poetry, Christian mystics, and other contemplative traditions
• Daily verse recommendations for sustained practice

REFLECT WITH AI GUIDANCE
• Ask questions about verses and receive thoughtful responses
• Compare teachings across traditions
• Explore layers of meaning in ancient texts

JOURNAL YOUR INSIGHTS
• Save reflections tied to specific verses
• Track your contemplative practice over time
• Build a personal library of wisdom

Perfect for students of philosophy, meditation practitioners, and anyone seeking deeper understanding of humanity's spiritual traditions.

No ads. No distractions. Just texts, reflection, and space for contemplation.
\`\`\`

### Keywords (100 chars max, comma-separated)
\`\`\`
wisdom,buddhism,taoism,meditation,philosophy,dharma,contemplation,spirituality,sacred texts,upanishad
\`\`\`

## Screenshots & Assets

### Required Screenshots
You'll need screenshots for:
- **6.7" display** (iPhone 15 Pro Max): 1290 x 2796 pixels (3-10 screenshots)
- **6.1" display** (iPhone 15 Pro): 1179 x 2556 pixels (3-10 screenshots)

**Recommended screens to capture:**
1. Daily verse view with beautiful typography
2. Verse detail with layers/commentary
3. Chat/Ask Pratibha interface
4. Journal notes list
5. Learning paths overview

**Visual style:**
- Dark theme (#090912 background) as designed
- Show actual content (real verses, not lorem ipsum)
- Keep UI clean and minimal (matches app aesthetic)

### App Preview Video (Optional)
- 15-30 second video showing app flow
- Same size requirements as screenshots

## TestFlight Testing

### Internal Testing
Once your first build is uploaded:
1. Go to **App Store Connect** → **TestFlight**
2. Add internal testers (up to 100, must have Apple IDs on your team)
3. They can install immediately (no review required)

### External Testing (Recommended)
1. Create an external test group
2. Add up to 10,000 testers via email
3. First build requires **Beta App Review** (~24-48 hours)
4. Test authentication, verse reading, chat, and journal features
5. Gather feedback on any crashes or UX issues

## Final Submission

### Version Information
- **Version**: 1.0.0
- **Build**: Auto-incremented by EAS
- **Copyright**: 2026 Agni Agama (or Conor Byrnes)

### What's New in This Version
\`\`\`
Initial release of Pratibha for iOS.

• Browse verses from Buddhism, Taoism, Hinduism, and mystical traditions
• Ask questions and receive AI-powered insights
• Journal your reflections and track contemplative practice
• Follow guided learning paths through wisdom traditions
\`\`\`

### Review Notes (for Apple reviewers)
\`\`\`
Pratibha is an educational app for studying world wisdom texts.

TEST ACCOUNT (if required):
Email: [create a test account]
Password: [provide test credentials]

KEY FEATURES TO TEST:
1. Browse daily verse and verse library (no account needed)
2. Sign in with Google or email/password
3. Ask questions about verses (chat feature)
4. Save journal notes
5. Follow learning paths

The app connects to:
- Pratibha API (https://pratibha-1.onrender.com) for verse content
- Convex backend (https://energized-armadillo-158.convex.cloud) for authentication and user data

No in-app purchases or subscriptions in this version.
\`\`\`

## Post-Submission

### Review Timeline
- Initial review: 1-3 days typically
- Rejections require fixes and resubmission
- Common rejection reasons:
  - Missing privacy policy
  - Broken authentication flows
  - App crashes on launch
  - Missing screenshots or metadata

### After Approval
- App goes live on App Store
- Monitor crash reports in App Store Connect
- Respond to user reviews
- Plan updates based on feedback

## Future Considerations

### Features Not in 1.0
- In-app purchases / membership tiers
- Push notifications for daily verses
- Offline mode for verses
- Social features / circles

### Version Updates
For subsequent releases:
\`\`\`bash
# Update version in app.config.ts
# Build and submit
eas build --platform ios --profile production --auto-submit
\`\`\`

## Technical Notes

### Environment Variables
Production defaults are in `app.config.ts`:
- `EXPO_PUBLIC_API_BASE`: `https://pratibha-1.onrender.com`
- `EXPO_PUBLIC_CONVEX_URL`: `https://energized-armadillo-158.convex.cloud`

### Google OAuth Flow
1. User taps "Sign in with Google"
2. `expo-web-browser` opens: `https://energized-armadillo-158.convex.site/api/auth/signin/google?redirect=pratibha://`
3. User completes Google OAuth in browser
4. Redirects to `pratibha://` with token
5. App extracts token and calls `convex.setAuth(token)`
6. Token persisted in AsyncStorage

### Convex Deployment
If you modify Convex functions (auth, schema, etc.):
\`\`\`bash
cd web
npx convex deploy --prod
\`\`\`

Do NOT deploy from the `pratibha/` (Lynx) folder — it has a different schema.

## Resources

- [Expo EAS Documentation](https://docs.expo.dev/eas/)
- [App Store Connect](https://appstoreconnect.apple.com)
- [Apple Developer Portal](https://developer.apple.com)
- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/ios)

## Support

For questions or issues:
- Technical: Check mobile/README.md or mobile/IOS_HANDOFF.md
- App Store: [Apple Developer Support](https://developer.apple.com/support/)
- Pratibha-specific: conor@agniagama.com
