#!/usr/bin/env python3
"""Ingest John Wyndham, *Myths of Ífè* (London: Erskine Macdonald, 1921).

Public-domain source: recitation of the Ìfẹ̀ high priests (Òrní and Babaláwo
Arába) taken down by a colonial Assistant District Officer and recast as
English blank verse by Wyndham. Yoruba speech was not written down.

English is a Pratibha rendering (pd_adapted). The Original layer is Wyndham's
1921 English of the priest recitation. This is NOT M.A. Fabunmi (1969, not PD)
and does not follow any later copyrighted Ife ethnography.

Outsider English verse of insider recitation. The layers restore the
philosophical claim without adopting colonial framing, "fetish," or Wyndham's
Golden Bough guesses as doctrine. Ceremonial how-to (sacrifice recipes,
circumcision, festival license instructions) is excluded; the mythic argument
is kept.

Floor: ≥28 units. Ten tts_key heroes.
"""
from __future__ import annotations

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/myths_of_ife")
SLUG = "myths_of_ife"
COLL = "Myths of Ìfẹ̀"
THEMES = ["yoruba", "ife", "orisha", "oduduwa", "living speech"]
ROMAN = "Wyndham 1921 English of Ìfẹ̀ priest recitation"

PROV = (
    "English is a Pratibha rendering (pd_adapted) from John Wyndham, "
    "*Myths of Ífè* (London: Erskine Macdonald, 1921), public domain. "
    "Original layer is Wyndham's 1921 English of the Ìfẹ̀ priest recitation "
    "(Yoruba speech was not written down). Does not follow Fabunmi 1969 or "
    "any later copyrighted Ife ethnography."
)
NOTE = (
    "Outsider English verse of insider recitation. Recited by Ìfẹ̀ high "
    "priests (Òrní and Babaláwo Arába) to a colonial ADO; English blank verse "
    "is Wyndham's. Restore the philosophical claim without adopting colonial "
    "framing, \"fetish,\" or Wyndham's Golden Bough guesses as doctrine. "
    "Ceremonial how-to (sacrifice recipes, circumcision, festival license "
    "instructions) is excluded; the mythic argument is kept."
)

# Ten hero verses — mandala quotes + pre-baked Listen.
HEROES = {1, 3, 4, 6, 7, 11, 14, 19, 24, 28}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


UNITS: list[dict] = [
    {
        "n": 1,
        "title": "Where Truth Has Its Home",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "Oíbo, you have asked to hear our lore,\n"
            "The legends of the World's young hours—and where\n"
            "Could truth in greater surety have its home\n"
            "Than in the precincts of the shrines of Those\n"
            "Who made the World, and in the mouths of priests\n"
            "To whom their doings have been handed down\n"
            "From sire to son?"
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Òrní (religious head of Ìfẹ̀); "
            "Oíbo (white man, the colonial addressee)."
        ),
        "tr": (
            "You have asked to hear our lore, the legends of the world's young "
            "hours. Where could truth have a surer home than at the shrines of "
            "Those who made the World, and in the mouths of priests to whom "
            "their doings have been handed down from sire to son?"
        ),
        "comm": (
            "The claim is that truth is not a book and not a private vision but "
            "a place plus a mouth: shrine precincts of the makers, and priests "
            "who inherit speech. The Òrní opens the recitation by locating "
            "epistemology before cosmology. He does not first prove that the "
            "gods exist. He answers the colonial question — tell us your lore — "
            "by refusing the implied geography of knowledge. Truth does not "
            "travel better in a district officer's notebook than it lives at "
            "the shrines. Greater surety belongs to the precincts and the "
            "line of mouths. This is living speech as a philosophical method. "
            "The world was made by Those who still have altars; the making is "
            "not a closed past event but a presence that can be pronounced. "
            "Handed down from sire to son is not a footnote about orality. It "
            "is the claim that reliability is genealogical: a priest is a "
            "correct vessel because the words have already been tested by a "
            "line of speakers, not because a text has been frozen. Wyndham's "
            "blank verse is already a second remove — English of Yoruba that "
            "was not written down — and the unit must not pretend otherwise. "
            "The philosophical remainder is still sharp. Modern cultures "
            "locate truth in publication, laboratory, or confession. Ìfẹ̀ "
            "locates it where the makers are tended and where a mouth is "
            "authorized to speak them. Existentially, the teaching asks where "
            "you actually go when you want something true: a feed, a private "
            "feeling, or a place and a lineage that can correct you."
        ),
        "prac": (
            "Today, do not look up a teaching first. Go to one actual place "
            "where a practice is kept — a shrine, a table, a room that has "
            "held the same words longer than you have — and listen for one "
            "sentence that is handed, not invented. Write that sentence down "
            "as received, not improved."
        ),
        "terms": kt(
            (
                "lore",
                "Wyndham's English for the Òrní's recited knowledge -> not "
                "folklore-as-entertainment but the world's young hours kept "
                "at shrines -> \"myth\" in the dismissive sense misses that "
                "the speaker claims greater surety, not lesser",
            ),
            (
                "Òrní",
                "religious head of Ìfẹ̀ in this recitation (Wyndham: Órní) -> "
                "the living mouth through which Odudúwa and Orísha still "
                "speak -> \"king\" or \"chief\" flattens the claim that a "
                "body can host the makers",
            ),
            (
                "shrines of Those Who made the World",
                "precincts of the makers as the home of truth -> knowledge "
                "has a topology: you go where the makers are tended -> "
                "\"temple\" is too building-like; the surety is precinct plus "
                "priestly mouth",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Olorun, the Lord of Heaven\"",
                "Both place Yoruba knowledge of the highest in a structured "
                "relation — Johnson by naming Olorun as too exalted for direct "
                "business, the Òrní by seating truth at the makers' shrines "
                "and in priestly mouths.",
                "Johnson writes as a Yoruba clergyman in prose theology; this "
                "unit is an Ìfẹ̀ priest answering a colonial hearer, and it "
                "locates surety in shrine and lineage rather than in a reserved "
                "name for God alone.",
            ),
            (
                "Lalla Vakyani, \"I Found Him in My Own House\"",
                "Both refuse a distant archive of truth and insist that what "
                "matters is found where a life already stands — house for "
                "Lalla, shrine-mouth for the Òrní.",
                "Lalla's house is the inward finding of Śiva; the Òrní's home "
                "of truth is public precinct and inherited speech, not a "
                "solitary recognition.",
            ),
        ),
    },
    {
        "n": 2,
        "title": "Arámfè Made Heaven from Mass",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "You have not even heard\n"
            "Of the grey hour when my young eyes first opened\n"
            "To gaze upon a herbless Mass, unshaped\n"
            "And unadorned. I laboured and the grim years passed:\n"
            "The unshapely I had formed to beauty,\n"
            "And as the ages came I loved to make\n"
            "The beautiful more fair. . . All went not well."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Arámfè (father of the gods, thunder; "
            "spoken of as God). Him-Who-Speaks-Not is Wyndham's English for "
            "the higher distant Being some priests mention."
        ),
        "tr": (
            "You have not even heard of the grey hour when my young eyes first "
            "opened on a herbless Mass, unshaped and unadorned. I knew the "
            "heart of Him-Who-Speaks-Not, the far-felt Purpose that gave me "
            "birth. I laboured. Streams, stars, hills, and birdsong came. I "
            "formed the unshapely to beauty, and then loved to make the "
            "beautiful more fair. All did not go well."
        ),
        "comm": (
            "The claim is that heaven is achieved work, not a given palace, "
            "and that achievement does not cancel failure. Arámfè's sons know "
            "only wine, chorus, and sunrise. He remembers Mass: herbless, "
            "unshaped, unadorned. Creation here is not a word that instantly "
            "completes a world. It is grim years, hazardous leading of "
            "unshapely stuff along a cliff's-edge way toward Paradise. The "
            "counterintuitive move is the last clause. All went not well. A "
            "noble animal emerges loathsome; a river tears its banks; "
            "cataract and precipice remain as scars of days when Heaven "
            "tottered. The father of the gods does not hide the wreckage "
            "inside a doctrine of omnipotent ease. He makes it the content of "
            "godhead: if the accomplished whole is Heaven, the anxious years "
            "are a destiny for gods. This is not Wyndham's Golden Bough "
            "guesswork and not a colonial fable of primitive cosmology. It is "
            "an Ìfẹ̀ argument about what it means to be a maker. Beauty is "
            "not the opposite of labour. Beauty is labour that has learned "
            "to love increment — and still admits predation, flood, and "
            "rift. Existentially, the teaching cuts the wish that a good "
            "order, once founded, should stay effortless. If even Heaven "
            "remembers tottering, your own making is not disqualified by "
            "the parts that went badly. The work is to keep forming, and to "
            "say the failure without surrendering the Purpose that gave the "
            "work birth."
        ),
        "prac": (
            "Name one thing you made that later tore its banks or came out "
            "loathsome. Do not scrap the whole. Spend twenty minutes repairing "
            "one edge of it, as Arámfè kept the scarred hills inside Heaven."
        ),
        "terms": kt(
            (
                "Arámfè",
                "father of the gods, thunder, often spoken of as God in this "
                "recitation -> maker who remembers Mass and tottering, not "
                "an idle sky-king -> collapsing him into Olorun from later "
                "handbooks imports a name Wyndham's priests do not use here",
            ),
            (
                "Mass",
                "herbless, unshaped, unadorned stuff before Heaven -> the "
                "given that must be led, not the enemy of godhead -> "
                "\"chaos\" is too Greek; Mass is nerveless and cold, awaiting "
                "labour",
            ),
            (
                "All went not well",
                "Arámfè's verdict on his own making -> failure belongs inside "
                "divine work, not after it as a human accident -> "
                "omnipotence-as-ease is the default this line refuses",
            ),
        ),
        "res": res(
            (
                "Psalms (Tehillim), Psalm 104",
                "Both remember creation as the setting of bounds, waters, "
                "hills, and living things rather than as a finished ornament "
                "dropped from nowhere.",
                "The psalm praises YHWH whose word and wisdom hold the order; "
                "Arámfè narrates grim years, tottering, and a Mass that did "
                "not all go well.",
            ),
            (
                "Tao Te Ching 25",
                "Both set a prior, almost unshapely something before the "
                "named heavens and the work of ordering.",
                "The Dao is nameless and does not labour as a father-god; "
                "Arámfè is a worker who knows a still higher Purpose and "
                "admits that parts of the work preyed on other parts.",
            ),
        ),
    },
    {
        "n": 3,
        "title": "Him-Who-Speaks-Not",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "But I knew well the heart\n"
            "Of Him-Who-Speaks-Not, the far-felt Purpose that gave\n"
            "Me birth; I laboured and the grim years passed:\n"
            "Streams flowed along their sunny beds; I set\n"
            "The stars above me, and the hills about."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: none beyond Arámfè. Him-Who-Speaks-Not is "
            "Wyndham's English for the higher distant Being some priests "
            "mention; it is not a recovered Yoruba name."
        ),
        "tr": (
            "I knew well the heart of Him-Who-Speaks-Not, the far-felt Purpose "
            "that gave me birth. I laboured, and the grim years passed. "
            "Streams found sunny beds. I set the stars above me and the hills "
            "about me."
        ),
        "comm": (
            "The claim is that even the father of the gods is not the last "
            "word. Arámfè makes Heaven, later sends sons, later hurls "
            "thunderbolts, and still names a higher: Him-Who-Speaks-Not, a "
            "far-felt Purpose that gave him birth. The priests, in Wyndham's "
            "Persons list, mention a higher and very distant Being; they do "
            "not give that Being a bargain-name. Silence is the doctrine. "
            "The contested move is hierarchical without being a ladder you "
            "climb. Arámfè is not a demigod waiting to be promoted. He is "
            "God for the recitation — thunder, father, maker — and he knows "
            "he is derived. Purpose precedes speaker. The one who does not "
            "speak is not mute from weakness; speech is what the middle gods "
            "do when they found worlds and argue. The highest is felt, not "
            "addressed. This must not be filled with later ethnography or "
            "with Olorun imported from Johnson as if the names were already "
            "the same sentence. What the Ìfẹ̀ recitation actually gives is "
            "the structure: a working god who can fail and thunder, and "
            "behind him a Purpose that does not enter the market of prayer. "
            "Existentially, the line trains a check on spiritual chatter. "
            "If the maker of Heaven labours from a Purpose that will not "
            "talk, your own urgency to get a voice from the absolute may be "
            "a confusion of ranks. Do the work the Purpose implies. Do not "
            "demand that the last source explain itself in your ear."
        ),
        "prac": (
            "Sit ten minutes without asking the highest for a word. Let "
            "purpose be far-felt, not answered. Then do one piece of shaping "
            "work as if labour were the only speech you are owed."
        ),
        "terms": kt(
            (
                "Him-Who-Speaks-Not",
                "Wyndham's English for the higher distant Being some Ìfẹ̀ "
                "priests mention -> Purpose that births Arámfè, not a cult "
                "addressee -> inventing a Yoruba proper name for this figure "
                "exceeds the source",
            ),
            (
                "far-felt Purpose",
                "how Arámfè knows that silent source -> knowledge as "
                "pressure and orientation, not conversation -> \"will of "
                "God\" is too speech-like; this Purpose does not speak",
            ),
            (
                "gave Me birth",
                "Arámfè is derived, not self-originating -> godhead in this "
                "myth is middle: maker of Heaven, child of Silence -> "
                "\"first cause\" language erases the birth",
            ),
        ),
        "res": res(
            (
                "Plotinus, Enneads VI.9.6, \"The Unity Beyond Human Conception\"",
                "Both place a last source beyond the speaking, shaping gods "
                "and beyond what can be handled as an object of address.",
                "Plotinus's One is approached by the soul's interior ascent; "
                "Him-Who-Speaks-Not is named by a working thunder-father who "
                "then turns back to streams, stars, and hills.",
            ),
            (
                "Senegalese Animism, \"The Invisible Master Is Named as the Sky\"",
                "Both keep a supreme that is known and yet not turned into "
                "the ordinary addressee of cult.",
                "Serer Rog shares a name with the sky and takes satisfaction "
                "in the good; Him-Who-Speaks-Not is more remote still, a "
                "Purpose behind Arámfè, without even a sky-name in this "
                "recitation.",
            ),
        ),
    },
    {
        "n": 4,
        "title": "Kingship and the Bag",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "Odúwa, first-born of my sons, to you I give\n"
            "The five-clawed Bird, the sand of power. . .\n"
            "You are their judge; Yours is the kingship. . .\n"
            "Wisest of my sons, Orísha, yours is the grateful\n"
            "task to loose Vague spirits waiting for the Dawn\n"
            "—to make the race that shall be; and to you I give\n"
            "This bag of Wisdom's guarded lore and arts\n"
            "For Man's well-being and advancement."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odúwa / Odudúwa (first-born, king of men); "
            "Orísha (wisest son, maker of the race); the five-clawed Bird "
            "and the bag of lore."
        ),
        "tr": (
            "Odúwa, first-born, receives the five-clawed Bird and the sand of "
            "power: call a despairing land to life above the jealous sea, "
            "found homesteads, judge a race that will not live as gods. "
            "Kingship is his. Orísha, wisest, receives the task of loosing "
            "vague spirits who wait for dawn — and the bag of Wisdom's "
            "guarded lore and arts for the well-being of that race."
        ),
        "comm": (
            "The claim is that founding a world requires a split the first-born "
            "will hate: rule is not the same gift as lore. Arámfè does not "
            "hand one son the whole of Heaven's competence. Odúwa gets bird, "
            "sand, kingship, judgment — the power to make land and to be "
            "obeyed. Orísha gets the bag and the work of making people from "
            "spirits that are still only waiting. The younger sons get chorus, "
            "dance, worship, crafts: mirth and labour. A mortal race is "
            "explicitly not destined for the eternal life of gods. The "
            "counterintuitive move is to call Orísha's task grateful. Wisdom "
            "looks like the better portion because hearts will turn to the "
            "god who spells strange benefits. Arámfè has already decided that "
            "kingship without arts is one office, and arts without the crown "
            "another. Ìfẹ̀ political theology starts here, before the theft. "
            "Empire can raise land from water and still lack the clue that "
            "wakes lore. Craft can shape a people and still owe judgment to "
            "a brother. Later war is not a foreign accident; it is this "
            "division refused. Existentially, the teaching asks which bag "
            "you keep grabbing. Many lives treat every gift as incomplete "
            "until it includes the other office — status plus technique, "
            "voice plus veto. Arámfè's sentence is colder and kinder: a "
            "fitting task is already a world. The disaster begins when the "
            "king decides that kingship is cheated unless it also owns the "
            "arts."
        ),
        "prac": (
            "Write two lists: what you actually hold (your bird and sand) and "
            "what you keep trying to seize from a sibling office (someone "
            "else's bag). Return one seized item — a credit, a decision, a "
            "craft — to the person whose task it is."
        ),
        "terms": kt(
            (
                "Odúwa / Odudúwa",
                "first-born son of Arámfè, given bird, sand, and kingship -> "
                "judge of a mortal race, not owner of all gifts -> later "
                "ethnographic Oduduwa-as-sole-founder collapses the split "
                "this recitation insists on",
            ),
            (
                "Orísha",
                "wisest son, looser of vague spirits, keeper of the bag -> "
                "maker of humankind and of arts, not the crown -> English "
                "\"orisha\" as any deity is wider; here Orísha is a person "
                "in the story, the Great",
            ),
            (
                "bag of Wisdom's guarded lore and arts",
                "Arámfè's gift to Orísha for man's well-being -> portable "
                "competence, not a throne -> \"magic sack\" misses that the "
                "bag is pedagogy waiting for the right teacher",
            ),
        ),
        "res": res(
            (
                "Bhagavad Gita 18.43–45, \"Own Work as the Path to Success\"",
                "Both assign different offices rather than one total "
                "competence, and treat the fitting task as the way a world "
                "holds.",
                "The Gita grounds the split in guṇa and svadharma toward "
                "Krishna; Arámfè splits kingship from lore inside a single "
                "divine family, and the plot will turn on the refusal of "
                "that split.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith, \"Shaped by the Hand of Orisala\"",
                "Both give a shaping god a share in making humankind beside "
                "a higher maker — Johnson's Orisala beside Olorun, this "
                "recitation's Orísha beside Arámfè.",
                "Johnson's Orisala shapes a lump God has already made; "
                "Orísha here receives a bag of arts and the work of loosing "
                "spirits, while land and kingship go to Odúwa.",
            ),
        ),
    },
    {
        "n": 5,
        "title": "Odúwa Protests the Gift",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "Yet, Lord Arámfè,\n"
            "I am your first-born: wherefore do you give\n"
            "The arts and wisdom to Orísha? I,\n"
            "The King, will be obeyed; the hearts of men\n"
            "Will turn in wonder to the God who spells\n"
            "Strange benefits. But Arámfè said \"Enough;\n"
            "To each is fitting task is given. Farewell.\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odúwa (first-born, already speaking as "
            "King); Orísha (the one given arts)."
        ),
        "tr": (
            "Odúwa answers: I am first-born; why give arts and wisdom to "
            "Orísha? I, the king, will be obeyed, and the hearts of men will "
            "turn in wonder to the god who spells strange benefits. Arámfè "
            "says only: Enough. To each a fitting task is given. Farewell."
        ),
        "comm": (
            "The claim is that primogeniture does not entitle a king to every "
            "wonder, and that the father will not argue the point. Odúwa "
            "has already accepted exile and homesteads. What he cannot "
            "accept is a rival magnet. He predicts, correctly, that men will "
            "love the god of benefits more than the god of obedience. The "
            "protest is political psychology, not mere spite: a crown that "
            "cannot spell strange goods will be obeyed in form and deserted "
            "in love. Arámfè's answer is almost rude. Enough. Fitting task. "
            "Farewell. There is no theodicy of the split, no promise that "
            "hearts will come around, no extra portion to soothe the "
            "first-born. The contested move is the refusal to optimize the "
            "gift for the king's self-image. Heaven does not redesign "
            "offices so that the ruler also owns pedagogy. This is the last "
            "calm sentence before the road. After farewell, the only way "
            "Odúwa can correct the distribution is theft. The recitation "
            "lets us hear that the war is already reasoned before it is "
            "committed. Existentially, the teaching is about the moment you "
            "negotiate a role you were actually given. The wish to be both "
            "obeyed and wondered-at is ordinary. Arámfè treats it as a "
            "conversation that has ended. A fitting task includes the "
            "benefits you will not personally dispense. Farewell is the "
            "doctrine: stop petitioning the assignment."
        ),
        "prac": (
            "Catch one sentence today that begins \"But I am the one who "
            "should also...\" Stop it. Finish the assigned task without "
            "annexing the wonder that belongs to another office. Say "
            "farewell to the extra portion."
        ),
        "terms": kt(
            (
                "first-born",
                "Odúwa's ground of protest -> seniority as a claim on arts "
                "as well as crown -> the recitation will not let birth-order "
                "rewrite Arámfè's split",
            ),
            (
                "strange benefits",
                "what Odúwa fears will steal hearts toward Orísha -> "
                "wonder as political threat, not mere gratitude -> "
                "\"blessings\" is too pious; these benefits unseat love of "
                "the king",
            ),
            (
                "fitting task",
                "Arámfè's last word before exile -> office as what fits, "
                "not what flatters -> \"duty\" is thinner; fit includes "
                "limit",
            ),
        ),
        "res": res(
            (
                "Bhagavad Gita 3.35, \"Better One's Own Imperfect Dharma\"",
                "Both prefer the assigned work, even when another office "
                "looks more wonderful, to the seizure of a neighbor's "
                "portion.",
                "Krishna argues the point at length for Arjuna; Arámfè "
                "ends the hearing in two lines and sends the sons out.",
            ),
            (
                "Conference of the Birds, \"Ask for the King Alone\"",
                "Both treat a wrong object of wanting — benefits, or a "
                "lesser station — as the thing that keeps a company from "
                "its real work.",
                "ʿAṭṭār's birds must want the King; Odúwa already has "
                "kingship and still wants the bag. The error is surplus, "
                "not lack of a throne.",
            ),
        ),
    },
    {
        "n": 6,
        "title": "The Bag Stolen on the Road",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "But by the roadside while Orísha slept\n"
            "Odúwa came by stealth and bore away\n"
            "The bag Arámfè gave. Thus was the will\n"
            "Of God undone: for thus with the charmed sand\n"
            "Cast wide on the unmastered sea, his sons\n"
            "Called forth a World of envy and of war."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odúwa; Orísha; the bag Arámfè gave."
        ),
        "tr": (
            "By the roadside, while Orísha sleeps, Odúwa comes by stealth and "
            "bears away the bag Arámfè gave. Thus the will of God is undone. "
            "With charmed sand cast on the unmastered sea, the sons call "
            "forth a world of envy and of war."
        ),
        "comm": (
            "The claim is that the world we inhabit is founded on a theft, "
            "and that the theft is not a side-plot but the means of "
            "creation. Odúwa does not steal after the land exists. He steals "
            "on the road, then uses the sand — his rightful tool — to call "
            "land from sea, and the bag comes with him into that land. The "
            "will of God undone is Arámfè's distribution, not the project of "
            "a world as such. The sons still make a world. They make it "
            "wrong-handed: envy and war are not later moral failures "
            "imported into an innocent earth; they are the signature of how "
            "earth was called. Sleep is part of the metaphysics. Orísha, "
            "wisest, can be robbed because wisdom sleeps on a roadside like "
            "any traveler. Kingship stays awake enough to take what it was "
            "refused. The recitation will spend the middle books showing "
            "that the bag without its clue cannot be opened — theft gets "
            "the object and misses the art. That later irony does not "
            "soften this sentence. A world can be geographically successful "
            "and theologically stolen. Existentially, the teaching is "
            "uncomfortable for anyone who thinks their household, company, "
            "or nation was raised from chaos by clean tools. Ask what was "
            "taken while a wiser office slept. The sand may be yours. The "
            "bag may not. If both are in your hand, envy is already the "
            "climate, even when the new shore looks like triumph."
        ),
        "prac": (
            "Identify one advantage you hold that was taken while someone "
            "abler in that craft was not watching. Do not confess in "
            "public theater. Return the usable part, or else stop calling "
            "the advantage a gift."
        ),
        "terms": kt(
            (
                "by stealth",
                "Odúwa's method on the road -> kingship uses night and sleep, "
                "not argument, once farewell has closed the case -> "
                "\"trickster\" imports Éshu; Éshu is not in this theft",
            ),
            (
                "will of God undone",
                "Arámfè's split reversed by the theft -> the world can be "
                "made against the maker's assignment -> not atheism; the "
                "will is real and violated",
            ),
            (
                "World of envy and of war",
                "what the stolen founding actually produces -> climate of "
                "the new earth, not an episode -> \"fallen world\" is too "
                "Edenic; this world is called forth already envious",
            ),
        ),
        "res": res(
            (
                "A.B. Ellis, Yoruba òwe, \"A jealous woman has no flesh upon "
                "her breast\"",
                "Both treat envy as a wasting climate that hollows the one "
                "who holds it, not as a passing mood.",
                "Ellis's proverb moralizes a household vice; the Ìfẹ̀ "
                "recitation makes envy the founding weather of the world "
                "Odúwa calls from the sea.",
            ),
            (
                "Conference of the Birds, \"The Parrot's Beautiful Captivity\"",
                "Both show a treasure or beauty held in the wrong way, so "
                "that possession becomes a cage.",
                "The parrot's cage is fear of losing beauty; Odúwa's theft "
                "is ambition to own the arts, and the cage will be a bag "
                "that will not speak.",
            ),
        ),
    },
    {
        "n": 7,
        "title": "Odúm’la Speaks in the Òrní",
        "src": "Wyndham 1921, I. The Beginning",
        "orig": (
            "They left on Earth Órní Odúm’la charged\n"
            "To tend the shrines and utter solemn words\n"
            "Inspired by Those invisible. And when\n"
            "Odúm’la's time had come to yield the crown,\n"
            "Ífa proclaimed that son with whom Odúm’la's soul abode.\n"
            "And now with me that Being is—about, within—\n"
            "And on our sacred days these lips pronounce\n"
            "The words of Odudúwa and Orísha."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odúm’la (first Òrní); Òrní; Ífa "
            "(messenger, who names the son in whom the soul abides)."
        ),
        "tr": (
            "When the Great Gods pass from sight, they leave Òrní Odúm’la "
            "to father a mourning people, tend the shrines, and utter words "
            "inspired by Those invisible. When his time comes to yield the "
            "crown, Ífa proclaims the son with whom Odúm’la's soul abides. "
            "That Being is now with the speaker — about, within — and on "
            "sacred days these lips pronounce the words of Odudúwa and "
            "Orísha."
        ),
        "comm": (
            "The claim is that divine speech did not end when the gods "
            "vanished; it changed bodies. Odúm’la is not a memorial "
            "official. He is charged to utter solemn words inspired by "
            "Those invisible, and his soul abides in a son Ífa can "
            "recognize. The present Òrní does not say he remembers the "
            "gods. He says that Being is about and within him, and that "
            "his lips, on sacred days, pronounce Odudúwa and Orísha. This "
            "is succession as incarnation of office, not as legal "
            "inheritance alone. The people are mourning because the Great "
            "Ones have gone to Arámfè's hills; the cure for mourning is "
            "not nostalgia but a mouth that still hosts them. Ífa's role "
            "matters. The messenger who will elsewhere carry requests to "
            "the father here discerns where a soul has lodged. Wisdom in "
            "Ìfẹ̀ is often this: finding the correct body for a continuing "
            "presence. The unit must not be turned into a general West "
            "African reincarnation essay, and it must not be Christianized "
            "into a single incarnation. The recitation's precision is "
            "local and serial: from Odúm’la to son to this Òrní, one "
            "Being, many bodies, two gods still speaking. Existentially, "
            "the teaching asks whether any office you hold is only your "
            "career. Some work is a soul that abides — a charge to father "
            "the mourning and keep speaking words you did not invent. If "
            "you cannot say \"with me that Being is,\" you may be holding "
            "a title without the mouth."
        ),
        "prac": (
            "Choose one office you actually hold — parent, teacher, chair, "
            "elder sibling. Speak one sentence today that is not yours: a "
            "sentence the work itself requires. Do not sign it with your "
            "personality. Let the office use the lips."
        ),
        "terms": kt(
            (
                "Odúm’la",
                "first Òrní, left on earth when the Great Gods passed -> "
                "father of a mourning people and continuing mouth of the "
                "invisible -> \"first king\" misses the inspired utterance",
            ),
            (
                "soul abode",
                "Ífa finds the son in whom Odúm’la's soul remains -> "
                "succession by indwelling, not by vote -> transmigration "
                "here is of an office-soul, not of every person",
            ),
            (
                "these lips pronounce",
                "the present Òrní's claim -> Odudúwa and Orísha still have "
                "a human mouth on sacred days -> \"recitation\" as "
                "performance understates the ontology: the Being is about, "
                "within",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Father Has Come Again\"",
                "Both teach that a departed presence returns in a living "
                "body and is recognized by name and role.",
                "Johnson describes ordinary parents reborn as Babatunde and "
                "Yetunde; here a single office-soul of Odúm’la abides in "
                "the Òrní so that two vanished gods can still speak.",
            ),
            (
                "Bhagavad Gita 4.4–6, \"Births Many, Memory One\"",
                "Both hold that one continuing awareness can occupy a "
                "series of bodies without becoming a new person each time.",
                "Krishna remembers all births while Arjuna does not; the "
                "Òrní's continuity is discerned by Ífa and enacted as "
                "liturgical speech, not as a god's private memory of aeons.",
            ),
        ),
    },
    {
        "n": 8,
        "title": "The Cliff over Chaos",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "From the sandy brink they peered down the sheer precipice.\n"
            "Behind them lay the parched, forbidding leagues; but yet\n"
            "the Sun was there, and breezes soft. . . Beneath\n"
            "Hung chaos—dank blackness and the threatening roar\n"
            "Of untamed waters. Then Odudúwa spoke:\n"
            "\"Better a homeless life in desert places:\n"
            "dare we turn and flee to some lost valley of the hills?\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odudúwa; Orísha. The cliff is the stern "
            "bar Arámfè set between Heaven's vales and the unmade waste."
        ),
        "tr": (
            "From the sandy brink they peer down the sheer precipice. Behind "
            "them: parched leagues, yet still sun and soft breeze and the "
            "memory of mountains. Beneath: chaos, dank blackness, the roar "
            "of untamed waters. Odudúwa asks whether they dare turn and "
            "flee to some lost valley — better a homeless life in desert "
            "places than a city founded under that yawn."
        ),
        "comm": (
            "The claim is that the first political temptation of the gods "
            "is nostalgia disguised as prudence. They have already stolen "
            "and already marched. At the cliff they see the assignment: "
            "untamed water, no sun below, a city to be founded for unborn "
            "men in what feels like a dungeon. Odúwa, who wanted kingship, "
            "now wants a lost valley. The desert behind them is harsh, but "
            "it still has the sun of Heaven. Chaos beneath has none. The "
            "counterintuitive move is that flight would not restore "
            "innocence. They are already outcasts by the father's sending "
            "and by the roadside theft. A hidden valley would be desertion "
            "of the dumb spirits who wait for life, and it would assume "
            "that Arámfè has no bodes. Cowardice here is metaphysical: the "
            "refusal to let godhead be used on the ungoverned. Many "
            "creation stories enjoy the view from the brink. This one lets "
            "the future king flinch. Kingship that seized the bag still "
            "quails at the roar. The recitation is honest about the body. "
            "Gods peer tremblingly. Courage is not their native climate; "
            "it will have to be argued by Orísha in the next breath. "
            "Existentially, the cliff is any threshold where the work "
            "finally looks like chaos and the road behind still smells "
            "like home. The teaching does not say the roar is imaginary. "
            "It says a lost valley is not a philosophy. It is a wish to "
            "remain a tourist of Heaven after you have already been sent."
        ),
        "prac": (
            "Stand at one brink you have been delaying — a conversation, a "
            "page, a repair. Name the lost valley you keep offering "
            "yourself. Take one step toward the roar, not back toward the "
            "soft breeze."
        ),
        "terms": kt(
            (
                "sheer precipice",
                "the bar Arámfè set between smiling vales and the waste -> "
                "creation begins as a drop, not a door -> \"fall\" in the "
                "Edenic sense is wrong; they are sent, and they peer",
            ),
            (
                "untamed waters",
                "chaos beneath Heaven's cliff -> not yet Olókun's curbed "
                "sea; water without office -> \"ocean\" already implies a "
                "queen they have not yet appointed",
            ),
            (
                "lost valley",
                "Odúwa's wish to flee -> nostalgia for a pocket of Heaven "
                "after exile has begun -> prudence is the mask; desertion "
                "is the act",
            ),
        ),
        "res": res(
            (
                "Psalms (Tehillim), Psalm 24, \"Lift Up Your Heads, O Gates\"",
                "Both set a founding against the fact of waters and a "
                "threshold that must be crossed before a king can enter.",
                "The psalm's earth is already founded on the seas by YHWH; "
                "here the gods have not yet poured sand, and the king "
                "wants to flee the threshold.",
            ),
            (
                "Heart Sutra, \"No Attainment, and So No Fear\"",
                "Both face an abyss that looks like the end of safety.",
                "The sūtra dissolves fear by dissolving attainment; Odúwa "
                "fears a very real unmade water, and the cure in the next "
                "unit is not emptiness but the hunger of spirits for life.",
            ),
        ),
    },
    {
        "n": 9,
        "title": "Is Godhead Blind",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "Then spoke Orísha whom men call The Great:\n"
            "\"Forbidding is our task, you say—but think\n"
            "how boundless is the fate you flinch from!\n"
            "Besides, is Godhead blind? You think Arámfè\n"
            "would not know? Has Might no bodes with eyes and ears?\n"
            "Dumb spirits hungering for life await us: let us go.\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Orísha the Great; Odúwa; Arámfè."
        ),
        "tr": (
            "Orísha, whom men call the Great, answers: is this Odúwa, my "
            "mother's son who stole the gift? The task is forbidding — but "
            "think how boundless is the fate you flinch from. Is godhead "
            "blind? Would Arámfè not know? Has Might no watchers? Dumb "
            "spirits hungering for life await us. Let us go."
        ),
        "comm": (
            "The claim is that godhead is not a privilege of calm but an "
            "obligation to the unborn, under a gaze that cannot be dodged. "
            "Orísha names the theft and still argues for descent. He does "
            "not forgive the bag; he refuses the extra sin of flight. Three "
            "reasons, stacked: the fate below is boundless (the work is "
            "worth the dark); Arámfè is not blind (flight is already "
            "seen); dumb spirits hunger for life (someone is waiting who "
            "cannot yet speak). The last is the philosophical center. "
            "Creation is owed to hungering shades, not to the gods' career. "
            "They are not exploring. They are late for an appointment with "
            "those who have no mouths yet. \"Is Godhead blind\" is "
            "sarcasm with a metaphysics: if you are a god, you do not get "
            "the human alibi of a private getaway. Might has bodes. The "
            "father who laboured from a silent Purpose still sees. The "
            "recitation thus binds omniscience to ethics without making "
            "Arámfè a bargainer. He does not need to be asked. He would "
            "know. Existentially, Orísha's questions cut two escapes. One "
            "is aesthetic despair: the task looks ugly, so it cannot be "
            "ours. The other is spiritual privacy: if we go back to the "
            "hills quietly, no one will notice. The spirits notice by "
            "hungering. The father notices by having bodes. Let us go is "
            "not bravado. It is the only sentence left that matches the "
            "office of a maker."
        ),
        "prac": (
            "Name one task you are calling \"forbidding\" because it would "
            "end a calm you have already outlived. Ask Orísha's question "
            "aloud: who is hungering for life because you delay? Then go "
            "do the first unpretty action they need."
        ),
        "terms": kt(
            (
                "Godhead",
                "Orísha's word for what cannot pretend not to see -> office "
                "with witnesses, not a mood of power -> \"divinity\" as "
                "status misses the sarcasm: are we really going to act "
                "blind?",
            ),
            (
                "bodes",
                "Wyndham's watchers of Might -> Arámfè's eyes and ears in "
                "the waste -> not a police doctrine; the point is that "
                "flight is already public to the father",
            ),
            (
                "Dumb spirits hungering for life",
                "those Orísha was charged to loose -> the unmade as "
                "appetite, not as clay -> \"souls\" is too finished; they "
                "are still mute and waiting for Dawn",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Olorun, the Lord of Heaven\"",
                "Both keep a high seeing that does not have to be fetched "
                "by ordinary petition — Johnson's Olorun too exalted to "
                "handle affairs, Orísha's Arámfè who would know if they "
                "fled.",
                "Johnson routes practice through òrìṣà intermediaries; here "
                "Orísha uses the father's gaze to force a brother over the "
                "cliff toward the hungering spirits.",
            ),
            (
                "Plotinus, Enneads V.1.6, \"The Emanation of the "
                "Intellectual-Principle from The One\"",
                "Both refuse the idea that the higher is unaware of what "
                "proceeds from it.",
                "Plotinus describes necessary overflow from the One; Orísha "
                "speaks in accusation and hunger, and the next act is a "
                "chain hung down a cliff, not an emanation without drama.",
            ),
        ),
    },
    {
        "n": 10,
        "title": "Sand and the Five-Clawed Bird",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "So spoke\n"
            "Orísha; and Odúwa hung a chain\n"
            "Over the cliff to the dark water's face,\n"
            "And sent Ojúmu, the wise priest, to pour\n"
            "The magic sand upon the sea and loose\n"
            "The five-clawed Bird to scatter far and wide\n"
            "Triumphant land."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odúwa; Ojúmu (the wise priest who pours); "
            "the five-clawed Bird; the sand of power."
        ),
        "tr": (
            "Odúwa hangs a chain from the cliff to the dark water. He sends "
            "Ojúmu, the wise priest, to pour the magic sand upon the sea and "
            "loose the five-clawed Bird. The bird scatters triumphant land "
            "far and wide."
        ),
        "comm": (
            "The claim is that earth is not spoken into being by a king "
            "alone; it is poured and scratched into being by a priest and a "
            "bird. Odúwa hangs the chain — he still has the nerve to "
            "connect Heaven's brink to the water's face — but the actual "
            "making is delegated. Ojúmu pours. The five-clawed Bird "
            "scatters. Land is triumphant, yet it will immediately begin "
            "to crumble under waves. The philosophy is in the instruments. "
            "Sand of power is almost nothing: grain against flood. A bird "
            "with five claws is almost comic against an unmastered sea. "
            "Ìfẹ̀ cosmogony trusts the small tool that has been given, not "
            "a second sun. The priest's presence at the first act also "
            "matters. Before there are men, there is already a wise "
            "pourer. Cult does not arrive after nature as decoration; a "
            "priest is part of how nature is possible. This must not be "
            "inflated with later Ifá manuals or with Fabunmi's city "
            "lore. The recitation gives a chain, sand, bird, priest, and "
            "a land that wins only as it is scattered. Existentially, the "
            "teaching is against waiting for a complete method. If you "
            "have sand and a bird, you pour. Triumphant land is a scatter, "
            "not a finished map. The waves will have their chapter. Your "
            "job at the brink is to let the small charmed thing do the "
            "work your fear called impossible."
        ),
        "prac": (
            "Take the smallest real tool you have for a task you have been "
            "calling oceanic. Use it for fifteen minutes — pour, scratch, "
            "scatter. Do not wait for a better instrument."
        ),
        "terms": kt(
            (
                "Ojúmu",
                "the wise priest sent down the chain -> pourer of sand, "
                "already necessary before humankind -> \"assistant\" misses "
                "that earth begins as a priestly act",
            ),
            (
                "five-clawed Bird",
                "Arámfè's creature, loosed to scatter land -> land as what "
                "a bird can scratch from poured sand -> not an emblem to "
                "decode from later bestiaries; the recitation gives the "
                "function, not a Yoruba species-name beyond Bird",
            ),
            (
                "magic sand",
                "the sand of power Arámfè gave Odúwa -> almost nothing, "
                "enough to call shore from flood -> \"magic\" is Wyndham's "
                "English; the force is assigned power, not stage trick",
            ),
        ),
        "res": res(
            (
                "Psalms (Tehillim), Psalm 104",
                "Both imagine dry land as a victory over waters that would "
                "cover everything if unbounded.",
                "The psalm's founder speaks and sets a boundary; here a "
                "priest pours and a bird scatters, and the next lines will "
                "show the sea still sucking the shore away.",
            ),
            (
                "Tao Te Ching 78",
                "Both trust what is small, grainy, or yielding against what "
                "looks like unmastered flood.",
                "Daoist water overcomes by softness; this sand overcomes "
                "water only as it is poured under command, and the marsh "
                "will keep pressing.",
            ),
        ),
    },
    {
        "n": 11,
        "title": "Olókun Set to Curb the Sea",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "So Odudúwa called Olókun and Olóssa to the cliff:\n"
            "\"Beneath, the waters wrestle with the new-rising World,\n"
            "and would destroy our kingdom and undo Arámfè's will.\n"
            "Olókun! to the sea! For there your rule shall be:\n"
            "To curb the hungry waves upon the coastlands for ever.\n"
            "And you, Olóssa, where your ripple laps the fruitful bank,\n"
            "shall see continually the offerings of thankful men.\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Olókun (sea); Olóssa (lagoons); Odudúwa "
            "appointing their offices from the cliff."
        ),
        "tr": (
            "Odudúwa calls Olókun and Olóssa to the cliff. Beneath, the "
            "waters wrestle the new-rising world and would undo Arámfè's "
            "will. Olókun is sent to the sea, to curb hungry waves on the "
            "coastlands forever. Olóssa is sent to the lagoons, where her "
            "ripple laps the fruitful bank and thankful men will bring "
            "offerings."
        ),
        "comm": (
            "The claim is that a world cannot be held by sand alone; the "
            "destructive element must be given a queen, not merely opposed. "
            "Waves suck the crumbling shore; lagoons climb into reedy "
            "swamp. Odúwa's answer is office. Olókun is not asked to dry "
            "the ocean. She is told to rule it — curb, not cancel. Olóssa "
            "receives the near waters, the fruitful bank, the human thanks "
            "that will come later. Restraint is a dominion, not a "
            "negation. This is political ecology before there are cities: "
            "hunger of waves is acknowledged as permanent (\"for ever\"), "
            "and therefore it needs a ruler who lives inside that hunger. "
            "Men will bring gifts because a curbed sea is already a "
            "benefaction. The unit must not become a manual of offerings. "
            "The philosophical gift is the appointment. Chaos becomes "
            "addressable when it has a name and a job. Until Olókun, water "
            "is ungoverned roar. After her, the same water is a kingdom "
            "that can be asked to remember the coastlands. Existentially, "
            "the teaching is about forces you keep trying to abolish. "
            "Anger, appetite, flood-work, grief: some of these will not "
            "die. They can be given a curb and a precinct. A queen of the "
            "sea is not a fantasy of control. She is the refusal to leave "
            "hunger untitled, because untitled hunger eats the world."
        ),
        "prac": (
            "Choose one recurring force you have been trying to dry up. "
            "Name it, give it a precinct (when and where it may move), and "
            "curb it there for a day. Do not pretend it will vanish."
        ),
        "terms": kt(
            (
                "Olókun",
                "goddess of the sea, set to curb hungry waves -> dominion "
                "inside the destructive element, not its erasure -> "
                "reducing her to \"wealth\" or to later cult-notes misses "
                "this first task: hold the coast",
            ),
            (
                "Olóssa",
                "goddess of the lagoons -> the near water that laps "
                "fruitful banks and receives thanks -> not a lesser "
                "Olókun; a different office at the edge of fields",
            ),
            (
                "curb",
                "Odúwa's verb for what rule does to waves -> limit as "
                "care for the new-rising world -> \"conquer\" is the wrong "
                "verb; the sea remains",
            ),
        ),
        "res": res(
            (
                "Psalms (Tehillim), Psalm 104",
                "Both imagine the sea as a hungry power that must be "
                "bounded so that land and human work can stand.",
                "The psalm's boundary is YHWH's decree; here Odúwa "
                "appoints a goddess to live in the sea as its queen, and "
                "thanks will go to her, not only to the high father.",
            ),
            (
                "Senegalese Animism, \"One Does Not Address God; One "
                "Addresses the Spirits\"",
                "Both put the working relationship at a local power of "
                "water rather than at the silent or sky-high absolute.",
                "Serer practice never addresses Roog; Ìfẹ̀ men will bring "
                "gifts to Olókun and Olóssa while Him-Who-Speaks-Not "
                "remains unspoken.",
            ),
        ),
    },
    {
        "n": 12,
        "title": "Farewell to the Wine of Heaven",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "\"We go to our sad kingdom. Such is the will\n"
            "Of Old Arámfè: so let it be. But ere\n"
            "The hour the wilderness which gapes for us\n"
            "Engulf us utterly. . .\n"
            "Good-bye, ye plains we roamed.\n"
            "Good-bye to sunlight and the shifting shadows\n"
            "Cast on the crags of Heaven's blue hills. Ah! wine\n"
            "Of Heaven, farewell\" . . . So came the Gods to Ífè."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Ìfẹ̀ (Ífè in Wyndham), the first "
            "stronghold they will found beneath the cliff."
        ),
        "tr": (
            "We go to our sad kingdom. Such is Arámfè's will; so let it be. "
            "Before the wilderness engulfs us, goodbye to the plains, to "
            "sunlight and shifting shadows on Heaven's blue hills. Wine of "
            "Heaven, farewell. So the gods come to Ìfẹ̀."
        ),
        "comm": (
            "The claim is that Ìfẹ̀ begins as a goodbye, not as a conquest "
            "fanfare. Land is now steadfast enough to receive them. Odúwa "
            "calls the gods to the cliff and speaks sorrow. The will is "
            "accepted (\"so let it be\") and the body still grieves sunlight. "
            "Wine of Heaven, earlier named as an age of mirth and sunrise, "
            "is what they lose: not abstract bliss, but the specific "
            "climate of Arámfè's vales — misty hollows, silvering moon, "
            "wind on grasslands. Descent is therefore a change of drink. "
            "They will later teach palm-wine and drum, which are earthly "
            "analogues, not the same vintage. The contested move is to "
            "let the king who stole the bag also be the one who loves "
            "Heaven enough to say farewell properly. Theft did not make "
            "him a nihilist. It made him a founder who already knows the "
            "kingdom is sad. Sacred city, in this telling, is the place "
            "you arrive after you have admitted the loss of the climate "
            "that trained you. Existentially, the line is for anyone who "
            "enters a necessary life and tries to smuggle the old wine in "
            "the same cup. Say goodbye to the exact light you will not "
            "have. Then go. Ìfẹ̀ is not a consolation prize. It is the "
            "work that remains when the hills have been looked at for the "
            "last lingering time."
        ),
        "prac": (
            "Name the \"wine of Heaven\" you are still trying to drink in a "
            "life that has already changed climate — a pace, a audience, a "
            "light. Say farewell to it once, aloud. Do the day's work in "
            "the sadder kingdom without that vintage."
        ),
        "terms": kt(
            (
                "sad kingdom",
                "Odúwa's name for the world below -> Ìfẹ̀ as accepted "
                "sorrow, not failed Heaven -> \"earth\" is too neutral; "
                "sadness is in the founding speech",
            ),
            (
                "wine of Heaven",
                "mirth and sunrise of Arámfè's vales -> the climate they "
                "cannot export -> later palm-wine is analogue, not identity",
            ),
            (
                "So came the Gods to Ífè",
                "the descent's punchline -> arrival is aftermath of "
                "farewell -> origin-story as tourism (\"they chose a "
                "capital\") misses the grief",
            ),
        ),
        "res": res(
            (
                "Conference of the Birds, the leaving of the valleys",
                "Both make a company leave a loved climate for a harder "
                "kingdom that is the only way the work continues.",
                "ʿAṭṭār's birds travel toward the King; these gods travel "
                "away from their father's hills toward a city they must "
                "build in darkness.",
            ),
            (
                "Bhagavad Gita 2.1–3, \"Stand Up — This Fainting Is Unworthy "
                "of You\"",
                "Both face a warrior or king who would rather keep a "
                "familiar order than enter the field that has already been "
                "assigned.",
                "Krishna rebukes Arjuna into battle; Odúwa's farewell is "
                "already obedience mixed with grief, and no charioteer "
                "need prod him over the last inch.",
            ),
        ),
    },
    {
        "n": 13,
        "title": "The Marsh and the Unconquerable Sand",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "Always the marsh\n"
            "Pressed eagerly on Ífè; but ever the Bird\n"
            "Returned with the unconquerable sand\n"
            "Ojúmu poured from his enchanted shell,\n"
            "And the marsh yielded."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Ìfẹ̀; Ojúmu; the Bird; the shell of sand."
        ),
        "tr": (
            "Always the marsh presses eagerly on Ìfẹ̀. Ever the Bird "
            "returns with the unconquerable sand Ojúmu pours from his "
            "enchanted shell. The marsh yields."
        ),
        "comm": (
            "The claim is that a founded city is not a finished victory "
            "over wet chaos; it is a rhythm of pressure and return. The "
            "gods have arrived. The world is still sunless. Marsh presses "
            "eagerly — the adverb matters. The unmade is not a defeated "
            "enemy sulking offshore; it is keen to take the town back. "
            "What holds Ìfẹ̀ is not a wall of theology but a bird that "
            "keeps coming back with sand from a priest's shell. "
            "Unconquerable is said of the sand, not of the city. The "
            "city can be sodden, the people can lament; the grain still "
            "wins a little ground each time it is poured. This is "
            "maintenance as cosmogony. Creation did not end at the first "
            "scatter. It continues as repetition against eagerness. Ógun "
            "will soon bid the forest grow, and the forest will bud the "
            "pallid shoots of hopeless night — even growth can be wrong "
            "in the dark. Sand, at least, is honest: it does not pretend "
            "to be a garden yet. Existentially, the teaching is for work "
            "that must be redone because the marsh is part of the site, "
            "not a surprise. If you need the problem to stay solved, you "
            "will hate Ìfẹ̀. If you can become the one who returns with "
            "sand, you are already in the priest's office. Yielding is "
            "what marshes do when someone does not get bored of pouring."
        ),
        "prac": (
            "Identify the marsh that presses on one room of your life — "
            "the mess that returns eagerly. Pour one shell of sand today: "
            "a small, repeated act that has already worked before. Do not "
            "redesign the city."
        ),
        "terms": kt(
            (
                "marsh",
                "eager wet that presses on Ìfẹ̀ -> the unmade as appetite "
                "at the town's edge -> \"chaos\" is too grand; marsh is "
                "local and persistent",
            ),
            (
                "unconquerable sand",
                "what the Bird brings back from Ojúmu's shell -> tiny "
                "matter that does not lose -> the city is conquerable; the "
                "practice of pouring is not",
            ),
            (
                "enchanted shell",
                "Ojúmu's vessel -> a held portion, enough for this return "
                "-> not a cornucopia; the bird must come again",
            ),
        ),
        "res": res(
            (
                "Tao Te Ching 8 and 78",
                "Both set a yielding or granular force against a heavier "
                "encroachment and trust repetition more than a single "
                "conquest.",
                "Daoist water takes the low place as virtue; here water is "
                "the problem and sand is the returning answer.",
            ),
            (
                "Senegalese Animism, \"The Woods Are Sanctuaries\"",
                "Both treat a living edge of land — woods, marsh — as an "
                "agent that must be dealt with, not as scenery.",
                "Serer woods are sanctuaries of presence; Ìfẹ̀'s marsh is "
                "an eager undoer, and the sanctuary will have to be "
                "scratched out again by sand.",
            ),
        ),
    },
    {
        "n": 14,
        "title": "Images Thrown into Wombs",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "Yet for live men\n"
            "Orísha, the Creator, yearned, and called\n"
            "To him the longing shades from other glooms;\n"
            "He threw their images into the wombs\n"
            "Of Night, Olókun and Olóssa, and all\n"
            "The wives of the great Gods bore babes with eyes\n"
            "Of those born blind—unknowing of their want—\n"
            "And limbs to feel the heartless wind."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Orísha the Creator; Olókun; Olóssa; "
            "Night as a goddess who also bears."
        ),
        "tr": (
            "Orísha the Creator yearns for live men. He calls longing "
            "shades from other glooms and throws their images into the "
            "wombs of Night, Olókun, Olóssa, and the wives of the great "
            "gods. The babes are born with the eyes of the blind — they "
            "do not know what they lack — and with limbs that feel the "
            "heartless wind."
        ),
        "comm": (
            "The claim is that humankind begins as yearning answered in "
            "the dark, not as a finished creature placed in a garden. "
            "Orísha still does not have the opened bag; he has the office "
            "of making. He yearns. He calls shades who already long. He "
            "throws images — forms, not yet sunlit persons — into wombs "
            "that belong to Night and to the water-queens. Birth is "
            "therefore a collaboration of the maker with goddesses of "
            "darkness and sea. The children arrive able to feel wind and "
            "unable to know light. Blindness here is not punishment. It "
            "is the climate of a sunless age: you cannot miss a sun you "
            "have never had. The contested move is to create anyway. A "
            "cautious god would wait for Day. Orísha will not leave the "
            "hungering mute until the weather improves. Later he will "
            "complain to Odúwa that their day is endless night — the "
            "maker becomes the advocate of his unfinished people. Johnson "
            "will say Orisala shapes a lump; this recitation says images "
            "are thrown into wombs in gloom. Keep the versions distinct. "
            "The Ìfẹ̀ sentence is wetter and more maternal, and it refuses "
            "to make first people spectators of a completed world. They "
            "are the world trying to have eyes. Existentially, the "
            "teaching blesses work done before the lighting is good. If "
            "you only make when you can guarantee recognition, you will "
            "make no one. Throw the image. Let the child feel wind. Light "
            "can be asked for later; life cannot be postponed to the day "
            "it will understand itself."
        ),
        "prac": (
            "Begin one making you have delayed until conditions were "
            "bright enough. Do it in the actual gloom of today. Do not "
            "explain the missing sun to the work. Let it have limbs first."
        ),
        "terms": kt(
            (
                "images",
                "what Orísha throws into wombs -> forms of longing shades, "
                "not yet daylit persons -> \"souls\" finishes them too "
                "soon; they are images in the dark",
            ),
            (
                "wombs of Night, Olókun and Olóssa",
                "the first mothers of humankind in this recitation -> "
                "darkness and water as natal, not only chaotic -> a "
                "male-only creation story cannot survive this line",
            ),
            (
                "eyes of those born blind",
                "the first human condition -> want unknown because light "
                "has not yet been given -> \"ignorance\" moralizes what is "
                "climatic",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Shaped by the Hand of "
                "Orisala\"",
                "Both give a shaping òrìṣà the work of making human form "
                "beside a higher god.",
                "Johnson's Orisala shapes a lump already made by Olorun; "
                "Orísha throws images into the wombs of Night and the "
                "water-queens, and the children are born before there is "
                "sun.",
            ),
            (
                "Plotinus, Enneads V.1.6",
                "Both describe lower lives as images proceeding from a "
                "higher looking-toward.",
                "Plotinus's images degrade as they recede from the One; "
                "Orísha's images are a mercy to hungering shades, and the "
                "lack they suffer is missing Day, not metaphysical "
                "distance alone.",
            ),
        ),
    },
    {
        "n": 15,
        "title": "Fire on the Vulture's Head",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "A deep compassion moved thundrous Arámfè,\n"
            "The Father of the Gods, and he sent down\n"
            "The vulture with red fire upon his head for men;\n"
            "and, by the Gods' command, the bird still wears\n"
            "no plumage where those embers burned him—\n"
            "A mark of honour for remembrance. Again\n"
            "the pale Moon sought Night's retreat; and Day took wings."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Arámfè; Ífa has gone as messenger to "
            "ask for sun and flame. The vulture is not given another "
            "Yoruba name here."
        ),
        "tr": (
            "Compassion moves thunderous Arámfè. He sends the vulture with "
            "red fire on its head for men. By command the bird still wears "
            "no plumage where the embers burned it — a mark of honour for "
            "remembrance. He speaks again: the pale Moon joins Night's "
            "watch; Day takes wings, roaming from the mists of Dawn to Eve "
            "who calls the toilers home."
        ),
        "comm": (
            "The claim is that light arrives as compassion answering a "
            "messenger, and that the carrier is honoured in the scar. "
            "Orísha has named the lack: endless night, wan woods, unused "
            "eyes. Odúwa sends Ífa. Arámfè, who could have said the sons "
            "stole and must sit in the dark they chose, is moved. Fire "
            "comes down on a vulture's head. The baldness is not a curse "
            "story smuggled in from another folklore. The recitation "
            "calls it honour for remembrance: the body of the bird keeps "
            "the fact that men have fire because someone burned. Moon and "
            "Day follow as further speech of the father — Night is no "
            "longer a lone watcher; Evening becomes a goddess who calls "
            "toilers home. The world gets a clock. The contested move is "
            "to treat illumination as care rather than as the restoration "
            "of a right. They asked. He pitied. The sun is not a stolen "
            "bag. It is a sent bird. Existentially, the teaching separates "
            "two kinds of goods. Some things you hold because you took "
            "them on the road. Some things arrive because a father still "
            "has compassion after the theft. Do not confuse them. And if "
            "you carry fire for others, do not hide the burned place. The "
            "bald patch is how a people remembers that light had a cost "
            "the carrier paid."
        ),
        "prac": (
            "Do one act of carrying light for someone who cannot yet see "
            "what they lack — an explanation, a lamp, a walk home. Do not "
            "demand thanks. Notice what it costs you, and do not hide the "
            "cost as if scar were shame."
        ),
        "terms": kt(
            (
                "vulture",
                "the bird that brings red fire on its head -> carrier "
                "honoured by the burned place -> not an omen-animal to "
                "load with later folklore; here it is a servant of "
                "compassion",
            ),
            (
                "mark of honour for remembrance",
                "the unfeathered patch -> memory worn on a body, not "
                "written -> \"disfigurement\" is the colonial eye; the "
                "gods command it as honour",
            ),
            (
                "Day took wings",
                "Day as a flying goddess from Dawn's mists to Eve -> time "
                "as persons who roam and call -> clock-time misses that "
                "evening is someone who calls toilers home",
            ),
        ),
        "res": res(
            (
                "Psalms (Tehillim), Psalm 148, \"Praise from Heaven and Earth\"",
                "Both populate sun, moon, and night as ordered companions "
                "in a living cosmos rather than as dead lamps.",
                "The psalm's lights praise YHWH; here the lights are sent "
                "in pity because unused human eyes have been waiting in a "
                "sunless town.",
            ),
            (
                "Lalla Vakyani, \"The Sun Does Not Glow for the Good Land "
                "Only\"",
                "Both refuse a light that would belong only to the already "
                "fortunate.",
                "Lalla's sun is impartial radiance; Arámfè's fire is a "
                "specific answer to Ìfẹ̀'s petition, carried on a burned "
                "head.",
            ),
        ),
    },
    {
        "n": 16,
        "title": "The Age of Mirth",
        "src": "Wyndham 1921, II. The Descent",
        "orig": (
            "Sparks flew from Ládi's anvil, while Ógun taught\n"
            "The use of iron, and wise Obálufon\n"
            "Made brazen vessels and showed how wine streams out\n"
            "From the slim palms. And in the night the Gods\n"
            "Set torches in their thronging courts to light\n"
            "The dance, and Heaven's music touched the drum\n"
            "Once more as in its ancient home. And mirth\n"
            "With Odudúwa reigned."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Ógun (iron); Ládi (Ógun's smith); "
            "Obálufon (brass and palm-wine); Odudúwa as king of the "
            "mirthful age."
        ),
        "tr": (
            "When bright Day lifts the unused eyes of men, sparks fly from "
            "Ládi's anvil. Ógun teaches iron. Obálufon makes brass vessels "
            "and shows how wine streams from slim palms. At night the gods "
            "set torches for the dance; Heaven's music touches the drum "
            "again. Mirth reigns with Odudúwa."
        ),
        "comm": (
            "The claim is that the arts of Heaven survive descent only as "
            "taught crafts and as night-mirth, and that this is a real "
            "reign, not a prelude too slight to count. Eyes that have "
            "never seen light are terrified by Day — the recitation is "
            "exact: terror of bright Day lifts from unused eyes — and "
            "immediately there is work. Iron. Brass. Palm-wine. Drum. The "
            "younger sons' portion (chorus, dance, crafts, joys of labour) "
            "finally has a climate in which it can be given. Odúwa still "
            "holds the stolen bag, unopened in its depths, and yet mirth "
            "can reign with him. The contested move is to let a tainted "
            "kingship host a true age of joy. Moralism wants the thief's "
            "city to be only a war-camp. Ìfẹ̀ remembers anvil, wine, and "
            "torchlit courts first. Culture is not the opposite of a "
            "stolen founding; it is what gods still know how to teach "
            "when sun has come. The bag's later silence will matter more "
            "because this age shows what shared arts look like when they "
            "are actually taught. Existentially, the teaching allows "
            "happiness that is not yet justice. You may be living in a "
            "house whose title is compromised and whose nights are still "
            "worth the drum. Do not use that as permission to keep the "
            "bag. Use it as evidence that craft and mirth are how a "
            "people becomes able to see what else is missing."
        ),
        "prac": (
            "Tonight, make one useful thing (even a repaired handle or a "
            "shared drink) and then keep one hour of music or unhurried "
            "talk. Let labour and mirth share the same reign. Do not use "
            "the hour to litigate the house's old thefts."
        ),
        "terms": kt(
            (
                "Ógun",
                "god of iron, teacher of its use, son of Odúwa -> craft "
                "and later war share one metal -> \"god of war\" alone "
                "erases the anvil that first means harvest-tools and making",
            ),
            (
                "Obálufon",
                "worker in brass who also shows palm-wine -> vessel and "
                "drink as one wisdom -> not a footnote craftsman; he is "
                "how Heaven's wine finds an earthly stream",
            ),
            (
                "mirth",
                "what reigns with Odudúwa after Day comes -> chorus, "
                "torch, drum, the analogue of Heaven -> frivolity is the "
                "wrong gloss; mirth is the climate the younger gods were "
                "sent to teach",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Ogun, God of Iron\"",
                "Both bind Ógun to iron as a consecrated craft, not only "
                "to battlefield fury.",
                "Johnson stresses war and smiths' consecration; this "
                "recitation first shows Ógun teaching use of iron in an "
                "age of mirth before any human war has begun.",
            ),
            (
                "Kashf al-Maḥjūb, \"The Patched Frock and the Sweetness of "
                "Faith\"",
                "Both treat a humble material culture — frock, brass, "
                "drum — as a real climate of the sacred, not a wait for "
                "pure doctrine.",
                "Hujwīrī's sweetness is interior faith worn as patched "
                "cloth; Ìfẹ̀'s mirth is public, metallic, and still hosted "
                "by a king who holds a stolen bag.",
            ),
        ),
    },
    {
        "n": 17,
        "title": "Good Humour Is the Last Gift",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "A tale is told how God in the Beginning sent\n"
            "three sons into the World—Earth, Water and the Forest—\n"
            "With one and twenty gifts for Earth and men;\n"
            "and all save one the Forest and the Rivers stole;\n"
            "and how God promised Earth that men should win\n"
            "the twenty gifts again by virtue\n"
            "Of that last one, Good Humour."
        ),
        "roman": (
            f"{ROMAN}. A tale inside the recitation: Earth, Water, Forest, "
            "and twenty-one gifts. No further Yoruba names."
        ),
        "tr": (
            "A tale is told: God sends three sons — Earth, Water, and the "
            "Forest — with twenty-one gifts for Earth and for men, the sons "
            "of Earth. Forest and Rivers steal all but one. God promises "
            "Earth that men will win the twenty back by the last gift, Good "
            "Humour. The tale is true: when the gods teach their crafts, "
            "men learn to seek thatch, food, and wine in forest and river "
            "patiently. So man prevails."
        ),
        "comm": (
            "The claim is that what the world withholds is recovered not by "
            "force against forest and river but by a temperament: good "
            "humour, the one gift that could not be stolen. Earth is "
            "first-born and still the loser of twenty portions. Water and "
            "Forest are not evil; they are the places where thatch, food, "
            "and wine actually live, and they keep those goods until men "
            "approach without the sourness of owners who have been robbed. "
            "Patience is the practical form of the last gift. The "
            "recitation insists the tale is true because it matches the "
            "age of crafts: Ógun and the gods make arts known, and men "
            "learn to seek rather than to raid. The contested move is to "
            "place humour — not sacrifice, not a second bag, not thunder — "
            "at the hinge of ecology. A people that cannot joke with the "
            "fact that forest and river hold the stores will stay hungry "
            "in the name of dignity. This is not comic relief before the "
            "war chapter. It is the alternative physics of getting things "
            "back. Existentially, the teaching diagnoses a modern reflex: "
            "when a commons seems stolen, escalate. Ìfẹ̀ says: keep the "
            "one gift that makes seeking possible. Good humour is not "
            "cheerfulness as denial. It is the refusal to let theft have "
            "your last instrument. With that instrument you can still go "
            "to the trees and the water as a learner."
        ),
        "prac": (
            "Go today to one place that holds a good you want — kitchen, "
            "office, woods, river of errands — and ask for it with "
            "patience instead of grievance. Win back one small store by "
            "good humour. Do not take it as a raid."
        ),
        "terms": kt(
            (
                "Earth, Water and the Forest",
                "three sons sent with the gifts -> the world as siblings "
                "who can steal from one another -> not elements in a "
                "Greek table; they are persons of a tale",
            ),
            (
                "Good Humour",
                "the last unstolen gift, by which the twenty return -> "
                "patience that can seek thatch, food, and wine -> "
                "\"cheerfulness\" is too thin; it is the virtue that "
                "keeps seeking from turning into war",
            ),
            (
                "patiently",
                "how men actually prevail in forest and river -> the "
                "lived form of Good Humour -> haste is the hidden theft "
                "of the last gift",
            ),
        ),
        "res": res(
            (
                "Tao Te Ching 8",
                "Both trust a yielding, unforced approach to the places "
                "that hold the goods of life.",
                "Daoist water takes the low place as the Way; here Water "
                "is also a thief of gifts, and humour — not water — is "
                "the human instrument of recovery.",
            ),
            (
                "A.B. Ellis, Yoruba òwe, \"If you are not able to build a "
                "house at once\"",
                "Both counsel a paced winning-back of what cannot be "
                "seized in one proud gesture.",
                "Ellis's proverb is household patience; this tale scales "
                "patience to the whole relation of Earth with Forest and "
                "River.",
            ),
        ),
    },
    {
        "n": 18,
        "title": "Give Back the Bag",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "The sound of drums was heard and Great Orísha\n"
            "Approached with skilled Obálufon, and said:\n"
            "\"The time has come to teach Arámfè's arts\n"
            "To men. Give back the bag (for it is mine!)\n"
            "That I may do our Father's bidding. Else,\n"
            "Have a care, is it not told how caution slept\n"
            "In the still woods when the proud leopard fell,\n"
            "Lured on by silence, 'neath the monster's foot?\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Orísha; Obálufon; Odúwa. The leopard "
            "saying is Wyndham's English of a Yoruba threat he footnotes "
            "(elephant and leopard)."
        ),
        "tr": (
            "Drums sound. Great Orísha comes with Obálufon before Odúwa "
            "and Ógun: the time has come to teach Arámfè's arts to men. "
            "Give back the bag — it is mine — that I may do our father's "
            "bidding. Else remember how caution slept in still woods when "
            "the proud leopard fell, lured by silence, under the monster's "
            "foot."
        ),
        "comm": (
            "The claim is that a stolen pedagogy has a due date, and that "
            "the due date is the readiness of men, not the convenience of "
            "the king. Orísha has waited through the age of mirth. Iron "
            "and brass and wine are already in the world; the deeper arts "
            "in the bag are not. He does not ask for the crown. He asks "
            "for the tool of his own office, in the palace where the Òrní "
            "will later reign, with a craftsman beside him. The proverb "
            "is the argument's edge. Silence is not safety. A proud "
            "leopard can be lured by a hush and crushed. Odúwa's quiet "
            "possession of the bag is that hush. The footnote Wyndham "
            "preserves — the elephant has power to crush the leopard, "
            "though he be silent — keeps the saying inside Yoruba speech "
            "without turning the unit into a drum-manual. The contested "
            "move is to threaten a king with a forest image in the name "
            "of a father's bidding. Arts are not a favor Odúwa may keep "
            "as regalia. They are a debt to men. Odúwa will answer as "
            "kings answer: Am I not king? Who speaks unseemly has packed "
            "his load. The war starts from that collision of two true "
            "sentences: the bag is Orísha's, and Odúwa is king. "
            "Existentially, the teaching is about the day you must ask "
            "for your own work back. Politeness that never names the "
            "theft becomes the silence that lures you under the foot. "
            "Ask clearly. Bring a witness who makes. Do not ask for the "
            "throne you were not given."
        ),
        "prac": (
            "Ask one person, without ornament, for a tool or credit that "
            "is actually yours to use for others. Do not ask for their "
            "rank. If they refuse by invoking rank alone, do not start a "
            "war today — write the sentence of the refusal so you cannot "
            "re-soften it."
        ),
        "terms": kt(
            (
                "Give back the bag",
                "Orísha's demand before the king -> restoration of a "
                "teaching office, not a coup -> \"treasure\" misses that "
                "the bag is for men, by the father's bidding",
            ),
            (
                "proud leopard",
                "the proverb's warning image -> silence can be a lure, "
                "caution can sleep -> Odúwa is the hush; Orísha names the "
                "foot that can fall",
            ),
            (
                "packed his load",
                "Odúwa's answering saying (Wyndham: the speaker is ready "
                "to travel) -> dissent treated as exile -> two Yoruba "
                "sayings collide, and war is the residue",
            ),
        ),
        "res": res(
            (
                "A.B. Ellis, Yoruba òwe, \"One lock does not know the "
                "wards of another\"",
                "Both use compact speech to say that one office cannot "
                "operate the inner work of another.",
                "Ellis's lock is mutual ignorance of crafts; here the "
                "king holds the lock and refuses the only hand that "
                "knows the wards.",
            ),
            (
                "Bhagavad Gita 3.19, \"Unattached, Do the Work That Must "
                "Be Done\"",
                "Both treat a delayed work — arts for men, the battle "
                "that holds worlds — as something that comes due and "
                "must be done.",
                "Krishna urges action without fruit-clinging; Orísha "
                "clings rightly to the bag because the bag is the work, "
                "not a fruit of prestige.",
            ),
        ),
    },
    {
        "n": 19,
        "title": "The First of Wars",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "Orísha and Odúwa called\n"
            "To arms their followings of Gods and men,\n"
            "And on that day the first of wars began\n"
            "In Ífè and the Forest. Such was the fall\n"
            "Of the Gods from paths divine, and such for men\n"
            "The woe that Odudúwa's theft prepared."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Orísha; Odúwa / Odudúwa; Ìfẹ̀."
        ),
        "tr": (
            "Orísha and Odúwa call to arms their followings of gods and "
            "men. On that day the first of wars begins in Ìfẹ̀ and the "
            "Forest. Such is the fall of the gods from paths divine, and "
            "such, for men, the woe Odudúwa's theft prepared."
        ),
        "comm": (
            "The claim is that war is not a human invention that later "
            "corrupts religion; it is a fall of gods, prepared by a "
            "theft, into which men are already drafted. Followings of "
            "gods and men: the first army is mixed. Ìfẹ̀ and the Forest "
            "are the first battlefield — city and wild together, the "
            "same pair that held thatch and wine a tale ago. The "
            "recitation names the event with liturgical exactness: the "
            "first of wars. There is a before, the age of mirth, when "
            "metal meant anvil. After this day, metal will remember "
            "this use. Fall from paths divine is not a Christian "
            "original sin pasted on. It is the priests' own verdict: "
            "godhead had a path, and the brothers left it. Woe for men "
            "is prepared, not accidental. The bag stolen on the road "
            "already contained this weather; the palace refusal only "
            "opens it. The contested move is to make the gods guilty "
            "in the hearing of a colonial officer without adopting his "
            "contempt. They are not \"fetish figures who fight.\" They "
            "are makers who knew better and called arms anyway. "
            "Existentially, the teaching locates the first war in a "
            "family argument about who owns the teaching of the world. "
            "Most public violence still has that shape: a stolen "
            "competence, a rank that will not return it, followings "
            "happy to be armed. If you want fewer wars, return bags "
            "before drums sound in the palace."
        ),
        "prac": (
            "Before you enlist anyone — even as gossip — in a quarrel "
            "about who owns a skill, try one more direct return of the "
            "bag. If you still call allies, admit that you are leaving "
            "a path you knew."
        ),
        "terms": kt(
            (
                "first of wars",
                "the day gods and men take arms in Ìfẹ̀ and the Forest -> "
                "war has a beginning in this telling, and it is divine "
                "before it is human -> \"always war\" is the cynicism "
                "the line refuses",
            ),
            (
                "paths divine",
                "the way the gods have left -> mirth, teaching, the "
                "father's split of offices -> not a vague holiness; a "
                "road they were walking",
            ),
            (
                "woe that Odudúwa's theft prepared",
                "human suffering as sequel of the roadside bag -> "
                "etiology of war -> blaming \"human nature\" alone "
                "absolves the founding theft",
            ),
        ),
        "res": res(
            (
                "Bhagavad Gita 2.4–6, \"How Can I Strike Those Worthy of "
                "Worship\"",
                "Both set the horror of war inside a kinship of the "
                "sacred — brothers, elders, teachers — rather than as "
                "a fight with strangers.",
                "Arjuna recoils and is taught to stand; the Ìfẹ̀ gods do "
                "not recoil in time, and the recitation calls their "
                "standing-to-arms a fall.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith, \"An Account at the "
                "Portals of Heaven\"",
                "Both keep a moral afterlife of deeds: what is done on "
                "earth is not sealed as merely local.",
                "Johnson's adage points to a future account; this unit "
                "already names woe in history as the prepared fruit of "
                "a theft among gods.",
            ),
        ),
    },
    {
        "n": 20,
        "title": "Thunder Cannot Stop Brothers",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "\"For now my thunderbolts I hurl, with deluges\n"
            "upon the land—to stay for aye your impious war.\"\n"
            "Dawn came; the storm was gone, and Old Arámfè\n"
            "in his grief departed on black clouds. But still\n"
            "the wrath, the anger of his sons endured,\n"
            "And in the dripping forests and the marshes\n"
            "The rebel Gods fought on."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Arámfè as thunder-father. The deluge "
            "refills marshes Ojúmu had dried."
        ),
        "tr": (
            "Arámfè hurls thunderbolts and deluges to fill marsh and "
            "lagoon and stay the impious war forever. Dawn comes. The "
            "storm is gone. The father departs on black clouds in "
            "grief. Still the wrath of his sons endures. In dripping "
            "forest and marsh the rebel gods fight on."
        ),
        "comm": (
            "The claim is that even the father of the gods cannot "
            "command peace once brothers have tasted the fall. Arámfè "
            "has speech, thunder, flood. He names the war impious. He "
            "tries to make the ground itself unfightable by returning "
            "the wet that Ojúmu dried — a terrible irony: the first "
            "creative labour is reversed as punishment. Dawn proves the "
            "limit. Storm passes. Grief takes the father away on clouds. "
            "Wrath stays. Rebel is now the right word for sons who were "
            "sent to make a world of mirth. The contested move is the "
            "admission, already forming in Arámfè, that here he is not "
            "omnipotent. In Heaven, yes. Here — he cannot tell. Thunder "
            "is not the last metaphysics; it is a failed policy. This "
            "must not be read as Wyndham's joke about a tribal sky-god. "
            "It is an Ìfẹ̀ thought about rank: a maker can send, split "
            "gifts, pity, light a sun, and still be unable to unmake a "
            "choice his sons prefer to his voice. Existentially, the "
            "teaching is for anyone who thinks a loud enough verdict "
            "will end a family war. You can flood the field. At dawn "
            "they will fight in the drip. Grief is more honest than "
            "another bolt. The work, if there is work left, will have "
            "to be a change of heart, not a change of weather."
        ),
        "prac": (
            "Do not add one more thunder — email, verdict, slam — to a "
            "quarrel that has already heard your power. Sit with the "
            "grief that you cannot stay it. Ask what a change of heart, "
            "not a change of weather, would look like for you alone."
        ),
        "terms": kt(
            (
                "thunderbolts",
                "Arámfè's instrument, now used as police -> power that "
                "cannot reach wrath -> \"sky-god weapon\" is museum talk; "
                "here thunder is a father's failed last resort",
            ),
            (
                "impious war",
                "his name for the brothers' fight -> a war against the "
                "paths they were given -> not impious because a colonial "
                "church says so; impious because they were sent to make "
                "mirth",
            ),
            (
                "rebel Gods",
                "what the sons are after they fight on -> rebellion "
                "defined by persistence after the father's storm -> "
                "\"heroes\" would flatter; the recitation does not",
            ),
        ),
        "res": res(
            (
                "Psalms (Tehillim), Psalm 29 (the voice of the LORD on "
                "the waters)",
                "Both imagine thunder as a father's or lord's voice "
                "meant to order a violent field.",
                "The psalm's voice accomplishes glory and sitting as "
                "king; Arámfè's thunder fails, and he leaves in grief "
                "while the sons fight on.",
            ),
            (
                "Senegalese Animism, \"The Invisible Master Is Named as "
                "the Sky\"",
                "Both know a high one associated with sky who regards "
                "conduct.",
                "Serer Rog takes satisfaction in the good and is not "
                "the cult addressee; Arámfè intervenes with flood and "
                "learns the limit of intervention in the world below.",
            ),
        ),
    },
    {
        "n": 21,
        "title": "By Strife Must It Endure",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "In the Unknown,\n"
            "Beyond the sky where I have set the Sun,\n"
            "Is He-Who-Speaks-Not: He knows all. Can this\n"
            "Be Truth: Amidst the unnatural strife of brothers\n"
            "The World was weaned: by strife must it endure—?"
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: none new. Him-Who-Speaks-Not returns "
            "as the all-knowing Purpose beyond Arámfè's sun."
        ),
        "tr": (
            "Beyond the sky where I set the Sun, in the Unknown, is "
            "Him-Who-Speaks-Not: he knows all. Can this be truth: "
            "amidst the unnatural strife of brothers the world was "
            "weaned — by strife must it endure?"
        ),
        "comm": (
            "The claim is the hardest in the book: the world may have "
            "been weaned on brother-strife, and strife may be the milk "
            "it still requires — and even the thunder-father does not "
            "know if that sentence is true. He has tried deluge. He "
            "reasons with himself in the clouds. Omnipotent in Heaven, "
            "puzzled here, he refers the question upward to the silent "
            "Purpose. Unnatural is his word for the fight; weaned is "
            "the metaphor that will not let the fight be only a "
            "mistake. A weaned world has been taken off a gentler food. "
            "If strife is what finished the weaning, then peace-as-return "
            "to Heaven's wine may be nostalgia, not destiny. The dash "
            "and the question mark are doctrine. This is not a war "
            "gospel. It is a metaphysical shudder. Him-Who-Speaks-Not "
            "knows; Arámfè does not. The recitation lets the highest "
            "speaking god end in interrogation. Wyndham's Golden Bough "
            "guesses must not be imported to close the question. The "
            "priests leave it open, which is more severe than a slogan "
            "about necessary violence. Existentially, the line forbids "
            "two comforts. One: if we repent hard enough, the world "
            "can be rewound to mirth without remainder. Two: because "
            "strife weaned the world, my next cruelty is ordained. The "
            "only honest stance the father models is to ask, in the "
            "Unknown's direction, whether endurance and unnatural "
            "strife are truly the same law — and to hate the war while "
            "asking."
        ),
        "prac": (
            "Write the question without answering it: what in your "
            "world was weaned on strife, and what only pretends that "
            "it must stay there? Sit with the question for ten minutes. "
            "Do not baptize your next harshness as cosmic law."
        ),
        "terms": kt(
            (
                "He-Who-Speaks-Not",
                "the all-knowing Purpose beyond the sun Arámfè set -> "
                "even the father must refer a question he cannot close -> "
                "do not supply a Yoruba name the recitation withholds",
            ),
            (
                "weaned",
                "the world taken off a gentler food amidst brother-strife "
                "-> founding as a bitter education -> \"created\" is too "
                "clean; weaning implies a prior milk (Heaven's mirth)",
            ),
            (
                "by strife must it endure",
                "the unconfirmed law Arámfè fears -> endurance as "
                "possible ontology of war -> the question mark is part "
                "of the term; without it the line becomes propaganda",
            ),
        ),
        "res": res(
            (
                "Bhagavad Gita 3.20–22, \"Janaka's Proof and the Holding "
                "of Worlds\"",
                "Both ask whether a world is held in being by a kind of "
                "conflictual or strenuous action rather than by rest.",
                "Krishna affirms action as what holds worlds and offers "
                "himself as the pattern; Arámfè only questions, and the "
                "strife he sees is unnatural brother-war, not offered "
                "duty.",
            ),
            (
                "Tao Te Ching 40",
                "Both suspect that reversal, return, or a hard opposite "
                "is how things come to be and stay.",
                "The Dao's reversal is the movement of the Way, quiet "
                "and yielding; Arámfè's suspected law is bloody, and he "
                "hopes it is not true.",
            ),
        ),
    },
    {
        "n": 22,
        "title": "Two Hundred Years without a Legend",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "'Tis said the anger of the Gods endured two hundred years:\n"
            "we know the priest Osányi made strange amulets\n"
            "for all the mortal soldiers of the Gods. . .\n"
            "but not one word of the great deeds, of hopes and fears,\n"
            "of imminent defeat or victory snatched away\n"
            "is handed down: no legend has defied, no voice\n"
            "called through the dimness and the baffling years."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Osányi (priest, maker of charms). The "
            "blank is the teaching: charms remembered, deeds not."
        ),
        "tr": (
            "It is said the anger of the gods endured two hundred years. "
            "We know Osányi made strange amulets for the mortal soldiers "
            "— charms to turn a spear, rob a sword of sting, make one "
            "terrible. Not one word of the great deeds, hopes, fears, "
            "near defeat, or snatched victory is handed down. No legend "
            "has defied the dimness. No voice has called through the "
            "baffling years."
        ),
        "comm": (
            "The claim is that a war can last centuries and still fail "
            "to become knowledge, while the technician of survival is "
            "remembered. Two hundred years is \"'tis said.\" What \"we "
            "know\" is Osányi and the amulets. The priests of Ìfẹ̀, "
            "whose opening boast was that truth lives in their mouths, "
            "here admit a blank. Heroic narrative did not survive. "
            "Technique did. That inversion is the philosophy. Living "
            "speech is not obliged to glorify the fall. It can keep the "
            "names of those who tried to keep soldiers alive and drop "
            "the saga of who almost won. The contested move is to treat "
            "the absence of legend as a kind of judgment. Dimness is "
            "not a research gap for the colonial notebook to fill. It "
            "is what the tradition chose, or what the war deserved. "
            "Great deeds that are not handed down cannot instruct. "
            "Charms that are handed down still do not justify the "
            "anger. Existentially, the teaching asks what you keep "
            "from your own long conflicts. If you remember only your "
            "epic and forget the dull devices that kept people from "
            "dying, you have inverted Ìfẹ̀'s archive. If you remember "
            "only devices and never name the anger that made them "
            "necessary, you have the other half. The baffling years "
            "are a warning: some victories are not worth a voice."
        ),
        "prac": (
            "Take one old conflict you still narrate as an epic. Write "
            "three sentences about the unglamorous things that kept "
            "people intact, and leave the \"great deeds\" unwritten "
            "today. Let a blank be a judgment."
        ),
        "terms": kt(
            (
                "Osányi",
                "priest and maker of charms for mortal soldiers -> what "
                "the tradition actually kept from the long war -> "
                "\"magician\" is colonial; he is the named technician of "
                "survival",
            ),
            (
                "two hundred years",
                "the said duration of divine anger -> time without a "
                "story -> chronology without legend is the point",
            ),
            (
                "no voice called through",
                "the priests' admission of blankness -> living speech "
                "can refuse to carry a war -> \"lost history\" implies "
                "an accident; this sounds like a held silence",
            ),
        ),
        "res": res(
            (
                "Lalla Vakyani, \"The Mantra of Silence\"",
                "Both treat a withheld word as a spiritual fact, not as "
                "a failure of memory alone.",
                "Lalla's silence is a mantra toward Śiva; Ìfẹ̀'s silence "
                "is the blank where war-legend would have been, and the "
                "kept words are a priest's amulets.",
            ),
            (
                "Tao Te Ching 2 and 56",
                "Both suspect that the loud career of doing and winning "
                "is not what the wise transmit.",
                "The Daoist sage practices non-display; the Ìfẹ̀ priests "
                "display the blank itself, as if the war earned no "
                "song.",
            ),
        ),
    },
    {
        "n": 23,
        "title": "Who Has No House Will Buy No Broom",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "What means this empty war between one mother's sons?\n"
            "'Twas said of old 'Who has no house will buy no broom.'\n"
            "Why then did Great Orísha bring plagues\n"
            "on those he made in love? . . . The bag you seized;\n"
            "but not its clue—the skill, the wisdom\n"
            "Of Great Orísha which alone could wake\n"
            "The sleeping lore."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Ógun speaking; Odúwa; Orísha. The "
            "broom saying is a Yoruba òwe in Wyndham's English."
        ),
        "tr": (
            "Ógun stands before the king at dawn: what means this empty "
            "war between one mother's sons? You say Orísha willed it. "
            "Of old it is said, who has no house will buy no broom. Why "
            "then would Orísha bring plagues on those he made in love? "
            "You seized the bag, but not its clue — the skill and wisdom "
            "that alone can wake the sleeping lore. Give the nations; "
            "give back the bag."
        ),
        "comm": (
            "The claim is that possession without competence is empty, "
            "and that a maker does not ruin his own house for sport. "
            "Ógun, warrior-son, is tired. He uses a proverb the way "
            "Ìfẹ̀ thinks: a broom is for a house. No one buys the tool "
            "if they have nowhere to sweep. Orísha made men in love; "
            "he has no motive to unhouse them. Therefore the war's "
            "cause cannot be Orísha's taste for plague. It is the bag "
            "held without its clue. The clue is not in the cloth. It "
            "is Orísha's skill — the only waking agent of the sleeping "
            "lore. Odúwa has the object and not the art. Empire of "
            "nations is already his; it does not console him, because "
            "envy wanted the inner treasure, not the map. The "
            "contested move is a son's disloyalty in the name of "
            "peace. Ógun joins \"enemies\" by telling the truth of the "
            "theft to the thief. Soft voices of the night have already "
            "asked for sleep; now iron asks for return. Existentially, "
            "the teaching is about tools you keep as trophies. If you "
            "cannot wake what you hold, you do not hold it. You hold "
            "a bag-shaped grievance. Buy no broom until you have a "
            "house — and if you stole a house-lore, give it back to "
            "the sweeper."
        ),
        "prac": (
            "Find one object, title, or login you keep that you cannot "
            "actually use well. Return it, or sit with the person who "
            "has the clue and let them wake it. Do not call unread "
            "ownership \"leadership.\""
        ),
        "terms": kt(
            (
                "Who has no house will buy no broom",
                "Yoruba saying in Wyndham's English -> you do not acquire "
                "a tool against your own interest -> Ógun applies it: "
                "Orísha will not plague the people he made",
            ),
            (
                "clue",
                "Orísha's skill and wisdom, not in the seized bag -> "
                "the waking agent of lore -> \"key\" is close; clue "
                "also means the thread you must follow, which Odúwa "
                "never had",
            ),
            (
                "sleeping lore",
                "arts that cannot teach themselves -> knowledge as "
                "something that must be woken by the right mind -> a "
                "stolen book, in this metaphysics, stays asleep",
            ),
        ),
        "res": res(
            (
                "A.B. Ellis, Yoruba òwe, \"He who owns the inner square "
                "of the house is…\"",
                "Both use house-speech to decide who actually holds an "
                "interior competence.",
                "Ellis's proverb ranks the inner-square owner; Ógun "
                "says the inner lore has an owner who is not the king "
                "holding the bag.",
            ),
            (
                "Lalla Vakyani, \"I Found Him in My Own House\"",
                "Both place the needed thing in a house — but one finds, "
                "the other cannot wake what he seized.",
                "Lalla's house yields Śiva to the one who looks inward; "
                "Odúwa's seized bag yields nothing, because the house of "
                "lore is Orísha's skill.",
            ),
        ),
    },
    {
        "n": 24,
        "title": "The Bag Sinks Voiceless",
        "src": "Wyndham 1921, III. The War of the Gods",
        "orig": (
            "Then Odudúwa\n"
            "Transformed to stone and sank beneath the soil,\n"
            "Bearing away the fateful bag.\n"
            "And thus,\n"
            "Beneath, through all the ages of the World\n"
            "A voiceless lore and arts which found no teacher\n"
            "Have lain in bondage."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Odudúwa becomes stone and sinks with "
            "the bag. Ógun is left a diminished crown."
        ),
        "tr": (
            "Odudúwa transforms to stone and sinks beneath the soil, "
            "bearing away the fateful bag. Beneath, through all the "
            "ages of the world, a voiceless lore and arts that found "
            "no teacher have lain in bondage."
        ),
        "comm": (
            "The claim is that some knowledge can be imprisoned in the "
            "earth by a will that would rather bury it than restore it. "
            "Odúwa, offered a way back to the father's hills and a "
            "diminished chieftaincy for Ógun, chooses neither teaching "
            "nor reign. He becomes stone. The bag goes with him. "
            "Voiceless lore is the exact remainder: the arts exist, "
            "they have no mouth, they have no teacher, they are in "
            "bondage. This is the opposite of the Òrní's opening boast. "
            "Truth has a home at shrines — and a portion of truth has "
            "been made homeless under the soil by the first king. The "
            "contested move is to refuse a happy recovery. Many myths "
            "would have Orísha open the bag at last. Ìfẹ̀ says the bag "
            "is still below. Whatever men later learn, they learn "
            "without that full clue. The theft's last success is "
            "silence, not use. Existentially, the teaching is about "
            "the spite that would fossilize a gift. If I cannot be "
            "the one who spells strange benefits, no one will. Stone "
            "is that sentence given a body. Check the places in your "
            "work where you have sunk a skill so that a rival cannot "
            "teach it. Digging it up would be repentance. Leaving it "
            "voiceless is how ages of the world stay poorer than they "
            "needed to be."
        ),
        "prac": (
            "Name one skill, document, or introduction you have buried "
            "so that it would not make another person shine. Write the "
            "first page of it, or speak the introduction, today. Do not "
            "take it to stone with you."
        ),
        "terms": kt(
            (
                "transformed to stone",
                "Odúwa's last act -> exit that sequesters the bag -> "
                "apotheosis-as-rock is not honour here; it is refusal",
            ),
            (
                "voiceless lore",
                "arts under the soil with no teacher -> knowledge as "
                "something that can be gagged -> \"lost wisdom\" sounds "
                "romantic; bondage is the recitation's word",
            ),
            (
                "fateful bag",
                "the gift that undid a world by being held wrong -> "
                "fate as the long consequence of a roadside stealth -> "
                "not a destiny assigned by Him-Who-Speaks-Not in the "
                "opening gift, but a fate Odúwa chose",
            ),
        ),
        "res": res(
            (
                "Heart Sutra, \"Form Is Emptiness, Emptiness Is Form\"",
                "Both confront a treasure that cannot be handled as a "
                "solid possession without losing what it was.",
                "The sūtra frees by seeing form and emptiness as "
                "inseparable; Odúwa solidifies himself and the bag into "
                "stone, which is the wrong metaphysics of a lore that "
                "needed a mouth.",
            ),
            (
                "Conference of the Birds, \"The Parrot's Beautiful "
                "Captivity\"",
                "Both show a precious thing locked away until it cannot "
                "do its work in the world.",
                "The parrot still speaks inside the cage; the bag in "
                "bondage does not speak at all, and the jailer has "
                "become the jail.",
            ),
        ),
    },
    {
        "n": 25,
        "title": "Life Should Spring from Forest",
        "src": "Wyndham 1921, IV. Mórimi (mythic argument only)",
        "orig": (
            "She saw the clustered tree-tops breaking into leaf\n"
            "Copper and red and every green, and she\n"
            "Remembered how beneath the new year's buds\n"
            "It was ordained by Peregún ’Gbo, lord\n"
            "Of uninhabitable woods that Life\n"
            "Should spring from Forest, and Life from Life,—till all\n"
            "The Woods were gladdened with the voice of beasts\n"
            "And birds."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Peregún ’Gbo (forest god); Mórimi. "
            "Cult recipe excluded."
        ),
        "tr": (
            "Mórimi sees the new year's leaves — copper, red, every "
            "green — and remembers the ordinance of Peregún ’Gbo, lord "
            "of uninhabitable woods: life should spring from forest, "
            "and life from life, until the woods are glad with beasts "
            "and birds. From the forest's womb leaped the sloth that "
            "laughs by night; amid the boughs the sloth brought forth "
            "the ape that bore the leopard."
        ),
        "comm": (
            "The claim is that life is not inserted into the woods from "
            "a workshop of the sky; it is ordained to spring from "
            "forest, and then from life, in a glad genealogy. Peregún "
            "’Gbo is lord of woods that were uninhabitable — the same "
            "wild that pressed and hid and fought. His ordinance is "
            "biological and philosophical at once: the forest is natal. "
            "Sloth, ape, leopard are not a modern taxonomy and not a "
            "cult diagram. They are the recitation's way of saying that "
            "forms come from prior forms, voice from voice, until "
            "uninhabitable space becomes a chorus. Mórimi will go on, "
            "in the full chapter, toward a bargained child; that "
            "how-to is excluded here. What is kept is the premise she "
            "starts from, which is already enough to judge the later "
            "temptation. If life springs from life, the forest is not "
            "a warehouse of parts for ritual engineering. It is a "
            "womb that already knows how to be glad. The contested "
            "move is to let a childless queen's eyes, seeing spring, "
            "remember an ecology instead of a transaction. Existentially, "
            "the teaching asks where you think new life comes from in "
            "your own woods — work, household, street. If you believe "
            "it must be purchased from a grim counter, you have already "
            "left Peregún ’Gbo. If you believe life from life, you look "
            "for the living thing that can bear the next living thing, "
            "and you let the woods be glad before you are."
        ),
        "prac": (
            "Walk among actual trees or, if you cannot, among the "
            "oldest living things you can reach. Do not ask them for "
            "a child, a job, or a sign. Watch one form that has come "
            "from another form. Say: life from life. Leave."
        ),
        "terms": kt(
            (
                "Peregún ’Gbo",
                "forest god, lord of uninhabitable woods, who ordains "
                "life from forest -> natal wild, not a store of ritual "
                "ingredients -> do not enlarge him with cult recipes "
                "this ingest excludes",
            ),
            (
                "Life from Life",
                "the ordinance under the new year's buds -> genealogy "
                "as the forest's law -> \"creation from nothing\" is "
                "the opposite metaphysics",
            ),
            (
                "uninhabitable woods",
                "what the forest was before the glad voices -> the wild "
                "as prior emptiness of beasts, not as evil -> habitation "
                "arrives as voice, sloth to leopard",
            ),
        ),
        "res": res(
            (
                "Tao Te Ching 42",
                "Both describe a sequence in which the one generates "
                "the next, and living multiplicity arrives by descent "
                "from life rather than by imported parts.",
                "The Dao's sequence is abstract (one, two, three, ten "
                "thousand); Peregún ’Gbo's is fleshed — sloth, ape, "
                "leopard — and gladness is the test.",
            ),
            (
                "Senegalese Animism, \"The Woods Are Sanctuaries\"",
                "Both refuse to treat forest as dead timber or as a "
                "neutral backdrop to human will.",
                "Serer woods are sanctuaries of named presence; Ìfẹ̀'s "
                "woods are a womb with a lord who wants them full of "
                "voice.",
            ),
        ),
    },
    {
        "n": 26,
        "title": "Will Gods Drive Bargains",
        "src": "Wyndham 1921, IV. Mórimi (argument only; no rite)",
        "orig": (
            "Then doubt seized Mórimi but still she answered:\n"
            "\"Will Gods not give? Is the grim World a morning market\n"
            "Where they drive bargains with the folk they made?\n"
            "Are babes as bangles which Obálufon fashions to barter?\"\n"
            "But Édi answered her: \"But once Arámfè spoke\n"
            "to Odudúwa, and with what heavy hearts the Gods\n"
            "went forth from Heaven's valleys to the blackness!\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Mórimi; Édi the Perverter; Obálufon; "
            "Arámfè. Sacrifice instructions excluded."
        ),
        "tr": (
            "Doubt seizes Mórimi, and she still answers: will gods not "
            "give? Is the grim world a morning market where they drive "
            "bargains with the folk they made? Are babes as bangles "
            "Obálufon fashions to barter? Édi, the Perverter, smooth of "
            "tongue, answers with the heavy hearts of the gods' descent "
            "— as if a hard sending justified a hard trade."
        ),
        "comm": (
            "The claim is Mórimi's question, and it stands even though "
            "the chapter will show her worn down: gods who made folk "
            "do not get to run a morning market with those folk. A "
            "child is not a brass bangle. The grim world may be grim; "
            "grimness is not a license for barter theology. Édi is "
            "named the Perverter, the one whose guile compels to "
            "conscious sin. His rhetoric is important. He does not "
            "deny the gods. He uses true plot — Arámfè spoke once, "
            "the gods went out with heavy hearts — to argue that a "
            "costly command must be obeyed when it comes thrice. "
            "Truth plus pressure is his method. The ingest stops "
            "before the altar. The philosophical fight is already "
            "complete: gift versus bargain, child versus bangle, "
            "maker versus merchant. Johnson's Olorun is too exalted "
            "to handle affairs; Mórimi demands something adjacent "
            "and hotter — that the gods give, not haggle. Whether "
            "the grim world answers her as she hopes is another "
            "story. The recitation is honest enough to let Édi win "
            "the night and still let her question judge him. "
            "Existentially, keep the question in any system that "
            "wants your dearest thing as payment for a promised "
            "good. If the world is a morning market, the makers "
            "have already fallen a second time, past war, into "
            "trade. Refuse that metaphysics even when a smooth "
            "voice has all the plot-points."
        ),
        "prac": (
            "Catch one place today where you are treating a person "
            "or a living good as a bangle — something to trade for "
            "a promised upgrade. Stop the trade. Ask Mórimi's "
            "question: will the source not give? Do not follow a "
            "smooth voice that uses true stories to close the sale."
        ),
        "terms": kt(
            (
                "morning market",
                "Mórimi's image for a world of divine haggling -> "
                "theology as trade -> the grimness of the world is "
                "not accepted as proof that the image is true",
            ),
            (
                "Édi",
                "the Perverter, smooth of tongue, who compels to "
                "conscious sin -> not a cartoon devil; he reasons "
                "from real myth toward a bargained act -> do not "
                "collapse him into Éshu; the recitation names both, "
                "and Édi is the perverter here",
            ),
            (
                "babes as bangles",
                "Obálufon's brass used as the measure of a child -> "
                "the exact category mistake -> a made ornament can "
                "be bartered; a person the gods made cannot",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Olorun, the Lord "
                "of Heaven\"",
                "Both resist a highest that would sit at a counter "
                "and handle human affairs as business.",
                "Johnson's Olorun is simply too exalted to deal; "
                "Mórimi's protest is ethical: even in a grim world "
                "the makers must not haggle children.",
            ),
            (
                "Kashf al-Maḥjūb, on bargaining away the sweet for "
                "the show of religion",
                "Both unmask a transaction that dresses itself as "
                "obedience or piety.",
                "Hujwīrī's target is spiritual display; Mórimi's "
                "target is a cosmos imagined as a market, and Édi "
                "is the salesman.",
            ),
        ),
    },
    {
        "n": 27,
        "title": "Arrayed as the Forest",
        "src": "Wyndham 1921, V. The Úbo Wars (argument only)",
        "orig": (
            "But to these colonists the Gods, their Fathers,\n"
            "Gave no good gifts: 'midst battles with the Wild the town grew.\n"
            "And the longed-for voice came to Olúbo:\n"
            "\"See with the rain I come each year upon your fields:\n"
            "Your work of yester-year is all undone\n"
            "By my swift desolation. Be this your symbol:\n"
            "Go thus against the Scornful Ones arrayed as I.\""
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Úbo (first daughter-town of Ìfẹ̀); "
            "Olúbo; the Forest-God. Festival license and sacrifice "
            "notes excluded."
        ),
        "tr": (
            "To the colonists of Úbo the gods, their fathers, give no "
            "good gifts. The town grows through battles with the wild. "
            "The Forest-God speaks: each year I come with rain, trees, "
            "rank grass; I undo last year's work. Let that be your "
            "symbol. Go against the Scornful Ones arrayed as I. Later, "
            "fire — the fire the vulture brought — undoes grass."
        ),
        "comm": (
            "The claim is that a people given no gifts will learn a "
            "god by the way that god undoes them, and that mimicry of "
            "undoing is a dangerous politics. Úbo is Ìfẹ̀'s first "
            "daughter and is sent out empty-handed. Dull remembrance "
            "of unnatural wrongs — the long war, the sunk bag — breeds "
            "the first rebel thought against the gods. The Forest-God "
            "does not console. He offers his own annual desolation as "
            "a symbol: come as I come, arrayed as rank growth, and "
            "take the scornful city that laughed (who lights a lamp "
            "between the leopard's paws?). Grass-clad men scale walls "
            "in a festival hour. Fire answers grass. The philosophical "
            "core is not the later festival's license; it is the "
            "logic of array. To be arrayed as the forest is to become "
            "the force that erases human year-work. Ìfẹ̀ had appointed "
            "Olókun to curb the sea; it did not appoint a curb for "
            "its own scorn. A daughter-town without gifts becomes "
            "wilderness on purpose. Existentially, the teaching is "
            "about neglected colonies of your own life — projects, "
            "people, rooms you sent out with no arts. If they return "
            "arrayed as what undoes you, the forest is not mysterious. "
            "You taught them scarcity, and a god of scarcity gave them "
            "a symbol. Fire will \"win\" and still not have been a "
            "gift. The deeper repair would have been to send arts the "
            "first time."
        ),
        "prac": (
            "Name one \"colony\" you sent out with no good gifts — a "
            "person, team, or habit you expected to fend in the wild. "
            "Send one real art today (a tool, a teaching, a share). "
            "Do not wait to fight them when they come back as grass."
        ),
        "terms": kt(
            (
                "Úbo",
                "first daughter of Odúwa's city, given no good gifts -> "
                "colony as the birth of rebel thought -> not a footnote "
                "town; she is what Ìfẹ̀ becomes when it scorns its own "
                "young",
            ),
            (
                "arrayed as I",
                "the Forest-God's symbol: come as annual desolation -> "
                "mimicry of the wild as strategy -> do not turn this "
                "into costume-instruction; the thought is political "
                "ecology",
            ),
            (
                "Scornful Ones",
                "Ìfẹ̀ as seen from Úbo -> laughers who light a lamp "
                "between leopard's paws -> scorn is the gift they did "
                "give",
            ),
        ),
        "res": res(
            (
                "Tao Te Ching 76",
                "Both know that the rigid and scornful break, and that "
                "what is living is grass-like, rank, returning.",
                "The Dao prefers the soft for life; here grass-array is "
                "also an army, and fire — a sent heavenly gift — undoes "
                "it. Softness is not automatically innocent.",
            ),
            (
                "Senegalese Animism, \"The Woods Are Sanctuaries\"",
                "Both treat forest as an agent that can enter human "
                "politics, not as scenery.",
                "Serer woods shelter presence and cult; this Forest-God "
                "lends his desolation as a rebel symbol against a "
                "scornful mother-city.",
            ),
        ),
    },
    {
        "n": 28,
        "title": "Ógun Goes to His Trees",
        "src": "Wyndham 1921, VI. The Passing of Ógun",
        "orig": (
            "Yet she rejects me. Ah! my trees\n"
            "Would be more kind, and to my trees I go.\"\n"
            "Dawn came; and Ógun stood upon a hill\n"
            "To Westward, and turned to take a last farewell\n"
            "Of his old queen of cities—but white and dense,\n"
            "O'er harbouring woods and unremembering Ífè\n"
            "A mist was laid and blotted all."
        ),
        "roman": (
            f"{ROMAN}. Key Yoruba: Ógun; Orányan; Ìfẹ̀. The city chooses "
            "the warrior son; the iron god goes to the forest he planted."
        ),
        "tr": (
            "Ìfẹ̀ chooses Orányan. Ógun, who grew old with the city and "
            "planted her forests as a robe, says: she rejects me. My "
            "trees would be more kind; to my trees I go. At dawn he "
            "stands on a westward hill to take farewell of his queen of "
            "cities. A white dense mist lies over harbouring woods and "
            "unremembering Ìfẹ̀ and blots all."
        ),
        "comm": (
            "The claim is that a city can become unable to see the god "
            "who made her livable, and that the god's last metaphysics "
            "is kindness of trees. Ógun has argued for peace, asked to "
            "finish Arámfè's bidding, refused the romance of endless "
            "war that Orányan names as the world's true destiny. Ìfẹ̀'s "
            "young men want rumours, red war, the living lustre of a "
            "name. The old chiefs want the roof and the evening fire. "
            "The cry that chooses Orányan is, for Ógun, the parrot-egg "
            "sentence: the walls will not hold a rule of iron against "
            "treachery inside. He does not turn to stone (Osányi's "
            "charms are forgotten). He does not become a river as Óshun "
            "did. He goes to the trees he planted — the robe of "
            "queenly Ìfẹ̀ — expecting more kindness from what he grew "
            "than from the mouths he saved. Dawn's mist is the last "
            "image: unremembering Ìfẹ̀ is blotted. The god cannot even "
            "complete farewell. Memory fails at the scale of weather. "
            "The contested move is to let the iron god prefer forest "
            "kindness to civic fame without calling that preference "
            "weakness. He is not fleeing a fight he invented; he is "
            "leaving a people who have chosen the fight as their wine. "
            "Existentially, the teaching is about the day a work no "
            "longer knows you. Do not curse it into stone. Do not "
            "fake a river-exit. Go to the living things you actually "
            "planted. If mist blots the city, that is already the "
            "city's memory of you. Kindness may still be in the trees."
        ),
        "prac": (
            "If a room you built has chosen a louder occupant, do not "
            "stage a last speech it cannot hear. Go to one living thing "
            "you planted — a tree, a practice, a person you grew — and "
            "keep company there for an hour. Let mist have the city."
        ),
        "terms": kt(
            (
                "Orányan",
                "Ógun's warrior son, chosen by Ìfẹ̀'s young men -> wide "
                "renown against obscurity -> not a villain; he is the "
                "destiny the city prefers to peace",
            ),
            (
                "my trees would be more kind",
                "Ógun's last metaphysics -> planted forest as the robe "
                "and the remaining friend -> \"nature-lover\" is too "
                "soft; these are trees he set for a queen who forgot",
            ),
            (
                "unremembering Ífè",
                "the city under mist, unable to complete even a "
                "farewell -> memory as weather that can blot a god -> "
                "the opening unit's sure home of truth can also forget",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith, \"Iron and the Sacred "
                "Tree\"",
                "Both bind Ógun's metal to living wood, so that iron "
                "religion is not only forge and war.",
                "Johnson keeps iron and tree as paired sacred facts; "
                "this ending makes the trees kinder than the city, and "
                "Ógun leaves the forge-throne for the forest he planted.",
            ),
            (
                "Conference of the Birds, the departure from the "
                "seventh valley toward the King",
                "Both end a long company-story with a leaving in which "
                "the familiar city or flock can no longer be the home "
                "of the seeker.",
                "ʿAṭṭār's birds find they were the King; Ógun finds the "
                "city has chosen another king, and his last likeness is "
                "mist over trees, not a revealed identity.",
            ),
        ),
    },
]


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.{SLUG}_{n:03d}"
    words = _word_count(u["comm"])
    if words < 150:
        raise SystemExit(f"{uid}: commentary has {words} words (need ≥150)")
    if len(u["res"]) < 2:
        raise SystemExit(f"{uid}: need ≥2 resonances")
    layers = [
        {"kind": "original", "label": "Original", "body": u["orig"]},
        {"kind": "iast", "label": "Romanization", "body": u["roman"]},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"IFE_{n:03d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": u["title"],
        "title": u["title"],
        "unit_type": "teaching_passage",
        "commentary": u["comm"],
        "themes": THEMES,
        "tags": [SLUG] + THEMES,
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "category": "yoruba-ife",
            "verse": str(n),
            "section": u["src"],
            "cultural_context": NOTE,
            "original_source": u["src"],
            "original_reliability": (
                "SOURCED — Wyndham 1921 verse of Ìfẹ̀ priest recitation; "
                "Yoruba not preserved"
            ),
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": u["orig"],
        "transliteration": u["roman"],
    }
    if n in HEROES:
        unit["tts_key"] = True
    path = os.path.join(OUT, f"{uid.replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return uid


def build() -> int:
    os.makedirs(OUT, exist_ok=True)
    keep = {write_unit(u) for u in UNITS}
    removed = 0
    for name in os.listdir(OUT):
        if not name.endswith(".yml"):
            continue
        stem = name[:-4]
        if not stem.startswith(f"{SLUG}_{SLUG}_"):
            continue
        n_str = stem.split("_")[-1]
        uid_chk = f"{SLUG}.{SLUG}_{n_str}"
        if uid_chk not in keep:
            os.remove(os.path.join(OUT, name))
            removed += 1
    ns = [u["n"] for u in UNITS]
    if len(ns) != len(set(ns)):
        raise SystemExit("duplicate unit numbers")
    heroes = [u["n"] for u in UNITS if u["n"] in HEROES]
    ids = [f"{SLUG}.{SLUG}_{n:03d}" for n in ns]
    print(f"{SLUG}: {len(ids)} units (min 28) · tts_key {heroes} · removed extras {removed}")
    for uid in ids:
        print(" ", uid)
    if len(ids) < 28:
        raise SystemExit(f"floor not met: {len(ids)} < 28")
    if len(heroes) != 10:
        raise SystemExit(f"need 10 tts_key, got {len(heroes)}")
    return len(ids)


if __name__ == "__main__":
    build()
