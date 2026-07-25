/**
 * Guardrail: Next.js loads `.env.local` for production builds and it overrides
 * `.env.production`. That silently bakes localhost API URLs into Cloudflare
 * deploys. Fail fast if that would happen.
 */
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const localPath = resolve(root, ".env.local");

if (existsSync(localPath)) {
  const text = readFileSync(localPath, "utf8");
  const api = (text.match(/^NEXT_PUBLIC_API_BASE=(.*)$/m)?.[1] || "").trim();
  if (/localhost|127\.0\.0\.1/i.test(api)) {
    console.error(
      [
        "Refusing to deploy: web/.env.local sets NEXT_PUBLIC_API_BASE to a local URL.",
        "Next.js applies .env.local during `next build`, which would ship localhost to production.",
        "Use web/.env.development.local for local API overrides instead, then redeploy.",
        `Current NEXT_PUBLIC_API_BASE=${api || "(empty)"}`,
      ].join("\n"),
    );
    process.exit(1);
  }
}

const prodPath = resolve(root, ".env.production");
if (!existsSync(prodPath)) {
  console.error("Missing web/.env.production — required for production API/site URLs.");
  process.exit(1);
}
const prod = readFileSync(prodPath, "utf8");
const prodApi = (prod.match(/^NEXT_PUBLIC_API_BASE=(.*)$/m)?.[1] || "").trim();
if (!prodApi || /localhost|127\.0\.0\.1/i.test(prodApi)) {
  console.error(`web/.env.production must set a public NEXT_PUBLIC_API_BASE (got ${prodApi || "empty"}).`);
  process.exit(1);
}

console.log(`predeploy ok: production API base will be ${prodApi}`);
