#!/usr/bin/env python3
"""Ingest Futa Toro Pulaar texts from Henri Gaden, *Le Poular*, t. I *Textes* (1913).

Public-domain source: Henri Gaden, *Le Poular: dialecte peul du Fouta sénégalais*,
t. I, *Étude morphologique. Textes* (Paris: E. Leroux, 1913). Internet Archive:
le-poular-etude-morphologique-textes. Pulaar is Gaden's Latin transcription of
Ajami written by Futa literates (Mahmadou Alfa, Tyerno Aoudi, and others).
English is a Pratibha rendering (pd_adapted) from Gaden's facing French.

Does not follow Gaden 1931 *Proverbes et maximes peuls* (too late for US PD).
Does not follow Hampâté Bâ / *Koumen* (not PD).

Floor: 28 units. Ten are hero verses (tts_key) for the collection mandala
and Listen bake.
"""
from __future__ import annotations

import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/pulaar_texts")
SLUG = "pulaar_texts"
COLL = "Pulaar Texts (Gaden)"
PROV = (
    "English is a Pratibha rendering (pd_adapted) from Henri Gaden's facing French in "
    "*Le Poular*, t. I *Textes* (Paris: Leroux, 1913 — public domain). Pulaar is Gaden's "
    "Latin transcription of Futa Toro Ajami written by Futa literates (named in Gaden). "
    "Does not follow Gaden 1931 *Proverbes* (too late)."
)
NOTE = (
    "Futa Toro Pulaar (Gaden: poulàr) from the Senegal river valley. Gaden asked Futa "
    "literates accustomed to Ajami to compose or dictate; he prints their Pulaar and a "
    "facing French version. Named authors in this selection include Mahmadou Alfa and "
    "Tyerno Aoudi. A mallol (pl. malli) is a proverb or parabolic locution whose apparent "
    "sense covers a hidden one. Orthography is Gaden's 1913 Latin plate (long vowels "
    "marked), not modern Pulaar ɓ ɗ ƴ ŋ."
)

# Ten heroes spread across Gaden's book (tales → early mallol → later mallol).
# Required: 001 tale formula, 002 counsel, 003 sababu, 005 truth, 006 heart.
HEROES = {1, 2, 3, 5, 6, 8, 20, 24, 25, 27}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


# Each unit: n, gaden, title, pul, tr, comm, prac, terms, resonances
UNITS: list[dict] = [
    {
        "n": 1,
        "gaden": "Contes populaires, opening formula (tale 10 and following)",
        "title": "What Was Here, What Will Be, What Will Not Be",
        "pul": "won ko wonnō do, ina wona wonatā, ko tindol.",
        "tr": "This is what was here; it will be, or it will not be. It is a tale — a thing to be heard.",
        "comm": "The claim is ontological before it is narrative. Gaden notes that European \"once upon a time\" is only the past. Futa Pulaar refuses that thin tense. won names existence without locating it. The facts were here formerly (wonnō do). Perhaps they will happen later (wona). Perhaps they will never happen (wonatā). The telling exists because an audience is here that wants to hear (tindol). Time is not the container of the teaching. Hearing is. This is how a pastoral-Islamic people, whose pre-Islamic cult the ethnographers could not find as a book, still philosophize in their own language. The tale is not a lie about the past. It is a mode of existence offered to listeners. Gaden adds that a Futa tale usually ends with a moral. The formula already contains the method: do not ask first whether this happened. Ask whether you can hear it. Existentially the sentence trains a discipline against both historicism and fantasy. You do not need the event to have been dated. You need an ear. A teaching that cannot survive wonatā — it will not be — was only news. A teaching that can be heard whether or not it occurs is already a practice.",
        "prac": "Tell one true thing as if it were a tindol: it was here, it may be, it may never be. Do not argue its date. Speak it to one living ear. If no one can hear it, it is not yet a teaching.",
        "terms": kt(
            ("won", "verbal root of existence, without tense — the tale's events exist in a tenseless field; English 'there was' flattens the formula into a past anecdote"),
            ("wonnō do / wona / wonatā", "was here / will be / will not be — three modalities of the same root; the teaching is not located in one of them; hearing holds all three"),
            ("tindol", "thing for hearing (rac. tin, to hear) — the tale as audible object; 'story' is too literary, 'folktale' too folkloric; this is existence offered to an ear"),
            ("ko", "relative / focusing particle: 'it is (that which)...'; Gaden: ko often stands before a noun to specify it"),
        ),
        "res": res(
            ("Zhuāngzǐ, opening 'once there was' parables", "Both use a narrative that is not bound to a dated event.", "Zhuāngzǐ's wanderings dissolve the need for a moral; Futa tindol usually ends in one."),
            ("Heraclitus B1, on listening (akousai) to the logos", "Both make hearing, not seeing a dated fact, the gate of the teaching.", "Heraclitus' logos is one; Futa tales are many, each opened by the same formula."),
        ),
    },
    {
        "n": 2,
        "gaden": "Tale 15, Les conseils d'un père",
        "title": "A Father's Counsel",
        "pul": "mido rēntinma gede: neno wonā dādīdo, lāmdo wonā gidirādo, lembel wonā debbo, dutten wonā biddo; wata woppu bibbe bāmma nanga bibbe yumma, sabu bi bāmma ina yidanma maide, kono yidanāma koyēra.",
        "tr": "I am going to put you on guard against some things: a flatterer is not a companion; a king is not a comrade; a second wife is not a wife; a stepson is not a son. Do not abandon your father's children to take your mother's children, because your father's children will wish death for you, but they will not wish shame for you.",
        "comm": "The claim is a map of false nearness. Four relations look like intimacy and are not: the neno who praises you, the king who rules you, the second wife, the stepson. Then a fifth, harder: even blood splits. Father's children and mother's children are not the same loyalty. The scandal is the last clause. Agnatic kin may wish you dead. They will not wish you shamed. Death is a fact. Shame is the destruction of the name. This is Pulaar ethics in Pulaar, not a French report that the Peul consults his mother. The dying father speaks koyēra. Honor is the thing kin will not spend even on an enemy-brother. The rest of Gaden's tale is a plot that proves the counsel by violating it: the son takes a neno as companion, and the praise-man sells him. The unit keeps the counsel. Practice is the list, not the plot twist. Existentially: name the relations you have mistaken for companionship. A patron is not a friend. A second arrangement is not the first. And when you must choose a loyalty, ask not who loves you, but who would refuse your shame.",
        "prac": "Write four names you have been using wrongly: someone you called friend who is a patron, someone you called kin who is a faction. For one day, use the accurate word. Do not abandon anyone. Stop lying about the relation.",
        "terms": kt(
            ("neno", "flatterer of artisan/griot caste (rac. nen, to flatter) — not 'griot' as musician only; one who lives by your praise cannot be your dādīdo (companion)"),
            ("koyēra", "shame, dishonor — worse than death in this sentence; later semteende / pulaaku; Gaden's 1913 text already has the ranking"),
            ("bibbe bāmma / bibbe yumma", "father's children / mother's children — split lineage inside one household; English 'siblings' hides the fork the father is pointing at"),
            ("wonā", "is not — four negations of false equivalence; the counsel is not advice to be cold; it is a refusal to name the wrong thing as the right thing"),
        ),
        "res": res(
            ("Analects 13.3, rectification of names", "Both insist a king is not a comrade and a second is not a first.", "Confucius aims at ritual-political order; this father aims at a son's survival inside caste and polygyny."),
            ("Sirach 6:5–17, on false friends", "Both warn that proximity is not loyalty.", "Biblical wisdom is theistic gnomic verse; this is a dying man's list, then a tale that proves it by breach."),
        ),
    },
    {
        "n": 3,
        "gaden": "Mallol 66",
        "title": "Everything Is Done by a Cause",
        "pul": "hüde fuf, ko sababu wadata.",
        "tr": "Every affair — it is a cause that does it.",
        "comm": "The claim is causal without being mechanical. Nothing just occurs. A sababu does it. Gaden places this as the first of his proverbes et locutions proverbiales, and the next mallol rhymes it: water is not salty without a reason. Futa Pulaar, already deep in Islam, uses an Arabic loan for cause and a Pulaar verb for the doing. The world is not a pile of accidents. It is a field of reasons, including reasons people will not admit. This is not yet Western determinism. Sababu in Sahelian usage includes motive, pretext, the hidden why, the social cause. To say ko sababu wadata is to refuse both God did it, so do not look and it just happened. Look for the cause. The looking is the practice. The proverb does not say the cause is always just. It says there is one. Existentially: stop calling your pattern bad luck. Name the sababu. If you cannot name one, you are not done looking. A life that cannot survive this sentence is a life that has outsourced its own agency to weather.",
        "prac": "Take one thing that just happened this week. Do not stop at luck or fate. Name one sababu you can actually point to — a choice, a hunger, a fear, a word. If the first name is false, look again.",
        "terms": kt(
            ("hüde", "thing, affair, matter — not a physical object only; a happening; English 'everything' is too cosmic; this is every case"),
            ("sababu", "cause, reason (Arabic sabab in Pulaar) — loanword as conceptual tool; 'reason' in the philosophical sense, not 'excuse' only, though pretext is included"),
            ("wadata", "does / makes (it) — the cause is an agent-like doer; English 'is caused' is too passive"),
            ("fuf", "all, every — totality of affairs, not of atoms"),
        ),
        "res": res(
            ("Aristotle, Physics II, on aitia", "Both refuse uncaused happenings.", "Aristotle's four causes are a technical system; sababu is a proverb's one word for why."),
            ("Qurʾān 18:84–85, sabab as a means God gives Dhū l-Qarnayn", "Both inherit the Arabic root of means and cause.", "The Qurʾān can mean a cord, a way, a means to a horizon; Futa usage here is everyday causality you must name."),
        ),
    },
    {
        "n": 4,
        "gaden": "Mallol 68",
        "title": "A Small Act Returns a Small Act",
        "pul": "badel fuf ko battel.",
        "tr": "Every small act is a small act in return.",
        "comm": "The claim is reciprocity at the scale where people pretend nothing counts. Not only blood-feud and not only royal justice: badel, a little deed, is already battel, a little deed coming back. Gaden glosses talion, and then the more important half: one renders good for good and, especially, evil for evil. The proverb's compactness is the teaching. There is no leftover smallness that does not re-enter the world. This is Pulaar social physics. The cattle-world of the ethnography already lived it: bridewealth named in cows, green leaves tossed to the dead. Here the language itself says that action is echo. You do not get to do a small cruelty as if it evaporated. You also do not get to do a small kindness as if it were nothing. Existentially: stop storing petty acts in a bin marked doesn't matter. They matter in the diminutive. That is their whole size, and they return at that size. The moral is not grandeur. It is attention at the scale you actually live.",
        "prac": "Do one deliberately small good today that you will not advertise. Do not cancel one small harm by a speech. Watch whether a battel appears. If none appears, you still did the badel. That was the point.",
        "terms": kt(
            ("badel", "small action (diminutive of an act) — the proverb's subject is not war or law; it is the little thing; 'deed' is too grand"),
            ("battel", "small action in return — echo, not a different category; 'revenge' is only the dark reading; Gaden includes good for good"),
            ("fuf", "every — no exempt petty act"),
            ("ko", "it is (that) — identity, not mere similarity: the return is the act's other face"),
        ),
        "res": res(
            ("Matthew 7:2, measure for measure", "Both bind outgoing act to returning act.", "Matthew aims at mercy beyond talion; this proverb states the law the mercy would have to exceed."),
            ("Karma as action-return (Bhagavad Gītā 3–4)", "Both refuse a deed that dies at the doer.", "Indic karma is often multi-life; battel is this-world social echo."),
        ),
    },
    {
        "n": 5,
        "gaden": "Mallol 69",
        "title": "Truth Catches the Lie",
        "pul": "so pene dawi, so gōnga hirdi. mā hebto pene.",
        "tr": "If the lies set out early and the truth in the evening, it will overtake the lies.",
        "comm": "The claim is temporal and almost pastoral: departure times. Lies leave at dawn, hustling. Truth leaves in the evening, late. The proverb does not say truth is faster in essence. It says truth catches up. Gaden's gloss is the European flattening: truth always comes out. The Pulaar image is a road. Two parties have started. One had a head start. The late one still arrives on the early one's back. This belongs with Fulɓe mobility. A herder knows that the one who left late can still meet the one who left first, if the first is a lie and the second is gōnga. The moral is patience without passivity. You do not have to win the morning. You have to be the thing that overtakes. Existentially: if you are late with the true word, do not despair of the morning's rumor. Set out. The proverb is a promise to the late-teller, and a warning to the early-liar. Speed is not the virtue. Catching is.",
        "prac": "If a false version of something you know has already left this morning, do not match its speed with a louder lie. Speak the true version once, even late. Then stop. Let hebto be the proverb's job, not your panic.",
        "terms": kt(
            ("gōnga", "truth — not 'fact' only; the true word / true state; 'honesty' is too moralistic; this is what can travel and catch"),
            ("pene", "lies (plural) — they travel as a group, with a head start"),
            ("dawi / hirdi", "leave early / leave in the evening — pastoral clock, not clock-time; dawn and dusk are when a camp actually moves"),
            ("hebto", "overtake, catch up — a physical verb for a moral event; English 'comes out' loses the road"),
        ),
        "res": res(
            ("Dào Dé Jīng 78, the slow and soft conquering the hard", "Both trust the late, unhurried term.", "Daoist softness wins by emptiness; here truth wins by pursuit on a road."),
            ("Luke 12:3, what is whispered will be shouted", "Both promise exposure of the hidden word.", "Christian apocalypse is a last day; this overtaking can happen this evening."),
        ),
    },
    {
        "n": 6,
        "gaden": "Mallol 70",
        "title": "The Heart Is Not a Joint",
        "pul": "berde wana hofūru, sako hofe.",
        "tr": "The heart is not a joint, that it might be bent.",
        "comm": "The claim is that feeling is not an obedient limb. A joint exists to flex on command. The heart does not. Gaden: sentiment cannot be ordered. This is the Pulaar refusal of a certain Islamicate and colonial fantasy — that the inner can be drilled like the body at circumcision, where Lasnet saw impassibility. Impassibility is the face. Berde is not the face. You can keep the face still. You cannot hinge the heart. The proverb is not a romantic license to follow every impulse. It is a limit on tyranny, including self-tyranny. You may require conduct. You may not require love, grief, or desire to take the angle you prefer. Pulaaku as later named is composure. This mallol is the remainder: composure is not the same as a bent heart. Existentially: stop commanding yourself to feel otherwise as if the heart were an elbow. Change the situation, the company, the act. Leave the heart its unhinged nature. That honesty is already a practice. The contested move is to keep duty without falsifying the inner weather.",
        "prac": "Catch one sentence today that begins 'I should feel...' Stop it. Keep the outer duty if there is one. Do not order the heart as if it were a joint. Notice what it actually does when you stop bending it.",
        "terms": kt(
            ("berde", "heart as organ of feeling — not anatomical cardiology; the inner that will not take orders"),
            ("hofūru", "joint, articulation — the body's obedient bend; the metaphor's insult: do not treat the heart as a knee"),
            ("sako", "so that / as if it were the kind of thing that... — counterfactual purpose: it is not that kind of thing"),
            ("wana", "is not — the same negation-pattern as the father's wonā"),
        ),
        "res": res(
            ("Pascal, Pensées, reasons of the heart", "Both deny that the heart is a syllogism or a lever.", "Pascal's heart knows God; this proverb does not name what the heart knows, only that it will not bend on command."),
            ("Stoic propatheia versus judgment (Epictetus, Discourses I)", "Both distinguish inner weather from commanded virtue.", "Stoics train judgment to withhold assent; this proverb does not promise training will hinge the berde."),
        ),
    },
    {
        "n": 7,
        "gaden": "Mallol 79",
        "title": "Nature Is a Birthmark Rolling Does Not Remove",
        "pul": "dikku ko būlol tallāde 'ittatā.",
        "tr": "Innate manner is a natural mark: rolling does not remove it.",
        "comm": "The claim is that character is not surface dirt. A birthmark survives being rolled. Gaden: the naturally well-conducted stay so in every circumstance; the badly natured likewise. This can become fatalism. The philosophical use is stricter: do not trust a change that is only tumbling. Travel, conversion, a new language, a new mosque, a new job — tallāde — do not by themselves lift dikku. If you want a different mark, something other than rolling is required, and the proverb does not pretend to name that other thing. It only kills the fantasy of the tumble. Read beside the cattle ethnography: the herd's way is transmitted. Read beside what the cow ate, the heifer suckles. Futa Pulaar keeps saying that the given is sticky. Islam in Futa is a real conversion. The proverb still warns that a converted mouth can carry an unconverted dikku. Existentially: stop relocating to escape yourself. The mark goes with the hide. If you must change, change a practice that is not mere motion. The contested move is to refuse tourism as repentance.",
        "prac": "Name one dikku you have been trying to roll away by changing rooms, jobs, or company. Keep the body still for one day and watch the mark. If it is harmful, choose one non-rolling act — apology, abstinence, a craft — instead of another move.",
        "terms": kt(
            ("dikku", "innate manner of being, natural bearing — 'character' is close; 'personality' is too modern-psychological"),
            ("būlol", "natural mark, birthmark — visible given on the body as analog of invisible given in conduct"),
            ("tallāde", "rolling — motion that looks like processing (hides are rolled, bodies are rolled); 'travel' and 'ordeal' both sit inside the verb"),
            ("'ittatā", "does not remove — a hard negative future; the mark will still be there after the roll"),
        ),
        "res": res(
            ("Heraclitus B119, ēthos anthrōpōi daimōn", "Both bind a person's way as a given companion.", "Heraclitus' daimōn is a divine allotment; dikku is more like a hide-mark."),
            ("Mencius 6A, on xing (nature) and cultivation", "Both ask whether nature can be worked.", "Mencius waters sprouts; this proverb only says rolling is not the work."),
        ),
    },
    {
        "n": 8,
        "gaden": "Mallol 145",
        "title": "What the Cow Ate, the Heifer Suckles",
        "pul": "ko nagge nāmi, dūm nale muinata.",
        "tr": "What the cow has eaten is what the heifer suckles.",
        "comm": "The claim is transmission as milk, not as lecture. The calf does not suckle a theory. She suckles what already became the mother's body. Gaden: qualities and faults of parents pass to children. The image is more precise than like father like son. Diet becomes blood becomes milk becomes the next body. A people whose remaining cult was the herd will say inheritance in the language of nursing. This is the Pulaar text that the ethnography of boolâtrie was circling and could not quote. The proverb is also a warning to the eater, not only a law about children. You are what will be drunk. Your nāmi — what you take in — is not private. It will be somebody's milk. That is pastoral metaphysics in one clause. Existentially: look at what you are eating, hearing, envying, repeating. That is the future's milk. Change the cow's mouth if you care about the heifer. The contested move is to treat intake as already pedagogy.",
        "prac": "Before you take something in today — food, a story, a grievance — ask: would I want a young life to suckle this? If no, do not eat it. If yes, eat it as if you were already milk.",
        "terms": kt(
            ("nagge", "cow — the sacred-economic animal of Fulɓe life, here the parent-body; English 'cow' is livestock, not a liturgical center"),
            ("nale", "heifer, young female cattle — the next generation as a nursing animal, not as an abstract 'child'"),
            ("nāmi / muinata", "has eaten / suckles — two mouths, one substance; 'inherit' in English loses the mouths"),
            ("dūm", "that (very thing) — identity of what was eaten and what is drunk; no remainder, no filter"),
        ),
        "res": res(
            ("Chāndogya Upaniṣad 6, food-chain of annam", "Both make eating a cosmological act that becomes the next body.", "The Upaniṣad generalizes food as Brahman; this proverb stays in the cow-heifer pair."),
            ("Jeremiah 31:29, the parents have eaten sour grapes", "Both transmit the eaten to the child.", "Jeremiah can refuse inherited guilt; this mallol states the milk-law without a prophet's override."),
        ),
    },
    {
        "n": 9,
        "gaden": "Mallol 146",
        "title": "The Good Morning Is Known from Dawn",
        "pul": "subaka moddo 'andeté ko gila fadiri.",
        "tr": "The good morning is recognized from the first light.",
        "comm": "The claim is that quality shows at the start, not at the advertisement of noon. Gaden: one sees in the child what the adult will be; one knows from the outset what a new chief is worth. The next proverb repeats it botanically: what fruits begins by flowering. Futa speech trusts beginnings. This is not fortune-telling. It is attention. Dawn is small. It is already the day, or it is not. Subaka is also the hour of ṣubḥ prayer. A good morning in an Islamic river valley is both weather and worship. The proverb does not need to choose. First light is enough to know. If you must wait until noon to see whether a person, a project, or a rule is good, you have been refusing dawn. Existentially: look at the first five minutes. They are not a draft. They are already the morning. Adjust there, not in a speech at midday. The contested move is to treat the opening as already a verdict, without waiting for a more flattering hour.",
        "prac": "Tomorrow, do not wait until the day has an opinion of itself. At first light — or at the first five minutes of a task — name whether it is moddo. If it is not, change the opening, not the alibi at noon.",
        "terms": kt(
            ("subaka", "morning, dawn-time — Islamic and pastoral at once; English 'morning' misses the prayer-hour"),
            ("fadiri", "first light, aurora — the smallest beginning that already tells"),
            ("moddo", "good, as a morning can be good — qualitative, not moralistic 'virtuous'"),
            ("'andeté", "is known (passive / middle of knowing) — recognition, not inference from a report"),
        ),
        "res": res(
            ("Dào Dé Jīng 64, the tiny that is already the great", "Both read the dawn as the day.", "Daoist tiny is uncarved; this dawn is already classed as moddo or not."),
            ("Matthew 7:16, by their fruits", "Both read early signs as knowledge, not as guesswork.", "Fruit is an end; fadiri is a beginning that already counts as knowledge."),
        ),
    },
    {
        "n": 10,
        "gaden": "Mallol 93",
        "title": "If an Elder Dances, Let Them Bind Their Hair",
        "pul": "so maudo 'ami, yō mōro.",
        "tr": "If an elder dances, let them bind their hair.",
        "comm": "The claim is that dignity is not abstinence from joy; it is the way joy is worn. An elder may dance. The proverb does not say maudo must sit. It says: if dancing, then mōro — hair bound, the head prepared. Children may arrive undone. Age may not. Gaden's second gloss is the inner teaching: when you launch into an affair, devote yourself entirely. Half-dancing is the real indecency. This is pulaaku-adjacent without the later word: reserve is not joylessness. It is completeness of form. The ethnography saw Fulɓe gravity and rare dancing. The Pulaar proverb is more interesting than the stereotype. Dance, but do not dance as if you were still unformed. Existentially: pick one joy or one task you have been doing sloppily because you thought seriousness meant refusal. Do it. Bind the hair. Whole form, or don't enter the circle. The contested move is to allow the elder the dance while refusing the unprepared head.",
        "prac": "Enter one thing today that you have been half-doing — a conversation, a craft, a rest. If you enter, bind the hair: prepare, dress the part, stay until the form is complete. If you will not, do not step into the circle and call it humility.",
        "terms": kt(
            ("maudo", "elder, a person of weight — age and status; not merely 'adult'"),
            ("'ami", "dances — allowed, not forbidden; the if-clause is permission plus condition"),
            ("mōro", "bind the hair, make the coiffure — bodily readiness as the image of total commitment"),
            ("yō", "hortative 'let...' — a command of form, not a ban on the dance"),
        ),
        "res": res(
            ("Analects 3, ritual even in pleasure", "Both require form when the great person moves.", "Li is a code of occasions; mōro is one concrete gesture standing for total entry."),
            ("Nietzsche, The Gay Science, on the dancing god", "Both refuse a dignity that cannot dance.", "Nietzsche's dance is unbinding; this dance is bound hair."),
        ),
    },
    {
        "n": 11,
        "gaden": "Mallol 67",
        "title": "Water Is Not Salty Without a Reason",
        "pul": "diam lammatā mere.",
        "tr": "Water is not salty without a motive.",
        "comm": "The claim is the rhyme of sababu, now in a cup. Water that tastes of salt has a why. Mere — without motive — is the word Gaden also uses when a well-fed child has been left in an abandoned camp: not without a reason. Futa speech will not let a quality float. Salt in the water is not a mood of the river. It is an event with a cause: a tide, a well, a hand, a mineral. Pair this with hüde fuf, ko sababu wadata and you have a method. First: every affair is done by a cause. Second: even a taste has one. The contested move is to treat sensory givenness as already a question. You do not stop at the tongue. You ask what salted it. Islam in Futa already had a God who measures. This mallol does not replace God with chemistry. It refuses the shrug that calls a spoiled well fate and walks away. Existentially: the next thing that 'just tastes wrong' in a room, a deal, a friendship — name the salt. If you cannot, you have only had a flavor, not a teaching.",
        "prac": "Taste one situation that has gone off. Do not stop at the flavor. Name the mere you had been using as a shrug — 'that's just how it is' — and replace it with one actual motive you can point to.",
        "terms": kt(
            ("diam", "water — ordinary river and well water, not a cosmic element; the proverb's subject is a daily drink"),
            ("lammatā", "is not salty — a negative quality-verb; English 'unsalted' describes a product, this describes a state that needs a why if it reverses"),
            ("mere", "without motive / not without reason — the same hinge as mallol 81; English 'for no reason' is a shrug; mere is a refused shrug"),
        ),
        "res": res(
            ("Mallol 66 of this collection, ko sababu wadata", "Both refuse an uncaused quality in the world of affairs.", "66 names cause as a doer of every case; 67 names it as the salt in a cup — same method, smaller object."),
            ("Heraclitus B61, seawater drinkable and deadly", "Both make water's taste a philosophical fact, not a preference.", "Heraclitus splits one water into two uses; this mallol asks what made the one taste."),
        ),
    },
    {
        "n": 12,
        "gaden": "Mallol 72",
        "title": "Every Stick of Wood Has Its Ash",
        "pul": "leggel khalu e dukal mum.",
        "tr": "Every small piece of wood furnishes its small bit of ash.",
        "comm": "The claim is usefulness without rank. A stick is not a beam. It still burns down to a measure of ash that is its own. Gaden: each thing has its utility; the humblest can render a service. Futa hearths know this in the fingers: you do not throw the twig aside because it is not a log. Ash is the proof of having been used, not a leftover insult. The contested move is to refuse a scale of being in which only the large counts as real work. Pastoral and riverine life runs on small fuels, small gifts, small names. English 'everyone has something to offer' is a pep talk. This mallol is a physics of the fire: the small has a small product, and that product is still the thing's honor. Existentially: stop waiting to be a log. Burn as the stick you are. The ash will be the right size. Humility here is not self-erasure. It is accurate fuel.",
        "prac": "Do one task today that is beneath the title you prefer. Finish it until there is ash — a completed small product. Do not upgrade it into a speech about your potential.",
        "terms": kt(
            ("leggel", "small piece of wood (diminutive) — the proverb's hero is the twig, not the tree; English 'wood' is too generic"),
            ("khallu / khalu", "each, every one of a class — distributive, not a mass 'all wood'"),
            ("dukal", "a small quantity of ash — diminutive of use; 'ash' in English is waste; here it is the stick's delivered service"),
        ),
        "res": res(
            ("1 Corinthians 12, many members, one body", "Both refuse a body in which the small part is ornamental.", "Paul ranks gifts under one Spirit; this mallol ranks nothing — the ash is simply the stick's own."),
            ("Zhuangzi, the useless tree", "Both think about wood and worth.", "Zhuangzi saves the tree by uselessness; this stick is saved by burning down to a right-sized ash."),
        ),
    },
    {
        "n": 13,
        "gaden": "Mallol 75",
        "title": "The Toad Loves Water That Is Not Boiling",
        "pul": "fabru ina yidi diam, kono wana pasnadam.",
        "tr": "The toad loves water, but not boiling water.",
        "comm": "The claim is that need has a temperature. The toad is an animal of water. Excess of the same element kills it. Gaden: excess is a bad thing in everything. Futa speech chooses a creature that cannot live without what can also cook it. The proverb is not a warning against water. It is a warning against the fantasy that more of a good is still the good. Speech, honor, cattle, even ṣabr — patience itself — can be boiled. The contested move is to keep the object and refuse the degree. English 'everything in moderation' is a diet slogan. This mallol is a zoology of desire: the loved thing, past a threshold, is no longer the loved thing. Existentially: name one water you have been boiling because you love it. Cool it. Keep the need. Kill the scald. The toad's wisdom is not abstinence. It is the unboiled cup.",
        "prac": "Pick one good you have been doubling — work, talk, a comfort, a grievance. Keep the first measure. Pour off the second. Sit with the cooler cup and see whether the need was the heat or the water.",
        "terms": kt(
            ("fabru", "toad — a water-animal as the proverb's philosopher; English 'toad' is comic; here it is the one who knows the element from the scald"),
            ("diam", "water — the needed element, same word as mallol 67; continuity of the cup"),
            ("pasnadam", "boiling (water) — the same substance past the threshold; English 'hot water' is trouble; this is literally cooked need"),
        ),
        "res": res(
            ("Aristotle, Nicomachean Ethics II, the mean", "Both locate virtue between too little and too much of a needed thing.", "Aristotle theorizes a mean relative to us; the toad simply refuses the boil."),
            ("Dhammapada 24, on craving that grows by feeding", "Both warn that the loved object can become the trap.", "The Dhammapada aims at cessation; this mallol keeps the water and only kills the temperature."),
        ),
    },
    {
        "n": 14,
        "gaden": "Mallol 78",
        "title": "Whoever Loves God Will Love the Prophet",
        "pul": "mo yidi Alla kala, yidat Annabido.",
        "tr": "Whoever loves God will love the Prophet.",
        "comm": "The claim is that love of the unseen is tested on a named person. Alla is not a private atmosphere. If the love is real, it will include Annabido — the Prophet as the one through whom this river valley received the Name. Gaden flattens: the friends of our friends are our friends. That is the social half, and it is true. The theological half is stricter. You do not get to love God and refuse the messenger who made God speakable here. Futa Toro is an Islamic country in this book. The mallol is not a conversion pamphlet. It is a criterion of yide, love, as a transitive that cannot stop at the first object. The contested move is to treat devotion as a solo. Existentially: the next time you claim a love for a principle, a people, a God, look at the person through whom that love actually arrived. If you slight them, the principle was a mood. Speech here is loyalty's grammar: you cannot say the first name honestly without the second.",
        "prac": "Name one principle you say you love. Name the actual person through whom it reached you. Do one act of loyalty toward that person today — a word, a debt paid, a refusal to slight them in a room they are not in.",
        "terms": kt(
            ("yidi / yidat", "loves / will love — not 'like'; a binding affection that has a future tense; English 'love God' can be a feeling; this is a verb that must land on a second object"),
            ("Alla", "God — Arabic Allāh in Pulaar mouth; the unseen first object"),
            ("Annabido", "the Prophet (Annabi + class ending) — Muḥammad as the named second object; English 'the Prophet' is a title; here it is the test of the first love"),
        ),
        "res": res(
            ("Qurʾān 4:80, who obeys the Messenger has obeyed God", "Both bind love of God to the messenger as non-optional.", "The Qurʾān legislates obedience; this mallol speaks the bond as yide, love, in the future tense."),
            ("John 14:15, if you love me, keep my commandments", "Both make love visible on a second act.", "John's second act is keeping words; Futa's second object is a person the valley already names."),
        ),
    },
    {
        "n": 15,
        "gaden": "Mallol 80",
        "title": "Camels Boasting of Their Calluses",
        "pul": "soko gelōdi basodiri danale, nalla 'ērani.",
        "tr": "If the camels boast among themselves of their calluses, they spend the day without grazing.",
        "comm": "The claim is that vanity about a wound is still vanity, and it costs the day's food. Calluses are what camels have from kneeling and from loads. They are real. They are also not a feast. Gaden: there is nothing good to hope from those who take pride in their defects. Futa honor (koyēra's other face) can curdle into a competition of scars. The herd that talks about its sores does not eat. The contested move is to refuse suffering as a credential. English 'don't rest on your hardships' is a workshop poster. This mallol is pastoral: the mouth that is busy ranking calluses is a mouth that is not cropping. Existentially: notice one defect you have been displaying as identity. Stop narrating it for one day. Graze. The callus will still be there. At least the body will have been fed. Honor that cannot eat is not honor. It is a circle of camels comparing knees.",
        "prac": "Catch one story you tell about a scar, a slight, a hard year, as if the scar were a rank. Do not tell it today. Eat an ordinary meal, do an ordinary task, and let the callus be unmarked by speech.",
        "terms": kt(
            ("gelōdi", "camels — Sahel pack-animals, not desert romance; the proverb's fools are working beasts who forgot to work"),
            ("danale", "calluses, kneeling-pads — the honorable sore of a load-bearing life; English 'callus' is skin; here it is a boastable defect"),
            ("basodiri", "boast among themselves — a reciprocal vanity; the herd as an echo-chamber"),
            ("'ērani", "without grazing — the day's actual loss; English 'wasted the day' is clock-time; this is un-eaten pasture"),
        ),
        "res": res(
            ("Paul, 2 Corinthians 11–12, boasting in weakness", "Both know that wounds can become a speech.", "Paul boasts in weakness to point at grace; these camels boast in calluses and miss the grass."),
            ("Mallol 2 of this collection, neno is not a companion", "Both warn that speech about status is not the work.", "The father warns against the flatterer; this mallol warns against becoming the camel who flatters his own sore."),
        ),
    },
    {
        "n": 16,
        "gaden": "Mallol 85",
        "title": "Nothing Sharpens Like Hearing the Cry",
        "pul": "'ala ko dodini gen-guddo sako de nani palepale.",
        "tr": "Nothing makes a thief's wife cunning like when she hears the cries of those who want her husband caught.",
        "comm": "The claim is that hearing is not a passive sense. Palepale — the alarm, the hue and cry — enters an ear that already has a stake, and the mind flowers into ruse. Gaden: the spirit of those who have something to hide is never more fertile than when they feel discovered, or even only suspected. The mallol names a woman as accomplice, then widens: it applies to the guilty and to the partner. Futa speech is unsentimental here. Hearing is a moral event. You do not just receive sound. You become a kind of intelligence. The contested move is to treat listening as innocence. English 'I only heard' is a legal shrug. This proverb says the hearing was already a sharpening. Existentially: notice what you become more clever at the moment you overhear a threat to your cover. That cleverness is the mallol. Practice is not to stop having ears. It is to notice that the ear has already chosen a side. Patience and hearing meet here: the cry arrives first; the ruse is the refusal to sit still in the truth.",
        "prac": "When you next overhear a threat to something you have been hiding — a mistake, a vanity, a small cheat — do not invent the next move. Name the cover out loud to yourself. Let the ear have heard without commissioning a ruse.",
        "terms": kt(
            ("nani", "hears — not 'is told'; the verb of the ear as an event that changes the hearer"),
            ("palepale", "the cries of pursuit, hue and cry — public hearing as a weapon; English 'alarm' is a sound; this is a social hunt entering an ear"),
            ("dodini", "makes cunning / renders crafty — hearing as a cause of intelligence; English 'clever' is a compliment; here it is complicity waking up"),
            ("gen-guddo", "thief's wife — the proverb's first subject; accomplice as the one whose ear is already pledged"),
        ),
        "res": res(
            ("Heraclitus B1, the many who hear like the deaf", "Both make hearing a test of what kind of person you are, not a mere sense.", "Heraclitus' hearers miss the logos; this hearer understands too well and turns the hearing into a ruse."),
            ("2 Samuel 15–17, the counsel of Ahithophel and Hushai", "Both show intelligence flowering when a hidden side is threatened.", "The biblical scene is court politics; this mallol is a household ear at the moment of the cry."),
        ),
    },
    {
        "n": 17,
        "gaden": "Mallol 89",
        "title": "Not Every Pierced Ear Hangs Gold",
        "pul": "wana nofüru tuffidu fuf senete karine.",
        "tr": "It is not to every pierced ear that gold is hung.",
        "comm": "The claim is that opening is not reward. A pierced ear is already a prepared place. Gold does not follow as a right. Gaden: few ambitions are satisfied. Futa women's gold in the ear is honor made visible. The mallol strips the visibility: many ears are ready; few are weighted. Hearing and honor share an organ here. You can make a hole for glory and still hang nothing. The contested move is to treat preparation as entitlement. English 'not everyone gets the prize' is a contest. This proverb is quieter. The ear did its part. The gold is another order. Existentially: name one opening you have made — a skill, a wound, a public readiness — that you have been treating as a claim on gold. Leave the hole as a hole for one day. If gold comes, it will not have been because you stared at the piercing. Patience is the ungolded ear that does not close itself in spite.",
        "prac": "Touch the place in your life that is already pierced — trained, exposed, waiting. Do not add a demand. Do the ordinary work of the day with that opening unrewarded, and see whether honor was the gold or the readiness.",
        "terms": kt(
            ("nofūru", "ear — the organ of hearing and of ornament; English 'ear' is anatomy; here it is a site that can be prepared and still empty"),
            ("tuffidu", "pierced — a done opening; the work that looks like it should guarantee the next thing"),
            ("karine", "gold — visible honor, not mere metal; English 'gold' is wealth; here it is the hung sign that most prepared ears never get"),
            ("senete", "is hung / suspended — the gold as an act of hanging, not as a natural fruit of the hole"),
        ),
        "res": res(
            ("Matthew 22:14, many are called, few chosen", "Both split readiness from reward.", "Matthew's election is a king's feast; this mallol is a woman's ear that did its part and still hangs nothing."),
            ("Ecclesiastes 9:11, the race is not to the swift", "Both refuse a world in which preparation automatically collects its due.", "Qoheleth generalizes time and chance; Futa names the ungolded ear."),
        ),
    },
    {
        "n": 18,
        "gaden": "Mallol 90",
        "title": "The One on the Ground Knows the Hour of Return",
        "pul": "denowo boude buri heude bohe, kono gondo e lēidi buri 'andude de hotata.",
        "tr": "The one who climbs the baobabs gets more of their fruits, but the one who stays on the ground knows better when he will come home.",
        "comm": "The claim is a trade, not a sermon against adventure. Height gives fruit. Ground gives the hour of return. Gaden: the one who goes far in search of fortune has more chance of it, and runs far more risk. Futa baobabs are real trees with real fruit; they are also the image of leaving the lēidi, the earth, the known soil. The climber's knowledge is of quantity. The stayer's knowledge is of time: de hotata, when he will come back. Patience here is not meekness. It is knowing your own arrival. The contested move is to refuse a single scale of success. English 'the grass is greener' is envy. This mallol is two knowledges. Existentially: if you are climbing, admit you have bought fruit with ignorance of the hour. If you are on the ground, admit you have bought the hour with fewer fruits. Do not lie that you have both. Honor is accurate accounting of which knowledge you actually hold.",
        "prac": "Say out loud which of the two knowledges you are living this month: more fruit, or the hour of return. Do not claim the other. Make one decision today that matches the knowledge you actually have.",
        "terms": kt(
            ("denowo", "the climber — agent noun of going up; English 'ambitious person' moralizes; this is someone in a tree"),
            ("boude / bohe", "baobabs / their fruits — Sahel wealth as height; not a generic 'opportunity'"),
            ("lēidi", "earth, ground, country — the unclimbed place; English 'ground' is dirt; here it is the known soil that knows the hour"),
            ("hotata", "will return home — the stayer's knowledge; English 'come home' is sentimental; this is a time one can actually know"),
        ),
        "res": res(
            ("Analects 4.1, it is good to feel at home in humaneness", "Both weigh staying against gain.", "Confucius ranks the neighborhood of virtue; this mallol lets both the climber and the stayer be right about different things."),
            ("Odyssey, the man of many turns versus Ithaca", "Both know that fruit abroad costs the hour of return.", "Homer's hero must have both, after twenty years; Futa says you usually have one."),
        ),
    },
    {
        "n": 19,
        "gaden": "Mallol 94",
        "title": "The Stick Leans Where It Despised",
        "pul": "leggel, do yaiti, don 'onorto.",
        "tr": "The small piece of wood — the place it despised is the place it leans on.",
        "comm": "The claim is that refusal does not exempt you from needing the refused. A stick that scorned a spot will rest its weight there. Gaden: one is often obliged to content oneself with a situation one had not wanted at first. Futa speech is dry. The diminutive leggel is back, now as a fool of preference. You do not get a different physics because you had a taste. The contested move is to treat disdain as a future. English 'you'll be glad of it later' is a parent's taunt. This mallol is a posture: 'onorto, it supports itself, there. Patience is not waiting for a better wall. It is noticing that the despised place is already bearing you. Existentially: name one post, job, person, or room you have been leaning on while still narrating your contempt. Stop the narration. Either stand up and leave, or admit the lean. Half-contempt with full weight is the stick's comedy, and it is not a teaching until you feel the lean as a lean.",
        "prac": "Find one place you have been using while calling it beneath you. For today, either stop using it or thank it once, without irony. Do not do both the lean and the insult.",
        "terms": kt(
            ("leggel", "small piece of wood — same diminutive as mallol 72; now the stick is a moral agent of disdain"),
            ("yaiti", "despised, scorned — a completed slight; English 'didn't like' is preference; this is a judgment the stick will have to eat"),
            ("'onorto", "leans / supports itself — the physics of need; English 'ends up' is fate; this is weight placed"),
        ),
        "res": res(
            ("Psalm 118:22, the stone the builders refused", "Both turn a despised place into the thing that bears weight.", "The psalm makes the refuse a cornerstone of God's doing; this mallol makes it the stick's own need, without a hymn."),
            ("Epictetus, Enchiridion 8, do not seek that events happen as you wish", "Both refuse a world arranged around preference.", "Epictetus trains assent; the stick simply leans, having already scorned."),
        ),
    },
    {
        "n": 20,
        "gaden": "Mallol 97",
        "title": "One Grief Does Not Tear the Belly at a Stroke",
        "pul": "mette goto sekata redu lawol gotol.",
        "tr": "A single grief does not tear the belly by a single road.",
        "comm": "The claim is that pain has a pace, and despair is a lie about that pace. One mette does not open the belly in one cut. Gaden: one must not despair of a misfortune or a failure. Futa locates grief in redu, the belly, the same cavity that hunger and kinship occupy. The image is not a stiff upper lip. It is anatomy: tearing takes more than one pass. Lawol gotol — a single road, a single stroke — is the false geometry of panic. The contested move is to refuse the first blow as the whole story. English 'this too shall pass' is a consolation. This mallol is a limit on what one blow can do. Patience (the later Fulfulde muñal is not in Gaden's sentence, but the teaching is the thing) is staying in the un-torn belly long enough to see that the road was only one. Existentially: the next grief, do not narrate ruin. Feel the actual tear. It is not the whole wall. Honor here is not stoic marble. It is not letting one lawol write the book of the body.",
        "prac": "When the next single grief arrives, put a hand on the belly. Say: this is one road. Do not add a second cut with a story of total ruin. Stay until the first blow has been only the first blow.",
        "terms": kt(
            ("mette", "grief, chagrin, a hard turn — not 'sadness' as a mood; a blow that wants to become a tear"),
            ("redu", "belly — seat of feeling and kinship, not a stomach; English 'heart' would misplace it; Futa tears the gut"),
            ("lawol gotol", "a single road / a single stroke — the false geometry of despair; English 'all at once' is time; this is a path"),
            ("sekata", "does not tear — a hard negative; the proverb's mercy is a verb in the negative"),
        ),
        "res": res(
            ("Marcus Aurelius 8.36, do not let the imagination add to the present pain", "Both refuse to let one blow become the whole ruin.", "The emperor trains representation; this mallol trains the belly's actual resistance to a single road."),
            ("Qurʾān 94:5–6, with hardship comes ease", "Both refuse a last word to the first blow.", "The Qurʾān promises ease as God's pairing; this mallol promises nothing but the anatomy of an un-torn belly."),
        ),
    },
    {
        "n": 21,
        "gaden": "Mallol 98",
        "title": "God Has Other Than Leaves for the Couscous",
        "pul": "Alla ina dogi takkudi ko wana hiko.",
        "tr": "God has, to eat with the couscous, something other than foliage.",
        "comm": "The claim is that the refused dish is not the end of the table. Couscous wants a takkudi, an accompaniment. Leaves are a poor one. God has another. Gaden: who has not obtained what he desired must take his part, without despairing of finding something else, and even better. Futa Islam here is not a theodicy. It is a kitchen. Alla is the one who still has a sauce you have not tasted. The contested move is to treat the missed object as the only possible food. English 'God has a plan' is a poster. This mallol is more precise and less soothing: God has another accompaniment. Not your accompaniment. Another. Patience is eating what is actually in the bowl without declaring the kitchen empty. Existentially: name the hiko, the foliage, you have been chewing as if it were the only possible takkudi. Set it down. Ask what else is already on the mat. Do not invent a heaven. Look at the next ordinary food you had been calling a consolation prize. It may be the other thing God had.",
        "prac": "At the next meal, or the next refused outcome, name the foliage you wanted. Then eat what is there without calling it a failure of the table. If something else appears, receive it as takkudi, not as a poor substitute.",
        "terms": kt(
            ("takkudi", "accompaniment eaten with couscous — the second food that makes the staple a meal; English 'side dish' is restaurant talk; this is what the grain requires"),
            ("hiko", "foliage, leafage — a poor sauce; English 'greens' can be a delicacy; here leaves are what you settle for when you think the kitchen is empty"),
            ("Alla", "God — the same Name as mallol 78; here as a holder of other food, not as a judge"),
            ("ina dogi", "has / possesses — God's having as a present store, not a future plan"),
        ),
        "res": res(
            ("Matthew 6:26, your Father feeds the birds", "Both locate provision outside the anxious menu.", "Jesus forbids anxiety; this mallol forbids declaring the sauce to be only leaves."),
            ("Job 38–39, God as the one who still has stores the sufferer has not seen", "Both answer a refused desire with a larger kitchen.", "Job is whirlwind and cosmology; Futa is couscous and a better takkudi."),
        ),
    },
    {
        "n": 22,
        "gaden": "Mallol 104",
        "title": "Let the Unsupplied Man Do More Than He Says",
        "pul": "so gorko 'ala di, 'ala dam, 'ala be, ko dedata yo bur heude e ko hālala.",
        "tr": "If a man has neither food, nor drink, nor people, let him do more than he will say.",
        "comm": "The claim is that speech is a luxury of the supplied. Di, dam, be — food, drink, people — are the three stores. Without them, the mouth should undershoot the hands. Gaden: the poor man is obliged to suffer many affronts without speaking; the mallol is said especially of a poor husband with a rich wife. Futa honor here is a silence that is not meekness. It is arithmetic. Words cost a backing you do not have. Hālala, what he will say, should be less than dedata, what he does. The contested move is to treat talk as free. English 'actions speak louder' is a cliché. This mallol is harsher: if you lack the three stores, your extra speech is already a debt. Existentially: count your stores before your next sentence. If you are short of food, drink, or people — of backing — cut the sentence and keep the act. Speech that outruns supply is how the unsupplied man is torn. Patience is the extra deed that does not require an audience.",
        "prac": "Before you speak a need or a boast today, count: food, drink, people. If any of the three is thin, do one more silent act than you had planned to announce. Let the deed outrun the sentence.",
        "terms": kt(
            ("di / dam / be", "food / drink / people — the three stores; English 'resources' is abstract; these are a plate, a cup, and a kin-group"),
            ("hālala", "what he will say — speech as a future expenditure; English 'talk' is cheap; here it is costed against the stores"),
            ("dedata", "what he does / will do — the surplus that should exceed speech"),
            ("gorko", "a man — the proverb's subject in a polygynous honor-world; Gaden notes the poor husband especially"),
        ),
        "res": res(
            ("Analects 4.24, the gentleman is slow to speak and prompt in action", "Both rank deed above word, especially under constraint.", "Confucius trains a gentleman; this mallol trains a man whose three stores are empty."),
            ("James 2:15–16, go in peace without giving food", "Both refuse speech that is not backed by a plate.", "James accuses empty blessing; Futa tells the unsupplied man not to be that mouth."),
        ),
    },
    {
        "n": 23,
        "gaden": "Mallol 107",
        "title": "Age-Mates Walk Arm in Arm, and Each Can Go His Road",
        "pul": "gidirabe fingodirta ko hā iela, kono gōto fuf ina wāwi yade lawol mum.",
        "tr": "Age-mates go arm in arm so that it may be pleasant, but each one can go his own road.",
        "comm": "The claim is that companionship is a pleasure, not a necessity. Gidirabe, comrades of an age-set, walk fingodirta, arm in arm, for iela, the pleasantness of it. Then the blade: each can take lawol mum, his own path. Gaden: it is agreeable to be with a friend, but one can do without him. Futa honor does not make the friend a limb. The heart is not a joint; the friend is not a joint either. You may walk linked. You may unhook. The contested move is to refuse both loneliness-as-virtue and friendship-as-fusion. English 'we all need people' is a therapy. This mallol is drier: we like people. We can go. Existentially: notice one arm-in-arm you have been treating as a spine. Walk a stretch of your own road today without a speech of independence. If the friendship is real, it will survive the unhooking. If it was a hinge you had mistaken for a self, you will feel the difference. That feeling is the teaching.",
        "prac": "Walk or work one hour without the person you usually lean on for the pleasantness of it. Do not announce a break. Just take lawol mum for that hour, then return without a report.",
        "terms": kt(
            ("gidirabe", "age-mates, comrades of a set — not generic 'friends'; a Fulɓe social form of same-age bonding"),
            ("fingodirta", "go arm in arm — reciprocal linked walking; English 'hanging out' loses the bodies"),
            ("iela", "pleasantness, the agreeable — the honest motive; not duty, not destiny"),
            ("lawol mum", "his own road — the same lawol as grief's single road in mallol 97; here it is freedom of path, not a blow"),
        ),
        "res": res(
            ("Aristotle, Nicomachean Ethics VIII–IX, friendship as a good, not as being", "Both honor companionship without making it the substance of the person.", "Aristotle ranks friendships of virtue; this mallol simply notes that the arm can unhook."),
            ("Dhammapada 23, walk alone like a rhinoceros if need be", "Both allow the unaccompanied road.", "The Buddhist verse prefers solitude as purity; Futa prefers arm-in-arm and only then mentions that each can go."),
        ),
    },
    {
        "n": 24,
        "gaden": "Mallol 128",
        "title": "The Head Must Trust the Razor First",
        "pul": "hore, so molanāki pemborki Alla, pemborki mōlantāko hore Alla.",
        "tr": "The head, if it has not trusted the razor of God, the razor will not trust the head of God.",
        "comm": "The claim is that trust is not symmetric until the needy one moves. A head needs a razor. A razor does not need a head. Gaden: if the inferior does not go to his superior, the superior will ignore him. Then a theological shrug that is almost comic: the razor, the head, every thing belongs to God; the word Alla adds nothing to the sense. That 'nothing' is the teaching. You cannot wait for the instrument to come looking for you. You go. The contested move is to reverse the hunger. English 'meet halfway' is a couple's advice. This mallol is a barber: the hair does not negotiate. Existentially: name one razor you have been waiting to come to your head — a teacher, a judge, a helper, a God. Go. If you will not go, stop calling the delay their coldness. It was your unmoved skull. Hearing sits inside this: molanāki, has not trusted, is a completed non-event. Trust is an act toward the blade, not a feeling that the blade should have first.",
        "prac": "Go toward one person or practice you have been waiting to come to you. Make the first ordinary move — a question, an appointment, a kneeling. Do not wait for the razor to miss you first.",
        "terms": kt(
            ("hore", "head — the needy party; English 'head' is leadership; here it is the thing that has hair and must approach"),
            ("pemborki", "razor — the superior instrument; Gaden's gloss is chief and inferior, not grooming as vanity"),
            ("molanāki / mōlantāko", "has not trusted / will not trust — trust as a verb that must be initiated by the needy; English 'trust' is a feeling; this is an approach"),
            ("Alla", "of God — Gaden says the word adds nothing because everything is already God's; the Name here is a reminder, not a second plot"),
        ),
        "res": res(
            ("Qurʾān 2:186, let them come to Me, I answer the caller", "Both put the first step on the needy one.", "The Qurʾān promises an answer; this mallol promises nothing but that an unmoved head will not be sought by the razor."),
            ("Meister Eckhart, on the soul going out to God", "Both refuse a God (or a blade) that must hunt the one who needs cutting.", "Eckhart's going-out is Gelassenheit; Futa's is a head walking to a barber."),
        ),
    },
    {
        "n": 25,
        "gaden": "Mallol 147",
        "title": "What Fruits Begins by Flowering",
        "pul": "ko ina dibina fidat.",
        "tr": "What produces fruit begins by flowering.",
        "comm": "The claim is sequence as verdict. Flower is not decoration. It is the first form of the fruit. Gaden: same sense as the dawn mallol; from the flowering one already knows whether the harvest will be abundant. He notes the two aorists, in a and in at: the plant must first flower. Grammar is the teaching. You do not get fidat, fruiting, without dibina, flowering. Pair this with subaka moddo 'andeté ko gila fadiri: first light, first blossom, first five minutes. Futa speech keeps saying the beginning is already knowledge. The contested move is to treat openings as reversible cosmetics. English 'don't judge a book by its cover' is a warning against haste. This mallol is a warning against delay: the cover was already the fruit's first body. Existentially: look at what is flowering in a work, a love, a speech. Do not wait for the edible stage to decide what it is. Change the blossom, or accept the fruit it already is. Cause and dawn meet here: the sababu of a harvest is visible as a flower.",
        "prac": "Look at one project or relation in its current blossom — the tone of the first messages, the first habit. Name the fruit that blossom already is. If you do not want that fruit, change today's flower, not next season's speech.",
        "terms": kt(
            ("dibina", "is flowering / producing blossom — the obligatory first aorist; English 'bloom' is pretty; here it is already the harvest's form"),
            ("fidat", "fruits, comes to fruit — the second aorist; Gaden's grammatical note is the philosophy: it must first flower"),
            ("ko ina", "that which is (in the act of)... — a process named as a subject, not a static tree"),
        ),
        "res": res(
            ("Mallol 146 of this collection, the good morning known from dawn", "Both make the beginning already a knowledge of the end.", "146 is temporal (first light); 147 is botanical sequence. Same Futa method, two images."),
            ("Matthew 7:16–20, a good tree cannot bear bad fruit", "Both read fruit from an earlier form of the plant.", "Matthew argues nature of the tree; Futa argues obligatory sequence: flower, then fruit."),
        ),
    },
    {
        "n": 26,
        "gaden": "Mallol 148",
        "title": "The Herder Will Not Fall Short of Ganna",
        "pul": "'aga dasata Ganna, boggol dasata woidu.",
        "tr": "The herder will not be inferior to Ganna; the rope will not be shorter than the well is deep.",
        "comm": "The claim is adequacy as a matching of lengths, not as a boast. Ganna is a named Fulɓe herder whose reputation stuck to Futa: a measure of the craft. The 'aga, the herder in view, will not fall short of that measure — and the proof is the second clause: the well-rope will not be shorter than the well. Gaden: said of a child walking in the father's traces, for good or ill. Herd and blood again. Transmission is not a lecture (the heifer suckles what the cow ate). It is a rope cut to a depth. The contested move is to treat lineage as either doom or trophy. This mallol is drier: the length will match. If the father was Ganna, the rope is long. If the well is deep, do not bring a short cord and call it independence. Existentially: measure one inherited craft or vice as a rope against a well. Stop claiming you have a different length. If the match is bad, splice. If it is good, draw water. Honor in the herd-world is not originality. It is a rope that reaches.",
        "prac": "Name the Ganna in your line — the person whose craft or fault you are walking in. Measure one act today against that length. Lengthen the rope if it does not reach; stop pretending the well is shallower than it is.",
        "terms": kt(
            ("'aga", "herder, shepherd — the working Fulɓe title; English 'cowboy' is a costume; this is the person whose rope must reach water"),
            ("Ganna", "a named Futa herder of reputation — a local measure of excellence, not a mythic ancestor; English loses the proper name"),
            ("boggol", "rope — well-rope, the tool that must match depth; English 'resources' is vague"),
            ("woidu", "well — the depth that judges the rope; not a wishing-well, a working shaft"),
            ("dasata", "will not be inferior / will not fall short — a future of matching; English 'won't fail' is a pep talk; this is a length"),
        ),
        "res": res(
            ("Mallol 145 of this collection, what the cow ate the heifer suckles", "Both transmit a parent's measure into the child's body of work.", "145 is milk; 148 is a rope cut to a well. Same herd metaphysics, two tools."),
            ("Luke 6:40, a disciple is not above his teacher", "Both measure the younger against a named excellence.", "Luke aims at becoming like the teacher; Futa aims at a rope that reaches the same water."),
        ),
    },
    {
        "n": 27,
        "gaden": "Mallol 150",
        "title": "The Cow Steps on Her Calf and Does Not Hate",
        "pul": "nagge ina yabba bidum, kono 'anāni.",
        "tr": "The cow puts her foot on her young — yet she does not hate.",
        "comm": "The claim is that correction is not hatred. A cow's hoof on a calf looks like violence. It is weight, placement, the herd's rude care. Gaden: parents may correct their children without, for that, not loving them. Futa will not let the calf write the theology of the hoof. 'Anāni, she does not hate — the negative is the teaching. You may feel the foot and still be inside the love. The contested move is to equate pain with enmity. English 'tough love' is a slogan that often hides abuse. This mallol is more careful and more dangerous: it can excuse a cruel parent, and it can also save a true correction from being misread as exile. Read it with the heart that will not bend and the father who will not wish shame. Discipline that destroys koyēra is not this hoof. Discipline that keeps the calf in the herd is. Existentially: the next time a weight lands on you from someone whose herd you are actually in, ask whether the foot is hate or placement. If it is hate, leave. If it is placement, stop narrating exile. The cow's hoof is not a joint either. It does not wait for your feeling to agree.",
        "prac": "If you are the cow: correct one thing today without adding a speech of rejection. If you are the calf: receive one correction without answering it as hatred. Choose the side you are actually on, and do only that one act.",
        "terms": kt(
            ("nagge", "cow — again the parent-body of mallol 145; the herd's first theologian"),
            ("yabba", "puts the foot on, treads — a physical correction; English 'disciplines' is abstract; this is a hoof"),
            ("bidum", "her young, her offspring — not a generic child; the calf of this cow"),
            ("'anāni", "she does not hate — the proverb's whole philosophy in a negative; English 'still loves' adds a warmth the Pulaar does not gild"),
        ),
        "res": res(
            ("Hebrews 12:6, the Lord disciplines the one he loves", "Both refuse to read the blow as proof of rejection.", "Hebrews theologizes a Father-God; this mallol stays with a cow and a calf in a herd."),
            ("Mallol 70 of this collection, the heart is not a joint", "Both refuse to let commanded feeling replace the actual inner.", "70 protects the heart from being bent; 150 protects the hoof from being misread as hate. Together they split conduct from the story the feeling tells."),
        ),
    },
    {
        "n": 28,
        "gaden": "Mallol 151",
        "title": "He Will Not Speak of His Father's Marriage",
        "pul": "ko neddo boni nēdi kon fuf, hālatal tuddugu bammum.",
        "tr": "However badly raised a person is, he will not speak of his father's marriage.",
        "comm": "The claim is that honor is a silence that survives even a ruined upbringing. Nēdi, raising, can fail. The mouth still stops at tuddugu bammum, the father's marriage. Gaden: it is especially shameful for a Toucouleur to speak of his parents' marriage; it is not the son who will say ill of his father. Speech has a last fence. You can be badly made and still not take that fence down. The contested move is to treat honesty as a license to strip the house. English 'I have to tell my truth' can be a raid on the parents' bed. This mallol says: not that. Koyēra, the shame the dying father ranked above death, lives here as a refused sentence. Existentially: there is a story you have been calling candor that is actually a raid. Do not tell it. The teaching is not that families are holy. It is that some speech, once loosed, is not knowledge. It is koyēra spent. A badly raised person who still will not spend it has kept one piece of the name. That piece is the practice.",
        "prac": "Identify one true fact about a parent or a house that would strip them in a room they are not in. Do not tell it today. Keep the silence as the one act. If you must speak, speak of your own conduct, not of their marriage.",
        "terms": kt(
            ("nēdi", "raising, upbringing — the making of a person; English 'education' is school; this is how a house forms a mouth"),
            ("hālatal", "will not speak — the same speech-root as mallol 104; here a future refusal, not a poverty of words"),
            ("tuddugu", "marriage — the parents' union as a forbidden topic; English 'marriage' is a status; here it is a privacy the son does not get to loot"),
            ("bammum", "his father — the named limit; Gaden's Toucouleur shame is already in this 1913 sentence"),
        ),
        "res": res(
            ("Exodus 20:12, honor your father and your mother", "Both put a fence around speech about the parents.", "The commandment is a duty toward living parents; this mallol is a last fence that even a badly raised mouth will not cross."),
            ("Analects 1.11, while the father is alive, observe his will", "Both make the father's life a limit on the son's display.", "Confucius watches conduct across a death; Futa forbids a particular sentence about the marriage itself."),
        ),
    },
]


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.{SLUG}_{n:03d}"
    hero = n in HEROES
    original = u["pul"]
    layers = [
        {"kind": "original", "label": "Original", "body": original},
        {"kind": "iast", "label": "Romanization", "body": original},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"PUL_{n:03d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": u["gaden"],
        "title": u["title"],
        "unit_type": "verse",
        "commentary": u["comm"],
        "themes": ["pulaar", "mallol", "living speech", "futa toro"],
        "tags": [SLUG, "pulaar", "mallol", "futa-toro"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "category": "pulaar",
            "verse": str(n),
            "gaden": u["gaden"],
            "cultural_context": NOTE,
            "original_source": "Gaden, Le Poular, t. I Textes (Paris: Leroux, 1913)",
            "original_reliability": "SOURCED — Gaden 1913 Latin transcription of Futa Toro Ajami, lightly cleaned of OCR junk; not Gaden 1931",
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": original,
        "transliteration": original,
    }
    if hero:
        unit["tts_key"] = True
    path = os.path.join(OUT, f"{uid.replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return uid


def build() -> int:
    short = [(u["n"], len(u["comm"].split())) for u in UNITS if len(u["comm"].split()) < 150]
    if short:
        raise SystemExit(f"commentary under 150 words: {short}")
    if len(UNITS) < 28:
        raise SystemExit(f"floor is 28 units, got {len(UNITS)}")
    if len(HEROES) != 10:
        raise SystemExit(f"need 10 heroes, got {sorted(HEROES)}")
    missing = HEROES - {u["n"] for u in UNITS}
    if missing:
        raise SystemExit(f"heroes not in UNITS: {sorted(missing)}")
    os.makedirs(OUT, exist_ok=True)
    ids = [write_unit(u) for u in UNITS]
    keep_files = {f"{uid.replace('.', '_')}.yml" for uid in ids}
    removed = 0
    for name in os.listdir(OUT):
        if name.endswith(".yml") and name not in keep_files:
            os.remove(os.path.join(OUT, name))
            removed += 1
    hero_ids = [f"{SLUG}.{SLUG}_{u['n']:03d}" for u in UNITS if u["n"] in HEROES]
    print(f"{SLUG}: {len(ids)} units (min 28) · heroes {[u['n'] for u in UNITS if u['n'] in HEROES]}")
    print(f"tts_key ids: {hero_ids}")
    print(f"wrote {len(ids)} yml to {OUT}" + (f" (removed {removed} stale)" if removed else ""))
    return len(ids)


if __name__ == "__main__":
    build()
