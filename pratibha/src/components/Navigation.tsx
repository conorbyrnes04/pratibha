import React from "@lynx-js/react";

interface NavigationProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function Navigation({ currentPage, onNavigate }: NavigationProps) {
  const pages = [
    { id: "home", label: "TODAY" },
    { id: "read", label: "READ" },
    { id: "journal", label: "JOURNAL" },
  ];

  return (
    <view
      style={{
        display: "linear",
        flexDirection: "row",
        backgroundColor: "#0a0a0f",
        borderTopWidth: 1,
        borderTopColor: "#333",
        height: 60,
      }}
    >
      {pages.map((page) => {
        const isActive = currentPage === page.id;
        return (
          <view
            key={page.id}
            bindtap={() => onNavigate(page.id)}
            style={{
              flex: 1,
              justifyContent: "center",
              alignItems: "center",
              borderTopWidth: isActive ? 2 : 0,
              borderTopColor: isActive ? "#c9a227" : "transparent",
            }}
          >
            <text
              style={{
                color: isActive ? "#c9a227" : "#666",
                fontSize: 11,
                fontWeight: isActive ? "600" : "normal",
                letterSpacing: 1,
              }}
            >
              {page.label}
            </text>
          </view>
        );
      })}
    </view>
  );
}
