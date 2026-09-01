import type { Locale } from "../locales";
import type { Messages } from "./en";
import { en } from "./en";
import { ar } from "./ar";
import { es } from "./es";
import { fr } from "./fr";
import { ja } from "./ja";
import { ptBR } from "./pt-BR";
import { ru } from "./ru";
import { zh } from "./zh";

export const catalogs: Record<Locale, Messages> = {
  en,
  fr,
  es,
  "pt-BR": ptBR,
  zh,
  ru,
  ja,
  ar,
};

export { en };
export type { Messages };
