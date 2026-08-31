import { useCallback, useState } from "@lynx-js/react";
import { ConvexProvider } from "./convex/ConvexProvider";
import { AuthProvider, useAuth } from "./auth/AuthProvider";
import { Navigation } from "./components/Navigation";
import { HomePage } from "./pages/HomePage";
import { LoginPage } from "./pages/LoginPage";
import { JournalPage } from "./pages/JournalPage";
import { ReadPage } from "./pages/ReadPage";
import { ChatPage } from "./pages/ChatPage";
import { LearnPage } from "./pages/LearnPage";
import { LexiconPage } from "./pages/LexiconPage";
import { SourcesPage } from "./pages/SourcesPage";
import { ManuscriptPage } from "./pages/ManuscriptPage";

function AppContent() {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState("home");
  const [openVerseId, setOpenVerseId] = useState<string | null>(null);

  const onNavigate = useCallback((page: string) => {
    "background only";
    if (page !== "read") setOpenVerseId(null);
    setCurrentPage(page);
  }, []);

  const openVerse = useCallback((verseId: string) => {
    "background only";
    setOpenVerseId(verseId);
    setCurrentPage("read");
  }, []);

  if (loading) {
    return (
      <view
        style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "#0a0a0f",
        }}
      >
        <text style={{ color: "#f0c979", fontSize: 16 }}>Loading...</text>
      </view>
    );
  }

  return (
    <view style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      <Navigation currentPage={currentPage} onNavigate={onNavigate} signedIn={Boolean(user)} />
      <scroll-view scroll-y style={{ flex: 1 }}>
        {currentPage === "login" && <LoginPage onLogin={() => onNavigate("home")} />}
        {currentPage === "home" && <HomePage onNavigate={onNavigate} />}
        {currentPage === "read" && <ReadPage openVerseId={openVerseId} />}
        {currentPage === "chat" && <ChatPage />}
        {currentPage === "learn" && <LearnPage />}
        {currentPage === "lexicon" && <LexiconPage />}
        {currentPage === "journal" && <JournalPage />}
        {currentPage === "manuscript" && <ManuscriptPage onOpenVerse={openVerse} />}
        {currentPage === "sources" && <SourcesPage />}
      </scroll-view>
    </view>
  );
}

export function App() {
  return (
    <page>
      <ConvexProvider>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </ConvexProvider>
    </page>
  );
}
