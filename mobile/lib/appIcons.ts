export type AppIconId = "default" | "Yantra" | "YantraCrop" | "Parchment" | "Vermillion" | "Lapis";

export type AppIconOption = {
  id: AppIconId;
  /** PascalCase name for expo-alternate-app-icons, or null for the default icon. */
  nativeName: string | null;
  label: string;
  hint: string;
  preview: number;
  background: string;
};

export const APP_ICONS: AppIconOption[] = [
  {
    id: "default",
    nativeName: null,
    label: "Seal",
    hint: "Eight-petal seal on field",
    preview: require("../assets/images/icons/seal-192.png"),
    background: "#090912",
  },
  {
    id: "Yantra",
    nativeName: "Yantra",
    label: "Yantra",
    hint: "Full yantra with gates",
    preview: require("../assets/images/icons/yantra-192.png"),
    background: "#090912",
  },
  {
    id: "YantraCrop",
    nativeName: "YantraCrop",
    label: "Yantra crop",
    hint: "Tight to the lotus ring",
    preview: require("../assets/images/icons/yantra-crop-192.png"),
    background: "#090912",
  },
  {
    id: "Parchment",
    nativeName: "Parchment",
    label: "Parchment",
    hint: "Seal on parchment",
    preview: require("../assets/images/icons/parchment-192.png"),
    background: "#f6efe4",
  },
  {
    id: "Vermillion",
    nativeName: "Vermillion",
    label: "Vermillion",
    hint: "White seal on vermillion",
    preview: require("../assets/images/icons/vermillion-192.png"),
    background: "#b85b3d",
  },
  {
    id: "Lapis",
    nativeName: "Lapis",
    label: "Lapis",
    hint: "Seal on lapis",
    preview: require("../assets/images/icons/lapis-192.png"),
    background: "#324867",
  },
];
