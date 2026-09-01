import type { LearningTrack } from "../learningPaths";
import { DEEPENING_TRAILS } from "./deepeningTrails";
import { LINEAGE_TRAILS } from "./lineageTrails";
import { WESTERN_TRAILS } from "./westernTrails";

/** Authored tradition trails that are not on the essential spine. */
export const LIVING_TRAILS: LearningTrack[] = [
  {
    id: "seer-in-its-nature",
    title: "The Seer in Its Nature",
    level: "Beginner",
    focus: "Patañjali: still the turnings, rest as the seer",
    outcome:
      "Know yoga as the stilling of mind's fluctuations, train practice and dispassion, walk the eight limbs as one discipline, and recognize kaivalya as the seer no longer confused with what it sees.",
    description:
      "A six-gate walk through the Yoga Sūtras: definition, means, friendliness, kriyā, the eight limbs, and release.",
    arc:
      "We begin with the opening definition — yoga is the stilling of the mind's turnings, after which the seer rests in its own nature. Then we take up the two wings, practice and dispassion. We stabilize the heart with friendliness, compassion, joy, and equanimity. Kriyā-yoga gives the heat of daily work. The eight limbs show that posture is only one joint of a longer body. We end where Patañjali ends: the seer standing free of identification with what appears.",
    estimatedSessions: "6 gates · ~20 min each",
    steps: [
      {
        id: "ys-now-the-teaching",
        title: "Now the teaching of yoga",
        orientation:
          "Every yoga that is not this opening is a later decoration. We start where Patañjali starts.",
        teaching:
          "Atha yogānuśāsanam — now, the teaching. The 'now' is not a date. It is the moment the mind is ready to be instructed rather than entertained. Yoga is then defined with a single mechanism: the stilling of cittavṛtti, the mind's turnings. When those turnings quiet, the seer (draṣṭṛ) abides in its own nature. Otherwise it takes the form of whatever is turning. The claim is diagnostic: you already are the seer; you have been wearing the weather of thought as if it were your face.",
        keyIdea: "Yoga is the stilling of the mind's turnings. Then the seer rests as itself.",
        misconception:
          "That yoga begins with a posture, or that stilling means making the mind blank and useless.",
        passageId: "patañjali_yoga_sūtras.ys_1_01_04",
        supportingPassageIds: ["siva_sutra.ss_i_1"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Help me hear these four sūtras as a diagnosis, not a slogan. What is the difference between stilling the turnings and suppressing thought?",
        practice:
          "Sit for four minutes. Each time a thought dresses itself as you, name it silently: turning. Do not fight it. Watch it lose the costume. Rest one breath as the one who saw it.",
        journalPrompt:
          "Where today did I take a turning of mind as my face? What remained when I stopped wearing it?",
        integration:
          "You can tell, in a live moment, the difference between a thought and the seer that knows it.",
      },
      {
        id: "ys-practice-and-dispassion",
        title: "Practice and dispassion",
        orientation:
          "The definition is useless without the two wings that make stilling possible.",
        teaching:
          "Abhyāsa is the effort to stay. Vairāgya is the release of the thirst that keeps restarting the turnings. Patañjali pairs them because either alone fails: practice without dispassion becomes grim striving; dispassion without practice becomes a mood. The mind stills when you return, again, and when you stop feeding the return with craving for a particular result — including the result of being a successful yogin.",
        keyIdea: "Stay, and stop feeding the thirst that restarts the mind.",
        misconception:
          "That dispassion means not caring, or that practice means forcing the mind into silence.",
        passageId: "patañjali_yoga_sūtras.ys_1_12_16",
        supportingPassageIds: ["bhagavad_gita.bg_02_47"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Give me a concrete way to pair abhyāsa and vairāgya today. Where do people turn dispassion into coldness?",
        practice:
          "Choose one recurring pull — a refresh, a score, a replay. Each time it arises, return the body to the next ordinary task (abhyāsa) and set the fruit down (vairāgya). Do this for one hour of the day.",
        journalPrompt:
          "Which wing is weaker in me today — the staying, or the release of thirst?",
        integration:
          "You can name both wings in a real craving, and use both, not just the one you prefer.",
      },
      {
        id: "ys-four-immeasurables",
        title: "Stabilize the heart first",
        orientation:
          "Before finer concentrations, Patañjali clears the social weather of the mind.",
        teaching:
          "Friendliness toward the happy, compassion toward the suffering, joy toward the virtuous, equanimity toward the unvirtuous — these four are not manners. They are a way of stopping the mind from contracting around other people's weather. A mind that is jealous of joy, recoiling from pain, cynical toward goodness, or inflamed by harm cannot still. The heart is trained first so the seer is not hijacked by comparison.",
        keyIdea: "Clear the heart's contractions around others, or concentration will only concentrate them.",
        misconception:
          "That this is optional ethics after the 'real' yoga of sitting.",
        passageId: "patañjali_yoga_sūtras.ys_1_33_39",
        supportingPassageIds: ["shantideva_bodhicaryavatara.bca_06_01"],
        theme: "compassion",
        chatMode: "practice",
        chatPrompt:
          "Walk me through the four attitudes with one living person in each. Where does equanimity get mistaken for indifference?",
        practice:
          "Name one person you envy, one who is in pain, one whose goodness you discount, one who has harmed. Offer the matching attitude for three breaths each. Notice the body loosen or refuse.",
        journalPrompt:
          "Which of the four attitudes is hardest, and what does that refusal protect?",
        integration:
          "You can catch a contraction around another person and apply the matching attitude before it becomes a story.",
      },
      {
        id: "ys-kriya-yoga",
        title: "The heat of daily work",
        orientation:
          "Book II opens with a yoga you can do in an ordinary life: heat, study, surrender.",
        teaching:
          "Kriyā-yoga is tapas (the heat of disciplined action), svādhyāya (study of what you actually are), and īśvara-praṇidhāna (the offering of the work). This is not a lesser yoga for householders. It is how the kleśas — the afflictions that keep the mind turning — are thinned in the middle of a day. Heat without study is grim; study without offering becomes self-improvement; offering without heat is a wish.",
        keyIdea: "Thin the afflictions by heat, self-study, and offering the work.",
        misconception:
          "That kriyā-yoga is a beginner's substitute for 'real' samādhi.",
        passageId: "patañjali_yoga_sūtras.ys_2_01_02",
        supportingPassageIds: ["bhagavad_gita.bg_02_47"],
        theme: "action",
        chatMode: "explain",
        chatPrompt:
          "How do tapas, svādhyāya, and offering work together on a single affliction? Give me one example from ordinary work.",
        practice:
          "Pick one difficult task. Do it a little more cleanly than habit (tapas). Midway, ask what in you is actually at work (svādhyāya). At the end, offer the result without claiming it.",
        journalPrompt:
          "Which affliction did today's work thin — and which one did I feed?",
        integration:
          "You can run heat, study, and offering through one ordinary task without turning it into a performance.",
      },
      {
        id: "ys-eight-limbs",
        title: "Eight limbs, one body",
        orientation:
          "The famous list is not a ladder of prestige. It is one organism.",
        teaching:
          "Yama, niyama, āsana, prāṇāyama, pratyāhāra, dhāraṇā, dhyāna, samādhi — eight limbs of one yoga. Posture is the third limb, not the whole animal. The restraints and observances are how the seer stops leaking into harm. Breath and withdrawal gather the senses. Concentration, meditation, and absorption are the same attention ripening. If you skip the first limbs, the later ones concentrate your unreadiness.",
        keyIdea: "The eight limbs are one body. Posture is a joint, not the creature.",
        misconception:
          "That āsana is yoga, or that the later limbs can be reached by skipping how you treat people.",
        passageId: "patañjali_yoga_sūtras.ys_2_28_29",
        supportingPassageIds: ["patañjali_yoga_sūtras.ys_2_46_48"],
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Show me how the eight limbs are one organism, not a ladder. Where is my practice overdeveloped in one limb and starved in another?",
        practice:
          "Today, do not add a new pose. Keep one yama (non-harm, or truthfulness) through a single conversation, and one seated minute of staying. Feel them as the same yoga.",
        journalPrompt:
          "Which limb am I using as a substitute for the ones I avoid?",
        integration:
          "You can describe your practice as a body of limbs, and name the starved one without shame.",
      },
      {
        id: "ys-kaivalya",
        title: "The seer standing free",
        orientation:
          "The path ends not in a better personality but in the end of mistaken identity.",
        teaching:
          "When the covering of impurity thins, knowledge becomes infinite and little remains to be known. The gunas, having served their purpose, retire. The seer stands in its own form — kaivalya, aloneness, not isolation. This is not a reward after death. It is what was true at sūtra 1.3, now no longer intermittent. You do not become the seer. You stop confusing it with what it sees.",
        keyIdea: "Kaivalya is the seer no longer mistaken for the seen.",
        misconception:
          "That liberation is a blank void, or a special self that has finally won.",
        passageId: "patañjali_yoga_sūtras.ys_4_31_34",
        supportingPassageIds: ["patañjali_yoga_sūtras.ys_1_01_04"],
        theme: "self",
        chatMode: "explain",
        chatPrompt:
          "Help me hear kaivalya as the end of mistaken identity, not as a trophy. How does this complete the opening four sūtras?",
        practice:
          "Sit five minutes. When a thought, sensation, or role appears, let it be seen. Do not improve it. Rest as the seeing. At the end, do not congratulate a new self — notice there was never a second one to congratulate.",
        journalPrompt:
          "What identity was I still trying to liberate, instead of seeing through?",
        integration:
          "You can rest, briefly, as the seer without turning that rest into a new achievement.",
      },
    ],
  },
  {
    id: "emptiness-and-compassion",
    title: "Emptiness and Compassion",
    level: "Beginner",
    focus: "Buddhism: mind precedes, emptiness is form, compassion walks",
    outcome:
      "See that mind precedes the world you inhabit, that form is emptiness without a second realm, that dependent arising is that emptiness, and that compassion is how a groundless life still cares.",
    description:
      "A six-gate walk from the Dhammapada through the Heart Sūtra, Nāgārjuna, Śāntideva, and Dōgen.",
    arc:
      "We begin where the Dhammapada begins: mind precedes all things. Then the Heart Sūtra refuses both a solid world and a better void behind it. Nāgārjuna gives the argument — emptiness is dependent arising. Śāntideva turns that insight into bodhicitta and patience. Dōgen will not let practice and realization sit on opposite sides of a river.",
    estimatedSessions: "6 gates · ~20 min each",
    steps: [
      {
        id: "bd-mind-precedes",
        title: "Mind precedes all things",
        orientation:
          "Before emptiness, see the more ordinary fact: the world you inhabit is led by mind.",
        teaching:
          "The Dhammapada opens with a claim you can test before noon: mind is forerunner. Speak or act from a corrupted mind and dukkha follows like a wheel after the ox. Speak or act from a clear mind and ease follows like a shadow. This is not optimism. It is causal. The first work is not metaphysics. It is noticing that the tone of mind is already writing the next hour.",
        keyIdea: "Mind leads. The world you meet is already shaped by how you meet it.",
        misconception:
          "That this means the outer world is imaginary, or that thinking happy thoughts erases harm.",
        passageId: "dhammapada.dhp_ch01",
        supportingPassageIds: ["patañjali_yoga_sūtras.ys_1_01_04"],
        theme: "mind",
        chatMode: "practice",
        chatPrompt:
          "Help me test 'mind precedes' on one event today without sliding into magical thinking.",
        practice:
          "Before the next difficult conversation or message, pause for three breaths and name the tone of mind you are about to send ahead of you. Change the tone, not the script, if it is already corrupted.",
        journalPrompt:
          "Where did a corrupted mind write the hour before the facts did?",
        integration:
          "You can feel mind going ahead of an action, and choose the tone you send first.",
      },
      {
        id: "bd-form-is-emptiness",
        title: "Form is emptiness, emptiness is form",
        orientation:
          "Now the sūtra refuses both a solid world and a better void behind it.",
        teaching:
          "The Heart Sūtra's claim is an identity, not a ranking. Emptiness is not hiding behind form, and form is not a consolation prize. What we call form simply is emptiness; what we call emptiness simply is form — and the same for feeling, perception, formations, consciousness. If you hear only 'form is empty,' you still have a second realm to flee into. The second half closes the escape.",
        keyIdea: "Emptiness is not elsewhere. It is this, unclenched.",
        misconception:
          "That emptiness is a blank behind the world, or that form is a lie to be discarded.",
        passageId: "heart_sutra.hs_001",
        supportingPassageIds: ["nagarjuna_mulamadhyamakakarika.mmk_24_18"],
        theme: "emptiness",
        chatMode: "explain",
        chatPrompt:
          "Why does the sūtra need both halves — form is emptiness, and emptiness is form? Where do I still keep a second realm?",
        practice:
          "Choose one solid-seeming object and one solid-seeming feeling. For each, say: this is form, and this is emptiness — not two. Do not make either disappear. Notice the grip open by a fraction.",
        journalPrompt:
          "Where did I use emptiness as an escape from a form I did not want to feel?",
        integration:
          "You can hold a form without making it a thing, and hold emptiness without making it a place.",
      },
      {
        id: "bd-dependent-arising",
        title: "Emptiness is dependent arising",
        orientation:
          "Nāgārjuna supplies the argument for which the sūtra gave the slogan.",
        teaching:
          "Whatever is dependently arisen, that is emptiness. That is dependent designation; that itself is the middle way. Emptiness is not a substance called nothing. It is the fact that nothing stands on its own — not the self, not the teaching, not even emptiness. If things had essences they could not arise, change, or cease. Because they are empty, the path is possible.",
        keyIdea: "Emptiness is how things arise together — not a hole behind them.",
        misconception:
          "That emptiness annihilates the world, or that dependent arising is just a chain of billiard-ball causes.",
        passageId: "nagarjuna_mulamadhyamakakarika.mmk_24_18",
        supportingPassageIds: ["heart_sutra.hs_001"],
        theme: "emptiness",
        chatMode: "explain",
        chatPrompt:
          "Show me how emptiness and dependent arising are the same claim. What goes wrong if I take emptiness as a thing?",
        practice:
          "Take one irritation. Name three conditions without which it could not have arisen (sleep, a sentence, a history). Feel it lose its essence. Act from that, not from a solid enemy.",
        journalPrompt:
          "What irritation today lost its 'itself' when I named the conditions?",
        integration:
          "You can point to emptiness as dependent arising in a live feeling, not as a theory.",
      },
      {
        id: "bd-bodhicitta",
        title: "The mind that does not turn away",
        orientation:
          "Insight without the vow to stay with beings becomes another escape.",
        teaching:
          "Śāntideva's bodhicitta is the mind that wishes awakening for the sake of others, and then becomes that work. Emptiness does not cancel care. Because no one stands alone, your suffering is already shared, and so is the work of ending it. The vow is not a mood of niceness. It is the refusal to use emptiness as a private exit.",
        keyIdea: "Because nothing stands alone, compassion is not optional ethics. It is accurate.",
        misconception:
          "That compassion is a later add-on to emptiness, or that bodhicitta means fixing everyone.",
        passageId: "shantideva_bodhicaryavatara.bca_03_06",
        supportingPassageIds: ["shantideva_bodhicaryavatara.bca_01_15"],
        theme: "compassion",
        chatMode: "practice",
        chatPrompt:
          "How does emptiness make compassion more precise rather than more vague? Give me one vow I can keep today.",
        practice:
          "Before one ordinary help — a reply, a meal, a listening — say silently: this is not mine alone. Do the act without advertising it to yourself as virtue.",
        journalPrompt:
          "Where did I use insight as an exit from someone else's pain?",
        integration:
          "You can let emptiness make you more available, not less.",
      },
      {
        id: "bd-patience",
        title: "Patience with the fire",
        orientation:
          "The vow meets anger. This is where most paths quietly end.",
        teaching:
          "Śāntideva treats anger as the one fire that burns the forest of merit. Patience is not stuffing the feeling. It is staying with the heat without handing the next action to it. If the last gate said compassion is accurate, this gate asks whether you can stay accurate when someone is wrong, late, or sharp. Emptiness here means the insult has no essence solid enough to deserve your whole mind.",
        keyIdea: "Patience is compassion under heat — not a frozen face.",
        misconception:
          "That patience means letting harm continue, or that anger is more honest than care.",
        passageId: "shantideva_bodhicaryavatara.bca_06_01",
        supportingPassageIds: ["dhammapada.dhp_ch01"],
        theme: "compassion",
        chatMode: "practice",
        chatPrompt:
          "Help me practice patience without becoming a doormat. What does Śāntideva actually ask me to do with the heat?",
        practice:
          "The next time heat rises, feel it in the body for ten breaths before speech. Ask: is there a next action that is still accurate? If not, wait.",
        journalPrompt:
          "When did I hand the next sentence to anger, and what would patience have said instead?",
        integration:
          "You can stay with anger's heat long enough to choose an action that is not the fire itself.",
      },
      {
        id: "bd-practice-enlightenment",
        title: "Practice is already the thing",
        orientation:
          "Dōgen will not let you keep realization on the far shore of practice.",
        teaching:
          "When all dharmas are the Buddha-dharma, there is delusion and realization, practice, birth and death. When the myriad dharmas are without self, there is no delusion, no realization. The Buddha Way leaps beyond abundance and lack — and still flowers fall though we love them, weeds grow though we hate them. Practice is not a bridge to a later enlightenment. Sitting, walking, the falling flower, are already the thing you were postponing.",
        keyIdea: "Do not postpone the Way to a later self. This act is it — including the falling.",
        misconception:
          "That practice earns a later reward, or that 'already enlightened' means you can stop sitting.",
        passageId: "dōgen_shōbōgenzō.dog_001",
        supportingPassageIds: ["heart_sutra.hs_001"],
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Help me hear Dōgen without turning 'practice is enlightenment' into an excuse to stop, or into a prize for sitting.",
        practice:
          "Do one ordinary act — washing, walking, closing a door — as if it were not a means. When you catch yourself waiting for a better state, return to the act.",
        journalPrompt:
          "Where am I still postponing the Way to a later, more qualified self?",
        integration:
          "You can do one act without using it as a bridge to a later awakening.",
      },
    ],
  },
  {
    id: "the-horse-of-conversation",
    title: "The Horse of Conversation",
    level: "Beginner",
    focus: "Yoruba òwe: wisdom that travels by speech",
    outcome:
      "Hear a proverb as a vehicle, not a slogan: secrecy, peace, wisdom, inquiry, charity, and the dawn that does not come twice.",
    description:
      "Six òwe from the Yoruba house — living speech that carries a teaching across a day.",
    arc:
      "Òwe is 'the horse of conversation': a short saying that carries you farther than argument. We begin with what is hidden, then peace as the father of friendship, wisdom that is not inherited, the inquiry that saves a mistake, charity as the father of sacrifice, and the dawn that will not wake you twice.",
    estimatedSessions: "6 gates · ~15 min each",
    steps: [
      {
        id: "yw-what-is-hidden",
        title: "What is done in secret",
        orientation:
          "The first òwe names a law of shame before it moralizes.",
        teaching:
          "What is not wished to be known is done in secret. The proverb does not yet judge the hidden act. It describes a mechanics: concealment follows the wish not to be seen. Before you improve yourself, see the link. The secret is already teaching you what you believe would cost you face, love, or standing.",
        keyIdea: "Secrecy is a map of what you fear being known.",
        misconception:
          "That all secrecy is vice, or that the proverb is only about other people's hypocrisy.",
        passageId: "yoruba_proverbs.yoruba_proverbs_001",
        supportingPassageIds: ["dhammapada.dhp_ch01"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Help me use this proverb as a diagnosis of secrecy, not as a whip. What is the difference between privacy and concealment?",
        practice:
          "Notice one small thing you hesitate to speak. Without confessing it, ask: what am I afraid will be known? Let the secrecy itself be information.",
        journalPrompt:
          "What does one secret of mine reveal about what I think would be lost if it were seen?",
        integration:
          "You can tell secrecy from privacy, and let a secret teach you what you are protecting.",
      },
      {
        id: "yw-peace-father",
        title: "Peace is the father of friendship",
        orientation:
          "From the hidden self to the social field: friendship has a parent.",
        teaching:
          "Peace is the father of friendship. The proverb reverses the usual order. We often try to make friends in order to get peace. Here peace comes first — a settled field — and friendship is what that field can bear. Without peace, what we call friendship is an alliance against unrest.",
        keyIdea: "Friendship grows from peace, not the other way around.",
        misconception:
          "That peace means agreement, or that friendship can be forced by loyalty talk.",
        passageId: "yoruba_proverbs.yoruba_proverbs_017",
        supportingPassageIds: ["shantideva_bodhicaryavatara.bca_06_01"],
        theme: "compassion",
        chatMode: "explain",
        chatPrompt:
          "How is peace the father of friendship rather than its reward? Where do I try to befriend in order to quiet unrest?",
        practice:
          "Before you next seek company or send a message to 'make it okay,' spend two minutes settling the body. Then speak from that, or wait.",
        journalPrompt:
          "Which friendship of mine is actually an alliance against unrest?",
        integration:
          "You can feel when you are using a person to buy peace, and stop.",
      },
      {
        id: "yw-wisdom-not-born",
        title: "Wisdom is not inherited",
        orientation:
          "Fortune can arrive at birth. Wisdom cannot.",
        teaching:
          "A man may be born to a fortune, but wisdom comes only from learning. The proverb cuts a confusion common to every house of privilege and every spiritual scene: inheritance is not insight. You can be given texts, teachers, and ease, and still not have learned. Wisdom is the one wealth that refuses to be bequeathed.",
        keyIdea: "Fortune can be given. Wisdom has to be learned.",
        misconception:
          "That long study, or a famous lineage, is already wisdom.",
        passageId: "yoruba_proverbs.yoruba_proverbs_038",
        supportingPassageIds: ["patañjali_yoga_sūtras.ys_1_12_16"],
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Where do I treat inherited language — family, school, lineage — as if it were already wisdom?",
        practice:
          "Take one sentence you repeat because it was given to you. Ask whether you have learned it. If not, sit with the not-knowing rather than reciting.",
        journalPrompt:
          "What fortune of speech have I been spending as if it were my own insight?",
        integration:
          "You can tell a received sentence from a learned one, and refuse to spend the first as the second.",
      },
      {
        id: "yw-inquiry-saves",
        title: "Inquiry saves the mistake",
        orientation:
          "Wisdom now becomes a method: ask before you act.",
        teaching:
          "Inquiry saves a man from making mistakes. The proverb is not praise of curiosity as a personality. It is a brake. The mistake is often already loaded; inquiry is the pause that unloads it. Shame after error is cheaper than the question before it — and more expensive in the end.",
        keyIdea: "Ask first. The mistake is usually the act that skipped the question.",
        misconception:
          "That inquiry means endless hesitation, or that a decisive person does not ask.",
        passageId: "yoruba_proverbs.yoruba_proverbs_049",
        supportingPassageIds: ["epictetus_works.epi_enc_001"],
        theme: "action",
        chatMode: "practice",
        chatPrompt:
          "Give me a one-question inquiry I can run before a decision today without becoming timid.",
        practice:
          "Before one decision that usually goes on rails, ask one living question of someone who knows, or of the situation itself. Wait for the answer.",
        journalPrompt:
          "Which recent mistake was an unasked question?",
        integration:
          "You can insert one real question before an habitual act.",
      },
      {
        id: "yw-charity-father",
        title: "Charity is the father of sacrifice",
        orientation:
          "Giving has a parent too. Sacrifice without charity is display.",
        teaching:
          "Charity is the father of sacrifice. The large offering is born from the smaller, daily willingness to let something go toward another. If you skip charity and jump to sacrifice, you get theater: a costly gesture that has not learned to give. The proverb restores the order — learn to release in small, then the large gift is not a performance.",
        keyIdea: "Sacrifice that never practiced charity is a show.",
        misconception:
          "That a grand gesture proves a generous heart.",
        passageId: "yoruba_proverbs.yoruba_proverbs_052",
        supportingPassageIds: ["shantideva_bodhicaryavatara.bca_03_06"],
        theme: "compassion",
        chatMode: "practice",
        chatPrompt:
          "How do I tell charity from sacrificial theater? What small release would father a truer gift?",
        practice:
          "Make one small, unadvertised gift of time, attention, or goods. Do not tell the story of it, including to yourself.",
        journalPrompt:
          "Where have I offered a large gesture instead of a small, real release?",
        integration:
          "You can give something small without turning it into a portrait of yourself.",
      },
      {
        id: "yw-dawn-once",
        title: "The dawn does not come twice",
        orientation:
          "The last òwe is about time: this waking is the one you have.",
        teaching:
          "The dawn does not come twice to wake a man. The proverb is not a hustle slogan. It is a fact about occasions. A teaching, a person, a chance to ask, a chance to repair — some openings do not re-open in the same shape. The work is not panic. It is answering the dawn that is here, instead of waiting for a more convenient morning.",
        keyIdea: "This opening will not wake you in the same way again.",
        misconception:
          "That every missed chance is final, or that urgency is the same as presence.",
        passageId: "yoruba_proverbs.yoruba_proverbs_071",
        supportingPassageIds: ["dōgen_shōbōgenzō.dog_001"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me hear this proverb as presence, not as panic. What dawn is here today that will not come in this shape again?",
        practice:
          "Name one opening that is actually here — a conversation, a gate, a repair. Do the first honest step before the day dilutes it.",
        journalPrompt:
          "What dawn did I miss by waiting for a better morning — and what dawn is still here?",
        integration:
          "You can answer one present opening without turning the proverb into self-punishment.",
      },
    ],
  },
  {
    id: "the-sacred-tremor",
    title: "The Sacred Tremor",
    level: "Intermediate",
    focus: "Spandakārikā: vibration as method, not a second recognition",
    outcome:
      "Feel opening and closing in this awareness; test the pulse in an ordinary blockage; let agitation dissolve without a purification project; tell the binding surge from the tremor; discern the pulse in waking; locate it in a spike; catch what escaped attention; inhabit arising and dissolving without becoming their puppet.",
    description:
      "An eight-gate method-walk through the Spandakārikā — the pulse itself, not another identity-claim.",
    arc:
      "Recognition already named what you are. Here the work is kinetic. The world is a pulse of eyelids — unmeṣa and nimeṣa in this looking. There is no obstruction anywhere; a wall is a contraction of attention. Effort cannot purify the pulse. The same tremor binds when you ride only the outward phase and call excitement awakening. Method is fieriness toward the vibration in ordinary waking, including anger, joy, and the running body. Catch what escaped. Fruition is inhabiting arising and dissolving — not a new self called lord, and not a restatement of you are Śiva.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "sp-opening-closing",
        title: "Opening and closing of the eyes",
        orientation:
          "If unmeṣa-nimeṣa remain a story about Śakti's eyes in the sky, later fieriness is just enthusiasm.",
        teaching:
          "Through whose opening and closing of the eyes the world's dissolution and arising occur — that source we praise. This is not a blink metaphor and not a cosmology to admire. Unmeṣa is the outward unfurling of appearance; nimeṣa is the inward reabsorption. They are not sequential events on a timeline. They are the intrinsic breathing of awareness. The Śiva Sūtra names the surge as Bhairava — an identity. Here you do not conclude the name. You notice the pulse: something appearing, something withdrawing, in this looking. The path is not transcendence of the world. It is attending to the world-making tremor as it is already doing this.",
        keyIdea: "Feel the turn between appearing and withdrawing. Do not name it Śiva.",
        misconception:
          "That creation and dissolution are cosmic events out there, or that the eyelids are only a pretty metaphor.",
        passageId: "yoga_spandakarika.sp_01",
        supportingPassageIds: ["siva_sutra.ss_i_5"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Do not conclude that I am Śiva. Model the pulse: opening and closing already happening. Help me feel unmeṣa-nimeṣa in this awareness, not as a cosmic story out there.",
        practice:
          "Sit five minutes with ordinary breath. At each turn between in and out, notice appearing and withdrawing before you name anything. Do not congratulate a recognition. Just keep the pulse in view.",
        journalPrompt:
          "Where am I still watching creation happen somewhere else?",
        integration:
          "You can feel unmeṣa-nimeṣa in this awareness, not only as a story about the cosmos.",
      },
      {
        id: "sp-no-obstruction",
        title: "No obstruction anywhere",
        orientation:
          "After the eyelids, the mind looks for a special place where vibration lives. The kārikā refuses a hidden ground.",
        teaching:
          "That in which every effect abides and from which it emerges — because its nature is uncovered, there is no obstruction anywhere. Spanda is not a gem behind the world. Unlike a ground you reach by negating appearance, the pulse remains transparent as the creative pulsation itself. Obstruction is never a rupture in the tremor. It is a contraction of attention. The method is not to travel to an uncovered zone. It is to test the claim here: in this thought, this wall, this boredom — is the pulse missing, or have you stopped feeling for it?",
        keyIdea: "A blockage is a mood of attention, not a hole in the tremor.",
        misconception:
          "That the pulse is hidden behind manifestation, or that you must get to a special place to feel it.",
        passageId: "yoga_spandakarika.sp_02",
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Do not send me to a special uncovered place. Help me test the pulse in an ordinary blockage. What am I still treating as a place the tremor cannot reach?",
        practice:
          "Pick one apparent obstruction today — a stuck thought, a tense jaw, a closed door. Ask once: is the pulse absent here, or am I contracted? Do not fix the obstruction. Feel for continuity through it for one minute.",
        journalPrompt:
          "What am I still treating as a place the pulse cannot reach?",
        integration:
          "You can catch the hunt for a special uncovered place, and test the pulse in an ordinary blockage.",
      },
      {
        id: "sp-agitation-dissolves",
        title: "When agitation dissolves",
        orientation:
          "The ego now tries to produce the pulse by purifying itself. Verse 8 inverts that project.",
        teaching:
          "When the agitation of one who cannot purify himself by effort, and who still wants actions, dissolves — then the supreme state. This is not a blank mind and not a prize for discipline. Kṣobha is the dualistic ripple, the oscillation of doing and desiring. The verse diagnoses the futility of volitional self-purification. It does not counsel laziness. It says: the tremor you would earn is already the ground under the earning. When the false effort collapses, what remains is not void. It is the pulse prior to agitation. Do not turn stop-purifying into a new purification.",
        keyIdea: "Let agitation subside. Do not improve yourself into the supreme state.",
        misconception:
          "That you manufacture the supreme state by purifying yourself, or that a blank mind is the goal.",
        passageId: "yoga_spandakarika.sp_08",
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Refuse the self-improvement reading. Model unveiling after agitation, not a better self. What purification project am I still running as if it could manufacture the tremor?",
        practice:
          "Name one purification project running today — a better self, a cleaner mood, a holier record. Set it down for twenty minutes. Let agitation be felt until it lessens without your help. Do not score the lessening.",
        journalPrompt:
          "What purification project am I still running as if it could manufacture the tremor?",
        integration:
          "You can tell unveiling after kṣobha from a self-improvement program that borrowed the word pulse.",
      },
      {
        id: "sp-same-pulse-binds",
        title: "The same pulse binds",
        orientation:
          "This gate keeps Spanda from becoming recognition in other clothes, and from becoming a cult of excitement.",
        teaching:
          "The vibration that is the ground of liberation is also how the unawakened get lost. They do not lack spanda. They identify with the outward-moving phase — unmeṣa toward objects — and miss the inward turn that would show the pulse as their own looking. Cyclic existence is not imposed from outside. It is this mis-taking of the surge. So: excitement is not the method. Mood is not the tremor. Suppressing the pulse is also not the method. Attend to both phases. The bind is riding only the going-out and calling it life.",
        keyIdea: "Bondage is not lack of vibration. It is riding only the outward phase.",
        misconception:
          "That bondage is lack of spanda, or that excitement and enthusiasm are awakening.",
        passageId: "yoga_spandakarika.sp_20",
        supportingPassageIds: ["yoga_spandakarika.sp_19"],
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Do not let me treat surge as awakening. Model both phases. Where am I still taking mood or enthusiasm as proof of the tremor?",
        practice:
          "At the next craving, anger, or spiritual high, silently mark: outward phase. Do not act on the story for ninety seconds. Feel whether any inward return is already happening. Do not congratulate a mood.",
        journalPrompt:
          "Where am I still taking surge, mood, or enthusiasm as proof of awakening?",
        integration:
          "You can tell the binding surge from the pulse, and stop treating excitement as awakening.",
      },
      {
        id: "sp-fieriness",
        title: "Fieriness toward the tremor",
        orientation:
          "After the bind is named, the text gives the act: constant discernment of the vibration in waking.",
        teaching:
          "Therefore one constantly engaged in discerning the reality of the vibration attains one's own nature even in waking, without delay. Fieriness here is not frenzy. It is sustained turning of attention toward the throb that is already the ground of knowing. The waking state is singled out because the world looks most solid there. You do not need another state. You need the discernment that the solid-looking world is pulsing. Do not hold I am That as a souvenir from another path. Discern the tremor in this walking, this washing, this sentence.",
        keyIdea: "Discern now, in waking. A stored conclusion is not the method.",
        misconception:
          "That the pulse is for the cushion, or that holding an identity-claim is the same as discerning the tremor.",
        passageId: "yoga_spandakarika.sp_21",
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Do not let me postpone this to meditation or cash it in as I am That. Model fieriness as discernment in waking. Where am I still saving the pulse for the cushion?",
        practice:
          "Choose one ordinary waking hour. Each time you remember, return attention to the subtle throb in the body-mind — not a trance, not a slogan. When you forget, return. Count no states.",
        journalPrompt:
          "Where am I still saving the pulse for the cushion, or holding a conclusion instead of discerning?",
        integration:
          "You can discern the tremor in ordinary waking, without postponing it to meditation or to an identity-claim.",
      },
      {
        id: "sp-anger-joy-running",
        title: "Anger, joy, the running body",
        orientation:
          "Fieriness now has to survive weather. Whatever state one reaches, there the vibration is established.",
        teaching:
          "Whether in extreme anger, intense joy, the deliberating mind, or running — whatever state one reaches, there the vibration is established. The verse does not prescribe a state to cultivate. It forbids postponement. Spanda is not confined to absorption. The hinge of opening and closing operates in the spike. Practice that only works when you are settled is not this method. Practice that hunts anger and rapture for a thrill is also not this method. At the state you are already in, locate the tremor. That is the instruction.",
        keyIdea: "This state. Not a better one. Locate the pulse without riding the story.",
        misconception:
          "That practice waits for calm, or that hunting intensity is the path.",
        passageId: "yoga_spandakarika.sp_22",
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Do not wait for calm and do not hunt spikes. Model locating the tremor in the state I am already in. Am I postponing practice, or chasing intensity as if it were the method?",
        practice:
          "At the next spike — anger, joy, hurry, or the scramble of what shall I do — pause inside it. Locate the vibration in the body. Do not finish the story for ten breaths. Then complete the next necessary action at ordinary speed.",
        journalPrompt:
          "Am I still waiting for a calm state to practice — or chasing intensity as if it were the path?",
        integration:
          "You can find the tremor in a spike without waiting for calm and without collecting intensity.",
      },
      {
        id: "sp-catch-what-escaped",
        title: "Catch what escaped",
        orientation:
          "Extremes can still make the pulse seem like a special object. The method is looking again at what you missed.",
        teaching:
          "Just as an object that escaped attention is more clearly perceived when you make the effort to see it better from all angles, so the tremor appears when you ardently strive toward it. That which exists, in whatever manner and wherever, through whatever means — when one seizes that very power in that very way, it is not long before it unfolds. You do not construct a new state. You align with the potency already operating as looking, in the manner it already is. Staring at a thing called spanda is how you lose it. Looking again at what you missed is how you catch it.",
        keyIdea: "Look again. The power is seized in the way it already exists.",
        misconception:
          "That the pulse is a special object you could stare at, miss, or possess.",
        passageId: "yoga_spandakarika.sp_36",
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Do not let me stare at a thing called vibration. Model looking again at what escaped. What did I miss that is already the manner of the power?",
        practice:
          "Name one thing that escaped attention today — a person's tone, a bodily signal, a word you spoke. Look again from another angle for two minutes. That second look is the method. Do not hunt a mystical object behind it.",
        journalPrompt:
          "Am I still staring at the pulse as an object I could miss or possess?",
        integration:
          "You can catch the pulse by looking again at what you missed, not by staring at a thing called vibration.",
      },
      {
        id: "sp-lord-of-the-wheel",
        title: "Lord of the wheel",
        orientation:
          "Fruition is inhabiting arising and dissolving — not occult control, and not a second I am Śiva.",
        teaching:
          "When one is firmly established in that one reality, then by bringing dissolution and arising under measure, one attains the status of experiencer, and thereby becomes lord of the wheel. This is not annihilating the cosmic rhythm and not a magician's grip on other people. It is ceasing to be the puppet of laya-udaya. Thoughts still arise and dissolve. You inhabit the rhythm instead of being thrown by it. Pratyabhijñā will say the universe is the body of Śiva — a recognition conclusion. Here the instruction remains kinetic: stay established in the tremor until manifestation and return are no longer an accident that befalls you. Do not collect lordship as a new self.",
        keyIdea: "Inhabit the rhythm. Do not become a character who owns it.",
        misconception:
          "That fruition means controlling the world, or that this gate restates you are Śiva.",
        passageId: "yoga_spandakarika.sp_51",
        supportingPassageIds: ["pratyabhijnahrdayam.phr_020"],
        theme: "freedom",
        chatMode: "compare",
        chatPrompt:
          "Keep this kinetic. Do not let me cash it in as I am Śiva or as occult control. Help me inhabit arising and dissolving without becoming a new character called lord. Where am I still waiting for the rhythm to happen to me?",
        practice:
          "Sit five minutes and watch one thought arise and dissolve without being thrown into its story. When the body wants to become the lord of the thought, return to the pulse. Then stand and do one ordinary action at the speed of that watching.",
        journalPrompt:
          "Am I still waiting for the rhythm to happen to me — or hoping to become someone who controls it?",
        integration:
          "You can inhabit arising and dissolving without being their puppet and without a new identity called lord.",
      },
    ],
  },
  ...LINEAGE_TRAILS,
  ...WESTERN_TRAILS,
  ...DEEPENING_TRAILS,
];
