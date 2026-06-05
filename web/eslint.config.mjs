import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

const eslintConfig = [
  { ignores: [".next/**", "node_modules/**"] },
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    rules: {
      // react-hooks@7 introduced these stricter rules. They flag intentional
      // patterns we rely on (syncing state from the URL/storage on mount,
      // closing the mobile menu on route change, run-once fetches). Keep them
      // as warnings rather than hard errors.
      "react-hooks/set-state-in-effect": "warn",
      "react-hooks/exhaustive-deps": "warn",
    },
  },
];

export default eslintConfig;
