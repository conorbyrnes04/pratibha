const config = {
  owner: "conm4n",
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
      ITSAppUsesNonExemptEncryption: false,
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
    apiBase: process.env.EXPO_PUBLIC_API_BASE ?? "https://pratibha-1.onrender.com",
    eas: {
      projectId: "7051a79c-f704-4c73-9672-e170d31f0aaf",
    },
  },
};

export default config;
