import type { LearningTrack } from "../../learningPaths";

/** Confucian cultivation — rén at hand, then the Mean. Not a second Stoic handbook. */
export const HUMANENESS_AT_HAND: LearningTrack = {
  id: "humaneness-at-hand",
  title: "Humaneness at Hand",
  level: "Beginner",
  focus: "Confucian: rén as trained reciprocity; the Mean as equilibrium, not mediocrity",
  outcome:
    "Learn with joy rather than grim self-improvement; examine three relations daily; return to li instead of a mood called kindness; keep zhong and shu as one thread; reverse one action you would not welcome; rectify one name you have been using loosely; follow nature as a path that cannot be left; catch equilibrium before pleasure and anger dress as the whole of you.",
  description:
    "An eight-gate walk through the Analects and the Zhōngyōng: cultivation in the near, not a metaphysics of the Self.",
  arc:
    "Virtue is not remote. We begin where the Analects begin: learning that is pleasant when timed, not grim. Zeng's three daily exams make the craft domestic. Yan Yuan is told that rén is to subdue the self and return to li — not a warmer feeling. One thread runs through: zhong inward, shu outward. Shu is then the one word you could practice for a life. Names must be correct or the room cannot move. Heaven confers nature; accordance with it is the Way. Last: before pleasure and anger arise, the Mean is equilibrium; when they arise in due degree, harmony. This is not the Kashmiri gap. It is civic and ordinary — a balance you keep in a room.",
  estimatedSessions: "8 gates · ~20 min each",
  steps: [
    {
      id: "cf-learn-joy",
      title: "Is it not pleasant to learn",
      orientation:
        "If cultivation begins as grim self-improvement, later rén becomes a performance. Confucius opens with timed joy.",
      teaching:
        "Is it not pleasant to learn with constant perseverance and to apply it in due season? Is it not delightful to have friends come from distant quarters? Is he not a junzi who feels no discomposure though others take no note of him? The difficulty is that you want virtue to be a private grind, or a reputation. Learning here is timed application, not hoarding. The friend from afar is the test of whether the work made a room. Being unknown without sourness is the last clause: if you need to be seen learning, you are already off the path.",
      keyIdea: "Learning is pleasant when applied in season. Obscurity is not a failure of the work.",
      misconception:
        "That cultivation is grim self-improvement, or that it has failed if no one notices you.",
      passageId: "confucius_analects.an_01_01",
      supportingPassageIds: ["confucius_analects.an_06_20"],
      theme: "practice",
      chatMode: "practice",
      chatPrompt:
        "Help me tell timed application from grim self-improvement. Where am I still studying so I will be seen?",
      practice:
        "Choose one small skill you already know and apply it once today at the right moment — not as a display. Afterward, notice whether you hunted for a witness.",
      journalPrompt:
        "Where am I still treating learning as a grind, or as a reputation?",
      integration:
        "You can apply one learned thing in season without needing to be noticed.",
    },
    {
      id: "cf-three-exams",
      title: "I daily examine myself on three points",
      orientation:
        "Joy without a daily audit becomes a mood. Zeng makes the craft checkable in three relations.",
      teaching:
        "Zengzi examines himself daily on three points: in acting for others, whether he has been faithful; in intercourse with friends, whether he has been sincere; whether he has practiced what he was taught. This is not a guilt inventory. It is three hinges: service, friendship, and whether teaching left the page. The difficulty is that you want a spiritual exam about states. Confucius will not give you that. The questions are about other people and about whether you did the thing you already know.",
      keyIdea: "The exam is relational. Faithfulness, sincerity, and practiced teaching — not a mood score.",
      misconception:
        "That self-cultivation is a private inner-state inventory, or that the exam is meant to produce shame.",
      passageId: "confucius_analects.an_01_04",
      supportingPassageIds: ["confucius_analects.an_14_25"],
      theme: "practice",
      chatMode: "practice",
      chatPrompt:
        "Help me run Zeng's three questions without turning them into self-hatred. Which relation did I skip?",
      practice:
        "Tonight, answer Zeng's three questions in writing — one sentence each. Where the answer is no, name one repair you can make tomorrow, not a new identity as a failure.",
      journalPrompt:
        "In which of the three relations am I still unexamined — service, friendship, or practiced teaching?",
      integration:
        "You can run a daily exam on relations rather than on spiritual moods.",
    },
    {
      id: "cf-return-to-li",
      title: "Subdue the self and return to li",
      orientation:
        "If rén is a feeling, later reciprocity becomes niceness. Yan Yuan is given a craft: restrain, return to form.",
      teaching:
        "Yan Yuan asks about perfect virtue. The Master says: to subdue one's self and return to propriety — that is rén. If a man can for one day subdue himself and return to li, all under heaven will ascribe rén to him. Is the practice of rén from a man himself, or is it from others? Look not at what is contrary to li; listen not, speak not, make no movement contrary to li. The difficulty: you want rén to be warmth you already have. Confucius makes it a refusal of the unformed impulse, and a return to shared form. The ascription from all under heaven is not a prize. It is what happens when one person stops being the exception to the room.",
      keyIdea: "Rén is self-restraint returning to form — not a nicer feeling you wait to have.",
      misconception:
        "That humaneness is a warm mood, or that li is empty etiquette you can skip if your heart is good.",
      passageId: "confucius_analects.an_12_01",
      supportingPassageIds: ["confucius_analects.an_03_03"],
      theme: "virtue",
      chatMode: "explain",
      chatPrompt:
        "Help me hear rén as return to form, not as a feeling. Where am I still waiting to feel kind before I keep the form?",
      practice:
        "Pick one ordinary form you already know — a greeting, a meal, a meeting. Keep it fully once today while the impulse wants an exception. Do not announce the virtue.",
      journalPrompt:
        "Where did I skip a form because I told myself my heart was already good?",
      integration:
        "You can keep one shared form without waiting to feel rén first.",
    },
    {
      id: "cf-one-thread",
      title: "One thread: zhong and shu",
      orientation:
        "Without the thread, li is a pile of rules. Confucius says the teaching is one, then leaves. Zeng names it.",
      teaching:
        "The Master says: Shen, my Way is threaded by one. Zeng says only: yes. The others have to ask. Zeng answers: the Master's Way is zhong and shu — and that is all. Zhong is being true in the inward; shu is extending that truthfulness as reciprocity. The difficulty is collecting Confucian maxims as a cabinet. The one thread is not a slogan you admire. It is the test of whether the inner fidelity and the outer reversal are the same craft. If they split, you have etiquette without a person, or sincerity that never reaches anyone.",
      keyIdea: "One thread: fidelity inward, reciprocity outward. Not two virtues you could specialize in.",
      misconception:
        "That the Analects are a cabinet of maxims, or that inner sincerity can skip how you treat others.",
      passageId: "confucius_analects.an_04_15",
      supportingPassageIds: ["zhongyong.zy_08"],
      theme: "virtue",
      chatMode: "explain",
      chatPrompt:
        "Help me keep zhong and shu as one craft. Where have I specialized in one and dropped the other?",
      practice:
        "Name one place you are loyal to a private principle while being careless with a person. Reverse one concrete act toward that person today so the inner claim has an outer body.",
      journalPrompt:
        "Where have I kept inner sincerity and skipped reciprocity — or kept manners and skipped being true?",
      integration:
        "You can feel zhong and shu as one move, not as two specialties.",
    },
    {
      id: "cf-shu",
      title: "The one word you could practice for a life",
      orientation:
        "The thread still needs a handle you can pick up under pressure. Shu is that word — reversal, not a theory of rights.",
      teaching:
        "Zigong asks if there is one word that can be practiced for a whole life. The Master says: is not shu such a word? What you do not want done to yourself, do not do to others. This is not the Christian golden rule as a positive duty to love as you wish to be loved. It is a stop. The difficulty is using it as a slogan while still doing the thing you would hate. Shu is the pause before you send what you would not welcome. It is how zhong leaves the self without becoming a metaphysics.",
      keyIdea: "Shu is a lifelong stop: do not send what you would not welcome.",
      misconception:
        "That reciprocity is a slogan, or that it is the same teaching as a positive command to love others as yourself.",
      passageId: "confucius_analects.an_15_23",
      supportingPassageIds: ["confucius_analects.an_12_02"],
      theme: "virtue",
      chatMode: "practice",
      chatPrompt:
        "Help me use shu as a stop, not as a motto. What am I about to send that I would not welcome?",
      practice:
        "Before the next message, request, or correction, reverse it: would I welcome this done to me, in this tone, at this hour? If not, rewrite or withhold. Send only what survives the reversal.",
      journalPrompt:
        "What did I almost send that I would not welcome — and did I stop?",
      integration:
        "You can catch one outgoing act and reverse it before it lands.",
    },
    {
      id: "cf-rectify-names",
      title: "If names be not correct",
      orientation:
        "Reciprocity still fails if the words in the room are lying. Zhengming is not pedantry. It is how a common world stays walkable.",
      teaching:
        "Asked what he would do first in government, Confucius says: rectify names. Zilu calls it wide of the mark. The Master does not apologize. If names are not correct, speech does not match things; affairs cannot succeed; li and music do not flourish; punishments miss; people do not know how to move hand or foot. The junzi's speech must be speakable and doable — nothing careless in words. The difficulty: you think naming is decoration. Here a false name is a ruined room. Calling a slight a betrayal, or a convenience a duty, is already a politics.",
      keyIdea: "A false name makes the next action unwalkable. Speech is ethics before it is style.",
      misconception:
        "That rectifying names is pedantry, or that how you name a situation is morally neutral.",
      passageId: "confucius_analects.an_13_03",
      supportingPassageIds: ["confucius_analects.an_011"],
      theme: "speech",
      chatMode: "practice",
      chatPrompt:
        "Help me catch one name I am using that does not match the thing. What action becomes impossible while that name stays?",
      practice:
        "Write the name you have been giving one conflict or person. Strike it. Write a plainer name that you could act on without theatre. Use only the second name in the next conversation.",
      journalPrompt:
        "Which name have I been using that made the room unwalkable?",
      integration:
        "You can drop one inflated name and speak a word you could actually carry out.",
    },
    {
      id: "cf-heaven-nature",
      title: "What Heaven confers is called nature",
      orientation:
        "The Analects stayed in the room. Zhōngyōng names the ground of the room: nature, Way, teaching — not a second religion of escape.",
      teaching:
        "What Heaven has conferred is called nature. Accordance with this nature is called the Way. Cultivating the Way is called teaching. The Way may not be left for an instant; if it could be left, it would not be the Way. The junzi is cautious over what is not seen and apprehensive over what is not heard. The difficulty: you want a path you visit, then leave for ordinary life. If it can be left, it was never the Way. This is not Kashmiri recognition and not a hidden God. It is the claim that the human pattern Heaven conferred is already the path — and teaching is cultivating it, not importing a better nature.",
      keyIdea: "The Way is accordance with conferred nature. If you can leave it, it was not the Way.",
      misconception:
        "That the Way is a special practice you visit and then leave, or that teaching means importing a better nature than the one conferred.",
      passageId: "zhongyong.zy_01",
      supportingPassageIds: ["zhongyong.zy_02"],
      theme: "self",
      chatMode: "explain",
      chatPrompt:
        "Help me hear nature-Way-teaching as one sequence, not as a retreat from ordinary life. Where do I still treat the Way as visitable?",
      practice:
        "For one hour, do not take a break from the Way as if it were a hobby. Keep one ordinary duty — a conversation, a meal, a walk — as the site of accordance, not as time off from cultivation.",
      journalPrompt:
        "Where do I still leave the Way as if it were a visit?",
      integration:
        "You can treat one hour of ordinary duty as the Way, not as time off from it.",
    },
    {
      id: "cf-before-stirring",
      title: "Before pleasure and anger arise",
      orientation:
        "If the Mean is mediocrity, the whole walk collapsed into being moderate. Equilibrium is the unstirred root; harmony is feeling in due degree.",
      teaching:
        "While pleasure, anger, sorrow, and joy have not yet arisen, that is called equilibrium (zhong). When they arise and all hit the due measure, that is called harmony (he). Equilibrium is the great root of the world; harmony is the universal path. Let both be perfected, and heaven and earth take their places; the ten thousand things are nourished. The difficulty: you hear 'mean' as playing it safe, or as the Kashmiri madhya — a Goddess-pause between breaths. This zhong is the mind before the weather of feeling claims to be the whole person. He is not suppression. It is anger that still knows its measure. Do not cash this in as a mystical gap. Keep it as how a room stays habitable when feeling arrives.",
      keyIdea: "The Mean is unstirred equilibrium, then feeling in due degree — not mediocrity, and not the madhya.",
      misconception:
        "That the Mean is mediocrity, that it means suppressing feeling, or that this is the same seam as the Kashmiri gap.",
      passageId: "zhongyong.zy_04",
      supportingPassageIds: ["zhongyong.zy_05"],
      theme: "mind",
      chatMode: "compare",
      chatPrompt:
        "Keep this civic. Do not let me cash equilibrium in as the madhya or as being bland. Where is feeling about to become the whole of me without measure?",
      practice:
        "When the next irritation or pleasure rises, pause one breath before speech. Ask: has this already become my whole face? If yes, wait until it can move at due degree. Then speak one measured sentence, or none.",
      journalPrompt:
        "Where did feeling dress as the whole of me — and what would due degree have been?",
      integration:
        "You can let a feeling arise without letting it be the whole of you, and without flattening it into blandness.",
    },
  ],
};
