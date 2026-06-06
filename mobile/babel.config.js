module.exports = function (api) {
  api.cache(true);
  return {
    presets: ["babel-preset-expo"],
    plugins: [
      [
        "module-resolver",
        {
          alias: {
            "@": "./",
            "@shared": "../web/src/lib",
          },
          extensions: [".ts", ".tsx", ".js", ".jsx"],
        },
      ],
    ],
  };
};
