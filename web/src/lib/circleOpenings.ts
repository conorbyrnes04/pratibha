import { FEATURED_CIRCLE_DOORS } from "@/lib/circleVerses";

export type CircleOpening = {
  id: string;
  label: string;
  body: string;
};

/** Editorial first lights — not student voices. Shown until a verse has offerings. */
export const CIRCLE_OPENINGS: CircleOpening[] = [
  {
    id: "siva_sutra.ss_i_1",
    label: "Consciousness is the Self",
    body: "Stop treating awareness as something you own. The sūtra names it as the ground in which the owner appears. Notice the lighting, not the furniture, and say what that noticing does.",
  },
  {
    id: "siva_sutra.ss_i_2",
    label: "Knowledge is bondage",
    body: "The knowledge that binds is the story that says you are a knower facing a world. Where did a piece of knowing tighten you today? Offer that, not a definition.",
  },
  {
    id: "siva_sutra.ss_i_5",
    label: "The surge of awareness is Bhairava",
    body: "Bhairava is not a mood you manufacture. It is the surge already running through perception. Catch one pulse — startle, beauty, anger — and write from inside it, not about it.",
  },
  {
    id: "pratyabhijnahrdayam.phr_001",
    label: "Consciousness, autonomous",
    body: "Citi is free, and the universe is its work. If that is true, bondage is a contraction you are performing. Name the contraction you are still calling fate.",
  },
  {
    id: "pratyabhijnahrdayam.phr_013",
    label: "Pratyabhijñāhṛdayam 13",
    body: "Recognition is not an attainment. It is the mind turning and finding it was never other than what it sought. Where are you still approaching as a seeker?",
  },
  {
    id: "pratyabhijnahrdayam.phr_020",
    label: "Pratyabhijñāhṛdayam 20",
    body: "The last teaching is ordinary: sovereignty lived inside a day. What would it mean to finish this hour without seizing the fruit of it?",
  },
  {
    id: "vijnana_bhairava.yukti_001",
    label: "Vijñāna Bhairava 1",
    body: "The first doorway is the turn of the breath. Not a special breath — this one. Sit at the pause and write only what is actually there.",
  },
  {
    id: "vijnana_bhairava.yukti_002",
    label: "Vijñāna Bhairava 2",
    body: "A second door, same house. If method becomes a project, you have left the yukti. What method are you still using as an identity?",
  },
  {
    id: "bhagavad_gita.bg_02_47",
    label: "Your claim is to action alone",
    body: "You have a right to the act, never to its fruits. Name one action you are still holding hostage to an outcome, and what happens if you put the fruit down.",
  },
  {
    id: "bhagavad_gita.bg_06_35",
    label: "Practice and dispassion",
    body: "The restless mind is trained by practice and by not feeding it. Which of those two are you pretending to do while doing the other?",
  },
  {
    id: "epictetus_works.epi_enc_001",
    label: "The division that liberates",
    body: "Some things are up to you; some are not. The Enchiridion opens by splitting the world. Draw the line through one event from this week, and stand on the side that is yours.",
  },
  {
    id: "tao_te_ching.ttc_md_002",
    label: "The use of absence",
    body: "The hub is empty, and that is why the cart moves. Where are you stuffing the hollow with commentary? Leave one absence unnamed, then write around it.",
  },
];

const OPENING_BY_ID = new Map(CIRCLE_OPENINGS.map((row) => [row.id, row]));

export function circleOpeningFor(verseId: string): CircleOpening | undefined {
  return OPENING_BY_ID.get(verseId);
}

export function featuredDoorLabel(verseId: string): string | undefined {
  return FEATURED_CIRCLE_DOORS.find((door) => door.id === verseId)?.label;
}
