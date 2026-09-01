import type { LearningTrack } from "../learningPaths";
import { LALLAS_HOUSE } from "./tracks/lallasHouse";
import { STRAIGHT_SPEECH } from "./tracks/straightSpeech";
import { KNOW_YOURSELF } from "./tracks/knowYourself";
import { UNVEILING_THE_VEILED } from "./tracks/unveilingTheVeiled";
import { THE_SEVEN_VALLEYS } from "./tracks/theSevenValleys";
import { THE_REED_COMPLAINS } from "./tracks/theReedComplains";
import { THE_BODY_OF_HATHA } from "./tracks/theBodyOfHatha";
import { HUMANENESS_AT_HAND } from "./tracks/humanenessAtHand";
import { CUTTING_THE_DIAMOND } from "./tracks/cuttingTheDiamond";

/**
 * Off-spine deepening walks compiled after the first tradition tiles shipped.
 * Psalms (`before-the-face`) lives in westernTrails.ts.
 * Spanda (`the-sacred-tremor`) is inlined in livingTrails.ts.
 */
export const DEEPENING_TRAILS: LearningTrack[] = [
  LALLAS_HOUSE,
  STRAIGHT_SPEECH,
  KNOW_YOURSELF,
  UNVEILING_THE_VEILED,
  THE_SEVEN_VALLEYS,
  THE_REED_COMPLAINS,
  THE_BODY_OF_HATHA,
  HUMANENESS_AT_HAND,
  CUTTING_THE_DIAMOND,
];
