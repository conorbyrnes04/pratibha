import React from "@lynx-js/react";

interface NavigationProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function Navigation({ currentPage, onNavigate }: NavigationProps) {
  const pages = [
    { id: "home", label: "Today" },
    { id: "read", label: "Read" },
    { id: "journal", label: "Journal" },
  ];

  return (
    <view
      style={{
        flexDirection: "row",
        backgroundColor: "#1a1a2e",
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: "#333",
        gap: 12,
      }}
    >
      <text style={{ color: "#f0c979", fontSize: 20, fontWeight: "bold", marginRight: "auto" }}>
        Pratibha
      </text>
      {pages.map((page) => (
        <view
          key={page.id}
          onClick={() => onNavigate(page.id)}
          style={{
            paddingVertical: 8,
            paddingHorizontal: 16,
            backgroundColor: currentPage === page.id ? "#f0c979" : "transparent",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          <text
            style={{
              color: currentPage === page.id ? "#000" : "#ccc",
              fontSize: 14,
              fontWeight: currentPage === page.id ? "600" : "normal",
            }}
          >
            {page.label}
          </text>
        </view>
      ))}
    </view>
  );
}
