const { getDefaultConfig } = require("expo/metro-config");
const path = require("path");

const projectRoot = __dirname;
const sharedLib = path.resolve(projectRoot, "../web/src/lib");

const config = getDefaultConfig(projectRoot);
config.watchFolders = [sharedLib];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, "node_modules"),
  path.resolve(projectRoot, "../web/node_modules"),
];

module.exports = config;
