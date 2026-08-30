import type { VerseItem } from "@shared/types";

export const MOCK_VERSES: VerseItem[] = [
  {
    _id: "dhp-001",
    sutra_id: "dhp-001",
    title: "Mind is the Forerunner",
    source: "Dhammapada",
    tradition: "Buddhism",
    verse: "Mind is the forerunner of all actions.\nAll deeds are led by mind, created by mind.\nIf one speaks or acts with a corrupt mind, suffering follows,\nAs the wheel follows the hoof of the ox drawing the cart.",
    translatedBy: "Thanissaro Bhikkhu",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Context",
        content: "The opening verse of the Dhammapada establishes the foundational Buddhist principle that mental states determine experience."
      }
    ]
  },
  {
    _id: "ttc-001",
    sutra_id: "ttc-001",
    title: "The Tao That Can Be Told",
    source: "Tao Te Ching",
    tradition: "Taoism",
    verse: "The Tao that can be told is not the eternal Tao.\nThe name that can be named is not the eternal name.\nThe nameless is the beginning of heaven and earth.\nThe named is the mother of ten thousand things.",
    translatedBy: "Stephen Mitchell",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Commentary",
        content: "Lao Tzu begins by pointing to the inadequacy of language to capture ultimate reality."
      }
    ]
  },
  {
    _id: "bg-002-47",
    sutra_id: "bg-002-47",
    title: "Your Right is to Work",
    source: "Bhagavad Gita",
    tradition: "Hinduism",
    verse: "Your right is to work only, but never to its fruits.\nLet not the fruits of action be your motive,\nNor let your attachment be to inaction.",
    translatedBy: "Eknath Easwaran",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Teaching",
        content: "This verse from Chapter 2 encapsulates karma yoga - the path of selfless action without attachment to results."
      }
    ]
  },
  {
    _id: "isha-001",
    sutra_id: "isha-001",
    title: "The Lord Pervades All",
    source: "Isha Upanishad",
    tradition: "Hinduism",
    verse: "The Lord is enshrined in the hearts of all.\nThe Lord is the supreme reality.\nRejoice in him through renunciation.\nCovet nothing. All belongs to the Lord.",
    translatedBy: "Eknath Easwaran",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Context",
        content: "The opening mantra of this Upanishad establishes the vision of divine immanence in all things."
      }
    ]
  },
  {
    _id: "dhp-183",
    sutra_id: "dhp-183",
    title: "The Teaching of All Buddhas",
    source: "Dhammapada",
    tradition: "Buddhism",
    verse: "To avoid all evil,\nTo cultivate good,\nAnd to purify one's mind —\nThis is the teaching of the Buddhas.",
    translatedBy: "Thanissaro Bhikkhu",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Summary",
        content: "This verse distills the entire Buddhist path into three essential principles."
      }
    ]
  },
  {
    _id: "ttc-011",
    sutra_id: "ttc-011",
    title: "The Usefulness of What Is Not",
    source: "Tao Te Ching",
    tradition: "Taoism",
    verse: "Thirty spokes share the wheel's hub;\nIt is the center hole that makes it useful.\nShape clay into a vessel;\nIt is the space within that makes it useful.",
    translatedBy: "Stephen Mitchell",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Teaching",
        content: "Lao Tzu points to the paradox that emptiness and space are what make things functional."
      }
    ]
  },
  {
    _id: "rumi-001",
    sutra_id: "rumi-001",
    title: "The Guesthouse",
    source: "Masnavi",
    tradition: "Sufism",
    verse: "This being human is a guest house.\nEvery morning a new arrival.\nA joy, a depression, a meanness,\nSome momentary awareness comes as an unexpected visitor.",
    translatedBy: "Coleman Barks",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Commentary",
        content: "Rumi's famous metaphor teaches us to welcome all experiences with equanimity."
      }
    ]
  },
  {
    _id: "meister-eckhart-001",
    sutra_id: "meister-eckhart-001",
    title: "Letting Go",
    source: "Sermons",
    tradition: "Christian Mysticism",
    verse: "The most powerful prayer, one wellnigh omnipotent, and the worthiest work of all is the outcome of a quiet mind. The quieter it is the more powerful, the worthier, the deeper, the more telling and more perfect the prayer is.",
    translatedBy: "Raymond Blakney",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Teaching",
        content: "Meister Eckhart emphasizes contemplative silence as the foundation of spiritual practice."
      }
    ]
  },
  {
    _id: "dhp-223",
    sutra_id: "dhp-223",
    title: "Conquer Anger with Love",
    source: "Dhammapada",
    tradition: "Buddhism",
    verse: "Conquer anger with love.\nConquer evil with good.\nConquer the miser with generosity.\nConquer the liar with truth.",
    translatedBy: "Eknath Easwaran",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Practice",
        content: "The Buddha teaches transformation through opposites - meeting negativity with positive qualities."
      }
    ]
  },
  {
    _id: "ttc-048",
    sutra_id: "ttc-048",
    title: "Less and Less",
    source: "Tao Te Ching",
    tradition: "Taoism",
    verse: "In the pursuit of learning, every day something is acquired.\nIn the pursuit of Tao, every day something is dropped.\nLess and less is done\nUntil non-action is achieved.",
    translatedBy: "Stephen Mitchell",
    editorial_maturity: "publishable" as const,
    layers: [
      {
        layer_name: "Teaching",
        content: "Lao Tzu contrasts worldly learning (accumulation) with spiritual practice (letting go)."
      }
    ]
  }
];

// Get a random verse from the mock data
export function getRandomMockVerse(): VerseItem {
  const randomIndex = Math.floor(Math.random() * MOCK_VERSES.length);
  return MOCK_VERSES[randomIndex];
}

// Get daily verse (deterministic based on date for consistency)
export function getMockDailyVerse(): VerseItem {
  const today = new Date();
  const dayOfYear = Math.floor((today.getTime() - new Date(today.getFullYear(), 0, 0).getTime()) / 86400000);
  const index = dayOfYear % MOCK_VERSES.length;
  return MOCK_VERSES[index];
}
