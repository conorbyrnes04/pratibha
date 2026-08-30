import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy - Pratibha",
  description: "Privacy policy for Pratibha - how we handle your data",
};

export default function PrivacyPage() {
  return (
    <div className="container mx-auto max-w-4xl px-4 py-16">
      <h1 className="mb-8 text-4xl font-bold">Privacy Policy</h1>
      
      <div className="prose prose-invert max-w-none space-y-6">
        <p className="text-muted-foreground">
          <strong>Last Updated:</strong> August 30, 2026
        </p>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Introduction</h2>
          <p>
            Pratibha is a contemplative companion for studying world wisdom texts. 
            This privacy policy explains how we collect, use, and protect your personal information 
            when you use our website and mobile applications.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Information We Collect</h2>
          
          <h3 className="text-xl font-semibold mt-6 mb-3">Account Information</h3>
          <p>
            When you create an account, we collect:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Email address</strong> - Required for account creation and authentication</li>
            <li><strong>Password</strong> - Stored securely using industry-standard encryption (if using email/password authentication)</li>
            <li><strong>Name</strong> - Optional, provided when signing in with Google</li>
          </ul>

          <h3 className="text-xl font-semibold mt-6 mb-3">User-Generated Content</h3>
          <p>
            When you use Pratibha, we store:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Journal notes</strong> - Your personal reflections and insights on wisdom texts</li>
            <li><strong>Learning progress</strong> - Your completion status for learning paths and study sessions</li>
            <li><strong>Chat history</strong> - Conversations with the AI assistant about verses and texts</li>
            <li><strong>Verse likes and bookmarks</strong> - Content you've marked for future reference</li>
          </ul>

          <h3 className="text-xl font-semibold mt-6 mb-3">OAuth Authentication</h3>
          <p>
            If you sign in with Google, we receive basic profile information (email, name) through Google's OAuth service. 
            We do not have access to your Google password or other Google account data.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">How We Use Your Information</h2>
          <p>
            We use your information solely for providing and improving the Pratibha service:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Authentication</strong> - Verifying your identity and securing your account</li>
            <li><strong>App functionality</strong> - Storing your journal entries, progress, and preferences</li>
            <li><strong>AI features</strong> - Providing personalized responses to your questions about wisdom texts</li>
            <li><strong>Service improvements</strong> - Understanding how features are used to enhance the experience</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Data Storage and Security</h2>
          <p>
            Your data is stored securely using:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Convex</strong> - A secure, serverless backend platform for user accounts, journal notes, and learning progress</li>
            <li><strong>Encryption</strong> - All data is transmitted over HTTPS and stored with encryption at rest</li>
            <li><strong>Access controls</strong> - Only you can access your personal journal notes and progress data</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">What We Don't Do</h2>
          <p>
            Pratibha is committed to respecting your privacy:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>We <strong>do not sell</strong> your personal information to third parties</li>
            <li>We <strong>do not use</strong> your data for advertising or marketing purposes</li>
            <li>We <strong>do not track</strong> you across other websites or apps</li>
            <li>We <strong>do not share</strong> your journal entries or personal reflections with anyone</li>
            <li>We <strong>do not use</strong> third-party analytics or tracking tools</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Third-Party Services</h2>
          <p>
            Pratibha integrates with the following third-party services:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Google OAuth</strong> - For optional sign-in with Google (governed by Google's Privacy Policy)</li>
            <li><strong>Convex</strong> - For secure data storage (governed by Convex's Privacy Policy)</li>
          </ul>
          <p className="mt-4">
            These services have their own privacy policies, and we recommend reviewing them.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Your Rights</h2>
          <p>
            You have the right to:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Access</strong> your personal data - View all information we have about you</li>
            <li><strong>Delete</strong> your account - Remove all your data from our systems</li>
            <li><strong>Export</strong> your data - Download your journal entries and other content</li>
            <li><strong>Correct</strong> inaccuracies - Update your account information at any time</li>
          </ul>
          <p className="mt-4">
            To exercise these rights, please contact us at the email below.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Children's Privacy</h2>
          <p>
            Pratibha is not intended for children under 13. We do not knowingly collect personal 
            information from children under 13. If you believe we have collected information from 
            a child under 13, please contact us immediately.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Changes to This Policy</h2>
          <p>
            We may update this privacy policy from time to time. We will notify you of any 
            significant changes by posting the new policy on this page and updating the 
            "Last Updated" date at the top.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mt-8 mb-4">Contact Us</h2>
          <p>
            If you have questions about this privacy policy or how we handle your data, please contact us:
          </p>
          <ul className="list-none space-y-2 mt-4">
            <li><strong>Email:</strong> conor@agniagama.com</li>
            <li><strong>Website:</strong> <a href="https://pratibha.agniagama.com" className="text-accent hover:underline">pratibha.agniagama.com</a></li>
          </ul>
        </section>

        <section className="border-t border-border pt-8 mt-12">
          <p className="text-sm text-muted-foreground">
            Pratibha is developed and maintained by Ape Kode LLC. This privacy policy applies to 
            both the web application at pratibha.agniagama.com and the iOS mobile application.
          </p>
        </section>
      </div>
    </div>
  );
}
