import React from "react";
import { ConvexProvider } from "./convex/ConvexProvider";
import { AuthProvider } from "./auth/AuthProvider";
import { Navigation } from "./components/Navigation";
import { HomePage } from "./pages/HomePage";

export default function App() {
  const [currentPage, setCurrentPage] = React.useState("home");

  return (
    <ConvexProvider>
      <AuthProvider>
        <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh", backgroundColor: "#0a0a0f" }}>
          <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
          <main style={{ flex: 1, padding: "20px" }}>
            {currentPage === "home" && <HomePage />}
            {currentPage === "login" && <div style={{ color: "#fff" }}>Login (Coming Soon)</div>}
            {currentPage === "journal" && <div style={{ color: "#fff" }}>Journal (Coming Soon)</div>}
          </main>
        </div>
      </AuthProvider>
    </ConvexProvider>
  );
}
