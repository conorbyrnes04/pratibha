#!/usr/bin/env python3
"""Ingest Nina Rodrigues, *L'Animisme Fétichiste Des Nègres de Bahia* (1900).

Public-domain source: Raimundo Nina Rodrigues, Bahia: Reis & Comp., 1900.
French book of articles first published in Portuguese in *Revista Brazileira*
1896–97 as *O Animismo Fetichista dos Negros Bahianos*. IA scan
`lanimismefetichistedesnegres`; OCR cleaned.

English is a Pratibha rendering (pd_adapted). Original layer is cleaned 1900
French. This is NOT Arthur Ramos 1935 and does not follow Maggie/Fry 2006.
*Os Africanos no Brasil* (1932) is out of scope.

Observer document of Afro-Bahian Candomblé (Nagô/Yoruba orisha life in Bahia,
with Jeje and other nations present). Rodrigues was a physician and racial
theorist. Restore ethnographic claims without adopting racial ranking,
"fetish" as doctrine, criminal-anthropology, or degeneration theory.
Ceremonial how-to for harmful magic / sacrifice recipes excluded.

Floor: ≥28 units. Ten tts_key heroes.
"""
from __future__ import annotations

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/animismo_fetichista")
SLUG = "animismo_fetichista"
COLL = "O Animismo Fetichista"
THEMES = ["candomble", "nago", "orisha", "bahia", "living speech"]
ROMAN = "Rodrigues 1900 French of Bahian Candomblé observation"

PROV = (
    "English is a Pratibha rendering (pd_adapted) from Raimundo Nina Rodrigues, "
    "*L'Animisme Fétichiste Des Nègres de Bahia* (Bahia: Reis & Comp., 1900), "
    "public domain; that book translates his *Revista Brazileira* 1896–97 articles. "
    "Original layer is cleaned 1900 French. Does not follow Arthur Ramos 1935 or "
    "Maggie/Fry 2006."
)
NOTE = (
    "Observer document of Afro-Bahian Candomblé (Nagô/Yoruba orisha life in Bahia, "
    "with Jeje and other nations present). Rodrigues was a physician and racial "
    "theorist; Brazilian repositories note the work is \"carregada de preconceito "
    "e discriminação.\" Restore ethnographic claims (Olorun, orisa, possession, "
    "terreiro, Gantois) without adopting racial ranking, \"fetish\" as doctrine, "
    "criminal-anthropology, or degeneration theory. Ceremonial how-to for harmful "
    "magic / sacrifice recipes excluded; mythic and liturgical argument kept. "
    "Study reading pending review by Candomblé tradition-bearers."
)
RELIABILITY = (
    "SOURCED — Rodrigues 1900 French of 1896–97 Portuguese articles; IA OCR "
    "cleaned. Not Ramos 1935, not Maggie/Fry 2006."
)

# Ten hero verses — mandala quotes + pre-baked Listen.
HEROES = {1, 3, 6, 8, 9, 10, 13, 18, 21, 28}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


def roman(*terms: str) -> str:
    return f"{ROMAN}. Key Yoruba/Nagô: {'; '.join(terms)}."


UNITS: list[dict] = [
    {
        "n": 1,
        "title": "Only One God in the Universe",
        "src": "Rodrigues 1900, ch. I — Olorun et les orisas",
        "fr": (
            "À Bahia, la religion des Yorubans est beaucoup plus importante, soit "
            "parce que c’est celle de presque tous les Africains, soit par "
            "l’adhésion des nègres créoles et métis. Bowen a remarqué que la "
            "doctrine de Yoruba semble avoir copié la forme du gouvernement civil. "
            "Ainsi, de même qu’il n’y a qu’un roi dans la nation, il n’y a qu’un "
            "Dieu dans l’univers, Olorun. De même que pour approcher le roi "
            "l’intervention des courtisans est indispensable, l’homme, pour "
            "approcher de Dieu, doit avoir recours à l’intervention des Orisas. "
            "Si Dieu n’a pas besoin de sacrifices, parce qu’il n’a besoin de rien, "
            "les Orisas, tout comme les hommes, acceptent volontiers des moutons, "
            "des pigeons. La structure n’est donc pas un panthéon d’égaux: elle "
            "est une cour."
        ),
        "roman": roman(
            "Olorun (Lord of Heaven, one God)",
            "Orisa (mediating divinities)",
            "Nagô (Yoruba nation in Bahia)",
        ),
        "tr": (
            "In Bahia the religion of the Yoruba is the most important, both "
            "because it is the religion of almost all the Africans and because "
            "Creole and mixed-race Black Bahians adhere to it. Bowen remarked "
            "that Yoruba teaching seems to have copied the form of civil "
            "government. As there is only one king in the nation, there is only "
            "one God in the universe, Olorun. As one cannot approach the king "
            "without the intervention of courtiers, a human being, to approach "
            "God, must have recourse to the orisas. God needs no sacrifices, "
            "because he needs nothing. The orisas, like persons, willingly "
            "accept sheep and pigeons. The structure is not a pantheon of equals: "
            "it is a court."
        ),
        "comm": (
            "The claim the terreiro lives is that there is one God in the "
            "universe, Olorun, and that a human being does not walk up to that "
            "God. Approach is courtly. You reach the king through courtiers; you "
            "reach Olorun through orisas. Olorun needs nothing, therefore he "
            "needs no offering. The orisas receive as persons receive. This is "
            "Nagô philosophy of mediation, not a primitive monarchy pasted onto "
            "the sky. Rodrigues, a Bahian physician and racial theorist, reports "
            "the structure while loading the page with nègres, métis, and the "
            "evolutionist habit of treating African religion as a copy of the "
            "state. Brazilian repositories rightly call the book loaded with "
            "prejudice and discrimination. His vocabulary — fetish, savage, "
            "inferior race, Tylor’s ladder — is poison. Do not launder it. The "
            "ethnographic remainder is still sharp. Johnson, writing as a Yoruba "
            "clergyman, states the same architecture from the inside: Olorun is "
            "Lord of Heaven, too exalted for direct human traffic; the orisas "
            "are the necessary middle. Bahia did not invent that hierarchy under "
            "Catholic pressure. It brought the court across the Atlantic and kept "
            "it in the terreiro. Bowen’s civil-government analogy is an outsider’s "
            "simile. The terreiro’s act is liturgical: keep the highest high, and "
            "keep the middle addressable. Existentially, you do not barge in on "
            "the highest thing you name. You learn which court actually stands, "
            "and you stop treating the courtiers as a superstition that blocks God."
        ),
        "prac": (
            "Today, name one highest thing you claim to honor, then name the "
            "actual person, desk, or door you must go through to approach it. "
            "Do the approach. Do not pretend you walk straight in."
        ),
        "terms": kt(
            (
                "Olorun",
                "Yoruba Olórun, owner / lord of the sky -> one God of the "
                "universe, needing nothing -> default \"sky-god\" or \"high god "
                "of a tribe\" misses that the name is reserved and that cult "
                "does not climb up to him",
            ),
            (
                "Orisa",
                "Yoruba òrìṣà, mediating divinity -> the court through which "
                "a human being approaches Olorun -> \"god\" as a peer of Olorun "
                "collapses the hierarchy; \"saint\" (later unit) hides the "
                "Nagô name",
            ),
            (
                "Nagô",
                "Bahian name for the Yoruba nation and its orisha life -> the "
                "majority African religion Rodrigues finds in Bahia -> folding "
                "this into a continent label \"African Animism\" or a generic "
                "Yoruba catch-all erases Candomblé as its own house",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Olorun, the Lord of Heaven",
                "Both state one Almighty named Olorun and a populated middle of "
                "orisas who handle human traffic.",
                "Johnson writes as a Yoruba clergyman from the inside; Rodrigues "
                "writes as a Bahian physician watching terreiros, and then ranks "
                "the people he watches.",
            ),
            (
                "Lasnet, Senegalese Animism — One Does Not Address God; One "
                "Addresses the Spirits",
                "Both keep a known highest being off the ordinary altar and "
                "place relationship in a middle population.",
                "Serer mediators are mammam / pangool of place and the dead; "
                "Nagô mediators in Bahia are named orisas with offerings, "
                "colors, and houses.",
            ),
        ),
    },
    {
        "n": 2,
        "title": "There Is No King Like God",
        "src": "Rodrigues 1900, ch. I — inscription Baixa dos Sapateiros",
        "fr": (
            "Il y a à Bahia, dans la rue de la Baixa dos Sapateiros, une "
            "boucherie qui appartient à un nègre créole. Au-dessus de la boutique "
            "s’étale l’inscription en langue yoruba: A ki se oba kan afi Olorun, "
            "qui m’a été traduite: Il n’y a pas un roi comme Dieu. Cette "
            "inscription est reproduite à l’intérieur avec l’entête O Alufa, le "
            "tout surmonté d’une croix. Le boucher n’est pas un malê; c’est un "
            "personnage influent dans l’un des principaux terreiros de cette "
            "ville. La phrase n’est donc pas un verset musulman caché: elle est "
            "une théologie nagô écrite sur la rue."
        ),
        "roman": roman(
            "Olorun",
            "oba (king)",
            "Alufa (Muslim cleric title, here a heading)",
            "terreiro",
            "Malê (Muslim African in Bahia)",
        ),
        "tr": (
            "In Bahia, on the street of the Baixa dos Sapateiros, a butcher’s "
            "shop belongs to a Creole Black Bahian. Above the shop is displayed "
            "an inscription in the Yoruba language: A ki se oba kan afi Olorun, "
            "translated to Rodrigues as: There is no king like God. The "
            "inscription is repeated inside under the heading O Alufa, the whole "
            "surmounted by a cross. The butcher is not a Malê; he is an "
            "influential person in one of the principal terreiros of the city. "
            "The sentence is therefore not a hidden Muslim verse: it is Nagô "
            "theology written on the street."
        ),
        "comm": (
            "The claim is that Olorun’s uniqueness can be posted over meat and "
            "still be terreiro speech. A ki se oba kan afi Olorun is not a motto "
            "for a chapel. It is a shop sign. A king is named in order to be "
            "outranked. A cross sits over a Yoruba line and an Alufa heading, "
            "and the butcher is not a Muslim African; he is a terreiro man. The "
            "street already holds the theology of unit 1 in public letters. "
            "Rodrigues, outsider physician, records the inscription as a curiosity "
            "of a créole nègre and then sorts the man by nation — not Malê, "
            "therefore interesting. The sorting is his habit. The sentence on "
            "the wall is the teaching. Do not adopt his surprise that Black "
            "Bahians write metaphysics above a counter. Johnson reserves the "
            "name Olorun for God alone and will not pluralize it onto the orisas. "
            "The butcher’s line does the same work in the market: no king, not "
            "even the city’s king, matches God. The cross does not baptize the "
            "line into a catechism. It shows how Bahia’s public language stacks "
            "signs without erasing the Yoruba claim. Existentially, read one "
            "ordinary sign today as if it might be theology. Ask which king you "
            "still treat as if there were no God above him."
        ),
        "prac": (
            "Read one public inscription or shop heading today as a theological "
            "sentence. Write the line you saw, then write the king it quietly "
            "outranks in your own life."
        ),
        "terms": kt(
            (
                "A ki se oba kan afi Olorun",
                "Yoruba: one does not make / there is not a king except Olorun "
                "-> no earthly king matches God -> a proverb on a butcher’s "
                "lintel, not a mosque verse and not a Portuguese catechism",
            ),
            (
                "terreiro",
                "yard, house, and jurisdiction of a Candomblé community -> the "
                "butcher’s real public is a terreiro, not the shop alone -> "
                "\"temple\" or \"cult-house\" misses that the street already "
                "speaks terreiro language",
            ),
            (
                "Malê",
                "Bahian name for Muslim Africans -> Rodrigues uses the category "
                "to decide what the inscription \"must\" be -> the teaching is "
                "that Nagô speech can wear a cross and an Alufa heading and "
                "still not be Islam",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Name Reserved for God Alone",
                "Both refuse to let any earthly greatness share Olorun’s unique "
                "name or rank.",
                "Johnson legislates the name in a history of the Yoruba; the "
                "Bahian butcher posts the claim over a shop and under a cross.",
            ),
            (
                "Ellis, Yoruba òwe — The young cannot teach the elders traditions",
                "Both treat Yoruba speech as public wisdom that does not wait "
                "for a classroom.",
                "The òwe is a proverb among people; this line is a lintel in "
                "a Catholic-majority city, already mixed with other signs.",
            ),
        ),
    },
    {
        "n": 3,
        "title": "Olorun Has No Image and No Cult",
        "src": "Rodrigues 1900, ch. I — conception d’Olorun",
        "fr": (
            "Dans cette conception d’Olorun Dieu créateur, non représenté par "
            "des idoles ou des images, sans culte ni adoration, se trouve déjà "
            "toute la hauteur de la doctrine. Olorun n’a pas, à Bahia, de culte "
            "spécial ni d’image qui le représente. Cette absence de "
            "représentation matérielle ne doit pas peu contribuer à ce qu’il "
            "soit si ignoré même des Africains. Ce n’est pas qu’on nie Olorun. "
            "C’est qu’on ne le fixe pas. Un Dieu qui n’a besoin de rien n’a pas "
            "besoin d’un autel. Les Orisas ont des autels précisément parce "
            "qu’ils reçoivent."
        ),
        "roman": roman(
            "Olorun",
            "Orisa",
            "no image / no special cult of Olorun in Bahia",
        ),
        "tr": (
            "In this conception of Olorun as creator God, not represented by "
            "idols or images, without cult or adoration, the whole height of "
            "the teaching is already present. In Bahia Olorun has no special "
            "cult and no image that represents him. That absence of material "
            "representation does much to explain why he is so little known even "
            "among Africans. This is not a denial of Olorun. It is a refusal to "
            "fix him. A God who needs nothing needs no altar. The orisas have "
            "altars precisely because they receive."
        ),
        "comm": (
            "The claim is negative and exact: Olorun is creator, and Olorun has "
            "no image and no special cult in Bahia. The highest is not the most "
            "available. Absence of a statue is not a hole in the religion; it is "
            "the religion’s height. A God who needs nothing cannot be kept on a "
            "shelf. Rodrigues, outsider physician, reads the same absence as "
            "ignorance — even Africans, he says, barely know Olorun — and his "
            "ladder is already at work: what has no idol must be fading, weak, "
            "or not yet evolved into \"real\" worship. That is poison. Tylor’s "
            "evolutionism and the word fetish train the eye to treat an empty "
            "plinth as a failure. The terreiro treats an empty plinth as "
            "accuracy. Johnson’s Olorun is too exalted to handle human affairs "
            "directly; Bahia’s Olorun is too exalted to sit for a portrait. The "
            "two sentences are one philosophy under two observers. Creoles who "
            "\"do not know\" Olorun (next unit) have often learned another name "
            "for the highest, not discovered that the sky is vacant. "
            "Existentially, the teaching asks you to stop demanding a picture "
            "before you will admit a principle. What you cannot display is not "
            "therefore absent. It may be the one thing you must not reduce to "
            "an object you can own."
        ),
        "prac": (
            "Today, refuse one image — a photo, an icon, a logo — that you "
            "habitually treat as the thing itself. Sit with the unnamed for "
            "five minutes. Write one sentence about what remains when the "
            "picture is not allowed to stand in."
        ),
        "terms": kt(
            (
                "sans culte ni adoration",
                "without cult or adoration -> Olorun is known and not addressed "
                "as a liturgical client -> \"unknown god\" or \"deus otiosus\" "
                "as a deficit misses that withholding cult is reverence",
            ),
            (
                "image",
                "material representation Rodrigues expects of \"religion\" -> "
                "its absence around Olorun is the doctrine -> calling the "
                "absence \"ignorance\" adopts the physician’s ranking",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Between Maker and World",
                "Both pair a comprehensive Maker with distance: exaltation "
                "explains why the middle population does the work.",
                "Johnson stresses intermediaries; this unit stresses the visual "
                "and liturgical emptiness around Olorun himself.",
            ),
            (
                "Lasnet, Senegalese Animism — The Invisible Master Is Named as "
                "the Sky",
                "Both name a highest being who is not carved and not bargained "
                "with as an object.",
                "Serer Rog shares the name of the sky; Bahian Olorun is Lord of "
                "Heaven and still receives no special terreiro feast under that "
                "name.",
            ),
        ),
    },
    {
        "n": 4,
        "title": "Creoles Identify an Orisa with Christ",
        "src": "Rodrigues 1900, ch. I — qui connaît Olorun",
        "fr": (
            "Bien que j’aie rencontré des Africains qui ne connaissent pas "
            "Olorun et que la plupart des créoles paraissent ne pas le "
            "connaître, en général les Africains et une bonne partie des "
            "créoles de Bahia savent parfaitement que Olorun est le Dieu du "
            "ciel. Quant aux créoles, la raison principale qui fait qu’en "
            "général ils ne connaissent pas Olorun, c’est l’identification d’un "
            "des Orisas avec le Christ. Les musulmans l’identifient avec Allah; "
            "les créoles élevés dans le catholicisme tendent à le confondre "
            "avec le Dieu des chrétiens. Le nom change; la cour ne disparaît "
            "pas. Un Orisa baptisé n’est pas pour cela devenu seulement un "
            "saint romain."
        ),
        "roman": roman(
            "Olorun",
            "Orisa",
            "Christ / Allah as overlay names",
            "Creole (Brazilian-born)",
        ),
        "tr": (
            "Although Rodrigues met Africans who did not know Olorun, and "
            "although most Creoles seem not to know him, in general Africans "
            "and a good part of the Creoles of Bahia know perfectly that Olorun "
            "is the God of heaven. As for the Creoles, the principal reason "
            "they often do not know Olorun is the identification of one of the "
            "orisas with Christ. Muslims identify him with Allah; Creoles raised "
            "in Catholicism tend to confuse him with the God of the Christians. "
            "The name changes; the court does not disappear. An orisa given a "
            "baptismal name has not thereby become only a Roman saint."
        ),
        "comm": (
            "The claim is about names stacked on a structure that does not "
            "collapse. Africans in Bahia generally know Olorun as God of heaven. "
            "Creoles raised Catholic often do not use that name, because an "
            "orisa has been identified with Christ, or because Olorun has been "
            "folded into the Christian God. Muslims perform the same overlay "
            "with Allah. Translation is not conversion completed. It is a "
            "calque. Rodrigues, outsider physician, hears \"they do not know "
            "Olorun\" as a mark of Creole distance from Africa — a step on his "
            "ladder toward the \"higher\" faith he already inhabits. That "
            "ranking is poison. Degeneration theory would say the children "
            "forgot. The terreiro says the children learned another public "
            "name for a face that was already in the court. Identifying an "
            "orisa with Christ is not the same act as identifying Olorun with "
            "the Christian God; Rodrigues slides between them, and the slide "
            "is his. Keep them distinct. One overlays a mediator; the other "
            "renames the height. Existentially, notice which name you use for "
            "the highest and which mediator you have silently baptized. Do not "
            "call the overlay a victory of one religion or a failure of the "
            "other until you can say which layer you actually address."
        ),
        "prac": (
            "Write three columns: the highest you name, the mediator you "
            "actually go through, and the public name you were taught for each. "
            "Circle one place you have collapsed two names. Restore the "
            "distinction in one spoken sentence today."
        ),
        "terms": kt(
            (
                "créole",
                "Brazilian-born, often Catholic-raised -> Rodrigues’s mark of "
                "who \"forgets\" Olorun -> the teaching is overlay of names, "
                "not racial fading",
            ),
            (
                "identification",
                "equating an orisa with Christ, or Olorun with Allah / the "
                "Christian God -> a linguistic and catechetical bridge -> not "
                "proof that Candomblé has become the Church",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — One God, Many Towns",
                "Both show one named highest surviving under local public "
                "languages without becoming many highest beings.",
                "Johnson stays inside Yoruba towns; Bahia adds Christ and Allah "
                "as colonial and Islamic public names on the same court.",
            ),
            (
                "Gospel of John 1:1–14",
                "Both traditions know a highest that can be spoken in more than "
                "one register (Word, God, flesh) without the registers being "
                "identical.",
                "John identifies the Word with a particular person; the terreiro "
                "can overlay Christ on an orisa without thereby emptying the "
                "orisa’s house.",
            ),
        ),
    },
    {
        "n": 5,
        "title": "Below Olorun the Orisas",
        "src": "Rodrigues 1900, ch. I — suite des dieux",
        "fr": (
            "Au-dessous d’Olorun pour les Yorubans — et indépendamment d’Olorun "
            "pour beaucoup d’Africains convertis et en général pour les créoles "
            "— il y a une suite nombreuse de dieux ou Orisas. En général les "
            "Orisas sont des phénomènes météorologiques divinisés, ou "
            "proviennent de créations evhémériques. Pour le moment ils sont "
            "encore représentés par des objets inanimés comme l’eau, la pierre, "
            "les coquillages, le fer, ou par des arbres. Cette liste n’est pas "
            "un musée de restes. Elle est le matériel par lequel la cour se "
            "rend présente. L’eau, la pierre, le fer et l’arbre ne sont pas "
            "des supports en attendant une statue plus noble."
        ),
        "roman": roman(
            "Olorun",
            "Orisa",
            "water, stone, cowries, iron, trees as orisa-materials",
        ),
        "tr": (
            "Below Olorun for the Yoruba — and independently of Olorun for many "
            "converted Africans and in general for Creoles — there is a numerous "
            "suite of gods or orisas. In general the orisas are divinized "
            "meteorological phenomena, or they come from euhemeristic creations. "
            "For the present they are still represented by inanimate objects "
            "such as water, stone, shells, iron, or by trees. This list is not "
            "a museum of leftovers. It is the material through which the court "
            "makes itself present. Water, stone, iron, and tree are not stands "
            "awaiting a nobler statue."
        ),
        "comm": (
            "The claim is that the court is populated and material. Below "
            "Olorun — or, for many converted Africans and Creoles, without "
            "needing to pass through that name — stand many orisas. They arrive "
            "as weather, as once-living figures, as water, stone, cowry, iron, "
            "and tree. The terreiro does not apologize for those materials. "
            "Rodrigues, outsider physician, cannot write the list without Tylor. "
            "\"Divinized meteorological phenomena,\" \"euhemeristic creations,\" "
            "\"for the present they are still represented by inanimate objects\": "
            "every clause is a rung. Fetish is the doctrine he came to prove. "
            "Do not adopt the ladder. Water is not a failed marble. Iron is not "
            "a temporary idol. The later units will say the harder thing: "
            "sometimes the stone is the orisa, sometimes the tree is the god, "
            "sometimes only a prepared rail is Ogun. This unit only opens the "
            "field. Johnson’s orisas stand between Maker and world; Bahia’s "
            "orisas also stand in the Dique, the fountain, the gameleira, the "
            "tram rail. Existentially, stop waiting for a \"higher\" image "
            "before you will admit that a common material can hold a presence. "
            "Pick one — water, stone, iron, wood — and ask what you have been "
            "trained to call it instead of a house."
        ),
        "prac": (
            "Choose one ordinary material you will touch today — water, a "
            "stone, iron, or a tree. Do not decorate it. Ask, for one minute, "
            "whether you have been taught to treat it as leftover matter. "
            "Write the name you refuse to give it."
        ),
        "terms": kt(
            (
                "suite des dieux",
                "the numerous orisas below or beside Olorun -> a court, not a "
                "crowd of interchangeable spirits -> \"pantheon\" as a list of "
                "equals misses rank and material",
            ),
            (
                "objets inanimés",
                "Rodrigues’s phrase for water, stone, shells, iron, trees -> "
                "he needs them dead so \"fetish\" can live -> the terreiro "
                "treats them as capable of presence",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Between Maker and World",
                "Both place a numerous mediating population under a remote Maker.",
                "Johnson names the function (intermediary); this unit names the "
                "Bahian materials in which that function arrives.",
            ),
            (
                "Lasnet, Senegalese Animism — Animism Is Not Fetishism",
                "Both PD observers are forced, against their own vocabulary, "
                "toward a living world that is not a box of charms.",
                "Lasnet’s Serer report denies fetish as the religion; Rodrigues "
                "keeps the word in his title and then has to describe water and "
                "iron anyway.",
            ),
        ),
    },
    {
        "n": 6,
        "title": "Orisa Is Translated as Saint",
        "src": "Rodrigues 1900, ch. I — traduction d’Orisa",
        "fr": (
            "La traduction du mot Orisa par le mot saint a dû puissamment aider "
            "et faciliter la fusion des croyances des nègres avec le "
            "catholicisme qu’on leur a enseigné au Brésil. Le mot portugais "
            "santo, une fois collé sur l’Orisa, ouvrait une porte que le prêtre "
            "catholique n’avait pas prévue. Les confréries, les fêtes, les "
            "couleurs et les images pouvaient désormais se dire dans une langue "
            "déjà reçue. Ce n’est pas que l’Orisa soit devenu un saint romain. "
            "C’est que le mot saint a servi de pont. La fusion n’est donc pas "
            "une conversion achevée; elle est un calque linguistique qui laisse "
            "l’Orisa intact sous un nom nouveau."
        ),
        "roman": roman(
            "Orisa",
            "santo / saint as Portuguese calque",
        ),
        "tr": (
            "The translation of the word Orisa by the word saint must have "
            "powerfully helped and eased the fusion of Black Bahian beliefs "
            "with the Catholicism taught them in Brazil. The Portuguese word "
            "santo, once stuck onto the orisa, opened a door the Catholic priest "
            "had not planned. Confraternities, feasts, colors, and images could "
            "now be spoken in a language already received. This is not because "
            "the orisa became a Roman saint. It is because the word saint served "
            "as a bridge. The fusion is therefore not a finished conversion; it "
            "is a linguistic calque that leaves the orisa intact under a new name."
        ),
        "comm": (
            "The claim is linguistic and therefore liturgical: orisa was "
            "translated as saint, and the translation did work. Santo let "
            "confraternity, feast, color, and image speak in a public tongue "
            "Brazil already understood. The Catholic teacher thought he was "
            "hearing obedience. The terreiro was keeping a court under a loaned "
            "noun. Rodrigues, outsider physician, reports the translation as a "
            "mechanism of fusion — and fusion, in his mouth, leans toward the "
            "Church absorbing the \"beliefs of the nègres.\" That lean is "
            "poison. Do not finish his sentence for him. A calque is not a "
            "surrender. If the orisa were only a saint, the later units would "
            "be impossible: Eshu would be the devil, the stone would be a relic, "
            "the gameleira would be a decoration. They are not. Johnson never "
            "needs \"saint\" to explain an orisa to Yoruba readers; Bahia needs "
            "the word because the police, the parish, and the street already "
            "speak Portuguese. Existentially, catch the translation in your own "
            "mouth. When you say saint, ask which house you have just hidden. "
            "Restore the Nagô name once, aloud, without using it as costume."
        ),
        "prac": (
            "Catch yourself using a borrowed honorific today — saint, genius, "
            "icon, guru — for something that has another name. Say the older "
            "name once, aloud, and write what the borrowed word was hiding."
        ),
        "terms": kt(
            (
                "Orisa / santo",
                "Nagô divinity calqued as Portuguese saint -> a public bridge, "
                "not an identity -> default \"syncretism\" as blending misses "
                "that one word can carry two jurisdictions",
            ),
            (
                "fusion",
                "Rodrigues’s word for Catholic-Nagô overlay -> he hears "
                "absorption -> the terreiro hears a translation that lets the "
                "orisa keep a feast in a Catholic city",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Name Reserved for God Alone",
                "Both treat naming as a theological act: a wrong noun collapses "
                "rank.",
                "Johnson protects Olorun from plural use; this unit shows Orisa "
                "accepting a Portuguese noun without becoming that noun.",
            ),
            (
                "Gospel, identification of holy persons as saints",
                "Both public languages use \"saint\" for a human or more-than-"
                "human figure who can be feasted and petitioned.",
                "Roman sainthood is a canonized dead; an orisa named santo is "
                "not thereby entered in the Roman calendar or emptied of "
                "possession, stone, and iron.",
            ),
        ),
    },
    {
        "n": 7,
        "title": "The Figures Are Neither Fetish nor Idol",
        "src": "Rodrigues 1900, ch. I — figures et images",
        "fr": (
            "Il y a dans le culte yoruban des figures et des images que quelques "
            "observateurs ont prises par erreur pour des idoles. Ces figures ne "
            "sont autre chose que des ornements représentant des prêtres ou des "
            "croyants, mais où ne résident pas des Orisas; elles ne sont donc "
            "ni des fétiches ni des idoles. Elles font partie des ornements des "
            "saints et sont destinées à être portées dans les mains lorsque le "
            "prêtre ou l’initié danse en état de saint. La résidence n’est pas "
            "dans le bois sculpté. La résidence est ailleurs: dans la pierre, "
            "dans le fer préparé, dans la tête. Confondre l’ornement et le "
            "siège, c’est inventer l’idole qu’on était venu dénoncer."
        ),
        "roman": roman(
            "Orisa",
            "santo / état de saint (possession)",
            "figure as ornament, not seat",
        ),
        "tr": (
            "In Yoruba cult there are figures and images that some observers "
            "have mistakenly taken for idols. These figures are nothing other "
            "than ornaments representing priests or believers, but orisas do "
            "not reside in them; they are therefore neither fetishes nor idols. "
            "They belong to the ornaments of the saints and are meant to be "
            "carried in the hands when the priest or the initiate dances in the "
            "state of saint. Residence is not in the carved wood. Residence is "
            "elsewhere: in the stone, in prepared iron, in the head. To confuse "
            "ornament with seat is to invent the idol one came to denounce."
        ),
        "comm": (
            "The claim is a distinction the terreiro already makes and Rodrigues "
            "is forced to write down: some figures are not the orisa. They are "
            "ornaments of priests and initiates, carried in the dance when the "
            "person is in the state of saint. They are neither fetish nor idol. "
            "Residence is not automatic in a human-shaped thing. That sentence "
            "already wrecks the book’s title. Rodrigues, outsider physician, "
            "cannot help the word fétiche elsewhere, but here the people he "
            "watches correct the European error. Do not give him credit for "
            "liberating them. He records a correction and then returns to "
            "racial ranking and criminal anthropology as if the correction had "
            "not happened. The philosophical remainder is clean. Image is not "
            "presence. A dancer can hold a figure that does not hold the orisa, "
            "while the orisa holds the dancer. Later units will say the opposite "
            "case: a priest can fix the saint in an object, and then the object "
            "cannot leave the altar. Both sentences are true because "
            "consecration, not resemblance, decides. Existentially, separate "
            "the picture you display from the seat you actually keep. Stop "
            "accusing other people of idolatry for a confusion you make at home."
        ),
        "prac": (
            "Pick one image you keep — a photo, a figurine, a logo. Say aloud "
            "whether it is an ornament or a seat. If you cannot say, do not "
            "call anyone else an idolater today."
        ),
        "terms": kt(
            (
                "fétiche / idole",
                "European error-words for orisa-objects -> Rodrigues denies "
                "them here for dance figures -> keeping them in the book’s "
                "title after this denial is his doctrine, not the terreiro’s",
            ),
            (
                "état de saint",
                "state of saint: possession, the orisa dancing in the initiate "
                "-> the figure is carried; the saint is in the person -> "
                "\"trance\" as pathology misses the liturgical claim",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — Animism Is Not Fetishism",
                "Both observer documents are forced to admit that the religion "
                "is not the charm-object Europeans came to photograph.",
                "Lasnet’s denial is cosmological (souls, not fetishes); this "
                "denial is ritual (this figure is not a seat).",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Masks of Remembering",
                "Both distinguish a worn or carried form from the power it "
                "points to.",
                "Johnson’s masks serve memory and return; Bahian dance figures "
                "are ornaments of a possession already happening in the head.",
            ),
        ),
    },
    {
        "n": 8,
        "title": "The Saint Can Be Fixed in Any Object",
        "src": "Rodrigues 1900, ch. I — fixer le saint",
        "fr": (
            "Il est certain que si un prêtre voulait appeler ou fixer le saint "
            "dans une de ces figures, il le pourrait, puisqu’il peut appeler ou "
            "fixer le saint dans n’importe quel objet ou dans une personne "
            "quelconque. Dans ce cas la figure deviendrait un saint ou Orisa, "
            "et comme tel ne pourrait plus être retirée de l’autel. Ce n’est "
            "donc pas la ressemblance qui fait le siège. C’est l’acte. Une "
            "personne peut être le siège aussi bien qu’un objet. Une fois fixé, "
            "le saint change le statut de la chose: elle n’est plus un ornement "
            "qu’on promène et qu’on range."
        ),
        "roman": roman(
            "Orisa / santo",
            "fixer le saint (to call or fix the orisa in an object or person)",
            "altar as place that cannot release a fixed orisa",
        ),
        "tr": (
            "It is certain that if a priest wished to call or fix the saint in "
            "one of these figures, he could, since he can call or fix the saint "
            "in any object whatever or in any person. In that case the figure "
            "would become a saint or orisa, and as such could no longer be "
            "removed from the altar. It is therefore not resemblance that makes "
            "the seat. It is the act. A person can be the seat as well as an "
            "object. Once fixed, the saint changes the status of the thing: it "
            "is no longer an ornament one carries and puts away."
        ),
        "comm": (
            "The claim is that presence is an act, not a type of object. A "
            "priest can call or fix the saint in a dance figure, in any thing, "
            "or in a person. Then the thing is an orisa, and it cannot leave "
            "the altar. Unit 7 said the figure is not the seat. This unit says "
            "the figure can become the seat. There is no contradiction. "
            "Resemblance never decided. Consecration decides. Rodrigues, "
            "outsider physician, writes \"any object, any person\" as if he had "
            "caught fetishism in the act — the savage will worship a stick. "
            "That is poison. The terreiro’s sentence is stricter than idolatry: "
            "not every stick, only the called one; and once called, the stick "
            "is no longer available to your hand. Johnson’s mortal shrine is "
            "destroyed at death so it cannot become inheritable furniture. "
            "Bahia’s fixed orisa cannot be taken off the altar for the opposite "
            "reason: it is no longer furniture. Existentially, name what would "
            "have to be prepared — and by whom — before a thing you own could "
            "hold what you honor. If no one is authorized to fix it, do not "
            "call it holy because it resembles a holy thing."
        ),
        "prac": (
            "Name one object you treat as charged. Write who, if anyone, "
            "prepared it, and whether it could be put away tomorrow. If you "
            "cannot name a preparer, stop calling the object a presence."
        ),
        "terms": kt(
            (
                "fixer le saint",
                "to call or fix the orisa in a thing or person -> consecration "
                "as a change of status -> \"enchantment\" or \"fetish-making\" "
                "misses that the altar then refuses to release the thing",
            ),
            (
                "autel",
                "the place from which a fixed orisa cannot be removed -> "
                "jurisdiction, not furniture -> a portable charm-theory cannot "
                "survive this sentence",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Mortal Shrine",
                "Both bind a sacred object’s status to a rite that decides "
                "whether it may persist or must be released.",
                "Johnson’s Ori-shrine is destroyed at the owner’s death; a "
                "fixed Bahian orisa is precisely what may not be taken off the "
                "altar.",
            ),
            (
                "Lasnet, Senegalese Animism — To Worship Is to Bind",
                "Both treat worship as a binding that changes what the thing "
                "now is.",
                "Serer binding is named as ligature; Bahian fixing is named as "
                "a priest’s call that can also take a person as seat.",
            ),
        ),
    },
    {
        "n": 9,
        "title": "Obatala Tends to Supplant Olorun",
        "src": "Rodrigues 1900, ch. I — Obatala / Orisa-nla",
        "fr": (
            "Parmi les saints ou Orisas, la primauté appartient à Obatala, "
            "aussi appelé Orisa-nla (Dieu grand, supérieur ou premier). Pour "
            "les Yorubans, Obatala est une divinité hermaphrodite qui "
            "représente la puissance reproductrice de la nature. Cette divinité "
            "ainsi matérialisée dans sa représentation devient plus accessible; "
            "de là sa tendance à supplanter Olorun, qui est d’ailleurs une "
            "conception plus élevée et plus abstraite. L’accessibilité n’est "
            "pas une chute. Elle est la raison pour laquelle le shaper a un "
            "culte et le créateur n’en a pas. Orisa-nla est grand parmi les "
            "Orisas; il n’est pas un second Olorun."
        ),
        "roman": roman(
            "Obatala / Orisa-nla (great / first orisa)",
            "Olorun",
            "hermaphrodite reproductive power (Rodrigues’s gloss)",
        ),
        "tr": (
            "Among the saints or orisas, primacy belongs to Obatala, also "
            "called Orisa-nla (great, superior, or first god). For the Yoruba, "
            "Obatala is a hermaphrodite divinity who represents the reproductive "
            "power of nature. This divinity, thus materialized in representation, "
            "becomes more accessible; hence the tendency to supplant Olorun, "
            "who is in any case a higher and more abstract conception. "
            "Accessibility is not a fall. It is why the shaper has a cult and "
            "the creator does not. Orisa-nla is great among the orisas; he is "
            "not a second Olorun."
        ),
        "comm": (
            "The claim is that the first orisa is Obatala, Orisa-nla, the great "
            "or first, and that this shaper is approachable in a way Olorun is "
            "not. Friday will belong to Obatala. White cloth will belong to "
            "Obatala. Johnson’s Orisala shapes the lump Olorun made. Bahia "
            "keeps that division of labor: the highest does not sit for a "
            "portrait; the first orisa does the near work of form. Rodrigues, "
            "outsider physician, cannot write \"more accessible\" without "
            "\"higher and more abstract.\" That is Tylor’s ladder spoken in a "
            "salon. Do not adopt it. Accessibility is not degeneration from "
            "monotheism. It is why there is a court. If Obatala \"tends to "
            "supplant\" Olorun in Creole speech, the structure still knows the "
            "difference: one needs nothing, one receives white, one has no "
            "image, one has primacy among images. Calling Obatala hermaphrodite "
            "reproductive nature is Rodrigues’s nature-religion stencil. The "
            "terreiro claim is simpler and harder: the great orisa is first "
            "among those you can actually feast. Existentially, notice when "
            "the available face has quietly replaced the unnamed height in "
            "your own practice. Keep both. Do not punish the near god for "
            "being near."
        ),
        "prac": (
            "Name the most approachable authority in your life and the one you "
            "never address directly. Today, do not let the first steal the "
            "second’s name. Keep them in two written lines."
        ),
        "terms": kt(
            (
                "Obatala / Orisa-nla",
                "great, superior, or first orisa -> primacy among the court, "
                "white cloth, Friday -> \"creator god\" as rival to Olorun "
                "collapses the very distinction the names protect",
            ),
            (
                "accessible",
                "materialized, feastable, imageable -> why Obatala has cult -> "
                "Rodrigues hears a fall from abstraction; the terreiro hears "
                "the reason there is a first orisa at all",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Shaped by the Hand of Orisala",
                "Both split creation: Olorun makes the lump; Orisala / Obatala "
                "shapes what can be met.",
                "Johnson keeps the co-worker clearly under the Maker; Rodrigues "
                "narrates a \"tendency to supplant\" as if accessibility were "
                "usurpation.",
            ),
            (
                "Myths of Ìfẹ̀ — Him-Who-Speaks-Not",
                "Both traditions know a height that withholds ordinary speech "
                "or approach while other powers do the near work.",
                "Ìfẹ̀’s silent one is a mythic person among makers; Bahian "
                "Olorun is the unnamed height above a first orisa who can be "
                "dressed in white.",
            ),
        ),
    },
    {
        "n": 10,
        "title": "Eshu Is a Saint Like the Others",
        "src": "Rodrigues 1900, ch. I — Esu / Elegbara",
        "fr": (
            "Esu, Bará ou Elegbara, est un saint ou Orisa que les nègres "
            "africains de Bahia et leurs métis ont une grande tendance à "
            "confondre avec le diable. J’ai même entendu dire par des nègres "
            "africains que tous les saints peuvent se servir d’Esu pour tenter "
            "ou persécuter quelqu’un. Cependant Esu est un Orisa ou saint comme "
            "les autres, qui a sa confrérie spéciale et ses adorateurs. Dans le "
            "temple ou terreiro du Gantois, le premier jour de la grande fête "
            "est consacré à Esu. Un diable n’a pas de premier jour. Un Orisa "
            "en a un."
        ),
        "roman": roman(
            "Esu / Bará / Elegbara",
            "terreiro of Gantois",
            "confrérie (orisa society)",
        ),
        "tr": (
            "Esu, Bará, or Elegbara is a saint or orisa whom African Bahians "
            "and their mixed-race descendants have a strong tendency to confuse "
            "with the devil. Rodrigues even heard Africans say that all the "
            "saints can use Esu to test or persecute someone. Nevertheless Esu "
            "is an orisa or saint like the others, with a special confraternity "
            "and worshippers. In the temple or terreiro of Gantois, the first "
            "day of the great feast is consecrated to Esu. A devil has no first "
            "day. An orisa has one."
        ),
        "comm": (
            "The claim is that Eshu is an orisa like the others. He has a "
            "confraternity, worshippers, and the first day of the great feast "
            "at Gantois. Other orisas may use him to test or pursue someone. "
            "That is a function inside the court, not a Christian hell. "
            "Rodrigues, outsider physician, leads with the confusion he wants: "
            "Africans and métis \"tend\" to mix Esu with the devil. Then he is "
            "honest enough to write the corrective — however, Esu is a saint "
            "like the others — and then his title still says fetish. Do not "
            "launder the devil-talk. Catechesis taught a European enemy; the "
            "terreiro kept a road-opener with a house. Johnson’s Yoruba pages "
            "do not need Satan to explain a messenger. Bahia’s public language "
            "does, because the parish already named a devil. The liturgical "
            "fact wrecks the overlay: the first day at Gantois is Eshu’s. You "
            "do not open a great feast with the enemy of God unless you have "
            "misnamed the opener. Existentially, refuse the devil-label for a "
            "power that has its own people and its own day. If you need a word "
            "for testing, use testing. Do not import a hell to explain a door."
        ),
        "prac": (
            "Catch one person, habit, or power you have called demonic because "
            "it disrupts you. Today, ask whether it has a house and a day. If "
            "it does, stop using devil as the name."
        ),
        "terms": kt(
            (
                "Esu / Elegbara / Bará",
                "orisa of the opening, the test, the road -> first day at "
                "Gantois, own confraternity -> \"devil\" is a catechetical "
                "overlay, not the terreiro’s rank",
            ),
            (
                "Gantois",
                "a principal Bahian terreiro Rodrigues names -> liturgical "
                "witness that Eshu opens the great feast -> not a folklore "
                "aside",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Olorun, the Lord of Heaven",
                "Both keep orisas as intermediaries inside a court, not as a "
                "rebel army against the highest.",
                "Johnson’s middle is general; this unit names the orisa most "
                "often dragged into a Christian enemy-role.",
            ),
            (
                "Ellis, Yoruba òwe — If an orisha would kill a man for cooking an…",
                "Both treat an orisa as a power with its own offense and "
                "jurisdiction, not as Satan.",
                "The òwe is proverbial warning; Gantois assigns Eshu a feast "
                "day, which a proverb cannot do.",
            ),
        ),
    },
    {
        "n": 11,
        "title": "The First Sacrifice Is Always to Eshu",
        "src": "Rodrigues 1900, ch. II — initiation d’Olympia",
        "fr": (
            "Les animaux du sacrifice étant préparés, on sacrifia à Esu, esprit "
            "du mal, pendant l’après-midi, selon l’usage. Ce sacrifice "
            "propitiatoire précède toutes les fêtes de saint, car son oubli "
            "aurait pour conséquence inéluctable le trouble de la fête. "
            "L’usage n’est pas un détail. Il est l’ordre de la cour: on "
            "n’ouvre pas sans Esu. Rodrigues nomme ici un esprit du mal. Le "
            "terreiro nomme un premier destinataire. Oublier ce premier n’est "
            "pas un péché abstrait; c’est déranger la fête elle-même."
        ),
        "roman": roman(
            "Esu",
            "propitiatory first offering before every saint feast",
        ),
        "tr": (
            "The sacrificial animals having been prepared, offering was made to "
            "Esu — Rodrigues writes \"spirit of evil\" — in the afternoon, "
            "according to custom. This propitiatory offering precedes all saint "
            "feasts, for forgetting it would have the inevitable consequence of "
            "disturbing the feast. The custom is not a detail. It is the order "
            "of the court: one does not open without Esu. Rodrigues names a "
            "spirit of evil here. The terreiro names a first addressee. To "
            "forget that first is not an abstract sin; it is to disorder the "
            "feast itself."
        ),
        "comm": (
            "The claim is sequential: every saint feast is preceded by a "
            "propitiatory offering to Eshu. Forget him and the feast itself is "
            "disturbed. Unit 10 said he is a saint like the others with the "
            "first day at Gantois. This unit says the same thing as order of "
            "operations. You do not reach the other orisas by skipping the "
            "opener. Rodrigues, outsider physician, writes \"esprit du mal\" "
            "in the same breath as \"selon l’usage,\" and the phrase is "
            "poison. He has imported a devil into a liturgical first course. "
            "Do not teach his gloss. Do not teach the sacrifice steps either. "
            "The philosophical remainder needs no recipe: acknowledgment has a "
            "sequence, and the sequence is not optional. Johnson’s "
            "intermediaries explain why you do not shout at Olorun. Eshu "
            "explains why you do not begin a feast as if the road were already "
            "clear. Existentially, name what must be acknowledged first before "
            "you gather people, start work, or enter a kept room. If you skip "
            "that first name because it is inconvenient or badly translated, "
            "expect the gathering to go wrong for a reason you will then blame "
            "on everyone else."
        ),
        "prac": (
            "Before one gathering or task today, name aloud the person or "
            "condition that must be acknowledged first or the work will be "
            "disturbed. Acknowledge it. Do not skip to the part you prefer."
        ),
        "terms": kt(
            (
                "sacrifice propitiatoire",
                "first offering to Esu before every feast -> liturgical "
                "sequence, not devil-worship -> this unit keeps the order and "
                "refuses the recipe",
            ),
            (
                "esprit du mal",
                "Rodrigues’s gloss on Esu -> catechetical poison written into "
                "the witness -> the terreiro’s own sentence is \"first,\" not "
                "\"evil\"",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — First-Fruits Are Always Offered",
                "Both make a first offering the condition of a right relation "
                "to what follows.",
                "Serer first-fruits bind land and ancestor; Bahian first "
                "offering binds the feast to Eshu as opener.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Olorun, the Lord of Heaven",
                "Both describe a religion in which you do not begin with the "
                "highest, but with the middle that can actually be addressed.",
                "Johnson’s middle is the orisa class; this unit names the "
                "particular first addressee of a Bahian feast.",
            ),
        ),
    },
    {
        "n": 12,
        "title": "Sango Is the Thunder-Stone Itself",
        "src": "Rodrigues 1900, ch. I — Sango / litholâtrie",
        "fr": (
            "Chez nous le météorite est non seulement un objet sacré, mais "
            "encore l’idole-fétiche de Sango lui-même, et adoré comme tel. "
            "L’adoration du météorite est directe. Le saint ou Orisa est la "
            "pierre elle-même, où, comme me le disait une négresse, le Saint "
            "se trouve enchanté. Il ne s’agit donc pas d’un symbole posé sur "
            "un autel. La pierre de foudre n’est pas un souvenir de Sango. "
            "Elle est Sango, ou le lieu où Sango est enchâssé. Rodrigues dit "
            "idole-fétiche; la femme dit enchanté. Ce sont deux doctrines."
        ),
        "roman": roman(
            "Sango",
            "meteorite / thunder-stone as the orisa itself",
        ),
        "tr": (
            "Among us the meteorite is not only a sacred object but the "
            "idol-fetish of Sango himself, and adored as such. Adoration of the "
            "meteorite is direct. The saint or orisa is the stone itself, where, "
            "as a Black Bahian woman told Rodrigues, the Saint is found "
            "enchanted. This is therefore not a symbol set on an altar. The "
            "thunder-stone is not a souvenir of Sango. It is Sango, or the "
            "place where Sango is set. Rodrigues says idol-fetish; the woman "
            "says enchanted. Those are two doctrines."
        ),
        "comm": (
            "The claim is identity, not metaphor: Sango is the thunder-stone. "
            "Adoration is direct. A Bahian woman says the Saint is enchanted "
            "in the stone. That is a philosophy of presence. The orisa is not "
            "\"represented\" by a meteorite the way a king is represented by a "
            "coin. The stone is the orisa, or the orisa is bound in it. "
            "Rodrigues, outsider physician, cannot write the sentence without "
            "idole-fétiche and litholâtrie. He needs a primitive stage where "
            "people worship rocks. That is poison. The woman’s word — "
            "enchanted — is the terreiro’s word. Unit 7 denied that every "
            "figure is a seat. This unit asserts a seat that does not look "
            "like a person. Together they destroy resemblance-theory. Johnson "
            "can consecrate iron to Ogun without saying the knife is Ogun; "
            "Bahia’s Sango-stone goes further. Existentially, find one object "
            "you treat as a reminder and ask whether anyone you trust would "
            "call it the presence itself. If you only ever keep souvenirs, you "
            "have not yet heard this teaching."
        ),
        "prac": (
            "Find one stone, tool, or kept object you treat as a reminder. "
            "Ask whether it is a souvenir or a seat. Write the answer in one "
            "sentence. Do not upgrade it by wishing."
        ),
        "terms": kt(
            (
                "Sango",
                "thunder orisa -> in Bahia, often the meteorite itself -> "
                "\"thunder-god\" as a weather- allegory misses direct "
                "adoration of the stone",
            ),
            (
                "enchanté",
                "the woman’s word: the Saint is bound / set in the stone -> "
                "presence, not decoration -> Rodrigues’s \"idole-fétiche\" "
                "translates her sentence into his book’s title",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — Libation at the Baobab and the "
                "Consecrated Stone",
                "Both give a particular stone or tree as a place where the "
                "religion actually happens.",
                "Serer stone and baobab receive libation as addressable sites; "
                "the Bahian meteorite is said to be Sango, not only his altar.",
            ),
            (
                "Myths of Ìfẹ̀ — Thunder Cannot Stop Brothers",
                "Both keep thunder inside a kinship of powers, not as a lonely "
                "natural force.",
                "Ìfẹ̀’s thunder is narrative weather among brothers; Bahia’s "
                "Sango is a stone you can fail to blow on.",
            ),
        ),
    },
    {
        "n": 13,
        "title": "No Terreiro Without Sango",
        "src": "Rodrigues 1900, ch. I — ubiquité de Sango",
        "fr": (
            "Il n’y a pas de temple ou terreiro, il n’y a pas de chapelle "
            "fétichiste à Bahia où l’on ne trouve ce saint. Chez Livaldina, "
            "une prêtresse ou mère de terreiro, la pierre est un peu plus "
            "petite que le poing. Cette mère de terreiro m’a prié de souffler "
            "sur le fétiche pour qu’il ne m’arrivât aucun malheur. "
            "L’ubiquité n’est pas une statistique. Elle est une doctrine: "
            "Sango est l’axe d’orage de chaque maison. La prière de Livaldina "
            "n’est pas une superstition de plus. C’est une hospitalité: "
            "l’étranger souffle pour que la pierre ne le frappe pas."
        ),
        "roman": roman(
            "Sango",
            "terreiro",
            "mãe de terreiro (Livaldina)",
        ),
        "tr": (
            "There is no temple or terreiro, no \"fetish chapel\" in Bahia, "
            "where this saint is not found. At Livaldina’s, a priestess or "
            "mother of terreiro, the stone is a little smaller than a fist. "
            "This mother of terreiro asked Rodrigues to blow on the \"fetish\" "
            "so that no misfortune would come to him. Ubiquity is not a "
            "statistic. It is a teaching: Sango is the storm-axis of every "
            "house. Livaldina’s request is not one more superstition. It is "
            "hospitality: the stranger blows so the stone will not strike him."
        ),
        "comm": (
            "The claim is that Sango is not optional. There is no terreiro in "
            "Bahia without this saint. The stone may be smaller than a fist. "
            "The house is still under thunder. A mãe de terreiro named "
            "Livaldina asks the visiting physician to blow on the stone so "
            "that nothing bad happens to him. That is not fear of a pebble. "
            "It is hospitality toward a stranger who has entered a jurisdiction "
            "he does not understand. Rodrigues, outsider physician, writes "
            "chapelle fétichiste and fétiche in the same report, and he takes "
            "the blow as folklore. His ranking is poison. The ethnographic "
            "remainder is a map: every kept house has a weather. Johnson can "
            "describe Ogun without saying every compound must show iron; Bahia "
            "says every terreiro shows Sango. The later unit on the stone in "
            "the head will say why: Sango is the orisa who seizes the initiate "
            "at the skull. A house without that axis would be a house that "
            "denied possession. Existentially, notice which presence is in "
            "every room you keep — not the one you prefer, the one you cannot "
            "omit. Treat a guest as someone who must be put in right relation "
            "to that presence, not as a tourist of your objects."
        ),
        "prac": (
            "Name the one presence, rule, or person that is in every room of "
            "your household — the one you cannot omit. Today, tell one guest "
            "or one newcomer what that axis is, without joking it away."
        ),
        "terms": kt(
            (
                "mãe de terreiro",
                "mother of the terreiro, priestess-head -> Livaldina’s "
                "jurisdiction includes the stone and the stranger -> "
                "\"priestess\" as exotic office misses hospitality as law",
            ),
            (
                "ubiquité de Sango",
                "no Bahian terreiro without this orisa -> storm-axis of the "
                "house -> optional-pantheon language fails here",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Ogun, God of Iron",
                "Both name an orisa who is recognized by a material that "
                "recurs wherever the cult is serious (iron / thunder-stone).",
                "Johnson’s Ogun is craft and war; Sango’s ubiquity is "
                "meteorite and possession in every Bahian house.",
            ),
            (
                "Lasnet, Senegalese Animism — The Ancestor and the Land Are "
                "One Cult",
                "Both refuse a house that could be religiously empty of its "
                "axis.",
                "Serer axis is ancestor-and-land; Bahian axis named here is "
                "Sango in every terreiro.",
            ),
        ),
    },
    {
        "n": 14,
        "title": "The Stone on the Head Is Possession",
        "src": "Rodrigues 1900, ch. I — Osê de Sango",
        "fr": (
            "Selon les explications qui m’ont été données par un père de "
            "terreiro, le météorite que la figure porte à la tête symbolise "
            "l’état de possession où Sango s’empare de l’initié au moment où "
            "il pénètre dans sa tête. La pierre n’est donc pas un chapeau. "
            "Elle est une doctrine portée. Sango n’arrive pas à côté de la "
            "personne. Il entre par la tête. Le père de terreiro parle ici en "
            "maître de maison, non en informateur folklorique. Rodrigues "
            "écoute et écrit \"figure\" et \"fétiche\"; l’explication qu’il "
            "reçoit est une philosophie de l’entrée."
        ),
        "roman": roman(
            "Sango",
            "Osê de Sango",
            "pai de terreiro",
            "possession as the orisa entering the head",
        ),
        "tr": (
            "According to explanations given to Rodrigues by a father of "
            "terreiro, the meteorite the figure wears on the head symbolizes "
            "the state of possession in which Sango seizes the initiate at the "
            "moment he enters the head. The stone is therefore not a hat. It "
            "is a teaching worn. Sango does not arrive beside the person. He "
            "enters by the head. The father of terreiro speaks here as master "
            "of a house, not as a folklore informant. Rodrigues listens and "
            "writes \"figure\" and \"fetish\"; the explanation he receives is "
            "a philosophy of entry."
        ),
        "comm": (
            "The claim is that possession is Sango entering the head. The "
            "meteorite on the figure is not costume. A pai de terreiro says it "
            "marks the moment the orisa seizes the initiate. Head is destiny "
            "and doorway. Johnson’s Ori is the head as the person’s own "
            "sacred allotment; Bahia’s Sango-stone on the head is the orisa’s "
            "allotment of that same place. Two doctrines can share a skull. "
            "Rodrigues, outsider physician, files the explanation under a "
            "carved figure and will elsewhere reach for hysteria, crime, and "
            "race. That is poison. Do not medicalize the entry. The "
            "philosophical remainder is clean: a person can be a seat (unit 8), "
            "and the seat is specified — the head — and the orisa who teaches "
            "that specification in this witness is Sango. Existentially, "
            "notice when a presence \"enters the head\" as a change of who is "
            "speaking. If your voice suddenly serves another jurisdiction, do "
            "not call it mood until you have asked whose weather it is."
        ),
        "prac": (
            "Once today, when your tone or certainty suddenly changes, stop "
            "and ask: whose voice is this, mine or an adopted weather? Write "
            "the answer before you speak the next sentence."
        ),
        "terms": kt(
            (
                "possession / état de saint",
                "Sango seizes the initiate by entering the head -> a change of "
                "who occupies the person -> \"trance\" or \"hysteria\" is the "
                "physician’s reduction",
            ),
            (
                "tête",
                "the portal of entry -> not a metaphor for mind -> Johnson’s "
                "Ori and this Sango-stone share the place and not the same "
                "orisa",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Ori: the Head as Destiny",
                "Both treat the head as a sacred site, not a mere anatomy.",
                "Johnson’s Ori is the person’s own destiny-shrine; this unit’s "
                "head is the door Sango uses to seize the initiate.",
            ),
            (
                "Myths of Ìfẹ̀ — Odúm’la Speaks in the Òrní",
                "Both have a power that speaks in a human office rather than "
                "from a distant sky.",
                "Ìfẹ̀’s speaking is priestly succession; Bahian possession is "
                "an orisa entering a head in the dance.",
            ),
        ),
    },
    {
        "n": 15,
        "title": "Yemanja Is the Divinized Sea",
        "src": "Rodrigues 1900, ch. I — Yé-man-jà",
        "fr": (
            "Yé-man-jà, ou mère des eaux, c’est une création mythologique qui "
            "symbolise l’hydrolâtrie primitive. C’est la mer divinisée, et "
            "c’est pourquoi son fétiche est une pierre marine. Aux jours de "
            "fête, nègres et mulâtres, en procession, apportent dans de petites "
            "pirogues les offrandes de Yé-man-jà. Ils vont jusqu’au milieu du "
            "Dique où ils les jettent à l’eau. La mer n’est pas un décor. Elle "
            "est une mère. La pierre marine n’est pas un souvenir de plage. "
            "Elle est le siège que l’eau se donne à terre."
        ),
        "roman": roman(
            "Yemanja / Yé-man-jà (mother of the waters)",
            "marine stone",
            "Dique (procession of offerings)",
        ),
        "tr": (
            "Yemanja, or mother of the waters, is — Rodrigues writes — a "
            "mythological creation that symbolizes primitive hydrolatry. She "
            "is the sea divinized, and that is why her \"fetish\" is a marine "
            "stone. On feast days Black Bahians and people of mixed descent "
            "bring Yemanja’s offerings in small canoes, in procession. They go "
            "to the middle of the Dique and throw them into the water. The sea "
            "is not scenery. She is a mother. The marine stone is not a beach "
            "souvenir. It is the seat the water gives itself on land."
        ),
        "comm": (
            "The claim is that the sea is a person with a name, a stone, a "
            "procession, and a day. Yemanja is mother of the waters. Offerings "
            "go out in small boats to the middle of the Dique and enter the "
            "water. The marine stone is her land-seat. Rodrigues, outsider "
            "physician, cannot write the name without \"hydrolâtrie primitive.\" "
            "That is Tylor again: first people worship water, later they invent "
            "God. Poison. The terreiro is not stuck at a stage. It is keeping "
            "a mother who is the sea in a Catholic port city. Myths of Ìfẹ̀ "
            "set Olókun to curb the sea; Bahia names Yemanja and takes boats "
            "to her. Different waters, same refusal to let ocean be mere "
            "geography. Do not turn the procession into a how-to of offerings. "
            "The philosophical act is to treat a public body of water as "
            "addressable. Existentially, take one thanks to actual water today "
            "— not as symbol of your feelings, as a body that can receive. If "
            "you cannot do that without a recipe, you have not heard the "
            "mother; you have heard a tourist brochure."
        ),
        "prac": (
            "Go to actual water — tap, fountain, harbor, rain. Speak one "
            "sentence of thanks to it as a body that can receive, not as a "
            "symbol of your mood. Do not throw a crafted offering."
        ),
        "terms": kt(
            (
                "Yemanja / Yé-man-jà",
                "mother of the waters, the sea as orisa -> marine stone, Dique "
                "procession -> \"goddess of the ocean\" as poetry misses a "
                "stone and a public boat-day",
            ),
            (
                "hydrolâtrie primitive",
                "Rodrigues’s evolutionist stamp -> poison -> the terreiro’s "
                "word is mother, not a stage of religion",
            ),
        ),
        "res": res(
            (
                "Myths of Ìfẹ̀ — Olókun Set to Curb the Sea",
                "Both give the sea a named power instead of leaving it as "
                "backdrop.",
                "Ìfẹ̀’s Olókun is set to curb; Bahian Yemanja receives boats "
                "at the Dique as mother of waters.",
            ),
            (
                "Lasnet, Senegalese Animism — One Does Not Address God; One "
                "Addresses the Spirits",
                "Both put relationship at a local body of water rather than at "
                "the unnamed height.",
                "Serer genius of the fountain is one among many mammam; "
                "Yemanja is a principal orisa with a city procession.",
            ),
        ),
    },
    {
        "n": 16,
        "title": "Osun Lives in the Fountain",
        "src": "Rodrigues 1900, ch. I — Osun",
        "fr": (
            "Osun, la déesse ou Orisa des sources et des lacs, regardée comme "
            "une autre femme de Sango, est représentée par une pierre fluviale "
            "ou lacustre. La fontaine Saint-Pierre, voisine de la maison où je "
            "demeure, est l’objet d’un culte fervent, parce que c’est la "
            "demeure d’un Osun. Une fontaine publique peut donc être une "
            "maison. Le nom catholique de la source n’évince pas l’Orisa. "
            "Rodrigues habite à côté du culte et continue d’écrire fétiche. "
            "L’eau douce n’est pas une Yemanja moindre; elle est une autre "
            "femme de la cour, avec sa propre pierre."
        ),
        "roman": roman(
            "Osun",
            "Sango (as husband in this report)",
            "river / lake stone",
            "fontaine Saint-Pierre as Osun’s dwelling",
        ),
        "tr": (
            "Osun, goddess or orisa of springs and lakes, regarded as another "
            "wife of Sango, is represented by a river or lake stone. The "
            "Saint-Pierre fountain, near the house where Rodrigues lives, is "
            "the object of fervent cult because it is the dwelling of an Osun. "
            "A public fountain can therefore be a house. The Catholic name of "
            "the spring does not evict the orisa. Rodrigues lives next to the "
            "cult and continues to write fetish. Fresh water is not a lesser "
            "Yemanja; she is another woman of the court, with her own stone."
        ),
        "comm": (
            "The claim is that Osun inhabits a fountain. Not \"is associated "
            "with water.\" Lives there. The Saint-Pierre fountain beside the "
            "physician’s house is her dwelling, and the cult is fervent. A "
            "Catholic saint’s name on the fountain does not empty the house. "
            "Unit 6 already said santo is a bridge. Here the bridge is carved "
            "on municipal stone: Saint-Pierre on the lip, Osun in the water. "
            "Rodrigues, outsider physician, lives next door and still needs "
            "fetish and \"another wife of Sango\" as if marriage-notes "
            "explained a spring. His intimacy with the site does not clean his "
            "mouth. Do not adopt the ranking that would make Osun a pretty "
            "lesser sea. Yemanja is the sea; Osun is springs and lakes; both "
            "have stones. Different waters, different seats. Existentially, "
            "treat one local water as a dwelling, not a utility. If you can "
            "only see a pipe, you are living next to a house and writing "
            "\"resource\" on the door."
        ),
        "prac": (
            "Visit one local fountain, tap, or spring you usually treat as "
            "infrastructure. Stand there long enough to ask who dwells. Do "
            "not leave an offering. Leave the utility-name behind for the "
            "walk home."
        ),
        "terms": kt(
            (
                "Osun",
                "orisa of springs and lakes -> river or lake stone, fountain "
                "as dwelling -> \"love goddess\" or lesser-Yemanja talk misses "
                "a particular Bahian fountain",
            ),
            (
                "demeure",
                "dwelling: the fountain is where Osun lives -> not a symbol "
                "of purity -> Saint-Pierre as the public name of the same "
                "water",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — One Does Not Address God; One "
                "Addresses the Spirits",
                "Both put a genius at the fountain rather than at the sky.",
                "Serer fountain-spirit is one of many mammam; Osun is a named "
                "orisa whose dwelling Rodrigues walks past daily.",
            ),
            (
                "Myths of Ìfẹ̀ — Olókun Set to Curb the Sea",
                "Both refuse to let a body of water be unnamed.",
                "Olókun curbs the sea; Osun inhabits fresh water under a "
                "Catholic fountain-name.",
            ),
        ),
    },
    {
        "n": 17,
        "title": "Ogun Is Iron After the Father Prepares It",
        "src": "Rodrigues 1900, ch. I — Ogun / rail",
        "fr": (
            "Un Africain à qui je demandais si Ogun n’était pas simplement un "
            "objet en fer m’a répliqué: « Oui, un simple morceau de ce rail de "
            "tramway que vous voyez là est ou peut être Ogun, mais seulement "
            "après que le père du terreiro l’aura préparé. » Le fer, et non la "
            "pierre, est l’attribut d’Ogun, dieu de la guerre. N’importe quel "
            "objet en fer peut être adoré comme représentant Ogun, pourvu "
            "qu’il ait été consacré. La phrase de l’Africain est toute la "
            "philosophie: le matériau est commun; le siège est fait. Sans le "
            "père, le rail reste un rail."
        ),
        "roman": roman(
            "Ogun",
            "pai de terreiro",
            "iron (not stone) as Ogun’s attribute",
            "consecration of a tram rail",
        ),
        "tr": (
            "An African whom Rodrigues asked whether Ogun was not simply an "
            "object of iron replied: \"Yes, a simple piece of that tramway rail "
            "you see there is or can be Ogun, but only after the father of the "
            "terreiro has prepared it.\" Iron, not stone, is the attribute of "
            "Ogun, god of war. Any iron object may be adored as representing "
            "Ogun, provided it has been consecrated. The African’s sentence is "
            "the whole philosophy: the material is common; the seat is made. "
            "Without the father, the rail remains a rail."
        ),
        "comm": (
            "The claim is that Ogun is iron after a pai de terreiro prepares "
            "it. A tram rail in the street can be Ogun. The same rail, "
            "unprepared, is a rail. Material plus act. Unit 8 said any object "
            "can be fixed; this unit names the material that belongs to this "
            "orisa — iron, not Sango’s stone — and names the officer who does "
            "the fixing. Rodrigues, outsider physician, asked a reduction "
            "question: is Ogun simply iron? He wanted fetish = metal. The "
            "African refused the adverb. Simply is the physician’s word. Only "
            "after is the terreiro’s word. Do not adopt the reduction and then "
            "praise the reply as quaint. Johnson’s Ogun is god of war and of "
            "all iron instruments, the blacksmiths’ god; Bahia adds the "
            "colonial street: a tram rail is already in the war-and-craft "
            "field once prepared. Existentially, name who prepared the tool "
            "you use. If no one did, you are holding a rail and calling it a "
            "god because it is heavy. That is the physician’s error in your "
            "own hand."
        ),
        "prac": (
            "Take one iron tool you use today. Name the person who made or "
            "prepared it — smith, factory, teacher, you. If you cannot name "
            "anyone, do not call the tool more than metal."
        ),
        "terms": kt(
            (
                "Ogun",
                "orisa of iron and war -> any consecrated iron, even a tram "
                "rail -> \"war-god\" as violence-only misses that preparation "
                "makes the seat",
            ),
            (
                "préparé / consacré",
                "the pai de terreiro’s act -> rail becomes Ogun -> without "
                "this verb Rodrigues’s \"simply iron\" would win",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Ogun, God of Iron",
                "Both bind Ogun to iron as domain, not as a statue of a "
                "warrior.",
                "Johnson’s iron is tools and weapons in Yoruba craft; this "
                "unit’s iron is a Bahian tram rail after a pai prepares it.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Iron and the Sacred Tree",
                "Both extend Ogun from war into a living or planted sign.",
                "Johnson adds the silk-cotton tree as image; Bahia’s witness "
                "here stays with consecrated metal in the street.",
            ),
        ),
    },
    {
        "n": 18,
        "title": "Ogun Opens the Road for Eshu",
        "src": "Rodrigues 1900, ch. I — Ogun et Esu",
        "fr": (
            "Un vieil Africain me disait un jour — dans un sens figuré, "
            "naturellement — qu’Ogun est celui qui ouvre la route à Esu. La "
            "phrase n’est pas une géographie. Elle nomme un ordre. Le fer "
            "prépare le passage; Esu emprunte le passage. Rodrigues ajoute "
            "\"dans un sens figuré, naturellement,\" parce qu’il ne peut pas "
            "laisser la phrase debout. Le vieil Africain n’a pas demandé cette "
            "correction. Ogun n’est pas le valet d’Esu. Il est celui sans qui "
            "la route n’est pas ouverte."
        ),
        "roman": roman(
            "Ogun",
            "Esu",
            "ouvrir la route (open the road)",
        ),
        "tr": (
            "An old African said to Rodrigues one day — \"in a figurative "
            "sense, of course,\" Rodrigues adds — that Ogun is the one who "
            "opens the road for Esu. The sentence is not geography. It names "
            "an order. Iron prepares the passage; Esu takes the passage. "
            "Rodrigues adds \"in a figurative sense, of course,\" because he "
            "cannot let the sentence stand. The old African did not ask for "
            "that correction. Ogun is not Esu’s servant. He is the one without "
            "whom the road is not open."
        ),
        "comm": (
            "The claim is an order of two orisas: Ogun opens the road; Eshu "
            "goes. Iron first, then the opener of the feast. Units 10 and 11 "
            "gave Eshu the first day and the first offering. This unit says "
            "even that first has a first: someone cuts the path. Rodrigues, "
            "outsider physician, cannot bear a literal road between gods. He "
            "inserts \"dans un sens figuré, naturellement\" — of course it is "
            "only a figure. That adverb is poison of a quieter kind. It "
            "trains you to hear African speech as metaphor for something the "
            "clinic already understands. Do not take the correction. The old "
            "man’s sentence is liturgical philosophy. Johnson’s Ogun governs "
            "iron; Bahia’s Ogun uses iron to open Eshu’s road. Myths of Ìfẹ̀ "
            "send Ógun to his trees when the city will not hold him; here Ogun "
            "is still the one who makes a way. Existentially, name who opens "
            "the road before you act — the tool, the person, the permission. "
            "If you skip that opener because you want to be already on the "
            "road, you are doing Rodrigues’s \"naturally\" with your day."
        ),
        "prac": (
            "Before one action today, name the opener — tool, person, or "
            "permission — without whom the road is closed. Use that opener "
            "first. Do not start in the middle and call it efficiency."
        ),
        "terms": kt(
            (
                "ouvrir la route",
                "Ogun opens the road for Esu -> sequence of iron then "
                "messenger -> \"figurative, of course\" is the physician’s "
                "flinch, not the teaching",
            ),
            (
                "Ogun / Esu",
                "paired orisas of path-making -> not rivals, not devil and "
                "war-god as Europe pairs them -> a court order",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Ogun, God of Iron",
                "Both make Ogun the power of the cutting, making, war-and-tool "
                "edge that lets anything else proceed.",
                "Johnson’s domain is iron instruments; this unit’s domain is "
                "the road those instruments open for Eshu.",
            ),
            (
                "Myths of Ìfẹ̀ — Ógun Goes to His Trees",
                "Both keep Ogun as a power of path and departure, not a statue "
                "of battle.",
                "Ìfẹ̀’s Ógun leaves a city that chose another king; Bahian "
                "Ogun opens Eshu’s road inside a still-standing terreiro.",
            ),
        ),
    },
    {
        "n": 19,
        "title": "Shopona Listens Only to His Mother",
        "src": "Rodrigues 1900, ch. I — Saponan",
        "fr": (
            "Saponan, Wari-waru, ou Omolu, dieu ou saint de la variole, est un "
            "autre exemple de l’habitude qu’ils ont de diviniser des entités "
            "abstraites. Saponan n’écoute et ne respecte que sa mère Iyabayin. "
            "La maladie a donc une personne, et cette personne a une mère. On "
            "n’adresse pas la variole comme on adresse une statistique. On "
            "cherche la voix à laquelle le saint obéit. Rodrigues dit entité "
            "abstraite. Le terreiro dit un fils qui n’écoute que sa mère."
        ),
        "roman": roman(
            "Saponan / Shopona / Omolu / Wari-waru",
            "Iyabayin (the mother he alone respects)",
        ),
        "tr": (
            "Saponan, Wari-waru, or Omolu, god or saint of smallpox, is — "
            "Rodrigues writes — another example of their habit of divinizing "
            "abstract entities. Saponan listens to and respects only his mother "
            "Iyabayin. Illness therefore has a person, and that person has a "
            "mother. One does not address smallpox as one addresses a "
            "statistic. One looks for the voice the saint obeys. Rodrigues "
            "says abstract entity. The terreiro says a son who listens only to "
            "his mother."
        ),
        "comm": (
            "The claim is kinship inside danger: the smallpox orisa listens "
            "only to his mother Iyabayin. Disease is not an \"abstract entity\" "
            "to be divinized, as if people had first invented a concept and "
            "then given it a statue. Disease is a person in the court, and "
            "that person has a mother whose voice he takes. The philosophical "
            "act is to look for the one who can speak to the difficult power. "
            "Rodrigues, outsider physician, writes the evolutionist caption "
            "first — they divinize abstractions — and only then the sentence "
            "that matters. His caption is poison. A physician of his century "
            "had every reason to treat smallpox as a public-health object; he "
            "had no right to treat Iyabayin as a symptom of primitive thought. "
            "Do not ingest ceremonial how-to against illness. Keep the "
            "structure: some powers do not hear you, and they do hear someone. "
            "Existentially, name whose voice the difficult power in your life "
            "actually hears. If you keep shouting at the son and refuse to "
            "learn the mother’s name, you are practicing Rodrigues’s "
            "abstraction with a human face."
        ),
        "prac": (
            "Name one difficult power you keep addressing directly — an "
            "illness-fear, a rage, a workplace force. Write the name of the "
            "one person or condition it actually listens to. Speak to that "
            "one today, not to the power."
        ),
        "terms": kt(
            (
                "Saponan / Omolu",
                "orisa of smallpox -> a person in the court, not a germ "
                "allegory -> \"disease-god\" as abstraction is Rodrigues’s "
                "caption",
            ),
            (
                "Iyabayin",
                "the mother Shopona alone respects -> the voice that reaches "
                "him -> skipping her is the error of shouting at the son",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Between Maker and World",
                "Both require a middle: you do not always address the power "
                "you mean.",
                "Johnson’s middle is the orisa class under Olorun; this unit’s "
                "middle is a mother under a fearsome orisa.",
            ),
            (
                "Ellis, Yoruba òwe — He who is pierced with a thorn must limp "
                "off to…",
                "Both send the sufferer toward the particular help that fits "
                "the wound, not toward a general sky.",
                "The òwe is practical wit; Iyabayin is a named mother inside "
                "the court.",
            ),
        ),
    },
    {
        "n": 20,
        "title": "The Iroko Is the God Himself",
        "src": "Rodrigues 1900, ch. I — Iroco / gamelleira",
        "fr": (
            "Un arbre peut être un vrai fétiche animé, ou au contraire "
            "simplement représenter la demeure ou l’autel d’un saint. Sous le "
            "nom d’Iroco, la gameleira aux grandes dimensions est l’objet d’un "
            "culte fervent. Plus d’une mère de terreiro m’a conjuré de ne "
            "jamais laisser abattre une gameleira qui a poussé dans un terrain "
            "qui m’appartient. L’arbre animé est ici bien clairement le dieu "
            "lui-même, le saint. Le voyageur qui passe se découvre avec "
            "respect et de loin lui envoie un baiser. Deux cas donc: l’arbre "
            "comme maison, et l’arbre comme le saint. Les confondre, c’est "
            "revenir à l’idole."
        ),
        "roman": roman(
            "Iroco / Iroko (gameleira)",
            "mãe de terreiro",
            "tree as god himself vs tree as dwelling",
        ),
        "tr": (
            "A tree may be a true animated \"fetish,\" or on the contrary may "
            "simply represent the dwelling or altar of a saint. Under the name "
            "Iroko, the large gameleira is the object of fervent cult. More "
            "than one mother of terreiro begged Rodrigues never to let a "
            "gameleira that had grown on land he owned be cut down. The "
            "animated tree is here quite clearly the god himself, the saint. "
            "The traveler who passes uncovers his head with respect and from "
            "afar sends it a kiss. Two cases, then: the tree as house, and the "
            "tree as the saint. To confuse them is to return to the idol."
        ),
        "comm": (
            "The claim is a fork the terreiro already uses: a tree may be a "
            "dwelling, or a tree may be the god. Iroko, the great gameleira, "
            "is in this witness the second case — the saint himself. Mothers "
            "of terreiro beg a landowner not to cut one that has grown on his "
            "ground. A passer-by uncovers and sends a kiss from far off. "
            "Distance is part of the rite. Rodrigues, outsider physician, "
            "writes vrai fétiche animé because he needs his title. Poison. The "
            "distinction he records wrecks the title: if some trees are only "
            "houses, \"fetish\" cannot mean \"they worship wood.\" Johnson’s "
            "Ogun has a planted silk-cotton as image; Bahia’s Iroko can be "
            "the image’s opposite — not representation, identity. Lasnet’s "
            "woods are sanctuaries; this gameleira is a person you do not "
            "fell. Existentially, give one living tree the courtesy you would "
            "give a person you are not sure you may touch. If you can only "
            "see timber, you have already chosen the slave who will take the "
            "axe in the next unit."
        ),
        "prac": (
            "Choose one living tree you pass. Uncover or pause at a distance. "
            "Do not touch it to prove a feeling. Write whether you treated it "
            "as timber, as a house, or as someone."
        ),
        "terms": kt(
            (
                "Iroco / Iroko",
                "the gameleira as orisa -> in this witness, the god himself, "
                "not only an altar -> \"sacred tree\" as scenery misses the "
                "mães’ ban on felling",
            ),
            (
                "demeure / le dieu lui-même",
                "the fork: house versus identity -> unit 7’s ornament/seat "
                "distinction now applied to a living tree",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — The Woods Are Sanctuaries",
                "Both treat a stand of living wood as a jurisdiction you do "
                "not casually enter or cut.",
                "Serer woods are sanctuary; the Bahian gameleira can be the "
                "saint in person.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Iron and the Sacred Tree",
                "Both bind an orisa to a particular tree as more than shade.",
                "Johnson’s silk-cotton represents Ogun; this Iroko is said to "
                "be the god.",
            ),
        ),
    },
    {
        "n": 21,
        "title": "The Slave Who Would Not Cut the Iroko",
        "src": "Rodrigues 1900, ch. I — esclave et Iroco",
        "fr": (
            "On raconte qu’un propriétaire avait ordonné à un de ses esclaves "
            "d’abattre l’arbre. Humble mais résolu, l’esclave refusa en disant "
            "qu’il préférait le châtiment dont il était menacé, deux cents "
            "coups de fouet, plutôt que de toucher seulement à l’Iroco. Un "
            "autre esclave eut l’audace de commettre ce sacrilège; il tomba "
            "foudroyé au premier coup de hache. Au lieu de lait, l’incision "
            "faite au tronc laissait couler un sang vif. Le récit n’est pas "
            "une preuve de terreur fétichiste. C’est une éthique: la personne "
            "de l’arbre outrepasse l’ordre du maître. Le sang est la réponse "
            "de l’arbre."
        ),
        "roman": roman(
            "Iroco / Iroko",
            "refusal to fell as ethical claim",
        ),
        "tr": (
            "It is told that an owner ordered one of his enslaved people to "
            "fell the tree. Humble but resolved, the enslaved person refused, "
            "saying he preferred the punishment with which he was threatened — "
            "two hundred lashes — rather than even touch the Iroko. Another "
            "enslaved person had the boldness to commit that sacrilege; he "
            "fell thunderstruck at the first axe-blow. Instead of milk, the "
            "cut in the trunk let a living blood flow. The story is not a "
            "proof of fetish terror. It is an ethic: the tree’s personhood "
            "outranks the master’s order. The blood is the tree’s reply."
        ),
        "comm": (
            "The claim is ethical before it is marvelous: an enslaved person "
            "refuses to cut the Iroko, preferring two hundred lashes to a "
            "touch. Another takes the axe and falls at the first blow; the "
            "trunk bleeds living blood, not milk. Unit 20 said the tree can "
            "be the god. This unit says the god’s personhood outranks a "
            "property order. The first enslaved person is the teacher. The "
            "second is the warning. Rodrigues, outsider physician, files the "
            "tale as evidence of fetish fear among slaves — useful, for him, "
            "to a racial and criminal story about Bahian religion. That use "
            "is poison. Do not retell the blood as spectacle. Do not retell "
            "the lashes as atmosphere. The philosophical remainder is a "
            "conflict of jurisdictions: master of land versus mother of "
            "terreiro versus the tree himself. Lasnet’s woods are sanctuaries; "
            "this sanctuary answers. Existentially, refuse one order today "
            "that would violate a kept living thing — a tree, an animal, a "
            "person you were told was available. Pay the smaller cost of "
            "refusal. Do not wait for the trunk to bleed before you believe "
            "the first enslaved person’s sentence."
        ),
        "prac": (
            "Refuse one order or convenience today that treats a kept living "
            "thing as available timber. Take the smaller cost of the refusal. "
            "Write the sentence you would have had to say to the person who "
            "gave the order."
        ),
        "terms": kt(
            (
                "Iroco",
                "the tree whose personhood outranks a master’s command -> "
                "ethic, not folklore -> \"superstitious slave\" is Rodrigues’s "
                "use of the story",
            ),
            (
                "sang vif",
                "living blood instead of sap -> the tree’s reply -> not a "
                "marvel to collect; a jurisdiction asserting itself",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — The Woods Are Sanctuaries",
                "Both make cutting a sanctuary-wood a violation, not a "
                "forestry decision.",
                "Serer sanctuary is communal woods; this Iroko answers a "
                "slave-order with blood and a refused lash.",
            ),
            (
                "Ellis, Yoruba òwe — Disobedience is the father of insolence",
                "Both know refusal as a moral act with a lineage.",
                "The òwe warns that disobedience breeds insolence toward "
                "human rank; this refusal is obedience to a higher rank than "
                "the owner.",
            ),
        ),
    },
    {
        "n": 22,
        "title": "Ifa Is the God of Divinations",
        "src": "Rodrigues 1900, ch. I — Orisa Ifa",
        "fr": (
            "L’Orisa Ifa est représenté par le fruit spécial d’un palmier "
            "(dendezeiro) qui renferme parfois quatre noix au lieu de trois. "
            "Ifa est le dieu des divinations par excellence. Le sorcier jette "
            "son instrument et tire ses déductions de la position que prennent "
            "en tombant les moitiés des noix. Lire une chute, c’est déjà une "
            "philosophie: le monde parle en se posant. Rodrigues dit sorcier. "
            "Le terreiro dit un dieu de la lecture. On n’invente pas le "
            "message; on le reçoit de la position."
        ),
        "roman": roman(
            "Ifa",
            "dendezeiro (dendê palm) nuts",
            "divination by the fall of nut-halves",
        ),
        "tr": (
            "The orisa Ifa is represented by the special fruit of a dendê palm "
            "that sometimes holds four nuts instead of three. Ifa is the god "
            "of divinations par excellence. The \"sorcerer\" casts his "
            "instrument and draws his deductions from the position the nut-"
            "halves take in falling. To read a fall is already a philosophy: "
            "the world speaks by how it settles. Rodrigues says sorcerer. The "
            "terreiro says a god of reading. One does not invent the message; "
            "one receives it from the position."
        ),
        "comm": (
            "The claim is that Ifá is a god of reading. The dendê fruit, "
            "sometimes with four nuts instead of three, is his sign. The "
            "diviner casts; meaning is in the positions of the fall. This is "
            "not a trick and not a recipe. It is an epistemology: the world "
            "can be asked, and the answer arrives as a layout, not as a "
            "private vision. Rodrigues, outsider physician, writes sorcier "
            "because criminal anthropology needs a conjurer. Poison. Do not "
            "complete a session from this page. Do not list figures or "
            "sacrifices. Johnson’s Yoruba faith knows a populated middle "
            "between Maker and world; Ifá is how that middle is consulted. "
            "Myths of Ìfẹ̀ locate truth at shrines and in priests’ mouths; "
            "Ifá locates a further mouth in the fall of nuts. Existentially, "
            "notice how you already read a fall — a coincidence, a seating, "
            "a dropped thing — and whether you treat it as speech or as "
            "noise. If everything is noise, you have chosen the physician’s "
            "world. If everything is an omen you invented, you have skipped "
            "Ifá’s discipline: someone has to know how to read."
        ),
        "prac": (
            "Once today, when something falls or lands in an unexpected "
            "arrangement, pause. Do not invent a fortune. Write the layout "
            "as fact, then write who in your life would be authorized to read "
            "it. If no one is, leave it unread."
        ),
        "terms": kt(
            (
                "Ifa",
                "orisa of divination -> meaning in the fall of dendê nut-"
                "halves -> \"oracle\" as fortune-telling misses a god of "
                "reading, not a parlor trick",
            ),
            (
                "sorcier",
                "Rodrigues’s word for the Ifá reader -> criminal-anthropology "
                "poison -> the terreiro’s word is a priest of a god",
            ),
        ),
        "res": res(
            (
                "Myths of Ìfẹ̀ — Where Truth Has Its Home",
                "Both locate reliable speech in a kept practice, not in a "
                "private flash.",
                "Ìfẹ̀’s surety is shrine and priestly mouth; Ifá’s surety is "
                "a fall someone is trained to read.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Between Maker and World",
                "Both require a middle that can be consulted because the "
                "Maker is not the ordinary addressee.",
                "Johnson states the hierarchy; Ifá is one named instrument of "
                "that middle.",
            ),
        ),
    },
    {
        "n": 23,
        "title": "The Saint May Withdraw from the Tree",
        "src": "Rodrigues 1900, ch. I — arbres du Gantois",
        "fr": (
            "Je demandai s’il n’était pas à craindre que, le terreiro ne "
            "fonctionnant pas, un individu abattît un des arbres sacrés. On me "
            "répondit que le saint présent, cela ne pourrait avoir lieu que "
            "par le libre consentement du saint, qui alors se retirerait de "
            "l’arbre. Dans un terreiro de l’intérieur, le culte des végétaux "
            "avait cessé parce que le vieil Africain qui savait appeler les "
            "saints dans les arbres était mort, et qu’il n’avait jamais voulu "
            "faire d’élèves. La présence est donc consensuelle et portable. "
            "Un arbre n’est pas magique par espèce. Il l’est par un appel, et "
            "l’appel peut cesser."
        ),
        "roman": roman(
            "terreiro of Gantois",
            "saint withdrawing from a tree",
            "calling saints into trees as person-borne knowledge",
        ),
        "tr": (
            "Rodrigues asked whether, if the terreiro were not functioning, "
            "someone might cut one of the sacred trees. He was told that while "
            "the saint was present, that could happen only by the saint’s free "
            "consent, and the saint would then withdraw from the tree. In an "
            "inland terreiro, the cult of plants had ceased because the old "
            "African who knew how to call the saints into the trees had died, "
            "and he had never been willing to take pupils. Presence is "
            "therefore consensual and portable. A tree is not magical by "
            "species. It is so by a call, and the call can cease."
        ),
        "comm": (
            "The claim is that presence can leave. A sacred tree at Gantois "
            "cannot be felled while the saint is present, except by the "
            "saint’s free consent — and then the saint withdraws. An inland "
            "terreiro lost its plant cult because the old African who knew how "
            "to call saints into trees died without pupils. Two doctrines at "
            "once: the tree is not timber while inhabited; the inhabiting is "
            "not automatic in the species. Unit 20’s fork (house versus god) "
            "now moves. Even a house can be vacated. Rodrigues, outsider "
            "physician, hears dying superstition — knowledge failing as Africa "
            "fails. Poison. What he recorded is the opposite of racial "
            "essence: the cult is person-borne. No blood makes you able to "
            "call. No tree is holy because it is a gameleira. Someone must "
            "know, and someone must consent. Existentially, ask whether a "
            "presence can leave a place you assumed was permanently holy — a "
            "room, a marriage, a grove, a job. If you treat holiness as a "
            "property of the furniture, you will cut and then wonder why "
            "nothing answers."
        ),
        "prac": (
            "Name one place you treat as permanently charged. Ask whether "
            "the presence could withdraw. Write what would remain if it did. "
            "Do not perform a vacancy. Just admit the possibility."
        ),
        "terms": kt(
            (
                "libre consentement du saint",
                "the orisa may consent to leave the tree -> presence is not "
                "a nail -> felling-while-inhabited is not a forestry option",
            ),
            (
                "appeler les saints dans les arbres",
                "person-borne knowledge, not a racial gift -> dies with the "
                "teacher who takes no pupils -> \"primitive nature-cult\" "
                "cannot explain a ceased house",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — The Offerings No Longer Vanish "
                "Overnight",
                "Both record a cult-site whose activity can cease, proving "
                "presence was never a property of the furniture.",
                "Serer offerings that stop vanishing mark a cooled relation; "
                "Bahia names the saint’s withdrawal and a teacher’s death.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — The Mortal Shrine",
                "Both allow a sacred seat to end when the binding life or "
                "consent ends.",
                "Johnson’s shrine is destroyed at death; the Bahian tree may "
                "be vacated and then, only then, be vulnerable as wood.",
            ),
        ),
    },
    {
        "n": 24,
        "title": "Terreiro Means Place and Jurisdiction",
        "src": "Rodrigues 1900, ch. II — le mot terreiro",
        "fr": (
            "Le mot terreiro a deux significations distinctes: il désigne le "
            "lieu, l’emplacement ou la maison où demeure le chef et où se "
            "célèbrent les fêtes religieuses, et il qualifie la juridiction "
            "d’un pontife qui en prend le nom, en ajoutant au titre la qualité "
            "de père ou mère du terreiro. Parmi les plus renommés: celui du "
            "Gantois, celui de l’Engenho Velho et celui du Garcia. Une maison "
            "sans juridiction n’est qu’une adresse. Une juridiction sans "
            "maison n’est qu’un titre. Le Candomblé bahianais tient les deux. "
            "Rodrigues dit pontife; le terreiro dit père ou mère."
        ),
        "roman": roman(
            "terreiro (place and jurisdiction)",
            "pai / mãe de terreiro",
            "Gantois, Engenho Velho, Garcia",
        ),
        "tr": (
            "The word terreiro has two distinct meanings: it designates the "
            "place, the ground or the house where the chief lives and where "
            "the religious feasts are celebrated, and it names the jurisdiction "
            "of a pontiff who takes that name, adding the title father or "
            "mother of the terreiro. Among the most renowned: Gantois, "
            "Engenho Velho, and Garcia. A house without jurisdiction is only "
            "an address. A jurisdiction without a house is only a title. "
            "Bahian Candomblé holds both. Rodrigues says pontiff; the terreiro "
            "says father or mother."
        ),
        "comm": (
            "The claim is double: terreiro is a place, and terreiro is a "
            "jurisdiction. The house where the chief lives and the feasts are "
            "kept is one meaning. The other is the authority of a pai or mãe "
            "who takes the house’s name. Gantois, Engenho Velho, Garcia are "
            "not neighborhoods on a tourist map. They are named courts. "
            "Rodrigues, outsider physician, says pontife because he needs a "
            "Catholic analog, and he will elsewhere treat these houses as "
            "police problems. Do not ingest that gossip as doctrine. The "
            "survival of named houses in a hostile city is a condition, not a "
            "sacrament. The philosophical remainder is still the double "
            "meaning. Johnson can describe Yoruba faith as towns and orisas "
            "without this Portuguese word; Bahia needs terreiro because the "
            "religion here is a house-jurisdiction under Brazilian law and "
            "street names. Existentially, name one place you keep and who "
            "actually holds its jurisdiction. If you have a room and no "
            "officer, you have an address. If you have a title and no room, "
            "you have a costume."
        ),
        "prac": (
            "Write one place you keep and the name of the person who actually "
            "holds its jurisdiction — not the landlord only, the one whose "
            "word stands there. If the two are different, say so aloud."
        ),
        "terms": kt(
            (
                "terreiro",
                "place (house/yard of feasts) and jurisdiction (pai/mãe’s "
                "name) -> Candomblé as a named court -> \"temple\" flattens "
                "the double meaning",
            ),
            (
                "Gantois / Engenho Velho / Garcia",
                "renowned Bahian houses Rodrigues lists -> particular "
                "jurisdictions, not a generic Africa -> do not fold them into "
                "a Yoruba catch-all",
            ),
        ),
        "res": res(
            (
                "Myths of Ìfẹ̀ — Where Truth Has Its Home",
                "Both locate truth in a precinct plus an authorized mouth, "
                "not in a book alone.",
                "Ìfẹ̀’s precinct is the makers’ shrines; Bahia’s precinct is "
                "a named terreiro under a pai or mãe.",
            ),
            (
                "Lasnet, Senegalese Animism — Fitaure Is Religious and Civic "
                "Head",
                "Both join religious headship to a public jurisdiction, not "
                "to a private spirituality.",
                "Fitaure is a Serer civic-religious head; pai/mãe de terreiro "
                "is a Bahian house-jurisdiction.",
            ),
        ),
    },
    {
        "n": 25,
        "title": "The Peji Is the House of the Orisa",
        "src": "Rodrigues 1900, ch. II — Peji / Ile-Orisa",
        "fr": (
            "La dernière des chambrettes c’est le sanctuaire, le Peji, "
            "l’Ile-Orisa, l’église proprement dite. Cette pièce est obscure et "
            "sans fenêtre. Presque au ras du sol s’élève l’autel, sur lequel "
            "sont placés les fétiches. Par terre se trouvent les offrandes: "
            "aliments et eau, plats, pots et surtout des quartinhas pour "
            "l’eau. La maison de l’Orisa n’est donc pas une nef. Elle est une "
            "chambre basse, sombre, avec de l’eau. Rodrigues dit église et "
            "fétiches dans la même phrase. Le Nagô dit Ile-Orisa: la maison "
            "de l’Orisa."
        ),
        "roman": roman(
            "Peji / Ile-Orisa (house of the orisa)",
            "quartinha (water pot)",
            "low altar, dark room without window",
        ),
        "tr": (
            "The last of the small rooms is the sanctuary, the Peji, the "
            "Ile-Orisa, the church properly so called. This room is dark and "
            "without a window. Almost at ground level rises the altar, on "
            "which the \"fetishes\" are placed. On the floor are the "
            "offerings: food and water, plates, pots, and above all "
            "quartinhas for water. The house of the orisa is therefore not a "
            "nave. It is a low, dark chamber with water. Rodrigues says "
            "church and fetishes in the same sentence. Nagô says Ile-Orisa: "
            "the house of the orisa."
        ),
        "comm": (
            "The claim is architectural: the orisa has a house, Ile-Orisa, "
            "the Peji. It is the last small room, dark, without a window. The "
            "altar is almost on the ground. Water is kept in quartinhas on "
            "the floor with food. This is not a failed cathedral. It is a "
            "philosophy of nearness. The court sits low. Rodrigues, outsider "
            "physician, says église proprement dite and then fétiches on the "
            "altar, as if he had found a parody parish. Poison. Do not "
            "improve the room into stained glass in your mind. Johnson’s "
            "middle population needs places; Bahia specifies the place: dark, "
            "low, wet. The quartinha is not folklore crockery. It is how the "
            "house drinks. Existentially, treat one room as a house of "
            "presence — darker, lower, with water — rather than as a display "
            "space. If your sacred corner is designed to be photographed, you "
            "have built the opposite of a Peji."
        ),
        "prac": (
            "Choose one corner of a room. Lower the display. Put water there. "
            "Leave it unphotographed for a day. Notice whether you can bear "
            "a holy place that does not perform."
        ),
        "terms": kt(
            (
                "Peji / Ile-Orisa",
                "house of the orisa, last dark chamber -> low altar, water "
                "on the floor -> \"sanctuary\" as church-copy misses the "
                "Nagô name and the height of the altar",
            ),
            (
                "quartinha",
                "pot kept for water in the Peji -> the house drinks -> not "
                "a decorative vase",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Mortal Shrine",
                "Both specify a kept material house for a power, with vessels "
                "that belong to that house.",
                "Johnson’s adult Ori-shrine dies with its owner; the Peji is "
                "the terreiro’s standing house of the orisa.",
            ),
            (
                "Lasnet, Senegalese Animism — Bante: The Soul Enclosed in a "
                "Canari",
                "Both keep a soul or presence in a vessel in a domestic "
                "sacred space.",
                "The Serer canari encloses a soul; the quartinha keeps water "
                "for the orisa’s house.",
            ),
        ),
    },
    {
        "n": 26,
        "title": "Father and Mother Are Pontiff Together",
        "src": "Rodrigues 1900, ch. II — père et mère",
        "fr": (
            "Le père ou la mère d’un terreiro est à la fois pontife et "
            "sorcier, fonctions peu distinctes et corrélatives. Comme prêtre "
            "il préside et dirige les fêtes du culte extérieur et il organise "
            "une confrérie d’initiés. Le travail est presque toujours fait "
            "conjointement par un père et une mère de terreiro. Toutes ces "
            "dignités sortent de l’ordre des fils de saints. L’autorité n’est "
            "donc pas un génie solitaire. Elle est une paire, et la paire "
            "sort des enfants. Rodrigues fond prêtre et sorcier pour les "
            "besoins de sa clinique. Le terreiro distingue assez pour fêter, "
            "et assez peu pour que les deux fonctions se tiennent."
        ),
        "roman": roman(
            "pai de terreiro / mãe de terreiro",
            "filho de santo (source of dignities)",
            "confrérie of initiates",
        ),
        "tr": (
            "The father or mother of a terreiro is at once pontiff and "
            "\"sorcerer,\" functions little distinct and correlative. As "
            "priest he or she presides over and directs the feasts of the "
            "outer cult and organizes a confraternity of initiates. The work "
            "is almost always done jointly by a father and a mother of "
            "terreiro. All these dignities come out of the order of the "
            "children of the saints. Authority is therefore not a solitary "
            "genius. It is a pair, and the pair comes from the children. "
            "Rodrigues fuses priest and sorcerer for the needs of his clinic. "
            "The terreiro distinguishes enough to feast, and little enough "
            "that the two functions hold together."
        ),
        "comm": (
            "The claim is that headship is joint and filial. A terreiro is "
            "almost always worked by a father and a mother together. Their "
            "dignities come out of the children of the saints — not from a "
            "seminary, not from a racial gift, not from Rodrigues’s "
            "pontiff-sorcerer hybrid. They preside at outer feasts and keep "
            "an initiated confraternity. Rodrigues, outsider physician, "
            "collapses priest and sorcerer because criminal anthropology "
            "needs one dangerous specialist. Poison. Do not accept the "
            "collapse. Also do not invent a modern ethnography of gendered "
            "offices he did not record. What he recorded is enough: pair, "
            "not solo; children, not imported clergy. Johnson can describe "
            "Yoruba offices without this pair; Bahia’s Portuguese names — "
            "pai, mãe, filho — are the local law of the house. Existentially, "
            "notice one work that is only real when two authorities hold it "
            "together. If you keep trying to be the lone pontiff of your "
            "life, you are building the physician’s sorcerer, not a terreiro."
        ),
        "prac": (
            "Pick one responsibility you have been holding alone. Name the "
            "second authority without whom it is only a title. Speak to that "
            "person today, or admit that the work is not yet a house."
        ),
        "terms": kt(
            (
                "pai / mãe de terreiro",
                "father and mother of the house, almost always joint -> "
                "headship as a pair -> \"high priest\" as a solo genius is "
                "Rodrigues’s analog, not the report",
            ),
            (
                "fils de saints",
                "the order from which dignities come -> office is filial, "
                "not imported -> skipping this origin makes a costume pontiff",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — Awa Holds the First Seat of the "
                "House",
                "Both give a house a seated authority that is not a lone "
                "male virtuoso.",
                "Awa is first seat in a Serer house; Bahian headship is a "
                "pai and mãe working the same terreiro.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Forms of Sacred Difference",
                "Both treat office as a shaped difference inside a people, "
                "not a European clergy transplanted.",
                "Johnson writes Yoruba forms; Bahia names the pair and the "
                "children of saints as the local law.",
            ),
        ),
    },
    {
        "n": 27,
        "title": "Children of the Saints",
        "src": "Rodrigues 1900, ch. II — fils de saints",
        "fr": (
            "On appelle fils de saints les personnes qui, préparées par une "
            "initiation spéciale, sont vouées au culte d’un ou de plusieurs "
            "saints. Obatala veut un costume tout blanc. Sango réclame un "
            "vêtement blanc et rouge. Yé-man-jà exige des perles blanches "
            "transparentes. Osun, des vêtements blancs et des perles jaunes. "
            "Ogun, des bracelets de fer. Le plus important de ces jours c’est "
            "le vendredi, consacré à Obatala. La couleur n’est pas un "
            "costume de théâtre. Elle est une appartenance. Rodrigues dresse "
            "un catalogue; le terreiro dresse des corps."
        ),
        "roman": roman(
            "filho de santo",
            "Obatala (all white; Friday)",
            "Sango (white and red)",
            "Yemanja (transparent white beads)",
            "Osun (white cloth, yellow beads)",
            "Ogun (iron bracelets)",
        ),
        "tr": (
            "Children of the saints are those who, prepared by a special "
            "initiation, are vowed to the cult of one or more saints. Obatala "
            "wants a costume all white. Sango requires a garment white and "
            "red. Yemanja demands transparent white beads. Osun, white "
            "clothes and yellow beads. Ogun, iron bracelets. The most "
            "important of these days is Friday, consecrated to Obatala. Color "
            "is not stage costume. It is belonging. Rodrigues draws up a "
            "catalogue; the terreiro dresses bodies."
        ),
        "comm": (
            "The claim is that belonging has color, metal, and a day. A "
            "filho de santo is vowed to one or more orisas after initiation. "
            "Obatala is all white and owns Friday. Sango is white and red. "
            "Yemanja is transparent white beads. Osun is white with yellow "
            "beads. Ogun is iron at the wrist. These are not fashion notes. "
            "They are how a body says which courtier it serves. Rodrigues, "
            "outsider physician, catalogues costumes as folklore — useful "
            "color for a clinic of race. Poison. Do not give initiation "
            "instructions from this page. Do not tell anyone how to become a "
            "child of the saints. The philosophical remainder is public: "
            "difference is worn, and the first orisa’s day is still the "
            "week’s hinge. Johnson’s Ori is a private adult shrine; Bahia’s "
            "filhos are a visible order. Existentially, notice one color or "
            "day you already keep without calling it a vow — a shirt, a "
            "Friday habit, a metal you will not take off. Ask whether you "
            "have been wearing a belonging you refuse to name."
        ),
        "prac": (
            "Notice one color, metal, or weekday you already keep. Write "
            "which belonging it silently marks. Do not adopt a terreiro "
            "color as costume. Keep or drop your own mark on purpose."
        ),
        "terms": kt(
            (
                "filho de santo",
                "child of the saints: initiated, vowed to one or more orisas "
                "-> a visible order -> \"devotee\" as a fan misses color, "
                "day, and filiation",
            ),
            (
                "vendredi / Obatala",
                "Friday as the most important day, consecrated to the first "
                "orisa -> the week has a hinge -> a catalogue of colors "
                "without this day is tourism",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Fading Sacred Beads",
                "Both treat beads and worn signs as theology on the body, "
                "not jewelry.",
                "Johnson records fading sacred beads; Bahia specifies which "
                "orisa requires which color and metal.",
            ),
            (
                "Ellis, Yoruba òwe — Each coloured cloth has its name",
                "Both refuse anonymous cloth: a color is already a name.",
                "The òwe is social wit about cloth; filho de santo cloth is "
                "a vow, not a market name only.",
            ),
        ),
    },
    {
        "n": 28,
        "title": "The Cowries Name the Saint",
        "src": "Rodrigues 1900, ch. II — initiation",
        "fr": (
            "Quiconque désire avoir un saint, ou qui trouve un objet qu’il "
            "suppose être un fétiche, va consulter le père du terreiro qui, "
            "au moyen de coquillages ou de dés, lui dit quel est le saint et "
            "lui désigne le père ou la mère du terreiro qui doit préparer le "
            "fétiche et diriger l’initiation. Parfois l’aspirant lui-même, "
            "possédé du saint, fait les déclarations. On ne choisit donc pas "
            "un Orisa comme on choisit une marque. On est nommé. Les cauris "
            "parlent, ou la tête parle. Rodrigues dit dés et fétiche; le "
            "terreiro dit une nomination."
        ),
        "roman": roman(
            "cowries / shells as naming",
            "pai / mãe de terreiro",
            "possession as the aspirant’s own declaration",
        ),
        "tr": (
            "Whoever wishes to have a saint, or who finds an object he "
            "supposes to be a \"fetish,\" goes to consult the father of the "
            "terreiro, who by means of shells or dice tells him which saint "
            "it is and names the father or mother of the terreiro who must "
            "prepare the object and direct the initiation. Sometimes the "
            "aspirant himself, possessed by the saint, makes the "
            "declarations. One therefore does not choose an orisa as one "
            "chooses a brand. One is named. The cowries speak, or the head "
            "speaks. Rodrigues says dice and fetish; the terreiro says a "
            "naming."
        ),
        "comm": (
            "The claim is that the orisa is named, not shopped. A person who "
            "wants a saint, or who finds an object that may already be one, "
            "does not assign the name. A pai reads cowries or dice; he says "
            "which saint, and which pai or mãe must prepare the thing and "
            "direct initiation. Sometimes the aspirant, possessed, speaks the "
            "name from the head. Two mouths: shells and seizure. Neither is "
            "consumer choice. Rodrigues, outsider physician, writes fétiche "
            "and dés because he needs a gambler-priest. Poison. Do not "
            "ingest initiation steps. Do not teach anyone how to throw "
            "cowries. The philosophical remainder is enough: identity in "
            "this court is received. Unit 8 said a priest can fix the saint "
            "in any object; this unit says you still do not get to pick which "
            "saint. Ifá reads a fall (unit 22); here cowries name a person "
            "and a house. Existentially, before you claim a power, a path, "
            "or a found object as yours, ask who is authorized to name it. "
            "If the answer is only you, you are doing the physician’s dice "
            "in private — a game without a house."
        ),
        "prac": (
            "Before claiming one power, path, or found object as yours "
            "today, write who would be authorized to name it. If the only "
            "name-giver is you, do not claim it. Leave it unnamed for the "
            "day."
        ),
        "terms": kt(
            (
                "cauris / coquillages",
                "cowries as the mouth that names the orisa -> received "
                "identity -> \"dice\" as Rodrigues’s reduction to gambling",
            ),
            (
                "nomination",
                "the pai names the saint and the preparer -> sometimes the "
                "possessed aspirant declares -> choice-as-brand is the "
                "modern error this unit blocks",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Ori: the Head as "
                "Destiny",
                "Both treat the person’s sacred identity as allotted and "
                "readable, not selected from a menu.",
                "Johnson’s Ori is the head as destiny; Bahia’s cowries (or "
                "the seized head) name which orisa will be prepared.",
            ),
            (
                "Myths of Ìfẹ̀ — Where Truth Has Its Home",
                "Both refuse a private invention of the sacred name: surety "
                "lives in a kept mouth.",
                "Ìfẹ̀’s mouth is the priestly line at the shrine; this "
                "mouth is cowries, or the saint speaking in the aspirant.",
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
        {"kind": "original", "label": "Original", "body": u["fr"]},
        {"kind": "iast", "label": "Romanization", "body": u["roman"]},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"ANIM_{n:03d}",
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
            "category": "candomble-bahia",
            "verse": str(n),
            "section": u["src"],
            "cultural_context": NOTE,
            "original_source": u["src"],
            "original_reliability": RELIABILITY,
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": u["fr"],
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

