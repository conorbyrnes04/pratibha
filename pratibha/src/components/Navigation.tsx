import { C } from "../lib/theme";

interface NavigationProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  signedIn?: boolean;
}

const WALK = [
  { id: "home", label: "Today" },
  { id: "learn", label: "Path" },
  { id: "read", label: "Library" },
  { id: "manuscript", label: "Mine" },
];

const STUDY = [
  { id: "chat", label: "Chat" },
  { id: "journal", label: "Journal" },
  { id: "lexicon", label: "Lexicon" },
  { id: "sources", label: "Sources" },
];

const PRIMARY = [...WALK, ...STUDY];

export function Navigation({ currentPage, onNavigate, signedIn }: NavigationProps) {
  const pages = [
    ...PRIMARY,
    { id: signedIn ? "home" : "login", label: signedIn ? "Account" : "Sign in", account: true },
  ];

  return (
    <view
      style={{
        backgroundColor: C.cardAlt,
        paddingTop: 14,
        paddingBottom: 12,
        paddingLeft: 14,
        paddingRight: 14,
        borderBottomWidth: "1px",
        borderBottomColor: C.line,
      }}
    >
      <text style={{ color: C.gold, fontSize: 20, fontWeight: "bold", marginBottom: 10 }}>Pratibha</text>
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: "8px" }}>
        {pages.map((page) => {
          const active = currentPage === page.id && !("account" in page && page.account);
          return (
            <view
              key={page.label}
              bindtap={() => onNavigate(page.id)}
              style={{
                paddingTop: 6,
                paddingBottom: 6,
                paddingLeft: 12,
                paddingRight: 12,
                backgroundColor: active ? C.gold : "transparent",
                borderRadius: 4,
              }}
            >
              <text
                style={{
                  color: active ? "#000" : "#ccc",
                  fontSize: 13,
                  fontWeight: active ? "600" : "normal",
                }}
              >
                {page.label}
              </text>
            </view>
          );
        })}
      </view>
    </view>
  );
}
