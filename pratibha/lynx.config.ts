import { defineConfig } from "@lynx-js/rspeedy";
import { pluginReactLynx } from "@lynx-js/react-rsbuild-plugin";
import { config as loadEnv } from "dotenv";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
loadEnv({ path: resolve(root, ".env") });
loadEnv({ path: resolve(root, "../.env") });

const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL || "";
const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export default defineConfig({
  plugins: [pluginReactLynx()],
  source: {
    entry: {
      index: "./src/index.tsx",
    },
    define: {
      "process.env.NEXT_PUBLIC_CONVEX_URL": JSON.stringify(convexUrl),
      "process.env.NEXT_PUBLIC_API_BASE": JSON.stringify(apiBase),
      "process.env.NEXT_PUBLIC_SITE_URL": JSON.stringify(siteUrl),
    },
  },
  server: {
    port: 3001,
  },
});
