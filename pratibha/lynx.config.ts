import { defineConfig } from "@lynx-js/rspeedy";
import { pluginReactLynx } from "@lynx-js/react-rsbuild-plugin";

export default defineConfig({
  plugins: [pluginReactLynx()],
  // Only build lynx bundle - web env fails with WASM error on Node 20
  environments: {
    lynx: {},
  },
  source: {
    entry: {
      index: "./src/index.tsx",
    },
  },
  server: {
    port: 3000,
  },
});
