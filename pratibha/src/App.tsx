import React, { useState, useEffect } from "@lynx-js/react";
import { ConvexProvider } from "./convex/ConvexProvider";
import { AuthProvider, useAuth } from "./auth/AuthProvider";
import { Navigation } from "./components/Navigation";
import { HomePage } from "./pages/HomePage";
import { LoginPage } from "./pages/LoginPage";
import { JournalPage } from "./pages/JournalPage";
import { ReadPage } from "./pages/ReadPage";

function AppContent() {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState("home");

  useEffect(() => {
    if (user && currentPage === "login") {
      setCurrentPage("home");
    }
  }, [user, currentPage]);

  if (loading) {
    return (
      <view style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#0a0a0f" }}>
        <text style={{ color: "#f0c979", fontSize: 16 }}>Loading...</text>
      </view>
    );
  }

  // Render login immediately when no user, regardless of currentPage state
  if (!user) {
    return <LoginPage onLogin={() => setCurrentPage("home")} />;
  }

  return (
    <view style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      {currentPage === "home" && <HomePage />}
      {currentPage === "read" && <ReadPage />}
      {currentPage === "journal" && <JournalPage />}
      <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
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
