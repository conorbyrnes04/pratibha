export type ComparePreset = {
  id: string;
  label: string;
  voiceA: string;
  voiceB: string;
  verseA?: string;
  verseB?: string;
  prompt: string;
};

/** Quick cross-tradition pairings — verse ids resolved at runtime when omitted. */
export const COMPARE_PRESETS: ComparePreset[] = [
  {
    id: "stilling-mind",
    label: "Stilling the mind",
    voiceA: "Patañjali Yoga Sūtras",
    voiceB: "The Book of Chuang Tzu",
    verseA: "patañjali_yoga_sūtras.ys_1_02",
    verseB: "the_book_of_chuang_tzu.zhuangzi_md_015",
    prompt: "Compare Patanjali YS 1.2 and Zhuangzi on stilling mental flux versus wu wei / mirror mind.",
  },
  {
    id: "desire-discipline",
    label: "Desire & discipline",
    voiceA: "Bhagavad Gita",
    voiceB: "Epictetus Works",
    prompt: "Compare Bhagavad Gita and Epictetus on desire, discipline, and inner freedom.",
  },
  {
    id: "change-logos",
    label: "Change & logos",
    voiceA: "Heraclitus Fragments",
    voiceB: "Tao Te Ching",
    prompt: "How do Heraclitus and the Tao Te Ching treat change, flow, and the underlying order?",
  },
  {
    id: "witness-liberation",
    label: "Witness & liberation",
    voiceA: "Astavakra Gita",
    voiceB: "Patañjali Yoga Sūtras",
    verseB: "patañjali_yoga_sūtras.ys_1_03",
    prompt: "Compare Astavakra and Patanjali on the witness (sākṣin) and liberation through stilling the mind.",
  },
];
