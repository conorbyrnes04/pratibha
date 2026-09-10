const config = {
  owner: "conm4n",
  name: "Pratibha",
  slug: "pratibha",
  version: "1.0.0",
  orientation: "default",
  icon: "./assets/images/icon.png",
  scheme: "pratibha",
  userInterfaceStyle: "automatic",
  // OTA so sideloaded e-ink readers (Odin, Boox) pull JS/asset changes on launch
  // instead of needing a fresh APK each time. Applies on the next cold start.
  runtimeVersion: { policy: "appVersion" as const },
  updates: {
    url: "https://u.expo.dev/7051a79c-f704-4c73-9672-e170d31f0aaf",
    checkAutomatically: "ON_LOAD",
    fallbackToCacheTimeout: 0,
  },
  splash: {
    image: "./assets/images/splash-icon.png",
    resizeMode: "contain",
    backgroundColor: "#090912",
  },
  ios: {
    supportsTablet: true,
    bundleIdentifier: "com.pratibha.app",
    infoPlist: {
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
    softwareKeyboardLayoutMode: "resize",
    predictiveBackGestureEnabled: true,
    edgeToEdgeEnabled: true,
    permissions: [
      "android.permission.INTERNET",
      "android.permission.ACCESS_NETWORK_STATE",
      "android.permission.VIBRATE",
    ],
    blockedPermissions: [
      "android.permission.READ_EXTERNAL_STORAGE",
      "android.permission.WRITE_EXTERNAL_STORAGE",
      "android.permission.SYSTEM_ALERT_WINDOW",
    ],
    allowBackup: true,
  },
  androidStatusBar: {
    backgroundColor: "#090912",
    barStyle: "light-content",
    translucent: true,
  },
  androidNavigationBar: {
    backgroundColor: "#090912",
    barStyle: "light-content",
  },
  plugins: [
    "expo-router",
    "expo-font",
    [
      "expo-navigation-bar",
      {
        backgroundColor: "#090912",
        barStyle: "light",
      },
    ],
    [
      "expo-alternate-app-icons",
      [
        {
          name: "Yantra",
          ios: "./assets/images/icons/yantra.png",
          android: {
            foregroundImage: "./assets/images/icons/yantra.png",
            backgroundColor: "#090912",
          },
        },
        {
          name: "YantraCrop",
          ios: "./assets/images/icons/yantra-crop.png",
          android: {
            foregroundImage: "./assets/images/icons/yantra-crop.png",
            backgroundColor: "#090912",
          },
        },
        {
          name: "Parchment",
          ios: "./assets/images/icons/parchment.png",
          android: {
            foregroundImage: "./assets/images/icons/parchment.png",
            backgroundColor: "#f6efe4",
          },
        },
        {
          name: "Vermillion",
          ios: "./assets/images/icons/vermillion.png",
          android: {
            foregroundImage: "./assets/images/icons/vermillion.png",
            backgroundColor: "#b85b3d",
          },
        },
        {
          name: "Lapis",
          ios: "./assets/images/icons/lapis.png",
          android: {
            foregroundImage: "./assets/images/icons/lapis.png",
            backgroundColor: "#324867",
          },
        },
      ],
    ],
  ],
  experiments: {
    typedRoutes: true,
  },
  extra: {
    apiBase: process.env.EXPO_PUBLIC_API_BASE ?? "https://pratibha-1.onrender.com",
    // Generated collection art (Red Book / thangka) is served by the web frontend,
    // not the Render backend — mobile fetches it straight from the site.
    webBase: process.env.EXPO_PUBLIC_WEB_BASE ?? "https://pratibha.agniagama.com",
    convexUrl: process.env.EXPO_PUBLIC_CONVEX_URL ?? "https://giant-lapwing-264.convex.cloud",
    eas: {
      projectId: "7051a79c-f704-4c73-9672-e170d31f0aaf",
    },
  },
};

export default config;
