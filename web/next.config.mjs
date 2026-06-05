import { fileURLToPath } from "node:url";
import { dirname } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Pin the workspace root so Turbopack does not pick up the stray
  // package-lock.json in the home directory.
  turbopack: {
    root: __dirname,
  },
  // The app is opened at 127.0.0.1:3000 while the dev server's origin is
  // localhost:3000. Next 16 blocks cross-origin dev resources (HMR/runtime)
  // by default, which silently prevents client hydration. Allow both hosts.
  allowedDevOrigins: ["127.0.0.1", "localhost"],
};

export default nextConfig;
