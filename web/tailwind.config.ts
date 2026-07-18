import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      // Default Tailwind xs/sm are too small for long-form reading on this UI.
      fontSize: {
        xs: ["0.875rem", { lineHeight: "1.4" }],
        sm: ["1.05rem", { lineHeight: "1.55" }],
        base: ["1.15rem", { lineHeight: "1.65" }],
        lg: ["1.3rem", { lineHeight: "1.7" }],
        xl: ["1.45rem", { lineHeight: "1.65" }],
      },
    },
  },
  plugins: [],
};
export default config;
