import type { LearningTrack } from "../learningPaths";

/** Dedicated lineage walks that retarget Vedānta, Tao, and Greek chooser tiles. */
export const LINEAGE_TRAILS: LearningTrack[] = [
  {
    id: "you-are-that",
    title: "You Are That",
    level: "Beginner",
    focus: "Upaniṣads: fullness, discrimination, the witness, the Fourth",
    outcome:
      "Live from non-diminishing fullness, choose the good over the pleasant, hear tat tvam asi as addressed to the reader, and rest as the ground of waking rather than as the waking person.",
    description:
      "An eight-gate walk through Īśā, Kaṭha, Chāndogya, Śvetāśvatara, and the Māṇḍūkya.",
    arc:
      "We begin where Īśā begins: fullness does not shrink by appearing, so you can take part without coveting. Kaṭha then refuses to let 'spiritual life' mean choosing the pleasant. Only then does Chāndogya dare the sentence — you are That — and Śvetāśvatara shows why sorrow is identification with the bird that eats. Waking is named as an aperture, not as the Self. The Māṇḍūkya strips every state until the Fourth is not a fourth room, and OM's silence is the same awareness that heard the sound.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "isa-fullness",
        title: "Fullness taken from fullness remains fullness",
        orientation:
          "Before the world can be lived in, the scarcity-story has to lose its metaphysics.",
        teaching:
          "The invocation is not poetry in front of the teaching. It is the teaching's grammar. That is full; this is full; from fullness, fullness appears; take fullness from fullness and fullness remains. If manifestation reduced the source, possessiveness would be rational. Because it does not, grasping is a mistake about what kind of universe this is. Begin by catching the mind where it is already bargaining from lack — as if the next acquisition could complete a hole in being.",
        keyIdea: "The whole does not diminish by appearing. Lack is a mood, not the structure of the world.",
        misconception:
          "That spiritual life starts with a deficit you must fill, or that the world is a theft from God.",
        passageId: "isavasya_upanishad.isa_001",
        supportingPassageIds: ["plotinus_enneads.enn_v_1_06"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Help me hear pūrṇam as a claim about reality, not as a consolation. Where does my mind still treat the world as a scarce container?",
        practice:
          "Speak the invocation once, slowly. Then name one place today where you are already operating from lack. Do not fix it. See that the lack-story and the verse cannot both be true.",
        journalPrompt:
          "Where is my mind already operating from lack — and what would change if fullness were the ground, not the prize?",
        integration:
          "Lack feels like a mood you can notice, not like the structure of the world.",
      },
      {
        id: "isa-renunciation-in-action",
        title: "Enjoy through renunciation",
        orientation:
          "Fullness without a way to live becomes an excuse to leave. Īśā will not allow that split.",
        teaching:
          "All this moving world is covered by the Lord. Through what is relinquished, enjoy; do not covet anyone's wealth. Then: keep doing actions here, even for a hundred years — only so does action not stain. Renunciation is not a train out of life. It is the loosening of the claim 'mine' while the hands keep working. The text refuses both world-rejection and worldliness. You stay. You stop owning what you stay among.",
        keyIdea: "Renunciation is non-grasping participation. Action remains; ownership loosens.",
        misconception:
          "That holy life means withdrawal, or that staying in the world requires claiming it.",
        passageId: "isavasya_upanishad.isa_002",
        supportingPassageIds: ["bhagavad_gita.bg_02_47"],
        theme: "action",
        chatMode: "practice",
        chatPrompt:
          "Show me the difference between leaving a task and doing it without the inner claim of mine. Where do I confuse tyāga with avoidance?",
        practice:
          "Choose one ordinary task. Perform it fully. At the end, do not let the result report on your worth. Set the claim down with the tool.",
        journalPrompt:
          "Can I take part without claiming? What did the task become when 'mine' loosened?",
        integration:
          "You can finish a task without needing it to prove you.",
      },
      {
        id: "katha-two-paths",
        title: "The good is not the pleasant",
        orientation:
          "Death will not let Naciketas — or you — dress appetite as inquiry.",
        teaching:
          "The good is one thing, the pleasant another; both bind a person. It goes well for the one who takes the good; the one who chooses the pleasant falls from the goal. Both approach. The wise examine and discriminate. The fool chooses the pleasant for security. Naciketas, offered the wealth-snare, refused it. If you skip this gate, 'you are That' becomes a slogan for whatever you already wanted. The pleasant can wear spiritual clothes. The good often looks thinner at first.",
        keyIdea: "Śreyas and preyas both arrive. Wisdom is the fork, not the mood after.",
        misconception:
          "That what feels immediately relieving is the path, or that the good must feel grim.",
        passageId: "katha_upanishad.kau_04_two_paths",
        supportingPassageIds: ["bhagavad_gita.bg_02_47"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Walk me through one live choice. Help me name the pleasant option and the good one without letting the pleasant call itself wisdom.",
        practice:
          "In one real choice today, say aloud the two options: the pleasant, the good. Take the good, even if it is small — a conversation, a refusal, a remaining.",
        journalPrompt:
          "Which of the two am I choosing when I say I want truth?",
        integration:
          "You can feel the fork before you dress it as wisdom.",
      },
      {
        id: "chandogya-that-thou-art",
        title: "You are That",
        orientation:
          "Now the sentence can land — addressed to the one who is reading, not to a better self-image.",
        teaching:
          "That subtle essence is the Self of this whole world. That is the real. That is the Self. You are that, Śvetaketu. Uddālaka does not treat the mahāvākya as a slogan requiring instant assent. The boy asks to be taught again. 'You' does not mean the learned, changeable person who arrived at the lesson. It means the ātman already the inner reality of 'this whole.' If you hear a promotion of the ego to cosmic status, you have missed the pointing. If you hear a command to believe, you have missed the affection — dear one, so be it — and the work of remaining under the sentence until it is not a sentence.",
        keyIdea: "Tat tvam asi addresses the reader beneath the biography. It is a pointing, not a promotion.",
        misconception:
          "That 'you are That' inflates the person, or that it is a belief you must force.",
        passageId: "chāndogya_upaniṣad.chu_06_08_07",
        supportingPassageIds: ["siva_sutra.ss_i_1"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Who is the 'you' in tat tvam asi? Help me keep it from becoming either a slogan or a self-improvement fantasy.",
        practice:
          "Say the sentence once to the one who is reading — not to the résumé. Then, like Śvetaketu, ask to be shown further, and wait without manufacturing an experience.",
        journalPrompt:
          "Who do I think 'you' refers to when I hear tat tvam asi?",
        integration:
          "The sentence points at the reader, not at a better self-image.",
      },
      {
        id: "svu-two-birds",
        title: "Two birds on one tree",
        orientation:
          "Sorrow has a mechanics: identification with the bird that eats.",
        teaching:
          "Two companion birds on one tree. One eats the sweet fruit; the other, not eating, watches. The person sunk in non-sovereignty grieves. When he sees the other — the Lord, already on the same tree — sorrow lifts. The fruit does not have to vanish. The watching bird is not a cold observer you invent; it is the deeper axis you forgot. Freedom here is participatory: seeing, and ceasing to take the eater as the whole of you.",
        keyIdea: "Experience continues. Identification with the eater is the sorrow.",
        misconception:
          "That the witnessing bird means numbness, or that the eating bird must be killed.",
        passageId: "svetasvatara_upanishad.svu_011",
        supportingPassageIds: ["astavakra_gita.asg_1_7"],
        theme: "witness",
        chatMode: "practice",
        chatPrompt:
          "Help me use the two birds in a live reaction without turning witness into dissociation.",
        practice:
          "In one charged moment, silently name the fruit-eating bird. Rest sixty seconds as the watching bird. Do not edit the fruit. Notice they share a tree.",
        journalPrompt:
          "Which bird did I take myself to be in the last hour?",
        integration:
          "You can watch a reaction without pretending you are only it.",
      },
      {
        id: "muk-waking-aperture",
        title: "Waking is not the whole Self",
        orientation:
          "The daylight person is a mode of consciousness, not its ground.",
        teaching:
          "The first quarter is Vaiśvānara: sphere of waking, outward-facing, seven limbs, nineteen mouths, eater of the gross. Individual waking is cosmic consciousness at a particular aperture. The sense of being a separate someone in a world of objects is what happens when awareness identifies with the apparatus — eye, name, preference, memory — rather than with the field in which the apparatus appears. You do not have to leave the day. You have to stop taking the day-person as the one who is.",
        keyIdea: "Waking is an aperture. The seer is not the nineteen mouths.",
        misconception:
          "That the waking personality is the Self, or that spiritual life means distrusting the senses as such.",
        passageId: "mandukya_upanishad_and_gaudapada_karika.muk_005",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_004"],
        theme: "consciousness",
        chatMode: "explain",
        chatPrompt:
          "Help me feel waking as a mode rather than as the whole of me, without sliding into depersonalization.",
        practice:
          "For three minutes of ordinary seeing, notice the apparatus — eye, name, like and dislike — and the awareness in which that apparatus appears. Then go on with the day as the same awareness, not as a new personality.",
        journalPrompt:
          "Do I take the daylight person as the one who is?",
        integration:
          "Waking feels like a mode, not like the whole of you.",
      },
      {
        id: "muk-turiya",
        title: "Not waking, not dream, not sleep",
        orientation:
          "The Fourth is reached by stripping states, not by adding a special one.",
        teaching:
          "Not inwardly conscious, not outwardly, not both, not a mass of consciousness, not consciousness, not unconsciousness. Unseen, ungraspable, the essence of recognizing the single Self, the quieting of the world-display, peaceful, without a second. This they call the Fourth. This is the Ātman. This is to be known. If you hunt turīya as a fourth inner weather, you are still collecting states. The method is apophasis: every label the mind offers, not that. What remains is not a blank. It is what the labels were appearing in.",
        keyIdea: "Turīya is the ground of the three states, not a fourth room beside them.",
        misconception:
          "That the Fourth is a special experience you must produce, or that it is unconsciousness.",
        passageId: "mandukya_upanishad_and_gaudapada_karika.muk_009",
        supportingPassageIds: ["vijnana_bhairava.yukti_047"],
        theme: "consciousness",
        chatMode: "explain",
        chatPrompt:
          "Why does the verse refuse every positive description? Where am I still looking for turīya as a state?",
        practice:
          "Sit five minutes. When a state labels itself — awake, foggy, dreaming-thought — say not that. Rest as what the label appears in. Do not replace it with a better label.",
        journalPrompt:
          "Am I hunting a fourth experience?",
        integration:
          "You stop looking for the Fourth as a special inner weather.",
      },
      {
        id: "muk-silence-after-om",
        title: "The silence after OM",
        orientation:
          "The Upaniṣad ends in the present tense: the Self merges into the Self by the Self.",
        teaching:
          "The Fourth is without measure — amātrā. The three sounds are within the silence; the silence is not a fourth letter. OM is the Ātman. One who knows this enters the Self by the Self into the Self. Subject, object, and instrument are the same word. This is not a future event. The sound dissolves. The awareness that heard it does not. If the quiet after OM feels empty, you are still waiting for an object. If it feels like the same knowing that heard the syllable, you have the verse.",
        keyIdea: "The silence after the sound is the same awareness that heard it.",
        misconception:
          "That the quiet is a blank to endure, or that merger is the person being erased into an other.",
        passageId: "mandukya_upanishad_and_gaudapada_karika.muk_015",
        supportingPassageIds: ["vijnana_bhairava.yukti_001"],
        theme: "silence",
        chatMode: "practice",
        chatPrompt:
          "Walk me through sounding OM so the silence is recognized as ground, not as a gap to fill.",
        practice:
          "Sound OM once — A, U, M — and follow it into the silence. Rest one unhurried breath in that measureless quiet. Do not make the silence. Notice it was already there.",
        journalPrompt:
          "Is the quiet after sound empty, or full?",
        integration:
          "The silence after the sound feels like the same awareness that heard it.",
      },
    ],
  },
  {
    id: "nameless-source",
    title: "The Nameless Source",
    level: "Beginner",
    focus: "Tao: the unnameable, return, useful absence, wúwéi",
    outcome:
      "Stop pinning the Way with a name, watch the ten thousand things return, use emptiness instead of stuffing it, and subtract one forcing from ordinary action.",
    description:
      "An eight-gate walk through the Tao Te Ching, with Zhuangzi's heart-fasting as the inner method.",
    arc:
      "The named way is not the enduring way. Something formless already circulates as mother of the world, and the pattern is return. Emptiness is what makes the wheel, the vessel, and the room work. Non-acting leaves nothing undone; water goes where no one wants to be; the heart fasts of its plans; the Way is daily diminishing, not daily adding.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "ttc-unname",
        title: "The name that unnames itself",
        orientation:
          "The book opens by refusing to be what you will try to make it.",
        teaching:
          "The way that can be walked is not the enduring way. The name that can be named is not the enduring name. This is not mystical fog. Language pins; what it points at does not stay pinned. Named and unnamed are the same reality, approached with desire or without: desire sees the boundary, non-desire the interior. Dark upon dark is not a door that opens once. It is the structure of inexhaustible opening. If you need the last word, you will meet only the fringe.",
        keyIdea: "The named Way and the unnamed Way are one reality, approached differently.",
        misconception:
          "That the Tao is a secret name you have not learned yet, or that language is useless.",
        passageId: "tao_te_ching.ttc_md_001",
        supportingPassageIds: ["plotinus_enneads.enn_vi_9_01"],
        theme: "way",
        chatMode: "explain",
        chatPrompt:
          "Help me hear chapter 1 as an instruction about how to read, not as a riddle to solve.",
        practice:
          "Hold one conviction without using its name for ten breaths. Let it be approached, not filed. Notice the urge to pin it so you can own it.",
        journalPrompt:
          "What am I trying to pin with a name so I can own it?",
        integration:
          "You can touch a thing without needing the last word on it.",
      },
      {
        id: "ttc-formless-mother",
        title: "Something formless before heaven and earth",
        orientation:
          "Forced to name it, Lǎozǐ says Way, then Great, then passing, far, returning.",
        teaching:
          "There is a thing, blended and whole, born before heaven and earth — silent, empty, standing alone, circulating without peril, mother of the world. I do not know its name; I style it dào. Compelled, I call it Great: passing, far, returning. Humans model earth; earth, heaven; heaven, the Way; the Way models what is so of itself. Return is not failure. It is how the Great moves. You are not asked to invent a creator. You are asked to notice a process that was already mothering the ten thousand things, including the one who wants a better theory.",
        keyIdea: "Return is the Way's motion, not a defeat.",
        misconception:
          "That the Tao is a person behind the world, or that returning means going backwards in time.",
        passageId: "tao_te_ching.ttc_md_007",
        supportingPassageIds: ["tao_te_ching.ttc_md_001"],
        theme: "way",
        chatMode: "explain",
        chatPrompt:
          "What does it mean that the Way models zìrán — what is so of itself — rather than commanding?",
        practice:
          "Watch one cycle complete today — a task, a mood, a conversation. Notice the return without improving it or calling it a loss.",
        journalPrompt:
          "Do I need a creator, or can I trust a mothering process already underway?",
        integration:
          "Return feels like the Way's motion, not like defeat.",
      },
      {
        id: "ttc-return-to-root",
        title: "The ten thousand things return to the root",
        orientation:
          "Empty to the utmost, then watch. Stillness is how the pattern becomes visible.",
        teaching:
          "Bring emptiness to its utmost; guard stillness. The ten thousand things arise together — you watch their return. Each goes back to its root. That return is stillness, returning to destiny, the constant. Knowing the constant is clarity; not knowing it, reckless action brings misfortune. This is not Buddhism's impermanence as the dissolution of a constructed self. It is cyclical completion as the most basic pattern. Forcing is what happens when you cannot bear a thing finishing.",
        keyIdea: "Stillness is how you see the return. Recklessness is acting as if there were no cycle.",
        misconception:
          "That stillness means shutting life down, or that return is death-talk.",
        passageId: "tao_te_ching.ttc_md_003",
        supportingPassageIds: ["plotinus_enneads.enn_v_1_06"],
        theme: "emptiness",
        chatMode: "practice",
        chatPrompt:
          "Help me watch one arising return without turning stillness into a pose or a freeze.",
        practice:
          "Sit until the inner noise drops one notch. Watch one urge or thought go back without escorting it to a conclusion.",
        journalPrompt:
          "What am I forcing because I cannot bear the return?",
        integration:
          "You can let a thing finish without grabbing the next.",
      },
      {
        id: "ttc-empty-hub",
        title: "The empty hub does the work",
        orientation:
          "Absence is not a hole in being. It is what function needs.",
        teaching:
          "Thirty spokes; the hole at the hub makes the wheel work. Clay walls; the void makes the vessel work. Doors and windows; the empty room is what you live in. What has being gives the useful shape; what has non-being gives the actual use. Do not hear that matter is a lie. Hear which part is the enabling condition. If you stuff every pause, every surface, every conversation, you have spokes and no turning.",
        keyIdea: "Form is the container of function; emptiness is the function.",
        misconception:
          "That emptiness means nothing matters, or that you should despise form.",
        passageId: "tao_te_ching.ttc_md_002",
        supportingPassageIds: ["vijnana_bhairava.yukti_002"],
        theme: "emptiness",
        chatMode: "explain",
        chatPrompt:
          "Show me one place in my day where I am stuffing the space that would let the thing work.",
        practice:
          "Clear one small space — a surface, a pause in speech, a gap in the calendar — and leave it empty on purpose. Use the absence.",
        journalPrompt:
          "Where am I stuffing the space that would let the thing work?",
        integration:
          "You have used an absence today instead of filling it.",
      },
      {
        id: "ttc-nothing-undone",
        title: "Nothing left undone",
        orientation:
          "Wúwéi is the grain of the Way, not an alibi for neglect.",
        teaching:
          "The Way is constant: non-acting, and yet nothing left undone. If this were guarded, the ten thousand things would transform by themselves. When desire restarts, settle it with the nameless uncarved block. Without desire, by stillness, the world settles itself. Wúwéi is not laziness. It is not forcing the grain. The extra push is often the interference. Enough is when the need is met, not when you have been seen meeting it.",
        keyIdea: "Non-acting is not inactivity. It is action without the extra force that distorts.",
        misconception:
          "That wúwéi means doing nothing, or that effort as such is the enemy.",
        passageId: "tao_te_ching.ttc_md_008",
        supportingPassageIds: ["bhagavad_gita.bg_02_47"],
        theme: "action",
        chatMode: "practice",
        chatPrompt:
          "Where is my effort the interference? Give me a way to do the next necessary act with one less push.",
        practice:
          "Do the next necessary act with one less push than habit. Stop when it is enough, not when you have been seen doing it.",
        journalPrompt:
          "Where is my effort the interference?",
        integration:
          "You can leave a thing unfinished by ego and finished by need.",
      },
      {
        id: "ttc-like-water",
        title: "Water goes where no one wants to be",
        orientation:
          "Closeness to the Way looks like the low place, not the contest.",
        teaching:
          "Supreme goodness is like water. It benefits the ten thousand things without contending, and settles where people disdain to go — therefore it is close to the Way. Low is not humiliation. It is how water works. If you need the high seat to know you are good, you are already contending. The practice is not a speech about humility. It is taking the share that nourishes without a portrait of the one who took it.",
        keyIdea: "Water benefits without contending. The low place is how it reaches.",
        misconception:
          "That low means self-erasure, or that non-contention means letting harm run.",
        passageId: "tao_te_ching.ttc_md_006",
        supportingPassageIds: ["the_book_of_chuang_tzu.zhuangzi_md_004"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "What low place am I avoiding that would actually nourish? Help me take it without turning it into a humility performance.",
        practice:
          "Take the unglamorous share of one joint task. Do it cleanly. Do not tell the story of it, including to yourself.",
        journalPrompt:
          "What low place am I avoiding that would actually nourish?",
        integration:
          "You can occupy a low place without turning it into a story.",
      },
      {
        id: "zz-heart-fasting",
        title: "Heart-fasting",
        orientation:
          "Yan Hui asked for a method to steer a ruler. Confucius emptied the one who wanted to steer.",
        teaching:
          "Ritual fasting is not heart-fasting. Unify intention. Do not listen with the ears; listen with the heart-mind. Do not listen with the heart-mind; listen with qi. Qi is emptiness, waiting for things. Only the Way gathers in emptiness. That emptiness is heart-fasting. The method is de-methodologizing the self that wanted a technique to win the room. If you arrive with the plan already written, nothing can gather.",
        keyIdea: "The Way gathers in emptiness. Plans to steer are a full stomach.",
        misconception:
          "That emptiness means having no care, or that listening is passivity.",
        passageId: "the_book_of_chuang_tzu.zhuangzi_md_004",
        supportingPassageIds: ["tao_te_ching.ttc_md_002"],
        theme: "emptiness",
        chatMode: "practice",
        chatPrompt:
          "Help me drop the plan to steer one conversation without becoming blank or withdrawn.",
        practice:
          "Before one conversation, drop the plan to steer it. Listen until the breath feels like the listener. Receive one thing you did not pre-write.",
        journalPrompt:
          "What method am I using to stay in control of the room?",
        integration:
          "You have received a situation you did not pre-write.",
      },
      {
        id: "ttc-way-subtracts",
        title: "The Way subtracts",
        orientation:
          "The path closes as a discipline of diminishing, not of becoming more impressive.",
        teaching:
          "In pursuing the Way, daily diminish. Diminish again, until non-action — and nothing left undone. The world is not taken by accumulating affairs. Learning adds distinctions; the Way strips contrivance. This is not anti-intellectualism. It is a claim about what kind of knowing lets you align. The extra check, the extra opinion, the extra improvement: often these are how you refuse to trust the grain. Subtract one. See if the hour still holds.",
        keyIdea: "The Way is daily diminishing. Adding is often how we avoid trust.",
        misconception:
          "That subtraction means becoming less capable, or that ignorance is the Way.",
        passageId: "tao_te_ching.ttc_md_011",
        supportingPassageIds: ["tao_te_ching.ttc_md_008"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "What one extra move can I remove from a habit today without calling it self-erasure?",
        practice:
          "Remove one extra move from a habit — an extra check, opinion, or improvement. Live the hour with the subtraction.",
        journalPrompt:
          "What am I adding so I will not have to trust the Way?",
        integration:
          "Diminishing feels like alignment, not like self-erasure.",
      },
    ],
  },
  {
    id: "become-sunlike",
    title: "Become Sunlike",
    level: "Intermediate",
    focus: "Plotinus: unity, overflow, forgetting, the inward turn, union",
    outcome:
      "See that a life is by unity, that the One overflows without loss, that the soul forgets by misplaced love, and that return is chiselling until seer and seen are not two.",
    description:
      "A six-gate walk through the Enneads: from unity and emanation to the forgotten soul's return.",
    arc:
      "A thing is by being one. The One does not remain childless: Intellect proceeds as overflow, not as lack. The soul forgets the Father by wanting to own herself among things. She must stop chasing copies, chisel the statue until she is sunlike, and rest alone to the alone — not as a report, as a simplification.",
    estimatedSessions: "6 gates · ~20 min each",
    steps: [
      {
        id: "enn-unity",
        title: "A thing is by being one",
        orientation:
          "Before overflow and return, Plotinus names why anything is a this at all.",
        teaching:
          "All beings are beings by unity. An army, a chorus, a house, a living body: deprive them of the unity predicated of them and they are not those things. When the unity dissolves they become other, and those others exist only insofar as each is one. You are not a heap of roles that happens to share a name. The unity by which this life is a life is not a number you add. It is the condition of there being a this. Scatter is cheap. Oneness is what you keep losing and having to gather.",
        keyIdea: "Unity is not a count. It is why there is a this rather than a heap.",
        misconception:
          "That unity means sameness, or that you become one by collecting more parts.",
        passageId: "plotinus_enneads.enn_vi_9_01",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_001"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Help me tell a heap from a life in my own attention today, without turning unity into a self-help slogan.",
        practice:
          "Name one scatter — tabs, roles, arguments. Gather to one act for ten minutes. Feel the difference between heap and one.",
        journalPrompt:
          "What in me is a heap pretending to be a life?",
        integration:
          "You can tell a heap from a life, in your own attention.",
      },
      {
        id: "enn-overflow",
        title: "The One does not stay childless",
        orientation:
          "The puzzle of the ancients: why did the perfect not remain alone?",
        teaching:
          "How does Intellect come from the One, which then becomes what it sees? If the One is complete, why is there anything else? Plotinus's answer is not lack. Overflow is what completeness does. Generation here is not a fall from boredom or a cosmic accident. The One remains; Intellect looks, and looking, is. You are not asked to solve the metaphysics as a puzzle. You are asked to recognize a generosity that does not reduce the source — the same grammar Īśā used for fullness. Giving from need makes you less. Giving from fullness does not.",
        keyIdea: "The many proceed from the One as overflow, not as a leak in perfection.",
        misconception:
          "That creation means God was lonely, or that the world is a fall that should not have happened.",
        passageId: "plotinus_enneads.enn_v_1_06",
        supportingPassageIds: ["tao_te_ching.ttc_md_001"],
        theme: "consciousness",
        chatMode: "explain",
        chatPrompt:
          "Why does Plotinus refuse to let the One remain childless? Help me feel overflow as generosity rather than as a mistake.",
        practice:
          "Give one thing from fullness, not from needing to be needed — a word, a help, a silence. Notice whether the source felt reduced.",
        journalPrompt:
          "Why did the perfect not remain alone — in this philosophy, and in the way I give?",
        integration:
          "You have felt a giving that did not make you less.",
      },
      {
        id: "enn-forgetting",
        title: "The soul no longer knows the Father",
        orientation:
          "Descent is not a myth about the past. It is misplaced love, now.",
        teaching:
          "The soul no longer knows the Father, and has forgotten herself. Forgetting is not amnesia. It is becoming enamored of what is beneath her, wanting self-ownership among things that pass. Two disciplines: see the dishonour of what you overprize, and recall what you are. Without the first, memory of worth becomes vanity. Without the second, critique of the world becomes bitterness. The downward spiral is ignorance wearing the face of appetite.",
        keyIdea: "Forgetfulness is misplaced love. Return begins by withdrawing honour from what cannot bear it.",
        misconception:
          "That the soul is wicked, or that the world is to be hated rather than rightly ranked.",
        passageId: "plotinus_enneads.enn_v_1_01",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_012"],
        theme: "self",
        chatMode: "question",
        chatPrompt:
          "What honour am I paying to what is beneath me? Help me use both disciplines — dishonour of the overprized, and recall of worth — without self-contempt.",
        practice:
          "Pick one prized object — status, comfort, a wound. Name what it cannot give. Then remember, for one minute, a worth that does not come from it.",
        journalPrompt:
          "What honour am I paying to what is beneath me?",
        integration:
          "You can catch a downward love without dramatizing it.",
      },
      {
        id: "enn-copies",
        title: "Do not chase the copies",
        orientation:
          "Beautiful things are real as traces. They are not the Beauty they copy.",
        teaching:
          "How will you see the inaccessible Beauty? Withdraw into yourself. When beautiful forms pull, do not pursue them as the end — they are eidōla, remnants, shadows. Hasten toward what they represent. This is not hatred of the world. It is refusing to hunt the source in a gleam. The senses can start the love. They cannot complete it. If you try to keep the remnant, you lose even the remnant's work, which was to point.",
        keyIdea: "The gleam is a copy. Turn inward before you try to keep it.",
        misconception:
          "That Plotinus wants you to despise beauty, or that inward means ignoring the world.",
        passageId: "plotinus_enneads.enn_i_6_08",
        supportingPassageIds: ["tao_te_ching.ttc_md_003"],
        theme: "beauty",
        chatMode: "practice",
        chatPrompt:
          "A beautiful thing pulls. How do I thank the copy and turn toward what it copies, without becoming cold?",
        practice:
          "When a beautiful thing pulls, look once, thank it, and step back inward before you try to keep it.",
        journalPrompt:
          "Where am I hunting beauty in a remnant?",
        integration:
          "You can admire without chasing the copy as if it were the source.",
      },
      {
        id: "enn-chisel",
        title: "Never stop chiselling your statue",
        orientation:
          "Only the sunlike sees the sun. The work is the condition of the vision.",
        teaching:
          "Withdraw into yourself and look. How will you see a beautiful soul? By becoming one: cut away, straighten, polish, as a sculptor reveals the statue by taking off what is too much. Never stop chiselling. As you become this work, self-gathered, you see the goodness established within — then you can strain toward the First Beauty. You were waiting to see in order to become able to see. Plotinus reverses it. The seeing is the becoming. The becoming is the seeing.",
        keyIdea: "Only the sunlike sees the sun. Cut excess; do not add ornament and call it vision.",
        misconception:
          "That you wait for a vision and then improve, or that chiselling means self-hatred.",
        passageId: "plotinus_enneads.enn_i_6_09",
        supportingPassageIds: ["siva_sutra.ss_i_5"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "What one excess can I cut today so that seeing becomes possible? Keep me from turning the chisel into punishment.",
        practice:
          "Cut one excess from the statue today — a vanity, a cruelty, a fog. Do not add ornament. Look again.",
        journalPrompt:
          "Am I waiting to see Beauty before I become able to see it?",
        integration:
          "You have removed something so that seeing could happen.",
      },
      {
        id: "enn-alone-to-alone",
        title: "Alone to the alone",
        orientation:
          "The path ends where seer and seen are no longer two — and this is not for gossip.",
        teaching:
          "The vision is not a report for the uninitiate. In it the distinction of seer and seen dissolves. What remains is unified awareness, still, beyond the fidget of intellect and passion. Alone to the alone is not loneliness. It is the end of the second self who stands outside the rest, describing it. If you can sell the quiet, you have not reached it. If you can rest without a narrator, you have the shape of the gate — whether or not you claim the name union.",
        keyIdea: "Union is a simplification, not a story you tell about yourself.",
        misconception:
          "That union is an experience to display, or that it annihilates you into a blank.",
        passageId: "plotinus_enneads.enn_vi_9_11",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_020"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Help me sit toward simplification without manufacturing a mystical report.",
        practice:
          "Sit until the inner narrator has nothing left to sell. Do not describe the quiet to yourself. Leave it unnamed. Then return to the next ordinary act.",
        journalPrompt:
          "What would remain if seer and seen were not two?",
        integration:
          "You can rest without a second self standing outside the rest.",
      },
    ],
  },
];
