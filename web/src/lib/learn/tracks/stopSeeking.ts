import type { LearningTrack } from "../../learningPaths";

/** Aṣṭāvakra sudden teaching — stop the seeker. Not a second recognition path. */
export const STOP_SEEKING: LearningTrack = {
  id: "stop-seeking",
  title: "Stop Seeking",
  level: "Intermediate",
  focus: "Aṣṭāvakra: already free; peace without effort; bondage is the mind's movement; drop the student-slot",
  outcome:
    "Admit which of Janaka's three questions you are still living; rest now once without a later date; let being and non-being arise without hiring yourself as engineer; name one movement of bondage as citta; stop one run that was begging the waves; drop the student-slot for a day without hunting a replacement.",
  description:
    "A six-gate sudden teaching after You Are That. Not the two-birds witness bead. Not PHR, Śiva Sūtra, or VBT restated.",
  arc:
    "You-are-that already walked fullness, tat tvam asi, and the Fourth. Recognition already used Aṣṭāvakra 1.7 as a witness bead — we do not reuse it. This walk is the seeker's career meeting a teaching that refuses the career. Janaka asks how knowledge, liberation, and dispassion are obtained. Rest in consciousness even now. Peace comes without manufacturing it against arising and passing. Bondage is the mind wanting, grieving, grasping. The universe shines as waves — why run like a beggar? Last: where is teacher, scripture, aim? You do not finish the Gītā. You drop the slot of being its student. If you use the last verse to quit learning while still hunting a state, you failed the gate.",
  estimatedSessions: "6 gates · ~20 min each",
  steps: [
    {
      id: "asg-questions",
      title: "How is knowledge attained?",
      orientation:
        "If we skip Janaka's questions, later 'already free' becomes a slogan the seeker wears. Begin as a seeker who wants a method.",
      teaching:
        "How is knowledge attained? How does liberation come about? How is dispassion obtained? Tell me this, my Lord. The path begins in honesty: three hungers, a request for a method. The difficulty: you skip this and quote non-dual slogans while still organizing a search — a career of seeking dressed as already knowing. Name the hunger. Circle the question you are actually living. Do not google a fourth. Sit with it unsolved.",
      keyIdea: "The walk begins as a seeker. Do not dress as one who already knows.",
      misconception:
        "That non-dual study means you are past Janaka's questions, or that adding a fourth question is the path.",
      passageId: "astavakra_gita.asg_1_1",
      supportingPassageIds: ["chāndogya_upaniṣad.chu_06_08_07"],
      theme: "self-inquiry",
      chatMode: "compare",
      chatPrompt:
        "Help me admit which of the three questions I am still living. How is this different from already hearing tat tvam asi — and where am I dressing as one who knows?",
      practice:
        "Write Janaka's three questions. Circle the one you are actually living. For today, stop googling a fourth. Sit with the circled question unsolved for five minutes.",
      journalPrompt:
        "Which of the three questions am I still using as a career?",
      integration:
        "You can admit you are still a seeker of one of the three, without dressing as one who already knows.",
    },
    {
      id: "asg-already",
      title: "Already, if you rest",
      orientation:
        "The questions want a later method. Aṣṭāvakra answers with adhunā eva — even now. Not the two-birds bead.",
      teaching:
        "If you separate the body and rest in consciousness, you will be happy, peaceful, free from bondage even now. The witness bead already exists — we do not restate the two birds. The shock here is the tense: already, now, not after a career of improving the body-story. The difficulty: you schedule liberation after more work, or you turn rest into another project for later. When a body-story starts a plan, rest sixty seconds as the one who knows the story. Do not improve the story. Stand up and continue.",
      keyIdea: "Rest now. Freedom is not a later date on the body-story.",
      misconception:
        "That liberation is scheduled after more work on the body, or that this is the same move as the two-birds witness practice.",
      passageId: "astavakra_gita.asg_1_4",
      supportingPassageIds: ["svetasvatara_upanishad.svu_011"],
      theme: "freedom",
      chatMode: "compare",
      chatPrompt:
        "Help me rest now without turning it into the two-birds career. Where am I still scheduling freedom after more work on the body-story?",
      practice:
        "Once today, when a body-story starts a plan (fix, improve, wait until), rest sixty seconds as the one who knows the story. Do not improve the story. Stand up and continue.",
      journalPrompt:
        "Where am I still scheduling liberation after more work on the body-story?",
      integration:
        "You can rest now once, without adding a later date for freedom.",
    },
    {
      id: "asg-peace",
      title: "Peace without effort",
      orientation:
        "'Already' without this becomes laziness. Peace is not produced by managing being and non-being.",
      teaching:
        "One who knows with certainty that the changes of being and non-being arise by nature becomes changeless, free of affliction, and effortlessly comes to peace. Not fatalism. Not a blank. The weather of arising and passing belongs to svabhāva — their own contingent nature — not to a deficiency in you that you must campaign against. The difficulty: you hire yourself as engineer of the weather and call the campaign the path. Let one arising and one passing be 'by nature' for ten minutes. Do the next duty without using the management as identity.",
      keyIdea: "Peace is not manufactured by managing arising and passing. They arise by nature.",
      misconception:
        "That effortless peace is laziness, or fatalism, or a campaign to suppress change.",
      passageId: "astavakra_gita.ag_01_11",
      theme: "freedom",
      chatMode: "explain",
      chatPrompt:
        "Help me let being and non-being arise without hiring myself as their engineer. Where am I still manufacturing peace?",
      practice:
        "Name one arising and one passing you have been managing. Let both be 'by nature' for ten minutes. Do the next duty without using the management as identity.",
      journalPrompt:
        "Where am I still trying to manufacture peace by managing being and non-being?",
      integration:
        "You can let one pair of being/non-being arise without hiring yourself as their engineer.",
    },
    {
      id: "asg-bondage",
      title: "The movements of bondage",
      orientation:
        "Effortless peace still fails if bondage is a metaphysics. Aṣṭāvakra locates it in this hour's citta.",
      teaching:
        "Bondage is then, when the mind desires something, grieves; abandons, grasps; is elated, is angry. Not a cosmic prison. Not ignorance as a system you must first understand. The knot is this hour's wanting. The difficulty: you look for a better theory of māyā while the movement is already running. Catch one of the six. Name it as citta, not as the world. Wait until the movement is seen before you act from it. You do not need a new metaphysics if you can catch the movement.",
      keyIdea: "Bondage is the mind's movement this hour — not a cosmic trap you must first theorize.",
      misconception:
        "That bondage is a metaphysical knot elsewhere, or that naming the six is already freedom without catching one.",
      passageId: "astavakra_gita.ag_08_01",
      theme: "self",
      chatMode: "practice",
      chatPrompt:
        "Help me catch one movement as citta, not as the world. Which of the six am I still calling me?",
      practice:
        "Catch one of the six: want, grief, drop, grab, elation, anger. Name it as citta, not as the world. Wait until the movement is seen before you act from it.",
      journalPrompt:
        "Which movement am I still calling 'me' — wanting, grieving, grasping, rejecting?",
      integration:
        "You can name one movement of bondage as the mind's, not as the structure of reality.",
    },
    {
      id: "asg-ocean",
      title: "Why do you run like a beggar?",
      orientation:
        "If the ocean is an image, you keep running. Distinct from recognition-as-flash and from the two birds.",
      teaching:
        "The universe shines forth like waves in the sea. Knowing 'I am that,' why do you run as if poor? The move is: stop the run. Poverty is the seeker's gait, not a fact about awareness. The difficulty: you admire the ocean while booking the next retreat — recognition as tourism. This is not PHR's fire, not VBT's doorway, not the watching bird. Cancel one seeking-move that was going to complete you. Stand still as the water. Then do an ordinary duty.",
      keyIdea: "Stop running toward the waves as if you were not the water.",
      misconception:
        "That the ocean is an image to admire, or that this restates recognition, the two birds, or a VBT doorway.",
      passageId: "astavakra_gita.ag_15_07",
      supportingPassageIds: ["pratyabhijnahrdayam.phr_014"],
      theme: "recognition",
      chatMode: "compare",
      chatPrompt:
        "Help me stop one run without restating PHR's fire. Where am I still begging the waves to make me the sea?",
      practice:
        "Cancel or postpone one seeking-move today (a tab, a purchase, a spiritual errand) that was going to complete you. Stand still one minute as the water, then do an ordinary duty.",
      journalPrompt:
        "Where am I still running toward a wave as if I were not the water?",
      integration:
        "You can stop one run that was begging the waves to make you the sea.",
    },
    {
      id: "asg-beyond",
      title: "Beyond teacher and teaching",
      orientation:
        "Last gate: the seeker-position dissolves. If you use this to quit learning while hunting a state, you failed.",
      teaching:
        "For me — the auspicious one, free of limiting adjuncts — where are instruction, scripture, disciple, or teacher? Where, indeed, is any human aim? This is not contempt for study. It is the closer: the student-slot was the last costume of seeking. You do not finish the Aṣṭāvakra Gītā. You drop the career of being its student. The difficulty: changing brands — a new guru, a new aim — while quoting this verse. Close the book. Keep one ordinary kindness. If the slot itches, notice it as a slot, not as a need for a replacement.",
      keyIdea: "Drop the student-slot. Do not hunt a replacement teacher or a replacement aim.",
      misconception:
        "That this verse licenses contempt for learning, or that quitting books while hunting a state is the same as dropping the seeker.",
      passageId: "astavakra_gita.ag_20_01",
      theme: "freedom",
      chatMode: "practice",
      chatPrompt:
        "Help me drop the student-slot for a day without hunting a replacement. Where is the itch still organizing a search?",
      practice:
        "Close the book after this station. For the rest of the day, do not start a new teaching. Keep one ordinary kindness. If the student-slot itches, notice it as a slot — not as a need for a new guru.",
      journalPrompt:
        "Where am I still keeping a student-slot open so the search can continue?",
      integration:
        "You can drop the student-slot for a day without hunting a replacement teacher or a replacement aim.",
    },
  ],
};
