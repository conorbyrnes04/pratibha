import { LEARNING_TRACKS } from "./learningPaths";
import type { SumiSlug } from "@/lib/sumiGlyphs";

/** A bead is one move in a theme's argument, seated on an existing path gate. */
export type ThreadStepRef = {
  id: string;
  /** Tradition or text name shown on the bead. */
  tradition: string;
  /** One line — the thread's voice at this bead. */
  insight: string;
  /** Why this bead is the next step in the theme's claim. */
  move: string;
  /** Structural parallel with the theme / previous bead. */
  homology: string;
  /** Where this tradition parts, and why that matters. */
  divergence: string;
  trackId: string;
  stepId: string;
  passageId: string;
  /** Optional explicit sumi ink mark; falls back to sumiGlyph(tradition). */
  glyphSlug?: SumiSlug;
};

export type LearningThread = {
  id: string;
  title: string;
  subtitle: string;
  /** One philosophical claim. The title may stay poetic; this must be explicit. */
  thesis: string;
  /** The argument of the whole thread. */
  arc: string;
  /** Thread-level practice, not borrowed from the last path gate. */
  practice: string;
  /** What you should be able to recognize after the whole theme. */
  integration: string;
  /** Single character or short glyph for the bindu. */
  glyph: string;
  /** Optional explicit sumi ink mark for the thread medallion. */
  glyphSlug?: SumiSlug;
  /** Hue shift for this thread's accent (degrees). */
  hue: number;
  steps: ThreadStepRef[];
};

/** Theme-first recommended order: foundations-adjacent first, then deepening. */
export const RECOMMENDED_THREADS: string[] = [
  "action-without-seizing",
  "the-gap",
  "living-breath",
  "recognition",
  "the-witness",
  "becoming-light",
  "emanation-return",
  "death-as-teacher",
];

export const LEARNING_THREADS: LearningThread[] = [
  {
    id: "the-gap",
    title: "The Gap",
    subtitle: "The madhya — the still hinge between every two states",
    thesis: "The opening is not a mood. It is a method: rest in the seam between any two states.",
    arc:
      "We start where the seam is most intimate — the turn of the breath — then generalize: any two cognitions, the lip of sleep, the functional hollow that makes a vessel useful, the emptied heart that can finally hear. The claim tightens from a Kashmiri technique into a cross-tradition fact about experience: every transition is already a doorway, if you stop skipping it.",
    practice:
      "Three times today, catch a seam — between two breaths, two thoughts, or two tasks — and rest there for one unhurried beat before the next thing begins.",
    integration:
      "You can find a seam in ordinary experience and treat it as the destination, not as dead time to skip.",
    glyph: "○",
    hue: 42,
    steps: [
      {
        id: "gap-vbt-center",
        tradition: "Vijñāna Bhairava",
        insight: "Between out-breath and in-breath, śakti rests in the Center.",
        move: "Name the seam where it is most bodily: the turn of the breath.",
        homology: "Opens the theme in seed form — a gap that is full, not empty.",
        divergence:
          "Here the pause is Śakti at rest, a Goddess-presence. Later beads will refuse that theism and still keep the seam.",
        trackId: "the-112-doorways",
        stepId: "vbt-the-center",
        passageId: "vijnana_bhairava.yukti_002",
      },
      {
        id: "gap-vbt-seam",
        tradition: "Vijñāna Bhairava",
        insight: "Between any two cognitions, take refuge in the seam.",
        move: "Widen the Center from breath to every transition in experience.",
        homology: "Same structure as the breath-turn: two poles, one interval, rest in the interval.",
        divergence:
          "The breath gate is rhythmic and given. This gate is structural — it appears wherever the mind jumps, so the method leaves the cushion.",
        trackId: "the-112-doorways",
        stepId: "vbt-seam-between",
        passageId: "vijnana_bhairava.yukti_034",
      },
      {
        id: "gap-phr-middle",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Unfold the middle — bliss hides in the gap of the breath.",
        move: "The seam is not only a technique; it is where contraction releases.",
        homology: "Madhya is the same hinge: between breaths, thoughts, states.",
        divergence:
          "VBT treats the gap as a doorway you enter. Recognition treats it as the native tone of uncontracted Consciousness — bliss already there, not imported.",
        trackId: "heart-of-recognition",
        stepId: "phr-the-middle",
        passageId: "pratyabhijnahrdayam.phr_017",
      },
      {
        id: "gap-mandukya",
        tradition: "Vijñāna Bhairava · turīya",
        insight: "At the lip of sleep — the wakeful Fourth shows.",
        move: "Take the widest nightly seam: waking has released the world, sleep has not yet claimed you.",
        homology: "Again two states and a lucid interval — now at the scale of a whole day.",
        divergence:
          "This is not a sitting you schedule. It is a threshold you already cross. The art is staying lucid without thinking yourself back awake.",
        trackId: "the-112-doorways",
        stepId: "vbt-threshold-sleep",
        passageId: "vijnana_bhairava.yukti_047",
      },
      {
        id: "gap-tao-absence",
        tradition: "Tao Te Ching",
        insight: "The hollow of the vessel is what holds the tea.",
        move: "Leave Kashmir. The gap is useful, not mystical — absence is what makes a thing work.",
        homology: "Same structure: the empty interval is the functional heart of the whole.",
        divergence:
          "No Śakti, no turīya, no bliss of Consciousness. The Tao names the axle-hole and the room. The seam becomes civic and ordinary — a pause you stop filling.",
        trackId: "letting-go-death-emptiness",
        stepId: "use-absence",
        passageId: "tao_te_ching.ttc_md_002",
      },
      {
        id: "gap-zhuangzi",
        tradition: "Zhuangzi",
        insight: "Empty the heart-mind enough to hear what is actually there.",
        move: "The seam becomes hospitality: you empty so another can arrive.",
        homology: "Still a clearing between two fillings — now the filling is your own commentary.",
        divergence:
          "The Kashmiri gap is entered to taste presence. Zhuangzi empties to receive. The method is ethical and conversational, not yogic.",
        trackId: "letting-go-death-emptiness",
        stepId: "empty-to-receive",
        passageId: "the_book_of_chuang_tzu.zhuangzi_md_004",
      },
      {
        id: "gap-letting-go-breath",
        tradition: "Letting Go path · breath",
        insight: "Enter the gap in the breath — full, not empty.",
        move: "Return to the body with the whole argument in hand: the pause is a miniature death you can ride.",
        homology: "Closes the circle on the first breath-turn, now read as impermanence practiced rather than feared.",
        divergence:
          "This sitting belongs to a path about dying. The gap is not only Center or hollow vessel — it is a rehearsal of ending, tender rather than grim.",
        trackId: "letting-go-death-emptiness",
        stepId: "enter-the-gap",
        passageId: "vijnana_bhairava.yukti_001",
      },
    ],
  },
  {
    id: "becoming-light",
    title: "Becoming Light",
    subtitle: "You cannot see the sun unless you have first become sunlike",
    thesis: "The Source is not grasped as an object. You see it by resemblance — by becoming light.",
    arc:
      "Plotinus gives the claim: the eye sees the sun only by becoming sunlike. Śaivism answers with surge and flash — awareness catching itself. The Yoginīhṛdaya interiorizes the whole diagram in the body. Then a counter-bead: Aṣṭāvakra will not let you manufacture light; you are already the witness. The fire that never went out is the last word: you were never kindling from nothing.",
    practice:
      "Once today, set down one excessive thing — a grasping, a performance, a haze — and notice what brightness was already under it. Do not add light. Subtract the cover.",
    integration:
      "You can tell the difference between chasing a vision and becoming like what you seek.",
    glyph: "☀",
    glyphSlug: "sun",
    hue: 28,
    steps: [
      {
        id: "light-plotinus",
        tradition: "Plotinus",
        insight: "Never cease chiselling your statue until virtue shines.",
        move: "State the law of vision: likeness before sight.",
        homology: "Opens the theme — ascent as subtraction, not acquisition.",
        divergence:
          "Plotinus chisels toward Beauty and the One. Later beads will refuse the sculptor's effort and call the light already burning.",
        trackId: "the-one-and-the-many",
        stepId: "om-become-sunlike",
        passageId: "plotinus_enneads.enn_i_6_09",
      },
      {
        id: "light-ss",
        tradition: "Śiva Sūtra",
        insight: "The surge of awareness itself is Bhairava.",
        move: "Light arrives as a pulse, not only as a polished statue.",
        homology: "Same seeing-by-being: the surge is awareness recognizing itself.",
        divergence:
          "Plotinus works by removal over time. Udyama is sudden — a vertical welling. Effort here would miss the flash.",
        trackId: "three-doors-of-shiva",
        stepId: "ss-udyamo-bhairavah",
        passageId: "siva_sutra.ss_i_5",
      },
      {
        id: "light-yh-flash",
        tradition: "Yoginīhṛdaya",
        insight: "The world springs when the Goddess sees her own radiance.",
        move: "The flash is cosmogonic: self-aware light emits a universe.",
        homology: "Catching yourself being aware is the same hinge Plotinus and Vasugupta named.",
        divergence:
          "This is not the soul becoming sunlike. It is the Goddess looking at her own sphurattā. Manifestation is play, not a fall to be reversed.",
        trackId: "descent-of-the-cakra",
        stepId: "yh-sphuratta",
        passageId: "yoginihrdaya.yh_006",
      },
      {
        id: "light-yh",
        tradition: "Yoginīhṛdaya",
        insight: "Re-find the whole diagram in the body; climb to the partless summit.",
        move: "Bring the light down into the subtle body — the statue is now a cakra.",
        homology: "Ascent still, but through centers rather than virtues.",
        divergence:
          "Plotinus chisels character. This path interiorizes a diagram. The body is the mountain, not an obstacle to leave.",
        trackId: "descent-of-the-cakra",
        stepId: "yh-interiorize",
        passageId: "yoginihrdaya.yh_011",
      },
      {
        id: "light-witness",
        tradition: "Aṣṭāvakra",
        insight: "You are the bird that watches — not the one that must become sun.",
        move: "The counter-claim: light is not produced by chiselling. You already are the witness.",
        homology: "Still a seeing that is not of objects — but it is recognition, not resemblance-work.",
        divergence:
          "Plotinus says become sunlike. Aṣṭāvakra says stop identifying with the eater. The danger of this theme is spiritual athleticism; this bead refuses it.",
        trackId: "recognizing-awareness",
        stepId: "recognize-the-witness",
        passageId: "astavakra_gita.asg_1_7",
      },
      {
        id: "light-fire",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "The Fire of Consciousness never went out — even under the forgetting.",
        move: "Close the argument: you were not kindling. You were noticing a flame that kept burning.",
        homology: "Unites chiselling and witness: the work is uncovering, not manufacturing.",
        divergence:
          "Unlike Plotinus' statue, nothing essential was ever missing. Lost time was still fuel. The anxiety of having to generate awakening from scratch dissolves.",
        trackId: "heart-of-recognition",
        stepId: "phr-fire-never-out",
        passageId: "pratyabhijnahrdayam.phr_014",
      },
    ],
  },
  {
    id: "emanation-return",
    title: "Emanation & Return",
    subtitle: "The One overflows into the many — and the many remember",
    thesis: "The many are the One going forth; the return adds nothing — it reverses direction.",
    arc:
      "Name the Source that cannot be named. Watch it overflow without loss. Meet the ten thousand things as waves already returning. Then the wound: forgetting. Then the hinge: you are the same One at a contracted aperture. Recognition turns the current. The Perfect I is the homecoming lived in a body.",
    practice:
      "Once today, catch attention pouring outward. Reverse it — not to acquire a state, only to rest in the awareness that was doing the pouring.",
    integration:
      "You can read a stretch of your own life as overflow, forgetting, and return — without treating the many as a mistake.",
    glyph: "∞",
    glyphSlug: "infinity",
    hue: 195,
    steps: [
      {
        id: "er-nameless",
        tradition: "Tao Te Ching",
        insight: "The dao that can be named is not the enduring dao.",
        move: "Before a story of descent, point at what cannot be a thing.",
        homology: "Opens the theme: Source prior to division.",
        divergence:
          "The Tao undoes its own first word. Plotinus and Śaivism will name the One and citi. Start here so naming does not harden too soon.",
        trackId: "the-one-and-the-many",
        stepId: "om-source-no-name",
        passageId: "tao_te_ching.ttc_md_001",
      },
      {
        id: "er-plotinus",
        tradition: "Plotinus",
        insight: "The One overflows; Intellect turns back and beholds its source.",
        move: "Explain how the perfect One gives rise to the many without being emptied.",
        homology: "Fullness pours; each level is born gazing back.",
        divergence:
          "Emanation here is necessary overflow of perfection, staged (One, Nous, Soul). Śaivism will call the same unfolding free will, not necessity.",
        trackId: "the-one-and-the-many",
        stepId: "om-overflow",
        passageId: "plotinus_enneads.enn_v_1_06",
      },
      {
        id: "er-phr",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "She unfolds the universe on her own canvas, by free will.",
        move: "The same going-forth, now as play rather than overflow.",
        homology: "One source, a world appearing without the source being elsewhere.",
        divergence:
          "Plotinus' One does not choose. Citi paints by svecchā. Bondage later will be forgotten authorship of that painting — a Śaiva twist Plotinus does not need.",
        trackId: "heart-of-recognition",
        stepId: "phr-free-unfolding",
        passageId: "pratyabhijnahrdayam.phr_002",
      },
      {
        id: "er-tao",
        tradition: "Tao Te Ching",
        insight: "The ten thousand things arise together — I watch them return.",
        move: "Hold multiplicity without contempt and without grasping.",
        homology: "Waves on one water: real as waves, never other than water.",
        divergence:
          "No hierarchy of hypostases. The Tao watches arising and return with serenity. The 'fall' has not yet been named — that is the next bead.",
        trackId: "the-one-and-the-many",
        stepId: "om-ten-thousand",
        passageId: "tao_te_ching.ttc_md_003",
      },
      {
        id: "er-forgetting",
        tradition: "Plotinus",
        insight: "The soul forgot the Father through self-will — not exile.",
        move: "Name the wound: bondage is forgetting, not punishment.",
        homology: "The many have a shadow — separation as lost memory.",
        divergence:
          "The Tao's ten thousand were already returning. Plotinus introduces pathos: the child who forgot its name. Śaivism will agree, and call it bewildered authorship.",
        trackId: "the-one-and-the-many",
        stepId: "om-forgetting",
        passageId: "plotinus_enneads.enn_v_1_01",
      },
      {
        id: "er-turn",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Recognition of authorship turns the mind into the vehicle home.",
        move: "The current reverses. Nothing is added; direction changes.",
        homology: "Same energy that went out now flows in — Plotinus' turn of the soul.",
        divergence:
          "The instrument is pratyabhijñā, not Beauty's ladder. The mind that bound you is the mind that frees you, re-aimed.",
        trackId: "the-one-and-the-many",
        stepId: "om-the-turn",
        passageId: "pratyabhijnahrdayam.phr_013",
      },
      {
        id: "er-union",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "The alone to the Alone — liberation lived while embodied.",
        move: "Homecoming is identity recognized, not a soul arriving at a distant God.",
        homology: "The circle closes: overflow and return are one movement.",
        divergence:
          "Plotinus' 'flight of the alone to the Alone' can sound like two lonelies meeting. This bead insists there were never two. Jīvanmukti keeps the body.",
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
    thesis: "Liberation is recognition of what was never missing — not the gaining of a new state.",
    arc:
      "Name the ground: consciousness is the Self. See how even knowledge binds. Map forgotten authorship as the exact definition of bondage. Then the turn. Then the inquiry in the desireless gap. One doorway, fully entered, is enough — not because you collected states, but because you remembered.",
    practice:
      "When you catch yourself seeking a better state, ask once: 'What is already aware of this seeking?' Rest there. Do not add a technique on top.",
    integration:
      "You can distinguish remembering from acquiring — and catch spiritual knowledge when it hardens into another identity.",
    glyph: "ॐ",
    glyphSlug: "star",
    hue: 55,
    steps: [
      {
        id: "rec-ss",
        tradition: "Śiva Sūtra",
        insight: "Consciousness is the Self — not a possession, the ground.",
        move: "Reverse the usual ontology: you do not have awareness; you are it.",
        homology: "Opens the theme as a single sentence you can test now.",
        divergence:
          "This is the sudden door. Later beads will show how the same knowledge, held wrongly, becomes a cage.",
        trackId: "three-doors-of-shiva",
        stepId: "ss-caitanyam-atma",
        passageId: "siva_sutra.ss_i_1",
      },
      {
        id: "rec-knowledge-binds",
        tradition: "Śiva Sūtra",
        insight: "Knowledge is bondage when it fences the open into 'I am this.'",
        move: "The first shock: the thing that seems to free you can contract you.",
        homology: "Still about what you take yourself to be — now as a mechanism.",
        divergence:
          "Sūtra 1 named the ground. Sūtra 2 names the fence. Spiritual knowledge is not exempt.",
        trackId: "recognizing-awareness",
        stepId: "see-knowledge-bind",
        passageId: "siva_sutra.ss_i_2",
      },
      {
        id: "rec-bondage",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Bondage is forgotten authorship of a play you yourself are staging.",
        move: "Give the exact definition: not sin, not exile — bewilderment by your own powers.",
        homology: "Forgetting again, now as the Śaiva diagnosis of saṃsāra.",
        divergence:
          "Unlike a moral fall, nothing was done to you. You contracted. That is why recognition, not purification, is the medicine.",
        trackId: "heart-of-recognition",
        stepId: "phr-forgotten-authorship",
        passageId: "pratyabhijnahrdayam.phr_012",
      },
      {
        id: "rec-phr",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Recognition of authorship turns the mind into the vehicle home.",
        move: "The turn: same mind, reversed.",
        homology: "Remembering in motion — the thesis enacted.",
        divergence:
          "No new faculty is installed. If you are waiting to acquire recognition, you are still in the previous bead's forgetting.",
        trackId: "heart-of-recognition",
        stepId: "phr-the-turn",
        passageId: "pratyabhijnahrdayam.phr_013",
      },
      {
        id: "rec-who",
        tradition: "Vijñāna Bhairava",
        insight: "When neither desire nor thought arises — who am I?",
        move: "Ask the question in a natural trough, not as a philosophy exam.",
        homology: "Recognition in the gap where the costume of craving falls off.",
        divergence:
          "PHR's turn is a reversal of authorship. This is an inquiry in a lull. You do not answer; you notice what remains awake.",
        trackId: "the-112-doorways",
        stepId: "vbt-who-am-i",
        passageId: "vijnana_bhairava.yukti_069",
      },
      {
        id: "rec-vbt",
        tradition: "Vijñāna Bhairava",
        insight: "One doorway, fully entered — you become Bhairava.",
        move: "Close: you do not need one hundred and twelve completions. You need one true entry.",
        homology: "Remembrance, not collection — the thesis in its sharpest form.",
        divergence:
          "The 112 doorways can become a spiritual inventory. This bead refuses that. Completeness is intensity of entry, not coverage.",
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
    thesis: "The breath is already a teaching. You do not start it; you notice who is speaking as it.",
    arc:
      "First the breath as Her speech — haṃsa you never begin. Then the Center at the turn. Then sound dying into silence. Then the Gītā's patient return of a restless mind. Then the Tao's useful hollow. Then Zhuangzi's emptied listening. The breath leaves the Trika club and becomes a way of attending anywhere.",
    practice:
      "Ten breaths. On each turn, rest one beat. Do not hold or control. Just notice the speech that is already happening as you.",
    integration:
      "You can treat one ordinary breath as address — and return attention without treating wandering as failure.",
    glyph: "ॐ",
    glyphSlug: "spiral",
    hue: 12,
    steps: [
      {
        id: "breath-vbt-utterance",
        tradition: "Vijñāna Bhairava",
        insight: "The breath is Her speech — haṃsa you never have to begin.",
        move: "Stop starting a practice. Notice the utterance already running.",
        homology: "Opens the theme: breath as given speech, not a technique you inaugurate.",
        divergence:
          "Later beads will keep the breath and drop the Goddess-as-speaker. Start here so the intimacy is not lost.",
        trackId: "the-112-doorways",
        stepId: "vbt-breath-utterance",
        passageId: "vijnana_bhairava.yukti_001",
      },
      {
        id: "breath-vbt-turn",
        tradition: "Vijñāna Bhairava",
        insight: "At the turn of the breath, śakti reveals herself in the Center.",
        move: "The teaching concentrates at the hinge, not the flow.",
        homology: "Same breath, now the pause is the shrine.",
        divergence:
          "The first bead was continuous utterance. This is the still point. Both are the same life, two readings.",
        trackId: "the-112-doorways",
        stepId: "vbt-the-center",
        passageId: "vijnana_bhairava.yukti_002",
      },
      {
        id: "breath-edge-sound",
        tradition: "Vijñāna Bhairava",
        insight: "The silence at the birth and death of a sound is the same hinge.",
        move: "Leave the nostrils. Any arising and vanishing has the same seam.",
        homology: "Birth and death of a tone = in-breath and out-breath.",
        divergence:
          "Sound makes the gap audible. You can practice in a room, not only in a sit.",
        trackId: "the-112-doorways",
        stepId: "vbt-edge-of-sound",
        passageId: "vijnana_bhairava.yukti_015",
      },
      {
        id: "breath-phr",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Bliss of Consciousness through the unfoldment of the middle.",
        move: "The breath-gap is named as madhya — a repeatable center, not a special state.",
        homology: "Same hinge, now as the native tone of uncontracted awareness.",
        divergence:
          "Less Goddess-speech, more recognition yoga. The bliss is not added pleasure.",
        trackId: "heart-of-recognition",
        stepId: "phr-the-middle",
        passageId: "pratyabhijnahrdayam.phr_017",
      },
      {
        id: "breath-gita",
        tradition: "Bhagavad Gītā",
        insight: "The mind is as hard to hold as the wind — mastery is the return.",
        move: "Leave Kashmir. Attention training without tantra: abhyāsa and vairāgya.",
        homology: "Still a rhythm of leaving and coming back — now the 'breath' is attention itself.",
        divergence:
          "No haṃsa, no Śakti. Krishna answers restlessness with patient repetition. Wandering is not failure; returning is the practice.",
        trackId: "action-without-contraction",
        stepId: "steady-the-mind",
        passageId: "bhagavad_gita.bg_06_35",
      },
      {
        id: "breath-tao",
        tradition: "Tao Te Ching",
        insight: "Leave the hollow unused — that is what holds the tea.",
        move: "The pause is useful. Stop filling every interval.",
        homology: "Functional emptiness = the breath's unfilled turn.",
        divergence:
          "No inner Goddess. A civic, almost craftsperson's reading of the same hollow.",
        trackId: "letting-go-death-emptiness",
        stepId: "use-absence",
        passageId: "tao_te_ching.ttc_md_002",
      },
    ],
  },
  {
    id: "action-without-seizing",
    title: "Action Without Seizing",
    subtitle: "Act fully. Do not white-knuckle the fruit.",
    thesis: "Clear action is possible without contraction around the outcome — that is freedom, not indifference.",
    arc:
      "Begin in honest paralysis. Separate what is yours to govern. Act without possessiveness. Distinguish inner renunciation from flight. Steady the mind that keeps grasping. End in surrender that is more lucid than control. Zhuangzi's emptied listening keeps the theme from becoming only a battlefield ethic.",
    practice:
      "Choose one ordinary task. Offer the doing; release the result on the first out-breath. If anxiety returns, come back to the task, not to the fantasy of managing the universe.",
    integration:
      "You can throw yourself into an action and notice — then loosen — the grip on how it turns out.",
    glyph: "弓",
    hue: 88,
    steps: [
      {
        id: "act-crisis",
        tradition: "Bhagavad Gītā",
        insight: "The path begins in being stuck — the crisis is the doorway.",
        move: "Do not skip the overwhelm. Treat it as sacred data.",
        homology: "Opens the theme in the body of a dilemma, not a calm precept.",
        divergence:
          "A 'spiritual' start is often imagined as composure. Arjuna breaks down first. Later Stoic precision comes after this honesty.",
        trackId: "action-without-contraction",
        stepId: "meet-the-crisis",
        passageId: "bhagavad_gita.bg_01_47",
      },
      {
        id: "act-govern",
        tradition: "Epictetus",
        insight: "Freedom is trained by locating effort only where power reaches.",
        move: "Draw the line: judgments are yours; outcomes are not.",
        homology: "Same stuckness, now with a hinge that makes action possible.",
        divergence:
          "The Gita stays on a battlefield of dharma. Epictetus gives a portable division. Precision can look cold; it is meant to concentrate care, not withdraw it.",
        trackId: "action-without-contraction",
        stepId: "separate-governance",
        passageId: "epictetus_works.epi_enc_001",
      },
      {
        id: "act-fruit",
        tradition: "Bhagavad Gītā",
        insight: "You have a right to the action, never to its fruits.",
        move: "Turn inner freedom into a way of working.",
        homology: "Release what is not yours — now while acting, not only while sorting.",
        divergence:
          "Epictetus withdraws demand. Krishna asks for total presence to the work. Non-possessiveness is not less care; it is care without the hedge.",
        trackId: "action-without-contraction",
        stepId: "release-ownership",
        passageId: "bhagavad_gita.bg_02_47",
      },
      {
        id: "act-renounce",
        tradition: "Bhagavad Gītā",
        insight: "Renounce the grasping, not the engagement.",
        move: "Name the counterfeit: leaving the field to look wise.",
        homology: "Still about non-seizing — now the temptation is flight.",
        divergence:
          "Stoic withdrawal from what is not yours can be misread as stepping away. This bead insists you often stay, but differently.",
        trackId: "action-without-contraction",
        stepId: "renounce-within-action",
        passageId: "bhagavad_gita.bg_05_10",
      },
      {
        id: "act-zhuangzi",
        tradition: "Zhuangzi",
        insight: "Empty the heart-mind and you can finally hear the situation.",
        move: "Wuwei as reception: action that is not pre-loaded with your agenda.",
        homology: "Non-seizing again — you release the commentary that fills every space.",
        divergence:
          "The Gita's hero must fight. Zhuangzi empties to become available. The theme is not only duty; it is hospitality to what is there.",
        trackId: "letting-go-death-emptiness",
        stepId: "empty-to-receive",
        passageId: "the_book_of_chuang_tzu.zhuangzi_md_004",
      },
      {
        id: "act-surrender",
        tradition: "Bhagavad Gītā",
        insight: "Surrender is lucid release after clarity — not collapse before it.",
        move: "Close: you have sorted, acted, emptied. Now stop white-knuckling the universe.",
        homology: "The whole theme in one gesture: clear action, then genuine setting-down.",
        divergence:
          "Not fatalism. The work of the previous beads is the condition. Surrender without that work is just giving up.",
        trackId: "action-without-contraction",
        stepId: "surrender-with-clarity",
        passageId: "bhagavad_gita.bg_18_66",
      },
    ],
  },
  {
    id: "death-as-teacher",
    title: "Death as Teacher",
    subtitle: "Rehearse release now, so loss does not find you unpracticed",
    thesis: "Death is not only an ending. It is a discipline of loosening identification — and its fruit is composure offered to others.",
    arc:
      "Socrates names philosophy as the practice of dying. Trust the unseen that actually steers a life. Empty enough to receive. Discover that absence is useful. Enter the breath's miniature death. Close with composure as a gift, not a private attainment. (Katha is not yet a path gate; the Upaniṣadic death-teaching waits in the well of supporting passages.)",
    practice:
      "Name one thing you treat as if it could make you permanent. Ask: if this changed, what in you would still be aware of the change? Rest there without forcing an answer.",
    integration:
      "You can practice a small release today and recognize composure as something you leave in a room, not something you hoard.",
    glyph: "☽",
    hue: 220,
    steps: [
      {
        id: "death-socrates",
        tradition: "Plato · Phaedo",
        insight: "Philosophy is rehearsal for dying — loosening what is already perishing.",
        move: "Reframe death as an operation available now, not only an event later.",
        homology: "Opens the theme: release of false centers before mortality forces it.",
        divergence:
          "Not morbidity. The fruit is vividness. Later beads will make the rehearsal bodily and ethical.",
        trackId: "letting-go-death-emptiness",
        stepId: "train-for-death",
        passageId: "phaedo_plato.phaedo_md_001",
      },
      {
        id: "death-unseen",
        tradition: "Plato · Phaedo",
        insight: "The soul has affinity with what is invisible — weight the unseen rightly.",
        move: "Letting go of the visible requires a discipline of attention.",
        homology: "Still about not letting the loudest evidence dictate what is real.",
        divergence:
          "Less 'dying' than epistemology. Values and intentions are the unseen that actually govern a life.",
        trackId: "letting-go-death-emptiness",
        stepId: "see-the-unseen",
        passageId: "phaedo_plato.phaedo_md_003",
      },
      {
        id: "death-empty",
        tradition: "Zhuangzi",
        insight: "Fast the heart-mind so you can receive what death and loss actually bring.",
        move: "Emptiness as hospitality, not grim sacrifice.",
        homology: "Release of agenda — a living analog of loosening identification.",
        divergence:
          "Socrates rehearses losing the body. Zhuangzi empties commentary. The teacher is availability, not the hemlock.",
        trackId: "letting-go-death-emptiness",
        stepId: "empty-to-receive",
        passageId: "the_book_of_chuang_tzu.zhuangzi_md_004",
      },
      {
        id: "death-absence",
        tradition: "Tao Te Ching",
        insight: "The gap is what makes the vessel work.",
        move: "Absence is structural, not a defect to fill before you die.",
        homology: "The useful hollow = the space left when clinging loosens.",
        divergence:
          "No soul-discourse. A craftsperson's metaphysics of empty space. Death-teaching becomes how you treat pauses in a day.",
        trackId: "letting-go-death-emptiness",
        stepId: "use-absence",
        passageId: "tao_te_ching.ttc_md_002",
      },
      {
        id: "death-breath",
        tradition: "Vijñāna Bhairava",
        insight: "Each pause between breaths is a death-and-rebirth you can ride.",
        move: "Make the rehearsal intimate and constant.",
        homology: "Impermanence practiced in the most ordinary rhythm.",
        divergence:
          "Plato thought death. This bead feels it. The threshold is always available — no execution day required.",
        trackId: "letting-go-death-emptiness",
        stepId: "enter-the-gap",
        passageId: "vijnana_bhairava.yukti_001",
      },
      {
        id: "death-composure",
        tradition: "Plato · Phaedo",
        insight: "A life rehearsed in release leaves composure as a gift in the room.",
        move: "The inner work is not private. Tone is the legacy.",
        homology: "The whole theme ripens into ethics: how you meet ending teaches others.",
        divergence:
          "Not a personal samādhi. Socrates' calm is offered. Letting go, matured, is generosity.",
        trackId: "letting-go-death-emptiness",
        stepId: "final-composure",
        passageId: "phaedo_plato.phaedo_md_007",
      },
    ],
  },
  {
    id: "the-witness",
    title: "The Witness",
    subtitle: "You are the one who sees — not the changing seen",
    thesis: "The witness is ordinary awareness recognized, not a special state attained — and it remains through waking, the lip of sleep, and contraction.",
    arc:
      "Name the ground. Watch knowledge fence it into a self. Relocate as the watching bird. Map how the same awareness contracts. Catch the surge when it breaks through. At the lip of sleep, taste objectless lucidity (the Fourth, by another name — Mandukya is not yet a path gate). Stabilize in an ordinary trigger. The witness is frequent return, not a peak.",
    practice:
      "Whatever you feel in this minute, ask once: 'Who is aware of this?' Do not answer in words. Rest as that, and let the feeling continue at the edge.",
    integration:
      "You can, at will, recognize yourself as the one aware of an experience rather than as the experience — including when awareness has narrowed.",
    glyph: "👁",
    glyphSlug: "eye",
    hue: 168,
    steps: [
      {
        id: "wit-ground",
        tradition: "Śiva Sūtra",
        insight: "Consciousness is the Self — the ground, not a function you own.",
        move: "Reverse priority: stop looking only at contents.",
        homology: "Opens the theme as a testable shift of attention.",
        divergence:
          "This is Śaiva suddenness. The next bead will show the same ground getting fenced by 'I am this.'",
        trackId: "recognizing-awareness",
        stepId: "name-the-ground",
        passageId: "siva_sutra.ss_i_1",
      },
      {
        id: "wit-bind",
        tradition: "Śiva Sūtra",
        insight: "Limited knowledge is how the witness gets mistaken for a character.",
        move: "See the mechanism of losing the witness without leaving the room.",
        homology: "Same awareness, now caught in a definition.",
        divergence:
          "Sūtra 1 was invitation. Sūtra 2 is diagnosis. Even this theme can become a defended identity.",
        trackId: "recognizing-awareness",
        stepId: "see-knowledge-bind",
        passageId: "siva_sutra.ss_i_2",
      },
      {
        id: "wit-astavakra",
        tradition: "Aṣṭāvakra",
        insight: "You are the bird that watches, not the bird that eats.",
        move: "The classic relocation: from fruit to the one who sees the fruit.",
        homology: "Witness as already the case — not a state to climb into.",
        divergence:
          "No Śaiva surge yet. Aṣṭāvakra is almost severe in his directness. The eater is not destroyed; you stop taking it as the whole of you.",
        trackId: "recognizing-awareness",
        stepId: "recognize-the-witness",
        passageId: "astavakra_gita.asg_1_7",
      },
      {
        id: "wit-contraction",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "The small self is awareness voluntarily narrowed.",
        move: "If the witness can contract, contraction can be felt and loosened.",
        homology: "The eater is saṅkoca — not an enemy soul, a movement.",
        divergence:
          "Aṣṭāvakra says you are not the body-mind. PHR says the limited subject is the One at a narrowed aperture. Softer, and more usable in a defensive moment.",
        trackId: "recognizing-awareness",
        stepId: "learn-contraction",
        passageId: "pratyabhijnahrdayam.phr_004",
      },
      {
        id: "wit-surge",
        tradition: "Śiva Sūtra",
        insight: "Recognition also arrives as a surge of aliveness.",
        move: "The witness is not only cool observation. Catch its pulse.",
        homology: "Same awareness, now in energetic form at the seams.",
        divergence:
          "Aṣṭāvakra can sound still. Udyama is vivid. Both are the witness; this bead refuses a purely conceptual reading.",
        trackId: "recognizing-awareness",
        stepId: "taste-the-surge",
        passageId: "siva_sutra.ss_i_5",
      },
      {
        id: "wit-sleep",
        tradition: "Vijñāna Bhairava",
        insight: "At the lip of sleep, awareness remains while objects fall away.",
        move: "Taste the witness when the world has let go — the Fourth by another door.",
        homology: "Objectless lucidity: waking, dream, and sleep as states the witness outlasts.",
        divergence:
          "Mandukya would name turīya as the fourth. This gate trains the nightly seam instead. Same claim, different handle — and you already cross it.",
        trackId: "the-112-doorways",
        stepId: "vbt-threshold-sleep",
        passageId: "vijnana_bhairava.yukti_047",
      },
      {
        id: "wit-ordinary",
        tradition: "Pratyabhijñāhṛdayam",
        insight: "Stable recognition is frequent return in ordinary life — not a peak.",
        move: "Close: a doorbell, a sip, a doorway. The witness survives interruption.",
        homology: "The whole theme as a way of living, not an event.",
        divergence:
          "Retreat-intensity is not the measure. If the witness only appears on the cushion, the argument failed.",
        trackId: "recognizing-awareness",
        stepId: "stabilize-recognition",
        passageId: "pratyabhijnahrdayam.phr_020",
      },
    ],
  },
];

export function findThread(threadId: string): LearningThread | undefined {
  return LEARNING_THREADS.find((t) => t.id === threadId);
}

export function findBead(thread: LearningThread, beadId: string): ThreadStepRef | undefined {
  return thread.steps.find((s) => s.id === beadId);
}

export function beadIndex(thread: LearningThread, beadId: string): number {
  return thread.steps.findIndex((s) => s.id === beadId);
}

/** Path step title for a bead destination (for denser bead labels). */
export function pathStepTitleForBead(bead: ThreadStepRef): string | null {
  const track = LEARNING_TRACKS.find((t) => t.id === bead.trackId);
  return track?.steps.find((s) => s.id === bead.stepId)?.title ?? null;
}

export type ThreadMembership = {
  thread: LearningThread;
  bead: ThreadStepRef;
};

/** Which threads include this path gate — for reverse links on path steps. */
export function threadsForPathStep(trackId: string, stepId: string): ThreadMembership[] {
  const out: ThreadMembership[] = [];
  for (const thread of LEARNING_THREADS) {
    for (const bead of thread.steps) {
      if (bead.trackId === trackId && bead.stepId === stepId) {
        out.push({ thread, bead });
      }
    }
  }
  return out;
}

export function threadBeadCount(thread: LearningThread): number {
  return thread.steps.length;
}
