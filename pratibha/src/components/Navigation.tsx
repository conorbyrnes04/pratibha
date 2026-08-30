import React from "react";

interface NavigationProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function Navigation({ currentPage, onNavigate }: NavigationProps) {
  const pages = [
    { id: "home", label: "Home" },
    { id: "login", label: "Login" },
    { id: "journal", label: "Journal" },
  ];

  return (
    <nav
      style={{
        display: "flex",
        gap: "16px",
        backgroundColor: "#1a1a2e",
        padding: "16px",
        borderBottom: "1px solid #333",
      }}
    >
      {pages.map((page) => (
        <button
          key={page.id}
          onClick={() => onNavigate(page.id)}
          style={{
            background: currentPage === page.id ? "#f0c979" : "#666",
            color: currentPage === page.id ? "#000" : "#fff",
            border: "none",
            padding: "8px 16px",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "14px",
          }}
        >
          {page.label}
        </button>
      ))}
    </nav>
  );
}
