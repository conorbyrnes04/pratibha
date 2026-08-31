export type ChatMode = "question" | "explain" | "compare" | "practice";

export type LearningStepSpec = {
  id: string;
  title: string;
  /** Where we are in the journey and why this step comes now. 1-2 sentences. */
  orientation: string;
  /** The core teaching: the actual conceptual move, explained as a teacher would
   *  before you read the passage. This is the heart of the in-depth experience. */
  teaching: string;
  /** The single idea to carry away. */
  keyIdea: string;
  /** The common misunderstanding this step is designed to prevent. */
  misconception?: string;
  /** Primary passage anchor (must be an authored unit). */
  passageId: string;
  /** Optional resonant readings from other traditions. */
  supportingPassageIds?: string[];
  theme?: string;
  chatMode?: ChatMode;
  chatPrompt: string;
  /** A contemplative exercise to actually do. */
  practice: string;
  /** A written reflection prompt. */
  journalPrompt: string;
  /** The checkpoint: what you should be able to recognize or do before moving on. */
  integration: string;
};

export type LearningTrack = {
  id: string;
  title: string;
  level: "Beginner" | "Intermediate" | "Advanced";
  focus: string;
  outcome: string;
  description: string;
  /** The intellectual arc of the whole path, in the teacher's voice. */
  arc: string;
  estimatedSessions: string;
  steps: LearningStepSpec[];
};

export const LEARNING_TRACKS: LearningTrack[] = [
  {
    id: "descent-of-the-cakra",
    title: "The Descent of the Cakra",
    level: "Intermediate",
    focus: "Śrī Vidyā: the śrīcakra as the body of the Goddess — and of you",
    outcome:
      "Walk the opening of the Yoginīhṛdaya as an initiation: from fitness and secrecy, through the threefold agreement and the cosmos arising from self-recognition, down into the diagram's unfolding, and back inward through the subtle body.",
    description:
      "An initiatic path through the Heart of the Yoginī (Cakrasaṃketa, ślokas 1–35), walked gate by gate.",
    arc:
      "The Yoginīhṛdaya does not call its chapters lessons but saṃketas — appointed encounters. So this path is itself a saṃketa: an agreed sequence of meetings through which the secret descends, ear to ear. You do not advance by reading the next step; you advance by passing a gate — a practice that must ripen first. We begin by becoming askable (fitness, secrecy, the sky-going heart), receive the threefold agreement and why understanding is itself authority, witness the cosmos flash into being from consciousness seeing its own radiance, trace the long descent of that light into structure, senses, world and earth, and finally reverse the current — re-finding the whole diagram in the body and climbing to the partless summit.",
    estimatedSessions: "11 gates · ~20 min each",
    steps: [
      {
        id: "yh-threshold-question",
        title: "The Question That Opens the Absolute",
        orientation:
          "Gate 0 · The Threshold (Adhikāra). Before the cakra can be shown, the one who would see it must be made askable.",
        teaching:
          "Notice who speaks first. Not the god, but the Goddess — and she asks. Revelation here begins as a demand made from fullness, not from lack. This sets the posture of everything that follows: you do not seize this teaching, you petition it. The 'unknown meanings' (ajñātārtha) the Goddess asks Bhairava to reveal are not missing facts; they are senses the text withholds until they are desired within a relationship. So the work begins by un-knowing on purpose — loosening your certainties until your central concern becomes a living question again, one you can hold open without rushing to close it.",
        keyIdea: "Truth is drawn out by desire and address, not seized. Begin by becoming askable.",
        misconception:
          "That a wise response would mean feeling certain. Here revelation opens with a question asked from fullness.",
        passageId: "yoginihrdaya.yh_001",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "In Yoginīhṛdaya 1.1 the Goddess, who is fullness itself, still asks. Help me understand why revelation here begins as a demand made from fullness rather than from lack.",
        practice:
          "Before study, form one precise question and address it aloud, as to a presence: 'Speak this, completely.' Then read as one who has asked.",
        journalPrompt:
          "What do I already claim to know that keeps me from being taught? Can I hold my central concern as a question, without rushing to answer it?",
        integration:
          "You can hold your central concern as an open question without collapsing it into a quick certainty.",
      },
      {
        id: "yh-secrecy-khecara",
        title: "Whispered Ear to Ear — Secrecy and the Sky-Going State",
        orientation:
          "Gate 0 · The Threshold. Secrecy here is interiority, not concealment: what is withheld gathers heat.",
        teaching:
          "The teaching travels mouth to ear and is 'kept carefully hidden' — not as gatekeeping for its own sake, but because meaning received in trust and silence is a different object than meaning published flat. And the promise is enormous: the instant one truly knows this, one becomes khecara, the sky-goer. But the sky (kha) is the void at the hub of a wheel transposed inward — the open space of the heart. To move in that sky is liberation. Knowing, here, is not cleverness; it is the capacity for tested, loving, sustained attention. Feel how a truth withheld concentrates, gathering in the central void of the chest.",
        keyIdea: "The 'sky' you learn to move in is the open void of the heart; knowing it is freedom.",
        misconception:
          "That khecaratā is merely a magic power of flight. The sky is the inner void of consciousness; moving in it is liberation.",
        passageId: "yoginihrdaya.yh_002",
        supportingPassageIds: ["vijnana_bhairava.yukti_001"],
        theme: "secrecy",
        chatMode: "explain",
        chatPrompt:
          "Explain khecaratā in Yoginīhṛdaya 1.2–5: how is 'moving in the sky' really about the void (kha) of the heart, and why is secrecy tied to its efficacy?",
        practice:
          "Choose your most precious insight and, for one full day, do not speak it. Carry it silently. Let the unspoken truth gather as heat in the void of the chest.",
        journalPrompt:
          "Can I hold something precious in silence without needing to be seen holding it? What does the withheld truth do in me?",
        integration:
          "Silence around the work feels like fuel rather than deprivation.",
      },
      {
        id: "yh-threefold-samketa",
        title: "Threefold Co-Presence — Cakra, Mantra, Worship",
        orientation:
          "Gate I · The Agreement (Saṃketa). The architecture is named: one presence met in three modes.",
        teaching:
          "Saṃketa cannot be said in one word — agreement, appointed meeting-place, co-presence. The cakra does not depict the Goddess; the mantra does not refer to her; the worship does not commemorate her. Each is a rendez-vous where she and Śiva are actually present by agreement, and that co-presence is what makes the form efficacious. A true symbol is not a token you decode; it is an appointment you keep. The whole treatise unfolds these three modes — diagram, sound, rite — as one presence modulated three ways. Your task is to stop arriving at your sacred forms as reminders of something absent, and start arriving as one expected, to be met.",
        keyIdea: "A true symbol is a meeting-place you arrive at, not a sign you decode.",
        misconception:
          "That the diagram, mantra, and rite are representations of an absent deity. They are sites of real co-presence.",
        passageId: "yoginihrdaya.yh_003",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001"],
        theme: "ritual",
        chatMode: "explain",
        chatPrompt:
          "The term saṃketa (Yoginīhṛdaya 1.6) means agreement, meeting-place, and co-presence at once. Help me grasp how cakra, mantra, and pūjā are appointments rather than representations.",
        practice:
          "Take one daily sacred form — an image, a phrase, a small rite. Today, arrive at it on time and fully, expecting to be met there.",
        journalPrompt:
          "Do my sacred forms point at something absent, or are they places I actually go? Which one could become a meeting?",
        integration:
          "At least one of your forms has stopped being a reminder and become a meeting.",
      },
      {
        id: "yh-authority-of-knowing",
        title: "The Seat of Supreme Authority",
        orientation:
          "Gate I · The Agreement. Understanding is not a permission slip; it is assimilation to the will that animates the diagram.",
        teaching:
          "'So long as one does not know this triad, one does not become a bearer of the highest authority in the cakra.' This is not a password rule. To know the saṃketa is to be assimilated to the will (ājñā) that animates the diagram, so that your own command participates in hers. Incomprehension is not innocent here — it is exclusion from a sovereignty already latent in you. The diagram waits, inert, until understanding makes you its conduit. So the gate asks an uncomfortable question: where in your practice are you running on autopilot, enacting forms whose shape you have never understood?",
        keyIdea: "Where understanding is absent, authority is only borrowed; knowing the form makes you its conduit.",
        misconception:
          "That authority over a practice is conferred by permission or repetition. Here it is conferred by understanding.",
        passageId: "yoginihrdaya.yh_004",
        supportingPassageIds: ["siva_sutra.ss_i_1"],
        theme: "self",
        chatMode: "question",
        chatPrompt:
          "Yoginīhṛdaya 1.7 says one becomes a 'bearer of supreme authority' only by knowing the threefold agreement. Help me see why this is ontological participation, not a permission rule.",
        practice:
          "Pick one practice you perform without understanding its form. Withhold the autopilot and ask it: 'What presence are you the meeting-place of?'",
        journalPrompt:
          "Where in my practice am I running on autopilot, enacting a form whose shape I have never understood?",
        integration:
          "You would rather not perform a rite than perform one you do not understand.",
      },
      {
        id: "yh-five-energies-four-fires",
        title: "Five Energies, Four Fires",
        orientation:
          "Gate II · The Flashing (Sphurattā). Before tracing the diagram's parts, witness its birth as a living rhythm.",
        teaching:
          "The śrīcakra is not a static figure. It exists only as the conjunction of two opposed movements: five energies pouring out (sṛṣṭi) and four fires drawing back (laya). Remove the tension and there is no cakra at all. Reality is intrinsically rhythmic — creation and dissolution are not sequential events but simultaneous vectors, and the Goddess is the whole oscillation rather than either pole. Note the asymmetry: five against four. The cosmos leans, ever so slightly, toward appearing. You can find this same conjunction in the breath — and discover that the 'self' is not a thing but the standing pattern the two movements keep making.",
        keyIdea: "You are not a thing but a standing pattern that emission and reabsorption keep making.",
        misconception:
          "That the diagram is a static figure. Its very existence is the live conjunction of outflow and return.",
        passageId: "yoginihrdaya.yh_005",
        supportingPassageIds: ["yoga_spandakarika.sp_02"],
        theme: "emanation",
        chatMode: "practice",
        chatPrompt:
          "Turn Yoginīhṛdaya 1.8 (five emanative energies, four resorptive fires) into a breath practice in which I rest as the conjunction of sṛṣṭi and laya rather than as either pole.",
        practice:
          "Watch three full breaths. On each in-breath sense laya — the world melting toward your centre; on each out-breath sense sṛṣṭi — the world flung outward. Rest as the meeting-point of the two.",
        journalPrompt:
          "Is my sense of self a thing, or a standing pattern that some movement keeps making?",
        integration:
          "You can feel yourself as the oscillation rather than as either pole.",
      },
      {
        id: "yh-sphuratta",
        title: "Sphurattā — The Cakra Springs from the Goddess Seeing Herself",
        orientation:
          "Gate II · The Flashing. The heart of the heart: manifestation is reflexive.",
        teaching:
          "The Supreme Power, freely taking the form of all that exists, beholds her own flashing-forth — and in that seeing, the cakra arises. Manifestation is reflexive: the world is not made by the Goddess as an external product; it is her looking at her own radiance. This rests on the distinction between prakāśa (the light of consciousness) and vimarśa (its self-awareness); sphurattā is the live hinge where light becomes aware of itself as light, and that very self-awareness emits the cosmos. Nothing compels it — creation is free play (svecchā), not necessity. Your own moments of suddenly catching yourself being aware are micro-instances of the same flash from which a universe springs.",
        keyIdea: "Catching yourself in the act of being aware is the same flash from which a world springs.",
        misconception:
          "That the world is produced by the Goddess as an external object. It is her self-recognition taking form.",
        passageId: "yoginihrdaya.yh_006",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001", "siva_sutra.ss_i_5"],
        theme: "light",
        chatMode: "practice",
        chatPrompt:
          "Yoginīhṛdaya 1.9 says the cakra arises when the Goddess perceives her own sphurattā. Help me practice catching the 'flash' of self-aware awareness as a taste of that arising.",
        practice:
          "Once today, the instant you notice you are aware, catch the small flash of realising you are present. Do not analyse it. Stay one breath in it as sphurattā — the flash from which a world is said to spring.",
        journalPrompt:
          "Have I ever caught myself in the very act of being aware? What was present in that flash before I named it?",
        integration:
          "You have caught the flash at least once and recognised it as the same act the verse describes.",
      },
      {
        id: "yh-ninefold-womb",
        title: "From the Void-A and the Bindu — The Ninefold Womb",
        orientation:
          "Gate III · The Descent (Avatāra). Now trace the fall from light into world; it begins with structure, not matter.",
        teaching:
          "From the meeting of the unmanifest (void-A) and the bindu streams not a thing but a seat — the womb-throne of the three levels of the Word. And its first offspring are not earth or water but structure: dharma and its opposite, the selves, and above all the triad knower–knowable–knowing. Reality is cognitive at its root. The subject, the object, and the act between them are not brute givens; they are the womb's first children, a 'compact mass of consciousness-and-bliss' (cidānandaghana). The neutral furniture of your experience — that there is a me here perceiving a world there — is itself the first emanation of a luminous point.",
        keyIdea: "Subject, object, and the knowing between them are the cosmos's first children, not neutral givens.",
        misconception:
          "That the world is first physical and only later cognized. Here it is cognitive at its very root.",
        passageId: "yoginihrdaya.yh_007",
        supportingPassageIds: ["mandukya_upanishad_and_gaudapada_karika.muk_001"],
        theme: "consciousness",
        chatMode: "explain",
        chatPrompt:
          "In Yoginīhṛdaya 1.10cd–13 the first emanation is the triad knower–knowable–knowing. Help me understand why reality here is cognitive at its root rather than physical-then-known.",
        practice:
          "Take one perception. Notice its three children — knower, known, and the live knowing between. Hold all three at once for three breaths as a single field.",
        journalPrompt:
          "What do I treat as the neutral furniture of experience — the given that needs no explanation?",
        integration:
          "The split between you and what you perceive has, for a moment, stopped feeling absolute.",
      },
      {
        id: "yh-expanding-triangles",
        title: "The Expanding Triangles — Consciousness Differentiates into the Senses",
        orientation:
          "Gate III · The Descent. The diagram's geometry is the structure of perception itself.",
        teaching:
          "As the womb expands through its triangles, what is generated is the apparatus of experience itself: the phonemes (sound), the elements (world), and the senses (cognition) — laid on one nested figure, asserting they are one differentiation seen three ways. Ambikā, the Mother, sits still at the centre, ringed by the vowels, the seed-powers of all speech, while the whole expansion is governed by a 'fire of resorption' — even creation carries the counter-movement of return. When you hear a sound or see a colour, you are reading one of these triangles: a local flash of the same consciousness the whole diagram maps. Perception is the cosmos perceiving itself, not a subject sampling an outside.",
        keyIdea: "Perception is the cosmos perceiving itself — a local radiance, not a transaction with an outside.",
        misconception:
          "That the senses passively receive an independent world. Senses and their objects are co-emanated from the same point.",
        passageId: "yoginihrdaya.yh_008",
        supportingPassageIds: ["siva_sutra.ss_i_1"],
        theme: "consciousness",
        chatMode: "practice",
        chatPrompt:
          "Yoginīhṛdaya 1.14–18 maps sound, world, and the senses onto one expanding figure. Give me a practice for experiencing an act of perception as a radiance flashing from a still centre.",
        practice:
          "Choose one sense — hearing. For ten breaths attend not to what you hear but to the act of hearing as a radiance flashing from a still centre.",
        journalPrompt:
          "When I perceive, do I experience myself as receiving a world, or as a world appearing?",
        integration:
          "An ordinary act of perception has felt, briefly, like a radiance rather than a transaction.",
      },
      {
        id: "yh-five-portions",
        title: "The Five Portions — From Pure Consciousness to Earth",
        orientation:
          "Gate III · The Descent. The whole diagram is a scale model of reality's descent, read center to edge.",
        teaching:
          "The five kalās map onto the nested figures: pure consciousness at the inmost point, and earth at the outermost square. The direction is the teaching — the highest reality is the smallest, innermost point; the grossest is the largest outer ring. Magnitude is a mark of descent, not importance. To move inward across the diagram is to ascend through the levels of being toward the source; to move outward is to watch consciousness condense into world. So the world's solidity is not opposed to spirit; it is spirit's outermost shining, the place where consciousness has become earth — and can therefore be traced back home.",
        keyIdea: "Solid matter is not the opposite of spirit but its outermost shining — traceable back to the source.",
        misconception:
          "That transcendence means height or escape from matter. Here transcendence is innerness, and matter is its outer edge.",
        passageId: "yoginihrdaya.yh_009",
        supportingPassageIds: ["isavasya_upanishad.isa_001"],
        theme: "emanation",
        chatMode: "explain",
        chatPrompt:
          "Yoginīhṛdaya 1.19–21 maps the five kalās from cit at the centre to earth at the outer square. Help me understand why the world's solidity is the outermost shining of consciousness, not its opposite.",
        practice:
          "Look at the most ordinary solid object near you. Regard it as nivṛtti — the outer edge of consciousness condensed to earth. Trace one step inward, from its solidity to your bare awareness of it, and rest there.",
        journalPrompt:
          "Do I treat the world's solidity as the opposite of spirit? Can I feel matter and awareness as two ends of one continuum?",
        integration:
          "Solid matter and awareness feel like two ends of one continuum, not two worlds.",
      },
      {
        id: "yh-inverted-hierarchy",
        title: "The Inverted Hierarchy and the Erotic Point",
        orientation:
          "Gate III · The Descent. The supreme is not only 'deep within' — it saturates the busiest outer ring.",
        teaching:
          "Counted from the outside in — the order of return — the peaceful, highest energy is found pervading the outermost cakras, and the heat of action burns at the centre. The supreme is not only deep within; it saturates every level, periphery included. And the whole figure is declared a form of kāmakalā — the glyph of the desiring union of Śiva and Śakti — whose deepest nature is prasāra, expansion. The cosmos is not a neutral structure but an erotic one: it exists because two poles desire and unite, and its essence is verb, not noun — generous overflow. This dismantles the cliché that depth means withdrawal to a still inner point.",
        keyIdea: "The same divinity saturates the busiest outer ring; reality's essence is generous overflow, not a still point.",
        misconception:
          "That depth always means withdrawing inward to stillness. The supreme equally pervades the outer, active periphery.",
        passageId: "yoginihrdaya.yh_010",
        supportingPassageIds: ["tao_te_ching.ttc_md_001"],
        theme: "eros",
        chatMode: "compare",
        chatPrompt:
          "Yoginīhṛdaya 1.22–24 inverts the hierarchy (śāntā at the periphery) and calls the cakra a form of kāmakalā whose nature is expansion. Help me find the supreme in the busy, outer part of my day rather than only in stillness.",
        practice:
          "Find the busiest, most peripheral part of your day. Instead of withdrawing to find depth, look for the supreme in it: let one ordinary act be felt as the expansion of a fullness, not a distraction from it.",
        journalPrompt:
          "Do I believe depth requires withdrawal from the busy surface of life? Where did I find the sacred in a 'peripheral' moment?",
        integration:
          "You have located the sacred in a 'peripheral' moment without retreating from it.",
      },
      {
        id: "yh-interiorize",
        title: "Interiorizing the Diagram — The Cakra in the Subtle Body",
        orientation:
          "Gate IV · The Return (Antaryāga). The current reverses: the external diagram is drawn back into your own axis and climbed.",
        teaching:
          "Now re-find the whole figure within. Its nine parts are distributed along the central channel from the base lotus to the great point above the head; to build the cakra in worship and to build yourself in yoga become one act. The ascent is graded by a phenomenology of dissolution: meditation 'with parts' (sakala) while images still hold; 'with-and-without parts' through the thinning resonances of the seed-sound HRĪṂ; and 'partless' (niṣkala) at the summit. The terminus is not a higher form but the formless 'Supremely Great,' unbounded by space or time, self-beautiful, awhirl with bliss. The path is a controlled de-thickening of attention — ending not in blankness but in unbounded, self-delighting plenitude.",
        keyIdea: "Liberation is a controlled de-thickening of attention — from image, to sound, to a plenitude past form.",
        misconception:
          "That the formless summit is blankness or void-as-absence. It is self-beautiful, blissful, unbounded plenitude.",
        passageId: "yoginihrdaya.yh_011",
        supportingPassageIds: ["vijnana_bhairava.yukti_001", "mandukya_upanishad_and_gaudapada_karika.muk_001"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Yoginīhṛdaya 1.25–27, 35 interiorizes the cakra in the body and ascends from sakala to niṣkala. Teach me the seed-sound dissolution practice that ends in the partless 'Supremely Great'.",
        practice:
          "Sit upright and intone a single syllable (use 'hrīṃ,' or simply 'mmm'). Follow it as it fades: vowel, then hum, then bare vibration, then the silence after. Each time it dissolves, rest one breath in the partless quiet above the sound before sounding it again.",
        journalPrompt:
          "Where, in my own body, is the centre of the diagram I have been studying? Did the silence after the sound feel fuller than the sound?",
        integration:
          "The silence after the sound has begun to feel fuller than the sound itself.",
      },
    ],
  },
  {
    id: "heart-of-recognition",
    title: "The Heart of Recognition",
    level: "Intermediate",
    focus: "Pratyabhijñā: remembering you are the Consciousness you have been seeking",
    outcome:
      "Walk Kṣemarāja's twenty sūtras as one recognition: from the sovereign Consciousness that is the ground of all, down through its self-contraction into the small, bewildered self, to the turn (pratyabhijñā) that reclaims your authorship — and out into a life lived as the Perfect 'I'.",
    description:
      "An initiatic descent-and-return through the Pratyabhijñāhṛdayam (the Heart of Recognition), sūtra by sūtra.",
    arc:
      "The Pratyabhijñāhṛdayam is the most compact map of awakening in the Kashmir Śaiva tradition: not a ladder you climb but a circle you complete. We begin by naming the ground — Consciousness, sovereignly free, as the only reality. Then we follow the descent: how that infinite light voluntarily contracts into a mind, into a small self, until it forgets that it is the author of its own world and mistakes its own powers for fate. At the floor of that forgetting we reach the hinge of the whole text — recognition (pratyabhijñā), the inward turn by which the mind discovers it was never anything other than the Consciousness it was seeking. From there we return: the fire that never went out, the bliss hidden in the gap of the breath, and finally the Perfect 'I' — liberation lived inside an ordinary day. You do not advance by reading the next sūtra; you advance by recognizing, in your own experience, what the sūtra names.",
    estimatedSessions: "9 gates · ~20 min each",
    steps: [
      {
        id: "phr-the-ground",
        title: "Consciousness Is the Sovereign Ground",
        orientation:
          "Gate I · The Ground. Before recognition can mean anything, we must name precisely what is to be recognized.",
        teaching:
          "The text opens not with an argument but with a declaration: citiḥ svatantrā viśva-siddhi-hetuḥ. Consciousness (citi — not your private, individual cetanā) is the sovereign cause of the universe's arising, holding, and dissolving — not one thing among others, not a product of the brain, but the field within which any thing whatever appears. The decisive word is svatantrā, absolute freedom: it is conditioned by nothing outside itself, because there is nothing outside itself. To begin the path of recognition is to entertain, as a hypothesis you will test in your own experience, that the awareness reading these words is not a small flicker inside a vast dead cosmos, but the very ground in which both 'cosmos' and 'small self' arise. Everything that follows is the patient unfolding of what this one sentence already contains.",
        keyIdea: "Consciousness is not a possession you have; it is the sovereign ground in which you and your world arise.",
        misconception:
          "That consciousness is a function produced by matter. Here it is the free ground, not the byproduct.",
        passageId: "pratyabhijnahrdayam.phr_001",
        supportingPassageIds: ["siva_sutra.ss_i_1"],
        theme: "consciousness",
        chatMode: "explain",
        chatPrompt:
          "Pratyabhijñāhṛdayam sūtra 1 says citi is svatantrā — sovereignly free. Help me understand why consciousness being the free ground, and not a product of matter, changes everything that follows.",
        practice:
          "Sit where you are. Notice the room, then the seeing of the room, then the fact that seeing needs no permission from the furniture. Follow that freedom back — past the myth of a private mind inside a dead cosmos — until awareness is not a flicker you own but the ground the world is painted on. Rest there as citi recognizing itself. Nothing outside has to grant this. There is nothing outside.",
        journalPrompt:
          "Do I experience awareness as something I have, or as the space in which everything — including 'me' — shows up?",
        integration:
          "You can entertain, in direct experience, that awareness is the ground rather than a product.",
      },
      {
        id: "phr-free-unfolding",
        title: "She Paints the World on Her Own Canvas",
        orientation:
          "Gate I · The Ground. If Consciousness is the only ground, what is the world made of — and what made it?",
        teaching:
          "Sūtra 2 answers the obvious objection. If Consciousness alone is, where does the world come from, and on what surface? svecchayā svabhittau viśvam unmīlayati — by her own will, she unfolds the universe upon her own canvas. The metaphor is exact: a canvas does not resist the painting; it is its very support — and here painter, paint, and canvas are one. There is no external matter, no recalcitrant stuff she must work against; only Consciousness freely modulating itself into the appearance of a world. The word is svecchayā, 'by her own will': creation is not compelled by necessity, lack, or law, but is free play (svātantrya). This is the deepest difference from a manufacturing God — the world is not built out of something, it is Consciousness voluntarily appearing as something.",
        keyIdea: "The world is not made out of other stuff; it is Consciousness freely appearing as a world, upon itself.",
        misconception:
          "That creation requires raw material or external necessity. Here it is free self-display — painter and canvas as one.",
        passageId: "pratyabhijnahrdayam.phr_002",
        supportingPassageIds: ["yoginihrdaya.yh_006"],
        theme: "freedom",
        chatMode: "explain",
        chatPrompt:
          "Sūtra 2 says the Goddess unfolds the universe 'on her own canvas' by free will. Help me grasp why there is no external material in this view, and why svātantrya (free play) matters.",
        practice:
          "Look at any object. Instead of 'a thing out there made of matter,' regard it for three breaths as an appearance arising in and as awareness — paint on a canvas not separate from the seeing.",
        journalPrompt:
          "Where do I assume the world is made of dead stuff I confront? What shifts if it is awareness appearing as form?",
        integration:
          "You can hold a perception as awareness's free self-display rather than as an encounter with alien matter.",
      },
      {
        id: "phr-contracted-aperture",
        title: "You Are That Same Light, at a Narrowed Aperture",
        orientation:
          "Gate II · The Contraction. Now the descent begins: how did the boundless become this single small one?",
        teaching:
          "How does infinite Consciousness become a finite person? Sūtra 4: the individual experient is that same Consciousness in which the universe has contracted (saṅkucita), so that the whole is still present — but as if seen through a narrowed aperture. The crucial claim is identity-in-difference: you are not a different kind of thing from universal Consciousness, nor a broken-off fragment, but that very Consciousness at a particular degree of contraction (saṅkoca). The whole is here; it is only apertured. This dismantles two errors at once — that you are merely a meat-machine that happens to glow, and that the divine is somewhere else, to be reached. The infinite is not far; it is here, contracted into the shape of 'me.' Recognition, when it comes, will be nothing other than the relaxing of that aperture.",
        keyIdea: "The small self is not a fragment or a machine but the whole Consciousness seen through a narrowed aperture.",
        misconception:
          "That the individual is a separate, lesser kind of being. It is the same Consciousness, contracted.",
        passageId: "pratyabhijnahrdayam.phr_004",
        supportingPassageIds: ["siva_sutra.ss_iii_1"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Sūtra 4 says the limited experient contains the universe 'in contracted form.' Explain saṅkoca as identity-in-difference rather than separation, and how to sense it.",
        practice:
          "When you next feel like a small, bounded self, silently note: 'the same light, narrowed.' Then feel for the wideness that the narrowing is a narrowing of.",
        journalPrompt:
          "Do I take myself to be a fragment cut off from the whole, or the whole at a particular aperture?",
        integration:
          "You can sense your limited self as a contraction of awareness rather than as a separate thing.",
      },
      {
        id: "phr-becoming-mind",
        title: "How Consciousness Becomes a Mind",
        orientation:
          "Gate II · The Contraction. The aperture has a mechanism — here is how the light hardens into a knower of objects.",
        teaching:
          "Sūtra 5 names the mechanism precisely: it is Consciousness itself that, descending from its pure status and contracting around the object (cetya), becomes the mind (citta). Mind is not a separate organ added to awareness; it is awareness at its most outturned, most object-bound, most forgetful of itself. Note the direction — the contraction is toward the knowable. Every time attention fixes on an object and loses the awareness in which the object appears, the descent of this sūtra is re-enacted in miniature. And this is liberating news disguised as cosmology: if mind is simply Consciousness turned outward and tightened, then the way home is not to destroy the mind but to reverse its direction — to let the outturned beam curve back toward its own source.",
        keyIdea: "Mind is not other than awareness; it is awareness contracted around objects and turned away from itself.",
        misconception:
          "That the mind must be silenced or destroyed. It need only be turned back toward its source.",
        passageId: "pratyabhijnahrdayam.phr_005",
        supportingPassageIds: ["siva_sutra.ss_i_2"],
        theme: "consciousness",
        chatMode: "explain",
        chatPrompt:
          "Sūtra 5 says Consciousness 'becomes the mind' by contracting toward the object. Give me a way to feel that outward contraction and reverse it.",
        practice:
          "Catch one moment of being wholly absorbed in an object (a screen, a worry). Gently curve attention back: notice the awareness in which the object appears. Feel the mind loosen from object toward source.",
        journalPrompt:
          "When did my mind today become wholly 'about' something and forget the awareness having it?",
        integration:
          "You can feel the mind as outturned awareness and curve it back toward its source at will.",
      },
      {
        id: "phr-forgotten-authorship",
        title: "The Exact Definition of Bondage",
        orientation:
          "Gate II · The Contraction. The descent reaches its floor — and a precise diagnosis of what is actually wrong.",
        teaching:
          "Sūtra 12 gives one of the most exact definitions of the human condition in any literature: to be a bound, transmigrating soul is to be bewildered by one's own powers, through complete ignorance of one's authorship of the fivefold act (manifesting, sustaining, dissolving, concealing, revealing). The bondage is not sin, not matter, not fate; it is a case of mistaken authorship. You are ceaselessly creating, sustaining, and dissolving your world of experience — and crediting the production to outside forces, so that your own powers return to you as a world that merely happens to you. The thief is dressed as the police. This is the floor of the descent and also its hinge: if bondage is forgotten authorship, then liberation cannot be the attainment of something new — it can only be the recognition of what you were doing all along.",
        keyIdea: "Bondage is not sin or matter but forgotten authorship: you author your experience and credit it to the outside.",
        misconception:
          "That liberation means acquiring a new state. It means recognizing the authorship you already exercise.",
        passageId: "pratyabhijnahrdayam.phr_012",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_010"],
        theme: "self",
        chatMode: "question",
        chatPrompt:
          "Sūtra 12 defines bondage as ignorance of one's authorship of the fivefold act. Help me see, in daily life, where I author my experience yet credit it entirely to the outside.",
        practice:
          "Pick one feeling-toned situation. Ask: 'What am I, right now, manifesting, sustaining, and dissolving in how I hold this?' Watch the authorship that usually hides.",
        journalPrompt:
          "Where today did my own creation return to me as a world that merely 'happened'? What was I authoring unawares?",
        integration:
          "You can catch yourself authoring an experience you would normally treat as imposed from outside.",
      },
      {
        id: "phr-the-turn",
        title: "Recognition — The Mind Turns and Becomes What It Sought",
        orientation:
          "Gate III · The Turn. Everything has descended to this single reversal; the whole text pivots here.",
        teaching:
          "Sūtra 13 is the turn the entire treatise is named for: when there is full recognition (parijñāna) of one's authorship, the mind itself, by becoming introverted (antarmukha), rises and becomes Citi, the supreme Consciousness. Pratyabhijñā means re-cognition: not learning a new fact but recognizing again what was always so — like suddenly recognizing the stranger before you as the friend you had been waiting for. Nothing is added; the very mind that was the contraction, simply by turning inward instead of outward, ascends to its own source. This is why the path is gentle rather than violent: the bound and the free are not two substances, and the whole distance between them is the direction of a single beam of attention. To recognize is to reverse the descent of sūtra 5 — and to arrive where you never actually left.",
        keyIdea: "Recognition is not gaining something new, but the mind turning inward and discovering it was always Consciousness.",
        misconception:
          "That awakening is a dramatic acquisition. It is re-cognition — knowing again what was never absent.",
        passageId: "pratyabhijnahrdayam.phr_013",
        supportingPassageIds: ["yoginihrdaya.yh_006", "siva_sutra.ss_i_5"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Sūtra 13 — the mind, becoming introverted, rises to Citi. Teach me pratyabhijñā as recognition (knowing again) rather than attainment, and how to make the inward turn.",
        practice:
          "The mind is already rushing the door — the next message, the next face, the next proof. For five minutes, do not chase it and do not stuff it back in. Soften the outward lean. Let looking turn toward the looker the way an exhale turns toward home. You cannot force recognition. You can stop fleeing the one who is looking. What meets you there is not an empty room. It is the mind discovering it was never other than the light it sought.",
        journalPrompt:
          "Have I ever 'recognized' awareness as what I already was, rather than reached for it as something far? What was that like?",
        integration:
          "You can perform the inward turn and taste recognition as remembering, not acquiring.",
      },
      {
        id: "phr-fire-never-out",
        title: "The Fire That Was Never Extinguished",
        orientation:
          "Gate IV · The Return. After the turn, a reassurance: the source was never truly lost, even at the bottom.",
        teaching:
          "Sūtra 14: the Fire of Consciousness, though dimmed in the lower stage, never wholly ceases — even there it partially consumes the fuel of the knowables. This is a tender and important step after the turn. It tells you that during the entire descent — through contraction, mind, bewilderment, the whole of forgotten authorship — the fire of awareness was still burning, still quietly assimilating every experience. You were never actually disconnected; you were only unaware of the burning. So recognition is not the lighting of a fire that had gone out, but the noticing of a fire that never did. This dissolves the anxiety that you must generate awakening from scratch, or that lost time is lost forever: the fuel of every experience you have ever had was, all along, feeding the same flame.",
        keyIdea: "Awareness never goes out; even in the deepest forgetting, the Fire of Consciousness keeps quietly burning.",
        misconception:
          "That you must kindle awareness from nothing. It has been burning throughout the entire descent.",
        passageId: "pratyabhijnahrdayam.phr_014",
        supportingPassageIds: ["siva_sutra.ss_i_5"],
        theme: "light",
        chatMode: "explain",
        chatPrompt:
          "Sūtra 14 says the Fire of Consciousness keeps burning even when covered. Help me feel that awareness was never actually lost, even in my times of deepest forgetting.",
        practice:
          "Recall a time you felt most lost or unaware. Notice: something was still aware of even that. Feel the fire that was burning beneath the forgetting — and that is reading this now.",
        journalPrompt:
          "Can I find the awareness that was present even in my most unconscious, contracted moments?",
        integration:
          "You trust that awareness was never absent, only unnoticed — even at your lowest.",
      },
      {
        id: "phr-the-middle",
        title: "Unfolding the Middle",
        orientation:
          "Gate IV · The Return. From recognition to a repeatable practice: the secret of the centre.",
        teaching:
          "Sūtra 17: by the unfolding of the Middle (madhya), the bliss of Consciousness is attained. Madhya — 'the middle' — is one of the most generative terms in the tradition: the central channel, the gap between two breaths, the pause between two thoughts, the still point between any two states. The teaching is that the centre is not a location but a seam, and at every seam in experience the contraction momentarily releases and the source shines through. So practice need not wait for special conditions — it lives in the cracks of ordinary experience. To 'unfold the middle' is to dwell in these gaps until they open: the hinge between in-breath and out-breath, the silence between words, the instant between perception and naming. Bliss (ānanda) here is not an added pleasure but the native tone of Consciousness uncontracted, found simply by slipping into its own centre.",
        keyIdea: "The 'middle' — the gap between breaths, thoughts, and states — is where contraction releases and the source shines through.",
        misconception:
          "That bliss must be produced or imported. It is the native tone of awareness, found in the gap.",
        passageId: "pratyabhijnahrdayam.phr_017",
        supportingPassageIds: ["vijnana_bhairava.yukti_001", "yoga_spandakarika.sp_02"],
        theme: "meditation",
        chatMode: "practice",
        chatPrompt:
          "Sūtra 17 — the bliss of Consciousness by 'unfolding the middle' (madhya). Teach me to use the gaps between breaths and thoughts as the doorway.",
        practice:
          "Rest attention on the turning-point between your out-breath and in-breath. Do not hold the breath; simply inhabit the pause. Let it widen on its own a few times, sensing it as the 'middle' opening.",
        journalPrompt:
          "Where are the 'gaps' in my day — between tasks, breaths, words — and what is present when I enter them instead of filling them?",
        integration:
          "You can find and rest in the 'middle' — a gap in experience — and feel the contraction ease there.",
      },
      {
        id: "phr-perfect-i",
        title: "The Perfect 'I' — Liberation While Living",
        orientation:
          "Gate IV · The Return. The terminus: recognition matured into a way of being, not a state to maintain.",
        teaching:
          "Sūtra 20 completes the arc: by entering the Perfect 'I'-consciousness (pūrṇāhantā) — whose nature is Light (prakāśa), Bliss (ānanda), and the great power of Mantra — one attains a perpetual lordship over the 'wheel' of one's own powers. This is jīvanmukti: liberation while still embodied, still perceiving, still acting. Note what it is not — not a trance to be guarded, not the erasure of the world, not a permanent special experience. It is a recovered relationship to the very same life: the powers that once bewildered you (sūtra 12) are now wielded as yours. 'Perfect I' does not mean an inflated ego; it means the 'I' that has reabsorbed the whole, so that 'I' and 'all this' are no longer two. The path that began by naming Consciousness as the sovereign ground ends with you standing knowingly as that ground, in the midst of an ordinary day. Recognition is complete when it no longer needs to be sustained — because nothing is left over to contract.",
        keyIdea: "The end is liberation while living: standing knowingly as the Consciousness you are, wielding your own powers in ordinary life.",
        misconception:
          "That the goal is a permanent trance or a world-erasing state. It is full 'I'-consciousness lived inside ordinary perception and action.",
        passageId: "pratyabhijnahrdayam.phr_020",
        supportingPassageIds: ["siva_sutra.ss_i_18", "pratyabhijnahrdayam.phr_015"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Sūtra 20 — the Perfect 'I' (pūrṇāhantā) and liberation while living. Help me understand jīvanmukti as a recovered relationship to ordinary life rather than a maintained trance.",
        practice:
          "Stand in an ordinary doorway. Feel the body pass through. Before the next room claims you, let \"I am\" sound — not the résumé, not the myth of me, but the simple light that is reading, walking, arriving. This knowing is not owned by the person in the doorway. It is the same light in every being, at every scale. Say it once, quietly: iti śivam. Then go through.",
        journalPrompt:
          "What would my ordinary day be like if I lived it as the Consciousness recognizing itself, rather than as a self chasing it?",
        integration:
          "Recognition is becoming a standpoint you live from, not a state you strain to keep.",
      },
    ],
  },
  {
    id: "three-doors-of-shiva",
    title: "The Three Doors",
    level: "Intermediate",
    focus: "The Śiva Sūtra's three upāyas: sudden recognition, the work of energy, the embodied path",
    outcome:
      "Walk the Śiva Sūtra as it was structured — three doors (upāyas) into one recognition: the sudden door of pure awareness (śāmbhava), the door of mind and effort (śākta), and the embodied door of breath, time, and ordinary life (āṇava).",
    description:
      "A path through Vasugupta's Śiva Sūtra, gate by gate, following its three sections as three means of awakening.",
    arc:
      "The Śiva Sūtra is not a ladder but a building with three doors, and the tradition reads its three sections as the three upāyas — three means suited to three temperaments and three moments. We enter first by the sudden door (śāmbhavopāya): no technique, only the direct recognition that consciousness is the Self, that even knowledge can bind, and that awakening can arrive as a vertical surge of aliveness. When the sudden door will not open, we take the door of energy (śāktopāya): mind turned into mantra, effort dignified as the practitioner, knowledge ripening into embodied reality. And when the mind too is restless, we take the embodied door (āṇavopāya): reclaiming even the limited mind as the Self, letting time become an ally, until the simple removal of confusion reveals a fulfilment that was never missing. Three doors — one room, and it was never locked.",
    estimatedSessions: "9 gates · ~20 min each",
    steps: [
      {
        id: "ss-caitanyam-atma",
        title: "Consciousness Is the Self",
        orientation:
          "Gate I · The Sudden Door (Śāmbhavopāya). The highest means is no means: we begin with a statement, not a technique.",
        teaching:
          "The Śiva Sūtra opens the sudden door with three words — caitanyam ātmā, 'Consciousness is the Self.' The tradition calls this section śāmbhavopāya, the means of Śiva: the path for those who can awaken by direct recognition alone, without mantra or breath-work. Notice the grammar — it does not instruct ('meditate,' 'purify'); it states what cannot be otherwise. Caitanya is not a faculty the self possesses but the self's very being: not 'I am conscious' but 'consciousness is what I am.' For the sudden door, that is already the whole teaching. If you can take it not as a proposition to believe but as a fact to verify by looking, the looking itself is the practice. There is nowhere to go, because the Self is not an object to reach — it is the awareness already reading this. The sudden door opens for whoever can stop reaching.",
        keyIdea: "Consciousness is not something the Self has; it is what the Self is — already present as this very awareness.",
        misconception:
          "That awakening needs a technique. The sudden door asks only for direct recognition of what is already so.",
        passageId: "siva_sutra.ss_i_1",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001"],
        theme: "awareness",
        chatMode: "explain",
        chatPrompt:
          "Śiva Sūtra I.1, caitanyam ātmā. Explain śāmbhavopāya — the 'sudden door' that uses no technique — and how to verify 'consciousness is the Self' by direct looking.",
        practice:
          "Look at whatever is nearest — the yellow of a leaf, the glow of the screen, a chair scraping. Do not hunt for a special state. Notice that all of it is already lit. Now stop following the objects and rest as the lighting itself. The sūtra is not asking you to become conscious. It is asking you to drop the fiction that there is a you over here and awareness over there. Stay until \"I am looking\" softens into looking looking.",
        journalPrompt:
          "Can I find the awareness that is reading this without doing anything to produce it?",
        integration:
          "You can recognize awareness directly, without a technique, as what you already are.",
      },
      {
        id: "ss-jnanam-bandhah",
        title: "Knowledge Is Bondage",
        orientation:
          "Gate I · The Sudden Door. A deliberate jolt: the very thing we trust to free us is named the chain.",
        teaching:
          "jñānaṃ bandhaḥ — 'knowledge is bondage.' The sūtra is meant to startle, and at the sudden door it does precise work. The knowledge meant is dualistic, limited knowing: the ceaseless stream of 'this, not that' by which awareness fences itself into a defined, defended identity. Every fixed self-concept — 'I am the kind of person who…' — is a piece of knowledge that contracts the boundless into the bounded. The trap is subtle because it includes spiritual knowledge: ideas about awakening can become the most prized identity of all, a new cage with finer bars. At the sudden door there is no fight with knowledge; there is only the immediate seeing that the knower of every concept is not itself a concept. The instant you notice that the awareness aware of a thought is not bound by it, the door is already open.",
        keyIdea: "Limited, fixed knowledge is the very mechanism that fences open awareness into a defended identity.",
        misconception:
          "That more knowledge — even spiritual knowledge — is always freeing. Held as identity, it binds.",
        passageId: "siva_sutra.ss_i_2",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_005", "astavakra_gita.asg_1_7"],
        theme: "knowledge",
        chatMode: "question",
        chatPrompt:
          "Śiva Sūtra I.2, jñānaṃ bandhaḥ. Help me see how even spiritual knowledge becomes a cage, and how the sudden door opens by noticing the knower is not itself a concept.",
        practice:
          "Catch the next naming: tree, morning, me. Feel how the word files the living thing into a known slot. For three breaths let the name stay, but refuse to let it finish the seeing. Watch rain, sun, and soil still moving in what you just called a tree. The bondage is not the word. It is the moment the word pretends to be the last word.",
        journalPrompt:
          "Which idea about myself — even a spiritual one — did I defend today as if it were the Self?",
        integration:
          "You can catch a self-concept hardening into a cage and notice the awareness that is not bound by it.",
      },
      {
        id: "ss-udyamo-bhairavah",
        title: "The Surge Is Bhairava",
        orientation:
          "Gate I · The Sudden Door. The sudden door has a felt form: a living upsurge, not only a calm insight.",
        teaching:
          "udyamo bhairavaḥ — 'the surge of awareness is Bhairava.' Here the sudden door reveals its energetic face. Udyama is the spontaneous welling-up of awareness — the sudden vividness that breaks through habit in a flash of wonder, beauty, shock, or the catch of breath before speech. The sūtra makes an astonishing identification: that surge is not a mood you generate; it is Bhairava, the absolute itself, momentarily un-contracted and self-aware. The Spanda tradition calls it the subtle tremor (spanda) at the root of all experience. For the sudden door this is decisive — recognition is not always a quiet, conceptual 'ah, I see'; it can arrive as a vertical jolt of aliveness. And because the surge is always available at the seams of experience, the sudden door has a handle you can actually find: catch the pulse, and you have caught Bhairava.",
        keyIdea: "Recognition has an energetic form: the spontaneous surge of vivid aliveness is the absolute briefly self-aware.",
        misconception:
          "That recognition is only a calm insight. It also arrives as a sudden, vertical surge of aliveness.",
        passageId: "siva_sutra.ss_i_5",
        supportingPassageIds: ["yoga_spandakarika.sp_02", "siva_sutra.ss_i_12"],
        theme: "awareness",
        chatMode: "practice",
        chatPrompt:
          "Śiva Sūtra I.5, udyamo bhairavaḥ. Turn the 'surge of awareness' into a brief embodied practice — where in ordinary experience can I catch this pulse?",
        practice:
          "Do not wait for a holy mood. Feel the next rise of life as it actually comes — the email that must be answered, the heat before a hard conversation, the first sip that wakes the mouth. That upsurge is not a problem to manage. Sit in it the way you sit in a flame: without backing up and without adding a story. If it is fierce, let it be fierce. The name of that intensity, undivided from the one who feels it, is Bhairava.",
        journalPrompt:
          "When did aliveness break through habit today, and what did the surge feel like before I named it?",
        integration:
          "You can locate the felt surge of awareness as a doorway, not only conceptual understanding.",
      },
      {
        id: "ss-cittam-mantrah",
        title: "Mind Is Mantra",
        orientation:
          "Gate II · The Door of Energy (Śāktopāya). When the sudden door won't open, we work through the mind — now the instrument, not the obstacle.",
        teaching:
          "The second section turns to śāktopāya, the means of energy (Śakti): the path for those who cannot simply recognize and must work through the mind. Its first sūtra reframes everything: cittaṃ mantraḥ — 'mind is mantra.' Ordinarily thought is noise, scattered and binding; but a mantra is sound that has become a vehicle of consciousness, sound that points back to its source. The teaching is that once recognition has begun, the mind itself can be used this way — not silenced, but turned into a mantra: a continuous reflective resonance that carries awareness toward itself. This is the genius of the door of energy — it does not demand a quiet mind as a precondition. It takes the very faculty that seemed to be the problem and makes it the path. Your thinking, rightly turned, becomes the means of your recognition.",
        keyIdea: "The mind need not be silenced to awaken; turned toward its source, thought itself becomes mantra.",
        misconception:
          "That you must first achieve a thought-free mind. The door of energy uses the mind as the very vehicle.",
        passageId: "siva_sutra.ss_ii_1",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_013"],
        theme: "meditation",
        chatMode: "explain",
        chatPrompt:
          "Śiva Sūtra II.1, cittaṃ mantraḥ — 'mind is mantra.' Explain śāktopāya and how the restless mind itself becomes the means rather than the obstacle.",
        practice:
          "Take one short phrase that points to awareness ('aware now,' or a name you trust). Let it repeat beneath your thinking for a few minutes — not to blank the mind but to bend its current back toward its source.",
        journalPrompt:
          "What is the habitual 'mantra' my mind already repeats? What would change if I gave it one that points home?",
        integration:
          "You can use a turned thought as a vehicle toward awareness instead of waiting for the mind to fall silent.",
      },
      {
        id: "ss-prayatnah-sadhakah",
        title: "Effort Is the Practitioner",
        orientation:
          "Gate II · The Door of Energy. This door asks for something the sudden door did not: sustained, willing effort.",
        teaching:
          "prayatnaḥ sādhakaḥ — 'effort is the practitioner,' or 'sustained effort is what accomplishes.' With this sūtra the text makes a decisive, humbling turn. At the sudden door, effort was beside the point — even an obstacle. Here, on the path of energy, effort (prayatna) is the very thing that does the work: not the obstacle to grace but the form grace takes in someone who must practice. Note the kind of effort meant, though — not anxious striving toward a distant goal, but the warm, repeated, willing turning of the mind toward its source, the same gesture again and again. This dignifies practice for those who are not built for sudden awakening: your patient, unspectacular returning is not a lesser path — it is the practitioner itself. The doing is not in the way; rightly understood, the doing is the door.",
        keyIdea: "On the path of energy, sustained willing effort is not the obstacle to awakening — it is what accomplishes it.",
        misconception:
          "That effort always blocks grace. On the door of energy, the right kind of effort is the means itself.",
        passageId: "siva_sutra.ss_ii_2",
        supportingPassageIds: ["bhagavad_gita.bg_06_35"],
        theme: "practice",
        chatMode: "question",
        chatPrompt:
          "Śiva Sūtra II.2, prayatnaḥ sādhakaḥ — 'effort is the practitioner.' Help me understand the right kind of effort on the path of energy, distinct from anxious striving.",
        practice:
          "Choose one small turning-toward-awareness and repeat it deliberately ten times across today (e.g., at each doorway). Treat the repetition itself, not any result, as the practice succeeding.",
        journalPrompt:
          "Do I secretly believe effort is 'unspiritual'? Where would patient repetition serve me better than waiting for a breakthrough?",
        integration:
          "You can value sustained, willing repetition as a legitimate door, not a lesser substitute.",
      },
      {
        id: "ss-vidya-sharira",
        title: "When Knowledge Becomes Flesh",
        orientation:
          "Gate II · The Door of Energy. The fruit of this door: understanding stops being abstract and becomes embodied reality.",
        teaching:
          "vidyā-śarīra-sattā mantra-rahasyam — 'knowledge becoming an embodied reality is the secret of mantra.' This is the ripening of the entire second door. You began by turning the mind into mantra (II.1) and dignifying effort (II.2); now the sūtra names the result — a point where what you understood as an idea becomes the very substance of your experience: knowledge with a body. The 'secret of mantra' is exactly this transformation: a true mantra is not a phrase you know about but a knowing you have become, so that the recognition no longer needs to be thought, because it is now lived in the nerves. This is the difference between a person who can explain non-duality and a person whose seeing has been re-grained by it. The door of energy completes when your insight is no longer information you carry, but a reality you are.",
        keyIdea: "The 'secret of mantra' is knowledge becoming embodied — insight that has passed from idea into lived substance.",
        misconception:
          "That understanding a teaching is the goal. The aim is for the knowing to become the body of your experience.",
        passageId: "siva_sutra.ss_ii_3",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_016"],
        theme: "knowledge",
        chatMode: "practice",
        chatPrompt:
          "Śiva Sūtra II.3 — knowledge becoming embodied reality as 'the secret of mantra.' Help me move an insight from something I know into something I am.",
        practice:
          "Take one insight you 'know' but don't yet live. For one full day, act once as if it were already true in your body — let understanding pass into a single concrete action.",
        journalPrompt:
          "Which truth do I understand perfectly and embody not at all? What would it look like as flesh, not idea?",
        integration:
          "You can tell a teaching you know about from one that has become embodied — and move at least one from the first to the second.",
      },
      {
        id: "ss-atma-cittam",
        title: "The Mind Is the Self",
        orientation:
          "Gate III · The Embodied Door (Āṇavopāya). The most graduated door begins by reclaiming the one thing the others set aside: the limited mind.",
        teaching:
          "The third section is āṇavopāya, the means of the limited individual (aṇu): the most embodied, graduated path — for those who must work through breath, body, attention, and time. Its opening sūtra seems to contradict the whole book: ātmā cittam — 'the mind is the Self.' Section I had insisted that consciousness is the Self and knowledge is bondage; now, at the embodied door, even the limited mind is reclaimed as the Self. The contradiction is the teaching. On the highest door you transcend the mind; on the embodied door you cannot yet, so you are told something kinder and more workable — this very mind, restless and ordinary and contracted, is not other than the Self either. You do not have to escape it to begin; you begin exactly here, with the mind you actually have, treating it not as the enemy of awakening but as the nearest form of it. The embodied door opens to whoever will start from where they are.",
        keyIdea: "The embodied path begins by reclaiming the ordinary, limited mind itself as a form of the Self — not the enemy.",
        misconception:
          "That the mind must be defeated before the path begins. The embodied door starts with the mind you actually have.",
        passageId: "siva_sutra.ss_iii_1",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_004"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Śiva Sūtra III.1, ātmā cittam — 'the mind is the Self' — seems to contradict I.1. Explain āṇavopāya and why the embodied door reclaims the ordinary mind.",
        practice:
          "Instead of fighting your restless mind today, once, regard it warmly: 'this too is the Self, contracted.' Begin your practice from inside that ordinary mind rather than waiting for a better one.",
        journalPrompt:
          "Do I treat my ordinary mind as the obstacle to 'real' practice? What changes if it is the doorway?",
        integration:
          "You can begin from your actual, ordinary mind rather than postponing practice until it improves.",
      },
      {
        id: "ss-time-ally",
        title: "Time Becomes an Ally",
        orientation:
          "Gate III · The Embodied Door. The embodied path unfolds in time — and learns to make time a friend rather than a pressure.",
        teaching:
          "Śiva Sūtra III.11 teaches that through time, the Self comes to abide in itself. On the sudden door, time is irrelevant — recognition is instantaneous or nothing. But the embodied door is explicitly graduated, and so it must befriend duration. Here time is not the enemy that ages and erodes, nor the pressure that whispers you are behind; it is the medium in which repeated recognition slowly stabilizes into a resting-in-itself. The aṇu, the limited one, cannot leap — but the limited one can return, and return, and return, and time is precisely what allows those returns to accumulate into a settled abiding. This is deep consolation for the embodied path: you are not failing because awakening is taking time. Taking time is the method. The Self abides in itself by the patient grace of duration — the way water finds its level not at once, but surely.",
        keyIdea: "On the embodied path, time is not the enemy but the medium in which repeated return ripens into stable abiding.",
        misconception:
          "That taking time means failing. For the graduated door, duration is the very method of stabilization.",
        passageId: "siva_sutra.ss_iii_11",
        supportingPassageIds: ["siva_sutra.ss_ii_2"],
        theme: "practice",
        chatMode: "question",
        chatPrompt:
          "Śiva Sūtra III.11 — through time, the Self abides in itself. Help me make time an ally on the embodied, graduated path rather than a source of pressure.",
        practice:
          "Pick one recognition practice and commit to it at the same time each day for several days. Let the repetition over time — not any single session — be the point.",
        journalPrompt:
          "Where am I treating the slowness of my growth as failure? What would change if duration were the method, not the obstacle?",
        integration:
          "You can let practice ripen over time without reading slowness as failure.",
      },
      {
        id: "ss-removal-of-confusion",
        title: "Nothing Is Gained; Confusion Simply Lifts",
        orientation:
          "Gate III · The Embodied Door. The terminus of all three doors: fulfilment is not an acquisition but the lifting of a fog.",
        teaching:
          "The text closes with a sūtra of great quietness: from the removal of confusion (moha), fulfilment arises. After three doors and forty-odd sūtras, the end is not a fireworks attainment but a subtraction — nothing is added, nothing new is reached; confusion simply no longer obscures what was already, fully, the case. This reframes the entire journey backward. The Self was never absent; the powers were always yours; the awareness was always the ground. What stood between you and fulfilment was never a missing thing to acquire, but only a fog to disperse. And this is why there were three doors rather than one: confusion has many densities, and different temperaments need different means to thin it — but every door opens onto the same room, and that room was never locked. The path ends where it secretly began: in what is already complete, now seen without the haze.",
        keyIdea: "Fulfilment is not gained but uncovered: remove the confusion and what was always complete simply shows.",
        misconception:
          "That awakening adds something you lack. It only removes the fog over what was already the case.",
        passageId: "siva_sutra.ss_iii_12",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_020", "the_book_of_chuang_tzu.zhuangzi_md_004"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Śiva Sūtra III.12 — fulfilment from the removal of confusion. Help me understand why the path ends in subtraction, not acquisition, and why there were three doors to one room.",
        practice:
          "Bring to mind something you are seeking 'out there.' Ask instead: 'What confusion, if it lifted, would reveal this as already here?' Sit with the question without rushing to answer it.",
        journalPrompt:
          "What am I trying to acquire that might already be present beneath a confusion I could let lift?",
      integration:
        "You can relate to awakening as the lifting of confusion rather than the acquisition of a new state.",
      },
    ],
  },
  {
    id: "the-112-doorways",
    title: "The 112 Doorways",
    level: "Intermediate",
    focus: "Vijñāna Bhairava Tantra: the breath, the senses, and the gaps as gates into Bhairava",
    outcome:
      "Walk ten of the 112 dhāraṇās as living doorways — breath, sound, void, delight, and the seam between states — until you can find the open gate of awareness in any ordinary moment.",
    description:
      "An initiatic path through the Vijñāna Bhairava Tantra: ten dhāraṇās, gathered into six gates, each a doorway from ordinary experience straight into Bhairava.",
    arc:
      "The Vijñāna Bhairava opens with the Goddess asking what Bhairava truly is — beyond syllable, ritual, and cosmology — and Bhairava answers not with a doctrine but with one hundred and twelve doorways. Each dhāraṇā is a small, exact contemplation that, fully entered, dissolves the meditator into the meditated. The radical generosity of the text is that it privileges no single method: a breath, the edge of a syllable, a patch of empty sky, a surge of delight, the gap between two thoughts — any of these, pressed all the way through, opens onto the same boundless consciousness. So this path does not march through all 112. It gathers ten into six gates — Breath, Sound, Void, Delight, the Seam between states, and Everywhere — and trains you to recognize the structure they share: every doorway is a place where the grasping mind, for an instant, finds nothing to hold, and in that holdlessness the ground reveals itself. Walk these few well and the other hundred open of their own accord.",
    estimatedSessions: "10 doorways · ~15 min each",
    steps: [
      {
        id: "vbt-breath-utterance",
        title: "The Goddess Is the Breath You Are Already Breathing",
        orientation:
          "Gate I · The Breath. We begin with the one practice you have been performing every moment, asleep and awake, and have never once had to begin.",
        teaching:
          "The very first dhāraṇā places the divine not in some far attainment but in the breath itself. The out-breath (prāṇa) rises and the in-breath (jīva, apāna) descends; this ceaseless rising and falling is the Supreme Goddess uttering herself as your living body — the unrepeated mantra haṃsa that breathes itself without your effort. To meditate here is not to control the breath but to feel it as Her speech: the very pulse that keeps you alive is already the Absolute saying 'I am.' You do not generate this utterance; you overhear it. The whole doorway is to stop owning the breath ('I am breathing') and begin to recognize it ('breathing is happening, and it is Her'). This is parā vāk in its most intimate form — the supreme Word vibrating as your own quiet inhalation.",
        keyIdea: "The breath is not yours to perform; it is the Goddess uttering herself as you — the mantra you never have to start.",
        misconception:
          "That this is a breathing technique. It is the reverse: noticing the breath that breathes itself, without your management.",
        passageId: "vijnana_bhairava.yukti_001",
        supportingPassageIds: ["yoginihrdaya.yh_001", "pratyabhijnahrdayam.phr_017"],
        theme: "breath",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 1 — the breath as the Goddess's self-utterance (haṃsa). Guide me to feel the rising and falling breath as Her speech rather than as something I am doing.",
        practice:
          "You do not begin this breath. Feel it starting at the nostrils and, at the same time, rising from the low belly — two doors of one current. For five cycles, hold both doors without making the breath better. The Goddess is not a visitor you invite. She is the speech already happening as you. When thought tries to run the inhale, return to the two doors and let her finish the sentence.",
        journalPrompt:
          "When I stop 'doing' my breath and let it breathe me, what shifts in who I take myself to be?",
        integration:
          "You can rest as the witness of the breath that breathes itself, sensing it as the Goddess's living utterance.",
      },
      {
        id: "vbt-the-center",
        title: "The Center Where the Breath Turns",
        orientation:
          "Gate I · The Breath. Having felt the breath as Her utterance, we slip into the silent hinge between its two halves.",
        teaching:
          "The second dhāraṇā points to the madhya — the Center. At the very top of the out-breath and the very bottom of the in-breath there is an instant when the breath is neither flowing out nor drawing in. In that pause the power (śakti) carried by the breath stops travelling and reveals itself, resting in the Center. This is the most precise doorway in the entire text: not the breath, but the gap that brackets it — the still point on which both movements turn. Do not manufacture this pause by holding the breath; simply notice the natural turn and let attention rest in it. And mark this well: the Center between two breaths is the same Center between two thoughts, between sleeping and waking, between any two states whatsoever. Learn it here, in the breath, and you are given the master key to every remaining gate on this path.",
        keyIdea: "Between the out-breath and the in-breath is a still hinge; rest there and śakti, no longer travelling, reveals herself.",
        misconception:
          "That you should hold the breath to create the pause. You only notice the pause that is already, naturally, occurring.",
        passageId: "vijnana_bhairava.yukti_002",
        supportingPassageIds: ["siva_sutra.ss_ii_13", "pratyabhijnahrdayam.phr_017"],
        theme: "the-center",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 2 — the Center (madhya) between the breaths. Help me find the natural turning point without holding my breath, and rest attention there.",
        practice:
          "At the turn of the next breath — not the inhale, not the exhale, the hinge — stop helping. Do not send the wind out to the world and do not pull it back into the knot of me. Hover at the threshold the way a candle holds its own pause. Rest there until the naming thins. What remains in that center, without a story, is the form the text calls Bhairava.",
        journalPrompt:
          "What did I notice in the gap between the breaths that I never notice in the breaths themselves?",
        integration:
          "You can locate and rest in the still Center between the breaths without manipulating the breath to find it.",
      },
      {
        id: "vbt-edge-of-sound",
        title: "The Silence at the Birth and Death of a Sound",
        orientation:
          "Gate II · The Sound. We leave the breath for the subtler edge where any sound first arises and finally dissolves.",
        teaching:
          "This dhāraṇā says: whoever fosters the perception of the very beginning, or the very ending, of any syllable becomes filled with the void. Every sound — a chanted syllable, a struck bell, a spoken word — arises out of silence and sinks back into it. The instruction is to ride attention to that razor-fine edge: the instant before the sound is fully sound, and the instant as it dissolves back into nothing. There, the mind that wants to seize 'a sound' discovers it has already slipped through its fingers, and into that ungraspability the spacious void (śūnya) floods. This is the real reason mantra liberates — not because a syllable is magic, but because its beginning and its ending are open doors. The middle of the sound is where the mind grasps; the edges are where Bhairava waits.",
        keyIdea: "Sound is bracketed by silence; attend to where it begins and where it ends and the void itself opens.",
        misconception:
          "That the power is in the loudness or meaning of the sound. The doorway is its edges — the silence it comes from and returns to.",
        passageId: "vijnana_bhairava.yukti_015",
        supportingPassageIds: ["siva_sutra.ss_i_4", "yoga_spandakarika.sp_02"],
        theme: "sound",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 15 — the void at the beginning and end of a syllable. Teach me to attend to the edges of a sound rather than its middle.",
        practice:
          "Chant a single long 'Oṃ' (or any sustained tone). Ignore the body of the sound; place all attention on the instant it begins out of silence and the instant it fades back. Repeat, each time resting a moment in the silence after. Five rounds.",
        journalPrompt:
          "What appeared in the silence at the edge of the sound that the sound itself was covering?",
        integration:
          "You can use the onset and fading of any sound as a doorway, resting in the void that brackets it.",
      },
      {
        id: "vbt-open-sky",
        title: "Gaze Into the Open Sky",
        orientation:
          "Gate III · The Void. From the edge of sound we step into the largest open doorway there is — the empty sky.",
        teaching:
          "Looking at the clear blue sky with an uninterrupted gaze, remaining completely still — all at once, the text promises, one attains the very nature of Bhairava. The mechanism is exquisitely simple: the eye seeks an object to land on, and the cloudless sky offers none. Finding nothing to fix upon, the gaze and the mind it carries are thrown back upon their own boundless, objectless nature, which is precisely the nature of Bhairava — vast, supportless, undivided. This is why emptiness is not nihilism here but the most direct revelation of fullness: when consciousness has nothing to grasp, it recognizes that it was never the small seer but the open space in which all seeing happens. Sky outside becomes sky within; the two are found to have the same nature.",
        keyIdea: "Given nothing to land on, the gaze falls back into its own objectless ground — and that ground is Bhairava.",
        misconception:
          "That you are staring at the sky to see something. You are letting the sky's emptiness empty you of the one who looks.",
        passageId: "vijnana_bhairava.yukti_056",
        supportingPassageIds: ["siva_sutra.ss_i_5", "astavakra_gita.asg_6_1"],
        theme: "void",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 56 — gazing into the cloudless sky until the mind dissolves. Help me understand why having no object to fix upon reveals Bhairava.",
        practice:
          "Find an open sky (or a blank, featureless expanse). Let the gaze rest softly into it without seeking anything, blinking as little as is comfortable, body still. When the mind reaches for an object and finds none, let it settle into the openness. A few minutes.",
        journalPrompt:
          "When my gaze had nothing to land on, what happened to the sense of being a separate 'looker'?",
        integration:
          "You can use any objectless openness — sky, a blank wall, the dark — to let the seeing mind fall back into its spacious source.",
      },
      {
        id: "vbt-delight-doorway",
        title: "Wherever the Mind Delights, Linger There",
        orientation:
          "Gate IV · Delight. The void was the empty door; now we discover that the fullest pleasures are doors too — if you know where to stand in them.",
        teaching:
          "This dhāraṇā overturns the ascetic assumption at a stroke: wherever the mind finds delight, it says, let your attention linger there — for in any such rapture the supreme reality shows itself. The secret is to shift attention from the object of pleasure to the felt rapture itself, the inner expansion. The beauty of a face, a chord of music, the first taste of water when thirsty — these are not temptations to be fled but flashes where consciousness briefly stops contracting and opens into its own bliss (ānanda). The pleasure is real, but its source is not the object; the object merely triggered the opening that was always available. Tantra's daring is to use the surge, not suppress it: ride the wave of delight back to the ocean of consciousness from which it rose.",
        keyIdea: "In any genuine delight, drop the object and rest in the rapture itself — that opening is consciousness tasting its own bliss.",
        misconception:
          "That pleasure is the obstacle. The pleasure is the doorway; the only error is mistaking the object for the source of the joy.",
        passageId: "vijnana_bhairava.yukti_046",
        supportingPassageIds: ["siva_sutra.ss_i_18", "yoga_spandakarika.sp_22"],
        theme: "delight",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 46 — wherever the mind delights, let attention linger. Teach me to turn from the object of pleasure to the felt rapture as a doorway to ānanda.",
        practice:
          "Next time a small delight arises — a sip of something good, a piece of music, sun on your skin — pause. Move attention off the object and onto the warm expansion in the chest and being. Stay there a few breaths after the trigger fades. Notice the bliss outlasts its cause.",
        journalPrompt:
          "When I lingered in the rapture itself rather than chasing the object, where did the joy seem to actually live?",
        integration:
          "You can treat any wholesome delight as a doorway by resting in the felt rapture rather than grasping its object.",
      },
      {
        id: "vbt-who-am-i",
        title: "When Neither Desire Nor Thought Arises, Who Am I?",
        orientation:
          "Gate IV · Delight. Delight showed the open expansion; now we find the same opening in the quiet trough where wanting itself falls still.",
        teaching:
          "This dhāraṇā offers a single luminous inquiry: 'When neither desire nor thought arises — who am I? Truly, I am just as I actually am.' There are moments, after a wish is satisfied or simply spent, when for an instant the mind wants nothing and thinks nothing. We usually rush past this trough toward the next wanting, but the text says to catch it and look: in the absence of desire and thought, what remains? Not a blank — a presence, awake and unconditioned, which is your actual nature laid bare without the costume of any craving. Desire and thought are not enemies; they are the waves whose subsiding lets you glimpse the still water you always were. The question is not answered with words but recognized in the gap: I am simply, already, this.",
        keyIdea: "In the gap where no desire or thought arises, what remains awake is your unconditioned nature — recognized, not concluded.",
        misconception:
          "That you must eliminate all desire to find the Self. You only need to notice the natural gaps where wanting briefly subsides on its own.",
        passageId: "vijnana_bhairava.yukti_069",
        supportingPassageIds: ["astavakra_gita.asg_1_7", "siva_sutra.ss_i_1"],
        theme: "self-inquiry",
        chatMode: "question",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 69 — 'when neither desire nor thought arise, who am I?' Help me use the natural trough after a desire subsides as a doorway to the unconditioned Self.",
        practice:
          "After your next desire is met (even a small one — a sip, a stretch), notice the brief lull before the next want arises. In that lull, ask once, gently: 'Who am I right now?' Do not answer; just feel what is present and awake. Repeat through the day.",
        journalPrompt:
          "In the moment when I wanted nothing and thought nothing, what was still unmistakably here?",
        integration:
          "You can recognize the desireless gap as a reliable doorway, resting as the presence that remains when wanting subsides.",
      },
      {
        id: "vbt-seam-between",
        title: "Take Refuge in the Gap Between Any Two States",
        orientation:
          "Gate V · The Seam Between States. We now generalize the Center: not only between breaths, but in the seam between any two experiences whatsoever.",
        teaching:
          "This dhāraṇā extends the teaching of the Center to its widest reach: contemplating the cognition of any two states or any two things, take refuge in the gap between them. Between one thought and the next, between an old mood released and a new one not yet arisen, between turning your attention from this object to that — there is always a seam, a near-instantaneous interval that the mind ordinarily skips. But that seam is not empty of you; it is full of you, undivided, before the next division begins. The practice is to slow down enough to inhabit the interval rather than the contents. Where the previous dhāraṇās gave you specific doorways — a breath, a sound, a delight — this one reveals that the doorway is structural: every transition in experience is a hairline crack through which the boundless shows. Once you feel this, the whole of life becomes porous with openings.",
        keyIdea: "Between any two states there is a seam; rest in the interval rather than the contents and the undivided ground appears.",
        misconception:
          "That the gap is a blank nothing to pass over. It is the undivided fullness that the contents on either side merely interrupt.",
        passageId: "vijnana_bhairava.yukti_034",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_017", "astavakra_gita.asg_11_7"],
        theme: "the-gap",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 34 — take refuge in the gap between any two cognitions or states. Help me inhabit the seam between thoughts and moods rather than their contents.",
        practice:
          "Watch the mind for a few minutes. Each time one thought ends and before the next begins, deliberately rest in the tiny gap. Then try it with moods: as one feeling releases, pause in the seam before the next arrives. Treat the interval as the destination.",
        journalPrompt:
          "When I rested in the seam between two thoughts, did it feel like absence — or like a fullness the thoughts had been hiding?",
        integration:
          "You can find and inhabit the interval between any two states as a structural doorway available all day long.",
      },
      {
        id: "vbt-threshold-sleep",
        title: "The Threshold Between Waking and Sleep",
        orientation:
          "Gate V · The Seam Between States. Of all the seams, one is especially wide and gentle each night: the doorway between waking and sleep.",
        teaching:
          "This dhāraṇā names a precise and accessible seam: when the external sensory field has dissolved but sleep has not yet come, that liminal state is the doorway. Each of us crosses this threshold twice daily, usually unconscious of it — the hypnagogic border where the senses have released the world but awareness has not yet gone dark. Held lightly, without grasping toward sleep or back toward waking, this margin reveals a consciousness that is awake yet objectless, the same Fourth (turīya) that underlies waking, dream, and deep sleep alike. The art is to stay just barely awake at the very lip of sleep — not to think about it, which pulls you back, nor to surrender, which pulls you under, but to float in the threshold itself. Mastered, this is one of the most natural samādhis available to a human being, offered freely every night.",
        keyIdea: "At the lip of sleep, the senses have released the world but awareness hasn't gone dark — float there and the wakeful Fourth shows.",
        misconception:
          "That this state is just drowsiness. Drowsiness is losing awareness; this is awareness remaining lucid while its objects fall away.",
        passageId: "vijnana_bhairava.yukti_047",
        supportingPassageIds: ["siva_sutra.ss_i_7", "mandukya_upanishad_and_gaudapada_karika.muk_015"],
        theme: "threshold",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 47 — the threshold between waking and sleep. Teach me to rest lucidly in the hypnagogic seam without falling asleep or snapping awake.",
        practice:
          "Tonight, as you fall asleep, set a gentle intention to notice the moment the senses release the room but you are still aware. Float in that margin without thinking or trying. If you slip under, no matter; the noticing itself is the practice.",
        journalPrompt:
          "At the very edge of sleep, when the world had let go but I had not yet, what quality of awareness was present?",
        integration:
          "You can recognize the waking–sleep threshold as a nightly doorway and rest in the lucid, objectless awareness it opens.",
      },
      {
        id: "vbt-everywhere",
        title: "Wherever the Mind Goes, Only Śiva",
        orientation:
          "Gate VI · Everywhere. The doorways now collapse into one realization: there was never anywhere that was not the gate.",
        teaching:
          "This dhāraṇā is the quiet thunderclap toward which all the others were leading: wherever the mind goes, externally or internally, it discovers nothing but the state of Śiva — and since that state is all-pervading, where could the mind possibly go to escape it? Every prior gate trained you to find the opening in a particular place: a breath, a sound, a sky, a delight, a seam. Now that training matures into the recognition that there is no non-sacred location, no thought or object outside of consciousness, nowhere the mind can travel that is not already the very thing it seeks. The search collapses not because you found the destination but because you realize you were never anywhere else. The 110 doorways were never 110 different rooms; they were 110 windows onto the one boundless space that was always, everywhere, the case.",
        keyIdea: "Since Śiva is all-pervading, wherever the mind goes it lands in Śiva — there is no location outside the gate.",
        misconception:
          "That awakening happens in a special place or state. The teaching is that no place is outside it; the search ends in omnipresence, not arrival.",
        passageId: "vijnana_bhairava.yukti_088",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001", "yoga_spandakarika.sp_30"],
        theme: "omnipresence",
        chatMode: "explain",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 88 — wherever the mind goes, it finds only Śiva. Help me understand how the many doorways collapse into the recognition that there is nowhere outside the gate.",
        practice:
          "For one hour, follow the mind wherever it wanders — to a worry, a plan, a sound, a craving — and at each landing place silently note: 'This too is Śiva; the mind has not left.' Watch the very habit of seeking-elsewhere lose its ground.",
        journalPrompt:
          "If there is genuinely nowhere my mind can go that is outside consciousness, what happens to my sense of seeking?",
        integration:
          "You can meet wherever the mind lands as already the open gate, ending the search for a special place or state.",
      },
      {
        id: "vbt-become-bhairava",
        title: "One Doorway, Fully Entered, Is Enough",
        orientation:
          "Gate VI · Everywhere. The seal of the whole text — and the most generous promise in it.",
        teaching:
          "Bhairava closes the teaching with a vow of stunning generosity: a practitioner who is fully connected (yukta) to even one of these methods becomes Bhairava himself. Not all 112 — one. The path was never a checklist to complete but a single key offered in a hundred shapes, so that whatever your temperament, at least one would fit your hand. Mastery here is not breadth but depth: one doorway entered all the way is the whole of liberation, because each door opens onto the identical boundless room. This reframes everything you have walked: you do not need to collect the dhāraṇās; you need to let one of them collect you. Choose the gate that quickened most — the breath, the gap, the sky, the delight — and live there until the one who passes through and the room beyond are recognized as one. That recognition is what it means to become Bhairava: not to reach a far state, but to stop being anyone other than the awareness that was always reading these words.",
        keyIdea: "You do not master 112 methods; you let one of them master you — for each door opens onto the identical boundless room.",
        misconception:
          "That you must practice all the doorways. One, fully entered, is the entire path; breadth is a beginning, depth is the door.",
        passageId: "vijnana_bhairava.yukti_112",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_020", "siva_sutra.ss_i_5"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Vijñāna Bhairava, dhāraṇā 112 — one who is connected to even one method becomes Bhairava. Help me choose the single doorway from this path that fits me, and commit to entering it fully.",
        practice:
          "Look back over the gates you have walked. Which one quickened something real — the breath, the Center, the edge of sound, the sky, delight, the gap, the threshold? Choose that one. For the coming week, practice only it, daily, until the practitioner and the openness it reveals feel like one thing.",
        journalPrompt:
          "Which single doorway is mine to live in — and what would it mean to enter it so fully that there is no longer anyone standing outside it?",
        integration:
          "You can commit to one chosen dhāraṇā and deepen it until practitioner and ground are recognized as one — the seal of the path.",
      },
    ],
  },
  {
    id: "the-one-and-the-many",
    title: "The One and the Many",
    level: "Advanced",
    focus: "Plotinus, Kashmir Śaivism, and the Tao on emanation, descent, and the return",
    outcome:
      "Trace a single arc across three traditions — how the One overflows into the many, how the soul forgets and descends, and how it turns and climbs home — until you can read your own life as that very movement.",
    description:
      "A comparative path through Plotinus' Enneads, the Pratyabhijñāhṛdayam, and the Tao Te Ching: one story of emanation and return, told in three voices.",
    arc:
      "Three traditions, separated by oceans and centuries, independently saw the same shape: a single boundless Source overflows into a multiplicity that forgets its origin, suffers the forgetting, and is at last drawn back — not to a different place, but to what it always was. Plotinus names the stages with surgical clarity (the One, Intellect, Soul, Nature) and describes the soul's descent and its ascent through Beauty. Kashmir Śaivism tells the same story as the free play of Consciousness contracting into a limited subject and then recognizing its own authorship. The Tao points wordlessly at the unnameable source from which the ten thousand things arise and to which they return. This path sets the three in conversation, gate by gate: first the Source beyond name and number, then the descent into multiplicity and forgetting, and finally the great return — Plotinus' 'never cease chiselling your statue,' the Śaiva recognition of the Perfect 'I,' the Tao's homecoming to the root. The aim is not comparative scholarship but recognition: that this emanation and return is the structure of your own existence, happening now.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "om-source-no-name",
        title: "The Source That Has No Name",
        orientation:
          "Gate I · The Source. Before there can be a story of descent and return, we must point at what everything comes from — and discover it cannot be named.",
        teaching:
          "The Tao Te Ching opens by undoing its own first word: the dao that can be walked is not the enduring dao; the name that can be named is not the enduring name. This is not coyness but precision. The Source of all things cannot itself be one of the things, cannot be captured by any name, because every name divides and the Source is prior to all division. Plotinus says the same of the One, and Śaivism of the sovereign Consciousness (citi) that is the ground of all appearance. To begin the path of emanation and return, you must first feel the vertigo of the truly first: that which has no name, no form, no inside or outside, and yet from which name, form, and world ceaselessly arise. Rest in the unnameable not as a concept but as the silence your every concept appears within.",
        keyIdea: "The Source of all things cannot be a thing or a name; it is the nameless ground from which all names arise.",
        misconception:
          "That the unnameable is a vague blank. It is the most concrete reality there is — too full and too prior to be caught in any name.",
        passageId: "tao_te_ching.ttc_md_001",
        supportingPassageIds: ["plotinus_enneads.enn_v_1_06", "pratyabhijnahrdayam.phr_001"],
        theme: "the-source",
        chatMode: "compare",
        chatPrompt:
          "Tao Te Ching ch.1 — 'the dao that can be named is not the enduring dao.' Compare this nameless Source with Plotinus' One and the Śaiva citi. Why must the first be beyond all naming?",
        practice:
          "Sit quietly and notice every name your mind reaches for — 'silence,' 'awareness,' 'God,' 'this.' Each time, gently set the name down and rest in what the name was pointing at, which has no name. A few minutes of laying down names.",
        journalPrompt:
          "What did I notice when I stopped trying to name the source of experience and simply rested as the unnameable openness it arises in?",
        integration:
          "You can recognize the unnameable Source as prior to every concept, and rest in it without grasping for a name.",
      },
      {
        id: "om-overflow",
        title: "The One Overflows",
        orientation:
          "Gate I · The Source. The Source is nameless — yet a universe pours from it. How does the perfect One give rise to the many without ceasing to be One?",
        teaching:
          "Plotinus gives the classic answer in a single luminous passage: 'The One is all things and no one of them.' Precisely because the Source lacks nothing, seeks nothing, and is not itself any being, it overflows — and from its exuberance the new arises. That first overflow turns back to gaze at its origin and, in gazing, becomes Intellect (Nous); Intellect in turn pours forth and becomes Soul; Soul, looking downward, generates Nature and the sensible world. Note the genius of the image: the One does not diminish by giving, as a spring is not emptied by the river. Each level is generated by contemplation of its prior and remains connected to it. Kashmir Śaivism tells it as Consciousness unfolding the universe on its own canvas by its own free will; the Tao, as the one giving birth to the two, the two to the three, the three to the ten thousand things. Creation is not a manufacture but an overflow of fullness.",
        keyIdea: "The One does not diminish by creating; it overflows from sheer fullness, and each level is born gazing back at its source.",
        misconception:
          "That creation depletes or divides the Source, or that it was a one-time event. The overflow is timeless, continuous, and costs the One nothing.",
        passageId: "plotinus_enneads.enn_v_1_06",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_002", "yoginihrdaya.yh_006"],
        theme: "emanation",
        chatMode: "explain",
        chatPrompt:
          "Plotinus Ennead V.1.6 — the Intellectual-Principle emanates from The One. Explain emanation as overflow rather than manufacture, and compare it with the Śaiva 'unfolding on her own canvas.'",
        practice:
          "Contemplate any abundant thing — sunlight, a spring, your own attention spilling onto whatever you regard. Feel how giving from fullness does not subtract. Then sense your awareness as such an overflow: pouring into perception without ever being emptied.",
        journalPrompt:
          "Where in my own experience do I give from fullness without being depleted — and what does that teach me about how the One creates?",
        integration:
          "You can understand the many as the timeless overflow of a One that loses nothing by giving rise to it.",
      },
      {
        id: "om-ten-thousand",
        title: "The Ten Thousand Things Arise — and Return",
        orientation:
          "Gate II · The Many. The overflow has reached the world of multiplicity. We pause to watch the many in their ceaseless arising and subsiding.",
        teaching:
          "The Tao Te Ching watches the result with serene eyes: 'The ten thousand things arise together; I watch them return.' From the nameless Source, fullness has poured all the way down into the teeming particularity of the world — leaves, creatures, thoughts, lives, each distinct, each in motion. Śaivism calls this the universe made multiple by the differentiation of reciprocally adapted objects and subjects; the Aṣṭāvakra Gītā sees it as waves rising on a single ocean. The crucial recognition at this gate is twofold: the many are real (the wave truly is a wave), and the many are not other than the One (the wave is only ever water). Multiplicity is not a fall from grace to be despised, nor an illusion to be dismissed — it is the One in the mode of the many, already on its way home, for everything that arises also returns. To rest here is to hold the ten thousand things without grasping and without contempt, watching them come and go as the breathing of the Source.",
        keyIdea: "The many are real yet never other than the One — the ten thousand things are the Source arising, already on their way back.",
        misconception:
          "That multiplicity is either a mistake to escape or a mere illusion. It is the One in the mode of the many — real, and never separate.",
        passageId: "tao_te_ching.ttc_md_003",
        supportingPassageIds: ["siva_sutra.ss_i_3", "astavakra_gita.asg_15_7"],
        theme: "multiplicity",
        chatMode: "compare",
        chatPrompt:
          "Tao Te Ching ch.16 — the ten thousand things arise and return. Compare this serene view of multiplicity with the Śaiva account of a differentiated universe and the ocean-and-waves image of the Aṣṭāvakra Gītā.",
        practice:
          "Sit somewhere with movement — a street, a garden, a busy mind. Watch things arise and pass: a sound, a person, a thought. With each, sense it as a wave on one ocean: distinct, yet only water. Neither grasp nor dismiss; just watch the arising and returning.",
        journalPrompt:
          "Can I hold the particular things of my life as both fully real and never separate from their Source? Where does that view ease my grasping?",
        integration:
          "You can meet multiplicity without contempt or grasping, seeing the many as the One arising and returning.",
      },
      {
        id: "om-forgetting",
        title: "How the Soul Forgot the Father",
        orientation:
          "Gate II · The Many. The descent has a shadow side. We name the wound at the heart of the human condition: forgetting.",
        teaching:
          "Plotinus asks the question that gives the whole drama its pathos: what could have brought the souls to forget the Father, the God from whom they came, and to ignore at once themselves and their Source? His answer is precise: the source of the trouble is self-will — the soul's pleasure in its own separate motion, its descent into the sphere of process, its desire to belong to itself. Drifting further and further, it loses even the memory of its origin, like a child carried far from home who forgets the face of its father and, in time, its own name. This is the exact teaching of the Pratyabhijñāhṛdayam: to be a bound, transmigrating soul is to be bewildered by one's own powers, having forgotten one's authorship of the whole play. The bondage is not that the One abandoned us; it is that we, intoxicated by our own freedom to seem separate, forgot. And what was forgotten can be remembered. The wound names the cure.",
        keyIdea: "Bondage is not exile imposed from outside but a self-forgetting — the soul, drunk on separate selfhood, mislaid the memory of its Source.",
        misconception:
          "That separation from the divine is a punishment or a metaphysical fact. It is a forgetting — and what was forgotten can be recognized again.",
        passageId: "plotinus_enneads.enn_v_1_01",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_012", "astavakra_gita.asg_1_8"],
        theme: "forgetting",
        chatMode: "explain",
        chatPrompt:
          "Plotinus Ennead V.1.1 — the souls forgot the Father through self-will. Explain forgetting as the root of bondage, and compare it with the Śaiva teaching that the bound soul is bewildered by its own forgotten powers.",
        practice:
          "Recall a time you felt utterly separate, small, or exiled. Instead of fixing the feeling, ask: 'What have I forgotten about what I am?' Don't answer with a thought; let the question loosen the grip of the forgetting, even slightly.",
        journalPrompt:
          "In what specific ways do I live as though I had forgotten my Source — and what changes when I name that as forgetting rather than fact?",
        integration:
          "You can recognize your sense of separation as a self-forgetting rather than a fixed condition, opening the door to remembrance.",
      },
      {
        id: "om-contracted-aperture",
        title: "You Are the Same One at a Contracted Aperture",
        orientation:
          "Gate II · The Many. Before the turn homeward, the decisive recognition: the limited self is not a different being from the One but the One narrowed.",
        teaching:
          "The Pratyabhijñāhṛdayam states it with breathtaking economy: the individual experient, in whom Consciousness has contracted, still contains the universe in a contracted form. You are not a separate spark cut off from the fire; you are the whole fire, drawn down to the size of a single flame — the same Consciousness, undiminished in nature, narrowed only in aperture. Plotinus' confession in the Enneads carries the lived texture of this: 'Many times it has happened — lifted out of the body into myself, beholding a marvellous beauty, acquiring identity with the divine... yet there comes the moment of descent.' The descent into the body is not a change of substance but a contraction of scope; the divine identity is never lost, only momentarily un-lived. This is the hinge of the entire path. If the limited self were truly other than the One, no return would be possible. Because it is the One contracted, the return is not a journey to a far country but the simple widening of an aperture that was never anything but the One's own.",
        keyIdea: "The limited self is not separate from the One but the One at a contracted aperture — so the return is a widening, not a journey.",
        misconception:
          "That the small self must be destroyed to reach the One. It need not be destroyed but widened — it was always the One, narrowed.",
        passageId: "pratyabhijnahrdayam.phr_004",
        supportingPassageIds: ["plotinus_enneads.enn_i_6_08", "tao_te_ching.ttc_md_002"],
        theme: "contraction",
        chatMode: "explain",
        chatPrompt:
          "Pratyabhijñāhṛdayam 4 — the individual is Consciousness contracted, still containing the universe. Explain the limited self as the One at a narrowed aperture, and connect it to Plotinus' 'lifted out of the body into myself.'",
        practice:
          "Sense your awareness right now as a small, bounded pool. Then gently ask whether its nature — pure knowing — is any different from a vast awareness. Same water, smaller vessel. Let the felt boundary soften without trying to force it open.",
        journalPrompt:
          "If my limited self is the One at a contracted aperture, what in me is the contraction — and what is the unchanged nature underneath it?",
        integration:
          "You can hold the limited self as the One narrowed rather than the One denied, which makes the return thinkable as a widening.",
      },
      {
        id: "om-the-turn",
        title: "The Turn: Recognition Reverses the Current",
        orientation:
          "Gate III · The Return. The descent reaches its floor and the movement reverses — not by adding anything, but by a single act of recognition.",
        teaching:
          "The Pratyabhijñāhṛdayam marks the exact moment the whole current turns: when there is complete recognition (pratyabhijñā) of one's own authorship, the very mind that had wandered outward becomes the inward-turned vehicle of liberation. This is the structural counterpart to the outward emanation — the same energy, now flowing home. Plotinus describes the identical reversal as the soul turning from its admiration of external things back upon itself and its Source. Nothing new is acquired in the turn; what changes is direction. The faculties that produced bondage by facing outward produce freedom by facing in. This is why recognition, not effort, is the operative word: you do not manufacture your divinity, you recognize the One you have been all along, the way a person mistaken about their own identity suddenly remembers their name. The descent was forgetting in motion; the return is remembering in motion. And the instrument of both is the same consciousness, simply re-aimed.",
        keyIdea: "The return adds nothing; it reverses direction — the same mind that wandered out, recognizing its authorship, becomes the vehicle home.",
        misconception:
          "That the return requires acquiring a new power or state. It requires only recognition — the same faculties, re-aimed from outward to inward.",
        passageId: "pratyabhijnahrdayam.phr_013",
        supportingPassageIds: ["plotinus_enneads.enn_i_6_09", "yoga_spandakarika.sp_08"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Pratyabhijñāhṛdayam 13 — recognition of one's authorship turns the mind into the vehicle of liberation. Help me feel the return as a reversal of direction rather than an acquisition.",
        practice:
          "Notice attention flowing outward toward objects, plans, worries. Gently reverse it: let attention turn back to rest in the awareness that is doing the attending. Don't seek anything there; just let the current run home. Repeat whenever you catch the outward pull.",
        journalPrompt:
          "When I turned attention back toward the awareness behind it, what did I notice about whether anything needed to be added — or only redirected?",
        integration:
          "You can perform the turn at will — reversing attention from objects back to its source — and recognize the return as redirection, not acquisition.",
      },
      {
        id: "om-become-sunlike",
        title: "Never Cease Chiselling Your Statue",
        orientation:
          "Gate III · The Return. The current flows home; now Plotinus gives the most beautiful instruction in all of late antiquity for the ascent itself.",
        teaching:
          "How does the homeward soul actually rise? Plotinus answers with the image of the sculptor: 'Act as does the creator of a statue that is to be made beautiful — cut away all that is excessive, straighten all that is crooked, bring light to all that is overcast, and never cease chiselling your statue until there shall shine out the godlike splendour of virtue.' The ascent is not addition but subtraction — the removal of everything that is not the radiant form already latent within. And then the decisive principle: 'Never did the eye see the sun unless it had first become sunlike; and never can the soul have vision of the First Beauty unless itself be beautiful.' You cannot see the One as an object; you can only become like it and thereby see by being. This is the precise meeting point with the Śaiva ascent through the subtle centers to the partless summit, and with the Tao's polishing of the mirror. The return culminates not in reaching a far light but in becoming light — 'strike forward yet a step; you need a guide no longer; strain, and see.'",
        keyIdea: "You cannot see the One as an object; you become like it and see by being — the ascent is subtraction until you yourself are light.",
        misconception:
          "That you reach the Source by acquiring or grasping more. You reach it by becoming sunlike — chiselling away all that is not already the radiant form.",
        passageId: "plotinus_enneads.enn_i_6_09",
        supportingPassageIds: ["yoginihrdaya.yh_011", "siva_sutra.ss_i_5"],
        theme: "ascent",
        chatMode: "practice",
        chatPrompt:
          "Plotinus Ennead I.6.9 — 'never cease chiselling your statue' and 'never did eye see the sun unless it had become sunlike.' Teach me the ascent as subtraction and as becoming-like rather than grasping.",
        practice:
          "Choose one thing that is 'excessive' or 'crooked' in you — a habit of grasping, a hardness, a haze of distraction. For a few minutes, simply let it be chiselled away in attention, without adding anything. Sense what radiance is uncovered when something false is set down.",
        journalPrompt:
          "What in me is 'excessive' or 'overcast' that, if chiselled away, would let me become more sunlike — able to see by resemblance rather than by grasping?",
        integration:
          "You can practice the ascent as subtraction and resemblance — removing what is false until you see the Source by being like it.",
      },
      {
        id: "om-alone-to-alone",
        title: "The Alone to the Alone",
        orientation:
          "Gate III · The Return. The arc closes where it began — but now the One is recognized not as a far source but as your own inmost identity, lived.",
        teaching:
          "The Pratyabhijñāhṛdayam seals the return with its final movement: by entering the Perfect 'I'-consciousness — the unconditioned, full I-ness that is Śiva's own — one attains lordship over the play of emanation and reabsorption even while living and embodied. This is the homecoming the whole path described: not the soul reaching a distant One, but the soul recognizing that its truest 'I' and the One were never two. Plotinus' tradition called the final union 'the flight of the alone to the Alone' — and the deepest reading is not that a lonely soul flies to a lonely God, but that the Alone (your innermost, undivided self) is united with the Alone (the One), with nothing in between, because there was only ever the One. The Tao says it as the return to the root, which is stillness, which is called returning to one's destiny. The emanation that poured out through every gate of this path is now seen, from the summit, as a single circular movement: the One going forth as the many and coming home as you — and that homecoming, lived in an ordinary embodied life, is liberation itself.",
        keyIdea: "The return ends not in reaching a far One but in recognizing your inmost 'I' as the One — the alone united with the Alone, lived while embodied.",
        misconception:
          "That union is a distant soul merging with a distant God. There were never two: the inmost self and the One are one, recognized here and now.",
        passageId: "pratyabhijnahrdayam.phr_020",
        supportingPassageIds: ["plotinus_enneads.enn_vi_9_11", "tao_te_ching.ttc_md_003"],
        theme: "union",
        chatMode: "practice",
        chatPrompt:
          "Pratyabhijñāhṛdayam 20 — entering the Perfect 'I'-consciousness, liberation while embodied. Connect it to Plotinus Ennead VI.9 on union with the One and the Tao's return to the root, as the close of the emanation-and-return arc.",
        practice:
          "Rest as the bare sense 'I am' — not 'I am this or that,' just the unconditioned I-ness. Let it be felt as identical with the boundless Source, with nothing standing between. Stay a few minutes in the recognition: the One went forth as the many and has come home as this very awareness.",
        journalPrompt:
          "If my inmost 'I' and the One were never two, how does the whole arc — overflow, forgetting, descent, return — read as the single movement of my own life?",
        integration:
          "You can rest in the Perfect 'I' as identical with the Source, recognizing emanation and return as one circular movement lived in your own embodied life.",
      },
    ],
  },
  {
    id: "action-without-contraction",
    title: "Action Without Contraction",
    level: "Beginner",
    focus: "Duty, control, and non-possessive action",
    outcome:
      "Learn to act clearly and wholeheartedly when life is uncertain, morally complex, or emotionally charged — without seizing up around the outcome.",
    description:
      "Move from moral overwhelm into clear action, non-possessiveness, and grounded responsibility.",
    arc:
      "We begin where you actually are: stuck, conflicted, unsure how to act. Rather than rushing to relieve that discomfort, we treat it as the doorway. Step by step we separate what is yours to govern from what is not, learn to act fully while releasing the result, distinguish real renunciation from avoidance, steady the mind that keeps grasping, and finally arrive at surrender — not as collapse, but as the most lucid form of action there is.",
    estimatedSessions: "6 sessions · ~20 min each",
    steps: [
      {
        id: "meet-the-crisis",
        title: "Let the crisis become honest",
        orientation:
          "Every real path begins in a moment of being stuck. We start here on purpose.",
        teaching:
          "Arjuna collapses on the battlefield between two armies, unable to act. The Gita does not treat this paralysis as weakness to be overcome quickly; it treats it as the precise condition in which genuine teaching can finally land. Notice the move: the crisis is not the obstacle to the spiritual life, it is its beginning. When you face two real goods that cannot both be preserved, the confusion you feel is not failure — it is the honest registering of a world more complex than your previous certainties allowed. The work is not to make the discomfort disappear but to stay in it long enough to be taught.",
        keyIdea: "Confusion faced honestly is sacred data, not a verdict on your worth.",
        misconception:
          "That a 'spiritual' response would have meant feeling calm and certain. The Gita's hero begins by breaking down.",
        passageId: "bhagavad_gita.bg_01_47",
        supportingPassageIds: ["epictetus_works.epi_enc_001"],
        theme: "action",
        chatMode: "explain",
        chatPrompt:
          "Help me understand this crisis as the beginning of spiritual clarity, not as weakness. What is the difference between honest paralysis and avoidance?",
        practice:
          "Sit for three minutes with one situation where you feel stuck. Do not try to solve it. Simply name, silently, 'This is where I am being asked to look.' Let the discomfort be information.",
        journalPrompt:
          "Where am I facing two real goods that cannot both be preserved perfectly? What am I afraid the confusion says about me?",
        integration:
          "You can sit with a genuine dilemma without immediately collapsing it into a false certainty or fleeing it.",
      },
      {
        id: "separate-governance",
        title: "Separate what is yours to govern",
        orientation:
          "Before you can act well, you must see clearly what is actually in your power.",
        teaching:
          "Epictetus opens the Enchiridion with a single division that he claims is the hinge of all freedom: some things are up to us (our judgments, intentions, responses) and some are not (our body, reputation, circumstances, other people, outcomes). Suffering, he argues, comes almost entirely from treating the second category as if it were the first — from staking our peace on what we cannot command. This is not resignation. It is the opposite: by withdrawing your demand from what is not yours, you concentrate your whole force on the one place where you are genuinely sovereign — the quality of your response. Freedom is trained here, before reaction begins.",
        keyIdea:
          "Locate your effort only where your power actually reaches: your own judgment and intention.",
        misconception:
          "That this means becoming cold or passive. It means becoming precise about where to invest your care.",
        passageId: "epictetus_works.epi_enc_001",
        supportingPassageIds: ["epictetus_works.epi_enc_002"],
        theme: "freedom",
        chatMode: "explain",
        chatPrompt:
          "Show me how this passage trains freedom before reaction begins. Where do people misapply the division between what is and isn't up to them?",
        practice:
          "The next time an appearance pulls — news that disturbs, a message that provokes, a plan threatening to collapse — stop before you move toward it. Feel the grip as if the thing were reaching across a boundary. Ask only this: is this mine to govern, or not? If it is not, say it in the body: this is not mine. Freedom is not a later feeling. It is this withdrawal of demand from what was never yours. Then, and only then, decide what, if anything, you will actually do.",
        journalPrompt:
          "List one situation today as two columns: what is mine to govern, and what is not. Where had I confused the two?",
        integration:
          "Given any upset, you can quickly find the boundary between what you control and what you don't — and feel the relief of releasing the rest.",
      },
      {
        id: "release-ownership",
        title: "Act without possessiveness",
        orientation:
          "Now we turn the inner freedom of Step 2 into a way of acting in the world.",
        teaching:
          "The Gita's most famous teaching is easy to quote and hard to live: you have a right to your action, never to its fruits. The radical part is that this is not a counsel to care less — it is a counsel to act more fully. When you are gripping the outcome, part of your attention is always elsewhere, hedging, performing, anxious. Release the grip on the result and your whole capacity returns to the action itself, which can now be done cleanly, for its own rightness. Non-possessive action is not detachment from the work; it is total presence to the work, minus the contraction around what it will get you.",
        keyIdea:
          "Pour yourself fully into the action; let go of ownership of its result.",
        misconception:
          "That releasing the outcome means not caring or not trying. It means caring about the act itself rather than its payoff.",
        passageId: "bhagavad_gita.bg_02_47",
        supportingPassageIds: ["isavasya_upanishad.isa_002"],
        theme: "action",
        chatMode: "practice",
        chatPrompt:
          "Give me a concrete practice for acting fully without contracting around the outcome, using this passage. What does it feel like when I'm gripping vs. releasing?",
        practice:
          "Take one task that has you white-knuckling the outcome — the class, the message, the conversation that might go badly. Before you begin, offer the action and set the fruit down the way you would set a cup on a table you do not own. Work with your whole body in the doing. If the old grip returns, do not fight it. Feel it, and put the cup down again. Completion is the integrity of the act, not the harvest.",
        journalPrompt:
          "What action today can I perform carefully while releasing ownership of its result? What did the gripping feel like in my body?",
        integration:
          "You can throw yourself fully into a task while noticing — and loosening — the anxious grip on how it turns out.",
      },
      {
        id: "renounce-within-action",
        title: "Renounce inwardly, not avoidantly",
        orientation:
          "A crucial fork: real spiritual maturity is often confused with withdrawal. We separate them here.",
        teaching:
          "There is a counterfeit of renunciation that looks wise but is actually avoidance — leaving the marriage, quitting the job, going silent, all to escape difficulty rather than to meet it more freely. The Gita (and the Īśā Upaniṣad alongside it) insists that true renunciation is inward: you renounce the compulsive ownership and the craving, not the action and the world. You can be fully engaged in life and inwardly free at the same time; indeed that is the harder and higher path. The test is simple and uncomfortable: am I letting go to be free, or to be comfortable? Withdrawal motivated by fear only relocates the knot.",
        keyIdea:
          "Renounce the grasping, not the engagement. Inner freedom, not outer escape.",
        misconception:
          "That the spiritual move is always to step back or step away. Often it is to stay, but differently.",
        passageId: "bhagavad_gita.bg_05_10",
        supportingPassageIds: ["isavasya_upanishad.isa_002"],
        theme: "renunciation",
        chatMode: "compare",
        chatPrompt:
          "Compare inner renunciation with avoidant withdrawal using this passage. How can I tell, honestly, which one I'm doing?",
        practice:
          "Identify one thing you've been calling 'letting go of.' Ask honestly: am I releasing the craving, or fleeing the difficulty? If it's flight, imagine staying — but without the grasping.",
        journalPrompt:
          "Where am I mistaking avoidance for renunciation? What would it look like to stay, but inwardly free?",
        integration:
          "You can distinguish, in your own life, the renunciation that frees you from the withdrawal that merely protects you.",
      },
      {
        id: "steady-the-mind",
        title: "Return attention to steadiness",
        orientation:
          "Non-possessive action is impossible without a trained relationship to your own mind.",
        teaching:
          "Arjuna objects that the mind is restless, turbulent, hard to hold — 'as hard to master as the wind.' Krishna does not deny it; he answers with abhyāsa (steady practice) and vairāgya (non-attachment). The key insight for daily life is that mastery is not a single act of seizing the mind still — it is the repeated, patient return of attention each time it wanders. The skill is not in never drifting; it is in the gentleness and frequency of the return. Each return is one repetition of freedom. Over time the mind that could not secure its outcomes learns to rest in something steadier than outcomes.",
        keyIdea:
          "Mastery of mind is the patient, repeated return of attention — not a one-time conquest.",
        misconception:
          "That a steady mind means a mind that never wanders. It means a mind that returns, willingly and often.",
        passageId: "bhagavad_gita.bg_06_35",
        supportingPassageIds: ["vijnana_bhairava.yukti_002"],
        theme: "meditation",
        chatMode: "practice",
        chatPrompt:
          "Turn this passage into a short daily attention practice I can do before acting. How should I relate to the mind's wandering?",
        practice:
          "Sit with the breath. Krishna does not deny the wind. Each time attention flies, count the return as the practice, not the failure. After ten honest returns, loosen one craving-color that was riding the sitting — the wish to be calm, impressive, finished. Practice without that extra heat; release without going limp. The mind is graspable only where both hands are working.",
        journalPrompt:
          "What did my mind do today when it could not secure the outcome it wanted? How quickly could I return it to the present?",
        integration:
          "You treat each wandering of attention as an opportunity to practice the return, rather than as evidence of failure.",
      },
      {
        id: "surrender-with-clarity",
        title: "Surrender without collapsing",
        orientation:
          "The path culminates not in control but in a surrender that is more lucid than any control.",
        teaching:
          "The Gita ends not with a technique but with trust: act according to your clearest understanding of what is right, then release the rest into something larger than your management. This is the most misunderstood word in the spiritual vocabulary. Surrender is not giving up, going limp, or abandoning discernment. It is what becomes possible precisely after you have done the work of clarity — you have sorted what is yours, acted without grasping, steadied the mind — and now you let go of the exhausting fantasy that the outcome depends on your anxiety. Surrender is lucid action that has stopped white-knuckling the universe. It is the lightest and most awake thing a person can do.",
        keyIdea:
          "Surrender is the lucid release that follows clarity — not the collapse that precedes it.",
        misconception:
          "That surrender means passivity or fatalism. It is the freest form of engaged, clear-eyed action.",
        passageId: "bhagavad_gita.bg_18_66",
        supportingPassageIds: ["epictetus_works.epi_enc_003"],
        theme: "freedom",
        chatMode: "practice",
        chatPrompt:
          "Help me practice surrender as lucid action, not passivity. How is this different from giving up?",
        practice:
          "Bring to mind one situation you've been trying to control through worry. Do the one clear, right action available to you. Then, on an out-breath, deliberately set down the rest: 'I have done what is mine. The rest I release.'",
        journalPrompt:
          "What would I do next if I trusted clarity more than control? Where am I confusing worry with responsibility?",
        integration:
          "You can act decisively on what is clear and then genuinely set down the outcome, without that feeling like defeat.",
      },
    ],
  },
  {
    id: "recognizing-awareness",
    title: "Recognizing Awareness",
    level: "Intermediate",
    focus: "Witnessing, contraction, and recognition",
    outcome:
      "Learn to notice awareness itself, see how it contracts into a limited identity, and return — repeatedly — to recognition in the middle of ordinary life.",
    description:
      "Learn the contemplative movement from identification with experience to recognition of awareness itself.",
    arc:
      "This path trains a single capacity from many angles: the recognition of awareness as the ground rather than as one more object inside experience. We name the ground, see how knowledge itself can bind us to a fixed identity, locate the witness directly, map how boundless awareness contracts into a small self, feel the living surge that breaks through that contraction, and finally learn to stabilize recognition not in retreat but in speech, perception, and action.",
    estimatedSessions: "6 sessions · ~25 min each",
    steps: [
      {
        id: "name-the-ground",
        title: "Name the ground",
        orientation:
          "We begin by reversing the usual assumption about what is fundamental.",
        teaching:
          "The Śiva Sūtra opens with three words — caitanyam ātmā, 'consciousness is the Self' — and the entire non-dual path follows from taking them seriously. Ordinarily we treat consciousness as something we have: a function of the brain, a beam we point at objects, one item in our inventory. This sūtra reverses the priority. Consciousness is not a possession of the self; it is the Self — the very ground in which every experience, including the sense of being a separate person, appears. The instruction hidden in the statement is experiential: stop looking at the contents of awareness for a moment and notice the awareness in which they arise. That noticing is the whole journey in seed form.",
        keyIdea:
          "Awareness is not a thing you have; it is the ground in which everything, including 'you,' appears.",
        misconception:
          "That consciousness is a product or function inside you. Here it is the basis, not the byproduct.",
        passageId: "siva_sutra.ss_i_1",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001"],
        theme: "awareness",
        chatMode: "explain",
        chatPrompt:
          "Explain 'consciousness is the Self' in a way I can test in immediate experience right now, not just understand intellectually.",
        practice:
          "Look at whatever is nearest — the yellow of a leaf, the glow of the screen, a chair scraping. Do not hunt for a special state. Notice that all of it is already lit. Now stop following the objects and rest as the lighting itself. The sūtra is not asking you to become conscious. It is asking you to drop the fiction that there is a you over here and awareness over there. Stay until \"I am looking\" softens into looking looking.",
        journalPrompt:
          "What is present before I add a story about who I am? Can I find the awareness that is reading these words?",
        integration:
          "You can deliberately shift attention from the objects of experience to the awareness in which they appear.",
      },
      {
        id: "see-knowledge-bind",
        title: "Notice how knowledge binds",
        orientation:
          "A surprising turn: the very thing that seems to free us can trap us.",
        teaching:
          "The second Śiva Sūtra is jolting: jñānam bandhaḥ, 'knowledge is bondage.' How can knowledge bind? The point is precise. Limited, dualistic knowledge — the constant stream of definitions by which 'I am this, not that' — is exactly what fences boundless awareness into a small, defended identity. Every fixed self-concept ('I am someone who...') is a piece of knowledge that contracts. Even spiritual knowledge becomes a cage when it hardens into another identity to protect. This step asks you to watch the subtle moment where a useful thought becomes a wall — where knowing about yourself substitutes for being the openness you are.",
        keyIdea:
          "Fixed self-knowledge is the mechanism by which open awareness contracts into a defended identity.",
        misconception:
          "That more spiritual knowledge is always liberating. Held wrongly, it becomes one more thing to defend.",
        passageId: "siva_sutra.ss_i_2",
        supportingPassageIds: ["astavakra_gita.asg_1_7"],
        theme: "knowledge",
        chatMode: "question",
        chatPrompt:
          "Help me see when spiritual knowledge becomes another form of bondage. How do I hold understanding without it hardening into identity?",
        practice:
          "Catch the next naming: tree, morning, me. Feel how the word files the living thing into a known slot. For three breaths let the name stay, but refuse to let it finish the seeing. Watch rain, sun, and soil still moving in what you just called a tree. The bondage is not the word. It is the moment the word pretends to be the last word.",
        journalPrompt:
          "Which idea about myself did I defend today as if it were the Self? What would loosen if I held it as a passing thought?",
        integration:
          "You can catch the moment a self-concept hardens into something you defend, and loosen your grip on it.",
      },
      {
        id: "recognize-the-witness",
        title: "Recognize the witness",
        orientation:
          "Now a direct shift: from being lost in content to standing as the one who sees it.",
        teaching:
          "Aṣṭāvakra gives the seeker the most direct instruction in the non-dual canon: you are not the body, the senses, or the mind — you are the witness of all of them, the awareness that knows them and is not touched by them. The image of two birds on one tree (from the Upaniṣads) captures it: one bird eats the fruit, absorbed and agitated; the other simply watches, serene. Both are 'you,' but you have been identifying with the eater. The witness is not a new state to achieve; it is what is already effortlessly aware of every state. The practice is to keep gently relocating from the content to the one noticing the content.",
        keyIdea:
          "You are the witnessing awareness, not the changing experience it observes.",
        misconception:
          "That the witness is a special elevated state to attain. It is the ordinary awareness already present, simply recognized.",
        passageId: "astavakra_gita.asg_1_7",
        supportingPassageIds: ["svetasvatara_upanishad.svu_011"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Give me a direct witnessing practice from this verse, with no abstraction. How do I shift from the experience to the one experiencing?",
        practice:
          "Whatever you are feeling right now, silently ask: 'Who is aware of this feeling?' Do not answer in words — just notice the awareness that was already here. Rest as that, letting the feeling continue at the edge.",
        journalPrompt:
          "What did I notice today as an object — a sensation, an emotion, a thought — that I usually call 'me'?",
        integration:
          "You can, at will, recognize yourself as the one aware of an experience rather than as the experience itself.",
      },
      {
        id: "learn-contraction",
        title: "Map contraction",
        orientation:
          "To return to openness, you must understand exactly how it narrows.",
        teaching:
          "The Pratyabhijñāhṛdayam ('The Heart of Recognition') makes the whole path practical by describing its mechanism: the one universal Consciousness freely contracts itself into the limited experience of a separate subject. This is the key word — saṅkoca, contraction. Your ordinary sense of being a small self bounded by a body and a biography is not a mistake imposed from outside; it is awareness itself, voluntarily narrowing. Why does this matter? Because if contraction is something awareness does, it is something that can be recognized and, in any moment, relaxed. You learn to feel the very act of narrowing — into a role, a fear, a craving — and to recognize the spaciousness it contracted from.",
        keyIdea:
          "The limited self is not an error but a contraction of awareness — and what contracts can expand.",
        misconception:
          "That the separate self is a fixed fact to be destroyed. It is a movement to be recognized and loosened.",
        passageId: "pratyabhijnahrdayam.phr_004",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_005"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Explain saṅkoca (contraction) as an experiential pattern I can recognize in daily life. How does awareness narrow into a small self?",
        practice:
          "Next time you feel defensive or small, pause and feel the contraction physically — the tightening into a role or fear. Then ask: 'What was here before this narrowed?' Sense the space it contracted from.",
        journalPrompt:
          "Name one moment today where awareness narrowed into a role, fear, or preference. Could I feel the act of narrowing?",
        integration:
          "You can feel contraction happening in real time and recognize the openness from which it narrows.",
      },
      {
        id: "taste-the-surge",
        title: "Feel the surge of awareness",
        orientation:
          "Recognition needs a felt, energetic doorway — not only metaphysical understanding.",
        teaching:
          "The Śiva Sūtra names a living power: udyamo bhairavaḥ — 'the upsurge is Bhairava.' Udyama is the spontaneous welling-up of awareness, the sudden vividness that breaks through habit — in a moment of beauty, shock, wonder, or the catch of breath before speech. The Spanda tradition calls this the subtle tremor (spanda) at the root of all experience. The teaching is that this surge is not a feeling you produce; it is awareness itself becoming briefly self-aware, and it is always available at the seams of experience. Rather than only thinking about awareness, you learn to catch its felt pulse — the aliveness that is recognition in its energetic form.",
        keyIdea:
          "Recognition has a felt, energetic form: the spontaneous surge of aliveness at the seams of experience.",
        misconception:
          "That recognition is purely a calm, conceptual insight. It also arrives as a vivid, embodied surge.",
        passageId: "siva_sutra.ss_i_5",
        supportingPassageIds: ["yoga_spandakarika.sp_02"],
        theme: "awareness",
        chatMode: "practice",
        chatPrompt:
          "Turn udyama — the surge of awareness — into a brief embodied practice. Where in ordinary experience can I catch this pulse?",
        practice:
          "Recall a moment today when something made you suddenly more awake — a sound, a beauty, a start. Re-enter it in memory and feel the surge of vividness. That aliveness is awareness recognizing itself. Rest in it.",
        journalPrompt:
          "When did aliveness break through habit today? What did the surge feel like before I named it?",
        integration:
          "You can locate the felt surge of awareness in ordinary moments, not only conceptual insight.",
      },
      {
        id: "stabilize-recognition",
        title: "Stabilize recognition in ordinary life",
        orientation:
          "The goal is not a peak state but recognition that survives contact with daily life.",
        teaching:
          "The Pratyabhijñā path closes not in withdrawal but in integration: the recognized awareness is to be stabilized in the midst of perception, speech, and action — even in pleasure and difficulty. The Śiva Sūtra had already promised that 'the bliss of the world is the joy of samādhi,' meaning the ordinary world, rightly seen, is not an obstacle to recognition but its very field. Maturity here is measured by repetition, not intensity: not how deep a meditation you can reach in retreat, but how often you can recognize awareness while answering an email, washing a dish, or being interrupted. You build an ordinary trigger into a reminder, and recognition becomes a way of living rather than an event.",
        keyIdea:
          "Stable recognition is frequent, ordinary return — not a rare, dramatic peak.",
        misconception:
          "That the aim is to sustain a special state. The aim is to recognize awareness again and again amid normal activity.",
        passageId: "pratyabhijnahrdayam.phr_020",
        supportingPassageIds: ["siva_sutra.ss_i_18"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Help me stabilize recognition through ordinary perception, speech, and action. How do I build it into daily life rather than retreat?",
        practice:
          "Stand in an ordinary doorway. Feel the body pass through. Before the next room claims you, let \"I am\" sound — not the résumé, not the myth of me, but the simple light that is reading, walking, arriving. This knowing is not owned by the person in the doorway. It is the same light in every being, at every scale. Say it once, quietly: iti śivam. Then go through.",
        journalPrompt:
          "What ordinary trigger can become a reminder to recognize awareness? How did recognition hold up under interruption today?",
        integration:
          "You have a concrete daily cue that returns you to recognition in the middle of ordinary activity.",
      },
    ],
  },
  {
    id: "letting-go-death-emptiness",
    title: "Letting Go, Death, and Emptiness",
    level: "Advanced",
    focus: "Impermanence, emptiness, and fearless release",
    outcome:
      "Learn to practice with death, silence, absence, and breath so that letting go becomes fearless and tender rather than grim or avoidant.",
    description:
      "Train with impermanence, emptiness, and non-grasping so practice becomes fearless and tender.",
    arc:
      "This path turns letting go from a grim duty into a spacious art. We start with philosophy as the practice of dying, learn to trust what is not immediately visible, empty ourselves enough to truly receive, discover that absence is functional rather than deficient, enter the gap in the breath as a direct threshold practice, and close by asking how a life rehearsed in release leaves its trace in others.",
    estimatedSessions: "6 sessions · ~25 min each",
    steps: [
      {
        id: "train-for-death",
        title: "Practice before death arrives",
        orientation:
          "We open with the boldest reframing: that philosophy itself is rehearsal for dying.",
        teaching:
          "Socrates, calm on the day of his execution, defines philosophy as 'the practice of death' — and means something precise and usable, not morbid. To practice dying is to repeatedly loosen your identification with what is perishing: possessions, status, the body's sensations, the self-image you defend. Each time you release a false center of gravity before mortality forces the issue, thought stands in clearer relation to what is true. Death, in this frame, is not only an event at the end of life; it is an operation available now — the disciplined separation of awareness from compulsive identification. The fruit is not gloom but composure: you have already practiced losing what you will lose.",
        keyIdea:
          "To 'practice dying' is to release false identifications now, so you meet loss with composure rather than panic.",
        misconception:
          "That this is morbid or life-denying. It is a training in clarity and freedom that makes life more vivid, not less.",
        passageId: "phaedo_plato.phaedo_md_001",
        supportingPassageIds: ["svetasvatara_upanishad.svu_007"],
        theme: "death",
        chatMode: "explain",
        chatPrompt:
          "Explain philosophy as training for death in a way that supports practice rather than morbidity. What exactly am I practicing releasing?",
        practice:
          "Name three things you currently fear losing. After each, ask: 'If this changes, what in me is still aware of the change?' Rest in that witnessing position without forcing an answer.",
        journalPrompt:
          "What am I clinging to as if it could make me permanent? What would loosen if I practiced releasing it now?",
        integration:
          "You can name what you cling to for permanence and locate the awareness that would remain if it were lost.",
      },
      {
        id: "see-the-unseen",
        title: "Trust what is not immediately visible",
        orientation:
          "Letting go of the visible requires learning to weigh the unseen.",
        teaching:
          "Plato argues that the soul has an affinity with what is invisible, unchanging, and intelligible — and that wisdom is partly the discipline of not letting the loud evidence of the senses dictate what is real. This matters far beyond metaphysics. Most of what actually governs a good life is unseen: values, intentions, the quiet orientation of attention. To trust the unseen is to learn to act from what is real but not obvious, rather than being ruled by whatever is most immediately vivid. It is a discipline of attention: weighting the invisible appropriately when the visible shouts.",
        keyIdea:
          "Maturity is learning to weigh the unseen — values, intention, the real — against the loud evidence of the senses.",
        misconception:
          "That 'the unseen' is vague mysticism. Here it names the invisible orientations that actually steer a life.",
        passageId: "phaedo_plato.phaedo_md_003",
        supportingPassageIds: ["phaedo_plato.phaedo_md_005"],
        theme: "knowledge",
        chatMode: "question",
        chatPrompt:
          "Help me understand the soul's affinity with the unseen as a discipline of attention. How do I weigh the invisible against the obvious?",
        practice:
          "Recall one choice you made today. Ask: what invisible value or intention actually guided it? Notice how the unseen quietly steered the visible action.",
        journalPrompt:
          "What invisible value quietly governed one choice I made today? Where do I let the loudest visible thing override the truest unseen one?",
        integration:
          "You can identify the unseen intentions steering your actions and give them appropriate weight.",
      },
      {
        id: "empty-to-receive",
        title: "Become empty enough to receive",
        orientation:
          "Letting go shifts now from grim renunciation to spacious receptivity.",
        teaching:
          "Zhuangzi offers the 'fasting of the heart-mind' (xīn zhāi): do not listen with the ears, nor even with the mind, but with the qi — the open, receptive energy that has emptied itself of its own agenda. The image transforms letting go. Emptiness here is not loss or deprivation; it is the precondition for genuine reception. When you stop filling every space with your own commentary, preference, and self, you can finally hear what is actually there — another person, a situation, reality itself. To empty is not to become less; it is to become available. This is letting go as hospitality rather than sacrifice.",
        keyIdea:
          "Emptiness is not deprivation; it is the openness that lets you truly receive what is there.",
        misconception:
          "That emptying yourself means becoming blank or diminished. It means becoming spacious and available.",
        passageId: "the_book_of_chuang_tzu.zhuangzi_md_004",
        supportingPassageIds: ["the_book_of_chuang_tzu.zhuangzi_md_006"],
        theme: "emptiness",
        chatMode: "practice",
        chatPrompt:
          "Give me a heart-fasting style practice based on this passage. How do I empty myself to receive rather than to lose?",
        practice:
          "In your next conversation, listen for one minute without preparing a reply. Empty the space you usually fill with your own thoughts and simply receive what the other person is saying.",
        journalPrompt:
          "What did I hear differently when I stopped filling the space with myself? Where does my commentary crowd out reception?",
        integration:
          "You can deliberately empty your inner commentary to receive a person or situation more fully.",
      },
      {
        id: "use-absence",
        title: "Discover the use of absence",
        orientation:
          "We deepen emptiness from a personal stance into a structural insight about reality.",
        teaching:
          "The Tao Te Ching points to the axle-hole, the empty room, the hollow of a vessel: in each, it is the absence that makes the thing useful. Clay forms the cup, but the emptiness inside holds the tea; walls make the room, but the empty space is where you live. This is a quiet revolution in how to see. We habitually value only presence, accumulation, fullness — and overlook that absence, gap, and silence are not deficiencies but the very conditions of function. Applied to a life: the pauses, the unscheduled space, the things you do not say, the room you leave for others — these are not wasted. They are where everything actually happens.",
        keyIdea:
          "Absence is functional, not deficient — the gap is what makes the whole thing work.",
        misconception:
          "That emptiness and gaps are something missing to be filled. Often they are the most useful part.",
        passageId: "tao_te_ching.ttc_md_002",
        supportingPassageIds: ["tao_te_ching.ttc_md_001"],
        theme: "emptiness",
        chatMode: "compare",
        chatPrompt:
          "Compare Daoist functional emptiness here with Zhuangzi's receptive emptiness from the previous step. How are they different uses of 'empty'?",
        practice:
          "Hold the cup. Feel the clay, the weight, the lip. Then attend to the hollow the clay was thrown to make — the nothing that is what the cup is for. Drink from that. Now look at your day the same way: the schedule, the plan, the walls — and the space they were cut to serve. Leave one thing unfilled on purpose. Let the hollow do the work.",
        journalPrompt:
          "Where did an empty space, pause, or silence make action possible today? What do I rush to fill that I could leave open?",
        integration:
          "You can recognize the functional value of gaps and silences instead of compulsively filling them.",
      },
      {
        id: "enter-the-gap",
        title: "Enter the gap in the breath",
        orientation:
          "Now the path becomes fully embodied: a direct threshold practice for impermanence.",
        teaching:
          "The Vijñāna Bhairava locates the doorway not in a concept but in your own breath. Between every exhale and inhale, and every inhale and exhale, there is a brief pause — a turning-point where breath and thought momentarily cease. The tantra teaches that this gap is not empty in the sense of nothing; it is full (bharitā) in the sense of pure, contentless presence. Each pause is a miniature death-and-rebirth, an impermanence you can ride consciously rather than fear. Where the previous steps thought about emptiness and absence, this one has you feel it directly, in the most intimate and constant rhythm you have. The threshold of the breath is always available.",
        keyIdea:
          "The pause between breaths is a direct, always-available threshold of contentless presence.",
        misconception:
          "That you must hold or control the breath. You simply rest attention in the natural pause where it turns.",
        passageId: "vijnana_bhairava.yukti_001",
        supportingPassageIds: ["vijnana_bhairava.yukti_002"],
        theme: "breath",
        chatMode: "practice",
        chatPrompt:
          "Teach this breath threshold practice carefully and simply. What am I attending to in the pause, and what should I not do?",
        practice:
          "Follow your out-breath to its natural end. Rest in the still point before the in-breath for two or three seconds — feel it as spacious presence, not absence. Then rest again at the top of the in-breath. Continue for ten breaths, attending only to the turning-points.",
        journalPrompt:
          "What was present in the pause before the next breath or thought? Was the gap empty, or quietly full?",
        integration:
          "You can find and rest in the pause between breaths as a felt threshold of present awareness.",
      },
      {
        id: "final-composure",
        title: "Let composure become an offering",
        orientation:
          "The path closes by asking what a life rehearsed in release leaves behind.",
        teaching:
          "On his last day, Socrates is composed not because he is indifferent but because he has practiced release his whole life — and that composure becomes a gift to everyone in the room. This is the final turn: the inner work of letting go is not private. The way you meet loss, fear, and ending leaves a trace in others — a legacy of tone, courage, and care that outlasts any possession. Having trained with death, the unseen, emptiness, absence, and the breath, you arrive at the ethical question: what do I leave behind in the quality of my presence? Letting go, fully matured, becomes generosity — composure offered to those who will face what you faced.",
        keyIdea:
          "A life rehearsed in release matures into composure that becomes a gift to others.",
        misconception:
          "That this inner work is only about you. Its fruit shows up most in how you affect the people around you.",
        passageId: "phaedo_plato.phaedo_md_007",
        supportingPassageIds: ["phaedo_plato.phaedo_md_006"],
        theme: "death",
        chatMode: "practice",
        chatPrompt:
          "Help me turn Socrates' final composure into an ethical practice for today. How does my way of letting go affect others?",
        practice:
          "Recall one interaction today. Ask: what tone did I leave behind — anxiety or composure, grasping or care? In your next interaction, consciously offer the composure you've been practicing.",
        journalPrompt:
          "What legacy of tone, care, or courage did I leave in one interaction today?",
        integration:
          "You see your own composure as something you offer others, and can bring it deliberately into an interaction.",
      },
    ],
  },
  {
    id: "yoga-eight-limbs",
    title: "The Eight Limbs of Yoga",
    level: "Intermediate",
    focus: "Patañjali's Royal Yoga: stillness of mind's turnings",
    outcome:
      "Walk Patañjali's systematic path from ethical foundation through concentration to absorption, learning why the mind must be stilled and how to still it.",
    description:
      "A direct path through the Yoga Sūtras: the eight limbs (aṣṭāṅga) as a technology of liberation.",
    arc:
      "Yoga is here defined not as postures but as the complete cessation of the mind's oscillations (citta-vṛtti-nirodha). When the turnings stop, the seer rests in its own nature; when they continue, the seer is mistaken for the turnings. This path traces Patañjali's architecture: ethical restraints (yama, niyama) as the ground, posture and breath as the body's calming, sensory withdrawal as the hinge inward, and finally the three inner limbs (concentration, meditation, absorption) as one continuous deepening. You learn why control precedes surrender, why obstacles are named honestly, and how even powers (siddhis) can become distractions from the one freedom: kaivalya, the isolation of pure awareness from everything it is not.",
    estimatedSessions: "6 gates · ~25 min each",
    steps: [
      {
        id: "ys-define-yoga",
        title: "Yoga Is the Stilling of Mind's Turnings",
        orientation:
          "Gate I · The Definition. Before the method, the target must be named with surgical precision.",
        teaching:
          "Yoga is cessation: yogaś citta-vṛtti-nirodhaḥ. The mind churns — memories, plans, fears, fantasies — and you mistake that churning for who you are. When the turnings stop, the seer (draṣṭṛ) stands in its own nature (svarūpe), untouched. When they continue, you are identified with the turnings (vṛtti-sārūpyam). This is not philosophy but a testable claim: the mind's default state is agitation, and you cannot see clearly while the water is disturbed. Every technique in the remaining sūtras serves this one aim: still the water so the seer can see itself.",
        keyIdea: "Yoga is not a mood or a posture; it is the complete cessation of the mind's oscillations.",
        misconception:
          "That yoga is primarily physical. Patañjali names it as a mental discipline first — body serves mind.",
        passageId: "patanjali_yoga_sutras.ys_1_2",
        supportingPassageIds: ["patanjali_yoga_sutras.ys_1_3", "patanjali_yoga_sutras.ys_1_4"],
        theme: "definition",
        chatMode: "explain",
        chatPrompt:
          "Explain citta-vṛtti-nirodha — the cessation of mind's turnings — in a way I can test in my own experience right now.",
        practice:
          "Sit and watch your mind for three minutes without following any thought-stream. Each time you notice you've been carried away, gently return. The practice is not in never drifting; it is in the returning. That return is nirodha in seed form.",
        journalPrompt:
          "What are the recurring 'turnings' of my mind — the loops I get caught in — and can I feel the seer behind them?",
        integration:
          "You can distinguish between awareness itself and the contents it is aware of, and recognize the turnings as objects, not self.",
      },
      {
        id: "ys-obstacles",
        title: "The Obstacles Are Named Honestly",
        orientation:
          "Gate I · The Path. Patañjali does not promise ease; he catalogs what will arise and how to meet it.",
        teaching:
          "The obstacles (antarāya) to stilling are not moral failures but structural facts: illness, dullness, doubt, carelessness, sloth, distraction by sense-objects, false perception, failure to attain a stage, and instability in a stage once attained. And when obstacles arise, the mind becomes accompanied by suffering (duḥkha), depression, trembling of the limbs, and disturbed breath. The teaching is ruthlessly honest. You will get sick. You will doubt. The breath will roughen when the mind is disturbed. Knowing this in advance changes the relationship: obstacles are not proof you are doing it wrong; they are the curriculum. The response is not to will them away but to stabilize one principle (eka-tattva-abhyāsa) and practice friendliness, compassion, gladness, and equanimity toward all beings.",
        keyIdea: "Obstacles are not signs of failure; they are the expected texture of the path, to be met with steadiness.",
        misconception:
          "That a good practitioner would not experience doubt, distraction, or illness. Patañjali names them as inevitable.",
        passageId: "patanjali_yoga_sutras.ys_1_30",
        supportingPassageIds: ["patanjali_yoga_sutras.ys_1_31", "patanjali_yoga_sutras.ys_1_33"],
        theme: "obstacles",
        chatMode: "question",
        chatPrompt:
          "Help me understand how Patañjali's catalog of obstacles changes the way I relate to doubt and distraction in practice.",
        practice:
          "Name one obstacle you are currently experiencing on or off the cushion (doubt, distraction, sloth). Instead of treating it as evidence of inadequacy, say: 'This is sūtra 1.30 — the path is working.' Meet it with steadiness (abhyāsa) rather than shame.",
        journalPrompt:
          "Which obstacle from Patañjali's list is most active in my life right now, and how does naming it change my relationship to it?",
        integration:
          "You can name the obstacles you encounter as structural rather than personal, and meet them with equanimity.",
      },
      {
        id: "ys-eight-limbs",
        title: "The Eight Limbs as One Architecture",
        orientation:
          "Gate II · The System. Yoga is not scattered techniques; it is a graduated path, each limb depending on the prior.",
        teaching:
          "The eight limbs (aṣṭāṅga) are: yama (restraints with others), niyama (observances with oneself), āsana (posture), prāṇāyāma (breath regulation), pratyāhāra (sensory withdrawal), dhāraṇā (concentration), dhyāna (meditation), samādhi (absorption). The structure is deliberate. Ethical ground first: you cannot still the mind if you are creating harm and the mind knows it. Then the body: steady posture and smooth breath calm the nervous system, making inward attention possible. Then the senses are drawn in (pratyāhāra is the hinge — the moment perception stops being dragged outward). Only then do the three inner limbs begin: holding attention on one point (dhāraṇā), the point holding you (dhyāna), and the dissolution of the boundary between subject and object (samādhi). Each prepares the next. Skipping the early limbs produces fragile attainments that collapse under pressure.",
        keyIdea: "The eight limbs are not a menu; they are a sequence, each limb stabilizing the ground for the next.",
        misconception:
          "That you can jump straight to meditation or samādhi without ethical and somatic foundation. Patañjali insists on order.",
        passageId: "patanjali_yoga_sutras.ys_2_29",
        supportingPassageIds: ["patanjali_yoga_sutras.ys_2_30", "patanjali_yoga_sutras.ys_2_46"],
        theme: "system",
        chatMode: "explain",
        chatPrompt:
          "Walk me through the eight limbs as a system where each supports the next. Why does ethical conduct come before meditation?",
        practice:
          "Check your current practice. Are you trying to meditate (dhyāna) without first attending to restraint (yama) or posture (āsana)? Identify one earlier limb that needs strengthening and attend to it this week.",
        journalPrompt:
          "Which of the eight limbs is my actual foundation right now, and which am I skipping over in my hurry to reach samādhi?",
        integration:
          "You understand the eight limbs as a graduated system and can identify where you are in the sequence.",
      },
      {
        id: "ys-pratyahara",
        title: "Pratyāhāra — The Hinge Inward",
        orientation:
          "Gate III · The Withdrawal. Before the mind can concentrate, the senses must stop pulling outward.",
        teaching:
          "Pratyāhāra is sensory withdrawal: when the senses are no longer in contact with their objects, they imitate the nature of the mind itself — they stop reaching. This is not suppression or numbness; it is the voluntary redirection of attention. Ordinarily, perception is centrifugal: the eyes chase forms, the ears chase sounds, the tongue chases tastes. Even in stillness, the senses are hunting. Pratyāhāra is the reversal: attention stops flowing outward and rests in itself. Patañjali likens it to a tortoise drawing its limbs inward. The hinge matters because concentration (dhāraṇā) is impossible while the senses are still lobbying for attention. When pratyāhāra succeeds, the outer world does not disappear — you still hear the bird, see the wall — but it no longer commands you. Attention becomes yours to place rather than being seized by stimuli.",
        keyIdea: "Pratyāhāra is not sensory deprivation; it is the withdrawal of attention from being commanded by sense-objects.",
        misconception:
          "That sensory withdrawal means shutting down or becoming numb. It is redirection, not suppression.",
        passageId: "patanjali_yoga_sutras.ys_2_54",
        supportingPassageIds: ["patanjali_yoga_sutras.ys_2_55"],
        theme: "withdrawal",
        chatMode: "practice",
        chatPrompt:
          "Give me a practice for pratyāhāra — withdrawing the senses without suppressing them. How do I let the senses rest inward?",
        practice:
          "Sit with your eyes closed. Notice the sounds, the pressure of the seat, the temperature. Instead of following any sensation outward into story or preference, let attention rest at the inner surface where each arises. The sound is not chased; it arrives and is received. Five minutes.",
        journalPrompt:
          "Where do my senses habitually pull me outward, and can I feel the difference between that pull and a voluntarily placed attention?",
        integration:
          "You can withdraw attention from the command of sense-objects and rest it inward, without suppressing perception.",
      },
      {
        id: "ys-samadhi",
        title: "Samādhi — When the Object Alone Shines",
        orientation:
          "Gate III · Absorption. The three inner limbs culminate in a state where the boundary between knower and known dissolves.",
        teaching:
          "Concentration (dhāraṇā) is binding attention to one place. Meditation (dhyāna) is the unbroken flow of attention to that place. Samādhi is when the object alone shines, as if the mind were empty of its own form (svarūpa-śūnyam). The distinction is subtle but experiential. In concentration, you return again and again. In meditation, the returns become fewer; the flow is mostly unbroken. In samādhi, there is no returner — subject and object have not merged, but the sense of being a separate observer has thinned to the point that only the object seems present. Patañjali distinguishes stages: samādhi with seed (sabīja) — still referencing an object — and seedless (nirbīja), where even the object is transcended. The point is not to mystify absorption but to name it as the natural deepening of sustained attention when obstacles have been removed.",
        keyIdea: "Samādhi is not a special state imported; it is what happens when attention rests undistracted long enough for the subject-object boundary to thin.",
        misconception:
          "That samādhi is a rare, dramatic event. It is the quiet endpoint of sustained, obstacle-free attention.",
        passageId: "patanjali_yoga_sutras.ys_3_3",
        supportingPassageIds: ["patanjali_yoga_sutras.ys_1_41", "patanjali_yoga_sutras.ys_3_2"],
        theme: "absorption",
        chatMode: "explain",
        chatPrompt:
          "Explain the progression from dhāraṇā (concentration) to dhyāna (meditation) to samādhi (absorption) as a natural deepening.",
        practice:
          "Choose one object — the breath, a candle flame, a sound. Concentrate: return attention each time it wanders. After 5-10 minutes, notice if the returns become less effortful. That ease is the beginning of dhyāna. Do not force samādhi; let sustained attention reveal it.",
        journalPrompt:
          "Have I ever experienced the thinning of the subject-object boundary, even briefly? What was that like?",
        integration:
          "You understand samādhi as the natural culmination of sustained attention and can recognize its early signs.",
      },
      {
        id: "ys-kaivalya",
        title: "Kaivalya — The Isolation of Pure Seeing",
        orientation:
          "Gate IV · Liberation. The goal is not union but the recognition that awareness was never bound.",
        teaching:
          "Kaivalya is aloneness or isolation — not loneliness, but the recognition that pure awareness (puruṣa) is utterly distinct from the contents of experience (prakṛti). When the turnings of mind cease and even the subtlest identifications dissolve, awareness rests in itself, no longer mistaking itself for anything it perceives. This is the culmination of the whole system: not a merging with the divine (as in devotional paths), but a stark seeing-through. The powers (siddhis) that arise along the way — clairvoyance, control over elements, knowledge of past lives — are explicitly named as obstacles to kaivalya if clung to. They are displays of prakṛti's capacities, not the seer's nature. The final freedom is when awareness no longer needs to do anything, know anything, or become anything because it recognizes it was never not free. The path does not produce liberation; it removes the obscurations that made bondage seem real.",
        keyIdea: "Kaivalya is the isolation of awareness from all content — not a state to achieve, but the recognition of what was always true.",
        misconception:
          "That liberation is a special experience to attain. It is the seeing-through of the mistake that you were ever bound.",
        passageId: "patanjali_yoga_sutras.ys_4_34",
        supportingPassageIds: ["patanjali_yoga_sutras.ys_3_37", "patanjali_yoga_sutras.ys_4_26"],
        theme: "liberation",
        chatMode: "practice",
        chatPrompt:
          "Help me understand kaivalya as the end of mistaken identity rather than as a peak experience to collect.",
        practice:
          "Sit and ask: 'What am I aware of right now?' Note each answer (breath, sound, thought, sensation). Then ask: 'What is aware of all of this?' Rest as that — not as a special state, but as the ordinary awareness that was already here, mistaken for its contents.",
        journalPrompt:
          "If awareness was never bound, what is the 'work' of yoga actually undoing? What am I mistaking myself for?",
        integration:
          "You can hold kaivalya as the recognition of what is already true rather than as a distant goal, and practice accordingly.",
      },
    ],
  },
  {
    id: "buddhism-core",
    title: "The Buddhist Core",
    level: "Intermediate",
    focus: "Emptiness, compassion, and the end of suffering",
    outcome:
      "Walk the central teachings of Buddhism from suffering's diagnosis through emptiness to compassion — learning why clinging hurts, what 'empty' actually means, and how insight becomes care.",
    description:
      "A path through Buddhism's core: the Four Noble Truths, dependent origination, emptiness (śūnyatā), and the bodhisattva vow.",
    arc:
      "Buddhism begins with honesty: life as ordinarily lived involves suffering (duḥkha). Not as punishment, but as structural fact — because we cling to what changes. The diagnosis leads to a teaching about causation: nothing arises independently; everything is dependently originated (pratītyasamutpāda). Pushed further, this becomes the teaching of emptiness (śūnyatā): no thing has inherent, independent existence. The Heart Sūtra says it starkly — even the aggregates that seem to make up a self are empty. Nāgārjuna sharpens the edge: emptiness is not nihilism but the middle way between existence and non-existence. And the teaching does not end in detachment. Śāntideva and the Mahāyāna tradition insist: if all beings are empty of separate selfhood, compassion is not optional sentiment but the recognition of interdependence lived. Dōgen brings it into the body and the moment. Milarepa's songs show the path walked to its end in a Tibetan cave. The arc moves from suffering's diagnosis, through emptiness as liberating insight, to compassion as its ethical fruit.",
    estimatedSessions: "6 gates · ~25 min each",
    steps: [
      {
        id: "bud-dukkha",
        title: "The First Noble Truth — Life Involves Suffering",
        orientation:
          "Gate I · The Diagnosis. The Buddha names the problem with unflinching clarity before offering a cure.",
        teaching:
          "The First Noble Truth is duḥkha: suffering, unsatisfactoriness, the pervasive sense that things are not quite right. Birth is duḥkha, aging is duḥkha, sickness and death are duḥkha. Being separated from what you love is duḥkha; being stuck with what you hate is duḥkha; not getting what you want is duḥkha. Even pleasant experiences carry duḥkha because they will end and you will grieve the ending. This is not pessimism but precision. The teaching does not say life is only suffering, but that suffering is woven into the structure of ordinary existence. Why? Because we cling (upādāna) to what is impermanent (anicca) as if it could be made permanent, and to what has no fixed self (anattā) as if it were a solid identity. The diagnosis is the doorway: you cannot address a problem you refuse to name.",
        keyIdea: "Duḥkha is not moral punishment; it is the structural result of clinging to what is impermanent and selfless.",
        misconception:
          "That acknowledging suffering is pessimistic or life-denying. It is the precision required for diagnosis and cure.",
        passageId: "dhammapada.dhp_203",
        supportingPassageIds: ["heart_sutra.hs_001"],
        theme: "suffering",
        chatMode: "question",
        chatPrompt:
          "Help me see the First Noble Truth not as pessimism but as clear-eyed diagnosis. Where is duḥkha present in my ordinary life?",
        practice:
          "Notice one thing today you are clinging to — a plan, a relationship, a self-image, a mood. Feel the subtle grip. Ask: 'Is this permanent? Can I make it stay?' The gap between the grip and the answer is where duḥkha lives.",
        journalPrompt:
          "Where am I currently experiencing duḥkha, and can I trace it to clinging to something impermanent or insubstantial?",
        integration:
          "You can name duḥkha when it arises and recognize it as a structural response to clinging, not as a personal failure.",
      },
      {
        id: "bud-pratityasamutpada",
        title: "Dependent Origination — Nothing Stands Alone",
        orientation:
          "Gate II · The Mechanism. Suffering has a cause, and the cause is not arbitrary but lawful.",
        teaching:
          "The Second Noble Truth names craving (tṛṣṇā) as the cause of suffering. The Third promises cessation is possible. But the Buddha goes deeper: dependent origination (pratītyasamutpāda) is the map of how suffering arises and how it can be undone. Each link in the chain conditions the next: ignorance conditions formations, formations condition consciousness, consciousness conditions name-and-form, and so on through the senses, contact, feeling, craving, clinging, becoming, birth, and aging-and-death. This is not a one-time cosmogonic story but a description of how each moment of suffering is co-produced by conditions. The liberating insight is that if suffering is dependently arisen, it can dependently cease when the conditions are removed. You are not doomed by fate or original sin; you are caught in a net of causes that can be seen and loosened.",
        keyIdea: "Suffering arises from causes and conditions (pratītyasamutpāda), which means it can cease when those conditions are removed.",
        misconception:
          "That suffering is random or punishment. It is lawful, conditioned, and therefore workable.",
        passageId: "nagarjuna_mulamadhyamakakarika.mmk_24_18",
        supportingPassageIds: ["dhammapada.dhp_277"],
        theme: "causation",
        chatMode: "explain",
        chatPrompt:
          "Walk me through dependent origination (pratītyasamutpāda) as a mechanism I can see operating in my own life. How does ignorance condition the chain?",
        practice:
          "Trace one instance of reactivity backward: anger arose from aversion, aversion from unpleasant contact, contact from sense-meeting-object, the meeting from craving for things to be different. See the chain. Then ask: if craving had not arisen, would the anger have followed?",
        journalPrompt:
          "Can I see one pattern of suffering in my life as dependently originated — a chain of causes I can name and potentially interrupt?",
        integration:
          "You can trace suffering back through its causes and recognize it as conditionally arisen rather than fixed.",
      },
      {
        id: "bud-sunyata",
        title: "Emptiness — No Thing Has Independent Existence",
        orientation:
          "Gate III · The Insight. Dependent origination, followed to its end, becomes the teaching of emptiness.",
        teaching:
          "The Heart Sūtra declares: form is emptiness, emptiness is form. What does this mean? Emptiness (śūnyatā) is not nothingness; it is the absence of inherent, independent existence (svabhāva). Because all things arise dependently, no thing stands alone, permanent, and self-sufficient. The table is 'empty' not because it is not there, but because it is a temporary confluence of wood, labor, rain, seed, soil, and the intention to sit — none of which are themselves independent. Even 'you' are empty: the five aggregates (form, feeling, perception, mental formations, consciousness) that seem to compose a self are themselves dependently arisen and in flux. Emptiness is not a nihilistic void but the interdependence of all phenomena. It is liberating because clinging depends on reifying things as solid and separate. When you see emptiness, the grip loosens — not because nothing matters, but because the solidity you were grasping was never there.",
        keyIdea: "Emptiness (śūnyatā) is not nothingness; it is the absence of independent, inherent existence. All things are dependently originated.",
        misconception:
          "That emptiness means nothing exists or nothing matters. It means no thing exists independently — which is interdependence.",
        passageId: "heart_sutra.hs_001",
        supportingPassageIds: ["nagarjuna_mulamadhyamakakarika.mmk_24_18", "nagarjuna_mulamadhyamakakarika.mmk_01_01"],
        theme: "emptiness",
        chatMode: "compare",
        chatPrompt:
          "Compare Buddhist emptiness (śūnyatā) with the Tao's 'useful absence' and the Śaiva 'void as fullness.' How is emptiness not nihilism?",
        practice:
          "Hold an object (a cup, a pen). Name everything it depends on: materials, makers, causes stretching back. Ask: where does the 'cup' actually begin or end? Feel how it is empty of independent existence — not absent, but utterly relational.",
        journalPrompt:
          "If 'I' am also empty — dependently originated from aggregates, causes, conditions — does that make me less real, or differently real?",
        integration:
          "You can see emptiness as interdependence rather than nihilism, and apply it to both objects and the sense of self.",
      },
      {
        id: "bud-nagarjuna-middle",
        title: "Nāgārjuna's Middle Way — Beyond Existence and Non-Existence",
        orientation:
          "Gate III · The Refinement. Emptiness sharpens into the Middle Way: neither is nor is-not.",
        teaching:
          "Nāgārjuna, the great Madhyamaka philosopher, took the teaching of emptiness to its logical end. If all things are empty of inherent existence, then emptiness itself is empty. Clinging to emptiness as a position is still clinging. The Middle Way is neither asserting that things exist (eternalism) nor that they don't exist (nihilism). Things arise dependently; they function; they are not non-existent. But they do not have fixed, independent being; they are not existent in the way we naively suppose. This middle position is not a compromise but the only view that does not reify or annihilate. It is the philosophical precision behind the liberating insight: when you stop trying to grasp existence or non-existence, you can meet what is as it dependently arises.",
        keyIdea: "The Middle Way is neither existence nor non-existence — things arise dependently, neither solidly real nor utterly unreal.",
        misconception:
          "That the Middle Way is a vague compromise. It is razor-sharp: it refuses both reification and annihilation.",
        passageId: "nagarjuna_mulamadhyamakakarika.mmk_01_01",
        supportingPassageIds: ["nagarjuna_mulamadhyamakakarika.mmk_24_18"],
        theme: "middle-way",
        chatMode: "explain",
        chatPrompt:
          "Explain Nāgārjuna's Middle Way as a philosophical precision tool that cuts through both eternalism and nihilism.",
        practice:
          "Notice a judgment: 'This is good' or 'This is bad.' Feel how the judgment reifies the thing as independently having that quality. Now soften: the experience arose dependently; 'good' and 'bad' are relational, not inherent. Rest in the middle — neither affirming nor denying.",
        journalPrompt:
          "Where do I cling to things as if they were independently real (eternalism), and where do I dismiss them as if they were unreal (nihilism)?",
        integration:
          "You can recognize the Middle Way as a precision that avoids both grasping existence and falling into nihilism.",
      },
      {
        id: "bud-bodhisattva",
        title: "The Bodhisattva Vow — Compassion as Insight's Fruit",
        orientation:
          "Gate IV · The Turn. Emptiness does not end in detachment; it flowers into compassion.",
        teaching:
          "Śāntideva and the Mahāyāna tradition ask: if all beings are empty of separate, inherent selfhood, what is the ethical consequence? The bodhisattva vow is the answer: 'I will not enter final peace until all beings are liberated.' This is not a deferral of liberation out of guilt or martyrdom; it is the recognition that 'self' and 'other' are empty designations. If you and I are both dependently originated, your suffering is not happening to a truly separate being — it is suffering, period, and compassion is the natural response when that is seen. The bodhisattva does not abandon wisdom for compassion; compassion is what wisdom looks like when it meets suffering. Emptiness without compassion is incomplete; compassion without emptiness devolves into burnout or sentimentality. Together, they are the two wings of the path.",
        keyIdea: "Compassion (karuṇā) is not sentiment; it is the ethical consequence of seeing emptiness and interdependence clearly.",
        misconception:
          "That emptiness leads to cold detachment. In Mahāyāna, emptiness is the ground of boundless compassion.",
        passageId: "shantideva_bodhicaryavatara.bca_3_10",
        supportingPassageIds: ["shantideva_bodhicaryavatara.bca_8_90"],
        theme: "compassion",
        chatMode: "practice",
        chatPrompt:
          "Help me connect the insight of emptiness with the practice of compassion. How does seeing interdependence naturally produce care?",
        practice:
          "Think of someone you are in conflict with. Imagine their life as a stream of causes and conditions, just like yours — childhood, wounds, hopes, confusion. See them as empty of fixed selfhood, dependently arisen. Does the sense of absolute separation soften? That softening is the beginning of compassion.",
        journalPrompt:
          "If all beings are empty and interdependent, how does that change the way I hold my own needs and the needs of others?",
        integration:
          "You can hold emptiness and compassion together as one teaching: insight into interdependence that becomes care.",
      },
      {
        id: "bud-dogen-now",
        title: "Dōgen — This Very Body, This Very Moment",
        orientation:
          "Gate IV · The Embodiment. Zen master Dōgen brings the whole path into the immediacy of sitting and the ordinariness of now.",
        teaching:
          "Dōgen insists: practice is not a means to enlightenment; practice is enlightenment. Zazen (sitting meditation) is not a technique to produce a future awakening; it is Buddha-nature expressing itself right now, in this posture, this breath. The error is treating enlightenment as something distant to attain. Dōgen flips it: this very body is the Buddha-body; this very sitting is realization. The thinking that arises in zazen is not an obstacle to be eliminated but 'the scenery of original nature.' Mountains are mountains, rivers are rivers — not as metaphors but as they are, when conceptual overlay ceases. The teaching is radically anti-transcendental: you do not need to go elsewhere, become other, or wait for a special state. The ordinary is already it. The work is to stop adding commentary and meet what is.",
        keyIdea: "Practice is not a path to enlightenment; practice itself is enlightenment expressing in this body, this moment.",
        misconception:
          "That enlightenment is a rare, distant state to achieve. Dōgen says it is here, now, in the act of sitting itself.",
        passageId: "dogen_shobogenzo.sg_genjokoan_01",
        supportingPassageIds: ["dogen_shobogenzo.sg_zazenshin_01"],
        theme: "immediacy",
        chatMode: "practice",
        chatPrompt:
          "How do I practice Dōgen's teaching that 'this very sitting is Buddha'? What does it mean to stop seeking and just sit?",
        practice:
          "Sit for ten minutes. Do not meditate to become enlightened or to fix yourself. Just sit, as sitting. When the mind says 'this is boring' or 'am I doing it right?', notice that as thinking, let it be, and return to just sitting. The sitting itself is enough.",
        journalPrompt:
          "What would change if I treated this ordinary moment — this breath, this task — as already complete rather than as preparation for something better?",
        integration:
          "You can sit without the agenda of attainment, recognizing the practice itself as expression of awakened nature.",
      },
    ],
  },
  {
    id: "sufi-love-path",
    title: "The Sufi Path of Love",
    level: "Intermediate",
    focus: "The Beloved hidden in plain sight — love as the way",
    outcome:
      "Walk the Sufi path from Ibn ʿArabī's metaphysics of unity to Rūmī's ecstatic poetry, learning how love is both method and goal.",
    description:
      "A path through Sufi teaching: the unity of being (waḥdat al-wujūd), annihilation in the Beloved (fanāʾ), and love as the secret.",
    arc:
      "The Sufi path begins with a metaphysical claim as bold as any in the non-dual traditions: there is only One Reality (al-Ḥaqq), and everything that appears is Its self-disclosure. Ibn ʿArabī calls this waḥdat al-wujūd, the unity of being. You are not separate from the Beloved; you are the Beloved's way of knowing Itself through a particular aperture. The seeker (sālik) walks a path of stations (maqāmāt) and states (aḥwāl), learning to die to the false self (fanāʾ) so the Real can live through them (baqāʾ). Rūmī sings this teaching: the wound is where the light enters, the lover and Beloved are one flame. The path is not renunciation of the world but seeing the world as love-play, every encounter as the Beloved in disguise. Longing (shawq) is the engine; love (ʿishq) is the fuel; union (ittihād, carefully distinguished from identity) is the homecoming that was never really a departure.",
    estimatedSessions: "5 gates · ~20 min each",
    steps: [
      {
        id: "sufi-wahdat",
        title: "Waḥdat al-Wujūd — The Unity of Being",
        orientation:
          "Gate I · The Metaphysics. Ibn ʿArabī names the ground: there is only One Reality, appearing as many.",
        teaching:
          "Waḥdat al-wujūd (the unity of being) is Ibn ʿArabī's central teaching: existence itself is one. The many appearances — you, the tree, the thought, the star — are not separate existences but modes (shuʾūn) or self-disclosures (tajalliyāt) of the One Real (al-Ḥaqq). This is not pantheism (the universe is God) but panentheism (the universe is God's self-expression, but God is not exhausted by it). Every particular thing is like a mirror reflecting the One; the reflection is real as a reflection, but it has no independent being apart from the One it reflects. To see this is not to dissolve the world into abstraction but to see every particular as sacred, because it is the Beloved's face. The separation you feel is not metaphysical fact but epistemological ignorance (jahl). The path is the progressive removal of that ignorance.",
        keyIdea: "Waḥdat al-wujūd: all existence is one; the many are the One's self-disclosure, not separate beings.",
        misconception:
          "That this teaching erases distinction or makes ethics irrelevant. The One appears as the many; the task is seeing the One in the many.",
        passageId: "ibn_arabi_know_yourself.ia_001",
        supportingPassageIds: ["ibn_arabi_know_yourself.ia_002"],
        theme: "unity",
        chatMode: "compare",
        chatPrompt:
          "Compare Ibn ʿArabī's waḥdat al-wujūd with Kashmir Śaivism's citi and Plotinus' One. How is Sufi unity both similar and distinct?",
        practice:
          "Look at three very different things — a stone, a tree, a person. Ask of each: 'Whose existence is this? Who is appearing here?' Let the answer be: the One, disclosing Itself differently. See if the felt separation softens.",
        journalPrompt:
          "If all existence is the One Reality appearing, how does that change the way I hold separation, loneliness, or conflict?",
        integration:
          "You can see the world as the One's self-disclosure rather than as a collection of separate, independent beings.",
      },
      {
        id: "sufi-fana",
        title: "Fanāʾ — Annihilation of the False Self",
        orientation:
          "Gate II · The Death. The path requires a death: the constructed self must dissolve so the Real can live.",
        teaching:
          "Fanāʾ is extinction or annihilation — but not of your actual being. It is the death of the illusion that you are a separate, independent self (nafs) standing over against God. The Sufi analogy: a drop returns to the ocean. The drop does not cease to be; it ceases to be separate. The 'I' that says 'I am the lover and God is the Beloved' must die so the truth can be spoken: 'There is no lover but the Beloved.' This is terrifying and exhilarating. Terrifying because the constructed self clings to its story, its defenses, its boundaries. Exhilarating because what remains after fanāʾ is not absence but baqāʾ (subsistence in God) — the recognition that the life you thought was yours was always the Beloved's life, animating this form. Fanāʾ is not cultivated by force; it is what happens when longing becomes so intense that the boundary can no longer be maintained.",
        keyIdea: "Fanāʾ is the death of the illusion of separate selfhood, not the annihilation of being — what remains is the Beloved's life in you.",
        misconception:
          "That fanāʾ is literal death or self-destruction. It is the death of illusion, not of existence.",
        passageId: "rumi_mathnawi.rumi_001",
        supportingPassageIds: ["rumi_mathnawi.rumi_002"],
        theme: "annihilation",
        chatMode: "question",
        chatPrompt:
          "Help me understand fanāʾ as the death of false self rather than the annihilation of my being. What survives the death?",
        practice:
          "Sit and silently repeat: 'Not I, but the Beloved.' Feel the contraction of 'I' each time it asserts itself. Do not fight it; just notice it, and offer it back: 'Not I, but the Beloved.' Let the boundary soften.",
        journalPrompt:
          "What parts of my constructed self — my story, my defenses, my identity — am I most afraid to let die? What might remain if they did?",
        integration:
          "You can distinguish the constructed self (nafs) from essential being, and begin to loosen the grip on the former.",
      },
      {
        id: "sufi-love-method",
        title: "Love as Method, Not Only Goal",
        orientation:
          "Gate III · The Secret. Rūmī reveals: love is not the reward of the path; love is the path itself.",
        teaching:
          "Rūmī writes: 'Let yourself be silently drawn by the strange pull of what you really love. It will not lead you astray.' In Sufism, love (ʿishq) is not a feeling to manage or a distraction from spiritual work — it is the method. The longing (shawq) you feel for the Beloved is the Beloved pulling you home. Every heartbreak, every ache of separation, is the Beloved teaching you that nothing finite will satisfy. This is why Sufi poetry is so often erotic and intoxicated: the language of human love is the closest analog we have for the soul's relationship with the Real. The path is not to transcend desire but to let desire become singular, total, aimed only at the One. When that happens, even ordinary encounters — a friend, a bird, a stranger — become meetings with the Beloved in disguise. Love stops being a feeling you have and becomes the texture of seeing.",
        keyIdea: "Love (ʿishq) is not the goal but the method — longing for the Beloved is the Beloved pulling you home.",
        misconception:
          "That spiritual maturity means transcending desire or love. Sufism refines desire into a single flame aimed at the Real.",
        passageId: "rumi_mathnawi.rumi_003",
        supportingPassageIds: ["rumi_mathnawi.rumi_004"],
        theme: "love",
        chatMode: "practice",
        chatPrompt:
          "Give me a practice for turning longing into a spiritual method. How do I let desire for the Beloved refine ordinary desire?",
        practice:
          "Name one thing you long for — success, connection, peace, recognition. Feel the longing fully. Now ask: 'What is the longing underneath this longing?' Keep asking until you reach the wordless ache for union itself. That is shawq. Let it remain without trying to satisfy it with substitutes.",
        journalPrompt:
          "Where is my longing scattered across many objects, and can I feel the single longing for the Beloved underneath all of them?",
        integration:
          "You can recognize longing as the Beloved's call rather than as a deficiency to fix, and let it refine your desires.",
      },
      {
        id: "sufi-hidden-beloved",
        title: "The Beloved Hidden in Plain Sight",
        orientation:
          "Gate III · The Recognition. Every face you meet is the Beloved's face; the ordinary is already sacred.",
        teaching:
          "Rūmī teaches: 'Wherever you are, and whatever you do, be in love.' Not love as sentiment, but love as the recognition that everything is the Beloved's self-expression. The stranger on the street, the difficult colleague, the flaw in yourself — all are masks the Beloved wears. This is not an abstract metaphysical claim but a lived practice of vision. The Sufi sees with the 'eye of the heart' (ʿayn al-qalb), and through that eye, separation dissolves. The entire universe becomes a love letter written in a thousand scripts. This teaching prevents the spiritual path from becoming an escape: you do not flee the world to find the Beloved; you learn to see that the world is where the Beloved has always been, hiding in plain sight, waiting to be recognized.",
        keyIdea: "The Beloved is not distant but hidden in every encounter, every moment — the ordinary is the sacred in disguise.",
        misconception:
          "That spiritual life is about withdrawing from the world. Sufism says: the world is the Beloved's self-disclosure; stay and see.",
        passageId: "rumi_mathnawi.rumi_005",
        supportingPassageIds: ["ibn_arabi_know_yourself.ia_003"],
        theme: "presence",
        chatMode: "explain",
        chatPrompt:
          "Explain the Sufi teaching that the Beloved is hidden in every face and every moment. How does this change daily encounters?",
        practice:
          "In three interactions today, silently say before you speak: 'The Beloved is looking at me through these eyes.' Meet the person with that recognition. Notice if it changes the quality of attention you bring.",
        journalPrompt:
          "Can I recall one ordinary moment today where, if I had been paying attention, I might have recognized the Beloved's presence?",
        integration:
          "You can practice seeing the Beloved in ordinary encounters, not as a metaphor but as a recognition that changes perception.",
      },
      {
        id: "sufi-wound-light",
        title: "The Wound Is Where the Light Enters",
        orientation:
          "Gate IV · The Alchemy. Rūmī closes the path with the teaching that makes brokenness sacred.",
        teaching:
          "Rūmī writes: 'The wound is the place where the Light enters you.' This is the culmination of the Sufi path: suffering is not an obstacle to be removed before the real work can begin; it is the crack through which grace pours. Every heartbreak, every failure, every moment of not-knowing is the Beloved's way of widening you so more love can enter. The false self (nafs) is polished by difficulty; the heart (qalb) is opened by what it cannot control. This is not resignation or masochism — it is the recognition that the path does not run around pain but through it. Rūmī himself walked this: loss of his teacher Shams shattered him, and from that shattering poured the Mathnawī, 25,000 couplets of love. The wound does not need to be healed before you are whole; the wound is where you become whole.",
        keyIdea: "The wound is not an obstacle but the opening through which the Beloved enters — brokenness is sacred.",
        misconception:
          "That spiritual progress means transcending pain. Sufism says pain is the chisel that carves the heart into capacity.",
        passageId: "rumi_mathnawi.rumi_006",
        supportingPassageIds: ["rumi_mathnawi.rumi_007"],
        theme: "suffering",
        chatMode: "practice",
        chatPrompt:
          "Help me hold Rūmī's teaching that 'the wound is where the Light enters' in a way that honors both the pain and the opening it creates.",
        practice:
          "Bring to mind one wound — a grief, a failure, a betrayal. Instead of trying to close it or 'get over it,' ask: 'What has this opened in me? What capacity was not there before?' Let the wound be the teacher.",
        journalPrompt:
          "What wound in my life has, despite the pain, opened me to a depth or capacity I did not have before? Can I hold it as sacred?",
        integration:
          "You can meet suffering as the place where the Beloved is working on you, rather than as evidence you are off the path.",
      },
    ],
  },
  {
    id: "christian-mysticism",
    title: "Christian Mysticism — The Divine Darkness",
    level: "Advanced",
    focus: "The via negativa: unknowing as the highest knowing",
    outcome:
      "Walk the Christian mystic path from Dionysius' divine darkness through Eckhart's God beyond God to the Cloud of Unknowing's tender negation.",
    description:
      "The apophatic tradition: God is known by unknowing, encountered in darkness, named only by unsaying.",
    arc:
      "The Christian mystic tradition, at its most radical, insists: God is not a being among beings, not even the highest being, but beyond being itself. Dionysius the Areopagite names this the via negativa, the negative way: every name for God (good, wise, powerful) must be unsaid, because God transcends every category the mind can form. Meister Eckhart pushes further: there is God and the Godhead; God is the personal, relational Lord, but the Godhead is the nameless ground beyond personality, where even 'God' as a name falls away. The soul's highest work is Gelassenheit, releasement — letting go of images, concepts, and even the will to possess God. The Cloud of Unknowing teaches this as method: place everything you know beneath a 'cloud of forgetting' and reach toward God with a 'dart of longing love' through a cloud of unknowing. The fruit is not information about God but intimate union in darkness, where knower and known are no longer two.",
    estimatedSessions: "5 gates · ~20 min each",
    steps: [
      {
        id: "cm-via-negativa",
        title: "The Via Negativa — God Beyond Every Name",
        orientation:
          "Gate I · The Method. Dionysius opens the path: God is known not by what can be said, but by unsaying all names.",
        teaching:
          "Pseudo-Dionysius teaches the via negativa (negative way) as the highest theology. Every affirmation about God (God is good, God is wise, God is loving) is true as a pointer, but inadequate and ultimately false if taken literally, because God transcends all qualities the mind can name. Cataphatic theology (the way of affirmation) is a ladder you must eventually abandon. The via negativa climbs by unsaying: God is not good (in the way we know goodness), not wise (in the way we know wisdom), not even being (in the way we know beings). This is not nihilism; it is the recognition that God is beyond all categories — not less than being, but beyond it. The divine darkness is not absence but excess: too much light for the eye to see, so it registers as dark. To approach God is to enter a luminous unknowing.",
        keyIdea: "The via negativa: God is known by unknowing, approached by unsaying every name, encountered in divine darkness.",
        misconception:
          "That the negative way is atheism or emptiness. It is the recognition that God exceeds every concept, even the concept 'God.'",
        passageId: "pseudo_dionysius.pd_divine_names_01",
        supportingPassageIds: ["pseudo_dionysius.pd_mystical_theology_01"],
        theme: "negation",
        chatMode: "compare",
        chatPrompt:
          "Compare Dionysius' via negativa with Buddhist emptiness and the Upaniṣadic neti neti (not this, not this). How is apophatic theology similar and different?",
        practice:
          "Bring to mind your image of God or the Ultimate. Name the qualities: loving, powerful, wise. Now unsay each: 'not loving as I know love,' 'not powerful as I know power.' Keep unsaying until you reach a luminous not-knowing. Rest there.",
        journalPrompt:
          "What images or concepts of the divine am I clinging to, and what remains if I unsay them all?",
        integration:
          "You can practice unsaying your concepts of God, approaching the divine through luminous unknowing rather than through affirmation.",
      },
      {
        id: "cm-eckhart-godhead",
        title: "Eckhart — God and the Godhead",
        orientation:
          "Gate II · The Distinction. Meister Eckhart names the most radical distinction in Christian mysticism: God and the Godhead.",
        teaching:
          "Eckhart distinguishes God (Gott) from the Godhead (Gottheit). God is the personal, creative, relational Lord — Father, Son, Spirit — who loves, commands, and saves. The Godhead is the silent, nameless ground beyond all distinctions, the 'desert' or 'wilderness' where even the Trinity has not yet differentiated. To reach the Godhead, the soul must pass beyond God-as-person into the ground of the ground, where there is no 'I and Thou' but only the One. This is not atheism; it is the deepest theism, recognizing that the God we relate to is a face of something utterly beyond face. Eckhart's prayer is startling: 'I pray God to rid me of God' — meaning, let me pass beyond even my concept and experience of God into the nameless source. This teaching risks heresy (Eckhart was investigated), but it preserves the ultimate transcendence of the divine.",
        keyIdea: "God is the personal face of the Godhead; to reach the ultimate ground, even 'God' as a concept must be released.",
        misconception:
          "That Eckhart is denying God. He is distinguishing the relational God from the ground beyond all relation.",
        passageId: "meister_eckhart.me_sermon_52",
        supportingPassageIds: ["meister_eckhart.me_sermon_12"],
        theme: "godhead",
        chatMode: "explain",
        chatPrompt:
          "Explain Eckhart's distinction between God and Godhead in a way that shows it as deepening rather than denying relationship with the divine.",
        practice:
          "In prayer or meditation, relate to God as personal — speak, listen, feel the relationship. Then, gently, let even that relationship dissolve. Enter the silent ground where no one is speaking and no one is listening. Rest in the desert of the Godhead.",
        journalPrompt:
          "What would it mean to 'let go of God' — not as abandoning faith, but as releasing every fixed image to encounter the nameless ground?",
        integration:
          "You can hold both God-as-relation and the Godhead-beyond-relation, and recognize when the path calls you beyond even the personal divine.",
      },
      {
        id: "cm-gelassenheit",
        title: "Gelassenheit — Releasement and Poverty of Spirit",
        orientation:
          "Gate III · The Letting-Go. Eckhart names the soul's work: not achieving but releasing, not possessing but letting be.",
        teaching:
          "Gelassenheit is Eckhart's term for releasement or letting-be: the soul empties itself of images, desires, and even the will to possess God. 'Poverty of spirit' does not mean material lack; it means interior nakedness — not wanting, not willing, not knowing anything. The paradox: when you stop trying to grasp God, God can work freely in you. As long as you are 'full' of images, intentions, and self-project, there is no room for the divine to act. Gelassenheit is radical trust: you release the grip on outcomes, identities, and even your spiritual attainment. What remains is not absence but presence — not your life possessing God, but God's life living through you. This is the meeting point with Zen's 'no-self,' Sufism's fanāʾ, and the Śaiva recognition: the small self must get out of the way.",
        keyIdea: "Gelassenheit: releasement of all grasping, all images, all will — poverty of spirit as the condition for divine union.",
        misconception:
          "That poverty of spirit means passivity or giving up. It is active release, making space for grace to work unimpeded.",
        passageId: "meister_eckhart.me_poverty_of_spirit",
        supportingPassageIds: ["meister_eckhart.me_sermon_5b"],
        theme: "releasement",
        chatMode: "practice",
        chatPrompt:
          "Give me a practice for Gelassenheit — releasing the will to possess or control, including the will to possess God.",
        practice:
          "Sit in silence. Notice every subtle reaching: the wish to feel calm, to have an insight, to 'get it right.' Each time, release: 'Not my will.' Let even the wish for God's presence dissolve. Rest in empty openness, asking nothing.",
        journalPrompt:
          "What am I still trying to possess or control, even in my spiritual life? Can I practice Gelassenheit — releasing the grip on outcomes?",
        integration:
          "You can practice releasing the will to possess, control, or even experience God, and trust the emptiness you fear.",
      },
      {
        id: "cm-cloud-unknowing",
        title: "The Cloud of Unknowing — Love Through Darkness",
        orientation:
          "Gate IV · The Practice. The anonymous English mystic gives the path a method: reach through unknowing with love alone.",
        teaching:
          "The Cloud of Unknowing teaches: place everything you know and everything you are beneath a 'cloud of forgetting.' Above you is the 'cloud of unknowing' — the impenetrable darkness where God dwells, beyond all thought, image, and feeling. You cannot pierce this cloud with intellect or imagination. The only tool is a 'dart of longing love' — a naked intent toward God, stripped of all content. This is not an emotional state but a gesture of will: you aim your whole being at the divine, through the cloud, not knowing what you are aiming at or if you have reached. The teaching is tender: you are not abandoned in darkness; you are held in it. The cloud is not emptiness but intimacy beyond form. Unknowing becomes the highest knowing because it is union, not information.",
        keyIdea: "The cloud of unknowing: reach toward God through darkness with love alone, abandoning all concepts and images.",
        misconception:
          "That unknowing is confusion or ignorance. It is luminous intimacy beyond the reach of thought.",
        passageId: "cloud_of_unknowing.cou_chapter_03",
        supportingPassageIds: ["cloud_of_unknowing.cou_chapter_06"],
        theme: "unknowing",
        chatMode: "practice",
        chatPrompt:
          "Walk me through the Cloud of Unknowing's practice: forgetting below, unknowing above, and the dart of love piercing through.",
        practice:
          "Sit and imagine placing every thought, memory, image beneath you — the cloud of forgetting. Above is darkness — the cloud of unknowing. Through it, shoot a single wordless dart: love aimed at the unseen. No content, no image, just naked longing. Return each time the mind wanders. Ten minutes.",
        journalPrompt:
          "What was it like to aim love at what I cannot see, know, or imagine? Did the unknowing feel like abandonment or intimacy?",
        integration:
          "You can practice reaching toward the divine through unknowing with love, abandoning the need to understand or visualize.",
      },
      {
        id: "cm-union-darkness",
        title: "Union in Darkness — Knower and Known",
        orientation:
          "Gate IV · The Fruit. The apophatic path ends not in knowledge about God but in union beyond distinction.",
        teaching:
          "The mystics report: when the via negativa is walked to its end, something shifts. The one who was seeking and the One who was sought are no longer two. Dionysius speaks of mystical union (hénōsis) where the soul 'knows by unknowing.' Eckhart says the soul discovers it was always one with the Godhead's ground — 'I and the Father are one,' not as blasphemy but as realized truth. The Cloud teaches that love in darkness becomes identity: not that you become God, but that the life you thought was yours is recognized as God's life, lived through this form. This is the meeting point with all non-dual paths: the separation was epistemic, not ontological. You were never outside the One; you only thought you were. The darkness was not God's absence but the blinding excess of presence.",
        keyIdea: "Union in darkness: the apophatic path culminates not in knowing God but in being one with God beyond distinction.",
        misconception:
          "That union means losing yourself. It means finding who you always were — the divine life, never separate.",
        passageId: "meister_eckhart.me_sermon_6",
        supportingPassageIds: ["pseudo_dionysius.pd_mystical_theology_01", "cloud_of_unknowing.cou_chapter_26"],
        theme: "union",
        chatMode: "explain",
        chatPrompt:
          "Explain mystical union as the mystics describe it: not information about God, but identity with God beyond subject-object distinction.",
        practice:
          "Rest in the unknowing. Do not try to feel union or manufacture an experience. Simply be, without commentary, without reaching. If a sense arises that you and the darkness are not two, do not grasp it. Let it be.",
        journalPrompt:
          "If union is not an experience to collect but the recognition of what has always been true, what changes in how I relate to spiritual practice?",
        integration:
          "You can hold union as recognition rather than attainment, and meet the divine darkness as intimacy beyond form.",
      },
    ],
  },
  {
    id: "yoruba-wisdom",
    title: "Yoruba Wisdom",
    level: "Beginner",
    focus: "Proverbs (Òwe) as practical philosophy and ethical guidance",
    outcome:
      "Learn to see through Yoruba eyes: how proverbs encode wisdom about character, community, patience, and the art of living well.",
    description:
      "A path through Yoruba oral wisdom: proverbs (òwe) as condensed teachings on ethics, relationship, and the shape of a good life.",
    arc:
      "The Yoruba tradition of West Africa (primarily Nigeria, Benin, Togo) carries its philosophy not in written treatises but in proverbs — compressed, memorable teachings passed orally across generations. A proverb (òwe) is not decoration; it is a philosophical claim about how reality works and how to move through it with wisdom. The elders say: 'Proverbs are the horses of speech; when communication is lost, we use proverbs to retrieve it.' This path walks through core Yoruba teachings: the importance of good character (ìwà), respect for elders and ancestors, the necessity of patience (sùúrù), the power of community (ìjọba), and the recognition that the world is relational, not individualistic. Every proverb is a lens; together, they form a coherent worldview rooted in balance, reciprocity, and the long view.",
    estimatedSessions: "5 gates · ~15 min each",
    steps: [
      {
        id: "yor-iwa",
        title: "Ìwà — Character Is Destiny",
        orientation:
          "Gate I · The Foundation. Yoruba philosophy begins and ends with ìwà: good character is the highest achievement.",
        teaching:
          "The Yoruba saying goes: 'Ìwà l'ẹwà' — character is beauty. Not physical appearance, not wealth, not status, but how you carry yourself, how you treat others, how you hold integrity when no one is watching. Good character (ìwà rere) is the mark of a human being fully realized; bad character (ìwà burúkú) is the root of suffering and social disorder. This is not moralism but a practical claim: your character shapes your destiny (àyànmọ́) more than external circumstances. The proverbs teach this from every angle — 'A child who washes their hands eats with elders,' meaning respect and discipline open doors; 'The patient person eats ripe fruit,' meaning character includes the capacity to wait. Ìwà is not inherited; it is cultivated through practice, correction, and modeling. The path begins here because without character, all other wisdom is hollow.",
        keyIdea: "Ìwà (good character) is the foundation of wisdom, beauty, and a well-lived life — it shapes destiny more than circumstance.",
        misconception:
          "That character is innate or fixed. Yoruba teaching insists it is cultivated through deliberate practice and community modeling.",
        passageId: "yoruba_proverbs.yp_001",
        supportingPassageIds: ["yoruba_proverbs.yp_002"],
        theme: "character",
        chatMode: "question",
        chatPrompt:
          "Help me understand ìwà (character) as the Yoruba see it — not as morality imposed from outside, but as the art of becoming fully human.",
        practice:
          "Name one situation where your character was tested this week — a moment of impatience, dishonesty, or self-centeredness. Ask: 'What would good character (ìwà rere) have done?' Let that guide tomorrow.",
        journalPrompt:
          "What does 'character is beauty' mean in my life? Where have I prioritized appearance or achievement over the quality of how I show up?",
        integration:
          "You can recognize character as something you build through daily choices, not as a fixed trait, and see it as the foundation of a good life.",
      },
      {
        id: "yor-patience",
        title: "Sùúrù — The Patient Person Eats Ripe Fruit",
        orientation:
          "Gate II · The Discipline. Yoruba wisdom insists: patience (sùúrù) is not passive waiting but active endurance toward the right timing.",
        teaching:
          "The proverb says: 'Sùúrù l'ábà ọ̀tọ́' — patience is the father of good character. Patience (sùúrù) is not resignation or doing nothing; it is the discipline of waiting for the right time, refusing to act impulsively, and trusting the natural rhythm of things. The person who grabs green fruit because they cannot wait will eat bitterness; the patient person waits and eats sweetness. This applies to every domain: relationships (you cannot force intimacy), work (real mastery takes time), conflict (reacting in anger rarely resolves the issue). Patience is paired with preparation — you wait, yes, but you also ready yourself so that when the moment comes, you can act well. The teaching is both practical and philosophical: time has its own wisdom, and forcing results out of season creates distortion.",
        keyIdea: "Patience (sùúrù) is not passivity; it is the discipline of right timing, waiting for fruit to ripen before you pick it.",
        misconception:
          "That patience is weakness or doing nothing. Yoruba sùúrù is active endurance and preparation, respecting natural rhythms.",
        passageId: "yoruba_proverbs.yp_003",
        supportingPassageIds: ["yoruba_proverbs.yp_004"],
        theme: "patience",
        chatMode: "practice",
        chatPrompt:
          "Give me a practice for cultivating sùúrù (patience) as active discipline rather than passive waiting. How do I wait well?",
        practice:
          "Identify one thing you are impatient about — a goal, a relationship, a change. Ask: 'Is this fruit ripe, or am I grabbing it green?' If it is green, practice sùúrù: wait, prepare, and trust the timing.",
        journalPrompt:
          "Where in my life have I grabbed green fruit out of impatience, and what was the cost? Where do I need to practice sùúrù now?",
        integration:
          "You can recognize when you are forcing timing out of impatience and choose sùúrù — waiting for ripeness while preparing to act.",
      },
      {
        id: "yor-community",
        title: "Community Over Individualism — No One Is an Island",
        orientation:
          "Gate III · The Web. Yoruba philosophy is relational: the self is not an isolated atom but a node in a web of relationships.",
        teaching:
          "The proverb teaches: 'A single hand cannot tie a bundle.' No person, no matter how capable, can live a full life alone. The Yoruba worldview is fundamentally communal (ìjọba) — you exist because of and through others: ancestors, elders, peers, children, the yet-unborn. This is not collectivism that erases the individual; it is recognition that selfhood is relational. You are who you are because of those who raised you, taught you, challenged you, loved you. Reciprocity (ọ̀rẹ́) is the glue: you give because you have received; you will need help one day, as others need it now. Western individualism — the self-made person, the isolated hero — is seen as a kind of delusion. The wise person knows: their flourishing depends on the health of the whole, so they invest in relationship, not only in personal achievement.",
        keyIdea: "The self is relational, not isolated — community (ìjọba) and reciprocity (ọ̀rẹ́) are the ground of a good life.",
        misconception:
          "That community means losing individuality. Yoruba philosophy recognizes persons as unique, but always within a web of relation.",
        passageId: "yoruba_proverbs.yp_005",
        supportingPassageIds: ["yoruba_proverbs.yp_006"],
        theme: "community",
        chatMode: "compare",
        chatPrompt:
          "Compare Yoruba communal philosophy with Western individualism. How is the Yoruba self relational without erasing the person?",
        practice:
          "Name three people who made you who you are — who taught, challenged, or loved you into your current form. Reach out to one and express gratitude. Feel how you are not self-made.",
        journalPrompt:
          "Where do I act as if I am self-sufficient, and where does that create isolation or brittleness? How does recognizing my relational nature change things?",
        integration:
          "You can see yourself as relational rather than isolated, and invest in community as the ground of your own flourishing.",
      },
      {
        id: "yor-elders",
        title: "Respect for Elders and Ancestors — The Living and the Dead",
        orientation:
          "Gate III · The Chain. Yoruba wisdom insists: the living and the dead are one community; elders hold the accumulated wisdom.",
        teaching:
          "The proverb says: 'An elder in the house is a treasure.' Elders are not revered out of sentimentality but because they carry the distilled wisdom of experience. They have walked the path, made the mistakes, survived the crises; their counsel is tested. Disrespecting an elder is not just rudeness; it is rejecting access to wisdom. And beyond the living elders are the ancestors (egúngún) — those who came before, whose lives and sacrifices made yours possible. The ancestors are not absent; they are present, watchable, invokable. You honor them not as dead gods but as the living-dead, the elders of elders, still involved in the affairs of the family and community. This teaching breaks the modern illusion of the self-starting individual: you did not appear from nowhere. You are a link in a long chain, carrying forward what was given, responsible for passing it on.",
        keyIdea: "Elders and ancestors are living sources of wisdom; the community includes the dead, and respect flows backward and forward.",
        misconception:
          "That ancestor reverence is superstition. In Yoruba philosophy, it is recognition of continuity and debt across generations.",
        passageId: "yoruba_proverbs.yp_007",
        supportingPassageIds: ["yoruba_proverbs.yp_008"],
        theme: "ancestors",
        chatMode: "explain",
        chatPrompt:
          "Explain Yoruba ancestor reverence as philosophy rather than superstition. How does honoring the dead shape the living?",
        practice:
          "Name one ancestor — a grandparent, great-grandparent, someone whose life made yours possible. Speak their name aloud. Ask: 'What did you carry that I now carry? What am I responsible for passing on?'",
        journalPrompt:
          "What have I inherited — values, struggles, gifts — from those who came before me, and how does recognizing that change my sense of responsibility?",
        integration:
          "You can see yourself as part of a multi-generational chain, carrying forward what was given and responsible for what you pass on.",
      },
      {
        id: "yor-balance",
        title: "Balance and Moderation — The Middle Path",
        orientation:
          "Gate IV · The Way. Yoruba wisdom teaches balance (ìwọ̀ntúnwọ̀nsì): extremes distort; the middle way sustains.",
        teaching:
          "The proverb warns: 'Too much of anything is bad.' Yoruba philosophy is suspicious of extremes — too much wealth breeds arrogance, too much humility breeds exploitation, too much talking drowns wisdom, too much silence breeds misunderstanding. The ideal is balance (ìwọ̀ntúnwọ̀nsì): not lukewarm compromise but dynamic equilibrium, knowing when to speak and when to listen, when to give and when to hold, when to act and when to wait. This is not a rule but an art, requiring discernment (ọgbọ́n). The wise person reads the situation and calibrates their response — firm but not rigid, generous but not reckless, principled but not fanatical. Balance is the long-term strategy: extremes burn out, moderation endures. It is the ethical counterpart to sùúrù (patience) — both insist that force and rush distort what they touch.",
        keyIdea: "Balance (ìwọ̀ntúnwọ̀nsì) is the art of avoiding extremes — not compromise, but dynamic equilibrium in response to the situation.",
        misconception:
          "That balance means being lukewarm or never taking a stand. It is calibrated response, knowing when to be firm and when to yield.",
        passageId: "yoruba_proverbs.yp_009",
        supportingPassageIds: ["yoruba_proverbs.yp_010"],
        theme: "balance",
        chatMode: "practice",
        chatPrompt:
          "Help me practice ìwọ̀ntúnwọ̀nsì (balance) as an art of discernment. How do I know when I am tipping into an extreme?",
        practice:
          "Name one area where you tend toward excess — talking, working, giving, withdrawing. This week, practice the opposite without swinging to the other extreme. Feel for the middle.",
        journalPrompt:
          "Where am I currently out of balance, and what would a Yoruba elder advise? How do I find the middle way between extremes?",
        integration:
          "You can recognize your own extremes and practice balance as an art of reading the situation and calibrating your response.",
      },
    ],
  },
  {
    id: "native-american-wisdom",
    title: "Native American Wisdom",
    level: "Beginner",
    focus: "Living in relationship with all beings — the circle, the sacred, the land",
    outcome:
      "Learn the Native American worldview: everything is related, the Earth is sacred, and wisdom comes from walking in balance with all our relations.",
    description:
      "A path through Native teachings: the Sacred Hoop, respect for Earth and ancestors, and the vision of all beings as relatives.",
    arc:
      "Native American philosophy (drawing here from Lakota/Dakota traditions via Charles Eastman's 'The Soul of the Indian' and Zitkala-Ša's 'Old Indian Legends') sees the world as a web of relationships, not a collection of objects. All beings — human, animal, plant, stone, wind — are relatives, participants in one sacred circle. The Great Mystery (Wakan Tanka) is not a distant deity but the living presence in all things. Wisdom comes not from books but from listening: to elders, to dreams, to the land itself. The path teaches respect (for Earth, for ancestors, for all life), balance (walking in right relation), humility (humans are not above nature but within it), and gratitude (every gift requires acknowledgment). The vision is ecological and spiritual at once: care for the land is not separate from care for the soul, because the land and the soul are woven together. This is philosophy as a way of living, not only as a way of thinking.",
    estimatedSessions: "5 gates · ~20 min each",
    steps: [
      {
        id: "na-all-related",
        title: "Mitakuye Oyasin — All My Relations",
        orientation:
          "Gate I · The Circle. The foundational teaching: all beings are relatives; separation is illusion.",
        teaching:
          "The Lakota phrase 'Mitakuye Oyasin' — all my relations — is both greeting and worldview. It names the truth that every being is kin: the two-legged (humans), the four-legged (animals), the winged, the swimmers, the plant nations, the stone people, the ancestors, the yet-unborn. This is not metaphor or sentiment; it is ontology. You do not stand outside nature looking at it; you are a strand in the web. What you do to the web, you do to yourself. Harming the land, the water, the animals is harming relatives, and it will return as harm to you and your children. Honoring them is honoring the whole, which includes you. This teaching breaks the modern illusion of human exceptionalism: we are not above creation, managing it; we are within it, one voice in the chorus. The circle (the Sacred Hoop) is the shape of this truth: no hierarchy, no beginning or end, everyone facing the center, which is the Great Mystery.",
        keyIdea: "Mitakuye Oyasin: all beings are relatives; the world is a web of kinship, not a collection of resources.",
        misconception:
          "That this is poetic language for environmentalism. It is literal kinship — ontological, not metaphorical.",
        passageId: "soul_of_the_indian.soti_001",
        supportingPassageIds: ["soul_of_the_indian.soti_002"],
        theme: "relations",
        chatMode: "compare",
        chatPrompt:
          "Compare Mitakuye Oyasin (all my relations) with Buddhist interdependence and Yoruba communal philosophy. How is kinship with all beings different from abstract interconnection?",
        practice:
          "Go outside. Name three beings you encounter — a tree, a bird, a stone. Say silently: 'My relative.' Feel what shifts when you meet them as kin rather than as scenery or objects.",
        journalPrompt:
          "If all beings are my relatives, how does that change my relationship with the land, with animals, with what I consume?",
        integration:
          "You can see all beings as relatives rather than as resources, and recognize your actions as happening within a web of kinship.",
      },
      {
        id: "na-great-mystery",
        title: "Wakan Tanka — The Great Mystery",
        orientation:
          "Gate II · The Sacred. The divine is not a distant lord but the living mystery present in all things.",
        teaching:
          "Wakan Tanka (Lakota for the Great Mystery or Great Spirit) is not a person in the sky judging and commanding. It is the sacred power that animates everything — the wind, the buffalo, the thunder, the silence. Wakan means sacred, mysterious, incomprehensible; Tanka means great. Together: the great sacred mystery that cannot be grasped by thought but can be met in reverence. The teaching insists: the sacred is not confined to church or temple; it is everywhere. A stone, rightly seen, is wakan. A mountain is a grandmother. The four directions, the seasons, the life-and-death cycle — all are expressions of Wakan Tanka. Prayer is not petition but attunement: you listen, you offer tobacco, you participate in the sacred rhythm. This is closer to pantheism or panentheism than to theism, but even those labels miss the point — the Mystery refuses categories.",
        keyIdea: "Wakan Tanka: the Great Mystery is not a distant deity but the sacred presence in all beings and all moments.",
        misconception:
          "That Wakan Tanka is like the Abrahamic God. It is impersonal-personal, immanent, the sacred fabric of reality itself.",
        passageId: "soul_of_the_indian.soti_003",
        supportingPassageIds: ["soul_of_the_indian.soti_004"],
        theme: "sacred",
        chatMode: "explain",
        chatPrompt:
          "Explain Wakan Tanka as the Great Mystery — not a being among beings, but the sacred power present in all things.",
        practice:
          "Sit outside in silence. Do not pray words. Listen. Feel the wind, the temperature, the sounds. Ask: 'What is the Mystery speaking here?' Let it remain mystery; do not answer.",
        journalPrompt:
          "Where have I encountered the sacred outside of religious buildings — in nature, in silence, in a moment that stopped me?",
        integration:
          "You can recognize the sacred as present in ordinary things and moments, not confined to designated holy spaces.",
      },
      {
        id: "na-earth-mother",
        title: "Earth as Mother — Not Resource, but Relative",
        orientation:
          "Gate III · The Land. The Earth is not property to own or exploit; she is mother, ancestor, and teacher.",
        teaching:
          "Native philosophy does not speak of 'the environment' as if it were a backdrop to human action. The Earth is Unci Maka (Grandmother Earth) — she gives life, provides food, shelters all beings. You do not own land; you belong to it. The idea of buying and selling Earth is as absurd and obscene as selling your mother. This teaching collides directly with modern economics and law, which treat land as commodity. But the Native view is not naive romanticism; it is pragmatic wisdom. When you treat Earth as relative, you take only what you need, you give thanks, you ensure there is enough for the next seven generations. When you treat Earth as resource, you extract until it is exhausted, and your children inherit wasteland. The land teaches if you listen: the cycles of seasons, the patience of trees, the generosity of water. Wisdom is not only in human elders; it is in the land itself.",
        keyIdea: "Earth is Grandmother, not resource — a relative who gives life, deserving respect, gratitude, and reciprocity.",
        misconception:
          "That this is sentimentalism. It is a radically different ontology and ethic, tested by millennia of sustainable living.",
        passageId: "soul_of_the_indian.soti_005",
        supportingPassageIds: ["old_indian_legends.oil_001"],
        theme: "earth",
        chatMode: "question",
        chatPrompt:
          "Help me understand Earth as Mother/Grandmother — not as metaphor, but as a shift in ontology and ethics. What follows from that?",
        practice:
          "Before eating, touch the food and silently acknowledge: 'This came from Earth. Thank you, Grandmother.' Feel the chain: soil, rain, sun, hands. Let gratitude be real, not rote.",
        journalPrompt:
          "How does my current relationship with land and food reflect the idea of Earth as resource versus Earth as relative? What would shift?",
        integration:
          "You can meet Earth as relative deserving gratitude and reciprocity, not as backdrop or commodity.",
      },
      {
        id: "na-vision",
        title: "Vision and Listening — Wisdom Beyond Words",
        orientation:
          "Gate III · The Knowing. Knowledge comes not only from speaking but from silence, dreams, and deep listening.",
        teaching:
          "In Native tradition, wisdom arrives through vision (dreams, fasting, ceremony) as much as through teaching. A young person might go on a vision quest (hanbleceya) — fasting alone on a hill, waiting for the Great Mystery to speak through dream, animal encounter, or inner knowing. This is not escapism; it is a discipline of listening beneath the noise of ordinary life. Elders do not lecture; they tell stories, and the teaching is woven into the story for those who can hear it. Truth is not only propositional ('X is Y'); it is participatory. You learn by doing, by sitting with elders, by watching how the hunter moves or how the grandmother prepares the food. The teaching is embodied, relational, contextual. Words matter, but silence matters more. The modern obsession with documentation and explanation is seen as a kind of deafness — talking so much you cannot hear.",
        keyIdea: "Wisdom comes through vision, silence, and listening — not only through words and analysis.",
        misconception:
          "That vision quests are superstition. They are a method of accessing knowing beyond the discursive mind.",
        passageId: "soul_of_the_indian.soti_006",
        supportingPassageIds: ["old_indian_legends.oil_002"],
        theme: "vision",
        chatMode: "practice",
        chatPrompt:
          "How do I practice listening for wisdom beyond words — in silence, in dreams, in what is not said?",
        practice:
          "Spend ten minutes in silence, outside if possible. Do not meditate toward a goal. Just listen — to wind, to birds, to the space between sounds. If an image or knowing arises, receive it without analysis.",
        journalPrompt:
          "What have I learned recently not through words but through silence, dream, or deep listening? How do I make space for that kind of knowing?",
        integration:
          "You can value and cultivate non-verbal knowing — vision, silence, embodied wisdom — as legitimate and necessary.",
      },
      {
        id: "na-seven-generations",
        title: "Think Seven Generations Ahead",
        orientation:
          "Gate IV · The Responsibility. Every decision is made with the unborn in mind; the long view is not optional.",
        teaching:
          "The Haudenosaunee (Iroquois) teaching: when making a decision, consider its impact on the seventh generation yet to come. Not the next quarter, not the next election cycle — seven generations, roughly 140 years. This is not a suggestion; it is the baseline of responsible action. If a choice benefits you now but harms your great-great-great-great-great-grandchildren, it is a bad choice. This teaching assumes continuity and care across time. You are not the end; you are a link in a chain. The ancestors made sacrifices so you could be here; you owe the same to those coming. This is the opposite of short-term thinking that dominates modern economics and politics. It is also deeply pragmatic: the land and water do not reset every generation. Deplete them now, and seven generations will suffer. The teaching asks: can you hold the unborn in your heart as real as the living? If so, your decisions change.",
        keyIdea: "Seven generations: every decision must consider its impact on the unborn, 140 years ahead.",
        misconception:
          "That this is impractical idealism. It is tested pragmatism — the condition of long-term survival and flourishing.",
        passageId: "soul_of_the_indian.soti_007",
        supportingPassageIds: ["soul_of_the_indian.soti_008"],
        theme: "responsibility",
        chatMode: "practice",
        chatPrompt:
          "Help me practice 'seven generations' thinking: how do I hold the unborn as real as the living when I make decisions?",
        practice:
          "Name one decision you face. Ask: 'What will this mean for my great-great-great-great-great-grandchildren?' Let the long view test whether the choice is wise.",
        journalPrompt:
          "Where am I prioritizing short-term gain over long-term health — in my own life, in my community, in how I vote or spend?",
        integration:
          "You can hold the seventh generation as real and let the long view guide decisions, refusing the tyranny of the short term.",
      },
    ],
  },
  {
    id: "greek-presocratic-to-plotinus",
    title: "Greek Philosophy — From Fire to the One",
    level: "Advanced",
    focus: "Heraclitus, Parmenides, Plato, Plotinus — the Greek arc from flux to form to the One",
    outcome:
      "Walk the Greek philosophical tradition from Presocratic beginnings through Plato's forms to Plotinus' vision of the One and the soul's return.",
    description:
      "A pure Greek path: Heraclitus' flux, Parmenides' unchanging Being, Plato's ascent through Beauty, and Plotinus' emanation and return.",
    arc:
      "Greek philosophy begins with astonishment at change. Heraclitus sees everything flowing like a river — no thing is, all things become. Parmenides argues the opposite: true Being never changes; flux is illusion. Plato synthesizes: the visible world flows (Heraclitus was right about appearances), but eternal Forms exist beyond flux (Parmenides was right about Being). The soul climbs from particular beauties to Beauty itself through eros. Then Plotinus completes the arc: the One is beyond even Being, the source from which Intellect and Soul emanate. The soul's task is the return — from multiplicity and forgetfulness back to the One, through Beauty and contemplation. This is not comparative philosophy; it is the Greek lineage in its own voice, showing how the question 'What is real?' unfolded across centuries into a full metaphysics of ascent and return.",
    estimatedSessions: "6 gates · ~25 min each",
    steps: [
      {
        id: "greek-heraclitus-flux",
        title: "Heraclitus — Everything Flows",
        orientation:
          "Gate I · The Beginning. Greek philosophy opens with the shock of impermanence: nothing stays, all things flow.",
        teaching:
          "Heraclitus of Ephesus (c. 535–475 BCE) sees flux everywhere: 'You cannot step into the same river twice, for new waters are ever flowing upon you.' The river looks the same, but it is always different water. So with everything: the body, the city, the self. All things are in constant becoming. Fire is his image for reality — consuming, transforming, never still. But this is not chaos; there is logos, a hidden order or proportion governing the flux. Opposites are unified in tension: 'The way up and the way down are the same'; 'Cold things become warm, warm becomes cold.' Heraclitus names the human condition: we live in time, in change, and we forget. We treat what flows as if it were solid. The beginning of wisdom is waking up to the flux and learning to move with it rather than clinging to what cannot stay.",
        keyIdea: "Panta rhei: everything flows; reality is becoming, not static being — the river never stays the same.",
        misconception:
          "That flux means nihilism or randomness. Heraclitus sees order (logos) within the flow, a hidden harmony of opposites.",
        passageId: "heraclitus_fragments.her_frag_12",
        supportingPassageIds: ["heraclitus_fragments.her_frag_50", "heraclitus_fragments.her_frag_51"],
        theme: "flux",
        chatMode: "explain",
        chatPrompt:
          "Explain Heraclitus' teaching that 'everything flows' as both a metaphysical claim and a practical wisdom for living in time.",
        practice:
          "Observe one 'solid' thing in your life — a relationship, a role, a belief. Look closely: is it really the same as it was a year ago? Feel the flux underneath the appearance of stability.",
        journalPrompt:
          "Where am I clinging to what is changing, treating the river as if it could stand still? What would it mean to move with the flux?",
        integration:
          "You can recognize flux as the nature of reality and see clinging to permanence as the source of suffering.",
      },
      {
        id: "greek-parmenides-being",
        title: "Parmenides — Being Is, Non-Being Is Not",
        orientation:
          "Gate II · The Counter-Claim. Parmenides challenges Heraclitus: true reality does not change; what changes is not truly real.",
        teaching:
          "Parmenides of Elea (c. 515 BCE) argues: Being is; non-being is not — and that is the end of the matter. What truly is cannot come to be (for it would have to come from non-being, which is impossible) and cannot cease to be (for it would pass into non-being, which does not exist). Therefore, Being is eternal, unchanging, indivisible, and whole. The flux Heraclitus saw is not ultimate reality; it is appearance, the 'way of opinion' (doxa). True reality — the 'way of truth' (aletheia) — is timeless. This is the birth of metaphysics as a discipline: the visible world and the real world are not the same. Change, multiplicity, and becoming belong to the realm of appearance; true Being is One and unchanging. Plato will later synthesize Heraclitus and Parmenides — the Forms are unchanging Being, while the sensible world is flux.",
        keyIdea: "Being is unchanging and eternal; what changes belongs to appearance, not to ultimate reality.",
        misconception:
          "That Parmenides denies the visible world. He distinguishes appearance (which exists) from ultimate reality (which does not change).",
        passageId: "parmenides_fragments.par_frag_02",
        supportingPassageIds: ["parmenides_fragments.par_frag_08"],
        theme: "being",
        chatMode: "compare",
        chatPrompt:
          "Compare Heraclitus' flux with Parmenides' unchanging Being. How does Plato later synthesize these two positions?",
        practice:
          "Contemplate one thing you consider unchanging — a mathematical truth, a moral principle, an ideal. Ask: does this belong to the world of flux or to Parmenides' realm of Being?",
        journalPrompt:
          "What in my experience points toward something that does not change — an awareness, a truth, a presence — underneath the flux?",
        integration:
          "You can distinguish appearance (which changes) from Being (which does not) and recognize both as real in different senses.",
      },
      {
        id: "greek-plato-forms",
        title: "Plato — The Forms as True Reality",
        orientation:
          "Gate III · The Synthesis. Plato unites Heraclitus and Parmenides: the visible flows, the Forms are eternal.",
        teaching:
          "Plato inherits both Heraclitus' flux and Parmenides' Being and declares both true — but of different realms. The visible world (the realm of becoming) is always flowing: particular beautiful things come and go, just horses are born and die. But the Forms — Beauty itself, Justice itself, the Horse itself — are eternal, unchanging, and perfect. The particulars 'participate' in the Forms: this horse is a horse because it participates in Horseness; this act is just because it participates in Justice. The Forms are not physical or mental; they are a third kind of being, accessible to the intellect (nous) but not to the senses. The soul knew the Forms before birth and forgot them; learning is recollection (anamnesis). This is the foundation of Platonism: ultimate reality is not material but intelligible, not flux but eternal structure. The task is to turn the soul from shadows (appearances) to the light (Forms).",
        keyIdea: "The Forms are eternal, perfect archetypes; the visible world participates in them but is not ultimately real.",
        misconception:
          "That the Forms are 'just ideas in the mind.' Plato insists they are objective realities, more real than physical things.",
        passageId: "phaedo_plato.phaedo_md_002",
        supportingPassageIds: ["phaedo_plato.phaedo_md_004"],
        theme: "forms",
        chatMode: "explain",
        chatPrompt:
          "Explain Plato's Forms as a solution to the Heraclitus/Parmenides problem: how the world can both flow and have stable reality.",
        practice:
          "Look at something beautiful — a face, a tree, a piece of music. Ask: what makes it beautiful? Try to point at Beauty itself, not this or that beautiful thing. Feel the Form as distinct from its instances.",
        journalPrompt:
          "Do I believe there is such a thing as Beauty itself, Justice itself — or only beautiful things and just acts? What follows from each view?",
        integration:
          "You can distinguish the Form from its instances and recognize the intelligible realm as prior to the visible.",
      },
      {
        id: "greek-plato-ascent",
        title: "The Ascent Through Beauty — Eros as the Path",
        orientation:
          "Gate III · The Method. Plato names the soul's ascent: from particular beauties to Beauty itself, driven by eros.",
        teaching:
          "In the Symposium, Plato describes the ladder of love (eros): you begin attracted to one beautiful body, then recognize beauty in many bodies, then in beautiful souls, then in beautiful laws and institutions, then in beautiful knowledge, and finally — if you ascend all the way — you behold Beauty itself, eternal and perfect. Eros is not base desire to be transcended; it is the soul's longing for the eternal, misdirected toward particulars. Every time you love a beautiful thing, you are really longing for Beauty; you just mistake the reflection for the original. The ascent is not rejection of the body or the world; it is progressive refinement of what you love, climbing from image to archetype. And the vision of Beauty is not information; it is transformative — the soul becomes beautiful by beholding Beauty. This is mysticism grounded in eros, the philosophical counterpart to later Sufi and Christian bridal mysticism.",
        keyIdea: "Eros (love/desire) is the soul's longing for the eternal; the ascent through beauties leads to Beauty itself.",
        misconception:
          "That eros is bad or bodily desire to suppress. Plato sees it as the engine of the soul's ascent, misdirected until refined.",
        passageId: "phaedo_plato.phaedo_md_005",
        supportingPassageIds: ["plotinus_enneads.enn_i_6_09"],
        theme: "eros",
        chatMode: "practice",
        chatPrompt:
          "Turn Plato's ladder of love into a contemplative practice: how do I refine what I love, climbing from particular to universal?",
        practice:
          "Recall someone or something you find beautiful. Ask: 'What is the beauty I see here?' Then ask: 'Is there Beauty itself, beyond this instance?' Let eros move up the ladder.",
        journalPrompt:
          "Where is my desire aimed — at particulars that will fade, or at the eternal they point toward? How do I refine my loves?",
        integration:
          "You can recognize eros as longing for the eternal and practice refining your loves, climbing from image to archetype.",
      },
      {
        id: "greek-plotinus-one",
        title: "Plotinus — The One Beyond Being",
        orientation:
          "Gate IV · The Peak. Plotinus takes the Greek path to its zenith: the One is beyond even Being, the source of all.",
        teaching:
          "Plotinus (204–270 CE) completes Platonism by placing the One (to hen) beyond the Forms, beyond Being itself. The One is absolutely simple, without parts, without predicates — you cannot even say 'it is' because that would make it a being. From the One's perfection, Intellect (Nous) emanates, like light from the sun. Intellect contains the Forms and is the realm of true Being. From Intellect, Soul emanates, and from Soul, the material world. This is not creation in time; it is timeless overflow. The One does not diminish by giving rise to the many. And the soul's task is return (epistrophe): from distraction in matter, through self-knowledge in Soul, through contemplation of the Forms in Intellect, to mystical union with the One — 'the flight of the alone to the Alone.' Plotinus reports experiencing this union multiple times. It is not philosophy as argument but as ascent.",
        keyIdea: "The One is beyond Being, the source from which all emanates; the soul's path is return through contemplation to union.",
        misconception:
          "That the One is a person or God in the theistic sense. It is beyond personality, beyond language, the absolute transcendent source.",
        passageId: "plotinus_enneads.enn_v_1_06",
        supportingPassageIds: ["plotinus_enneads.enn_vi_9_11"],
        theme: "one",
        chatMode: "explain",
        chatPrompt:
          "Explain Plotinus' One as beyond Being itself, and the soul's return as the culmination of the Greek philosophical path.",
        practice:
          "Contemplate the source of all things: not a being, not even Being, but that from which being pours. Do not try to picture it. Let thought point and then release itself.",
        journalPrompt:
          "If the One is beyond even Being, what is the 'I' that seeks it — and what happens to that 'I' in union?",
        integration:
          "You can approach the One through apophatic contemplation, recognizing it as the source beyond all categories.",
      },
      {
        id: "greek-never-cease-chiselling",
        title: "Never Cease Chiselling Your Statue",
        orientation:
          "Gate IV · The Practice. Plotinus gives the instruction for the ascent: become beautiful, and you will see Beauty.",
        teaching:
          "Plotinus writes in the most beautiful passage of the Enneads: 'Withdraw into yourself and look. And if you do not yet see yourself beautiful, act as does the creator of a statue that is to be made beautiful: he cuts away here, he smooths there, he makes this line lighter, this other purer, until he has shown a beautiful face upon the statue. Do you also do this: cut away all that is excessive, straighten all that is crooked, bring light to all that is overcast, labour to make all one radiance of beauty, and never cease chiselling your statue until there shall shine out on you the godlike splendour of virtue... For never did eye see the sun unless it had first become sunlike; and never can the soul have vision of the First Beauty unless itself be beautiful.' The ascent is subtraction, not addition. You remove what is false until what remains is radiant. And you cannot see the One by looking at it as an object; you see it by becoming like it — vision by resemblance.",
        keyIdea: "Never cease chiselling: the ascent is removing what is false until you become sunlike and can see the sun.",
        misconception:
          "That you reach the One by acquiring more knowledge or virtue. You reach it by becoming beautiful through subtraction.",
        passageId: "plotinus_enneads.enn_i_6_09",
        supportingPassageIds: ["plotinus_enneads.enn_i_6_08"],
        theme: "ascent",
        chatMode: "practice",
        chatPrompt:
          "Turn Plotinus' statue metaphor into a spiritual practice: what in me is excessive, crooked, or overcast — and how do I chisel?",
        practice:
          "Name one thing that is 'excessive' in you — a compulsion, a defense, a false persona. For one day, chisel: set it down each time it arises. Notice what radiance is uncovered.",
        journalPrompt:
          "What would I look like if I never ceased chiselling — if I kept removing the false until only the godlike splendour remained?",
        integration:
          "You can practice the ascent as subtraction, chiselling away the false until the soul becomes sunlike and can see the sun.",
      },
    ],
  },
];

/** A realm is a grouping of paths by lineage/territory — the "courses" of the
 *  journey. trackIds also define the recommended order within the realm. */
export type LearningRealm = {
  id: string;
  title: string;
  /** One-line invitation shown under the realm heading. */
  blurb: string;
  trackIds: string[];
};

export const LEARNING_REALMS: LearningRealm[] = [
  {
    id: "foundations",
    title: "Foundations",
    blurb:
      "Where every path begins: steady the ground of attention, and learn to act without seizing up.",
    trackIds: ["action-without-contraction", "recognizing-awareness"],
  },
  {
    id: "trika",
    title: "The Trika · Kashmir Śaivism",
    blurb:
      "The path of recognition: you are the Consciousness you have been seeking — playing at being bound.",
    trackIds: [
      "heart-of-recognition",
      "three-doors-of-shiva",
      "the-112-doorways",
      "descent-of-the-cakra",
    ],
  },
  {
    id: "vedanta",
    title: "Vedānta & the Great Letting-Go",
    blurb:
      "The witness behind the three states, and the fearless release into emptiness.",
    trackIds: ["letting-go-death-emptiness"],
  },
  {
    id: "bridges",
    title: "Bridges Across Traditions",
    blurb:
      "One story of emanation and return, told by Plotinus, the Śaiva sages, and the Tao.",
    trackIds: ["the-one-and-the-many"],
  },
];

/** Recommended journey: beginner at the inner ring, deepening outward to the
 *  capstone. Used for mandala numbering, "Start here", and "Recommended next". */
export const RECOMMENDED_SPINE: string[] = [
  "action-without-contraction",
  "recognizing-awareness",
  "heart-of-recognition",
  "three-doors-of-shiva",
  "the-112-doorways",
  "descent-of-the-cakra",
  "letting-go-death-emptiness",
  "the-one-and-the-many",
];

/**
 * Philosophical Traditions — "Duolingo for each philosophical language."
 * Each tradition is a sequential trail teaching its vocabulary (key terms),
 * metaphors, images, and governing ideas through its source texts.
 */
import type { SumiSlug } from "./sumiGlyphs";

export type PhilosophicalTradition = {
  id: string;
  /** Display title (e.g. "Kashmir Śaivism") */
  title: string;
  /** One-line invitation shown on the tradition chooser */
  invitation: string;
  /** Sumi ink mark for the tradition card */
  glyph: SumiSlug;
  /** Tracks that belong to this tradition, in recommended order */
  trackIds: string[];
};

export const PHILOSOPHICAL_TRADITIONS: PhilosophicalTradition[] = [
  {
    id: "kashmir-shaivism",
    title: "Kashmir Śaivism",
    invitation: "Recognition: you are the Consciousness you have been seeking.",
    glyph: "shiva",
    trackIds: ["heart-of-recognition", "three-doors-of-shiva", "the-112-doorways", "descent-of-the-cakra"],
  },
  {
    id: "bhagavad-gita",
    title: "Bhagavad Gītā",
    invitation: "Act without seizing; serve without owning the fruit.",
    glyph: "vishnu",
    trackIds: ["action-without-contraction"],
  },
  {
    id: "vedanta",
    title: "Vedānta & Upaniṣads",
    invitation: "The witness behind waking, dream, and sleep — you are That.",
    glyph: "yantra",
    trackIds: ["recognizing-awareness"],
  },
  {
    id: "yoga",
    title: "Yoga (Patañjali)",
    invitation: "Stillness of the mind's turnings; the seer rests in its own nature.",
    glyph: "spiral",
    trackIds: ["yoga-eight-limbs"],
  },
  {
    id: "buddhism",
    title: "Buddhism",
    invitation: "Emptiness, compassion, the groundless ground.",
    glyph: "lotus",
    trackIds: ["buddhism-core"],
  },
  {
    id: "tao",
    title: "Tao",
    invitation: "The nameless source; the ten thousand things arise and return.",
    glyph: "dragon",
    trackIds: ["letting-go-death-emptiness"],
  },
  {
    id: "greek",
    title: "Greek Philosophy",
    invitation: "From flux to form to the One — Heraclitus, Plato, Plotinus.",
    glyph: "infinity",
    trackIds: ["greek-presocratic-to-plotinus"],
  },
  {
    id: "sufi",
    title: "Sufi",
    invitation: "The Beloved hides in plain sight; love is the way.",
    glyph: "spiral",
    trackIds: ["sufi-love-path"],
  },
  {
    id: "christian-mysticism",
    title: "Christian Mysticism",
    invitation: "The divine darkness; unknowing as the highest knowing.",
    glyph: "chalice",
    trackIds: ["christian-mysticism"],
  },
  {
    id: "yoruba",
    title: "Yoruba Wisdom",
    invitation: "Character is beauty; patience eats ripe fruit; all are kin.",
    glyph: "sun",
    trackIds: ["yoruba-wisdom"],
  },
  {
    id: "native-american",
    title: "Native American",
    invitation: "All my relations — Earth as Grandmother, the Sacred Hoop.",
    glyph: "eagle",
    trackIds: ["native-american-wisdom"],
  },
  {
    id: "bridges",
    title: "Bridges & Comparisons",
    invitation: "One story told in many voices — emanation and return across traditions.",
    glyph: "infinity",
    trackIds: ["the-one-and-the-many"],
  },
];

/** Traditions available in the corpus but awaiting first-pass tracks */
export const TRADITIONS_IN_DEVELOPMENT: Array<Omit<PhilosophicalTradition, "trackIds">> = [
  {
    id: "stoic",
    title: "Stoic Philosophy",
    invitation: "What is yours to govern; freedom through right judgment.",
    glyph: "sage",
  },
];
