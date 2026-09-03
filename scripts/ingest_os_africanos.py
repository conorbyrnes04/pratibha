#!/usr/bin/env python3
"""Ingest Raimundo Nina Rodrigues, *Os Africanos no Brasil*.

Written c. 1890–1905; first published posthumously São Paulo: Companhia
Editora Nacional, 1932 (IA scan labeled 1935). Author died 1906; public
domain in Brazil (life+70). Homero Pires preface/revision is NOT Original.
Do not use Cap. VIII (racial ranking) or Cap. IX (criminality) as teaching.
Edelstein 2010 SciELO is a diplomatic of Rodrigues’s Portuguese — used to
clean Originals. IA OCR is backup.

English is a Pratibha rendering (pd_adapted). Original layer is cleaned
Rodrigues Portuguese.

Sibling to *O Animismo Fetichista* (liturgy). This book is the historical
conditions through which Nagô, Jeje, Bantu, and Malê (Islam) practices took
root in Brazil. Rodrigues was a physician and racial theorist; the book is
carregada de preconceito. Restore nations, language, Malê prayer, Gêge-Nagô
cult, and police survival — not his hierarchy, not “fetish” as doctrine,
not criminal anthropology.

Floor: ≥28 units. Ten tts_key heroes.
"""
from __future__ import annotations

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/os_africanos_no_brasil")
SLUG = "os_africanos_no_brasil"
COLL = "Os Africanos no Brasil"
THEMES = ["candomble", "nago", "jeje", "male", "bahia"]
ROMAN = (
    "Rodrigues Portuguese of Afro-Brazilian observation "
    "(written c. 1905, pub. 1932)"
)

PROV = (
    "English is a Pratibha rendering (pd_adapted) from Raimundo Nina Rodrigues, "
    "*Os Africanos no Brasil* (written c. 1890–1905; first published São Paulo: "
    "Companhia Editora Nacional, 1932), public domain in Brazil (author d. 1906). "
    "Original layer is cleaned Rodrigues Portuguese. Does not follow Homero "
    "Pires’s preface or later editors."
)
NOTE = (
    "Historical conditions through which Nagô, Jeje, Bantu, and Malê (Islam) "
    "practices took root in Brazil. Sibling to *O Animismo Fetichista* "
    "(liturgy). Rodrigues was a physician and racial theorist; the book is "
    "carregada de preconceito. Restore nations, language, Malê prayer, "
    "Gêge-Nagô cult, and police survival — not his hierarchy, not \"fetish\" "
    "as doctrine, not criminal anthropology. Study reading pending review by "
    "Candomblé and Malê tradition-bearers."
)
RELIABILITY = (
    "SOURCED — Rodrigues Portuguese (posthumous 1932); Edelstein 2010 "
    "diplomatic of that text. Not Homero Pires preface. Not Cap. VIII/IX as "
    "doctrine."
)

# Ten hero verses — mandala quotes + pre-baked Listen.
HEROES = {1, 3, 4, 6, 11, 12, 17, 20, 24, 28}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


def roman(*terms: str) -> str:
    return f"{ROMAN}. Key terms: {'; '.join(terms)}."


UNITS: list[dict] = [
    {
        "n": 1,
        "title": "Nations Are Not One Gloss",
        "src": "Rodrigues, Os Africanos, cap. I",
        "pt": (
            "As designações populares de Nagô, Mina, Angola, Moçambique, etc., "
            "conservam, para o vulgo como para o letrado, o rigoroso valor "
            "sinonímico de Negro da Costa, ou Africano. Ora, antes de tudo, "
            "bem longe está da realidade a uniformidade étnica aparente que "
            "dá ao homem africano o seu negro verniz pigmentário."
        ),
        "roman": roman(
            "Nagô",
            "Mina",
            "Angola",
            "Moçambique",
            "Negro da Costa (period gloss, not a nation)",
        ),
        "tr": (
            "The popular designations Nagô, Mina, Angola, Mozambique, and the "
            "rest keep, for the crowd as for the lettered, the strict "
            "synonym-value of Negro da Costa, or African. Yet first of all, "
            "the apparent ethnic uniformity that the African person’s black "
            "pigmentary varnish is supposed to give is far from the reality."
        ),
        "comm": (
            "The claim the street still lives is that Nagô, Mina, Angola, and "
            "Mozambique are not one people painted black. Popular speech and "
            "learned speech both collapse those names into Negro da Costa or "
            "African, as if the coast were a single nation and pigment a "
            "single origin. That collapse is the first violence the book "
            "records, and it is still the first violence a reader can repeat. "
            "Rodrigues, a Bahian physician and racial theorist, writes the "
            "correction while keeping the poison: he denies ethnic uniformity "
            "and then points at a negro verniz pigmentário, a Black pigmentary "
            "varnish, as if the body were a coating over a type. The book is "
            "carregada de preconceito. Do not launder the ladder that will "
            "later rank nations, score intelligence, and dump Cap. VIII and "
            "IX into criminal anthropology. We do not teach those chapters as "
            "doctrine. The ethnographic remainder is the nation names "
            "themselves. Nagô is not Mina. Angola is not Mozambique. Bahia "
            "will show Sudanese weight, Jeje speech, Malê prayer, and "
            "Gêge-Nagô cult — not a continent-sized fetish. Johnson writes "
            "Yoruba faith from inside one nation; Lasnet writes Serer life "
            "from another. Neither will sit still under African as a gloss. "
            "Existentially, you refuse the one word that lets you stop "
            "learning the second."
        ),
        "prac": (
            "Today, catch one sentence in which you used African, Black, or "
            "the coast as if it named a single people. Replace it with the "
            "nation, language, or house you actually mean. If you do not "
            "know the second word, write that ignorance down instead of the "
            "gloss."
        ),
        "terms": kt(
            (
                "Nagô",
                "Bahian name for the Yoruba nation -> a people with language "
                "and orisha cult, not a skin-tone synonym -> folding Nagô "
                "into Negro da Costa erases the first nation this book can "
                "still teach",
            ),
            (
                "Negro da Costa",
                "period Brazilian gloss for a person from the African coast "
                "-> a market and police category, not an ethnicity -> "
                "keeping it as doctrine adopts the vulgar synonym Rodrigues "
                "himself says is false",
            ),
            (
                "verniz pigmentário",
                "pigmentary varnish -> Rodrigues’s racial image for Black "
                "skin as a coating that fakes unity -> the poison to name "
                "and refuse, even when the sentence correctly denies one "
                "African ethnicity",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Only One God in the "
                "Universe",
                "Both open by refusing a single African religion in Bahia "
                "and naming Nagô as a specific house.",
                "Animismo starts from Olorun’s court; this book starts from "
                "nation names the street has already flattened.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — One God, Many Towns",
                "Both keep Yoruba life from collapsing into one tribal "
                "label: towns and nations differ inside a shared highest "
                "name.",
                "Johnson writes from inside Yoruba towns; Rodrigues writes "
                "as a Bahian physician listing captive nations under a "
                "racial varnish he will not drop.",
            ),
        ),
    },
    {
        "n": 2,
        "title": "Bahia Was Sudanese",
        "src": "Rodrigues, Os Africanos, cap. I",
        "pt": (
            "A crença que domina os cientistas pátrios é que foram Bantus os "
            "povos negros que colonizaram o Brasil. No erro deste exclusivismo "
            "incidem etnólogos, historiadores e literatos. Os primeiros "
            "[sudaneses] predominaram na Bahia."
        ),
        "roman": roman(
            "sudaneses (West African / Sudanic nations in the old sense)",
            "Bantus",
            "Bahia",
        ),
        "tr": (
            "The belief that dominates the country’s scientists is that the "
            "Black peoples who settled Brazil were Bantu. Ethnologists, "
            "historians, and men of letters fall into the error of that "
            "exclusivism. The first group — the Sudanese — predominated in "
            "Bahia."
        ),
        "comm": (
            "The historical claim is a map, not a compliment: Bahia’s African "
            "majority was Sudanese in the old ethnographic sense — Yoruba/"
            "Nagô, Jeje/Ewe, Hausa, Tapa, and their neighbors — not "
            "exclusively Bantu. Brazilian science had already decided the "
            "country was Bantu-colonized, and the exclusivism flattened the "
            "city that would hold Gêge-Nagô terreiros and Malê houses. "
            "Rodrigues, racial theorist, writes the correction inside a "
            "poisoned verb. Colonizaram o Brasil treats captive nations as "
            "colonists and keeps the scientist’s right to sort stocks. Do "
            "not take Sudanese versus Bantu as a ranking of intelligence or "
            "religion. Cap. VIII’s ladder is out of the classroom. The "
            "ethnographic remainder is regional: what took root in Bahia is "
            "not what took root everywhere in Brazil. Nagô speech, Jeje "
            "titles, and Malê Arabic are Sudanese facts of this city. Bantu "
            "life is not therefore empty or \"monotheist by default\" — a "
            "later unit will refuse that smear. Johnson’s Yoruba faith is "
            "one Sudanese stream written from the inside; Ellis’s òwe keep "
            "Yoruba as a speaking people, not a Bantu footnote. "
            "Existentially, you correct the inherited map before you speak "
            "of African Brazil as one block. If your picture of the country "
            "has only one African family, you are still in the exclusivism "
            "the sentence names."
        ),
        "prac": (
            "Today, name the African nation you silently assume when someone "
            "says Bahia or Brazil. Write a second nation that the assumption "
            "erased. If you cannot, the exclusivism is still yours."
        ),
        "terms": kt(
            (
                "sudaneses",
                "nineteenth-century label for West African / Sudanic nations "
                "(Nagô, Jeje, Hausa, Tapa) -> Bahia’s predominant African "
                "presence -> not a racial grade above Bantu, and not a "
                "synonym for all of Brazil",
            ),
            (
                "Bantus",
                "Central and Southern African nations present in Brazil -> "
                "the exclusivist default of Brazilian science in Rodrigues’s "
                "day -> denying their monopoly in Bahia is not a denial of "
                "Bantu religion elsewhere",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Only One God in the "
                "Universe",
                "Both locate Bahia’s public African religion in a Yoruba/"
                "Nagô-weighted field rather than a generic Black Brazil.",
                "Animismo reports the terreiro’s court; this unit reports "
                "the demographic error that hid that court from scientists.",
            ),
            (
                "Ellis, Yoruba òwe — Another's eye is not like one's own",
                "Both refuse a single vantage: what one observer sees as "
                "the whole people is another people’s blind spot.",
                "The òwe is a proverb about persons; this sentence is a "
                "correction of a national scientific myth.",
            ),
        ),
    },
    {
        "n": 3,
        "title": "They Rebuilt Belief in Hidden Speech",
        "src": "Rodrigues, Os Africanos, cap. II",
        "pt": (
            "Por sob a ignorância e brutalidades dos senhores brancos "
            "reataram-se os laços dos imigrados, sob o duro regime do "
            "cativeiro reconstruíram, como puderam, as práticas, os usos e as "
            "crenças da pátria longínqua. O comércio continuado com a Costa "
            "d’África ia-os instruindo dos sucessos guerreiros e religiosos "
            "que por lá se desenrolavam."
        ),
        "roman": roman(
            "cativeiro (captivity / slavery)",
            "Costa d’África",
            "práticas, usos, crenças",
        ),
        "tr": (
            "Under the ignorance and brutalities of the white masters the "
            "bonds of the immigrants were retied; under the hard regime of "
            "captivity they rebuilt, as they could, the practices, the "
            "customs, and the beliefs of the distant homeland. Continued "
            "trade with the African coast kept instructing them in the "
            "warrior and religious events unfolding over there."
        ),
        "comm": (
            "The religious-historical claim is reconstruction under captivity: "
            "people torn from home retied their bonds and rebuilt practice, "
            "custom, and belief in a language the masters did not know. The "
            "Atlantic did not only take. Trade with the Costa d’África kept "
            "instructing the city in wars and rites still happening on the "
            "other shore. Candomblé and Malê Islam are not folk leftovers "
            "invented from scraps; they are rebuilt houses with a live "
            "supply line. Rodrigues, physician of a slave society, reports "
            "the fact while leaving white brutality as scenery and the "
            "rebuilders as ethnographic stock. That is the poison: he can "
            "see the reconstruction and still rank the reconstructors. Do "
            "not romanticize the trade as free cultural exchange. Do not "
            "treat the rebuilt rite as a degeneration of an African original "
            "the scientist owns. The ethnographic remainder is the method: "
            "language the owner cannot police, ships that still talk, "
            "practices rebuilt as they could — not as a museum would prefer. "
            "Ìfẹ̀ locates truth in priests’ mouths at the shrine; Bahia "
            "locates survival in mouths the plantation could not translate. "
            "Existentially, you notice a language you do not speak carrying "
            "a rite, and you stop calling that silence emptiness. What you "
            "cannot overhear is not therefore dead."
        ),
        "prac": (
            "Today, notice one language you do not speak that is carrying a "
            "rite, a song, or a prayer near you. Do not translate it. Write "
            "only that it is being kept without you."
        ),
        "terms": kt(
            (
                "cativeiro",
                "captivity / the slave regime -> the condition under which "
                "practices were rebuilt, not the origin of the practices -> "
                "\"slavery invented Candomblé\" misses the homeland already "
                "being reconstructed",
            ),
            (
                "Costa d’África",
                "the African coast as a live trading and news shore -> "
                "instruction continued after capture -> treating Brazil as "
                "cut off from Africa adopts the master’s ignorance as "
                "history",
            ),
        ),
        "res": res(
            (
                "Myths of Ìfẹ̀ — Where Truth Has Its Home",
                "Both place surety in a kept speech the outsider does not "
                "own: shrine mouths there, rebuilt homeland speech here.",
                "Ìfẹ̀’s recitation is priestly and seated; Bahia’s "
                "reconstruction happens under the whip and by coastal trade.",
            ),
            (
                "Lasnet, Senegalese Animism — One Does Not Leave Ancestral "
                "Land Voluntarily",
                "Both treat departure from homeland as a wound that does "
                "not cancel the cult of origin.",
                "Serer refusal is not to leave; this unit is what people "
                "did after they were taken.",
            ),
        ),
    },
    {
        "n": 4,
        "title": "Islam Organized in Captivity",
        "src": "Rodrigues, Os Africanos, cap. II",
        "pt": (
            "O Islamismo organizou-se em seita poderosa; vieram os mestres "
            "que pregavam a conversão e ensinavam a ler no árabe os livros "
            "do Alcorão, que também de lá vinham importados."
        ),
        "roman": roman(
            "Islamismo / Malê",
            "Alcorão",
            "árabe",
            "mestres (alufá / teachers)",
        ),
        "tr": (
            "Islam organized itself as a powerful community; teachers came "
            "who preached conversion and taught reading, in Arabic, the "
            "books of the Qur’an, which were also imported from there."
        ),
        "comm": (
            "The claim is institutional, not folkloric: Islam organized in "
            "captivity. Teachers preached conversion, taught Arabic literacy, "
            "and imported Qur’ans from Africa. Malê life in Bahia is a "
            "school and a mosque, not a rumor of \"Mohammedan Negroes.\" "
            "Rodrigues writes seita poderosa — a powerful sect — the "
            "physician’s word for a religion he will later feed into police "
            "panic and, in chapters we refuse as doctrine, into criminal "
            "anthropology. That is the poison. A sect is what you call a "
            "church you intend to rank. Do not teach 1835 as proof that "
            "Islam in Bahia was only revolt. Do not treat Arabic books as "
            "contraband metaphysics. The ethnographic remainder is the "
            "import and the lesson: the book came from there; the reading "
            "was taught here; the conversion was preached among people the "
            "city had classified as cargo. Johnson’s reserved name for God "
            "is Yoruba theology; Malê Bahia’s reserved book is Arabic. Both "
            "are organized address to a highest that is not a terreiro "
            "orisa. Lasnet’s Serer highest is named as the sky and not "
            "bargained with as an object; the Qur’an is a different "
            "discipline of the same refusal to make God a figurine. "
            "Existentially, you stop treating a captive religion as leftover "
            "magic. If a people can import a book and teach its letters "
            "under slavery, the religion is not a fragment. It is a house."
        ),
        "prac": (
            "Today, name one book you assumed could not have been taught "
            "under captivity or poverty. Write who would have had to carry "
            "it, and who would have had to teach the letters. Do not call "
            "that house a sect."
        ),
        "terms": kt(
            (
                "Malê",
                "Bahian name for African Muslims (often Nagô, Hausa, Tapa) "
                "-> Islam with Arabic literacy in captivity -> default "
                "\"slave revolt\" or \"sect\" hides the school and the "
                "imported Qur’an",
            ),
            (
                "Alcorão",
                "the Qur’an, imported and taught in Arabic -> the book of "
                "the house, not a fetish paper -> police files that call "
                "prayers \"papers\" adopt the raid as the description",
            ),
            (
                "seita",
                "Rodrigues’s \"sect\" for organized Islam -> racial-theory "
                "and police vocabulary -> the remainder is a community with "
                "teachers, conversion, and a book",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — The Name Reserved for "
                "God Alone",
                "Both protect a highest address that is not handled as a "
                "local figurine: reserved name there, imported Book here.",
                "Johnson legislates Yoruba naming; Malê Bahia organizes "
                "Arabic reading under captivity.",
            ),
            (
                "Lasnet, Senegalese Animism — The Invisible Master Is Named "
                "as the Sky",
                "Both keep the highest from being reduced to an object you "
                "can seize in a raid.",
                "Serer Rog shares the sky’s name without a mosque; Malê "
                "Bahia imports a Qur’an and teaches its letters.",
            ),
        ),
    },
    {
        "n": 5,
        "title": "The Houses Were Schools and Mosques",
        "src": "Rodrigues, Os Africanos, cap. II — 1835",
        "pt": (
            "Eram outras tantas escolas e igrejas maometanas: a casa dos "
            "nagôs libertos Belchior e Gaspar da Silva Cunha, na rua da "
            "Oração, onde pregava de mestre o alufá ou marabu Luis, Sanim "
            "na sua nação Tapa; a casa dos nagôs libertos Manuel Calafate e "
            "Aprígio; a casa do nagô Pacífico, Licutan entre os seus, nas "
            "lojas da casa de seu senhor, no Cruzeiro de São Francisco."
        ),
        "roman": roman(
            "alufá / marabu",
            "Sanim (Tapa nation)",
            "Licutan (Pacífico among his own)",
            "rua da Oração",
            "Cruzeiro de São Francisco",
        ),
        "tr": (
            "They were so many schools and Muslim churches: the house of "
            "the freed Nagô men Belchior and Gaspar da Silva Cunha, on Rua "
            "da Oração, where the alufá or marabout Luis preached as "
            "master — Sanim in his Tapa nation; the house of the freed Nagô "
            "men Manuel Calafate and Aprígio; the house of the Nagô "
            "Pacífico, Licutan among his own, in the shops of his master’s "
            "house at the Cruzeiro de São Francisco."
        ),
        "comm": (
            "The claim is an address book of Islam in Bahia: named houses, "
            "named freedmen, named teachers, named nations. Rua da Oração "
            "held a school where an alufá preached. Sanim is Tapa. Licutan "
            "is Pacífico among his own, teaching in the shops of a master’s "
            "house. These are mosques that look like rooms. Rodrigues lifts "
            "the list from the 1835 inquiry and keeps the police file’s "
            "appetite: houses as cells of a sect, names as a roster of "
            "danger. That is the poison. We do not teach the Malê revolt as "
            "the essence of the religion, and we do not turn this paragraph "
            "into a crime scene. The ethnographic remainder is the double "
            "name and the double use. A man is Pacífico in Portuguese and "
            "Licutan among his own. A shop is a shop and a mosque. A freed "
            "Nagô house is a school. Johnson’s many towns keep one God "
            "under different local names; these houses keep one Book under "
            "Nagô and Tapa mouths. Lasnet’s ancestral land is a cult you do "
            "not leave; these rooms are a cult rebuilt in someone else’s "
            "street grid. Existentially, you learn one house that taught a "
            "language the street did not, and you stop needing a minaret "
            "before you will admit a mosque. If the only church you can "
            "see is the one with a façade, you are still reading with the "
            "master’s eyes."
        ),
        "prac": (
            "Today, name one ordinary room — a shop, a kitchen, a rented "
            "house — that has served as a school or a place of prayer. "
            "Write the two names it has: the street name and the name used "
            "inside."
        ),
        "terms": kt(
            (
                "alufá",
                "Muslim teacher / imam in Bahian Malê speech (also marabu) "
                "-> the master who preaches and teaches letters -> \"witch "
                "doctor\" or \"sect leader\" is the police gloss",
            ),
            (
                "Licutan",
                "Pacífico’s name among his own -> the name the nation uses "
                "when Portuguese is the master’s tongue -> keeping only "
                "Pacífico adopts the baptismal record as the person",
            ),
            (
                "Tapa",
                "nation of Sanim (Nupe) -> Islam in Bahia is not only Nagô "
                "-> collapsing every alufá into Yoruba repeats the one-gloss "
                "error of cap. I",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — One God, Many Towns",
                "Both keep a single highest address housed under local "
                "names and rooms.",
                "Johnson’s towns are Yoruba polities; these houses are "
                "freedmen’s rooms and a master’s shop.",
            ),
            (
                "Nina Rodrigues, O Animismo Fetichista — Terreiro Means "
                "Place and Jurisdiction",
                "Both insist that a sacred house is a location with "
                "authority, not a vacant lot with rumors.",
                "The terreiro’s jurisdiction is orisha; these rooms’ "
                "jurisdiction is Arabic teaching and Malê prayer.",
            ),
        ),
    },
    {
        "n": 6,
        "title": "They Will Not Adore Wood",
        "src": "Rodrigues, Os Africanos, cap. II — Marcelina",
        "pt": (
            "Depõe a escrava Marcelina que os papéis achados são de reza dos "
            "malês, escritos e feitos pelos mestres que andam ensinando. Eles "
            "aborreciam, dizendo que ela ia à missa adorar pau, que está no "
            "altar, porque as imagens não são santos."
        ),
        "roman": roman(
            "reza dos malês",
            "mestres",
            "pau (wood on the altar)",
            "imagens / santos",
        ),
        "tr": (
            "The enslaved woman Marcelina deposes that the papers found are "
            "Malê prayers, written and made by the teachers who go about "
            "teaching. They abhorred it, saying she went to Mass to adore "
            "wood that stands on the altar, because the images are not "
            "saints."
        ),
        "comm": (
            "The theological claim is aniconic and exact: the papers are "
            "prayers, the teachers write them, and the images on a Catholic "
            "altar are wood, not saints. Malê Bahia refuses to adore pau. "
            "This is Islam’s old argument against the figurine, spoken in a "
            "slave inquiry. Rodrigues files Marcelina’s deposition as "
            "evidence and keeps the poison of the courtroom: an enslaved "
            "woman’s speech extracted, \"papers found,\" a religion made to "
            "testify against itself. Do not teach the raid as the meaning "
            "of the prayer. Do not treat her sentence as folklore about "
            "fanatics who hate Mass. The ethnographic remainder is the "
            "doctrine inside the deposition. Reza is writing. Mestres walk "
            "and teach. Images are not saints. Animismo will later show "
            "Catholic saints sitting with orishas in the terreiro; this "
            "house refuses the wood altogether. Both facts can be true in "
            "one city. Johnson reserves a name that must not be multiplied; "
            "Malê prayer reserves a God who must not be carved. "
            "Existentially, you catch idol or fetish in your mouth when you "
            "mean someone else’s prayer, and you ask whether you are "
            "defending a theology or defending a police inventory. The "
            "papers were prayers before they were exhibits."
        ),
        "prac": (
            "Today, catch idol, fetish, or wood in your mouth when you "
            "describe someone else’s altar. Replace the sneer with the "
            "name they use for what stands there. If you do not know the "
            "name, stop at that."
        ),
        "terms": kt(
            (
                "reza dos malês",
                "Malê prayer, written by teaching masters -> Arabic (or "
                "Arabic-script) devotion, not a spell-paper -> \"papers "
                "found\" is the raid’s name for a liturgy",
            ),
            (
                "pau",
                "wood on the altar -> Malê refusal of the image as God -> "
                "hearing only hatred of Catholicism misses aniconic "
                "theology",
            ),
            (
                "Marcelina",
                "enslaved deponent in the inquiry -> a voice the archive "
                "extracted -> do not make her the mascot of either the "
                "police or a later romance of resistance",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — The Figures Are "
                "Neither Fetish nor Idol",
                "Both refuse a cheap word for what stands on an altar: "
                "figures are not automatically idols; wood is not "
                "automatically a saint.",
                "Animismo defends orisha figures from the word fetish; "
                "Malê speech refuses the Catholic image as God.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — The Name Reserved for "
                "God Alone",
                "Both protect the highest from a multiplication that would "
                "let any object stand in.",
                "Johnson legislates a name; Marcelina reports a people who "
                "will not kneel to carved wood.",
            ),
        ),
    },
    {
        "n": 7,
        "title": "The Limamo Reads the Qur’an",
        "src": "Rodrigues, Os Africanos, cap. II",
        "pt": (
            "O atual Limamo é o nagô Luis, e a sede da igreja maometana, a "
            "sua residência no Barris, à rua Alegria n.º 3. Como ela não "
            "conhece o árabe e o Limamo não sabe ler nem escrever o "
            "português, existem na casa um Alcorão em árabe para o Limamo e "
            "uma versão portuguesa para sua mulher."
        ),
        "roman": roman(
            "Limamo (imam)",
            "Barris / rua Alegria n.º 3",
            "Alcorão em árabe",
            "versão portuguesa",
        ),
        "tr": (
            "The present Limamo is the Nagô Luis, and the seat of the "
            "Muslim church is his residence in the Barris, at Rua Alegria "
            "no. 3. Because she does not know Arabic and the Limamo cannot "
            "read or write Portuguese, the house holds a Qur’an in Arabic "
            "for the Limamo and a Portuguese version for his wife."
        ),
        "comm": (
            "The claim is a bilingual household of Islam: the imam is Nagô "
            "Luis; the mosque is his house on Rua Alegria; the Arabic "
            "Qur’an is his; the Portuguese version is his wife’s. Two "
            "literacies, one book, one address. This is not a deficit. It "
            "is how a religion lives when the city’s language is not the "
            "liturgical language. Rodrigues scores the gap as incapacity — "
            "he cannot write Portuguese; she does not know Arabic — the "
            "racial theorist’s habit of reading a divided competence as a "
            "lower type. Poison. Illiteracy in the master’s tongue is not "
            "ignorance of God. The ethnographic remainder is the pair of "
            "books on the table and the house that is the igreja. Johnson’s "
            "Yoruba faith keeps a reserved name; this house keeps a reserved "
            "script. Animismo’s terreiro is a jurisdiction with a peji; "
            "this mosque is a residence with a number. Existentially, you "
            "notice two languages in one house serving one book, and you "
            "stop treating the language you cannot read as the empty one. "
            "The highest thing in the room may be the page you are not "
            "trained to open."
        ),
        "prac": (
            "Today, sit with one book or prayer whose script you cannot "
            "read. Do not fetch a translation first. Write whose literacy "
            "the house is built around, and whose literacy it also made "
            "room for."
        ),
        "terms": kt(
            (
                "Limamo",
                "imam, here the Nagô Luis -> liturgical head of a house-"
                "mosque -> \"sect chief\" is the inquiry’s word",
            ),
            (
                "versão portuguesa",
                "Portuguese Qur’an for the wife -> a second literacy inside "
                "the same Islam -> treating only Arabic as \"real\" or only "
                "Portuguese as \"civilized\" repeats Rodrigues’s scoring",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Terreiro Means "
                "Place and Jurisdiction",
                "Both locate a religion in a house with an address, not in "
                "an abstract Africa.",
                "The terreiro’s jurisdiction is orisha; Rua Alegria 3 is a "
                "mosque whose liturgy is Arabic.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — The Name Reserved for "
                "God Alone",
                "Both keep a highest speech that is not the street’s "
                "ordinary tongue.",
                "Johnson reserves a spoken name; the Limamo reserves a "
                "script his wife approaches in Portuguese.",
            ),
        ),
    },
    {
        "n": 8,
        "title": "Jeje Has Its Own Name",
        "src": "Rodrigues, Os Africanos, cap. IV",
        "pt": (
            "Gêge, mas que os negros pronunciam antes gêge. Os gêges "
            "conhecem o termo genérico Ewe. Tão forte foi o elemento gêge "
            "na Bahia que a nação, distinta da Nagô, deixou a sua própria "
            "língua litúrgica."
        ),
        "roman": roman(
            "Gêge / Jeje",
            "Ewe",
            "língua litúrgica",
        ),
        "tr": (
            "Gêge — though Africans pronounce it rather gêge. The Jeje know "
            "the generic term Ewe. So strong was the Jeje element in Bahia "
            "that the nation, distinct from the Nagô, left its own "
            "liturgical language."
        ),
        "comm": (
            "The claim is a name with a phonetics and a language: Jeje is "
            "not a mispronunciation of Nagô. They know themselves as Ewe. "
            "The nation was strong enough in Bahia to leave a liturgical "
            "tongue, not only a footnote in someone else’s myth. Later "
            "units will say the public cult fused as Gêge-Nagô; fusion is "
            "not erasure of the Jeje name at the start. Rodrigues writes "
            "os negros pronunciam and keeps the mass-noun even while "
            "recording a nation’s own word. Poison: the physician can hear "
            "gêge and still see Negroes. Do not complete his sentence by "
            "treating Jeje as a lesser Yoruba, a slave-trade leftover, or a "
            "vodu scare-label. The ethnographic remainder is Ewe as a "
            "generic term the Jeje themselves know, and a Bahia in which "
            "that speech was strong. Johnson writes one Yoruba faith from "
            "inside; Ellis’s òwe are Yoruba speech. Jeje is the neighbor "
            "nation those pages do not get to annex. Lasnet’s Serer life is "
            "another West African house with its own names for the highest "
            "and the dead. Existentially, you refuse the one gloss that "
            "collapses Jeje into Nagô. If you can only say Yoruba "
            "Candomblé, you have already performed the exclusivism cap. I "
            "warned against."
        ),
        "prac": (
            "Today, refuse one gloss that collapses Jeje, Ewe, or \"Jeje "
            "nation\" into Yoruba or Nagô. Say the second name out loud. "
            "If you have never said it, that is the act."
        ),
        "terms": kt(
            (
                "Gêge / Jeje",
                "Bahian name for Ewe-speaking people and their cult -> a "
                "nation with its own liturgical language -> a dialect of "
                "Nagô or a synonym for vodu is the gloss this unit breaks",
            ),
            (
                "Ewe",
                "the generic term the Jeje know for themselves -> the "
                "African name behind the Bahian one -> leaving it unsaid "
                "lets Gêge float as a local curiosity",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Only One God in "
                "the Universe",
                "Both refuse a single African religion in Bahia, but this "
                "unit names the Jeje/Ewe house Animismo often hears only "
                "as a presence beside Nagô.",
                "Animismo’s opening weight is Yoruba; here Jeje is a "
                "nation with its own name and tongue.",
            ),
            (
                "Lasnet, Senegalese Animism — Animism Is Not Fetishism",
                "Both refuse a metropolitan label that would turn a people "
                "into a type.",
                "Lasnet denies fetish as the Serer religion; this unit "
                "denies Nagô as the only Bahian African nation.",
            ),
        ),
    },
    {
        "n": 9,
        "title": "After Language, Religions",
        "src": "Rodrigues, Os Africanos, cap. V",
        "pt": (
            "Depois da língua, as religiões. As múltiplas e variadas "
            "manifestações do sentimento religioso dão, depois da língua, o "
            "mais seguro critério das procedências. Língua, religião, "
            "festas e tradições, folk-lore."
        ),
        "roman": roman(
            "língua",
            "religiões",
            "procedências",
            "folk-lore",
        ),
        "tr": (
            "After language, the religions. The multiple and varied "
            "manifestations of religious feeling give, after language, the "
            "surest criterion of origins. Language, religion, festivals and "
            "traditions, folklore."
        ),
        "comm": (
            "The methodological claim is an order of knowing: language "
            "first, then religions. Festivals, traditions, and folklore "
            "follow. You do not sort a people by pigment and then assign "
            "them a cult. You listen to what they speak and how they pray. "
            "Rodrigues, racial theorist, means this as a criterion of "
            "procedências — origins as stock — and will use religion to "
            "classify bodies he has already ranked. That is the poison. A "
            "sure criterion of origins in his mouth is a racial tool. We "
            "keep the order and refuse the sorting. The ethnographic "
            "remainder is still sharp: Nagô speech and Nagô cult travel "
            "together; Jeje speech leaves Jeje titles; Malê Arabic marks "
            "Islam; a Bantu language is not a failed Gêge-Nagô. Johnson’s "
            "Yoruba faith is a religion that comes after a language; Ellis’s "
            "òwe are that language teaching. Lasnet’s Serer names bind "
            "worship to a tongue and a land. Existentially, you ask which "
            "language a rite is in before you name the rite. If you cannot "
            "hear the language, you do not yet know the origin, and you do "
            "not get to fill the silence with African as a type."
        ),
        "prac": (
            "Today, before you name a rite, ask which language it is in. "
            "Write the language if you know it. If you do not, write "
            "\"unknown\" and do not supply a people from the sound of the "
            "drums alone."
        ),
        "terms": kt(
            (
                "procedências",
                "origins / provenances -> for Rodrigues a racial sorter; "
                "for the remainder, the nation a language and a cult still "
                "name -> \"African origin\" as one box misses the order "
                "língua then religião",
            ),
            (
                "folk-lore",
                "Rodrigues’s last item in the list -> a scientist’s bin for "
                "what he will not call theology -> festivals and traditions "
                "here are evidence of nations, not charming leftovers",
            ),
        ),
        "res": res(
            (
                "Ellis, Yoruba òwe — The young cannot teach the elders "
                "traditions",
                "Both treat language as the first archive of a people: "
                "speech carries what a later science would call folklore.",
                "The òwe is the teaching; Rodrigues wants a criterion for "
                "sorting origins and will misuse it.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — One God, Many Towns",
                "Both let local speech and local cult mark difference "
                "inside a wider name.",
                "Johnson stays inside Yoruba towns; this unit is the rule "
                "for hearing many African nations in one Brazilian city.",
            ),
        ),
    },
    {
        "n": 10,
        "title": "Herbs Belong to the Orisa",
        "src": "Rodrigues, Os Africanos, cap. V",
        "pt": (
            "Ewé ti mabasa ko’é; Ewé shogbo ni torisa. As ervas que se não "
            "usam; todas as ervas são do orixá."
        ),
        "roman": roman(
            "ewé (leaf / herb)",
            "orisa / orixá",
            "Ewé ti mabasa ko’é; Ewé shogbo ni torisa",
        ),
        "tr": (
            "Ewé ti mabasa ko’é; Ewé shogbo ni torisa. The herbs one does "
            "not use; all herbs are the orisa’s."
        ),
        "comm": (
            "The liturgical claim is botanical and possessive: a leaf that "
            "is not used is not thereby free, and all herbs belong to the "
            "orisa. Nagô speech in Bahia keeps a proverb that will not let "
            "the forest be raw material. Medicine, food, and rite share a "
            "owner. Rodrigues files the line under folklore and origins, "
            "the physician’s habit of hearing a charm where a theology of "
            "use is speaking. Poison: herbs become evidence of primitive "
            "mentality, a step on the ladder toward \"real\" pharmacy. Do "
            "not complete a leaf-list from this page. Do not turn the òwe "
            "into a recipe. The ethnographic remainder is the proverb’s "
            "two clauses. Unused is still claimed. Used is already "
            "someone’s. Animismo’s Osun lives in the fountain and the iroko "
            "can be the god himself; the forest is populated before you "
            "pick. Ellis keeps Yoruba proverb as public wisdom; this òwe "
            "is that wisdom about leaves. Johnson’s middle population "
            "between Maker and world includes powers who own things you "
            "thought were vacant. Existentially, before you pick a plant "
            "as just a plant, you ask whose it is. If everything unused is "
            "yours, you have already stolen the orisa’s forest."
        ),
        "prac": (
            "Today, before you pick, buy, or brew one plant as \"just a "
            "plant,\" stop and ask whose it would be if a people you do "
            "not belong to already claimed it. Do not use it as a rite. "
            "Write the question."
        ),
        "terms": kt(
            (
                "ewé",
                "Yoruba leaf / herb -> liturgical plant, not wild inventory "
                "-> \"herb\" as folk medicine misses that unused leaves "
                "are still the orisa’s",
            ),
            (
                "orisa",
                "the owner in the proverb -> all herbs are t’òrìṣà -> a "
                "nature-spirit gloss hides the possessive theology",
            ),
        ),
        "res": res(
            (
                "Ellis, Yoruba òwe — If an orisha would kill a man for "
                "cooking an…",
                "Both treat the orisa as having jurisdiction over ordinary "
                "use of what looks like food or plant.",
                "Ellis’s òwe warns by sanction; this òwe claims the whole "
                "herb field before the cooking starts.",
            ),
            (
                "Nina Rodrigues, O Animismo Fetichista — The Iroko Is the "
                "God Himself",
                "Both refuse a vacant forest: a tree or a leaf can already "
                "be a power’s body or property.",
                "The iroko unit is one tree as the god; this proverb "
                "generalizes possession to all herbs.",
            ),
        ),
    },
    {
        "n": 11,
        "title": "There Is No King Except God",
        "src": "Rodrigues, Os Africanos, cap. V — Baixa dos Sapateiros",
        "pt": (
            "Tem havido nesta cidade inscrições em língua nagô em casas de "
            "comércio de negros, como em templos ou pêgis fetichistas. Nela "
            "se lê corretamente a sentença: Kosi obá kan afi Olorun, isto "
            "é: Só há um rei que é Deus, ou literalmente: Não há rei um "
            "senão Deus."
        ),
        "roman": roman(
            "Kosi obá kan afi Olorun",
            "obá (king)",
            "Olorun",
            "pêgi (peji / shrine)",
        ),
        "tr": (
            "There have been, in this city, inscriptions in the Nagô "
            "language on Black commercial houses as on temples or pejis. "
            "On one is correctly read the sentence: Kosi obá kan afi "
            "Olorun — that is: There is only one king, who is God, or "
            "literally: There is not one king except God."
        ),
        "comm": (
            "The theological claim is public and grammatical: there is no "
            "king except God. Nagô writes it on shops and on pejis. The "
            "street can read a metaphysics above a counter. Kosi obá kan "
            "afi Olorun is not a proverb hidden in a book; it is a lintel. "
            "Rodrigues cannot report the sentence without pêgis fetichistas "
            "— fetish shrines — the poison word that turns a temple into a "
            "specimen. Do not take fetish as the doctrine of the "
            "inscription. The ethnographic remainder is the same theology "
            "Animismo already painted on Baixa dos Sapateiros: one king, "
            "Olorun, and a city that lets that sentence stand in Yoruba on "
            "a commercial house. Johnson reserves the name and states the "
            "Lord of Heaven; Bahia paints the political consequence. Ellis’s "
            "òwe keep wisdom in speech; this wisdom is speech nailed up. "
            "Existentially, you write one sentence that names a king you "
            "will not put above God — office, party, market, or self — and "
            "you notice whether you would dare hang it where customers "
            "walk. A theology that cannot leave the study is still private."
        ),
        "prac": (
            "Today, write one sentence that names a king — office, brand, "
            "party, or self — you will not put above the highest you "
            "actually name. Put the sentence where you work, not where you "
            "pray."
        ),
        "terms": kt(
            (
                "Kosi obá kan afi Olorun",
                "There is not one king except God / there is only one king, "
                "who is God -> Nagô public theology -> a Muslim-looking "
                "line that Animismo already said a terreiro person can "
                "write",
            ),
            (
                "pêgi",
                "peji, the orisha’s shrine-house -> temple, not a fetish "
                "cabinet -> Rodrigues’s fetichistas is the poison glued to "
                "a real word",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — There Is No King "
                "Like God",
                "Both read the same Bahian Nagô inscription as theology on "
                "the street, not as a hidden Muslim verse.",
                "Animismo gives the butcher-shop scene in French; this "
                "Portuguese line stresses shops and pejis together.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Olorun, the Lord of "
                "Heaven",
                "Both name Olorun as the one who outranks every earthly "
                "oba.",
                "Johnson writes from inside Yoruba faith; this unit is the "
                "sentence painted in a Catholic-majority city.",
            ),
        ),
    },
    {
        "n": 12,
        "title": "Olorun Has No Cult and No Worshippers",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Olorun, o Céu-Deus, satisfazendo dificilmente a condição de "
            "objeto concreto de culto, é apenas a representação da mais "
            "alta aptidão da Raça para generalizar. Concepção da minoria "
            "inteligente, a divindade não penetrou a massa popular, e "
            "Olorun representa assim uma divindade singular que não tem "
            "culto organizado, que não possui sacerdócio, que não tem "
            "adoradores."
        ),
        "roman": roman(
            "Olorun (Céu-Deus)",
            "sem culto organizado",
            "sem sacerdócio",
            "sem adoradores",
        ),
        "tr": (
            "Olorun, the Heaven-God, hardly satisfying the condition of a "
            "concrete object of cult, is only the representation of the "
            "Race’s highest aptitude for generalizing. A conception of the "
            "intelligent minority, the divinity did not penetrate the "
            "popular mass, and Olorun thus represents a singular divinity "
            "who has no organized cult, who possesses no priesthood, who "
            "has no worshippers."
        ),
        "comm": (
            "The liturgical fact is negative and exact: Olorun has no "
            "organized cult, no priesthood, and no worshippers. The highest "
            "is not the most available. Absence of a feast is not a hole in "
            "the religion; it is the religion’s height. Rodrigues cannot "
            "state that fact without racial-theory poison. He calls Olorun "
            "the Race’s highest aptitude for generalizing, a conception of "
            "the intelligent minority that failed to penetrate the mass. "
            "Refuse that sentence as doctrine. There is no racial IQ of "
            "monotheism. There is no Nagô elite that invented a sky-god "
            "the people were too dull to keep. Animismo already said the "
            "same liturgical emptiness in French: no image, no special "
            "cult. Johnson’s Olorun is too exalted to handle human affairs "
            "directly. Lasnet’s invisible master is named as the sky and "
            "not addressed as an object. The ethnographic remainder is the "
            "empty plinth. Orishas receive because they receive. Olorun "
            "needs nothing, therefore he is not kept as a client. "
            "Existentially, you stop treating the unaddressed highest as a "
            "failure of the people who named it. What has no worshippers "
            "may be the one name you must not turn into a following you "
            "can count."
        ),
        "prac": (
            "Today, name one highest principle you claim and notice that "
            "you have no weekly rite for it. Do not invent one. Write "
            "whether the absence is reverence or neglect — and do not "
            "score anyone else’s empty plinth as stupidity."
        ),
        "terms": kt(
            (
                "Olorun",
                "Heaven-God, Lord of Heaven -> known, unaddressed, without "
                "organized cult -> \"unknown god\" or \"deus otiosus\" as "
                "racial deficit is Rodrigues’s poison",
            ),
            (
                "minoria inteligente",
                "intelligent minority -> racial-theory smear for who can "
                "think a high god -> refuse as doctrine; keep the "
                "liturgical fact that Olorun has no cult",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Olorun Has No "
                "Image and No Cult",
                "Both state the same Bahian fact: Olorun is known and not "
                "kept as a liturgical client.",
                "Animismo stresses no image; this unit adds no priesthood "
                "and no worshippers — and must refuse the racial gloss "
                "glued to the fact.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — Between Maker and World",
                "Both pair a comprehensive Maker with distance: exaltation "
                "explains why the middle population does the work.",
                "Johnson does not need a racial minority to explain the "
                "distance; Rodrigues does, and that need is poison.",
            ),
        ),
    },
    {
        "n": 13,
        "title": "Changô Takes Thunder from the Sky",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Nos Nagôs, não só as funções do raio e do trovão cabem a um "
            "orichá poderoso e antropomorfo, Changô, como outras funções de "
            "Olorun estão sendo distribuídas por divindades múltiplas, "
            "reservando-se apenas para ele a ideia vaga de uma entidade "
            "superior e quase inacessível."
        ),
        "roman": roman(
            "Changô / Ṣàngó",
            "orichá",
            "raio e trovão",
            "Olorun",
        ),
        "tr": (
            "Among the Nagô, not only do the functions of lightning and "
            "thunder belong to a powerful and anthropomorphic orisha, "
            "Changô, but other functions of Olorun are being distributed "
            "among multiple divinities, reserving for him only the vague "
            "idea of a superior and almost inaccessible entity."
        ),
        "comm": (
            "The liturgical claim is a division of labor: thunder and "
            "lightning belong to Changô, a powerful orisha with a face, and "
            "Olorun keeps the almost inaccessible height. The sky is not "
            "empty because the storm has a name. Rodrigues writes "
            "antropomorfo and funções distribuídas as if a high god were "
            "being looted by lesser figures — Tylor’s ladder, degeneration, "
            "the Race losing its aptitude to generalize. Poison. Do not "
            "teach Changô as a piece broken off a failing monotheism. "
            "Animismo already said Sango is the thunder-stone itself and "
            "that no terreiro stands without him. Johnson’s middle "
            "population is the point of a God who is not the storm. Ìfẹ̀ "
            "knows thunder cannot stop brothers: the sky’s violence is not "
            "the last word. The ethnographic remainder is the pair. Olorun "
            "remains. Changô takes the bolt. You approach the bolt; you do "
            "not barge in on the height. Existentially, you name the power "
            "you actually cry to when it thunders, and you stop calling "
            "the highest empty because it does not throw the spear. A God "
            "who keeps only inaccessibility is not a vacancy. A saint of "
            "thunder is not a theft."
        ),
        "prac": (
            "Today, when you hear thunder or name a storm, say which power "
            "you actually address — if any — and which highest you do not. "
            "Do not invent a rite. Write the two names, or write that you "
            "have been collapsing them."
        ),
        "terms": kt(
            (
                "Changô",
                "Ṣàngó, orisha of thunder and lightning -> the face the "
                "storm has in Nagô Bahia -> \"anthropomorphic sky-god\" as "
                "an evolutionary stage is Rodrigues’s ranking",
            ),
            (
                "inacessível",
                "almost inaccessible -> what is reserved to Olorun when "
                "functions are distributed -> a deficit only if you think "
                "the highest must be the most used",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Sango Is the "
                "Thunder-Stone Itself",
                "Both give thunder a Nagô name and a body in the terreiro, "
                "not a vague sky-mood.",
                "Animismo identifies Sango with the stone; this unit "
                "states the transfer of function from Olorun’s height.",
            ),
            (
                "Myths of Ìfẹ̀ — Thunder Cannot Stop Brothers",
                "Both keep thunder as a real power that does not get the "
                "last word over the human bond.",
                "Ìfẹ̀’s thunder fails to end kinship; Bahia’s Changô "
                "receives the bolt that Olorun will not wield as a cult.",
            ),
        ),
    },
    {
        "n": 14,
        "title": "Obatalá Shares the World with Odudua",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Obatalá é por excelência o rei dos orichás. É ainda o "
            "Céu-Deus, mas o céu-Deus a que estão confiadas as "
            "interferências imediatas nas ações humanas. Olorun, "
            "recolhendo-se à inação e ao repouso, confiava a Obatalá a "
            "missão de dirigir o mundo. Obatalá veio partilhar com Odudua "
            "a função da reprodução."
        ),
        "roman": roman(
            "Obatalá",
            "Odudua / Odùduwà",
            "orichás",
            "Olorun",
        ),
        "tr": (
            "Obatalá is by excellence the king of the orishas. He is still "
            "the Heaven-God, but the heaven-God to whom immediate "
            "interferences in human actions are entrusted. Olorun, "
            "withdrawing into inaction and rest, entrusted to Obatalá the "
            "mission of directing the world. Obatalá came to share with "
            "Odudua the function of reproduction."
        ),
        "comm": (
            "The cosmological claim is a court at work: Obatalá is king of "
            "the orishas, the heaven-God who still touches human action, "
            "and he shares the world’s making with Odudua. Olorun remains "
            "high; the world is run by a pair. Rodrigues writes inação e "
            "repouso as if the highest had retired like a tired monarch, a "
            "deus otiosus on a racial clock. Poison. Withdrawal is not "
            "senility of the Race. It is the same exaltation Animismo and "
            "Johnson already taught: the Maker does not do the weekly "
            "work. Johnson’s Orisala shapes the lump; Ìfẹ̀’s Odúwa protests "
            "a gift and still founds a world. Bahia keeps both names in "
            "one sentence. The ethnographic remainder is the share. "
            "Reproduction is not a private Obatalá file and not a Catholic "
            "\"creation\" pasted onto a fetish. Two powers, one mission, "
            "under a God who is not on the rota. Existentially, you notice "
            "who actually does the work you attribute to the highest name "
            "— the deputy, the partner, the pair — and you stop calling "
            "the deputies a decline. A world that needs two hands is not a "
            "failed monotheism."
        ),
        "prac": (
            "Today, name one task you keep assigning to a highest "
            "principle, then name the two people or offices that actually "
            "share that work. Thank the pair. Do not promote them into the "
            "highest name."
        ),
        "terms": kt(
            (
                "Obatalá",
                "king of the orishas, heaven-God of immediate action -> "
                "the deputy of Olorun in the world -> collapsing him into "
                "Olorun, or into a mere saint, hides the court",
            ),
            (
                "Odudua",
                "Odùduwà, co-sharer of reproduction and world-direction -> "
                "partner, not a later rival footnote -> Ìfẹ̀’s Odúwa is "
                "the same name under another observer",
            ),
        ),
        "res": res(
            (
                "Samuel Johnson, The Yoruba Faith — Shaped by the Hand of "
                "Orisala",
                "Both keep a shaper-god under the Maker: the world is "
                "worked, not only willed.",
                "Johnson’s Orisala shapes the lump Olorun made; Bahia’s "
                "Obatalá shares reproduction with Odudua.",
            ),
            (
                "Myths of Ìfẹ̀ — Odúwa Protests the Gift",
                "Both give Odùduwà agency in the world’s founding, not a "
                "silent female or male extra.",
                "Ìfẹ̀’s Odúwa protests a gift on the road; this unit "
                "states the share in reproduction as a Bahian liturgical "
                "fact.",
            ),
        ),
    },
    {
        "n": 15,
        "title": "Ochun Becomes the Naiad of Springs",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Na falta do rio Ochun, a orichá Ochun se converte numa espécie "
            "de naiade, a divindade das fontes e regatos. Yemanjá é nesta "
            "cidade a deusa do Dique. Para os Negros e Mestiços "
            "brasileiros, o mito de Yemanjá se confunde com o da "
            "mãe-d’água e o da sereia."
        ),
        "roman": roman(
            "Ochun / Ọ̀ṣun",
            "Yemanjá / Yemọja",
            "Dique",
            "mãe-d’água",
        ),
        "tr": (
            "Lacking the river Ochun, the orisha Ochun becomes a kind of "
            "naiad, the divinity of springs and streams. Yemanjá is, in "
            "this city, the goddess of the Dique. For Black Brazilians and "
            "mixed-race Brazilians the myth of Yemanjá mingles with that "
            "of the mãe-d’água and that of the mermaid."
        ),
        "comm": (
            "The historical claim is relocation, not loss: without the "
            "river Ọ̀ṣun, Ochun becomes the divinity of the springs that "
            "are here; Yemanjá is goddess of the Dique in this city; her "
            "story mingles with mãe-d’água and the mermaid. An orisha can "
            "move water. Rodrigues writes naiade as a classical downgrade "
            "and Negros e Mestiços as racial types who confuse myths. "
            "Poison. Mixture is not muddle, and a plaster later unit will "
            "show is not proof of a cheapened goddess. Animismo already "
            "said Osun lives in the fountain and Yemanja is the divinized "
            "sea. Ìfẹ̀ sets Olókun to curb the sea: water has a keeper. "
            "The ethnographic remainder is the Dique and the missing "
            "Nigerian river. Bahia did not forget Ochun; it found her in "
            "the water it had. Yemanjá meeting the mermaid is Brazilian "
            "water theology, a second name for a power already at the "
            "weir. Existentially, you name the water nearest you and "
            "refuse to call it empty. If your river is gone, the question "
            "is which spring you will not treat as decoration."
        ),
        "prac": (
            "Today, name the nearest spring, fountain, weir, or sea wall. "
            "Write whether you treat it as empty civic water. Do not "
            "invent an offering. Notice the vacancy you have been calling "
            "normal."
        ),
        "terms": kt(
            (
                "Ochun",
                "Ọ̀ṣun, orisha of a river -> in Bahia, springs and streams "
                "when that river is absent -> \"naiad\" as a pretty "
                "classical demotion hides a relocated cult",
            ),
            (
                "Yemanjá",
                "Yemọja, here goddess of the Dique -> mingles with "
                "mãe-d’água and the mermaid -> \"confusion\" as racial "
                "deficit is Rodrigues’s smear of a living syncretism",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Osun Lives in the "
                "Fountain",
                "Both relocate Ọ̀ṣun from a West African river to Bahian "
                "water that can actually be approached.",
                "Animismo stays with the fountain; this unit adds Yemanjá "
                "at the Dique and the mermaid meeting.",
            ),
            (
                "Myths of Ìfẹ̀ — Olókun Set to Curb the Sea",
                "Both give a named keeper to a body of water that would "
                "otherwise be treated as raw nature.",
                "Ìfẹ̀’s Olókun curbs the sea at the world’s founding; "
                "Bahia’s Yemanjá keeps a weir in a colonial city.",
            ),
        ),
    },
    {
        "n": 16,
        "title": "Ifá Learns Divination from Elegbá",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Ifá tentou a pesca, mas nada apanhou e descoroçoado foi pedir "
            "conselho a Elegbá. Propôs-lhe este que trouxesse nozes de "
            "dendezeiro com que o feiticeiro lhe ensinaria a adivinhar. "
            "Estipulou que lhe caberiam as primícias de todas as ofertas. "
            "Ifá ensinou a arte de adivinhar a Orungan, que foi assim o "
            "primeiro babalawo ou sacerdote de Ifá."
        ),
        "roman": roman(
            "Ifá",
            "Elegbá / Elegbara",
            "nozes de dendezeiro",
            "babalawo",
            "Orungan",
            "primícias",
        ),
        "tr": (
            "Ifá tried fishing, caught nothing, and disheartened went to "
            "ask Elegbá’s counsel. Elegbá proposed he bring dendê-palm nuts "
            "with which the teacher would teach him to divine. He "
            "stipulated that the first-fruits of all offerings would be "
            "his. Ifá taught the art of divining to Orungan, who was thus "
            "the first babalawo, or priest of Ifá."
        ),
        "comm": (
            "The mythic claim is a pedagogy: Ifá does not invent "
            "divination from the sky. He fails at fishing, asks Elegbá, "
            "receives dendê nuts, and pays first-fruits. Then he teaches "
            "Orungan, the first babalawo. Reading is learned, transmitted, "
            "and taxed at the opening. Rodrigues writes feiticeiro for the "
            "teacher — sorcerer — criminal anthropology leaning on a "
            "myth. Poison. Do not complete a figure-list or a sacrifice "
            "from this page. Do not treat Elegbá’s first-fruits as a recipe. "
            "The ethnographic remainder is the order. Counsel before nuts. "
            "Nuts before reading. First-fruits before the rest of the "
            "offerings. A first priest. Animismo’s Ifá is the god of "
            "divinations by the fall; this unit is how that god himself "
            "had to be taught. Lasnet’s first-fruits are always offered; "
            "Elegbá stipulated the same law. Ìfẹ̀ locates truth in priests’ "
            "mouths; the babalawo is one such mouth with a palm-nut "
            "instrument. Existentially, you notice who taught the skill "
            "you credit to the official name, and what opening portion "
            "that teacher still claims. If you skip the opener, you have "
            "already stolen the first-fruits."
        ),
        "prac": (
            "Today, before you use one skill you are known for, name the "
            "person who taught you the opening move and pay that debt in a "
            "small first portion — thanks, money, or credit said aloud. "
            "Do not invent a divination."
        ),
        "terms": kt(
            (
                "Elegbá",
                "Elegbara / Eṣu as the counsel who teaches Ifá to read -> "
                "opener who takes first-fruits -> \"devil\" or \"trickster "
                "only\" hides the pedagogue of the nuts",
            ),
            (
                "babalawo",
                "priest of Ifá, here first embodied in Orungan -> a "
                "trained reader, not a sorcerer -> feiticeiro is "
                "Rodrigues’s poison for the same office",
            ),
            (
                "primícias",
                "first-fruits of all offerings -> Elegbá’s stipulated "
                "share -> skipping the opener is not a minor etiquette "
                "lapse; it is the myth’s theft",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Ifa Is the God of "
                "Divinations",
                "Both keep Ifá as a god of reading whose instrument is the "
                "dendê nut.",
                "Animismo states the fall as philosophy; this unit states "
                "the teaching-story and the first babalawo.",
            ),
            (
                "Lasnet, Senegalese Animism — First-Fruits Are Always "
                "Offered",
                "Both put an opening portion before the rest of the "
                "relationship can proceed.",
                "Serer first-fruits bind land and harvest; Elegbá’s "
                "first-fruits bind every later offering of Ifá.",
            ),
        ),
    },
    {
        "n": 17,
        "title": "Gêge-Nagô Mythology Prevails",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Tão íntima é a fusão em que se encontra na Bahia a mitologia "
            "ewe com a iorubana que se tornou hoje impossível "
            "distingui-las. E como depois da iorubana é a mitologia gêge a "
            "mais complexa, antes se deve dizer que uma mitologia "
            "gêge-nagô do que puramente nagô prevalece no Brasil."
        ),
        "roman": roman(
            "mitologia ewe / gêge",
            "mitologia iorubana / nagô",
            "gêge-nagô",
        ),
        "tr": (
            "So intimate is the fusion in which Ewe mythology stands with "
            "Yoruba mythology in Bahia that it has become impossible today "
            "to distinguish them. And because after the Yoruba it is Jeje "
            "mythology that is the most complex, one should say that a "
            "Gêge-Nagô mythology, rather than a purely Nagô one, prevails "
            "in Brazil."
        ),
        "comm": (
            "The historical claim is a hyphen: what prevails in Brazil is "
            "Gêge-Nagô, not a pure Nagô export. Ewe and Yoruba myth have "
            "fused in Bahia past the point of clean sorting. Jeje is not a "
            "spice. It is the other half of the public cult. Rodrigues "
            "cannot praise the fusion without a complexity ranking — Jeje "
            "second after Yoruba, the ladder still humming. Poison. "
            "Complexity is not a racial score. We keep the hyphen and "
            "refuse the podium. Cap. VIII’s ranking of peoples is not "
            "doctrine. The ethnographic remainder is the impossibility. If "
            "you cannot distinguish the mythologies in the house, stop "
            "advertising a purely Yoruba Candomblé as the Brazilian fact. "
            "Unit 8 gave Jeje its own name and tongue; this unit gives the "
            "fused cult its honest title. Animismo hears Jeje beside Nagô "
            "and still opens on Olorun’s court; this book, later, admits "
            "the court is already hyphenated. Johnson writes one Yoruba "
            "faith; he does not get to annex Ewe. Existentially, you "
            "refuse Yoruba Candomblé as the only name for a house that "
            "also speaks Jeje. If your label has no hyphen and the house "
            "does, the exclusivism is yours."
        ),
        "prac": (
            "Today, take one tradition you habitually name with a single "
            "people. Add the second name the house actually uses, or write "
            "that you have never asked. Do not tidy the hyphen away."
        ),
        "terms": kt(
            (
                "gêge-nagô",
                "hyphenated public mythology of Bahia / Brazil -> fusion "
                "past sorting -> \"Yoruba Candomblé\" as a pure brand "
                "erases Jeje",
            ),
            (
                "fusão",
                "intimate fusion of Ewe and Yoruba myth -> a historical "
                "fact of the city -> \"syncretism\" as confusion or "
                "\"complexity\" as a racial grade both miss the hyphen",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Only One God in "
                "the Universe",
                "Both describe Bahia’s public African religion as "
                "Yoruba-weighted — and this unit corrects the weight with "
                "a Jeje hyphen.",
                "Animismo’s opening is Nagô court; this sentence says the "
                "prevailing mythology is already Gêge-Nagô.",
            ),
            (
                "Samuel Johnson, The Yoruba Faith — One God, Many Towns",
                "Both refuse a single tidy people under one cult-name.",
                "Johnson’s many towns stay Yoruba; Bahia’s prevailing cult "
                "is two nations fused past distinction.",
            ),
        ),
    },
    {
        "n": 18,
        "title": "Caboclo Candomblé Is Still African",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Se os nossos supostos candomblés de Caboclos ou Indígenas são, "
            "de fato, candomblés africanos, em todo o caso ainda hoje "
            "aderem à feitiçaria africana dominante na Bahia esparsos "
            "fragmentos das crenças tupi-guaranis. Encontrei no Recôncavo "
            "a crença no Mboi-tatá que a população supõe africana."
        ),
        "roman": roman(
            "candomblé de Caboclos",
            "Tupi-Guarani",
            "Mboi-tatá",
            "Recôncavo",
        ),
        "tr": (
            "If our supposed Caboclo or Indigenous candomblés are in fact "
            "African candomblés, in any case there still adhere today to "
            "the African practice dominant in Bahia scattered fragments of "
            "Tupi-Guarani beliefs. I found in the Recôncavo the belief in "
            "Mboi-tatá that the population supposes to be African."
        ),
        "comm": (
            "The historical claim is about altars, not blood-quantum: "
            "houses called Caboclo or Indigenous are, in fact, African "
            "candomblés, and Tupi-Guarani fragments can adhere to that "
            "dominant practice. Mboi-tatá in the Recôncavo is taken for "
            "African and is not. A name can migrate onto the wrong shore. "
            "Rodrigues writes feitiçaria africana dominante — dominant "
            "African witchcraft — the poison that makes the whole field a "
            "spell-house and the Indigenous remainder a residue. Do not "
            "teach Caboclo as fake Indian play. Do not teach it as proof "
            "that Candomblé \"became\" Indigenous. Do not invent a later "
            "ethnographer to settle the houses. The ethnographic remainder "
            "is the double caution. The altar may be African under a "
            "Caboclo poster. A snake-fire of the Recôncavo may be Tupi "
            "under an African rumor. Animismo’s figures are neither fetish "
            "nor idol; a Caboclo name is neither a passport nor a fraud "
            "until you ask which peji is lit. Lasnet binds ancestor and "
            "land as one cult; a transplanted African cult can carry a "
            "local ghost without changing its jurisdiction. Existentially, "
            "before you call a rite Indigenous or African, you ask which "
            "altar it actually serves. The poster is not the offering."
        ),
        "prac": (
            "Today, before you label one rite Indigenous, African, or "
            "mixed, ask which altar is actually being served. Write the "
            "altar if you know it. If you do not, refuse the label for the "
            "day."
        ),
        "terms": kt(
            (
                "Caboclo",
                "house or power named as Indigenous / mixed-forest in "
                "Bahian speech -> often an African candomblé under another "
                "poster -> taking the poster as the origin, or as a fraud, "
                "skips the altar",
            ),
            (
                "Mboi-tatá",
                "Tupi-Guarani fire-serpent of the Recôncavo -> supposed "
                "African by the population -> a fragment that adhered, not "
                "a proof that the candomblé is Indigenous",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — The Figures Are "
                "Neither Fetish nor Idol",
                "Both refuse a surface name — fetish, Caboclo, idol — as "
                "the essence of what the house is doing.",
                "Animismo defends orisha figures; this unit defends an "
                "African jurisdiction under an Indigenous poster, and a "
                "Tupi name under an African rumor.",
            ),
            (
                "Lasnet, Senegalese Animism — The Ancestor and the Land "
                "Are One Cult",
                "Both know that land-spirits and incoming cults can share "
                "a landscape without becoming one origin.",
                "Serer ancestor and land are one cult in place; Bahia’s "
                "African house can carry a Tupi fragment without changing "
                "its peji.",
            ),
        ),
    },
    {
        "n": 19,
        "title": "Only Gêge and Nagô Survive",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "São os únicos sobreviventes das religiões nagô e gêge no "
            "Brasil. E em rigor são os únicos sobreviventes."
        ),
        "roman": roman(
            "religiões nagô e gêge",
            "sobreviventes",
            "culto organizado",
        ),
        "tr": (
            "They are the only survivors of the Nagô and Jeje religions in "
            "Brazil. And strictly, they are the only survivors."
        ),
        "comm": (
            "The historical claim is narrow if you keep it honest: as "
            "organized public cult in Brazil, Nagô and Jeje are the "
            "survivors Rodrigues can still walk into. Strictly, he says, "
            "the only ones. That is a statement about visible terreiros, "
            "not a death certificate for every African religion in the "
            "country. Rodrigues means survival as racial fitness — the "
            "complex mythologies endured, the others faded — and the "
            "ladder is already under the sentence. Poison. We do not teach "
            "\"only Gêge-Nagô\" as the worth of African life. Malê Islam "
            "organized in houses. Bantu languages and fragments remain. "
            "Caboclo posters adhere. Popular remainder will be a later "
            "channel. Extinction-talk is how a physician prepares Cap. "
            "VIII. The ethnographic remainder is the organized house. A "
            "public cult with priesthood, peji, and festival is not the "
            "same as a proverb, a herb, or a prayer-paper. Johnson’s "
            "Yoruba faith is organized in towns; Bahia’s Gêge-Nagô is "
            "organized in terreiros. Lasnet’s Serer cult is organized on "
            "land. None of those facts bury the neighbor they cannot see. "
            "Existentially, you distinguish the public house you can enter "
            "from the rest of a people’s life you cannot see. If you call "
            "the unseen dead, you have joined the exclusivism."
        ),
        "prac": (
            "Today, name one tradition you can actually walk into as a "
            "public house, and one you only know as a rumor or a word. Do "
            "not declare the second extinct. Write the limit of what you "
            "have seen."
        ),
        "terms": kt(
            (
                "sobreviventes",
                "survivors — here, Nagô and Jeje as organized cult -> a "
                "fact about public terreiros -> \"survival of the fittest "
                "religion\" is Rodrigues’s racial clock",
            ),
            (
                "em rigor",
                "strictly / in rigor -> the narrowing that makes organized "
                "cult the only thing that counts -> useful as a scope, "
                "fatal as a ranking of peoples",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Terreiro Means "
                "Place and Jurisdiction",
                "Both treat the standing house — terreiro, peji, "
                "priesthood — as what can still be observed as a cult.",
                "Animismo describes the house; this unit claims, too "
                "strictly, that only Gêge-Nagô houses still stand.",
            ),
            (
                "Lasnet, Senegalese Animism — They Live Where They Were "
                "Born",
                "Both know a cult that remains visible because a people "
                "kept a place.",
                "Serer remaining is on ancestral land; Gêge-Nagô remaining "
                "is a terreiro in a city that tried to suppress it.",
            ),
        ),
    },
    {
        "n": 20,
        "title": "Mãe de Santo Is Vodu-no",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "A denominação, geralmente adotada na Bahia, de “pai ou mãe de "
            "santo ou de terreiro”, é tomada à língua gêge. “Mãe de santo” "
            "é a tradução literal de Vodu-no, nome dado às sacerdotisas "
            "gêges do culto de Dãnh-gbi (Vodu, orichá ou santo e no, mãe). "
            "Entre nós as sacerdotisas não são chamadas mulheres ou "
            "esposas de santo, mas sim, filhas de santo."
        ),
        "roman": roman(
            "mãe de santo",
            "Vodu-no (vodu + no, mother)",
            "Dãnh-gbi",
            "filha de santo",
            "pai de santo / de terreiro",
        ),
        "tr": (
            "The designation generally adopted in Bahia, \"father or "
            "mother of saint or of terreiro,\" is taken from the Jeje "
            "language. \"Mãe de santo\" is the literal translation of "
            "Vodu-no, the name given to Jeje priestesses of the cult of "
            "Dãnh-gbi (Vodu, orisha or saint, and no, mother). Among us "
            "the priestesses are not called women or wives of the saint, "
            "but daughters of the saint."
        ),
        "comm": (
            "The linguistic claim is Jeje in the most common Bahian title: "
            "mãe de santo is Vodu-no, mother of the saint, from the cult "
            "of Dãnh-gbi. Father or mother of saint or terreiro is taken "
            "from Gêge speech. And the house does not call the priestess "
            "wife of the saint; it calls her daughter. Kinship is "
            "filiation, not marriage to the power. Rodrigues cannot write "
            "Vodu without the metropolitan scare-label humming — vodu as "
            "sensation, fetish, African contagion. Poison. Keep the "
            "etymology; refuse the carnival. Dãnh-gbi is a named Jeje "
            "cult, not a headline. Animismo’s father and mother are "
            "pontiff together, and children of the saints are the house’s "
            "population. This unit gives those Portuguese titles their "
            "Jeje mouth. Johnson’s sacred difference has forms; Bahia’s "
            "form is daughter, not wife. Existentially, you say the title "
            "in the language it came from once today. If you can only say "
            "priestess or mama, you have already translated the Jeje "
            "away. A daughter is not a spouse. A mother of saint is not a "
            "generic wise woman. The hyphen in Gêge-Nagô lives in the "
            "office’s name."
        ),
        "prac": (
            "Today, say mãe de santo or Vodu-no out loud once, and write "
            "the kinship it actually names — mother, daughter — not wife, "
            "not generic priestess. Do not invent an initiation."
        ),
        "terms": kt(
            (
                "Vodu-no",
                "Jeje: vodu (orisha / saint) + no (mother) -> mãe de santo "
                "as a literal calque -> \"voodoo priestess\" is the "
                "scare-label glued to a title",
            ),
            (
                "filha de santo",
                "daughter of the saint -> the priestess’s kinship in "
                "Bahia, not wife or woman of the saint -> marriage-to-the-"
                "god as the default misses the house’s own word",
            ),
            (
                "Dãnh-gbi",
                "Jeje cult whose priestesses are Vodu-no -> a named power, "
                "not a synonym for all Candomblé -> folding it into Nagô "
                "orisha lists repeats the one-gloss error",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Father and Mother "
                "Are Pontiff Together",
                "Both treat pai and mãe de santo as a paired jurisdiction "
                "of the terreiro, not a European priesthood borrowed late.",
                "Animismo states the pontificate; this unit gives the Jeje "
                "etymology and the daughter, not wife, correction.",
            ),
            (
                "Nina Rodrigues, O Animismo Fetichista — Children of the "
                "Saints",
                "Both make filiation the house’s basic kinship: one is a "
                "child of the saint, not a freelance devotee.",
                "Animismo describes the population; this unit names the "
                "mother-title as a Jeje translation.",
            ),
        ),
    },
    {
        "n": 21,
        "title": "The Seventh-Day Mass Calls the Dead",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "A missa do sétimo ou do trigésimo dia do falecimento de uma "
            "filha de santo constitui um misto de práticas africanas e "
            "católicas. À missa católica segue-se o candomblé funerário em "
            "que se invoca o morto para conhecer as suas deliberações "
            "últimas."
        ),
        "roman": roman(
            "missa do sétimo / trigésimo dia",
            "filha de santo",
            "candomblé funerário",
            "deliberações últimas",
        ),
        "tr": (
            "The Mass of the seventh or the thirtieth day after the death "
            "of a filha de santo constitutes a mix of African and Catholic "
            "practices. The Catholic Mass is followed by the funeral "
            "candomblé in which the dead person is invoked in order to "
            "know their last deliberations."
        ),
        "comm": (
            "The liturgical claim is a sequence, not a muddle: seventh- or "
            "thirtieth-day Mass for a daughter of the saint, then the "
            "funeral candomblé that calls the dead to hear their last "
            "decisions. Catholic time-keeping, then the house’s own "
            "hearing of the dead. Two rooms, one death. Rodrigues writes "
            "misto as contamination — incomplete conversion, a leftover "
            "Africa stuck to a Mass. Poison. A mix is not a failure to "
            "choose. The ethnographic remainder is the order. Mass first. "
            "Then the dead are invoked. Last deliberations: the person is "
            "still a speaker in the house, not only a soul the priest has "
            "commended. Animismo’s children of the saints are a living "
            "population; this unit is what the house does when one of "
            "them dies. Lasnet’s dead are spoken to at the ear; Bahia "
            "speaks after a Mass the city will recognize. Johnson’s "
            "portals of Heaven keep an account; this funeral wants the "
            "dead’s own last word before the account closes. "
            "Existentially, you notice one funeral that uses two houses "
            "and refuse to call the second a leftover. If you only attend "
            "the Mass, you have heard the city’s rite and missed the "
            "house’s hearing."
        ),
        "prac": (
            "Today, notice one funeral, memorial, or anniversary that "
            "uses two houses — church and something else. Write the "
            "sequence. Do not call the second rite a leftover or a "
            "confusion."
        ),
        "terms": kt(
            (
                "candomblé funerário",
                "funeral candomblé after the Mass -> the dead are invoked "
                "for last deliberations -> \"pagan residue after church\" "
                "misses a second complete rite",
            ),
            (
                "deliberações últimas",
                "last deliberations of the dead -> the person still "
                "decides -> a soul that only rests has already been "
                "silenced by the Mass alone",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Children of the "
                "Saints",
                "Both treat the filha de santo as a member of a house "
                "whose kinship outlasts a private death.",
                "Animismo describes the living population; this unit is "
                "the house calling that member after the seventh-day Mass.",
            ),
            (
                "Lasnet, Senegalese Animism — Speak to the Dead at the Ear",
                "Both keep the newly dead as addressees, not only as "
                "bodies to be buried.",
                "Serer speech is at the ear of the corpse; Bahia’s hearing "
                "follows a Catholic Mass the street will accept.",
            ),
        ),
    },
    {
        "n": 22,
        "title": "Gesso Sirens at Gantois",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "No candomblé dos Gantois dos fins do ano de 1899, tive "
            "ocasião de ver como ídolos de Yemanjá e Ochun duas sereias de "
            "gesso barato, mandadas vir do Rio de Janeiro, uma prateada, "
            "Yemanjá, a outra dourada, Ochun."
        ),
        "roman": roman(
            "Gantois (1899)",
            "sereias de gesso",
            "Yemanjá (prateada)",
            "Ochun (dourada)",
        ),
        "tr": (
            "At the Gantois candomblé at the end of 1899, I had occasion "
            "to see, as images of Yemanjá and Ochun, two cheap plaster "
            "sirens ordered from Rio de Janeiro, one silvered, Yemanjá, "
            "the other gilded, Ochun."
        ),
        "comm": (
            "The liturgical claim is that the orisha can sit in a cheap "
            "vessel: at Gantois in 1899, Yemanjá and Ochun were plaster "
            "sirens from Rio, silvered and gilded. The power is not the "
            "plaster. The house can fix a water orisha in a shop-window "
            "mermaid and still be Gantois. Rodrigues writes ídolos and "
            "gesso barato as proof of degeneration — fetish, poverty, a "
            "religion sliding into carnival kitsch. Poison. Animismo "
            "already said the figures are neither fetish nor idol, and "
            "that the saint can be fixed in any object. A Rio siren is "
            "that doctrine in a crate. Unit 15 said Yemanjá mingles with "
            "the mermaid; here the mermaid is on the altar, color-coded. "
            "Johnson’s mortal shrine is destroyed at death; this shrine "
            "can be replaced by the next shipment without the orisha "
            "dying. Existentially, you refuse to mock the cheap vessel as "
            "if the power were the plaster. If your respect requires "
            "expensive material, you have joined the physician’s aesthetic "
            "ladder. The silver and the gold are signs. The gesso is not "
            "the goddess."
        ),
        "prac": (
            "Today, notice one cheap object that stands in for a power, a "
            "person, or a vow you actually keep. Do not upgrade it. Write "
            "whether your respect has been waiting for a costlier vessel."
        ),
        "terms": kt(
            (
                "gesso barato",
                "cheap plaster -> the vessel, not the orisha -> "
                "Rodrigues’s sneer treats poverty of material as poverty "
                "of cult",
            ),
            (
                "sereias",
                "sirens from Rio as Yemanjá and Ochun -> a fixed form the "
                "saint can occupy -> \"idol\" or \"kitsch\" misses "
                "Animismo’s rule that the saint may sit in any object",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — The Saint Can Be "
                "Fixed in Any Object",
                "Both allow the orisha to occupy a vessel that was not "
                "carved as an \"African idol.\"",
                "Animismo states the rule; Gantois 1899 is the rule in "
                "two plaster sirens from Rio.",
            ),
            (
                "Nina Rodrigues, O Animismo Fetichista — The Figures Are "
                "Neither Fetish nor Idol",
                "Both refuse fetish/idol as the name of what stands in "
                "the peji.",
                "Animismo argues the philosophy; this unit shows the "
                "physician still saying ídolos when he sees plaster.",
            ),
        ),
    },
    {
        "n": 23,
        "title": "Crioulo Hands Already Hold the Terreiros",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Como culto organizado, ele persistirá ainda por largo prazo, "
            "mesmo após a extinção dos velhos africanos sobreviventes à "
            "escravidão. Grande número de terreiros na capital como "
            "principalmente no interior do Estado já são dirigidos "
            "atualmente por negros crioulos e mestiços, instruídos nessas "
            "práticas litúrgicas."
        ),
        "roman": roman(
            "culto organizado",
            "crioulos",
            "terreiros",
            "práticas litúrgicas",
        ),
        "tr": (
            "As an organized cult it will persist for a long time yet, "
            "even after the extinction of the old Africans who survived "
            "slavery. A great number of terreiros in the capital, and "
            "especially in the interior of the state, are already directed "
            "today by Creole Black Brazilians and mixed-race people, "
            "instructed in these liturgical practices."
        ),
        "comm": (
            "The historical claim is succession, not dying: the organized "
            "cult will persist after the first-generation Africans are "
            "gone, because Creole hands already hold the terreiros, in "
            "the capital and in the interior, instructed in the liturgy. "
            "A tradition that can be taught is a tradition that can outlive "
            "the ship. Rodrigues writes extinção and mestiços as a racial "
            "clock — the old Africans die, mixture dilutes, the cult "
            "should fade and somehow does not. Poison. Creole direction is "
            "not a dilution of a pure African essence. It is the house "
            "working. Instruction is the mechanism. Animismo already saw "
            "Creoles adhere to Yoruba religion in Bahia; this unit names "
            "them as directors. Johnson’s many towns keep a faith without "
            "needing every priest to have been born in the first city. "
            "Ìfẹ̀’s truth lives in mouths handed down from sire to son; "
            "Bahia’s truth lives in liturgical instruction across a "
            "generation the plantation named crioulo. Existentially, you "
            "stop treating a tradition as dead because the first-generation "
            "speakers are gone. If you can be taught the practice, the "
            "house is not a museum of survivors. It is a school."
        ),
        "prac": (
            "Today, name one practice you keep that was taught by someone "
            "not born in the practice’s first country or first generation. "
            "Write the teacher’s instruction, not their blood. Do not "
            "call the line diluted."
        ),
        "terms": kt(
            (
                "crioulos",
                "Creole Black Brazilians, Brazilian-born -> already "
                "directing terreiros -> \"less authentic than African-born\" "
                "is the racial clock this unit breaks",
            ),
            (
                "extinção",
                "extinction of the old Africans -> Rodrigues’s demographic "
                "threat -> the remainder is liturgical instruction, not a "
                "dying race",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Only One God in "
                "the Universe",
                "Both already know Creole and mixed-race Bahians adhere to "
                "the Nagô house; this unit adds that they direct it.",
                "Animismo reports adhesion; this sentence reports "
                "succession after the African-born generation.",
            ),
            (
                "Myths of Ìfẹ̀ — Where Truth Has Its Home",
                "Both locate the cult’s future in instruction — mouths "
                "handed down — not in a first body’s survival.",
                "Ìfẹ̀’s handing-down is priestly lineage at the shrine; "
                "Bahia’s is liturgical teaching of Brazilian-born "
                "directors.",
            ),
        ),
    },
    {
        "n": 24,
        "title": "The Cult That Resisted the Whip",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "O culto gêge-nagô que resistiu à conversão católica a chicote "
            "nas fazendas e plantações; que sobreviveu a todas as "
            "violências dos senhores de escravos; que não se absorveu até "
            "hoje nas práticas do catolicismo dos brancos, diante de cuja "
            "resistência capitulou o clero católico que já nem tenta "
            "converter os infiéis; esse culto está destinado a resistir, "
            "por longo prazo ainda, à propaganda da imprensa como às "
            "violências da polícia."
        ),
        "roman": roman(
            "culto gêge-nagô",
            "chicote",
            "clero católico",
            "polícia",
            "imprensa",
        ),
        "tr": (
            "The Gêge-Nagô cult that resisted Catholic conversion by the "
            "whip on the plantations; that survived every violence of the "
            "slaveholders; that has not to this day been absorbed into the "
            "practices of the whites’ Catholicism, before whose resistance "
            "the Catholic clergy capitulated and no longer even tries to "
            "convert the \"infidels\" — that cult is destined to resist, "
            "for a long time yet, the propaganda of the press as well as "
            "the violences of the police."
        ),
        "comm": (
            "The historical claim is a resistance with a list of enemies: "
            "whip, slaveholder, white Catholicism, clergy, press, police. "
            "The Gêge-Nagô cult was not absorbed. The clergy stopped "
            "trying. The house is destined to outlast the next two "
            "violences as well. This is not a compliment Rodrigues enjoys. "
            "He writes infiéis and a destiny of resistance as a problem "
            "for the nation — a cult that will not die on schedule. "
            "Poison. Do not take his forecast as a wish for police "
            "victory, and do not take it as a romance of invincibility. "
            "The ethnographic remainder is the sequence of failed "
            "erasures. Conversion at the whip failed. Absorption into "
            "white Catholicism failed. Clergy capitulated. Press and "
            "police are named as the current instruments. Animismo’s "
            "terreiro is a jurisdiction; this unit is why that "
            "jurisdiction still has a door. Lasnet’s people do not leave "
            "ancestral land voluntarily; these people were taken and still "
            "did not become the master’s church. Existentially, you name "
            "one pressure that tried to absorb a practice you keep — "
            "office, family, feed, force — and you keep the practice "
            "today. Resistance here is not a mood. It is a cult that "
            "remained unabsorbed."
        ),
        "prac": (
            "Today, name one pressure — office, family, feed, or force — "
            "that has tried to absorb a practice you keep. Keep the "
            "practice once, unabsorbed. Do not announce it as heroism."
        ),
        "terms": kt(
            (
                "chicote",
                "the whip on plantations as an instrument of Catholic "
                "conversion -> failed -> \"mission\" as kindness hides "
                "this sentence’s instrument",
            ),
            (
                "infiéis",
                "the clergy’s word for the unconverted -> Rodrigues’s "
                "borrowed sneer -> the remainder is a cult the clergy "
                "stopped trying to absorb",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Terreiro Means "
                "Place and Jurisdiction",
                "Both treat the standing house as a jurisdiction that "
                "does not dissolve because the surrounding city is "
                "Catholic.",
                "Animismo defines the place; this unit names the violences "
                "the place outlasted.",
            ),
            (
                "Lasnet, Senegalese Animism — One Does Not Leave Ancestral "
                "Land Voluntarily",
                "Both refuse absorption as the natural end of a cult under "
                "pressure.",
                "Serer refusal is not to leave the land; Gêge-Nagô refusal "
                "is not to become the master’s church after being taken.",
            ),
        ),
    },
    {
        "n": 25,
        "title": "Police Destroy Altars Without Charge",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Como é que a polícia, estando todos os dias a suprimir "
            "templos, destruir ídolos e altares, a prender os diretores de "
            "candomblé, não chegou até hoje a promover a punição legal de "
            "um só desses crimes? Concedamos que haja devassidões nos "
            "candomblés. Esses atos nem constituem todo o culto, nem mesmo "
            "a essência do culto gêge-nagô."
        ),
        "roman": roman(
            "polícia",
            "suprimir templos",
            "diretores de candomblé",
            "essência do culto gêge-nagô",
        ),
        "tr": (
            "How is it that the police, being every day engaged in "
            "suppressing temples, destroying images and altars, arresting "
            "the directors of candomblé, have not to this day managed to "
            "bring legal punishment for a single one of these \"crimes\"? "
            "Let us grant that there are disorders in the candomblés. "
            "Those acts constitute neither the whole cult nor even the "
            "essence of the Gêge-Nagô cult."
        ),
        "comm": (
            "The civic claim is a contradiction the police live in: they "
            "destroy temples and altars, arrest directors, and never "
            "secure a legal punishment for the \"crimes\" they invent. "
            "And even if disorders happen, those acts are not the cult and "
            "not its essence. The house is not the raid. Rodrigues, "
            "physician and criminal anthropologist, can see the empty "
            "docket and still say crimes and devassidões — debaucheries — "
            "sexual and racial panic sitting on the sentence. Poison. We "
            "do not teach Cap. IX. We do not teach \"crime\" as a face of "
            "the cult. Keep his question and refuse his dump. The "
            "ethnographic remainder is the essence-clause. Gêge-Nagô cult "
            "has an essence that is not the police inventory and not the "
            "scandal the newspaper wants. Animismo’s peji is the house of "
            "the orisa; a destroyed altar is a destroyed house, not a "
            "cleaned crime scene. Lasnet’s woods are sanctuaries; Bahia’s "
            "sanctuaries are raided without a charge. Existentially, when "
            "you hear raid, you ask what altar was broken and what charge "
            "was filed. If the charge is missing, the violence was the "
            "event. Do not complete the missing charge with your own "
            "suspicion."
        ),
        "prac": (
            "Today, when you hear raid, raid, or \"they finally shut that "
            "place down,\" ask what altar or room was broken and what "
            "charge was filed. If you cannot name the charge, do not "
            "supply a crime."
        ),
        "terms": kt(
            (
                "essência do culto",
                "essence of the Gêge-Nagô cult -> not the disorders, not "
                "the police file -> \"candomblé means crime\" is the "
                "smear this sentence already refuses",
            ),
            (
                "devassidões",
                "disorders / debaucheries Rodrigues will \"grant\" -> "
                "sexual-racial panic -> even he says they are not the "
                "cult; do not make them the lesson",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — The Peji Is the "
                "House of the Orisa",
                "Both treat the altar-house as the cult’s location; "
                "destroying it is an attack on a house, not a cleanup.",
                "Animismo describes the peji standing; this unit describes "
                "the peji being destroyed without a legal crime.",
            ),
            (
                "Lasnet, Senegalese Animism — The Woods Are Sanctuaries",
                "Both know a sacred place the surrounding power does not "
                "get to redefine as vacant land.",
                "Serer woods remain sanctuaries in place; Bahian temples "
                "are suppressed daily and still are not convicted.",
            ),
        ),
    },
    {
        "n": 26,
        "title": "Catholic Saints Sit with African Powers",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Não posso voltar aqui à minuciosa demonstração que dei, no "
            "Animisme fetichiste, do modo por que na Bahia os Negros "
            "fetichistas se convertem ao Catolicismo. As notícias sobre "
            "candomblés fornecem novas demonstrações do modo por que, no "
            "culto africano, os santos católicos se associam aos fetiches "
            "negros."
        ),
        "roman": roman(
            "Animisme fetichiste (cross-reference)",
            "santos católicos",
            "culto africano",
            "associação",
        ),
        "tr": (
            "I cannot return here to the detailed demonstration I gave, in "
            "the Animisme fetichiste, of the way in which in Bahia African "
            "devotees convert to Catholicism. The reports on candomblés "
            "supply new demonstrations of the way in which, in the African "
            "cult, Catholic saints associate with African powers."
        ),
        "comm": (
            "The historical claim is association, not replacement: in the "
            "African cult, Catholic saints sit with African powers. "
            "Conversion, as Rodrigues described it in the 1900 French "
            "book, does not empty the peji. New candomblé reports show the "
            "same sitting-together. The saint is not the orisha’s death. "
            "Rodrigues cannot say this without Negros fetichistas and "
            "fetiches negros — the poison vocabulary that makes "
            "association a contamination of true Church by fetish. Refuse "
            "fetish as doctrine. Keep the sitting-together. Animismo "
            "already said orisa is translated as saint, and that Creoles "
            "identify an orisa with Christ. This later book points back "
            "and adds: the news from the houses keeps proving the "
            "association. Johnson’s one God in many towns does not need "
            "Rome; Bahia’s houses use Rome’s names without surrendering "
            "the court. Existentially, you catch just a saint in your "
            "mouth when the house also names an orisha. If you only hear "
            "the Catholic name, you have attended the overlay and missed "
            "the association. Two names on one altar are not one name "
            "winning."
        ),
        "prac": (
            "Today, catch just a saint or just folklore in your mouth "
            "when a house also keeps another name. Write both names if "
            "you know them. If you know only one, write that the other "
            "is being hidden from you — including by you."
        ),
        "terms": kt(
            (
                "associam",
                "saints associate with African powers -> sitting-together "
                "in the African cult -> \"conversion\" as replacement, or "
                "\"syncretism\" as confusion, both miss the verb",
            ),
            (
                "fetiches negros",
                "Rodrigues’s poison for the African powers -> refuse as "
                "doctrine -> the remainder is named orishas and Jeje "
                "powers the saint sits beside",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — Orisa Is "
                "Translated as Saint",
                "Both describe the Catholic name as a translation sitting "
                "on an orisha, not as the orisha’s deletion.",
                "Animismo gives the translation rule; this unit says later "
                "candomblé news keeps demonstrating the association.",
            ),
            (
                "Nina Rodrigues, O Animismo Fetichista — Creoles Identify "
                "an Orisa with Christ",
                "Both refuse to treat a Christian name as proof that the "
                "court has been dismissed.",
                "Animismo names Christ and Allah as overlay names; this "
                "sentence generalizes saints sitting with African powers.",
            ),
        ),
    },
    {
        "n": 27,
        "title": "Fetish Is Not the Terreiro",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Coisa bem diversa é o que afirmo quando me refiro à "
            "persistência do fetichismo negro. Para confundir coisas tão "
            "distintas era necessário tomar, pela situação fetichista do "
            "momento, uma ou algumas das formas cultuais em que se "
            "concretiza essa atitude mental. Os negros Bantus que, na "
            "África, não praticam nem conhecem essa religião, devem ser "
            "tidos naturalmente por monoteístas? Desprezando este modo "
            "superficialíssimo de ver as coisas..."
        ),
        "roman": roman(
            "fetichismo negro (period term, refused as doctrine)",
            "formas cultuais",
            "Bantus",
            "atitude mental",
        ),
        "tr": (
            "What I affirm when I refer to the persistence of Black "
            "\"fetishism\" is a quite different thing. To confuse things "
            "so distinct one would have to take, for the fetishist "
            "situation of the moment, one or another of the cult-forms in "
            "which that mental attitude is concretized. The Bantu Africans "
            "who, in Africa, neither practice nor know this religion — "
            "are they to be taken naturally as monotheists? Discarding "
            "this most superficial way of seeing things..."
        ),
        "comm": (
            "The philosophical claim, cleaned, is a refusal of one-form "
            "thinking: a Gêge-Nagô terreiro is not the whole of African "
            "religion, and Bantu life is not monotheism by default because "
            "it is not this terreiro. One cult-form is not a mental "
            "attitude of a Race. Rodrigues is trying to save his word "
            "fetichismo by making it a deep attitude and the terreiro only "
            "one surface. Keep the distinction of forms; refuse the mental "
            "attitude and the ranking. Poison: fetishism as a stage, "
            "monotheism as the higher grade, Bantu scored against Nagô, "
            "Cap. VIII waiting in the next room. We do not teach the "
            "ladder. The ethnographic remainder is plural African "
            "religion. Nagô and Jeje organized a public cult in Bahia. "
            "Bantu nations have their own houses and are not empty theists "
            "waiting for a grade. Malê Islam is another organization. "
            "Lasnet already said animism is not fetishism. Animismo "
            "already said the figures are neither fetish nor idol. "
            "Existentially, you refuse the ladder that makes one African "
            "religion the measure of another. If you only respect the "
            "house that looks like a terreiro, you have taken one "
            "cult-form for the whole sky."
        ),
        "prac": (
            "Today, catch fetish, primitive, or \"they don’t really have "
            "religion\" in your mouth about a people whose house is not "
            "the one you know. Write the house you do not know instead of "
            "the grade."
        ),
        "terms": kt(
            (
                "fetichismo",
                "Rodrigues’s period word for a supposed mental attitude -> "
                "poison when taught as doctrine -> keep only the warning "
                "not to take one cult-form for a people’s whole religion",
            ),
            (
                "Bantus",
                "nations who, he says, do not practice this Gêge-Nagô "
                "religion in Africa -> not therefore monotheists by "
                "default -> ranking them against Nagô is the ladder we "
                "refuse",
            ),
        ),
        "res": res(
            (
                "Lasnet, Senegalese Animism — Animism Is Not Fetishism",
                "Both refuse fetish as the name of a people’s religion, "
                "and refuse one metropolitan word as the whole field.",
                "Lasnet’s denial is cosmological (souls, not fetishes); "
                "this unit denies that one Bahian cult-form is all African "
                "religion, or that Bantu life is leftover monotheism.",
            ),
            (
                "Nina Rodrigues, O Animismo Fetichista — The Figures Are "
                "Neither Fetish nor Idol",
                "Both pry the word fetish off a real liturgical object or "
                "house.",
                "Animismo defends the figure in the peji; this unit "
                "defends the plurality of African religions against one "
                "peji used as a racial type.",
            ),
        ),
    },
    {
        "n": 28,
        "title": "Three Channels After the Organized Cult",
        "src": "Rodrigues, Os Africanos, cap. VII",
        "pt": (
            "Três são as vertentes de atividades psíquica que se oferecem, "
            "no Brasil, à satisfação do sentimento religioso: 1º, a "
            "atividade religiosa na adaptação fetichista do culto "
            "católico; 2º, a sobrevivência religiosa africana, nas "
            "superstições e magias populares; 3º, a atividade curativa e "
            "criminal dos feitiços."
        ),
        "roman": roman(
            "adaptação do culto católico",
            "sobrevivência religiosa africana",
            "feitiços (refused as the third face of the cult)",
        ),
        "tr": (
            "Three are the channels of psychic activity that offer "
            "themselves, in Brazil, to the satisfaction of religious "
            "feeling: first, religious activity in the \"fetishist\" "
            "adaptation of Catholic cult; second, African religious "
            "survival in popular superstitions and magics; third, the "
            "curative and criminal activity of spells."
        ),
        "comm": (
            "The historical claim, cleaned, is two real channels and a "
            "dump. First: African religious life adapted inside Catholic "
            "cult — saints sitting with powers, Mass then the dead, the "
            "overlay that does not empty the peji. Second: African "
            "survival in popular remainder — herbs, proverbs, Mboi-tatá "
            "rumors, the unorganized afterlife of nations. Those two are "
            "historical. Third — curative and criminal activity of spells "
            "— is Rodrigues’s criminal-anthropology chute. Refuse it as "
            "the third face of the cult. Do not teach crime as liturgy. "
            "Cap. IX is out of the classroom. He writes atividades "
            "psíquica and fetichista and feitiços because the physician "
            "needs a pathology to complete a triad. Poison. Keep the two "
            "doors you can actually walk: the Catholic adaptation and the "
            "popular remainder beside the organized Gêge-Nagô house this "
            "chapter has been describing. Animismo’s cowries name the "
            "saint in a standing terreiro; channel two is what leaks into "
            "the street when the terreiro is not the only mouth. Lasnet "
            "refuses fetish as the religion; we refuse crime as its third "
            "outlet. Existentially, you keep the two houses you can "
            "actually enter — the church that adapted, the popular "
            "remainder that still speaks — and you do not accept crime as "
            "the third door. If someone offers you a third face called "
            "sorcery-as-essence, you are being handed the police file "
            "bound as a theology."
        ),
        "prac": (
            "Today, name two channels of a tradition you actually meet — "
            "a public house and a popular remainder. If a third is offered "
            "as crime, devil, or \"the real dark stuff,\" refuse that "
            "door. Write the refusal in one sentence."
        ),
        "terms": kt(
            (
                "adaptação",
                "adaptation of Catholic cult -> channel 1, saints with "
                "African powers -> not a failed conversion and not the "
                "whole story",
            ),
            (
                "sobrevivência",
                "African religious survival in popular remainder -> "
                "channel 2 -> \"superstition\" is Rodrigues’s bin for "
                "unorganized life we still have to hear as remainder, not "
                "as trash",
            ),
            (
                "atividade criminal",
                "channel 3 in Rodrigues’s triad -> criminal-anthropology "
                "dump -> do not teach crime as the third face of the cult",
            ),
        ),
        "res": res(
            (
                "Nina Rodrigues, O Animismo Fetichista — The Cowries Name "
                "the Saint",
                "Both keep a standing liturgical instrument in an "
                "organized house — the channel this triad does not get to "
                "replace with crime.",
                "Animismo ends on a named reading in the terreiro; this "
                "unit maps what leaks beside that house and refuses the "
                "police third.",
            ),
            (
                "Lasnet, Senegalese Animism — Animism Is Not Fetishism",
                "Both refuse a metropolitan dump-category — fetish, crime "
                "— as the essence of a people’s religion.",
                "Lasnet denies fetish as Serer religion; this unit denies "
                "criminal spells as the third face of Afro-Brazilian cult.",
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
        {"kind": "original", "label": "Original", "body": u["pt"]},
        {"kind": "iast", "label": "Romanization", "body": u["roman"]},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"AFRIC_{n:03d}",
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
        "original": u["pt"],
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
