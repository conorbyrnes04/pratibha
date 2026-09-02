import type { Locale } from "../locales";
import type { Messages } from "./en";
import { en } from "./en";

export { en };
export type { Messages };

export async function loadCatalog(locale: Locale): Promise<Messages> {
  switch (locale) {
    case "fr":
      return (await import("./fr")).fr;
    case "es":
      return (await import("./es")).es;
    case "pt-BR":
      return (await import("./pt-BR")).ptBR;
    case "zh":
      return (await import("./zh")).zh;
    case "ru":
      return (await import("./ru")).ru;
    case "ja":
      return (await import("./ja")).ja;
    case "ar":
      return (await import("./ar")).ar;
    default:
      return en;
  }
}
