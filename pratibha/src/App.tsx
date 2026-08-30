import React from "react";
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

function AppContent() {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = React.useState("home");

  if (loading) {
    return (
      <view style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#0a0a0f" }}>
        <text style={{ color: "#f0c979", fontSize: 16 }}>Loading...</text>
      </view>
    );
  }

  return (
    <view style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      <Navigation currentPage={currentPage} onNavigate={setCurrentPage} signedIn={Boolean(user)} />
      <scroll-view style={{ flex: 1 }}>
        {currentPage === "login" && <LoginPage onLogin={() => setCurrentPage("home")} />}
        {currentPage === "home" && <HomePage />}
        {currentPage === "read" && <ReadPage />}
        {currentPage === "chat" && <ChatPage />}
        {currentPage === "learn" && <LearnPage />}
        {currentPage === "lexicon" && <LexiconPage />}
        {currentPage === "journal" && <JournalPage />}
        {currentPage === "sources" && <SourcesPage />}
      </scroll-view>
    </view>
  );
}

export default function App() {
  return (
    <ConvexProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ConvexProvider>
  );
}
