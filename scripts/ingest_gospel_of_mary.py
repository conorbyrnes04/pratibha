#!/usr/bin/env python3
"""Ingest the Gospel of Mary (BG 8502) by surviving argument-arc.

The Coptic is only about half the book (pp. 7–10, 15–19). Lost pages are not
invented. The surviving dialogue is segmented into ≥25 genuine units (floor),
each one claim or scene. Still a sibling of `ingest_new_testament_logia.py`
in the living-sayings family.

English: Pratibha adaptation of Mark M. Mattison's public-domain translation
(gospels.net; dedicated to the public domain). Coptic: working transcription of
the Sahidic of Papyrus Berolinensis 8502, not Till's 1955 apparatus.
Do not use Karen King, MacRae, Meyer, or the gnosis.org NHL English as a crib.
"""
from __future__ import annotations

import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/gospel_of_mary")
SLUG = "gospel_of_mary"
COLL = "Gospel of Mary"
PROV = (
    "English is a Pratibha adaptation (2026) of Mark M. Mattison's public-domain "
    "translation (gospels.net), itself based on the Sahidic of Papyrus "
    "Berolinensis 8502,1. Coptic is a working transcription of the exhibited "
    "manuscript wording, with lacunae marked. Does not follow King, MacRae, "
    "Meyer, or any copyrighted NHL English."
)
NOTE = (
    "A second-century Greek gospel surviving mainly in a fifth-century Sahidic "
    "codex (Berlin BG 8502). Pages 1–6 and 11–14 are lost. Mary Magdalene "
    "receives a hidden teaching after the resurrection; the soul ascends past "
    "the powers; Peter and Andrew refuse her, and Levi defends her."
)
# Ten heroes, spread: dissolve, sin, Human One, no extra law, Mary stands,
# treasure, garment, not-judging, silence, worth.
HEROES = {1, 2, 6, 7, 9, 12, 14, 16, 19, 25}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


UNITS: list[dict] = [
    {
        "n": 1,
        "title": "Matter dissolves into its own root",
        "section": "BG 8502, p. 7",
        "coptic": "ⲉⲓⲉ ⲧϩⲩⲗⲏ ⲛⲁⲧⲁⲕⲟ ϫⲛ ⲙⲙⲟⲛ ⲡⲉϫⲉ ⲡⲥⲱⲧⲏⲣ ϫⲉ ⲧⲫⲩⲥⲓⲥ ⲛⲓⲙ ⲡⲡⲗⲁⲥⲙⲁ ⲛⲓⲙ ⲡⲥⲱⲛⲧ ⲛⲓⲙ ⲉⲩϣⲟⲟⲡ ϩⲣⲁⲓ ⲛϩⲏⲧ ⲛⲛⲉⲩⲉⲣⲏⲩ ⲁⲩⲱ ⲟⲛ ⲥⲉⲛⲁⲃⲱⲗ ⲉⲃⲟⲗ ⲉϩⲣⲁⲓ ⲉⲧⲟⲩⲛⲟⲩⲛⲉ ⲙⲙⲓⲛ ⲙⲙⲟⲟⲩ ϫⲉ ⲧⲫⲩⲥⲓⲥ ⲛⲧϩⲩⲗⲏ ⲥⲃⲱⲗ ⲉⲃⲟⲗ ⲉϩⲣⲁⲓ ⲉⲧⲉⲥⲫⲩⲥⲓⲥ ⲙⲙⲁⲩⲁⲁⲥ ⲡⲉⲧⲉ ⲟⲩⲛⲧϥ ⲙⲁⲁϫⲉ ⲉⲥⲱⲧⲙ ⲙⲁⲣⲉϥⲥⲱⲧⲙ",
        "tr": "Then will matter be destroyed, or not? The Savior said, Every nature, every form, every creature exists in and with each other, but they will dissolve again into their own roots, because the nature of matter dissolves into its nature alone. Whoever has ears to hear should hear.",
        "comm": "The gospel opens, after six lost pages, on a cosmological claim rather than a miracle. The question wants destruction. The answer is unbinding. Things exist interpenetrating — then they return into their own root. Matter does not need to be hated; it has a nature that goes home. The contested move is to refuse both world-rejection and world-solidity. Dissolution is not a catastrophe. It is what matter does when it is no longer being forced to play at permanence. 'Ears to hear' is not a password for the clever. It is a demand that you stop treating the visible as a last word.",
        "prac": "Take one object you treat as permanent. Name its root (use, hunger, fear, habit). Let the object stay. Let the permanence-story go.",
        "terms": kt(
            ("ϩⲩⲗⲏ", "matter / hylē — not evil stuff, a nature that dissolves into itself"),
            ("ⲛⲟⲩⲛⲉ", "root — the return-point of each nature, not a better world behind this one"),
            ("ⲫⲩⲥⲓⲥ", "nature — the way a thing actually behaves when not propped up by fear"),
        ),
        "res": res(
            ("Gospel of Thomas 11", "The dead are not alive and the living will not die; this world is a crossing, not a fortress.", "Thomas speaks in riddle; Mary gives a physics of unbinding."),
            ("Tao Te Ching 16", "Return to the root is called stillness.", "Laozi's root is the nameless; Mary's root is each nature going home, including matter."),
        ),
    },
    {
        "n": 2,
        "title": "Sin does not exist — you make it",
        "section": "BG 8502, p. 7",
        "coptic": "ⲡⲉϫⲉ ⲡⲉⲧⲣⲟⲥ ⲛⲁϥ ϫⲉ ⲉⲡⲉⲓⲇⲏ ⲁⲕⲧⲁⲩⲟ ⲉⲣⲟⲛ ⲛϩⲱⲃ ⲛⲓⲙ ϫⲟⲟⲥ ⲉⲣⲟⲛ ⲛⲕⲉϩⲱⲃ ⲟⲩ ⲡⲉ ⲡⲛⲟⲃⲉ ⲙⲡⲕⲟⲥⲙⲟⲥ ⲡⲉϫⲉ ⲡⲥⲱⲧⲏⲣ ϫⲉ ⲙⲛ ⲛⲟⲃⲉ ϣⲟⲟⲡ ⲁⲗⲗⲁ ⲛⲧⲱⲧⲛ ⲉⲧⲉⲧⲛⲉⲓⲣⲉ ⲙⲡⲛⲟⲃⲉ ⲉⲧⲉⲧⲛⲉⲓⲣⲉ ⲙⲡⲉⲧⲉ ⲧⲫⲩⲥⲓⲥ ⲙⲡⲛⲟⲉⲓⲕ ⲉⲧⲉ ϣⲁⲩⲙⲟⲩⲧⲉ ⲉⲣⲟϥ ϫⲉ ⲡⲛⲟⲃⲉ",
        "tr": "Peter said to him, Since you have explained everything to us, tell us one more thing. What is the sin of the world? The Savior said, Sin does not exist, but you are the ones who make sin when you act according to the nature of adultery, which is called sin.",
        "comm": "Peter wants a substance called Sin sitting in the world. The Savior will not give him one. Sin is not a thing in the cosmos; it is a way of acting — named here as adultery, not first as sex but as splitting, mixing against nature, taking what is not yours to take. You make it. The misconception this gate blocks: that spirituality begins by locating a stain in matter, or in women, or in the world as such. The next sentence will say what the Good actually does. This one only demolishes the object Peter asked for.",
        "prac": "Before you name something a sin today, ask: am I pointing at a substance in the world, or at a mixing I am doing? Name the mixing. Stop it once.",
        "terms": kt(
            ("ⲛⲟⲃⲉ", "sin — here refused as a cosmic object; produced by a kind of acting"),
            ("ⲛⲟⲉⲓⲕ", "adultery — mixing against nature; taking what does not belong to that root"),
            ("ⲡⲕⲟⲥⲙⲟⲥ", "the world — Peter locates sin here; the Savior will not"),
        ),
        "res": res(
            ("A Course in Miracles, principle 1", "Nothing real can be threatened; nothing unreal exists.", "Both refuse sin as substance. The Course makes the world error; Mary lets matter have a nature that honestly dissolves."),
            ("Gospel of Thomas 14", "If you fast you will beget sin for yourselves — ritual can manufacture the stain it claims to remove.", "Thomas attacks pious production of guilt; Mary locates production in adulterous mixing."),
        ),
    },
    {
        "n": 3,
        "title": "The Good came to restore each nature",
        "section": "BG 8502, p. 7",
        "coptic": "ⲉⲧⲃⲉ ⲡⲁⲓ ⲁ ⲡⲁⲅⲁⲑⲟⲛ ⲉⲓ ⲉϩⲟⲩⲛ ⲉⲧⲏⲩⲧⲛ ϣⲁ ⲛⲁ ⲧⲫⲩⲥⲓⲥ ⲛⲓⲙ ϫⲉⲕⲁⲥ ⲉϥⲛⲁⲧⲁϩⲟⲥ ⲉⲣⲁⲧⲥ ϩⲛ ⲧⲉⲥⲛⲟⲩⲛⲉ",
        "tr": "That is why the Good came among you, as far as the things of every nature, in order to restore it within its root.",
        "comm": "If sin is not a substance, the Good is not a prosecutor. It comes among you — into the mixed field — as far as every nature, to restore each thing to its root. Restoration, not replacement. The first teaching (matter returns to its nature) is now the work of the Good. The misconception: that salvation extracts you from natures into a second, cleaner world. Here the Good goes all the way into the natures and seats them back where they belong. You do not have to destroy matter to be saved. You have to stop mixing it.",
        "prac": "Pick one thing you have been trying to save by destroying (a habit, a person, a mood). Ask what restoring it to its root would look like. Do that smaller act instead.",
        "terms": kt(
            ("ⲡⲁⲅⲁⲑⲟⲛ", "the Good — comes among you to restore, not to decorate a guilty world"),
            ("ⲧⲁϩⲟ ⲉⲣⲁⲧⲥ", "restore / set on its feet — each nature seated in its root"),
            ("ⲛⲟⲩⲛⲉ", "root — same word as matter's homecoming; now the Good's destination"),
        ),
        "res": res(
            ("Gospel of Thomas 70", "If you bring forth what is within you, it will save you; if you do not, it will destroy you.", "Thomas locates the crisis inside; Mary locates the Good as restorer of each nature's root."),
            ("Plotinus, Ennead I.6", "The soul is restored by becoming like the Good it sees.", "Plotinus restores by likeness and stripping; Mary restores each nature in place."),
        ),
    },
    {
        "n": 4,
        "title": "You die because you love what tricks you",
        "section": "BG 8502, pp. 7–8",
        "coptic": "ⲉⲧⲃⲉ ⲡⲁⲓ ⲧⲉⲧⲛϣⲱⲛⲉ ⲁⲩⲱ ⲧⲉⲧⲛⲙⲟⲩ ϫⲉ [ⲧⲉⲧⲛⲙⲉ ⲙⲡⲉⲧⲣ ϩⲁⲗ ⲙⲙⲱⲧⲛ] ⲡⲉⲧⲉ ⲟⲩⲛϭⲟⲙ ⲙⲙⲟϥ ⲉⲛⲟⲓ ⲙⲁⲣⲉϥⲛⲟⲓ",
        "tr": "That is why you get sick and die: because you love what tricks you. Anyone who can understand should understand.",
        "comm": "Death here is not a punishment laid on flesh. It is what follows from loving a trick. The object of love is not named as a demon. It is named as deceit — what has no stable face, what you keep marrying anyway. Sickness is the body's report of that marriage. The next unit will name the trick as imageless passion. This unit only places the cause: not matter, not the Savior's absence, but a love that prefers the cheat. The misconception: that you die because the world is evil. You die because you love what is lying to you.",
        "prac": "Name one thing you love that you already know is a trick (a refresh, a status, a story). Love it one degree less today. Do not replace it yet.",
        "terms": kt(
            ("ϩⲁⲗ", "trick / deceit — what is loved; the cause of sickness here"),
            ("ϣⲱⲛⲉ", "to be sick — the body's weather when love has no true object"),
            ("ⲙⲟⲩ", "to die — consequence of that love, not a sentence from outside"),
        ),
        "res": res(
            ("Gospel of Thomas 56", "Whoever has known the world has found a corpse.", "Thomas finds the world already dead; Mary finds death in a kind of loving."),
            ("Heraclitus B85", "It is hard to fight desire; whatever it wants, it buys with soul.", "Heraclitus prices desire in psyche; Mary prices the trick in sickness and death."),
        ),
    },
    {
        "n": 5,
        "title": "Passion has no image — be content at heart",
        "section": "BG 8502, p. 8",
        "coptic": "ⲧϩⲩⲗⲏ [ⲁⲥϫⲡⲉ] ⲟⲩⲡⲁⲑⲟⲥ ⲉⲙⲛⲧϥ ⲉⲓⲛⲉ ⲉⲃⲟⲗ ϫⲉ ⲛⲧⲁϥⲉⲓ ⲉⲃⲟⲗ ϩⲛ ⲟⲩⲡⲁⲣⲁⲫⲩⲥⲓⲥ ⲧⲟⲧⲉ ϣⲁⲣⲉ ⲟⲩϣⲧⲟⲣⲧⲣ ϣⲱⲡⲉ ϩⲙ ⲡⲥⲱⲙⲁ ⲧⲏⲣϥ ⲉⲧⲃⲉ ⲡⲁⲓ ⲁⲓϫⲟⲟⲥ ⲛⲏⲧⲛ ϫⲉ ϣⲱⲡⲉ ⲉⲧⲉⲧⲛϩⲏⲧ ⲥⲧⲟ ⲉϣⲱⲡⲉ ⲧⲉⲧⲛⲟ ⲛⲁⲧϩⲧⲏ ϭⲓⲛⲉ ⲛⲟⲩⲥⲧⲟ ⲙⲡⲉⲙⲧⲟ ⲉⲃⲟⲗ ⲛⲛⲉⲓⲇⲱⲗⲟⲛ ⲛⲧⲫⲩⲥⲓⲥ",
        "tr": "Matter gave birth to a passion that has no image, because it comes from what is contrary to nature. Then confusion arises in the whole body. That is why I told you to be content at heart. If you are discontented, find contentment in the presence of the various images of nature. Whoever has ears to hear should hear.",
        "comm": "The trick now has a physiology. Passion without an image — a heat that has no form because it is against nature. The body becomes a weather of confusion. The medicine is not contempt for images. It is contentment of heart, and if the heart is already split, to take contentment in the images of nature rather than in the imageless passion. The Savior does not say: flee the visible. He says: stop marrying the thing that has no face. Images of nature are allowed. The faceless urgency is not.",
        "prac": "Name one desire that has no image — a vague more, a faceless urgency. Set it down. Rest the heart on one actual thing of nature (light, weight, breath) for one minute.",
        "terms": kt(
            ("ⲡⲁⲑⲟⲥ", "passion — here imageless, born against nature, not every feeling"),
            ("ⲡⲁⲣⲁⲫⲩⲥⲓⲥ", "what is contrary to nature — the source of the faceless heat"),
            ("ϩⲧⲏ", "heart — contentment here is a placement of the heart, not a mood"),
        ),
        "res": res(
            ("Meister Eckhart, on detachment", "Imagelessness can be poverty that makes room, or a passion that has no face.", "Eckhart empties for God; Mary warns against an emptiness that is just hunger without an object."),
            ("Patañjali, Yoga Sūtra 1.2–3", "Stilling the turnings lets the seer rest in its nature.", "Patañjali stills citta; Mary traces confusion to loving a trick, then seats the heart among nature's images."),
        ),
    },
    {
        "n": 6,
        "title": "The Son of Humanity exists within you",
        "section": "BG 8502, pp. 8–9",
        "coptic": "ⲧⲉⲓⲣⲏⲛⲏ ⲛⲏⲧⲛ ϫⲓ ⲛⲁⲓ ⲛⲧⲁⲉⲓⲣⲏⲛⲏ ϩⲁⲣⲉϩ ϫⲉ ⲛⲛⲉⲗⲁⲁⲩ ⲣ ⲡⲗⲁⲛⲁ ⲙⲙⲱⲧⲛ ⲉϥϫⲱ ⲙⲙⲟⲥ ϫⲉ ⲉⲓⲥ ϩⲏⲡⲉ ⲙⲡⲉⲓⲥⲁ ⲏ ⲉⲓⲥ ϩⲏⲡⲉ ⲙⲡⲉⲓⲥⲁ ⲡϣⲏⲣⲉ ⲅⲁⲣ ⲙⲡⲣⲱⲙⲉ ϥϣⲟⲟⲡ ⲙⲡⲉⲧⲛϩⲟⲩⲛ ⲟⲩⲁϩⲧⲏⲩⲧⲛ ⲛⲥⲱϥ ⲛⲉⲧϣⲓⲛⲉ ⲛⲥⲱϥ ⲥⲉⲛⲁϩⲉ ⲉⲣⲟϥ",
        "tr": "Peace be with you. Acquire my peace. Be careful not to let anyone mislead you by saying, Look over here, or Look over there. The Son of Humanity exists within you. Follow him. Those who seek him will find him.",
        "comm": "The farewell is a map. Peace is to be acquired, not waited for as a mood. The Human One is not a figure on the horizon. He exists within. Follow is not travel; it is refusing the pointing-away. Luke 17 left entos open (within / among). Mary closes the pointing and keeps the within. The next unit will forbid the extra law. This one only relocates the one you follow. The misconception: that the living teaching is always over there — a teacher, a sign, a later age.",
        "prac": "Catch one spiritual 'look over there' today — a teacher, a sign, a mood. Return to the Human One as within. Stay ten breaths. Do not add a proof.",
        "terms": kt(
            ("ⲡϣⲏⲣⲉ ⲙⲡⲣⲱⲙⲉ", "Son of Humanity / the Human One — not a remote title; said to exist within"),
            ("ⲉⲓⲣⲏⲛⲏ", "peace — to be acquired, not waited for as a feeling"),
            ("ⲡⲗⲁⲛⲁ", "to mislead — the pointing-away that relocates what is already within"),
        ),
        "res": res(
            ("Luke 17:20–21", "The kingdom does not come with observation; it is within / among you.", "Luke's Greek is open (entos); Mary makes the Human One interior."),
            ("Gospel of Thomas 3", "The kingdom is inside you and outside you; leaders who point to sky or sea mislead.", "Thomas keeps inside-and-outside; Mary stresses within, then (next) the political danger of rule-making."),
        ),
    },
    {
        "n": 7,
        "title": "Do not lay down another law",
        "section": "BG 8502, p. 9",
        "coptic": "ⲃⲱⲕ ϭⲉ ⲛⲧⲉⲧⲛⲧⲁϣⲉⲟⲉⲓϣ ⲙⲡⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ ⲛⲧⲙⲛⲧⲣⲣⲟ ⲙⲡⲣⲕⲱ ⲛϩⲟⲣⲟⲥ ⲡⲁⲣⲁ ⲡⲉⲛⲧⲁⲓⲧⲁⲁϥ ⲛⲏⲧⲛ ⲟⲩⲇⲉ ⲙⲡⲣϯ ⲛⲟⲙⲟⲥ ⲛⲧϩⲉ ⲙⲡⲛⲟⲙⲟⲑⲉⲧⲏⲥ ⲙⲏⲡⲟⲧⲉ ⲛⲥⲉⲁⲙⲁϩⲧⲉ ⲙⲙⲱⲧⲛ ⲛϩⲏⲧϥ ⲛⲧⲉⲣⲉϥϫⲉ ⲛⲁⲓ ⲁϥⲃⲱⲕ",
        "tr": "Go then and preach the gospel of the kingdom. Do not lay down any rules beyond what I have given you, nor make a law like the lawgiver, lest you be bound by it. When he said these things, he left.",
        "comm": "Preach, then the second blow: do not become a second Moses. Extra rules bind the ones who make them. A gospel that starts as inner finding can harden, in a week, into a new law. Mary will later be accused of inventing teaching. This saying is why the accusation is false, and why Peter's later statute (who may hear) is already forbidden. He leaves. The group is now unsupervised. The misconception: that loyalty means adding fences around the gift.",
        "prac": "Name one extra spiritual rule you have added this month (a private law of who is in, what counts, when you are allowed). Drop it for today. Preach, if at all, without it.",
        "terms": kt(
            ("ϩⲟⲣⲟⲥ", "rule / limit — the extra statute that rebinds the free"),
            ("ⲛⲟⲙⲟⲑⲉⲧⲏⲥ", "lawgiver — the role they are forbidden to copy"),
            ("ⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ", "gospel — to be preached, not fenced"),
        ),
        "res": res(
            ("Matthew 23:4", "They tie heavy burdens and will not lift them.", "Matthew attacks the scribes' extra loads; Mary forbids the disciples from becoming that lawgiver."),
            ("Gospel of Thomas 14", "If you fast, you will beget sin for yourselves.", "Thomas warns that piety manufactures stain; Mary warns that extra law manufactures bondage."),
        ),
    },
    {
        "n": 8,
        "title": "If they did not spare him, why would they spare us?",
        "section": "BG 8502, p. 9",
        "coptic": "ⲛⲧⲟⲟⲩ ⲇⲉ ⲛⲉⲩⲗⲩⲡⲉⲓ ⲁⲩⲱ ⲁⲩⲣⲓⲙⲉ ⲉⲙⲁⲧⲉ ⲡⲉϫⲁⲩ ϫⲉ ⲛⲁϣ ⲛϩⲉ ⲧⲛⲛⲁⲃⲱⲕ ϣⲁ ⲛϩⲉⲑⲛⲟⲥ ⲛⲧⲛⲧⲁϣⲉⲟⲉⲓϣ ⲙⲡⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ ⲛⲧⲙⲛⲧⲣⲣⲟ ⲙⲡϣⲏⲣⲉ ⲙⲡⲣⲱⲙⲉ ⲉⲩⲧⲙϯ ⲥⲟ ⲇⲉ ⲛⲁϥ ⲉⲩⲛⲁϯ ⲥⲟ ⲛⲁⲛ ⲛⲁϣ ⲛϩⲉ",
        "tr": "But they grieved and wept bitterly. They said, How can we go to the Gentiles to preach the gospel of the kingdom of the Son of Humanity? If they did not spare him, why would they spare us?",
        "comm": "The men have the map and still collapse. The objection is not doctrinal. It is fear dressed as logistics: the Gentiles, the killing, the math of survival. They have just been told the Human One is within, and they locate danger only outside. Mary will stand in the next unit. This unit is the failure the farewell predicted — hearts divided, already, before a single Gentile is met. The misconception: that the obstacle to preaching is the world's violence. Here the obstacle is the weeping that cannot use the peace they were told to acquire.",
        "prac": "When a true task appears and you answer with 'they will not spare us,' name the fear without solving it. Acquire peace once (ten breaths). Then see whether the task is still impossible.",
        "terms": kt(
            ("ϩⲉⲑⲛⲟⲥ", "Gentiles / nations — the imagined outside that justifies not going"),
            ("ⲗⲩⲡⲉⲓ", "to grieve — the group's first act after the farewell"),
            ("ϯ ⲥⲟ", "to spare — they measure mission by whether violence will pause"),
        ),
        "res": res(
            ("Luke 24:17–21", "The downcast walkers: we had hoped he was the one; they crucified him.", "Luke's grief is on the road to Emmaus; Mary's is in the room, before any road."),
            ("John 20:19", "The doors were locked for fear of the Judeans.", "John locks the room; Mary will have a woman open it by turning hearts."),
        ),
    },
    {
        "n": 9,
        "title": "He has prepared us and made us Human",
        "section": "BG 8502, p. 9",
        "coptic": "ⲧⲟⲧⲉ ⲁⲙⲁⲣⲓϩⲁⲙ ⲧⲱⲟⲩⲛ ⲁⲥⲁⲥⲡⲁⲍⲉ ⲙⲙⲟⲟⲩ ⲧⲏⲣⲟⲩ ⲡⲉϫⲁⲥ ⲛⲛⲉⲥⲥⲛⲏⲩ ϫⲉ ⲙⲡⲣⲣⲓⲙⲉ ⲁⲩⲱ ⲙⲡⲣⲣ ⲗⲩⲡⲏ ⲟⲩⲇⲉ ⲙⲡⲣⲣ ϩⲏⲧ ⲥⲛⲁⲩ ⲧⲉϥⲭⲁⲣⲓⲥ ⲅⲁⲣ ⲛⲁϣⲱⲡⲉ ⲛⲙⲙⲏⲧⲛ ⲧⲏⲣⲧⲛ ⲁⲩⲱ ⲥⲛⲁⲣ ⲥⲕⲉⲡⲁⲍⲉ ⲙⲙⲱⲧⲛ ⲙⲁⲗⲗⲟⲛ ⲙⲁⲣⲛⲥⲙⲟⲩ ⲉⲧⲉϥⲙⲛⲧⲛⲟϭ ϫⲉ ⲁϥⲥⲃⲧⲱⲧⲛ ⲁϥⲁⲁⲛ ⲛⲣⲱⲙⲉ",
        "tr": "Then Mary arose, greeted them all, and said to her brothers and sisters, Do not weep and do not grieve, and do not let your hearts be divided, for his grace will be with you all and will protect you. Rather we should praise his greatness, because he has prepared us and made us Human.",
        "comm": "Mary does not add information first. She stops the split heart, names grace as already with them, and recalls what they have been made: Human — the same word as the Human One within. Leadership here is not rank. It is the one who can stand when the group is weeping about Gentiles and death. The later quarrel with Peter is already seeded: she has done the thing the farewell asked. The misconception: that after the teacher leaves, the remaining work is strategy. The remaining work is stature.",
        "prac": "In one anxious group (a thread, a table, a family), do not add a plan. Stop the split. Name one grace already with you. Speak as Human, not as the frightened remainder.",
        "terms": kt(
            ("ϩⲏⲧ ⲥⲛⲁⲩ", "a divided / double heart — the first thing Mary forbids"),
            ("ⲣⲱⲙⲉ", "Human — what the Savior has made them; not a gender, a stature"),
            ("ⲭⲁⲣⲓⲥ", "grace — with you, not waiting at the Gentile border"),
        ),
        "res": res(
            ("John 1:12–13", "Authority to become children of God, born not of bloods.", "John's childship is given by receiving the light; Mary's Human is a stature already prepared."),
            ("Gospel of Thomas 3", "When you know yourselves you will know you are children of the living Father.", "Thomas ties stature to self-knowledge; Mary announces it to a weeping room."),
        ),
    },
    {
        "n": 10,
        "title": "She turned their hearts toward the Good",
        "section": "BG 8502, p. 9",
        "coptic": "ⲛⲧⲉⲣⲉ ⲙⲁⲣⲓϩⲁⲙ ϫⲉ ⲛⲁⲓ ⲁⲥⲕⲧⲉ ⲡⲉⲩϩⲏⲧ ⲉϩⲟⲩⲛ ⲉⲡⲁⲅⲁⲑⲟⲛ ⲁⲩⲱ ⲁⲩⲁⲣⲭⲉⲓ ⲛϣⲁϫⲉ ⲉⲛϣⲁϫⲉ ⲙⲡⲥⲱⲧⲏⲣ",
        "tr": "When Mary said these things, she turned their hearts toward the Good, and they began to discuss the words of the Savior.",
        "comm": "The turning is the miracle of this page. Not a new vision. Not a vote. Hearts that were split now face the Good, and talk can begin. The Good is the same one that came to restore natures. Mary does not become the Good. She turns them toward it. Peter will ask her, next, for hidden words — because the turning worked, and he will need to contain it. The misconception: that leadership is having more content. Here it is an orientation of the heart that lets the already-given words be discussed.",
        "prac": "After you speak one true thing in a stuck conversation, stop. See whether hearts can turn. If they do, let the group discuss. Do not collect the turning as your proof.",
        "terms": kt(
            ("ⲕⲧⲉ ϩⲏⲧ", "to turn the heart — Mary's act; not persuasion as winning"),
            ("ⲡⲁⲅⲁⲑⲟⲛ", "the Good — the direction of the turn, already named as restorer"),
            ("ϣⲁϫⲉ", "words / discussion — what becomes possible after the turn"),
        ),
        "res": res(
            ("Luke 24:32", "Were not our hearts burning when he opened the word to us?", "Luke's burning is on the road with unrecognized Jesus; Mary's turning is in the room, by a disciple."),
            ("Śiva Sūtra I.2", "Knowledge is bondage — group knowledge without a turned heart is still collapse.", "The sūtra diagnoses; Mary performs the turning."),
        ),
    },
    {
        "n": 11,
        "title": "Tell us what we have not heard",
        "section": "BG 8502, p. 10",
        "coptic": "ⲡⲉϫⲉ ⲡⲉⲧⲣⲟⲥ ⲛⲙⲁⲣⲓϩⲁⲙ ϫⲉ ⲧⲥⲱⲛⲉ ⲧⲛⲥⲟⲟⲩⲛ ϫⲉ ⲁ ⲡⲥⲱⲧⲏⲣ ⲙⲉ ⲙⲙⲟ ⲛϩⲟⲩⲟ ⲉⲡⲕⲉⲥⲉⲉⲡⲉ ⲛⲛⲉϩⲓⲟⲙⲉ ϫⲱ ⲉⲣⲟⲛ ⲛⲛϣⲁϫⲉ ⲙⲡⲥⲱⲧⲏⲣ ⲉⲧⲉⲣⲉⲡⲉⲉⲓⲙⲉ ⲉⲣⲟⲟⲩ ⲉⲧⲛⲥⲟⲟⲩⲛ ⲙⲙⲟⲟⲩ ⲁⲛ ⲁⲩⲱ ⲉⲙⲡⲛⲥⲟⲧⲙⲟⲩ ⲡⲉϫⲉ ⲙⲁⲣⲓϩⲁⲙ ϫⲉ ⲡⲉⲑⲏⲡ ⲉⲣⲱⲧⲛ ϯⲛⲁⲧⲁⲩⲟϥ ⲉⲣⲱⲧⲛ",
        "tr": "Peter said to Mary, Sister, we know the Savior loved you more than the rest of the women. Tell us the words of the Savior that you remember, that you know and we do not, which we have not heard. Mary said, What is hidden from you I will proclaim to you.",
        "comm": "Peter admits a privilege and immediately contains it: more than the rest of the women. The request is real; the frame is a cage. Mary does not debate the containment. She offers what is hidden. Later he will resent that she had anything to offer. This unit is the hinge: he asks her to speak as a specialist of the women's column, and she answers as a witness of the hidden. The misconception: that love-more-than-the-women is the same as being heard. It is the setup for not being heard.",
        "prac": "Notice one time you ask someone to speak and already have a smaller box for what they are allowed to know. Drop the box. Hear the hidden as hidden, not as a gendered specialty.",
        "terms": kt(
            ("ⲥⲱⲛⲉ", "sister — Peter's address; kinship that still ranks her among the women"),
            ("ⲡⲉⲑⲏⲡ", "what is hidden — Mary's offering; not a secret club, a withheld teaching"),
            ("ⲛⲉϩⲓⲟⲙⲉ", "the women — the column Peter uses to contain the privilege he admits"),
        ),
        "res": res(
            ("Luke 10:39–42", "Mary sits at the Lord's feet; Martha's complaint is about a woman's place.", "Luke defends Mary's listening; this Peter invites Mary's speaking, then will punish it."),
            ("Gospel of Thomas 114", "Simon Peter said, Let Mary leave us, for women are not worthy of life.", "Thomas's Peter wants her out before she speaks; this Peter invites her, then turns."),
        ),
    },
    {
        "n": 12,
        "title": "Where the mind is, there is the treasure",
        "section": "BG 8502, p. 10",
        "coptic": "ⲁⲓⲛⲁⲩ ⲉⲡϫⲟⲉⲓⲥ ϩⲛ ⲟⲩϩⲟⲣⲟⲙⲁ ⲡⲉϫⲁⲓ ⲛⲁϥ ϫⲉ ⲡϫⲟⲉⲓⲥ ⲁⲓⲛⲁⲩ ⲉⲣⲟⲕ ⲙⲡⲟⲟⲩ ϩⲛ ⲟⲩϩⲟⲣⲟⲙⲁ ⲡⲉϫⲁϥ ⲛⲁⲓ ϫⲉ ⲛⲧⲟ ϩⲉⲛⲙⲁⲕⲁⲣⲓⲟⲥ ϫⲉ ⲙⲡⲉⲥⲧⲱⲧ ⲉⲁⲛⲁⲩ ⲉⲣⲟⲓ ⲡⲙⲁ ⲅⲁⲣ ⲉⲧⲉ ⲡⲛⲟⲩⲥ ⲙⲙⲁⲩ ⲉϥⲙⲙⲁⲩ ⲛϭⲓ ⲡⲉϩⲟ",
        "tr": "I saw the Lord in a vision and said, Lord, I saw you today in a vision. He said, You are blessed because you did not waver at the sight of me. For where the mind is, there is the treasure.",
        "comm": "The blessing is not seeing. It is not wavering at the seeing. Then the sentence that relocates the whole gospel: where the nous is, there is the treasure. Not where the relic is. Not where the male college is. Mind, here, is the seeing-place between soul and spirit (the next question). Treasure follows attention. If the mind wavers, the Lord is a spectacle; if it holds, the vision is a location of wealth. Matthew tied treasure to heart. Mary ties it to unwavering mind.",
        "prac": "When a true thing appears today (a person, a sentence, a silence), notice the waver. Hold the mind there for ten breaths. Do not collect the experience as status.",
        "terms": kt(
            ("ⲛⲟⲩⲥ", "mind / nous — the seeing-place; where it is, the treasure is"),
            ("ϩⲟ", "treasure — not stored elsewhere than attention"),
            ("ⲥⲧⲱⲧ", "to waver / shake — the failure; blessedness is unwavering, not the having of sights"),
        ),
        "res": res(
            ("Matthew 6:21", "Where your treasure is, there your heart will be.", "Matthew ties treasure to heart; Mary ties it to nous, and to not wavering in vision."),
            ("Gospel of Thomas 2", "The seeker is troubled, astonished, then rules — finding is a shock, not a possession.", "Thomas sequences seeking; Mary locates the treasure in unwavering mind."),
        ),
    },
    {
        "n": 13,
        "title": "Neither soul nor spirit sees — the mind between",
        "section": "BG 8502, p. 10 (then lacuna pp. 11–14)",
        "coptic": "ⲡϫⲟⲉⲓⲥ ⲧⲉⲛⲟⲩ ⲡⲉⲧⲛⲁⲩ ⲉϩⲟⲣⲟⲙⲁ ⲉϥⲛⲁⲩ ⲉⲣⲟϥ ϩⲛ ⲧⲉⲯⲩⲭⲏ ϩⲛ ⲡⲉⲡⲛⲉⲩⲙⲁ ⲡⲉϫⲉ ⲡⲥⲱⲧⲏⲣ ϫⲉ ⲙⲁϥⲛⲁⲩ ϩⲛ ⲧⲉⲯⲩⲭⲏ ⲟⲩⲇⲉ ϩⲙ ⲡⲉⲡⲛⲉⲩⲙⲁ ⲁⲗⲗⲁ ⲡⲛⲟⲩⲥ ⲉⲧϣⲟⲟⲡ ⲟⲩⲧⲉ ⲡⲥⲛⲁⲩ ⲡⲉⲧⲛⲁⲩ ⲉϩⲟⲣⲟⲙⲁ ⲁⲩⲱ ⲛⲧⲟϥ [...]",
        "tr": "I said to him, Lord, does the one who sees the vision see it in the soul or in the spirit? The Savior said, They do not see in the soul or in the spirit, but the mind which exists between the two is what sees the vision. [pages 11–14 missing]",
        "comm": "Mary asks the technical question every visionary tradition has to answer: which faculty sees? Soul and spirit are refused as the organ. Nous stands between them. The lacuna that follows is the gospel's honest wound: the ascent teaching is torn out, and we re-enter mid-climb. Do not fill the gap with a system. The surviving claim is already sharp. Vision is not a soul-mood and not a spirit-possession. It is mind, between. If you skip this, the later powers look like a cartoon afterlife. They are what a mind meets when it is actually seeing.",
        "prac": "Sit five minutes. When a seeing arises, ask: is this mood (soul) or inflation (spirit)? Rest as the between. When you cannot tell, that is the gate.",
        "terms": kt(
            ("ⲯⲩⲭⲏ", "soul — refused as the seer of the vision"),
            ("ⲡⲛⲉⲩⲙⲁ", "spirit — also refused; vision is not possession"),
            ("ⲟⲩⲧⲉ ⲡⲥⲛⲁⲩ", "between the two — nous as the interval, not a third substance to collect"),
        ),
        "res": res(
            ("Plotinus, Ennead V.1", "The soul sees the Intellectual-Principle by becoming like it, not by a lower faculty.", "Plotinus ranks hypostases; Mary names a between that is the organ of vision."),
            ("Pseudo-Dionysius, Mystical Theology I", "Leave sense and intellect for the ray of divine darkness.", "Dionysius strips nous at the summit; Mary needs nous as the seer of the vision. Divergence: different rungs."),
        ),
    },
    {
        "n": 14,
        "title": "I was a garment, and you did not know me",
        "section": "BG 8502, p. 15",
        "coptic": "ⲡⲉϫⲉ ⲧⲉⲡⲓⲑⲩⲙⲓⲁ ϫⲉ ⲙⲡⲓⲛⲁⲩ ⲉⲣⲟ ⲉⲣⲉⲃⲏⲕ ⲉⲡⲉⲥⲏⲧ ⲧⲉⲛⲟⲩ ⲇⲉ ϯⲛⲁⲩ ⲉⲣⲟ ⲉⲣⲉⲃⲏⲕ ⲉϩⲣⲁⲓ ⲉⲧⲃⲉ ⲟⲩ ⲧⲉϫⲓϭⲟⲗ ⲉⲡⲉⲓⲇⲏ ⲧⲉϩⲛ ⲧⲁⲉⲓ ⲡⲉϫⲉ ⲧⲉⲯⲩⲭⲏ ϫⲉ ⲁⲓⲛⲁⲩ ⲉⲣⲟ ⲛⲧⲟ ⲙⲡⲉⲛⲁⲩ ⲉⲣⲟⲓ ⲟⲩⲇⲉ ⲙⲡⲉⲥⲟⲩⲱⲛⲧ ⲛⲉⲓϣⲟⲟⲡ ⲛⲉ ⲛⲧⲟ ⲛⲑⲉ ⲛⲟⲩϩⲟⲓⲧⲉ ⲁⲩⲱ ⲙⲡⲉⲥⲟⲩⲱⲛⲧ ⲛⲧⲉⲣⲉⲥϫⲉ ⲛⲁⲓ ⲁⲥⲃⲱⲕ ⲉⲥⲣⲁϣⲉ ⲉⲙⲁⲧⲉ",
        "tr": "Desire said, I did not see you going down, but now I see you going up. Why are you lying, since you belong to me? The soul said, I saw you, but you did not see me or know me. I was to you just a garment, and you did not recognize me. When it said this, it left, rejoicing greatly.",
        "comm": "We re-enter mid-ascent. Desire's claim is ownership: you came up through me, so you are mine. The soul's answer is the whole anthropology of the book. Desire never saw the soul — only the garment. Belonging was a costume-error. The soul saw Desire; Desire did not know the wearer. Recognition is one-way, and that is enough to leave rejoicing. This is not prudery about wanting. It is the end of being identified with the heat that mistook a dress for a person.",
        "prac": "Name one desire that talks as if you belong to it. Answer, silently: you saw a garment. Walk to the next task without arguing with it.",
        "terms": kt(
            ("ⲉⲡⲓⲑⲩⲙⲓⲁ", "Desire — a power that claims the soul because it saw the ascent"),
            ("ϩⲟⲓⲧⲉ", "garment — what Desire knew; not the soul"),
            ("ⲥⲟⲩⲱⲛ", "recognize / know — Desire's failure; the soul's success"),
        ),
        "res": res(
            ("Gospel of Thomas 37", "When you take off your clothes without shame and put them underfoot — the garment is not you.", "Thomas makes stripping a condition of seeing; Mary makes Desire the one who never saw past the cloth."),
            ("Lalla, 'I found him in my own house'", "The search abroad mistakes a costume for a missing person.", "Lalla finds the guru as Self; Mary finds that Desire never knew her."),
        ),
    },
    {
        "n": 15,
        "title": "Ignorance says you are bound — do not judge",
        "section": "BG 8502, p. 15",
        "coptic": "ⲁⲥⲉⲓ ⲉϩⲣⲁⲓ ⲉⲧⲙⲉϩϣⲟⲙⲧⲉ ⲛϭⲟⲙ ⲉϣⲁⲩⲙⲟⲩⲧⲉ ⲉⲣⲟⲥ ϫⲉ ⲧⲙⲛⲧⲁⲧⲥⲟⲟⲩⲛ ⲁⲥϫⲛⲟⲩ ⲛⲧⲉⲯⲩⲭⲏ ϫⲉ ⲉⲣⲉⲃⲏⲕ ⲉⲧⲱⲛ ϩⲛ ⲟⲩⲡⲟⲛⲏⲣⲓⲁ ⲧⲉⲙⲏⲣ ⲉⲡⲉⲓⲇⲏ ⲧⲉⲙⲏⲣ ⲙⲡⲣⲣ ϩⲁⲡ",
        "tr": "It came to the third power, which is called Ignorance. It interrogated the soul: Where are you going? In wickedness you are bound. Since you are bound, do not judge.",
        "comm": "Ignorance moralizes. It calls the soul wicked and bound, then forbids judgment — a trap that uses spiritual language to keep the climber in place. 'Do not judge' from a jailer is not the Savior's teaching. It is a power borrowing a holy sentence. The next unit is the soul's answer. This one is the trap, isolated so you can hear the voice. The misconception: that every interior 'you are bound, be humble' is wisdom. Hear who is speaking.",
        "prac": "When an inner voice calls you bound and then says do not judge, name it Ignorance before you obey. Ask: is this a jailer or a teacher? Do not answer the jailer yet.",
        "terms": kt(
            ("ⲙⲛⲧⲁⲧⲥⲟⲟⲩⲛ", "Ignorance — a power that binds by moral interrogation"),
            ("ⲙⲏⲣ", "bound — the charge; also the condition Ignorance needs you to accept"),
            ("ϩⲁⲡ", "judgment — here forbidden by the jailer, not by the Savior"),
        ),
        "res": res(
            ("Matthew 7:1", "Do not judge, lest you be judged.", "Jesus forbids judging; Ignorance weaponizes the same sentence to halt ascent. Hear who is speaking."),
            ("Gospel of Thomas 39", "The Pharisees took the keys of knowledge and hid them; they did not enter, and did not let those who wanted to enter.", "Thomas's hiders block the door; Mary's Ignorance blocks with a pious command."),
        ),
    },
    {
        "n": 16,
        "title": "Why do you judge me, since I have not judged?",
        "section": "BG 8502, pp. 15–16",
        "coptic": "ⲡⲉϫⲉ ⲧⲉⲯⲩⲭⲏ ϫⲉ ⲉⲧⲃⲉ ⲟⲩ ⲧⲉⲣ ϩⲁⲡ ⲉⲣⲟⲓ ⲉⲙⲡⲓⲣ ϩⲁⲡ ⲁⲩⲙⲣⲣ ⲉⲣⲟⲓ ⲉⲙⲡⲓⲙⲣⲣ ⲙⲡⲟⲩⲥⲟⲩⲱⲛⲧ ⲁⲛⲟⲕ ⲇⲉ ⲁⲓⲥⲟⲩⲱⲛ ϫⲉ ⲡⲧⲏⲣϥ ⲛⲁⲃⲱⲗ ⲉⲃⲟⲗ ⲛⲁ ⲡⲕⲁϩ ⲙⲛ ⲛⲁ ⲧⲡⲉ",
        "tr": "The soul said, Why do you judge me, since I have not judged? I was bound, though I have not bound. They did not recognize me, but I have recognized that everything will dissolve — both the things of earth and the things of heaven.",
        "comm": "The soul does not accept the charge. I have not judged; I have not bound; you did not know me. What it does know is the first teaching of the book, now used as a passport: everything will dissolve. Heaven is not exempt. If even heaven dissolves, Ignorance's courtroom is temporary. Recognition here is one-way again, as with Desire: they did not know me; I have known the physics. The misconception: that to pass a moralizing power you must accept its verdict and then be humble. The soul refuses the verdict and remembers dissolution.",
        "prac": "Restate the first teaching against one inner court today: this too will dissolve, earth and heaven. Take the next honest step without accepting the charge.",
        "terms": kt(
            ("ϩⲁⲡ", "judgment — the soul refuses the charge of having judged"),
            ("ⲃⲱⲗ ⲉⲃⲟⲗ", "dissolve — earth and heaven; Ignorance's court included"),
            ("ⲥⲟⲩⲱⲛ", "recognize — they failed; the soul succeeded, and what it knows is unbinding"),
        ),
        "res": res(
            ("Gospel of Mary, BG 8502 p. 7", "Matter dissolves into its own root.", "The opening physics becomes, at this gate, a weapon against a power."),
            ("Nāgārjuna, MMK 24.18", "Empty things can dissolve because they have no essence.", "Nāgārjuna argues emptiness; Mary's soul uses dissolution as a passport past a power."),
        ),
    },
    {
        "n": 17,
        "title": "The seven forms of Wrath",
        "section": "BG 8502, p. 16",
        "coptic": "ⲧⲙⲉϩϥⲧⲟ ⲛϭⲟⲙ ⲉⲁⲥϫⲓ ⲛⲥⲁϣϥⲉ ⲛⲙⲟⲣⲫⲏ ⲧϣⲟⲣⲡ ⲧⲉ ⲡⲕⲁⲕⲉ ⲧⲙⲉϩⲥⲛⲧⲉ ⲧⲉⲡⲓⲑⲩⲙⲓⲁ ⲧⲙⲉϩϣⲟⲙⲧⲉ ⲧⲙⲛⲧⲁⲧⲥⲟⲟⲩⲛ ⲧⲙⲉϩϥⲧⲟ ⲡⲕⲱϩ ⲙⲡⲙⲟⲩ ⲧⲙⲉϩϯ ⲧⲙⲛⲧⲣⲣⲟ ⲛⲧⲥⲁⲣⲝ ⲧⲙⲉϩⲥⲟ ⲧⲙⲛⲧⲥⲟϭ ⲛⲥⲟⲫⲓⲁ ⲛⲧⲥⲁⲣⲝ ⲧⲙⲉϩⲥⲁϣϥⲉ ⲧⲥⲟⲫⲓⲁ ⲛⲧⲟⲣⲅⲏ ⲛⲁⲓ ⲛⲉ ⲧⲥⲁϣϥⲉ ⲛϭⲟⲙ ⲛⲧⲟⲣⲅⲏ",
        "tr": "When the soul had overcome the third power, it went up and saw the fourth power, which took seven forms: Darkness; Desire; Ignorance; Zeal for Death; the Kingdom of the Flesh; the Foolish Wisdom of Flesh; the Wisdom of Anger. These are the seven powers of Wrath.",
        "comm": "Wrath is not one feeling. It is a seven-form checkpoint: dark, want, not-knowing, death-zeal, flesh-kingdom, clever flesh, angry wisdom. Desire and Ignorance, already passed as separate powers, return as forms of Wrath — the climb is not a list you finish. The last two are the most religious: a stupid wisdom of flesh, and a wisdom that is just anger with a doctrine. The misconception: that wrath is only heat. Here it includes the cleverness that defends the flesh and the ideology that burns. Name the form, or you will think you have passed Wrath while sitting in its seventh face.",
        "prac": "When anger appears today, do not only call it anger. Ask which form it is wearing (dark, want, not-knowing, death-zeal, flesh-kingdom, cleverness, angry wisdom). Name the form once. Do not argue with it yet.",
        "terms": kt(
            ("ⲟⲣⲅⲏ", "Wrath — a seven-formed power, not a passing temper"),
            ("ⲙⲟⲣⲫⲏ", "form — Wrath's disguises; Desire and Ignorance among them"),
            ("ⲥⲟⲫⲓⲁ ⲛⲧⲥⲁⲣⲝ", "wisdom of flesh — cleverness in the service of the body-kingdom"),
        ),
        "res": res(
            ("Evagrius, Praktikos 6–14", "The eight logismoi, including anger and vainglory, as a sequence of thoughts.", "Evagrius maps thoughts to starve; Mary maps Wrath as a power with seven faces on an ascent."),
            ("John 8:44", "The devil is a liar and the father of it — a single adversary.", "John gives one father of lies; Mary gives Wrath a seven-form anatomy, including religious wisdom."),
        ),
    },
    {
        "n": 18,
        "title": "Where do you come from, murderer?",
        "section": "BG 8502, p. 16",
        "coptic": "ⲥⲉϫⲛⲟⲩ ⲛⲧⲉⲯⲩⲭⲏ ϫⲉ ⲉⲣⲉⲛⲏⲩ ⲧⲱⲛ ⲧⲉⲥϩⲟⲧⲃⲉ ⲁⲩⲱ ⲉⲣⲉⲃⲏⲕ ⲉⲧⲱⲛ ⲧⲉⲣⲣⲟ ⲛⲧⲟⲡⲟⲥ",
        "tr": "They ask the soul, Where do you come from, you murderer, and where are you going, conqueror of space?",
        "comm": "The powers call the soul a murderer because it has killed the binders. Conqueror of space is not a compliment. It is an accusation: you have left our territory. Origin and destination questions are how Wrath stalls a climber who has already passed Desire and Ignorance. The soul will answer in the next unit with past tenses. This unit is the charge. The misconception: that if you are named violent by a power you have outgrown, you must be violent. Sometimes the killing is of what bound you, and the name is the power's last tool.",
        "prac": "When you are called too much — too hard, too gone, too 'murderous' toward an old loyalty — ask who is naming you. If it is a binder you already left, do not take the name. Keep walking.",
        "terms": kt(
            ("ⲣⲉϥϩⲱⲧⲃ", "murderer — Wrath's name for the soul that killed its binders"),
            ("ⲣⲣⲟ ⲛⲧⲟⲡⲟⲥ", "conqueror of space / place — accused of leaving the powers' territory"),
            ("ⲧⲱⲛ", "where — origin and destination as stalling questions"),
        ),
        "res": res(
            ("John 8:14", "I know where I came from and where I am going; you do not know.", "Jesus answers the where; Mary's powers ask it to halt. Next unit: the soul answers anyway."),
            ("Gospel of Thomas 50", "If they ask you, Where did you come from?, say: we came from the light.", "Thomas scripts the passport; Mary lets Wrath insult, then answers with past-tense freedom."),
        ),
    },
    {
        "n": 19,
        "title": "What binds me has been killed — rest in silence",
        "section": "BG 8502, pp. 16–17",
        "coptic": "ⲡⲉϫⲉ ⲧⲉⲯⲩⲭⲏ ϫⲉ ⲡⲉⲧⲙⲟⲩⲣ ⲙⲙⲟⲓ ⲁⲩϩⲟⲧⲃϥ ⲁⲩⲱ ⲡⲉⲧⲕⲱⲧⲉ ⲉⲣⲟⲓ ⲁⲩϫⲣⲟ ⲉⲣⲟϥ ⲧⲁⲉⲡⲓⲑⲩⲙⲓⲁ ⲁⲥⲗⲟ ⲁⲩⲱ ⲧⲙⲛⲧⲁⲧⲥⲟⲟⲩⲛ ⲁⲥⲙⲟⲩ ϩⲛ ⲟⲩⲕⲟⲥⲙⲟⲥ ⲁⲩⲃⲟⲗⲧ ⲉⲃⲟⲗ ϩⲛ ⲟⲩⲕⲟⲥⲙⲟⲥ ⲁⲩⲱ ϩⲛ ⲟⲩⲧⲩⲡⲟⲥ ⲉⲃⲟⲗ ϩⲛ ⲟⲩⲧⲩⲡⲟⲥ ⲉϥϩⲓϫⲱϥ ⲁⲩⲱ ⲉⲃⲟⲗ ϩⲙ ⲡⲙⲣⲣⲉ ⲛⲧⲃϣⲉ ⲉϣⲁϥϣⲱⲡⲉ ϩⲛ ⲟⲩⲟⲉⲓϣ ϫⲓⲛ ⲧⲉⲛⲟⲩ ϯⲛⲁϫⲓ ⲛⲧⲁⲛⲁⲡⲁⲩⲥⲓⲥ ⲙⲡⲉⲭⲣⲟⲛⲟⲥ ⲛⲧⲉⲕⲁⲓⲣⲟⲥ ⲙⲡⲉⲛⲉϩ ϩⲛ ⲟⲩⲕⲁⲣⲱϥ",
        "tr": "The soul said, What binds me has been killed, what surrounds me has been overcome, my desire is gone, and ignorance has died. In a world I was released from a world, and in a type from a type which is above, and from the chain of forgetfulness which exists only for a time. From now on I will receive the rest of the time of the age in silence.",
        "comm": "The passport is past tense: binders killed, desire gone, ignorance dead, the chain of forgetfulness only for a time. Rest (anapausis) is received in silence — the same rest Matthew's yoke promised. Released from a world in a world: not extraction to another planet, a release inside the field. Type from a type above: the pattern-level is also left. The misconception: that arrival is more speech, more map, more proving you have passed. The soul's last act in the ascent is to take the rest of the age without talking.",
        "prac": "After one true sentence today, stop. Do not add the clever flesh-wisdom or the angry wisdom. Receive the rest of the hour in silence.",
        "terms": kt(
            ("ⲃϣⲉ", "forgetfulness — a chain that exists only for a time"),
            ("ⲁⲛⲁⲡⲁⲩⲥⲓⲥ", "rest — received, from now on, in silence"),
            ("ⲕⲁⲣⲱϥ", "silence — the rest of the age; the soul's remaining practice"),
        ),
        "res": res(
            ("Matthew 11:28–30", "Come to me, all who labor; you will find rest for your souls.", "Matthew's rest is under a kind yoke; Mary's is after the powers, in silence."),
            ("Pseudo-Dionysius, Mystical Theology I", "The mysteries are veiled in a silence that teaches secrets.", "Dionysius's silence is super-luminous darkness; Mary's is the soul's rest after Wrath."),
        ),
    },
    {
        "n": 20,
        "title": "Mary fell silent",
        "section": "BG 8502, p. 17",
        "coptic": "ⲛⲧⲉⲣⲉ ⲙⲁⲣⲓϩⲁⲙ ϫⲉ ⲛⲁⲓ ⲁⲥⲕⲁⲣⲱⲥ ϫⲉ ⲛⲉ ⲁ ⲡⲥⲱⲧⲏⲣ ϣⲁϫⲉ ⲛⲙⲙⲁⲥ ϣⲁ ⲡⲉⲓⲙⲁ",
        "tr": "When Mary said these things, she fell silent, because the Savior had spoken with her up to this point.",
        "comm": "The form of the gospel becomes the practice. Mary does not add a conclusion, a moral, or a claim to have seen the rest of the lost pages. She stops because he stopped. The lacuna of pp. 11–14 is not filled by invention. Silence here is fidelity to the measure of the speech, not a failure of nerve. Andrew and Peter will rush into that silence with objections. The misconception: that a teacher who falls silent has not finished, and that the group must complete her. The book says she finished when he did.",
        "prac": "When you have said all that was actually given, stop. Do not complete the silence with a theory. Let someone else speak first, or let no one.",
        "terms": kt(
            ("ⲕⲁⲣⲱⲥ", "she fell silent — the narrator's act matching the soul's rest"),
            ("ϣⲁ ⲡⲉⲓⲙⲁ", "up to this point — the measure of the Savior's speech; Mary will not exceed it"),
            ("ⲡⲥⲱⲧⲏⲣ", "the Savior — still the source; Mary is witness, not author of extra ending"),
        ),
        "res": res(
            ("The Cloud of Unknowing, 'I do not know'", "The teacher falls into the cloud with the student.", "The Cloud's silence is chosen unknowing; Mary's is the end of a reported ascent."),
            ("Gospel of Thomas 13", "Jesus took Thomas aside; when Thomas returns he will not say what Jesus said.", "Thomas withholds; Mary has spoken and then matches his stopping-point."),
        ),
    },
    {
        "n": 21,
        "title": "These teachings seem like different ideas",
        "section": "BG 8502, p. 17",
        "coptic": "ⲡⲉϫⲉ ⲁⲛⲇⲣⲉⲁⲥ ϫⲉ ϫⲟⲟⲥ ⲉⲧⲉⲧⲛⲟⲩⲱϣ ⲉⲧⲃⲉ ⲡⲉⲛⲧⲁⲥϫⲟⲟϥ ⲁⲛⲟⲕ ϩⲱ ϯⲡⲓⲥⲧⲉⲩⲉ ⲁⲛ ϫⲉ ⲁ ⲡⲥⲱⲧⲏⲣ ϫⲉ ⲛⲁⲓ ⲉϣϫⲉ ⲛⲉⲓⲥⲃⲟⲟⲩⲉ ⲅⲁⲣ ϩⲛ ⲕⲉⲙⲉⲉⲩⲉ ⲛⲉ",
        "tr": "Andrew said, Say what you will about what she has said; I myself do not believe the Savior said these things, because these teachings seem like different ideas.",
        "comm": "The powers now wear a face in the circle. Andrew's objection is doctrinal: different ideas — alien, other-minded, not our school. He grants the others permission to like it and withholds belief. This is a cleaner trap than Peter's, because it sounds like discernment. The ascent, the garment, the silence: he files them as another theology. The misconception: that 'this does not sound like us' is the same as 'this is not from the Savior.' Sometimes the Savior said the part you were not in the room for.",
        "prac": "When a teaching feels like 'different ideas,' pause before you file it as not-ours. Ask only: does it restore natures to their root, or add a law? Answer from that, not from the school-sound.",
        "terms": kt(
            ("ⲕⲉⲙⲉⲉⲩⲉ", "different ideas / other thoughts — Andrew's charge that the teaching is alien"),
            ("ⲡⲓⲥⲧⲉⲩⲉ", "believe — Andrew withholds it as if belief were a vote on style"),
            ("ⲥⲃⲟⲟⲩⲉ", "teachings — what he will not credit to the Savior"),
        ),
        "res": res(
            ("Luke 24:11", "The women's resurrection report seemed to the apostles an idle tale.", "Luke's men disbelieve the empty tomb as nonsense; Andrew disbelieves the inner ascent as a different school."),
            ("Gospel of Thomas 13", "The disciples compare Jesus to an angel or a wise philosopher; Thomas will not compare.", "Thomas's others reduce him to a type; Andrew reduces Mary to a rival type."),
        ),
    },
    {
        "n": 22,
        "title": "Did he speak with a woman without our knowledge?",
        "section": "BG 8502, pp. 17–18",
        "coptic": "ⲡⲉϫⲉ ⲡⲉⲧⲣⲟⲥ ϫⲉ ⲙⲏ ⲁϥϣⲁϫⲉ ⲙⲛ ⲟⲩⲥϩⲓⲙⲉ ⲛϫⲓⲟⲩⲉ ⲉⲣⲟⲛ ⲁⲩⲱ ⲁⲛ ⲉⲛⲟⲩⲟⲛϩ ⲉⲃⲟⲗ ⲉⲛⲛⲁⲕⲧⲟⲛ ⲁⲛⲟⲛ ⲧⲏⲣⲛ ⲛⲥⲱⲧⲙ ⲛⲥⲱⲥ ⲁϥⲥⲉⲧⲡⲥ ⲉϩⲟⲩⲉ ⲣⲟⲛ",
        "tr": "Peter spoke with the same concerns. He asked them concerning the Savior: He did not speak with a woman without our knowledge and not publicly with us, did he? Will we turn around and all listen to her? Did he prefer her to us?",
        "comm": "Peter's objection is gendered and institutional: a woman, in secret, preferred. He had asked her to speak. He now resents the speaking. The hidden teaching he requested is now evidence against her. Preference is the wound — more than us, not more than the rest of the women, the frame he used when he invited her. The extra law of who may hear is being drafted in real time. The misconception: that asking someone to testify means you will accept the testimony. Here the invitation was a test she was not allowed to pass.",
        "prac": "Notice one place you asked someone to speak and then resented the authority of what they said. Name the resentment without defending it. Listen once more, as if you had not invited them only to rank them.",
        "terms": kt(
            ("ⲥϩⲓⲙⲉ", "woman — Peter's containment; the issue he makes of the vessel"),
            ("ⲛϫⲓⲟⲩⲉ", "in secret / without our knowledge — the charge against a vision he asked to hear"),
            ("ⲥⲉⲧⲡ", "to prefer / choose — the wound; love restated as a slight to the men"),
        ),
        "res": res(
            ("Luke 24:10–11", "The women's report seemed an idle tale.", "Luke's disbelief is of the tomb; Peter's is of a woman preferred with hidden words."),
            ("Gospel of Thomas 114", "Simon Peter wants Mary excluded because women are not worthy of life.", "Thomas's Peter is exclusion first; this Peter is invitation, then exclusion. Same wound, later in the scene."),
        ),
    },
    {
        "n": 23,
        "title": "Did I think this up in my heart?",
        "section": "BG 8502, p. 18",
        "coptic": "ⲁⲥⲣⲓⲙⲉ ⲛϭⲓ ⲙⲁⲣⲓϩⲁⲙ ⲡⲉϫⲁⲥ ⲛⲡⲉⲧⲣⲟⲥ ϫⲉ ⲡⲁⲥⲟⲛ ⲡⲉⲧⲣⲟⲥ ⲉⲕⲙⲉⲉⲩⲉ ⲉⲟⲩ ⲉⲕⲙⲉⲉⲩⲉ ϫⲉ ⲛⲧⲁⲓⲙⲉⲉⲩⲉ ⲉⲣⲟⲟⲩ ⲙⲁⲩⲁⲁⲧ ϩⲙ ⲡⲁϩⲏⲧ ⲏ ϫⲉ ⲉⲓϫⲓϭⲟⲗ ⲉⲡⲥⲱⲧⲏⲣ",
        "tr": "Then Mary wept and said to Peter, My brother Peter, what are you thinking? Do you really think that I thought this up by myself in my heart, or that I am lying about the Savior?",
        "comm": "Mary's tears are not collapse. They are the soul's question to Wrath in human form: did I invent this, or am I lying? Brother is still her word for him. The gospel will not let you keep the ascent as private mysticism. It lands as a fight about who is allowed to have heard. If you skip this gate, Mary is a mascot. Here she is a witness under cross-examination, asking the examiner to name his thought. The misconception: that tears mean she has lost the unwavering mind. Unwavering was at the sight of the Lord. This is grief at being recoded as a liar.",
        "prac": "If you are recoded as inventor or liar for a true thing you reported, ask the recoder Peter's question back: what are you thinking? Do not add more content. Wait for the thought to be named.",
        "terms": kt(
            ("ϫⲓϭⲟⲗ", "to lie — Mary's question: invention or testimony?"),
            ("ϩⲏⲧ", "heart — accused of being the sole source; she had said the Savior spoke"),
            ("ⲥⲟⲛ", "brother — she keeps the kinship Peter is in the act of breaking"),
        ),
        "res": res(
            ("John 20:11–18", "Mary weeps at the tomb, then is sent to the brothers: I have seen the Lord.", "John's tears open the recognition; these tears answer a recognition already given and now refused."),
            ("Gospel of Mary, BG 8502 p. 10", "Blessed because you did not waver at the sight of me.", "Unwavering at the vision; weeping at the brothers. Two fidelities, not a contradiction."),
        ),
    },
    {
        "n": 24,
        "title": "Peter, you have always been angry",
        "section": "BG 8502, p. 18",
        "coptic": "ⲡⲉϫⲉ ⲗⲉⲩⲉⲓ ⲛⲡⲉⲧⲣⲟⲥ ϫⲉ ⲡⲉⲧⲣⲟⲥ ⲁⲕⲛⲟⲩϭⲥ ⲛⲟⲩⲟⲉⲓϣ ⲛⲓⲙ ⲧⲉⲛⲟⲩ ϯⲛⲁⲩ ⲉⲣⲟⲕ ⲉⲕϯⲧⲱⲛ ⲟⲩⲃⲉ ⲧⲉⲥϩⲓⲙⲉ ⲛⲑⲉ ⲛⲛⲓⲁⲛⲧⲓⲕⲉⲓⲙⲉⲛⲟⲥ",
        "tr": "Levi said to Peter, Peter, you have always been angry. Now I see you debating with this woman like the adversaries.",
        "comm": "Levi names the seventh form of Wrath in a man: always angry, now debating the woman like the adversaries — the antimimenoi, the opposing powers the soul just climbed. Peter has become the checkpoint. The debate is not a search for truth. It is Wrath's wisdom wearing a brother's face. Levi does not yet argue worth. He diagnoses. The misconception: that a long-standing temper is just 'how Peter is,' and therefore not a spiritual event. The book says the adversaries have found a seat in the circle.",
        "prac": "Where you are always angry in one relationship, say Levi's sentence to yourself: I am debating like the adversaries. Stop the debate for one hour. Do not settle the theology in that hour.",
        "terms": kt(
            ("ⲛⲟⲩϭⲥ", "to be angry — Levi's 'always'; Wrath as a character-trait in the group"),
            ("ϯⲧⲱⲛ", "to debate / contend — the form anger takes against 'this woman'"),
            ("ⲁⲛⲧⲓⲕⲉⲓⲙⲉⲛⲟⲥ", "adversaries / opposing powers — the soul's enemies; now a way of talking in the room"),
        ),
        "res": res(
            ("Gospel of Mary, BG 8502 p. 16", "The seventh form of Wrath is the Wisdom of Anger.", "The ascent's last face of Wrath sits down in Peter. Levi is the one who sees it."),
            ("Matthew 16:22–23", "Peter rebukes Jesus; Get behind me, Satan — you are not thinking the things of God.", "Matthew's Peter is adversary for a moment of the passion; Mary's Peter is adversary toward the witness of the ascent."),
        ),
    },
    {
        "n": 25,
        "title": "If the Savior made her worthy, who are you to reject her?",
        "section": "BG 8502, p. 18",
        "coptic": "ⲉϣϫⲉ ⲁ ⲡⲥⲱⲧⲏⲣ ⲁⲁⲥ ⲛⲁⲝⲓⲟⲥ ⲛⲧⲕ ⲛⲓⲙ ⲇⲉ ϩⲱⲱⲕ ⲉⲛⲟϫⲥ ⲉⲃⲟⲗ ⲡⲁⲛⲧⲱⲥ ⲉϥⲥⲟⲟⲩⲛ ⲙⲙⲟⲥ ⲛⲁⲧⲁⲕⲣⲓⲃⲉⲥ ⲉⲧⲃⲉ ⲡⲁⲓ ⲁϥⲙⲉ ⲙⲙⲟⲥ ⲛϩⲟⲩⲟ ⲉⲣⲟⲛ",
        "tr": "If the Savior made her worthy, who are you then to reject her? Surely the Savior knows her very well. That is why he loved her more than us.",
        "comm": "Worth is the Savior's to confer, not Peter's to revoke. Love-more-than-us is restated without Peter's 'than the rest of the women.' The ranking Peter used as a cage becomes, in Levi's mouth, a fact about knowledge: he knows her accurately, therefore he loved her more. Who are you is the question the powers asked the soul, now asked of the gatekeeper. The misconception: that the circle confers and withdraws worthiness to hear. The book locates worth in the one who made her worthy.",
        "prac": "Where you are the gatekeeper of who may have heard, step aside once. Ask Levi's question of yourself: if they were made worthy, who am I to reject them? Do the next ordinary act without the extra rule.",
        "terms": kt(
            ("ⲁⲝⲓⲟⲥ", "worthy — conferred by the Savior, not by the circle"),
            ("ⲛⲟϫ ⲉⲃⲟⲗ", "to reject / cast out — Peter's move; Levi forbids it"),
            ("ⲥⲟⲟⲩⲛ ⲛⲁⲧⲁⲕⲣⲓⲃⲉⲥ", "knows her accurately — the ground of the love, not a slight to the men"),
        ),
        "res": res(
            ("Gospel of Thomas 114", "Peter wants Mary out; Jesus answers by changing her.", "Thomas keeps Jesus as the solver; Mary lets a disciple rebuke Peter."),
            ("Luke 7:47", "The one who is forgiven more loves more.", "Luke ties love to forgiveness; Levi ties love to accurate knowing by the Savior."),
        ),
    },
    {
        "n": 26,
        "title": "Clothe yourselves with perfect Humanity",
        "section": "BG 8502, pp. 18–19",
        "coptic": "ⲙⲁⲗⲗⲟⲛ ⲙⲁⲣⲛϣⲓⲡⲉ ⲛⲧⲛϯ ϩⲓⲱⲱⲛ ⲙⲡⲧⲉⲗⲓⲟⲥ ⲛⲣⲱⲙⲉ ⲛⲧⲛϫⲡⲟϥ ⲛⲁⲛ ⲕⲁⲧⲁ ⲑⲉ ⲛⲧⲁϥϩⲱⲛ ⲉⲧⲟⲟⲧⲛ ⲛⲧⲛⲧⲁϣⲉⲟⲉⲓϣ ⲙⲡⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ ⲉⲛⲕⲱ ⲁⲛ ⲛⲕⲉϩⲟⲣⲟⲥ ⲟⲩⲇⲉ ⲕⲉⲛⲟⲙⲟⲥ ⲡⲁⲣⲁ ⲡⲉⲛⲧⲁ ⲡⲥⲱⲧⲏⲣ ϫⲟⲟϥ ⲛⲧⲉⲣⲉ ⲗⲉⲩⲉⲓ ϫⲉ ⲛⲁⲓ ⲁⲩⲁⲣⲭⲉⲓ ⲛⲃⲱⲕ ⲉⲃⲟⲗ ⲉⲧⲥⲃⲟ ⲁⲩⲱ ⲉⲧⲁϣⲉⲟⲉⲓϣ",
        "tr": "Rather we should be ashamed, clothe ourselves with perfect Humanity, acquire it as he instructed us, and preach the gospel, not laying down any other rule or other law beyond what the Savior said. When Levi said these things, they started to go out to teach and to preach.",
        "comm": "Levi returns the farewell. Shame is for the anger, not for Mary. Then the clothing: perfect Humanity — the stature Mary already named when she stood. Preach, and do not add a rule. The book ends not with a vision but with a group that can walk out because someone defended the witness. Acquire it: Humanity is not a feeling that arrived in the argument. It is put on, as he said. The last practice of the gospel is Levi's: be ashamed of the anger, put on the Human, go.",
        "prac": "Clothe yourself as Human — one ordinary act of going out (a message, a repair, a walk) without the extra rule about who is allowed. Do not wait to feel worthy. Put it on.",
        "terms": kt(
            ("ⲧⲉⲗⲓⲟⲥ ⲛⲣⲱⲙⲉ", "perfect Humanity — the clothing Levi commands; Mary's earlier 'he made us Human'"),
            ("ϣⲓⲡⲉ", "shame — directed at the anger, not at the witness"),
            ("ϩⲟⲣⲟⲥ", "rule / limit — the extra statute the farewell already forbade, now forbidden again as they go"),
        ),
        "res": res(
            ("Gospel of Mary, BG 8502 p. 9", "Do not lay down any rule beyond what I have given you.", "The farewell is restated as the condition of going out. Levi is the one who remembers it."),
            ("Colossians 3:9–10", "Strip the old human, put on the new, who is being renewed after the image.", "Paul's clothing is the new human in an image; Mary's is perfect Humanity as the Savior's instruction, without an extra law."),
        ),
    },
]


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.gom_{n:02d}"
    layers = [
        {"kind": "original", "label": "Original", "body": u["coptic"]},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"GOM_{n:02d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": u["section"],
        "title": u["title"],
        "unit_type": "teaching_passage",
        "commentary": u["comm"],
        "themes": ["vision", "ascent", "mary magdalene", "worthiness"],
        "tags": [SLUG, "christian", "gnostic", "sayings"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "section": u["section"],
            "cultural_context": NOTE,
            "original_source": "Sahidic Coptic, Papyrus Berolinensis 8502,1 (5th c.)",
            "original_reliability": "SOURCED — working transcription of BG 8502 wording; lacunae marked; not Till 1955 apparatus",
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": u["coptic"],
        "sanskrit_devanagari": u["coptic"],
        "sanskrit_iast": "Sahidic Coptic (see Original layer).",
    }
    if n in HEROES:
        unit["tts_key"] = True
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{uid.replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return uid


def build() -> int:
    keep = {write_unit(u) for u in UNITS}
    removed = 0
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if not name.endswith(".yml"):
                continue
            uid = name[: -len(".yml")].replace("_", ".", 1)
            # files are gospel_of_mary_gom_01.yml → gospel_of_mary.gom_01
            stem = name[: -len(".yml")]
            parts = stem.split("_gom_")
            reconstructed = f"{parts[0]}.gom_{parts[1]}" if len(parts) == 2 else ""
            if reconstructed and reconstructed not in keep:
                os.remove(os.path.join(OUT, name))
                removed += 1
    print(f"Wrote {len(keep)} units to {OUT}" + (f" (removed {removed} stale)" if removed else ""))
    print(f"Heroes: {sorted(HEROES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
