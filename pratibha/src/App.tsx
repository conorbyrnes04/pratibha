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
  const [currentPage, setCurrentPage] = useState("login");

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

  if (!user) {
    return (
      <view style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
        <scroll-view style={{ flex: 1 }}>
          <LoginPage onLogin={() => setCurrentPage("home")} />
        </scroll-view>
      </view>
    );
  }

  return (
    <view style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
      <scroll-view style={{ flex: 1 }}>
        {currentPage === "home" && <HomePage />}
        {currentPage === "read" && <ReadPage />}
        {currentPage === "journal" && <JournalPage />}
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
