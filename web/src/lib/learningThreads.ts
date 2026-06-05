/** A thread is one theme traced across traditions — a horizontal cut through
 *  the vertical paths. Each bead links to an existing path step. */
export type ThreadStepRef = {
  id: string;
  /** Tradition or text name shown on the bead. */
  tradition: string;
  /** One line — the thread's voice at this bead. */
  insight: string;
  trackId: string;
  stepId: string;
  passageId: string;
};

export type LearningThread = {
  id: string;
  title: string;
  subtitle: string;
  /** Single character or short glyph for the bindu. */
  glyph: string;
  /** Hue shift for this thread's accent (degrees). */
  hue: number;
  steps: ThreadStepRef[];
};

export const LEARNING_THREADS: LearningThread[] = [
  {
    id: "the-gap",
    title: "The Gap",
    subtitle: "The madhya — the still hinge between every two states",
    glyph: "○",
    hue: 42,
    steps: [
      {
        id: "gap-vbt-center",
        tradition: "Vijñāna Bhairava",
        insight: "Between out-breath and in-breath, śakti rests in the Center.",
        trackId: "the-112-doorways",
        stepId: "vbt-the-center",
        passageId: "vijnana_bhairava.yukti_002",
      },
      {
        id: "gap-vbt-seam",
        tradition: "Vijñāna Bhairava",
        insight: "Between any two cognitions, take refuge in the seam.",
        trackId: "the-112-doorways",
        stepId: "vbt-seam-between",
        passageId: "vijnana_bhairava.yukti_034",
      },
      {
        id: "gap-phr-middle",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Unfold the middle — bliss hides in the gap of the breath.",
        trackId: "heart-of-recognition",
        stepId: "phr-the-middle",
        passageId: "pratyabhijnahrdayam.phr_017",
      },
      {
        id: "gap-mandukya",
        tradition: "Vijñāna Bhairava · turīya",
        insight: "At the lip of sleep — the wakeful Fourth shows.",
        trackId: "the-112-doorways",
        stepId: "vbt-threshold-sleep",
        passageId: "vijnana_bhairava.yukti_047",
      },
    ],
  },
  {
    id: "becoming-light",
    title: "Becoming Light",
    subtitle: "You cannot see the sun unless you have first become sunlike",
    glyph: "☀",
    hue: 28,
    steps: [
      {
        id: "light-plotinus",
        tradition: "Plotinus",
        insight: "Never cease chiselling your statue until virtue shines.",
        trackId: "the-one-and-the-many",
        stepId: "om-become-sunlike",
        passageId: "plotinus_enneads.enn_i_6_09",
      },
      {
        id: "light-yh",
        tradition: "Yoginīhṛdaya",
        insight: "Re-find the whole diagram in the body; climb to the partless summit.",
        trackId: "descent-of-the-cakra",
        stepId: "yh-interiorize",
        passageId: "yoginihrdaya.yh_011",
      },
      {
        id: "light-ss",
        tradition: "Śiva Sūtra",
        insight: "The surge of awareness itself is Bhairava.",
        trackId: "three-doors-of-shiva",
        stepId: "ss-udyamo-bhairavah",
        passageId: "siva_sutra.ss_i_5",
      },
    ],
  },
  {
    id: "emanation-return",
    title: "Emanation & Return",
    subtitle: "The One overflows into the many — and the many remember",
    glyph: "∞",
    hue: 195,
    steps: [
      {
        id: "er-plotinus",
        tradition: "Plotinus",
        insight: "The One overflows; Intellect turns back and beholds its source.",
        trackId: "the-one-and-the-many",
        stepId: "om-overflow",
        passageId: "plotinus_enneads.enn_v_2_01",
      },
      {
        id: "er-phr",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "She unfolds the universe on her own canvas, by free will.",
        trackId: "heart-of-recognition",
        stepId: "phr-free-unfolding",
        passageId: "pratyabhijnahrdayam.phr_002",
      },
      {
        id: "er-tao",
        tradition: "Tao Te Ching",
        insight: "The ten thousand things arise together — I watch them return.",
        trackId: "the-one-and-the-many",
        stepId: "om-ten-thousand",
        passageId: "tao_te_ching.ttc_md_003",
      },
      {
        id: "er-union",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "The alone to the Alone — liberation lived while embodied.",
        trackId: "the-one-and-the-many",
        stepId: "om-alone-to-alone",
        passageId: "pratyabhijnahrdayam.phr_020",
      },
    ],
  },
  {
    id: "recognition",
    title: "Recognition",
    subtitle: "What was forgotten is remembered — not acquired",
    glyph: "ॐ",
    hue: 55,
    steps: [
      {
        id: "rec-ss",
        tradition: "Śiva Sūtra",
        insight: "Consciousness is the Self — not a possession, the ground.",
        trackId: "three-doors-of-shiva",
        stepId: "ss-caitanyam-atma",
        passageId: "siva_sutra.ss_i_1",
      },
      {
        id: "rec-phr",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Recognition of authorship turns the mind into the vehicle home.",
        trackId: "heart-of-recognition",
        stepId: "phr-the-turn",
        passageId: "pratyabhijnahrdayam.phr_013",
      },
      {
        id: "rec-vbt",
        tradition: "Vijñāna Bhairava",
        insight: "One doorway, fully entered — you become Bhairava.",
        trackId: "the-112-doorways",
        stepId: "vbt-become-bhairava",
        passageId: "vijnana_bhairava.yukti_112",
      },
    ],
  },
  {
    id: "living-breath",
    title: "The Living Breath",
    subtitle: "Haṃsa — the Goddess uttering herself as you",
    glyph: "ॐ",
    hue: 12,
    steps: [
      {
        id: "breath-vbt-utterance",
        tradition: "Vijñāna Bhairava",
        insight: "The breath is Her speech — haṃsa you never have to begin.",
        trackId: "the-112-doorways",
        stepId: "vbt-breath-utterance",
        passageId: "vijnana_bhairava.yukti_001",
      },
      {
        id: "breath-vbt-turn",
        tradition: "Vijñāna Bhairava",
        insight: "At the turn of the breath, śakti reveals herself in the Center.",
        trackId: "the-112-doorways",
        stepId: "vbt-the-center",
        passageId: "vijnana_bhairava.yukti_002",
      },
      {
        id: "breath-phr",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Bliss of Consciousness through the unfoldment of the middle.",
        trackId: "heart-of-recognition",
        stepId: "phr-the-middle",
        passageId: "pratyabhijnahrdayam.phr_017",
      },
      {
        id: "breath-letting-go",
        tradition: "Vijñāna Bhairava · Letting Go path",
        insight: "Enter the gap in the breath — full, not empty.",
        trackId: "letting-go-death-emptiness",
        stepId: "enter-the-gap",
        passageId: "vijnana_bhairava.yukti_001",
      },
    ],
  },
];
