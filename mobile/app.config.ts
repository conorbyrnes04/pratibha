const config = {
  name: "Pratibha",
  slug: "pratibha",
  version: "1.0.0",
  orientation: "portrait",
  icon: "./assets/images/icon.png",
  scheme: "pratibha",
  userInterfaceStyle: "dark",
  splash: {
    image: "./assets/images/splash-icon.png",
    resizeMode: "contain",
    backgroundColor: "#090912",
  },
  ios: {
    supportsTablet: true,
    bundleIdentifier: "com.pratibha.app",
    infoPlist: {
      NSAppTransportSecurity: {
        NSAllowsArbitraryLoads: true,
      },
    },
  },
  android: {
    adaptiveIcon: {
      foregroundImage: "./assets/images/android-icon-foreground.png",
      monochromeImage: "./assets/images/android-icon-monochrome.png",
      backgroundColor: "#090912",
    },
    package: "com.pratibha.app",
  },
  plugins: ["expo-router"],
  experiments: {
    typedRoutes: true,
  },
  extra: {
    apiBase: process.env.EXPO_PUBLIC_API_BASE ?? "http://127.0.0.1:8000",
  },
};

export default config;
