import type { LearningTrack } from "../../learningPaths";

/** Selected doorways through Haṭha — not one gate per catalogue verse. */
export const THE_BODY_OF_HATHA: LearningTrack = {
  id: "the-body-of-hatha",
  title: "The Body of Haṭha",
  level: "Beginner",
  focus: "Haṭha yoga: the body and breath as a staircase to rāja yoga, walked as a householder",
  outcome:
    "Sit one daily seat, keep the breath even, and refuse the catalogue — knowing haṭha as shelter and a lever, not a fitness brand.",
  description:
    "Eight selected doorways from the Haṭha Yoga Pradīpikā and the Śiva Saṃhitā: from Ādinātha's staircase to one daily seat and breath.",
  arc:
    "The Haṭha Yoga Pradīpikā is a catalogue large enough to drown a householder — āsanas, kumbhakas, mudrās, nāda. This path does not march it. It samples eight doorways so you can keep one method: haṭha as a staircase to rāja yoga, not a studio brand; the practice itself as the house, not an ashram you must first acquire; six inner conditions instead of more hours of stretching; āsana as the first accessory, not the whole of yoga; one chief seat, analog to sparing food among the yamas; the breath-mind knot (when the wind moves, the mind moves); even breath as the householder's restraint, without a long kumbhaka from the page; and the Śiva Saṃhitā's seal — yoga is how this is known, so other doctrines (and the remaining eighty-four āsanas) can wait. The last gate does what the 112 Doorways do: you do not complete the list; you let one daily seat and one even breath collect you.",
  estimatedSessions: "8 gates · ~20 min each",
  steps: [
    {
      id: "hyp-adinatha",
      title: "A Staircase, Not a Studio",
      orientation:
        "Gate 1 · The staircase. Before a single pose, the book names what haṭha is for — or you will spend the whole walk in a fitness brand.",
      teaching:
        "You already have a use for this word, and it is probably the wrong one. Haṭha arrives as a fitness class, an āsana brand, a body you improve. The book does not open there. It salutes Ādinātha — Śiva as the first lord who taught this knowledge — and it calls haṭha a staircase for the one who wants to climb to rāja yoga. A staircase is not the roof. You still have to put a foot on a rung; the rung is not the point. Name the difficulty: the body work is real, and it is easy to stop at the body. The act is to take one rung as a rung — sit, breathe — without promising yourself a peak at the top.",
      keyIdea: "Haṭha is a staircase toward rāja yoga. The pose is a rung, not the house.",
      misconception:
        "That haṭha is a fitness class or an āsana brand — stretching as the whole of yoga.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_001",
      supportingPassageIds: ["hatha_yoga_pradipika.hatha_yoga_pradipika_392"],
      theme: "staircase",
      chatMode: "explain",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 1.1 salutes Ādinātha and calls haṭha a staircase to rāja yoga. Help me drop the fitness-brand reading without pretending I am already at the top.",
      practice:
        "Before you move or stretch today, stand or sit still and say aloud what you are climbing toward — not a better shape, the stilling the staircase is for. Then take one rung: two minutes upright, no extra poses, no soundtrack.",
      journalPrompt:
        "When I say yoga, am I naming a body project or a climb whose top is stilling?",
      integration:
        "You can tell the difference between using the body as a rung and treating the rung as the whole house.",
    },
    {
      id: "hyp-house",
      title: "The House You Already Have",
      orientation:
        "Gate 2 · The house. The staircase is named. Now the text gives haṭha as shelter — so you stop waiting for a hermitage.",
      teaching:
        "The difficulty is location. You tell yourself haṭha needs a maṭha — a proper house, a quiet ashram, a life stripped for the cave. The verse turns the image: haṭha itself is the house that shelters from the burning of the three tāpas, and the tortoise-base for those who stay with the work. You do not first acquire a special building and then deserve to practice. The seat you can take in this room is the shelter. Heat still comes — restlessness, other people, the weather of the day. The act is to use breath and a steady form as the house, not to go hunting a better climate.",
      keyIdea: "The practice is the house. You do not need an ashram before you sit.",
      misconception:
        "That you need a special ashram, cave, or perfect room before haṭha can begin.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_010",
      theme: "shelter",
      chatMode: "practice",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 1.10 calls haṭha a house against the three heats. Help me take refuge in a seat in ordinary heat instead of postponing for a better place.",
      practice:
        "The next time heat rises — hurry, irritation, a hot room, a noisy house — do not leave for a better place. Sit or stand where you are. Three slow breaths. Feel the body as the walls. This is the house.",
      journalPrompt:
        "What heat am I using as an excuse to postpone practice until I have a better room?",
      integration:
        "You can take refuge in a seat in ordinary heat, without waiting for an ashram.",
    },
    {
      id: "hyp-six",
      title: "Six That Bring Success",
      orientation:
        "Gate 3 · The six. The catalogue will tempt volume. Success here is six inner conditions, none of them another hour of stretching.",
      teaching:
        "You will try to buy progress with more time on the floor. The list is not a stretching schedule. Courage, daring, perseverance, discriminative knowledge, faith, and a deliberate distance from scattering company — these are the six that make the work take. The difficulty is that they sound like character, so you skip them and add poses. Name the missing one today. Distance from company, for a householder, is not abandoning your people; it is one hour without feeding the scatter that undoes the seat. No extra āsana. The quality is the practice.",
      keyIdea: "The six that bring success are dispositions, not more hours of stretching.",
      misconception:
        "That speedy success means more hours of stretching, rather than the six inner conditions.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_016",
      theme: "conditions",
      chatMode: "question",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 1.16 lists six that bring success. Help me find which one is actually missing today, instead of adding stretching to hide it.",
      practice:
        "Name which of the six is absent this morning. For one ordinary hour of work or home, practice only that quality — courage to stay with what arises, or discrimination about what actually serves, or an hour of not scattering. Do not add stretching to compensate.",
      journalPrompt:
        "Which of the six is actually missing — and what extra stretching am I using to hide that?",
      integration:
        "You can point to one missing condition and work it in the day, instead of adding a pose.",
    },
    {
      id: "hyp-asana-first",
      title: "Āsana Is First, Not All",
      orientation:
        "Gate 4 · The first accessory. Now āsana may be praised — after you know it is a limb, not the organism.",
      teaching:
        "Āsana is described first because it is the first accessory of haṭha, practiced for a steady seat, health, and lightness of the body. The difficulty is the modern reversal: āsana became the whole of yoga, and the rest of the staircase dropped out of sight. First is not only. A chair that holds you upright for five minutes is āsana in the sense this gate needs — steady enough to sit, light enough that you are not fighting the body. You are not collecting shapes. You are making a seat that can later hold breath without drama.",
      keyIdea: "Āsana is the first accessory: a seat, health, lightness — not the whole of yoga.",
      misconception:
        "That āsana is the whole of yoga, rather than the first accessory of a longer method.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_019",
      supportingPassageIds: ["patañjali_yoga_sūtras.ys_2_46_48"],
      theme: "asana",
      chatMode: "explain",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 1.19 puts āsana first as an accessory for a steady seat, health, and lightness. Help me keep 'first' from becoming 'only.'",
      practice:
        "Sit upright for five minutes — cross-legged, kneeling, or a chair. Do not add a second pose. Notice where you are steady, where tension pulls you off, where the body is heavy or light. Stay. That is the accessory.",
      journalPrompt:
        "Where have I let the first accessory stand in for the whole path?",
      integration:
        "You can keep one upright seat as preparation, without treating the seat as the whole of yoga.",
    },
    {
      id: "hyp-siddha",
      title: "One Seat, as Sparing Food Is Among Yamas",
      orientation:
        "Gate 5 · The chief seat. Before the catalogue of poses opens, one seat is ranked as yama ranks measured food.",
      teaching:
        "Just as sparing food is chief among the yamas and ahiṃsā among the niyamas, the adept names siddhāsana chief of āsanas. The difficulty is appetite: you want the eighty-four. The analogy is not a fast; do not starve yourself. Sparing food here means one measured thing done as the root, not a pile of extras. For a householder, the chief seat is the one you can actually keep — a chair if that is honest — not a lock that needs a teacher in the room. Collecting poses is how you postpone the seat. One stable upright form, returned to, is the ranking this gate enforces.",
      keyIdea: "One seat, kept, outweighs a collection of poses — as measured food is chief among yamas.",
      misconception:
        "That you should collect many poses. Mastery here is one seat you can keep.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_040",
      theme: "one-seat",
      chatMode: "practice",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 1.40 ranks siddhāsana as yama ranks sparing food. Help me keep one householder seat instead of collecting poses or starting a fast.",
      practice:
        "Choose one upright seat you can take without specialist instruction (chair, cushion, or floor). Sit it for ten minutes today. Do not learn a second pose. Eat your next meal at ordinary size — the analogy is measure, not a fast.",
      journalPrompt: "How many poses am I collecting to avoid keeping one?",
      integration:
        "You can name your one seat and keep it, without adding shapes to feel like a yogin.",
    },
    {
      id: "hyp-breath-mind",
      title: "When the Wind Moves, the Mind Moves",
      orientation:
        "Gate 6 · The lever. The seat exists. Now the knot: vāta and citta move together. Reverse the order that tries to still thought first.",
      teaching:
        "You will try to control the mind first — a better thought, a stronger will — and visit the body later. The verse will not have it. Respiration disturbed, the mind becomes disturbed. Steady the wind and the mind can stand. That is haṭha's lever, and it is unflattering: your philosophy will not outrun a tight chest. Do not force a heroic hold. The act is to meet one ragged breath in the day and smooth the leaving of it. Let the mind follow if it will. You are not promised stillness. You are given the lever.",
      keyIdea: "Disturbed breath, disturbed mind. Steady the breath; do not argue with thought first.",
      misconception:
        "That you should control the mind first and visit the body later. Haṭha uses the breath as the lever.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_071",
      theme: "breath-mind",
      chatMode: "practice",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 2.2: when respiration is disturbed, the mind is disturbed. Help me use a smoothed exhale as the first move, without a long hold.",
      practice:
        "Catch one moment of irregular breath — a message, a queue, a sharp word. For two or three minutes, lengthen and smooth only the exhale. Do not hold. Do not fix the thoughts. Watch whether the mind follows the breath at all.",
      journalPrompt:
        "Where am I trying to argue the mind quiet while the breath stays ragged?",
      integration:
        "You can use a smoothed exhale as the first move when the mind is already noisy, instead of arguing with thought.",
    },
    {
      id: "hyp-breath-work",
      title: "So Long as the Breath Stays",
      orientation:
        "Gate 7 · Even breath. The lever is named. Now restrain means keep the breath even and present — not a kumbhaka taken from the catalogue.",
      teaching:
        "The verse is blunt: while the breathing air stays in the body, that is called life; death is its going out; therefore restrain the breath. The difficulty is the verb. Nirodha sounds like stop. A long kumbhaka taken from a manual, without a teacher, is how people hurt themselves. You do not do that here. Restrain, for this gate, means keep the breath with you — even in, even out, no added hold, no strain. You are participating in the fact of being alive, not staging a retention. If the count makes you gasp, shorten it. The state of mastery is not on offer. Eight even cycles are the act.",
      keyIdea: "Restrain the breath by keeping it even and present. Not a long hold from a page.",
      misconception:
        "That prāṇāyāma here means heroic kumbhaka or stopping the breath. For a householder it means even lengthening, no long retention.",
      passageId: "hatha_yoga_pradipika.hatha_yoga_pradipika_072",
      theme: "even-breath",
      chatMode: "practice",
      chatPrompt:
        "Haṭha Yoga Pradīpikā 2.3 says restrain the breath because it is life. Guide me in even inhale and exhale with no long kumbhaka, and help me stop if strain appears.",
      practice:
        "Sit your one seat. Take eight breaths, inhale and exhale the same easy count (four is enough). No pause at the top or bottom beyond the natural turn. If strain appears, drop the count and breathe ordinarily. Stop at eight.",
      journalPrompt:
        "Am I about to turn 'restrain the breath' into a hold I was never taught?",
      integration:
        "You can lengthen the breath evenly without inserting a hold, and you can stop when strain appears.",
    },
    {
      id: "hyp-commit",
      title: "One Method, Fully Kept",
      orientation:
        "Gate 8 · One method. The seal of a catalogue-path: you do not complete eighty-four āsanas. You keep one daily seat and breath.",
      teaching:
        "You have sampled a huge book. The hunger now is to finish it — eighty-four āsanas, every kumbhaka, a complete yogin. That hunger is the last misconception. Since by yoga all this is known as a certainty, all exertion should be made to acquire it; what need, then, of other doctrines? Other doctrines include the rest of the catalogue. You do not become a yogin by covering the list. You keep one method until it is how you know — a seat you already have, an even breath you already took. Breadth was the walk. Depth is the door. Choose the seat and the eight even breaths. Same time, same place, ten minutes, seven days. Add nothing. The state is not promised. The act is the appointment kept.",
      keyIdea: "Yoga is how this is known. One daily seat and even breath outweigh the unread catalogue.",
      misconception:
        "That you must complete eighty-four āsanas (or the rest of the manuals). One method, fully kept, is the path.",
      passageId: "siva_samhita.siva_samhita_014",
      supportingPassageIds: ["vijnana_bhairava.yukti_112"],
      theme: "commit",
      chatMode: "practice",
      chatPrompt:
        "Śiva Saṃhitā 1.18: by yoga all this is known; what need of other doctrines? Help me choose one daily seat-and-breath and refuse the rest of the catalogue for a week.",
      practice:
        "Look back over the seven gates. Keep only this: your one upright seat and eight even breaths, ten minutes, at a time you can actually keep, for seven days. Do not add a pose. Do not add a hold. If you miss a day, begin the seven again without drama.",
      journalPrompt:
        "Which single daily seat-and-breath am I willing to keep, and what catalogue am I using to postpone it?",
      integration:
        "You can name the one daily method and keep it for a week without expanding into the catalogue.",
    },
  ],
};
