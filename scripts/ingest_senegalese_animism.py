#!/usr/bin/env python3
"""Ingest Serer *cosaan* (Senegalese / Senegambian animism) from PD ethnography.

Public-domain sources:
  Alexandre Lasnet, *Une mission au Sénégal* (Paris: Challamel, 1900)
  L.-J.-B. Bérenger-Féraud, *Les peuplades de la Sénégambie* (Paris: Leroux, 1879)

English is a Pratibha rendering (pd_adapted). French observer sentences are the
Original when no Serer speech survives in the source. Gravrand is not used
(not PD). Boilat 1853 is the preferred local-author witness, but the available
Google scan was unusable in this pass.

Units 1–10 rewrite existing strong-draft commentaries into modern
pratibha_layers. Units 11+ add genuine Lasnet / Bérenger teachings (philosophy,
not medical catalog). Colonial contempt is not adopted as doctrine.

Floor: ≥28 units. Ten tts_key heroes.
"""
from __future__ import annotations

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/senegalese_animism")
SLUG = "senegalese_animism"
COLL = "Senegalese Animism"
THEMES = ["serer", "roog", "pangool", "living land", "senegambia"]
ROMAN = "French ethnographic report of Serer oral teaching"

PROV = (
    "English is a Pratibha rendering (pd_adapted) from Alexandre Lasnet, "
    "*Une mission au Sénégal* (Paris: Challamel, 1900) and L.-J.-B. Bérenger-Féraud, "
    "*Les peuplades de la Sénégambie* (Paris: Leroux, 1879), both public domain. "
    "Gravrand is not used (not PD). Boilat 1853 is named as preferred local-author "
    "witness but the available Google scan was unusable in this pass."
)
NOTE = (
    "Serer *cosaan* (tradition) is oral. There is no indigenous written scripture "
    "analogous to a sūtra. French observer sentences stand as Original where no "
    "Serer speech survives in the PD sources. The layers restore the philosophical "
    "claim without adopting colonial contempt, racial ranking, or 'fetish' as teaching. "
    "Key Serer terms kept in the Key Terms layer: Roog, Koch, Takhar, Tiurakh, "
    "mammam, pangool, gisanekal, Fitaure, Bante."
)

# Ten hero verses — mandala quotes + pre-baked Listen.
HEROES = {1, 2, 4, 5, 6, 9, 10, 11, 17, 28}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


UNITS: list[dict] = [
    {
        "n": 1,
        "title": "The Invisible Master Is Named as the Sky",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "Les Sérères croient à l'existence d'un être invisible, maître de toutes "
            "choses, qui habite le ciel au-dessus des nuages et qui voit avec "
            "satisfaction les hommes pratiquer le bien; ils le désignent du même nom "
            "que le ciel, rog sérère, koch none."
        ),
        "roman": (
            f"{ROMAN}. Key Serer terms: Rog / Roog (Serer-Sine: sky, God); "
            "Koch / Koox (Serer-Noon / Cangin: the same supreme being)."
        ),
        "tr": (
            "There is an invisible master of all things. That master inhabits the sky "
            "above the clouds, sees human conduct, and takes satisfaction in those who "
            "practice the good. The Serer name this master with the same word they use "
            "for the sky itself: Rog among the Sine, Koch among the Noon."
        ),
        "comm": (
            "The claim is that the highest principle is not an idol, not a carved object, "
            "and not a tribal mascot, but an invisible sovereignty coextensive with the "
            "sky. Lasnet's counterintuitive report — against the colonial habit of calling "
            "everything \"fetish\" — is that the Serer already possess a philosophical "
            "theism: one unseen master of all things. The further precision is linguistic. "
            "God and sky share a name. This is not a failure to distinguish meteorology "
            "from metaphysics. It is a refusal to locate the absolute in a manufactured "
            "image. The sky is the nearest analog of what cannot be pictured: height "
            "without a summit, presence without a statue, seeing without being seen. "
            "Serer later sources (not used here because they are not public domain) call "
            "this being Roog Sene, \"Roog the Immensity.\" Even in Lasnet's thinner 1900 "
            "notice the structure is already visible: invisibility, totality, moral regard, "
            "and a name that cannot be reduced to a cult-object. Delafosse will add the "
            "regional key: a creator God of this type is a cosmogonic-philosophical "
            "concept more than a liturgical addressee. The Serer confirm that pattern from "
            "the ground: they know the master of all things, and they do not confuse that "
            "knowledge with a temple of Roog. Existentially, the passage trains a "
            "distinction most religious cultures blur. The highest is not the most "
            "available. What is named as the sky is precisely what you cannot grasp, "
            "bargain with, or display. To \"practice the good\" is therefore not a private "
            "spirituality aimed at capturing God, but a way of living under a gaze that "
            "needs no shrine. The first philosophical act of Senegalese animism, in this "
            "source, is negative: do not make an image of the sky."
        ),
        "prac": (
            "Stand where you can see open sky. For three minutes do not pray to it and do "
            "not photograph it. Let the sky be the analog of what you cannot make into an "
            "object. Then name one ordinary good you will practice today as if it were "
            "already seen."
        ),
        "terms": kt(
            (
                "Rog / Roog",
                "Serer word for sky and for the supreme being -> God is not a being in "
                "the sky so much as the sky-name of the invisible master -> translating "
                "only as \"God\" loses the refusal of images; translating only as \"sky\" "
                "loses moral sovereignty",
            ),
            (
                "Koch / Koox",
                "Noon / Cangin name of the same supreme being (Lasnet: koch none) -> the "
                "Noon are among the Serer groups most resistant to conversion in the PD "
                "sources -> default \"local deity\" misses that this is the same "
                "philosophical absolute under another language",
            ),
            (
                "être invisible",
                "invisible being -> Lasnet's phrase already blocks idol-theory: the master "
                "is not the tree, the stone, or the gris-gris -> reducing the religion to "
                "\"fetishism\" contradicts the opening sentence of the very source that "
                "was supposed to prove it",
            ),
        ),
        "res": res(
            (
                "Īśāvāsya Upaniṣad 1",
                "Both begin from a totality that already envelops the world, so that the "
                "sacred is not added to objects but recognized as their covering.",
                "The Upaniṣad names that covering as the Lord (īśā) in a Vedic-renunciatory "
                "key; Serer teaching names it as the sky and then, in practice, withholds "
                "direct cult from it.",
            ),
            (
                "Dào Dé Jīng 1 and 25",
                "Both refuse a graspable name for the highest and use a cosmic analog "
                "(way, sky) rather than a statue.",
                "Daoist emptiness is non-theistic; Serer Rog remains a master who regards "
                "the good.",
            ),
        ),
    },
    {
        "n": 2,
        "title": "One Does Not Address God; One Addresses the Spirits",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "Ils croient surtout aux esprits, mammam, et ne s'adressent jamais à Dieu; "
            "ces esprits sont très nombreux, il y a le génie de la forêt, des champs, "
            "de la fontaine, du village, de la case, etc."
        ),
        "roman": (
            f"{ROMAN}. Key Serer terms: mammam (spirits actually addressed); "
            "pangool (later Serer name for ancestral and other-than-human intercessors)."
        ),
        "tr": (
            "They believe above all in the spirits, mammam, and they never address "
            "themselves to God. These spirits are very numerous: there is the genius of "
            "the forest, of the fields, of the spring, of the village, of the house, "
            "and so on."
        ),
        "comm": (
            "The claim is hierarchical and liturgical at once: the absolute is known, and "
            "the absolute is not the addressee of ordinary prayer. Lasnet's sentence is "
            "the hinge of Senegalese animist philosophy as the PD sources can state it. "
            "Belief \"especially\" (surtout) in the spirits does not cancel the previous "
            "unit's invisible master; it locates where relationship happens. You do not "
            "shout at the sky. You speak where life is locally thick — forest, field, "
            "fountain, village, house. This is the opposite of atheism and the opposite "
            "of idolatry. It is mediation. Later Serer language names the mediators "
            "pangool: sanctified ancestors and other-than-human powers who stand between "
            "the living and Roog. Lasnet's mammam is the 1900 ethnographic word for that "
            "populated middle. Each place has a genius because each place is a life, not "
            "a dead backdrop. The house is not spiritually empty until you import a god "
            "into it. The house already has a spirit because dwelling is already a "
            "relation. Delafosse's pan-African analysis fits the Serer report with unusual "
            "exactness: the creator is a cosmogonic idea; cult belongs to souls that are "
            "free to act in the near world — the dead, and the localized souls of land "
            "and water. The \"never\" of ne s'adressent jamais à Dieu is therefore not "
            "neglect. It is reverence. Direct address would treat Roog as a department, a "
            "patron you can corner. The spirits are how a world that is alive can be "
            "spoken to without reducing the sky to a customer. Existentially, the teaching "
            "cuts two modern errors. One is that God must be constantly accosted or "
            "religion has failed. The other is that matter is mute. Senegalese animism, "
            "in this source, says: keep the highest high, and keep the near world "
            "addressable. Practice happens in the middle."
        ),
        "prac": (
            "Today, do not address a remote absolute. Address what is actually near: the "
            "room, the water you drink, the ground you cross. Silently acknowledge each "
            "as already inhabited. Ask nothing of God-as-sky. Keep the highest high by "
            "speaking to the middle."
        ),
        "terms": kt(
            (
                "mammam",
                "Lasnet's term for the spirits the Serer actually address -> the "
                "operational divine, not the philosophical absolute -> \"ghosts\" is too "
                "thin; \"gods\" is too Olympian; they are local personal powers of places "
                "and dwellings",
            ),
            (
                "pangool",
                "Serer ancestral and saintly spirits (not named in Lasnet; the structure "
                "is already here) -> later sources make explicit that one reaches Roog "
                "through the pangool -> using only \"ancestors\" misses that some pangool "
                "are other-than-human and tied to land",
            ),
            (
                "ne s'adressent jamais à Dieu",
                "they never address themselves to God -> liturgical withholding, not "
                "unbelief -> English \"they don't pray\" is false; they pray, but not to "
                "Roog as if Roog were a nearby specialist",
            ),
        ),
        "res": res(
            (
                "Pratyabhijñāhṛdayam 1–2",
                "Both distinguish a sovereign ground from the forms in which that ground "
                "becomes approachable.",
                "Kashmir Śaiva teaching identifies the ground with consciousness itself; "
                "Serer teaching keeps Roog unaddressed and routes practice through local "
                "spirits.",
            ),
            (
                "Shinto kami of spring, grove, and house",
                "Both populate springs, groves, and dwellings with addressable presence "
                "rather than emptying the world for a distant God.",
                "Shinto has shrine architecture and a written mythic corpus; Serer address "
                "in this source is tree, stone, and household, without a temple of Roog.",
            ),
        ),
    },
    {
        "n": 3,
        "title": "Libation at the Baobab and the Consecrated Stone",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "Ils résident volontiers dans certains arbres comme le baobab; pour se les "
            "rendre favorables on fait au pied des arbres ou sur des pierres consacrées "
            "des libations de lait ou d'eau coupée de farine de mil et parfois des "
            "sacrifices d'animaux, les prémices de la récolte leur sont toujours offertes."
        ),
        "roman": (
            f"{ROMAN}. Practice terms: baobab as spirit-dwelling; libation of milk or "
            "millet-water; consecrated stones (pierres consacrées); first-fruits (prémices)."
        ),
        "tr": (
            "The spirits willingly reside in certain trees, such as the baobab. To render "
            "them favorable, one makes, at the foot of the trees or upon consecrated "
            "stones, libations of milk or of water mixed with millet flour, and sometimes "
            "animal offerings. The first-fruits of the harvest are always offered to them."
        ),
        "comm": (
            "The claim is that favor is not purchased from a sky-god but cultivated where "
            "a spirit already dwells. The baobab is not a symbol of the spirit; it is a "
            "residence. Lasnet's verb is résident: they live there. Practice therefore has "
            "a topology. You do not close your eyes and send a wish upward. You go to the "
            "foot of the tree or to a stone that has been set apart (pierres consacrées) "
            "and you pour. The materials are ordinary and exact: milk, or water cut with "
            "millet flour. This is not spectacle. It is the household's own food-world "
            "returned at the root of the tree that outlives households. Millet is the "
            "staple; water is life; milk is increase. To pour them is to admit that the "
            "harvest and the herd were never only yours. The \"always\" of first-fruits — "
            "leur sont toujours offertes — makes the rite structural rather than "
            "occasional. Before the human eats as owner, the spirits eat as hosts. "
            "Bérenger-Féraud's 1879 chapter confirms the same tree-sanctuary from another "
            "observer: the great trees of the forest are the Serer's venerated sanctuaries "
            "because Takhar and Tiurakh inhabit them. The two PD sources agree on the "
            "practice even when they disagree on pantheon names. That agreement is what "
            "makes the rite usable: libation at tree and stone is the public form of "
            "Senegalese animist relation. Existentially, the teaching is anti-abstraction. "
            "Gratitude that never leaves the head is not this religion. The body has to "
            "carry milk to a root. The stone has to be one stone, not \"nature in "
            "general.\" Animism here is not a mood about Gaia; it is a repeated pouring "
            "at a particular foot of a particular tree."
        ),
        "prac": (
            "Take water (or milk if you have it). Choose one actual tree or one stone you "
            "will return to, not \"nature.\" Pour a little at its foot. Say, inwardly, "
            "that the first of what sustains you is not yours to keep. Do not perform this "
            "as a spell for gain. Perform it as the admission that the place is already "
            "inhabited."
        ),
        "terms": kt(
            (
                "baobab",
                "the great tree of the Senegambian landscape, a preferred dwelling of "
                "spirits in Lasnet -> not a metaphor for strength; a house of the mammam "
                "-> \"sacred tree\" in tourist English misses that residence, not "
                "decoration, is the point",
            ),
            (
                "pierres consacrées",
                "consecrated stones -> a stone can be set apart as an addressable surface "
                "-> not every stone is sacred; consecration localizes the infinite middle "
                "of unit 2",
            ),
            (
                "prémices",
                "first-fruits of the harvest, always offered -> the economic theology of "
                "animism: increase is answered before it is stored -> \"tithe\" is too "
                "fiscal; this is the first taste returned to the dwellers of the land",
            ),
        ),
        "res": res(
            (
                "Hebrew Bible, first-fruits and standing stones (Exodus 23:19; Genesis 28:18)",
                "Both mark land-relation by offering the first of the yield and by setting "
                "a stone as a witness.",
                "Biblical first-fruits go to YHWH through priesthood; Serer first-fruits "
                "go to the local spirits who actually inhabit the field and tree.",
            ),
            (
                "Shinto offerings at a shinboku (marked tree)",
                "Both treat a marked tree as a dwelling and pour or present ordinary "
                "life-stuff there.",
                "Shinto shrine protocol is highly formalized; Lasnet's Serer rite is "
                "household-agricultural and described without a temple staff.",
            ),
        ),
    },
    {
        "n": 4,
        "title": "Takhar of Justice, Tiurakh of Increase",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Ils ont deux Dieux; d'une part Takhar qui préside à la justice, d'autre "
            "part Théourakh qui dispose de tous les biens. Ces deux dieux habitent dans "
            "les plus grands arbres des forêts, de sorte que les bois sont pour les "
            "Sérères des lieux sacrés, et les arbres séculaires des sanctuaires vénérés. "
            "Le Théourackh est le Dieu qui donne d'abondantes récoltes, fait prospérer "
            "les familles, les individus et les troupeaux. On le rend favorable à sa "
            "maison en déposant auprès de certains arbres désignés, des cadeaux."
        ),
        "roman": (
            f"{ROMAN}. Key Serer theonyms as recorded in 1879 French: Takhar (justice); "
            "Théourakh / Théourackh (later spelling Tiurakh / Tulrakh, wealth and increase)."
        ),
        "tr": (
            "They have two Gods: on one side Takhar, who presides over justice; on the "
            "other Tiurakh, who disposes of all goods. These two gods inhabit the greatest "
            "trees of the forests, so that the woods are sacred places for the Serer, and "
            "the age-old trees venerated sanctuaries. Tiurakh is the God who gives "
            "abundant harvests and makes families, persons, and herds prosper. One renders "
            "him favorable to one's house by depositing gifts beside certain designated "
            "trees."
        ),
        "comm": (
            "The claim is that the inhabited middle of Serer religion is not a chaos of "
            "\"fetishes\" but a moral-economic pair. Takhar is justice. Tiurakh is "
            "increase. Bérenger-Féraud, for all his colonial disdain in the surrounding "
            "paragraphs, records a theology with a clear axis: rightness and prosperity "
            "are distinct powers, both tree-dwelling, both approached in the forest. This "
            "complements Lasnet rather than canceling him. Lasnet recorded the unaddressed "
            "sky-God (Rog / Koch) and the many mammam. Bérenger recorded two named powers "
            "inside that many. Read together, the PD dossier gives a three-tier map: Roog "
            "as invisible master; Takhar and Tiurakh as named departmental sovereignties "
            "of justice and goods; countless local spirits of spring, field, and house. "
            "The forest as sanctuary follows from dwelling. If justice and increase "
            "inhabit the greatest trees, then to enter the woods is already to enter a "
            "court and a granary. \"Sacred grove\" is not romantic scenery. It is "
            "institutional space without masonry. The age of the tree matters: arbres "
            "séculaires — beings that have already outlasted human lawsuits and harvests. "
            "Justice that lives in a centuries-old tree is not the justice of the latest "
            "strong man. Increase that lives there is not identical with this year's "
            "profit. Existentially, the pairing is a check on spiritual greed. A religion "
            "of only Tiurakh would be a prosperity cult. A religion of only Takhar would "
            "be ordeal and fear. Senegalese animism, in this source, holds both: you may "
            "ask for the herd to multiply, and you still live under a justice that is not "
            "yours to administer as appetite. Gifts at the designated tree are how a house "
            "stays in relation to increase without pretending to own the source."
        ),
        "prac": (
            "At day's end, sort one event into Takhar or Tiurakh: was this about "
            "rightness, or about increase? Do not let the desire for goods write the "
            "verdict of justice. If you ask for increase, name a corresponding rightness "
            "you will keep."
        ),
        "terms": kt(
            (
                "Takhar",
                "Serer power who presides over justice (Bérenger 1879) -> later sources "
                "also call Takhar the god of vengeance or just retribution -> "
                "\"judge-god\" in a Greco-Roman sense over-personalizes; Takhar is "
                "justice as a living forest presence",
            ),
            (
                "Théourakh / Tiurakh",
                "the god who disposes of all goods, abundant harvests, family and herd "
                "prosperity -> not a devil of materialism; increase as a sacred power -> "
                "\"wealth god\" in a modern market sense misses that the gift is deposited "
                "at a tree for the house, not accumulated as capital",
            ),
            (
                "sanctuaires vénérés",
                "venerated sanctuaries -> the sanctuary is the age-old tree -> \"temple\" "
                "imports walls the PD sources say the Serer do not build for Roog",
            ),
        ),
        "res": res(
            (
                "Plato, Republic I–II (justice vs. advantage)",
                "Both refuse to collapse justice into whatever produces goods.",
                "Plato argues dialectically in a city; Serer teaching locates the "
                "distinction in two tree-dwelling powers.",
            ),
            (
                "Bhagavad Gītā 3.10–3.13 (sacrifice and the cycle of increase)",
                "Both bind prosperity to offering rather than to seizure.",
                "The Gītā's rite is Vedic-devotional toward a cosmic yajña; Tiurakh is "
                "approached at designated trees for the house.",
            ),
        ),
    },
    {
        "n": 5,
        "title": "The Soul Continues; Watch the Sky at Death",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "Les Sérères croient à une vie future et à la métempsycose, aussi quand "
            "l'un d'eux vient de mourir, ils examinent aussitôt le ciel et, s'ils voient "
            "voler un oiseau, ils sont pleins de joie, car ils pensent que l'âme du "
            "défunt est entrée dans son corps."
        ),
        "roman": (
            f"{ROMAN}. Practice: immediately after a death, look at the sky; a bird in "
            "flight is read as the soul's passage (métempsycose)."
        ),
        "tr": (
            "The Serer believe in a future life and in metempsychosis. So when one of "
            "them has just died, they at once examine the sky, and if they see a bird "
            "flying, they are full of joy, because they think the soul of the deceased "
            "has entered its body."
        ),
        "comm": (
            "The claim is that death is not annihilation and not only a departure \"up\" "
            "to Roog. The soul continues, and it may continue as a bird. Lasnet's word "
            "métempsycose is the French philosophical term for transmigration. What "
            "matters is the practice that follows from it: at the moment of death, "
            "attention goes to the sky. The same sky that names Roog is now scanned for "
            "a living sign that the person has taken another body of motion. Joy at the "
            "bird is theologically precise. If the soul can enter a bird, the dead are "
            "not trapped in the corpse and not erased. The corpse can be washed, oiled, "
            "spoken to (next unit); the soul may already be in flight. Watching the sky "
            "is therefore not omen-hunting in a vague sense. It is a metaphysics of "
            "continuity performed with the eyes. The bird is not a symbol of the soul in "
            "the way a poet uses a symbol. In the reported belief, the soul has entered "
            "the bird's body. This also closes a circle with unit 1. The sky is the "
            "master's name and the soul's exit-path. Animism here is not \"everything is "
            "alive\" as a slogan. It is a specific permeability: human soul, bird-body, "
            "sky-field. Delafosse's nia — personal life-soul surviving the corpse, of the "
            "same essence as other beings' souls — is the regional theory of this Serer "
            "joy. Existentially, the rite trains a non-panic attention at the threshold. "
            "The instruction is not \"do not grieve.\" Lasnet's funeral section is full of "
            "cries. The instruction is: look up. See whether life has already taken "
            "another vehicle. Continuity is not an argument you win in a seminar. It is a "
            "bird you might miss if you only stare at the corpse."
        ),
        "prac": (
            "When you next see a bird cross open sky, pause. Without forcing a belief, "
            "let the thought stand: a life-soul can move. Then look back at your own body "
            "and notice it as a current vehicle, not as the whole of what you are."
        ),
        "terms": kt(
            (
                "métempsycose",
                "metempsychosis, transmigration of the soul -> Lasnet's philosophical "
                "label for Serer afterlife belief -> \"reincarnation\" as a later human "
                "birth is narrower than the reported bird-entry",
            ),
            (
                "âme du défunt",
                "soul of the deceased -> a principle that can leave the washed body and "
                "enter a bird -> not the social memory of the person, and not a ghost "
                "stuck in the house by default",
            ),
            (
                "oiseau",
                "bird in flight as possible body of the departed soul -> joy, not fear, "
                "is the correct affect if the bird appears -> a \"bad omen\" reading "
                "inverts the source",
            ),
        ),
        "res": res(
            (
                "Bhagavad Gītā 2.22",
                "Both image the soul as changing garments or vehicles.",
                "The Gītā's garment is typically another human or cosmic birth in karmic "
                "sequence; Lasnet's Serer image is an immediate bird in this sky.",
            ),
            (
                "Phaedo 80c–84b",
                "Both treat death as a separation in which the soul's next state depends "
                "on its nature, and both refuse to equate the person with the corpse.",
                "Plato's soul seeks the intelligible; the Serer report allows the soul a "
                "bird-body in the same sky that names God.",
            ),
        ),
    },
    {
        "n": 6,
        "title": "Speak to the Dead at the Ear",
        "src": "Lasnet 1900, Sérères — Funérailles",
        "fr": (
            "Aussitôt après la mort le corps est soigneusement lavé, couvert d'huile ou "
            "de beurre et enveloppé de pagnes, les femmes poussent des cris et des "
            "gémissements; deux ou trois anciens de la famille prononcent des discours, "
            "puis tous vont successivement faire leurs adieux au décédé et lui parler à "
            "l'oreille. L'enterrement a lieu le jour même du décès, la fosse est creusée "
            "en dehors du village et orientée vers l'est. Aux pieds du mort on place "
            "quelquefois sa pipe, son tabac, de l'eau et un peu de couscous."
        ),
        "roman": (
            f"{ROMAN}. Practice sequence: wash and oil the body; farewell speeches; speak "
            "into the ear of the dead; same-day burial facing east; water and couscous at "
            "the feet."
        ),
        "tr": (
            "Immediately after death the body is carefully washed, covered with oil or "
            "butter, and wrapped in cloths. Two or three elders of the family deliver "
            "speeches, then all go in turn to bid farewell to the deceased and to speak "
            "into his ear. Burial is the same day, the grave dug outside the village and "
            "oriented toward the east. At the feet of the dead one sometimes places a "
            "pipe, tobacco, water, and a little couscous."
        ),
        "comm": (
            "The claim is that the newly dead still hear. Funeral practice is not "
            "disposal. It is the last conversation in the old vehicle, while unit 5 "
            "watches for the soul in the sky. Lasnet's detail — lui parler à l'oreille — "
            "is the most intimate practice in the PD dossier. You do not announce grief "
            "only to the living. You put your mouth to the ear of the washed body and "
            "speak as to someone who is still a someone. Washing, oiling, wrapping are "
            "not hygiene theater. They are honor paid to a body that has hosted a nia "
            "(in Delafosse's Manding term) and may still be listening at the threshold. "
            "Eastward orientation of the grave aligns the body with rising light, the "
            "same sky-axis as Roog. Water and couscous at the feet continue the "
            "food-logic of libation: the dead still belong to the economy of thirst and "
            "grain. The village boundary (en dehors du village) marks a change of "
            "residence, not an expulsion from relation. This unit is how Senegalese "
            "animism handles the hardest philosophical test: is the other still there "
            "when the breath has stopped? The practice answers yes, long enough to speak, "
            "and then yes in another mode (bird, ancestor, pangool). Colonial observers "
            "linger on alcohol and gunshots in the surrounding paragraphs. The usable "
            "core is quieter: wash, oil, speak into the ear, face the body east, leave "
            "water. Existentially, the teaching is against the modern habit of treating "
            "the corpse as a problem for logistics. If you will one day be spoken to in "
            "the ear, you are not only a medical event. And if you will one day have to "
            "speak into an ear, the work of love is verbal presence at a threshold you "
            "cannot control."
        ),
        "prac": (
            "You do not need a death today to train this. Sit with someone living. For "
            "one minute, speak as if the ear is holy — slow, particular, nothing "
            "performative. Then, alone, say one sentence you would want spoken into your "
            "ear at the threshold. Keep it true."
        ),
        "terms": kt(
            (
                "parler à l'oreille",
                "to speak into the ear of the deceased -> the dead as still addressable "
                "in the washed body -> \"saying goodbye\" in a purely sentimental sense "
                "misses the metaphysics: they hear",
            ),
            (
                "orientée vers l'est",
                "grave oriented toward the east -> alignment with rising sky-light, the "
                "Rog-axis -> \"facing east\" as mere custom without the sky-God of unit 1 "
                "is incomplete",
            ),
            (
                "anciens de la famille",
                "family elders who speak first -> speech at death is ordered, not only "
                "raw lament -> priesthood here is kinship seniority",
            ),
        ),
        "res": res(
            (
                "Jewish washing of the dead (taharah) and the refusal to leave a body unattended",
                "Both refuse to treat the body as trash, and both organize speech and care "
                "around the dead as still a someone.",
                "Jewish practice is monotheistic without local tree-spirits; Serer care "
                "sits inside an animist world where the soul may already be a bird.",
            ),
            (
                "Egyptian Opening of the Mouth (structural)",
                "Both treat the dead body as a site where speech and sensory function "
                "must be honored.",
                "Egyptian rite is temple-priestly and afterlife-book based; Serer rite is "
                "family-elders at the house and grave the same day.",
            ),
        ),
    },
    {
        "n": 7,
        "title": "Animism Is Not Fetishism",
        "src": "Lasnet 1900, Sérères — Religion (opening; refusal of idol-theory)",
        "fr": (
            "Les Sérères croient à l'existence d'un être invisible, maître de toutes "
            "choses, qui habite le ciel au-dessus des nuages et qui voit avec "
            "satisfaction les hommes pratiquer le bien; ils le désignent du même nom "
            "que le ciel, rog sérère, koch none. Ils croient surtout aux esprits, "
            "mammam, et ne s'adressent jamais à Dieu."
        ),
        "roman": (
            f"{ROMAN}. Lasnet's opening already blocks idol-theory: an invisible "
            "sky-named master, plus spirits one actually addresses. Bérenger's word "
            "\"idolâtrie\" in the 1879 chapter is colonial taxonomy, not the teaching."
        ),
        "tr": (
            "The Serer believe in an invisible being, master of all things, who inhabits "
            "the sky above the clouds and takes satisfaction in those who practice the "
            "good; they name him with the same word as the sky: Rog, Koch. They believe "
            "above all in the spirits, mammam, and they never address themselves to God."
        ),
        "comm": (
            "The claim is diagnostic: \"fetishism\" is a colonial insult pretending to be "
            "a taxonomy. Lasnet's own opening sentence is already the refutation. The "
            "master is invisible. The master is the sky-name. The master is not addressed. "
            "None of that is a carved object, a charm, or a \"gross\" religion of hardware. "
            "Bérenger, nine years earlier, still opened the same people with \"idolâtrie\" "
            "and \"fétichisme\" and \"childish intelligences.\" That vocabulary is the "
            "observer's poison, not the doctrine. What the doctrine is, Lasnet states "
            "without meaning to theorize: one unseen totality, a populated middle of "
            "place-spirits, and a liturgical withholding from the highest. Later "
            "Delafosse (1925, PD, used here only as a named conceptual key, not as a "
            "base text) will call this animism and refuse fetishism as the name of any "
            "religion. The Serer instance does not need his essay to stand. If the "
            "observer only sees horns, sachets, and trees, the observer has missed the "
            "philosophy the same page records. Existentially, the passage trains "
            "intellectual justice. If you can only see someone else's religion as "
            "hardware — beads, trees, gris-gris — you are looking at Catholicism and "
            "seeing only candles. The practice of study here is to ask, of any rite: "
            "what soul is being addressed, and what highest is being left unaddressed "
            "on purpose? Animism in this collection names that structure: personal "
            "souls, a high God who is thought rather than fed, and a cult that belongs "
            "to the free souls of the dead and of places. Takhar and Tiurakh sit inside "
            "that doctrine as named near-powers, not as a refutation of Roog."
        ),
        "prac": (
            "Pick one object you treat as \"spiritual\" (a necklace, an image, a stone). "
            "Ask: is this the religion, or a tool beside the religion? Then name, without "
            "addressing it, the highest you will not turn into an object today."
        ),
        "terms": kt(
            (
                "fétichisme",
                "colonial name for African religion as object-virtue -> Bérenger uses it "
                "as taxonomy; Lasnet's opening sentence already contradicts it -> using "
                "\"fetish\" as the name of Serer tradition repeats the disdain the "
                "philosophy refuses",
            ),
            (
                "Rog / Roog",
                "sky-name of the invisible master -> the PD proof that the absolute is "
                "not a statue -> \"they worship idols\" cannot survive this naming",
            ),
            (
                "mammam",
                "the addressed middle -> what colonial \"fetish\" collapses into hardware "
                "-> spirits of forest, field, spring, village, house are personal lives, "
                "not consecrated junk",
            ),
        ),
        "res": res(
            (
                "Dionysius the Areopagite, Mystical Theology ch. 1",
                "Both protect the highest from being treated as an object of ordinary "
                "handling.",
                "Christian negative theology still liturgically addresses God; Lasnet's "
                "Serer pattern withholds cult from the creator.",
            ),
            (
                "Islamic tawḥīd versus maraboutic amulets (as a structural pair)",
                "Both can coexist with object-virtue without being identical with it.",
                "Islam names the one God as the addressee of ṣalāt; Serer Rog is known "
                "and not the addressee of daily cult.",
            ),
        ),
    },
    {
        "n": 8,
        "title": "Souls of One Essence in Every Being",
        "src": "Lasnet 1900, Sérères — Religion (spirits of place; soul entering a bird)",
        "fr": (
            "Ils croient surtout aux esprits, mammam, et ne s'adressent jamais à Dieu; "
            "ces esprits sont très nombreux, il y a le génie de la forêt, des champs, "
            "de la fontaine, du village, de la case, etc. Ils résident volontiers dans "
            "certains arbres comme le baobab. Les Sérères croient à une vie future et à "
            "la métempsycose... ils pensent que l'âme du défunt est entrée dans son corps."
        ),
        "roman": (
            f"{ROMAN}. Ontology recovered from Lasnet: mammam of forest, field, spring, "
            "village, house; human soul able to enter a bird. Same-essence language is "
            "the philosophical reading of that populated world."
        ),
        "tr": (
            "They believe above all in the spirits, mammam — genius of the forest, the "
            "fields, the spring, the village, the house — and those spirits willingly "
            "reside in certain trees such as the baobab. They believe in a future life "
            "and in metempsychosis: the soul of the dead may enter the body of a bird. "
            "Personal life is not confined to the human envelope."
        ),
        "comm": (
            "The claim is ontological equality of essence across kinds, plus difference "
            "of office. Lasnet does not write the word essence. He writes a world in "
            "which a forest, a field, a spring, a village, a house, a baobab, a bird, "
            "and a newly dead human are all sites of personal life. That list is already "
            "the doctrine. A person's soul, a baobab's mammam, a spring's génie are the "
            "same sort of thing: addressable life. They are not the same job. While a "
            "living human soul is busy governing its own body, it is not a god. After "
            "death, freed from that inner administration, the same life may take a bird "
            "or become a power the living must reckon with. A field, having no wandering "
            "animal body to run, already has that outward independence — which is why "
            "land-soul and ancestor-soul can fuse, and why the Serer pour at the baobab "
            "rather than at an empty symbol. Later Delafosse will name this nia: personal "
            "life of one essence in the apparently inanimate as well as the animate. The "
            "Senegalese instance does not wait for the Mande word. Libation makes sense "
            "only if the tree has a life. Speaking into the ear makes sense only if the "
            "dead still have a life. Not addressing Roog makes sense if Roog is sky-scale "
            "soul, not a nearby specialist. Existentially, the teaching forbids two "
            "reductions. You may not treat a place as dead stuff. You may not treat a "
            "person as only a body. And you may not treat all souls as interchangeable "
            "helpers. Personality means this tree, this spring, this ancestor — not "
            "\"energy.\" The contemplative implication is severe: relation is always "
            "particular. Animism is the opposite of a blur."
        ),
        "prac": (
            "Walk through one ordinary setting (kitchen, street, field). Name three "
            "distinct beings — a tool or stone, a plant, a person. For each, silently "
            "say \"personal life, not mine.\" Feel the difference between that recognition "
            "and a vague glow of \"everything is one.\""
        ),
        "terms": kt(
            (
                "mammam",
                "spirits of forest, field, spring, village, house -> personal lives of "
                "places, not a generic life-force -> \"energy\" erases personality; "
                "\"god\" overstates department",
            ),
            (
                "âme",
                "soul able to leave a washed body and enter a bird -> the human instance "
                "of the same personal life the baobab already has -> English \"soul\" can "
                "sound Christian-immortal in a different key; here it is movable life",
            ),
            (
                "pangool",
                "later Serer name for the free ancestral and land powers in this middle "
                "-> what the living bind by rite -> not every mammam is an ancestor; some "
                "are other-than-human from the start",
            ),
        ),
        "res": res(
            (
                "Śiva Sūtra I.1 (caitanyam ātmā)",
                "Both refuse to treat awareness or life-principle as a byproduct of matter.",
                "The sūtra identifies consciousness as the Self of all; Lasnet describes "
                "many personal lives of places and birds, not one Self.",
            ),
            (
                "Zhuangzi, butterfly dream / Free and Easy Wandering",
                "Both make the species-boundary permeable to spirit.",
                "Zhuangzi's register is transformation and epistemic play; Serer watching "
                "and pouring are funeral and agricultural epistemology, not play.",
            ),
        ),
    },
    {
        "n": 9,
        "title": "The Ancestor and the Land Are One Cult",
        "src": "Lasnet 1900, Sérères — Mœurs, Organisation sociale; Bérenger 1879, Mœurs",
        "fr": (
            "Les Sérères sont de mœurs douces, très attachés à leur sol, ne songeant "
            "point à faire la guerre et ne s'occupant que de leurs troupeaux et de leurs "
            "cultures. Les notables s'appellent lamanes; ils constituent la classe aisée "
            "et sont seuls propriétaires du sol qu'ils se transmettent de père en fils "
            "et prêtent ou louent aux autres indigènes. Les Sérères sont doux, vivent "
            "sur leur sol auquel ils sont extrêmement attachés... Ils passent volontiers "
            "leur vie là où ils sont nés, groupés par familles dans un pli de terrain "
            "qu'ils ont mis en culture."
        ),
        "roman": (
            f"{ROMAN}. Key structure: attachment to a particular soil; lamane as "
            "land-master transmitting the parcel; family grouped on the fold of land. "
            "Ancestor and land are one cult because the founding dead and the soil are "
            "not two religions."
        ),
        "tr": (
            "The Serer are deeply attached to their soil. They live where they were born, "
            "grouped by families in a fold of land they have put under cultivation. The "
            "notables are called lamanes: they alone own the soil, transmit it from father "
            "to son, and lend or rent it to others. The land-master and the family dead "
            "are not two cults."
        ),
        "comm": (
            "The claim is that ancestor and land are not two religions glued together. "
            "They are one relation seen from two sides. Lasnet's Serer will not leave "
            "their soil voluntarily; those who wander are accused of foreign marriage "
            "and may be refused burial. Bérenger finds the same people grouped by families "
            "in a fold of earth they have made to yield. The lamane is the socio-political "
            "face of that fusion: a living notable who holds the parcel because the "
            "parcel is already a family god. To pour at a baobab on family ground is "
            "therefore not \"nature worship\" plus \"ancestor worship.\" It is one act: "
            "you feed the dwelling-soul of the people who belong to this soil and of the "
            "soil that belongs to those people. Later Delafosse will name the structure "
            "explicitly: the nia of the most distant ancestor merges with the soul of the "
            "ground that ancestor acquired; the priest is the oldest living descendant. "
            "The Senegalese PD dossier already shows the joint without the Mande "
            "etymology. The Fitaure of Bérenger (village religious chief) and the family "
            "anciens of Lasnet's funerals are local forms of that priesthood by seniority. "
            "Existentially, the teaching relocates spirituality from the consumer's "
            "choice of \"a path\" to the question: whose dead, which ground, which living "
            "elder still knows the formulas of this parcel? Even a modern reader far from "
            "a Serer village can take the philosophical point. You do not have a private "
            "sky-God hobby and a separate real-estate life. The soil you live on and the "
            "people you come from are already a cult, whether you have admitted it or "
            "not. Animism makes that admission explicit."
        ),
        "prac": (
            "Name the actual ground you slept on last night and one dead person whose "
            "life made yours possible. Hold them as one relation, not two topics. Offer "
            "a sip of water to the ground, and a sentence of thanks to that dead person, "
            "as a single act."
        ),
        "terms": kt(
            (
                "lamane",
                "Serer land-master (Lasnet: notables who own and lend soil) -> the "
                "socio-political face of the ancestor-land fusion -> \"chief\" in a "
                "colonial administrative sense misses the religious joint with the "
                "soil-soul",
            ),
            (
                "sol",
                "the particular soil, not Earth as a globe-goddess -> Bérenger: a fold of "
                "terrain put under cultivation -> \"Mother Earth\" rhetoric is too large "
                "and too impersonal",
            ),
            (
                "pangool",
                "the free ancestral and land powers fed by that joint cult -> what the "
                "lamane and the family elders stand before -> not a museum of \"ancestors\" "
                "separate from the field",
            ),
        ),
        "res": res(
            (
                "Chinese ancestral cult and she / earth altars",
                "Both fuse lineage dead with a particular earth, and both locate "
                "priesthood in the family rather than in a church of the high God.",
                "Chinese practice has a long written ritual code; this PD Serer account "
                "is oral-familial and land-parcel specific.",
            ),
            (
                "Hebrew land-promise and ancestral tomb",
                "Both bind a people to a ground through the dead.",
                "Biblical religion addresses the high God as the giver of land; Serer "
                "animism in these sources addresses the land-ancestor fusion and leaves "
                "Roog unaddressed.",
            ),
        ),
    },
    {
        "n": 10,
        "title": "To Worship Is to Bind",
        "src": "Lasnet 1900, Sérères — Religion (libation as binding); Bérenger 1879, Bante",
        "fr": (
            "Pour se les rendre favorables on fait au pied des arbres ou sur des pierres "
            "consacrées des libations de lait ou d'eau coupée de farine de mil... les "
            "prémices de la récolte leur sont toujours offertes. On le rend favorable à "
            "sa maison en déposant auprès de certains arbres désignés, des cadeaux."
        ),
        "roman": (
            f"{ROMAN}. Binding-acts in the PD Serer record: libation, first-fruits, "
            "tree-gifts. Later Mande lâ-siri (\"dispositions taken in order to bind\") "
            "names the same grammar; it is not the Serer word."
        ),
        "tr": (
            "To render the spirits favorable, one pours milk or millet-water at the foot "
            "of the trees or upon consecrated stones. The first-fruits of the harvest are "
            "always offered to them. One renders Tiurakh favorable to one's house by "
            "depositing gifts beside certain designated trees. Worship here is a set of "
            "dispositions that bind."
        ),
        "comm": (
            "The claim is that religion is a technology of relation, not a cloud of "
            "beliefs. Lasnet's verbs are already the philosophy: se les rendre favorables, "
            "toujours offertes, déposant des cadeaux. You do not \"have a spirituality.\" "
            "You take dispositions that bind. Bind does not here mean enslave a god like "
            "a demon in a grimoire. It means the same thing re-ligio is often said to "
            "mean: tie back. Milk at the baobab binds house to tree-soul. First-fruits "
            "bind harvest to the field's life. Speech in the ear binds the living to the "
            "newly dead. Gifts at Tiurakh's tree bind increase to the household without "
            "pretending the household generated increase from nothing. Why bind at all, "
            "if souls are personal and free? Precisely because they are personal and "
            "free. A free land-soul or ancestor-soul has temperament, rancor, taste, and "
            "power. Relation that is only inward feeling does not meet a personal other. "
            "Rite is how two personal lives, of one essence but different office, stay "
            "in working order. The Serer \"always\" of first-fruits is a standing bond, "
            "not a mood. Bérenger's Bante will show the same grammar turned to fear: a "
            "soul enclosed in a canari. Binding can bless a house or terrify an enemy. "
            "The definition still holds. Existentially, this judges contemporary "
            "practice. If nothing in your life binds you to a particular dead, a "
            "particular ground, a particular tree or stone, you do not have this religion "
            "even if you admire it. Animism is not an opinion that things are alive. It "
            "is the set of dispositions by which you stay tied to those lives. The sky "
            "remains unbound — Roog is not tied. The middle is what you bind, and by "
            "binding it, you live."
        ),
        "prac": (
            "Choose one bond you have been treating as a feeling (gratitude to a place, "
            "to a dead person, to a household). Give it a disposition: a time, a small "
            "offering, a repeated act. Do it once today. That act, not the opinion, is "
            "the religion."
        ),
        "terms": kt(
            (
                "se les rendre favorables",
                "to render the spirits favorable -> Lasnet's verb of cult -> English "
                "\"worship\" sounds like praise-feeling; this is binding-action",
            ),
            (
                "prémices",
                "first-fruits always offered -> the standing bond, not a mood of thanks "
                "-> without the always, gratitude stays private and the field is treated "
                "as owned",
            ),
            (
                "Bante",
                "later in Bérenger: enclosing a soul in a canari under a consecrated tree "
                "-> the same binding grammar turned to fear -> \"magic\" as a dump-word "
                "misses that this is cult used as constraint",
            ),
        ),
        "res": res(
            (
                "Latin religio as binding / obligation",
                "Both etymologies make religion a tie, not a sentiment.",
                "Roman religio becomes civic-legal; Serer binding in these sources remains "
                "familial-land rite and leaves the sky-God unbound.",
            ),
            (
                "Vedic yajña as maintaining the bond of gods and humans",
                "Both treat offering as what keeps worlds in relation.",
                "Vedic rite is priestly-Sanskrit and addressed to named devas including "
                "high gods; Serer binding in Lasnet ties near souls and leaves Roog "
                "without cult.",
            ),
        ),
    },
    {
        "n": 11,
        "title": "First-Fruits Are Always Offered",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "Pour se les rendre favorables on fait au pied des arbres ou sur des pierres "
            "consacrées des libations de lait ou d'eau coupée de farine de mil et parfois "
            "des sacrifices d'animaux, les prémices de la récolte leur sont toujours "
            "offertes."
        ),
        "roman": (
            f"{ROMAN}. Key term: prémices — first-fruits of the harvest, always offered "
            "to the mammam who dwell in tree and stone."
        ),
        "tr": (
            "To render the spirits favorable, one pours libations of milk or millet-water "
            "at the foot of the trees or upon consecrated stones, and sometimes offers "
            "animals. The first-fruits of the harvest are always offered to them."
        ),
        "comm": (
            "The claim is that increase is answered before it is stored. Lasnet's adverb "
            "is the teaching: toujours. First-fruits are not a festival you throw when "
            "the year was kind. They are a law of relation. Before the house eats as "
            "owner, the dwellers of tree and stone eat as hosts. The contested move is "
            "to refuse the modern sequence — harvest, store, feel grateful, maybe donate. "
            "Here the first taste is already spoken for. Millet-water and milk at the "
            "root are the daily grammar; first-fruits are that grammar applied to the "
            "year's yield. Tiurakh, in Bérenger, is the named power of abundant harvests "
            "and herds; this sentence is how a house stays in his debt without pretending "
            "the field was empty of persons. Colonial pages nearby will talk of "
            "superstition and wasted grain. The philosophy is the opposite of waste. It "
            "is the admission that yield has a source that is not the hoe. Existentially, "
            "the teaching judges any life that treats surplus as proof of private merit. "
            "If the first of what arrived is not returned to the place that grew it, the "
            "house has already begun to live as if the land were dead stuff. You do not "
            "need a millet harvest to take the claim. Whatever increased around you this "
            "season — money, food, time, a child's health — has a first taste that is "
            "not yours to keep as evidence that you are the source."
        ),
        "prac": (
            "Before you eat today's first real meal, set aside a small first portion — "
            "a bite of bread, a sip of water. Take it outside to one actual tree, stone, "
            "or patch of ground you did not make. Leave it. Then eat. Do not bargain."
        ),
        "terms": kt(
            (
                "prémices",
                "first-fruits, always offered -> economic theology: the first taste "
                "belongs to the dwellers of the land -> \"tithe\" is too fiscal and too "
                "addressed to a high God; this goes to the mammam of tree and stone",
            ),
            (
                "toujours",
                "always -> the rite is structural, not occasional -> a harvest festival "
                "you skip in a thin year would already have broken the bond",
            ),
            (
                "Tiurakh",
                "the named power of increase in Bérenger -> what first-fruits keep "
                "favorable to the house -> not a market god of accumulation",
            ),
        ),
        "res": res(
            (
                "Deuteronomy 26:1–11 (basket of first-fruits)",
                "Both require the first of the soil's yield to be carried and declared "
                "before the eater stores it as property.",
                "Israel's basket is spoken to YHWH with a land-history; Serer first-fruits "
                "are poured or left for the local spirits and leave Roog unaddressed.",
            ),
            (
                "Bhagavad Gītā 3.13 (they eat leftover after the offering)",
                "Both treat eating before offering as a kind of theft.",
                "The Gītā's leftover is from a cosmic yajña; Lasnet's always is "
                "household-agricultural at a particular tree.",
            ),
        ),
    },
    {
        "n": 12,
        "title": "The Soul Can Be Eaten While the Envelope Stays Intact",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "Très superstitieux, les Sérères ont une grande peur des sorciers, ils "
            "admettent peu la mort naturelle et la rapportent le plus souvent à un "
            "mauvais sort : l'âme a été mangée, son enveloppe restant intacte pour "
            "sauver les apparences."
        ),
        "roman": (
            f"{ROMAN}. Key teaching: the soul (âme) can be eaten while the envelope "
            "(enveloppe) remains intact. Lasnet's \"superstitious\" is observer contempt, "
            "not the doctrine."
        ),
        "tr": (
            "The Serer admit natural death only rarely and most often refer a death to "
            "a bad working: the soul has been eaten, its envelope remaining intact to "
            "save appearances."
        ),
        "comm": (
            "The claim is that a person is not identical with the visible envelope. A "
            "body can look whole — washed, oiled, still warm — while the life that made "
            "it a someone has already been taken. Lasnet hears this as superstition and "
            "fear of sorcerers. The recoverable philosophy is stricter. Death is not "
            "first a medical event. Death is first a question about the soul: was it "
            "released into a bird, or was it eaten? The envelope that \"saves appearances\" "
            "is a warning against naive empiricism. What you can see is not a sufficient "
            "account of what has happened. This is the dark twin of unit 5. There, joy "
            "at a bird means the soul found another vehicle. Here, an intact corpse can "
            "mean the opposite: the vehicle is still parked and the driver has been "
            "consumed. Colonial pages will rush to poison and fire as the \"real\" story. "
            "Those methods are recorded; they are not this unit's teaching. The teaching "
            "is the distinction between envelope and soul, and the refusal to call every "
            "stopping of breath natural. Existentially, the passage trains a vigilance "
            "that modern wellness language cannot host. You can look successful, fed, "
            "photogenic, and still be having your life eaten — by a relation, a habit, "
            "a workplace, a grief you will not name. The Serer report is not an "
            "invitation to hunt witches. It is a metaphysics in which the visible body "
            "is not the last word on whether a life is still there."
        ),
        "prac": (
            "Look at your own body as an envelope that can look well while something is "
            "being taken. Name one vitality you have been letting a habit or a relation "
            "eat. Take it back today by one protective act — a meal, sleep, a boundary — "
            "not a charm."
        ),
        "terms": kt(
            (
                "âme",
                "soul as what can be eaten -> the personal life, not the corpse -> "
                "\"life-force\" is too impersonal; this is a someone who can be consumed",
            ),
            (
                "enveloppe",
                "the intact bodily envelope that saves appearances -> visible wholeness "
                "as insufficient evidence -> \"body\" as the whole person is the error "
                "this word blocks",
            ),
            (
                "mauvais sort",
                "a bad working, a harmful sending -> Lasnet's gloss for the cause of "
                "most deaths -> \"curse\" in a fairy-tale sense is too light; this is "
                "soul-theft",
            ),
        ),
        "res": res(
            (
                "Matthew 10:28 (fear not those who kill the body but cannot kill the soul)",
                "Both refuse to treat the killing or stopping of the body as the last "
                "account of the person.",
                "Matthew splits body and soul to rank fear toward God; the Serer report "
                "fears a soul that can be eaten while the body still looks intact.",
            ),
            (
                "Phaedo 64c–67a (the body as a garment or prison of the soul)",
                "Both treat the visible body as not identical with the person.",
                "Plato wants the soul freed from the body; Lasnet's Serer fear a soul "
                "taken from a body that has not yet been allowed to finish its office.",
            ),
        ),
    },
    {
        "n": 13,
        "title": "Gisanekal Searches the Soul-Eater",
        "src": "Lasnet 1900, Sérères — Religion",
        "fr": (
            "À chaque mort un voyant, gisanekal, recherche le mangeur d'âme, le plus "
            "souvent il a recours au poison comme les Balantes ou les Diolas, quelquefois "
            "à l'épreuve du feu : un fer rouge est posé sur la langue de l'accusé, s'il "
            "fait une brûlure profonde, l'accusé est coupable."
        ),
        "roman": (
            f"{ROMAN}. Key Serer term: gisanekal — the seer who searches the soul-eater "
            "at each death. Poison and fire are recorded methods, not a practice to copy."
        ),
        "tr": (
            "At each death a seer, gisanekal, searches for the eater of the soul. Most "
            "often the search uses the poison ordeal known also among the Balanta and "
            "the Jola; sometimes the test of fire: a red iron is set on the tongue of "
            "the accused, and a deep burn marks guilt."
        ),
        "comm": (
            "The claim is that a death which may be soul-theft is not left as private "
            "grief. The community appoints a seer. Gisanekal is Lasnet's recording of "
            "that office: a watcher whose job is to find the eater. The contested move "
            "is to take the office seriously without adopting the ordeal as teaching. "
            "Poison and red iron are how a 1900 observer saw truth extracted from a "
            "hidden crime. They are not the philosophy. The philosophy is that soul-theft "
            "is a public question, and that someone in the village is authorized to look. "
            "Without that office, unit 12 collapses into panic or gossip. With it, the "
            "fear of eaten souls has a face and a procedure. Bérenger will show Takhar's "
            "priests judging sorcery by a drink; Lasnet names the seer at every death. "
            "Read together, Serer justice is not only about stolen objects. It is about "
            "stolen life. Colonial suppression of the punishments is recorded on the same "
            "page: the Serer then say sorcerers multiply because they are sure of "
            "impunity, and they accuse missionaries of favoring the eaters by making "
            "people renounce gris-gris. That complaint is not adopted here as a call to "
            "restore ordeal. It is evidence that protective objects and the seer's search "
            "were one system. Existentially, the teaching asks whether your world has "
            "anyone who is allowed to look when a life is being eaten, or whether you "
            "only have opinions and news. The practice is to authorize attention, not to "
            "heat iron."
        ),
        "prac": (
            "If you know a life that is being diminished — including your own — do not "
            "ordeal anyone. Appoint yourself seer for one hour: look, name the eater "
            "without spectacle (a habit, a silence, a person), and take one protective "
            "step. Do not announce guilt you cannot know."
        ),
        "terms": kt(
            (
                "gisanekal",
                "Lasnet's Serer word for the seer who searches the soul-eater at each "
                "death -> an office, not a hobby of omens -> \"witch-doctor\" is the "
                "colonial sneer; this is authorized looking",
            ),
            (
                "mangeur d'âme",
                "eater of the soul -> the agent of the theft in unit 12 -> not a metaphor "
                "for cancer; in the reported belief a someone has consumed a someone",
            ),
            (
                "épreuve",
                "ordeal (poison, fire) -> recorded method of the search -> not the "
                "teaching to practice; the teaching is that hidden soul-crime is not "
                "left to rumor",
            ),
        ),
        "res": res(
            (
                "1 Samuel 28 (Saul seeks a seer when ordinary means fail)",
                "Both appoint a specialist of the unseen when a public crisis exceeds "
                "ordinary looking.",
                "Saul's seer calls up a dead prophet against a ban; gisanekal searches "
                "the living eater of a newly dead soul.",
            ),
            (
                "Bérenger 1879, priests of Takhar and the ordeal drink (this collection)",
                "Both make sorcery a judged question, not a private suspicion.",
                "Bérenger's drink is a priestly test of the accused; Lasnet's gisanekal "
                "is a seer who starts from the death itself.",
            ),
        ),
    },
    {
        "n": 14,
        "title": "The First Child Is Born in the Mother's Village",
        "src": "Lasnet 1900, Sérères — Accouchement",
        "fr": (
            "Le premier enfant doit naître dans le village d'origine de sa mère, "
            "celle-ci d'ailleurs habite presque toujours chez ses parents dans la "
            "première année de mariage. Cette naissance est l'occasion de réjouissances, "
            "on boit et on tue une chèvre ou un mouton; on fête de la même façon la "
            "naissance de jumeaux."
        ),
        "roman": (
            f"{ROMAN}. Cosmology of first birth: the child must be born in the mother's "
            "village of origin; the mother lives with her parents in the first year of "
            "marriage."
        ),
        "tr": (
            "The first child must be born in the village of origin of the mother. She, "
            "for that matter, almost always lives with her parents in the first year of "
            "marriage. That birth is an occasion of rejoicing: one drinks and kills a "
            "goat or a sheep. Twin birth is celebrated in the same way."
        ),
        "comm": (
            "The claim is that a person begins on the mother's ground. First birth is "
            "not a private medical event in the husband's house. It is a return. The "
            "new life must arrive where the mother's own life first arrived. Lasnet "
            "records the rule as obligation (doit naître) and the social fact that "
            "explains it: the bride spends the first year among her parents. The "
            "husband's village does not yet own the first fruit of the marriage. The "
            "mother's village-soul does. This is kinship cosmology, not obstetrics. In "
            "a religion where ancestor and land are one cult, the first child's first "
            "air belongs to a particular fold of earth and a particular set of dead. "
            "To be born elsewhere would start the person already slightly unhoused. "
            "The feast — goat or sheep, drink, the same honors for twins — marks the "
            "arrival as increase (Tiurakh's department) that must be answered in public. "
            "Colonial pages nearby wander into midwifery and marabout charms. Those are "
            "not this unit. The teaching is topological: the first body of a new line "
            "is oriented, as the grave will later be oriented east. Existentially, the "
            "passage asks where your own life actually started, and whether you have "
            "treated that ground as optional scenery. You cannot perform a Serer first "
            "birth. You can refuse to treat origin as a zip code you have outgrown."
        ),
        "prac": (
            "Name the actual place of your own first days — town, house, or the nearest "
            "truth you have. Speak one sentence of thanks toward that ground. If you can "
            "reach water, pour a little for it. Do not invent a myth of self-birth."
        ),
        "terms": kt(
            (
                "village d'origine de sa mère",
                "the mother's village of origin -> the required ground of first birth -> "
                "\"hometown\" is too sentimental; this is a religious address of the "
                "new soul",
            ),
            (
                "premier enfant",
                "the first child -> the first fruit of the marriage, claimed by the "
                "mother's land -> later children may arrive elsewhere; the first is "
                "oriented",
            ),
            (
                "pangool",
                "the ancestral and land powers of the mother's village who receive that "
                "first arrival -> not named by Lasnet here, but the structure of units "
                "2 and 9 requires them",
            ),
        ),
        "res": res(
            (
                "Ruth 1:16–17 and the question of whose people and whose God",
                "Both treat a woman's ground and a woman's people as the frame in which "
                "a next generation is possible.",
                "Ruth attaches herself to Naomi's people and God; Serer first birth "
                "returns the child to the mother's village without converting the high "
                "God into the addressee.",
            ),
            (
                "Roman custom of the child raised to the father (tollere liberos)",
                "Both make first recognition of a child a public cosmological act, not "
                "a private feeling.",
                "The Roman father lifts the child into the paternal line; Serer rule "
                "gives the first birth to the mother's ground.",
            ),
        ),
    },
    {
        "n": 15,
        "title": "Naming on the Seventh Day",
        "src": "Lasnet 1900, Sérères — Accouchement",
        "fr": (
            "Le baptême se fait le septième jour, comme chez les musulmans, il ne donne "
            "lieu à aucune cérémonie particulière."
        ),
        "roman": (
            f"{ROMAN}. Seventh-day naming (Lasnet: baptême), without a particular "
            "ceremony — identity arrives quietly after a week of life."
        ),
        "tr": (
            "The naming is done on the seventh day, as among the Muslims. It gives rise "
            "to no particular ceremony."
        ),
        "comm": (
            "The claim is that a person is not complete at birth. Seven days later a "
            "name is given, and Lasnet's surprise is the teaching: there is no particular "
            "ceremony. Identity arrives as a quiet seventh-day act, not as a festival. "
            "The first-birth feast of the previous unit honors arrival on the mother's "
            "ground. Naming is a different office. It waits. The child has been a living "
            "envelope for a week before the community commits a word to that life. "
            "Comparison with Muslim practice is the observer's; the Serer structure "
            "stands without it. In a cosmology where souls can be eaten, enter birds, "
            "and be spoken to at the ear, a name is not a label stuck on a product. It "
            "is a binding of a someone into the speech of the living. The absence of "
            "spectacle is reverence, not poverty of rite. First-fruits get an always; "
            "the name gets a seventh day and no drum. Existentially, the teaching cuts "
            "the modern rush to brand a life before it has lasted. You do not need to "
            "copy a naming liturgy. You can let a new fact about someone — including "
            "yourself — remain unnamed until it has survived a week of ordinary days, "
            "and then give it a true word without a show."
        ),
        "prac": (
            "Do not announce a new identity, plan, or verdict today. Let it last until "
            "evening. At day's end, if it is still true, speak one quiet name for it to "
            "one person, or to the ground. No performance."
        ),
        "terms": kt(
            (
                "baptême",
                "Lasnet's French for the seventh-day naming -> not Christian sacrament; "
                "the giving of a name after a week of life -> \"christening\" imports a "
                "church the source does not have",
            ),
            (
                "septième jour",
                "the seventh day -> the delay before the person is spoken as a named "
                "someone -> birth is arrival; naming is admission into speech",
            ),
        ),
        "res": res(
            (
                "Luke 1:59–63 (John named on the eighth day)",
                "Both delay the public name past the day of birth and treat naming as a "
                "speech-act that settles who the child is.",
                "Luke's naming is eighth-day, covenantal, and contested in the family; "
                "Lasnet's Serer seventh day has no particular ceremony.",
            ),
            (
                "Yoruba naming (orúkọ) on a fixed early day (Samuel Johnson, structural)",
                "Both treat the early-day name as cosmology, not stationery.",
                "Johnson records a richer spoken liturgy of names; Lasnet records the "
                "delay and the refusal of spectacle.",
            ),
        ),
    },
    {
        "n": 16,
        "title": "Initiation Seclusion Outside the Village",
        "src": "Lasnet 1900, Sérères — Circumcision (threshold, not anatomy)",
        "fr": (
            "Les circoncis sont ensuite séquestrés sous un abri en dehors du village, "
            "ils ne peuvent sortir, le premier venu qui les rencontrerait aurait le "
            "droit de les rouer de coups; les parents doivent pourvoir à leurs besoins, "
            "on les nourrit bien et abondamment. Quand la guérison est complète, on "
            "commence la fête, les circoncis quittent leur abri, le brûlent et vont "
            "dans les villages danser."
        ),
        "roman": (
            f"{ROMAN}. Threshold teaching: seclusion under a shelter outside the village; "
            "then the shelter is burned and the initiates re-enter dancing. Anatomy is "
            "not the unit."
        ),
        "tr": (
            "The initiates are then secluded under a shelter outside the village. They "
            "may not go out; anyone who met them would have the right to beat them. The "
            "parents must provide for their needs; they are fed well and abundantly. When "
            "healing is complete, the feast begins: the initiates leave their shelter, "
            "burn it, and go into the villages to dance."
        ),
        "comm": (
            "The claim is that becoming adult is a change of residence before it is a "
            "change of status. Lasnet's medical catalog is refused here. What is kept "
            "is the topology. The boys leave the village. They live under a shelter that "
            "is not a house. They may not wander. Meeting them in that in-between is "
            "already a violation. Parents feed them from the village they cannot yet "
            "re-enter. Then the shelter is burned. Return is not a quiet walk home. It "
            "is fire plus dance. The contested move is to read this as threshold "
            "philosophy rather than as ethnography of a body-cut. A person who will "
            "later refuse to leave ancestral land must first learn what it is to be "
            "outside it, fed by it, and forbidden to stroll. The burning of the abri "
            "says: the liminal camp is not a second village you keep. You do not "
            "colonize the threshold. You destroy the hut that made you not-yet. "
            "Existentially, most modern initiations are either medical events or "
            "branding exercises that never leave the house. This teaching asks for an "
            "actual outside, an actual dependence, and an actual burning of the "
            "temporary self. You cannot found a Serer camp. You can leave one comfort, "
            "let yourself be fed by others without controlling the menu, and destroy "
            "the prop when you come back."
        ),
        "prac": (
            "Leave your usual room for one hour. Sit somewhere that is not yours — a "
            "stair, a park edge, a doorway. Eat something given or already prepared, "
            "not something you cook as host. When you return, throw away or recycle "
            "one object that was propping an old version of you. Do not announce an "
            "initiation."
        ),
        "terms": kt(
            (
                "en dehors du village",
                "outside the village -> the spatial definition of the threshold -> "
                "\"retreat\" as a spa weekend misses that the village is forbidden",
            ),
            (
                "abri",
                "shelter, not a house -> the liminal dwelling that must later be burned "
                "-> keeping the camp would make seclusion a second residence",
            ),
            (
                "le brûlent",
                "they burn it -> the threshold is destroyed, not archived -> modern "
                "\"integration\" often keeps every hut; this rite refuses that",
            ),
        ),
        "res": res(
            (
                "van Gennep's tripartite rite (separation, margin, aggregation) as later "
                "theory of this shape",
                "Both describe leaving, living in a marked outside, and returning changed.",
                "van Gennep generalizes; Lasnet records a Serer burning of the shelter "
                "and a dance back into the villages.",
            ),
            (
                "Benedictine novitiate outside full profession",
                "Both feed a person who is not yet a full member from the house that "
                "still withholds belonging.",
                "The monastery keeps the novitiate building; the Serer initiates burn "
                "the abri so the in-between cannot be inhabited again.",
            ),
        ),
    },
    {
        "n": 17,
        "title": "One Does Not Leave Ancestral Land Voluntarily",
        "src": "Lasnet 1900, Sérères — Mœurs; Bérenger 1879, Mœurs",
        "fr": (
            "Les Sérères sont de mœurs douces, très attachés à leur sol, ne songeant "
            "point à faire la guerre et ne s'occupant que de leurs troupeaux et de leurs "
            "cultures. Ils se déplacent difficilement... ceux qui s'éloignent sont mal "
            "considérés, on les accuse d'avoir contracté union avec des étrangères, "
            "parfois on leur refuse la sépulture. Jamais des Sérères ne se déplaceraient "
            "volontairement pour aller vivre en pays étranger."
        ),
        "roman": (
            f"{ROMAN}. Teaching: never leave ancestral land voluntarily. Those who go "
            "far are ill-regarded and may be refused burial."
        ),
        "tr": (
            "The Serer are deeply attached to their soil. They move with difficulty. "
            "Those who go far are ill-regarded; they are accused of having contracted "
            "union with foreign women, and sometimes burial is refused them. Never would "
            "Serer people displace themselves voluntarily to go live in a foreign land."
        ),
        "comm": (
            "The claim is that the land is not a location you can swap. Voluntary exile "
            "is a religious fault, not a career move. Lasnet's jamais is as strong as "
            "the always of first-fruits. The people who appear in Wolof country under "
            "Serer names are, in his report, captives taken young — not emigrants. "
            "Bérenger finds the same temperament: they pass their lives where they were "
            "born, grouped by families in a fold of cultivated ground, as little in love "
            "with migration as the Soninke are much in love with it. The sanction "
            "reveals the metaphysics. To leave is to be suspected of having given the "
            "line to a foreign bed. To be refused burial is to be refused the last "
            "conversation with the soil-soul. If ancestor and land are one cult, a "
            "voluntary departure is already a small death that the grave may decline "
            "to complete. Colonial administrators wanted workers and roads; they praised "
            "this attachment as convenient. That praise is not the teaching. The teaching "
            "is that a world of Roog, mammam, and pangool is local or it is rhetoric. "
            "Existentially, most readers of this unit have already left a ground. The "
            "point is not to shame travel. It is to stop calling rootlessness freedom "
            "as if the dead and the field had no claim. If you have left, the practice "
            "is to know that you have left, and to bind what can still be bound."
        ),
        "prac": (
            "Name the ground you have actually left — a town, a house, a family field. "
            "Do not call the leaving nothing. Send one concrete act of remaining toward "
            "it today: a call to a living elder, water poured where you now stand in "
            "its name, or a refusal to sell one inherited thing."
        ),
        "terms": kt(
            (
                "sol",
                "the ancestral soil -> not scenery, the cult-partner of the dead -> "
                "\"homeland\" as patriotism is too national; this is a parcel and a "
                "people",
            ),
            (
                "volontairement",
                "voluntarily -> the fault is chosen departure, not captivity -> Lasnet's "
                "Nones in Wolof country are explained as raided children, not emigrants",
            ),
            (
                "sépulture",
                "burial as a right of those who stayed -> refusal of the grave is "
                "refusal of the last land-bond -> \"funeral\" as a service you purchase "
                "anywhere misses the territorial metaphysics",
            ),
        ),
        "res": res(
            (
                "Psalm 137 (how shall we sing on foreign soil)",
                "Both make exile a religious wound, not a change of address.",
                "The psalm sings toward Zion under a high God; Serer refusal of voluntary "
                "leaving is attachment to a family parcel whose high God is not addressed.",
            ),
            (
                "Antigone's claim that the dead must have their ground",
                "Both treat burial-right as the last proof of belonging.",
                "Antigone defies a king for a brother's grave; Serer custom may refuse "
                "the grave to the one who left the soil by choice.",
            ),
        ),
    },
    {
        "n": 18,
        "title": "Gris-gris Inherited, Not Given Away",
        "src": "Lasnet 1900, Sérères — Ornements; Religion (missionaries and gris-gris)",
        "fr": (
            "Les colliers de coraux... constituent les bijoux de famille et se "
            "transmettent par héritage; un Sérère ne s'en dessaisit qu'à la dernière "
            "extrémité, par exemple en cas de famine, et encore il ne fait que les "
            "mettre en gage. Les gris-gris sont peu nombreux et des plus grossiers : "
            "cornes de bœuf, de biche, de bélier qui contiennent des graines de "
            "cotonnier, des cheveux et des matières plus viles encore. Les Sérères "
            "prétendent que les sorciers... multiplient leurs méfaits... ils accusent "
            "les missionnaires de les favoriser parce qu'ils essaient de les faire "
            "renoncer à leurs gris-gris."
        ),
        "roman": (
            f"{ROMAN}. Family jewels (coral) are inherited and only pledged in famine. "
            "Gris-gris are few, coarse, and refused to missionaries. The shared teaching: "
            "protective things of the line are not alienated."
        ),
        "tr": (
            "Coral necklaces are family jewels and are transmitted by inheritance. A "
            "Serer person parts with them only at the last extremity, for example in "
            "famine, and even then only puts them in pledge. Gris-gris are few and of "
            "the coarsest kind: horns of ox, hind, ram, holding cotton seeds, hair, and "
            "still viler matter. The Serer accuse missionaries of favoring sorcerers "
            "because they try to make people renounce their gris-gris."
        ),
        "comm": (
            "The claim is that what protects the line is not a commodity. Lasnet's "
            "explicit inheritance sentence is about coral family jewels: transmitted, "
            "not sold, pledged only in famine. The gris-gris sit on the next lines as "
            "few, coarse, and non-negotiable in another way: missionaries want them "
            "renounced, and the Serer hear that demand as leaving them open to "
            "soul-eaters. Honest reading keeps the two objects distinct and the grammar "
            "one. Horn, hair, seed, coral: none of this is jewelry in a shop sense. It "
            "is lineage-stuff. To give it away lightly is to treat protection as a "
            "fashion. Colonial taste calls the horns vile and the coral a price. The "
            "teaching recovered is anti-alienation. A famine-pledge still intends "
            "return. A mission-renunciation intends disappearance. The Serer complaint "
            "against the missionaries is therefore theological, not stubbornness about "
            "charms. If souls can be eaten, you do not hand over the few objects that "
            "bind the middle. This is unit 10's binding applied to portable things. "
            "Existentially, the passage asks what you have treated as sellable that was "
            "actually inherited protection — a practice, a photograph, a promise, a "
            "piece of family craft. You do not need a ram's horn. You need one thing "
            "you will not list for sale."
        ),
        "prac": (
            "Choose one inherited or protective object (a letter, a ring, a stone, a "
            "photograph). Do not sell it, gift it away, or post it today. Hold it and "
            "say: this is not merchandise. If you have none, write one sentence you "
            "will not alienate, and keep the paper."
        ),
        "terms": kt(
            (
                "gris-gris",
                "protective charms (horns, sachets, hair, seed) -> few and coarse in "
                "Lasnet's Serer record -> \"fetish\" is the colonial dump; these are "
                "portable binds against soul-theft",
            ),
            (
                "bijoux de famille",
                "family jewels, coral, transmitted by inheritance -> alienated only as "
                "famine-pledge -> the same anti-commodity grammar as the gris-gris, "
                "spoken of wealth that is also lineage",
            ),
            (
                "héritage",
                "inheritance -> the proper movement of protective things -> sale is the "
                "wrong verb; even famine uses gage (pledge), not gift",
            ),
        ),
        "res": res(
            (
                "Numbers 36 (ancestral inheritance not to pass away from the tribe)",
                "Both refuse to let lineage-stuff drift into foreign hands as if it were "
                "ordinary goods.",
                "Numbers legislates land-and-name inside Israel; Lasnet records coral and "
                "gris-gris as the portable Serer instance of the same refusal.",
            ),
            (
                "Catholic relics and medals kept in a family",
                "Both can look like \"objects\" to an outsider and still be non-vendible "
                "protection inside a cult.",
                "A relic is authorized by a church of the high God; Serer gris-gris bind "
                "the middle and leave Roog unaddressed.",
            ),
        ),
    },
    {
        "n": 19,
        "title": "The Grave Faces East; Water at the Feet",
        "src": "Lasnet 1900, Sérères — Funérailles",
        "fr": (
            "L'enterrement a lieu le jour même du décès, la fosse est creusée en dehors "
            "du village et orientée vers l'est, le lit du défunt est déposé dans le fond "
            "et le corps couché par-dessus; elle est couverte avec des branchages et des "
            "nattes, au-dessus on place la toiture de la case que l'on recouvre ensuite "
            "de terre ou de coquillages, la transformant en véritable tumulus. Aux pieds "
            "du mort on place quelquefois sa pipe, son tabac, de l'eau et un peu de "
            "couscous; auprès de la tombe on plante un piquet auquel sont suspendus son "
            "arc et ses flèches."
        ),
        "roman": (
            f"{ROMAN}. East-facing grave outside the village; pipe, tobacco, water, and "
            "couscous at the feet; roof of the house made into a tumulus. Speech at the "
            "ear is unit 6; this unit is orientation and continued feeding."
        ),
        "tr": (
            "Burial is the same day. The grave is dug outside the village and oriented "
            "toward the east. The dead person's bed is laid in the bottom and the body "
            "laid upon it. Branches and mats cover it; the roof of the house is placed "
            "above and covered with earth or shells, becoming a true tumulus. At the "
            "feet one sometimes places the pipe, tobacco, water, and a little couscous. "
            "Beside the tomb a stake is planted, and from it hang the bow and arrows."
        ),
        "comm": (
            "The claim is that the dead still thirst and still face the rising sky. "
            "Unit 6 kept the ear. This unit keeps the axis and the meal. East is not "
            "decoration. It is the Rog-axis of unit 1: the same sky that names the "
            "invisible master is the direction the body is aimed. Water and couscous "
            "at the feet continue the millet-and-water economy of libation. The dead "
            "have changed residence (outside the village) without leaving the household's "
            "food-world. The roof of the case becoming a tumulus is the house itself "
            "given to the new dwelling. A person is not extracted from architecture and "
            "dropped in a hole. The house-roof goes with them, then earth or shells "
            "make a mound. Bow and arrows at the stake say the dead still have a day "
            "outside the grave-goods museum: tools of a life are parked beside, not "
            "thrown away as trash. Colonial observers linger on drink after the burial. "
            "The usable core is drier: face east, leave water, give the roof. "
            "Existentially, the teaching is against the sealed, directionless, unfed "
            "modern grave as the image of what a person was. You may not control a "
            "cemetery. You can orient one act of care toward rising light and leave "
            "one ordinary need (water, a word, a tool) with someone who cannot fetch "
            "it."
        ),
        "prac": (
            "At sunrise or the nearest morning you have, face east for one minute. Then "
            "set a cup of water on the ground at your feet as if for someone who still "
            "thirsts. Pour it out when you leave. Do not make a shrine. Keep the "
            "orientation and the gift."
        ),
        "terms": kt(
            (
                "orientée vers l'est",
                "oriented toward the east -> alignment with rising sky-light, the Rog-axis "
                "-> compass custom without unit 1 is incomplete",
            ),
            (
                "eau / couscous",
                "water and grain at the feet -> the dead remain in the libation economy "
                "-> \"grave goods\" as archaeology misses continued feeding",
            ),
            (
                "tumulus",
                "the house-roof covered with earth or shells -> the dwelling follows the "
                "dead -> a flat anonymous grave would deny the change of residence",
            ),
        ),
        "res": res(
            (
                "Jewish burial facing a holy direction and leaving the dead with care, "
                "not display",
                "Both refuse a directionless dumping of the body and keep the dead inside "
                "a people's map of the world.",
                "Jewish orientation is toward the Temple / east in many diasporas under "
                "one God; Serer east is the sky-name of Roog plus water at the feet for "
                "a still-thirsty someone.",
            ),
            (
                "Egyptian burial with food and tools for a continuing person",
                "Both treat the dead as still needing the economy of the living.",
                "Egyptian provision is temple-booked for a long afterlife; Serer provision "
                "is same-day, household, and paired with possible bird-metempsychosis.",
            ),
        ),
    },
    {
        "n": 20,
        "title": "Awa Holds the First Seat of the House",
        "src": "Lasnet 1900, Sérères — Mariage",
        "fr": (
            "Comme chez les musulmans, la première femme a autorité sur les autres et "
            "s'appelle awa; elles habitent toutes le même carré, mais occupent des cases "
            "distinctes avec leurs enfants, le mari a également son logement à part."
        ),
        "roman": (
            f"{ROMAN}. Key term: awa — first wife as household authority. Distinct "
            "houses in one square; the husband also lodges apart. Household cosmology, "
            "not a catalog of marriage violence."
        ),
        "tr": (
            "As among the Muslims, the first wife has authority over the others and is "
            "called awa. They all live in the same square, but occupy distinct houses "
            "with their children; the husband likewise has his lodging apart."
        ),
        "comm": (
            "The claim is that a house is a cosmos with a first seat. Lasnet's sentence "
            "is short and it is enough. Authority in the square is named: awa. The "
            "women are not a heap. Each has a distinct case and her children. The "
            "husband is not the center of a single room; he lodges apart. Comparison "
            "with Muslim custom is the observer's crib. The Serer structure is spatial "
            "and hierarchical at once: one carré, several dwellings, one first-seat. "
            "This is not a romance of polygamy and not a license for the surrounding "
            "pages' ethnography of capture and incest, which this collection refuses as "
            "teaching. What is kept is the philosophy of the household as ordered "
            "multiplicity. In a religion of local mammam — genius of the house among "
            "them — the square is already a small village of spirits. Someone must hold "
            "the first relation to that genius. Awa is that office. Existentially, most "
            "modern households still have an unnamed first-seat and unnamed separate "
            "rooms of power, and they pretend otherwise until a fight. The teaching is "
            "to name the order without pretending the house is a single self. You do "
            "not appoint an awa. You can admit who actually holds first care in your "
            "square, give that person one concrete honor today, and keep distinct rooms "
            "from collapsing into a blur."
        ),
        "prac": (
            "Name who actually holds first care in your household or shared place — "
            "including if it is you. Do one act of honor toward that office today "
            "(thanks, a task taken off them, a door left closed). Do not invent a rank "
            "you do not live."
        ),
        "terms": kt(
            (
                "awa",
                "first wife; holder of authority over the other wives in the square -> "
                "household cosmology, not a romance title -> \"senior wife\" in a "
                "soap-opera sense misses the office",
            ),
            (
                "carré",
                "the square of houses -> one compound, several dwellings -> the village "
                "in miniature, already a map of mammam",
            ),
            (
                "cases distinctes",
                "distinct houses with their children -> multiplicity inside the bond -> "
                "a single shared bedroom as the image of family would erase this cosmos",
            ),
        ),
        "res": res(
            (
                "Proverbs 31 and the named competent woman of the house",
                "Both treat household authority as an office with a public name, not as "
                "private charm.",
                "Proverbs praises a wife inside a patriarchal Israelite house of one God; "
                "awa is first-seat in a plural square whose house-spirit is addressed, "
                "not Roog.",
            ),
            (
                "Roman paterfamilias versus the mater of the domus",
                "Both know that a domestic world has a ranked speaker, not a cloud of "
                "equals pretending to have no order.",
                "Roman law centers the father; Lasnet's Serer square names the first "
                "wife as the authority among the women and lodges the husband apart.",
            ),
        ),
    },
    {
        "n": 21,
        "title": "Those Who Leave May Be Refused Burial",
        "src": "Lasnet 1900, Sérères — Mœurs",
        "fr": (
            "Ils se déplacent difficilement et ne dépassent guère les escales où ils "
            "vont vendre leurs arachides; ceux qui s'éloignent sont mal considérés, on "
            "les accuse d'avoir contracté union avec des étrangères, parfois on leur "
            "refuse la sépulture. Très réservés quand ils reçoivent des étrangers même "
            "des Sérères d'une autre tribu, ils ne les laissent pas pénétrer dans leurs "
            "cases et les installent sur la place publique; après leur départ ils "
            "brisent les ustensiles qui ont renfermé leurs aliments."
        ),
        "roman": (
            f"{ROMAN}. Sanction of departure: ill-regard, accusation of foreign union, "
            "sometimes refusal of burial. Even a Serer of another tribe is kept on the "
            "public square; utensils that fed him are broken."
        ),
        "tr": (
            "They move with difficulty and scarcely go beyond the trading posts where "
            "they sell their groundnuts. Those who go far are ill-regarded; they are "
            "accused of having contracted union with foreign women; sometimes burial is "
            "refused them. They are very reserved even toward Serer of another tribe: "
            "they do not let them enter their houses, they lodge them on the public "
            "square, and after the departure they break the utensils that held their "
            "food."
        ),
        "comm": (
            "The claim is that burial is a right of those who stayed, and that even a "
            "guest leaves a stain the house must break. Unit 17 stated the vow: no "
            "voluntary exile. This unit states the liturgy of the boundary. A foreign "
            "union is not only romance out of group; it is a suspected gift of the line "
            "to another soil-soul. Refusal of sépulture is the last form of that "
            "judgment: the ground will not always complete the conversation of unit 6. "
            "The broken utensils are the everyday form. Food that has passed through an "
            "outsider's mouth cannot stay in the house's vessels. This looks like "
            "xenophobia to a colonial traveler who wanted hospitality on European terms. "
            "The recoverable teaching is purity of the house-genius. If the case has a "
            "mammam, then what enters it is not neutral. Public square is the proper "
            "place for the not-yet-kin. Breaking the bowl is not hatred of persons; it "
            "is resetting the vessel. Existentially, modern houses pretend to be "
            "frictionless hotels and then are shocked by the cost. You need not break "
            "crockery. You can know that your table is a cult-site, decide what may "
            "enter it, and perform one honest reset after a crossing that was not kin."
        ),
        "prac": (
            "After one encounter that was not of your house (a meeting, a guest, a "
            "feed of news), wash one actual vessel — a cup, a plate, your hands — as "
            "a reset, not as germ theater. Say: the house has a boundary. Do not "
            "perform contempt for a person."
        ),
        "terms": kt(
            (
                "sépulture",
                "burial refused to some who left -> the grave as a right of the staying "
                "-> \"cemetery access\" as a civic service misses the land-soul's veto",
            ),
            (
                "place publique",
                "the public square where even other-tribe Serer are lodged -> inside the "
                "case is not a hotel -> hospitality has a topology",
            ),
            (
                "brisent les ustensiles",
                "they break the utensils that held the guest's food -> the house-genius "
                "is reset by destroying the vessel -> \"rudeness\" is the traveler's "
                "word for a rite",
            ),
        ),
        "res": res(
            (
                "Numbers 19 (vessels and impurity after contact with death or the outside)",
                "Both treat certain contacts as leaving a residue that vessels cannot "
                "simply be washed of in the ordinary way.",
                "Priestly law is written and addressed to YHWH's camp; Serer breaking of "
                "bowls is household-animist and leaves Roog unaddressed.",
            ),
            (
                "Japanese satoyama / village boundary rites (structural)",
                "Both keep a difference between the inside of the dwelling and the place "
                "where strangers may stand.",
                "Japanese forms are shrine-and-kami coded; Lasnet's Serer form is the "
                "broken bowl and the refused grave.",
            ),
        ),
    },
    {
        "n": 22,
        "title": "The Lamane Holds the Soil",
        "src": "Lasnet 1900, Sérères — Organisation sociale",
        "fr": (
            "Les Sérères n'ont pour ainsi dire pas de castes nobles, de même ils n'ont "
            "pas de castes inférieures comme par exemple les artisans des populations "
            "musulmanes; les griots seuls restent à part. Les notables s'appellent "
            "lamanes; ils constituent la classe aisée et sont seuls propriétaires du sol "
            "qu'ils se transmettent de père en fils et prêtent ou louent aux autres "
            "indigènes; c'est parmi eux que l'on choisit les chefs de villages."
        ),
        "roman": (
            f"{ROMAN}. Key term: lamane — land-master, sole owner of soil transmitted "
            "father to son, lender of fields, source of village heads. Griots remain "
            "apart (see unit 24)."
        ),
        "tr": (
            "The Serer have almost no noble castes, and no artisan castes of the kind "
            "found among Muslim populations; the griots alone remain apart. The notables "
            "are called lamanes. They are the well-off class and the sole owners of the "
            "soil, which they transmit from father to son and lend or rent to others. "
            "Village heads are chosen from among them."
        ),
        "comm": (
            "The claim is that land is not a free market and not a royal whim. It sits "
            "with named masters who transmit it in the male line and lend it. Lamane is "
            "the living face of unit 9's ancestor-land fusion. To hold the soil is "
            "already a religious-political office: the parcel has a someone who may "
            "speak for it, rent it, and be chosen as village head because the soil "
            "already chose that house. Lasnet's surrounding colonial satisfaction — "
            "French residents, suppressed exactions — is not the teaching. The teaching "
            "is that ownership here is kinship with a field. Absence of a wide caste "
            "ladder (except griots) makes the lamane stand out more, not less. There "
            "is no separate priest-caste of Roog. The land-master is as close as this "
            "source comes to a standing clergy of the ground. Existentially, modern "
            "readers either idolize private property or pretend land is only theft. "
            "This office is neither. It is a hereditary trusteeship that can be lent. "
            "You probably are not a lamane. You can still ask who actually holds the "
            "ground you sleep on, and whether your relation to it is rent, gift, "
            "amnesia, or a vow."
        ),
        "prac": (
            "Find out, if you do not know, who holds the title or lease of the ground "
            "you slept on last night. Write the name. Then pour a sip of water for the "
            "ground itself, not for the paperwork. Notice the gap between owner and "
            "soil-soul."
        ),
        "terms": kt(
            (
                "lamane",
                "Serer land-master -> sole transmitter of soil, lender of fields, pool "
                "from which village heads are chosen -> \"landlord\" in a cash sense "
                "misses the cult-joint with the parcel",
            ),
            (
                "sol",
                "the soil as what can be owned only in this hereditary way -> not a "
                "commodity among many -> renting it out still leaves the lamane as the "
                "face of the field",
            ),
            (
                "chefs de villages",
                "village heads chosen among lamanes -> civic office grows from land-office "
                "-> Fitaure in Bérenger is the religious-civic twin of this structure",
            ),
        ),
        "res": res(
            (
                "Leviticus 25 (land shall not be sold in perpetuity; the land is Mine)",
                "Both refuse a total alienation of soil and keep a deeper claim behind "
                "the living holder.",
                "Leviticus names YHWH as the true owner; Serer lamane-right is family "
                "trusteeship of a parcel whose high God is not the addressee of the lease.",
            ),
            (
                "Chinese lineage land and the ancestral hall's fields",
                "Both lodge title in a descent group that lends use and still speaks for "
                "the earth of the dead.",
                "Chinese practice is hall-and-tablet coded; Lasnet's lamane is a notable "
                "who is also the village's pool of chiefs.",
            ),
        ),
    },
    {
        "n": 23,
        "title": "The Maternal Uncle Outranks the Father",
        "src": "Lasnet 1900, Sérères — Organisation sociale",
        "fr": (
            "La famille est assez mal organisée, le père a une autorité très relative, "
            "la mère n'est jamais consultée; le rôle de la femme est d'ailleurs des plus "
            "effacé. L'oncle maternel a plus d'autorité sur les enfants que le père. "
            "Souvent les enfants sont confiés à un proche qui est chargé de leur "
            "éducation jusqu'à douze ou treize ans pour les filles, quatorze ou quinze "
            "pour les garçons."
        ),
        "roman": (
            f"{ROMAN}. Kinship cosmology: the maternal uncle has more authority over "
            "the children than the father. Lasnet's contempt for the family as \"badly "
            "organized\" and the woman as a beast of burden is observer poison, not "
            "teaching. Awa (unit 20) already names female household office."
        ),
        "tr": (
            "The father's authority is only relative. The maternal uncle has more "
            "authority over the children than the father. Children are often entrusted "
            "to a relative charged with their education until twelve or thirteen for "
            "girls, fourteen or fifteen for boys."
        ),
        "comm": (
            "The claim is that blood-authority does not follow the European father-house "
            "by default. The mother's brother is the stronger pole. Lasnet calls the "
            "family badly organized because he is looking for a paterfamilias and finds "
            "a maternal uncle. That is his failure of theory, not theirs. In a world "
            "where the first child must be born in the mother's village, it is coherent "
            "that the mother's brother — the male of that village-line — speaks for the "
            "child more than the genitor who married in. The contested move is to take "
            "this as cosmology, not as an insult to fathers. Authority here is about "
            "which dead and which soil may claim the young. Entrusting children to a "
            "relative for education is the same grammar as initiation seclusion: the "
            "person is formed by more than the conjugal pair. Colonial sentences on "
            "the same page that degrade women as beasts of burden are refused. Unit 20 "
            "already recorded awa as named household authority; this unit records a "
            "named male office on the mother's side. Existentially, many houses still "
            "run on an unofficial uncle, aunt, or elder who actually holds the child "
            "while a legal father is elsewhere. The teaching is to honor the real pole "
            "without pretending the nuclear pair was the cosmos."
        ),
        "prac": (
            "Name the person, other than a legal parent, who actually helped form you "
            "— an uncle, aunt, teacher, elder. Send one concrete thanks today. If you "
            "hold that office for a younger person, do one act of authority that is "
            "care, not control."
        ),
        "terms": kt(
            (
                "oncle maternel",
                "the mother's brother -> stronger authority over children than the father "
                "-> \"uncle\" as a casual relative misses the office of the mother's "
                "ground",
            ),
            (
                "autorité très relative",
                "the father's merely relative authority -> Lasnet's complaint is the "
                "evidence of a different cosmos -> not a failed patriarchy; a maternal "
                "pole",
            ),
            (
                "village d'origine de sa mère",
                "the mother's village of unit 14 -> the ground this uncle represents -> "
                "without that unit, uncle-right looks like a quirk",
            ),
        ),
        "res": res(
            (
                "West African avunculate as a regional structure (compare Mande and "
                "Wolof reports in the same PD century)",
                "Both lodge a child's heavier bond on the mother's brother rather than "
                "on the conjugal father alone.",
                "Regional comparison can flatten; Lasnet's Serer instance is tied to "
                "first birth in the mother's village and refusal of foreign burial.",
            ),
            (
                "Gospel household sayings that relativize the father-house (Luke 8:19–21)",
                "Both refuse to treat the legal father-house as the only real kinship.",
                "Luke relocates family into doing the word of God; Serer uncle-right "
                "relocates it into the mother's soil-line without addressing Roog.",
            ),
        ),
    },
    {
        "n": 24,
        "title": "The Griot Is Returned to the Hollow Baobab",
        "src": "Lasnet 1900, Sérères — Funérailles",
        "fr": (
            "Les griots ne sont pas enterrés, on les jette dans un baobab creux, "
            "enveloppés de pagnes, et avec le même cérémonial que pour les autres "
            "Sérères."
        ),
        "roman": (
            f"{ROMAN}. Griots are not earth-buried; they are placed in a hollow baobab, "
            "wrapped in cloths, with the same ceremonial as other Serer. The baobab is "
            "already a spirit-dwelling (unit 3)."
        ),
        "tr": (
            "Griots are not buried. They are placed in a hollow baobab, wrapped in "
            "cloths, and with the same ceremonial as for the other Serer."
        ),
        "comm": (
            "The claim is that some souls have a different residence, not a lesser rite. "
            "Lasnet's verb jette can sound like contempt. The next clause blocks that "
            "reading: the same ceremonial as the others. Wrapping in pagnes is the same "
            "honor. What changes is the house. Ordinary Serer go into an east-facing "
            "tumulus outside the village. Griots go into the tree that already houses "
            "mammam. The baobab of unit 3 is not a dump. It is a preferred dwelling of "
            "spirits. To return a griot there is to assign a caste of speech to the "
            "tree-house rather than to the earth-mound. Colonial caste-sneer is refused. "
            "The griot remains apart in life (unit 22); in death that apartness is "
            "topological. Song and praise-speech belong to a different hollow than "
            "farming bodies. Existentially, the teaching is that equality of ceremonial "
            "care does not require identical placement. A society can honor two "
            "residences without pretending everyone is the same kind of dead. You "
            "cannot found a griot-tree. You can ask, of your own end, whether you have "
            "only imagined one generic hole, and whether some lives you know already "
            "belong to a different house."
        ),
        "prac": (
            "Stand at one actual tree. Without imitating a funeral, admit that a body "
            "could be housed in more than earth. Then do one act of equal care toward "
            "someone your world ranks apart — a thanks, a share of food, a listening — "
            "without demanding they occupy your house."
        ),
        "terms": kt(
            (
                "griot",
                "the praise-speaker caste, kept apart in life and given the baobab in "
                "death -> not a \"minstrel\" and not trash -> speech-people of a "
                "tree-residence",
            ),
            (
                "baobab creux",
                "hollow baobab -> already a mammam-dwelling in unit 3 -> the griot's "
                "grave is a spirit-house, not a refuse pit",
            ),
            (
                "même cérémonial",
                "the same ceremonial -> equality of rite with difference of place -> "
                "\"thrown away\" as a translation of jeter would erase this clause",
            ),
        ),
        "res": res(
            (
                "Hindu difference of funeral for sannyāsin (often without ordinary "
                "cremation-house rites)",
                "Both can honor a person with a full rite that is not the standard "
                "earth or fire of the householder.",
                "The sannyāsin's difference is renunciation of the world; the griot's "
                "is caste-office returned to the spirit-tree.",
            ),
            (
                "Celtic and northern tree-burial motifs (structural, late)",
                "Both imagine some dead as belonging to a tree rather than to a flat "
                "grave.",
                "Romantic tree-burial is often literary; Lasnet records a specific "
                "hollow baobab with the same wrapping as earth-burial.",
            ),
        ),
    },
    {
        "n": 25,
        "title": "The Woods Are Sanctuaries",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Ces deux dieux habitent dans les plus grands arbres des forêts, de sorte "
            "que les bois sont pour les Sérères des lieux sacrés, et les arbres "
            "séculaires des sanctuaires vénérés."
        ),
        "roman": (
            f"{ROMAN}. Takhar and Tiurakh inhabit the greatest trees; therefore the "
            "woods are sacred places and age-old trees are venerated sanctuaries."
        ),
        "tr": (
            "These two gods inhabit the greatest trees of the forests, so that the woods "
            "are sacred places for the Serer, and the age-old trees venerated sanctuaries."
        ),
        "comm": (
            "The claim is that sanctuary is not masonry. If justice and increase live "
            "in the greatest trees, then to enter the woods is already to enter a court "
            "and a granary. Bérenger's de sorte que is logical, not scenic. Sacredness "
            "follows from dwelling. The tree is not a symbol of Takhar. Takhar inhabits "
            "it. Age matters: arbres séculaires have already outlasted lawsuits and "
            "harvests. A justice that lives in a centuries-old tree is not the justice "
            "of the latest strong man. An increase that lives there is not this year's "
            "profit. Lasnet's baobab-libation is the household form of the same fact; "
            "Bérenger names the forest as institutional space without walls. Colonial "
            "\"poetry of childish forest mysticism\" on the surrounding page is refused. "
            "The recoverable teaching is architectural: the Serer did not fail to build "
            "temples. They located temples where the gods already lived. Existentially, "
            "a walk in \"nature\" that treats trees as carbon and shade has already "
            "desecrated this sanctuary without cutting a trunk. The practice is to enter "
            "one stand of old trees as if you had taken off your shoes in a court, and "
            "to keep Takhar and Tiurakh from collapsing into a mood."
        ),
        "prac": (
            "Enter one actual grove, park of old trees, or single elder tree. Do not "
            "photograph first. Stand as in a sanctuary for three minutes. Sort one "
            "concern into justice or increase, then leave without taking a souvenir."
        ),
        "terms": kt(
            (
                "bois",
                "the woods as sacred places because the two gods inhabit the greatest "
                "trees -> sacred geography, not scenery -> \"nature spirituality\" is "
                "too generic; these are particular groves",
            ),
            (
                "arbres séculaires",
                "age-old trees as venerated sanctuaries -> duration is part of the "
                "office -> a sapling planted as a symbol would not yet be this",
            ),
            (
                "Takhar / Tiurakh",
                "justice and increase as tree-dwelling powers -> the reason the woods "
                "are sanctuaries -> without the pair, \"sacred grove\" is only atmosphere",
            ),
        ),
        "res": res(
            (
                "Greek alsos / sacred grove of a named god",
                "Both make the grove a precinct because a power inhabits the trees, not "
                "because forest is pretty.",
                "Greek groves are often walled and priest-staffed for Olympian names; "
                "Serer woods in this source are the sanctuary itself, without a temple "
                "of Roog.",
            ),
            (
                "Shinto chinju no mori (shrine forest)",
                "Both keep old trees as the house of presence rather than as lumber.",
                "Shinto forest is attached to shrine buildings and kami-names in writing; "
                "Bérenger's Serer forest is the building.",
            ),
        ),
    },
    {
        "n": 26,
        "title": "Takhar's Priests Judge Theft and Sorcery",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Le dieu Takhar a pour ministres ou prêtres des vieillards recrutés dans "
            "certaines familles, ce sont eux qui jugent les questions de vol et de "
            "sorcellerie. Quand un individu a été volé, il va porter sa plainte au "
            "prêtre du Dieu Takhar auquel il donne tous les renseignements qu'il peut "
            "fournir, indiquant les soupçons qu'il a contre tel ou tel voisin; le "
            "prêtre en instruit le Dieu à l'aide de prières appropriées."
        ),
        "roman": (
            f"{ROMAN}. Priests of Takhar: elders recruited from certain families; they "
            "judge theft and sorcery. The priest instructs the god by prayer. Bérenger's "
            "\"savage\" is observer contempt, not the office."
        ),
        "tr": (
            "The god Takhar has for ministers or priests old men recruited from certain "
            "families. They are the ones who judge questions of theft and of sorcery. "
            "When someone has been robbed, he takes his complaint to the priest of the "
            "god Takhar, gives all the information he can, and names the neighbors he "
            "suspects. The priest instructs the god by means of prayers fitted to the "
            "case."
        ),
        "comm": (
            "The claim is that justice is a priesthood before it is a police. Theft and "
            "sorcery are the two crimes that matter because both steal what a person is "
            "or has. Takhar's elders are recruited from certain families: office is "
            "kinship, as the lamane is kinship with soil. The procedure is speech. The "
            "wronged person brings information and suspicion. The priest does not first "
            "invent a dungeon. He instructs the god by prayer. Bérenger's sneer that "
            "the prayer matches the gift rather than the object is colonial suspicion, "
            "named as divergence, not as doctrine. The teaching is that a stolen thing "
            "is a matter for the forest-justice, and that the god must be told. Guilt "
            "may then fall as illness; that consequence is recorded as belief, not as "
            "a recipe. Unit 13's gisanekal searches from a death; this unit's priest "
            "searches from a complaint. Together they say: hidden harm is not left to "
            "the strong. Existentially, modern life either litigates everything or "
            "gossips everything. This office is a third: a named elder who can speak "
            "the theft to a justice that is not the complainant's appetite. You cannot "
            "appoint yourself priest of Takhar. You can take one real loss to a fair "
            "elder rather than to a crowd, and you can pray the facts without adding "
            "vengeance as if it were information."
        ),
        "prac": (
            "If something was taken from you (an object, credit, a story), do not post "
            "it. Tell the facts once to one fair person older than the quarrel. Ask for "
            "rightness, not for a show. If nothing was taken, practice the same restraint "
            "on a rumor you were about to complete."
        ),
        "terms": kt(
            (
                "Takhar",
                "justice as a living forest presence whose priests are family-elders -> "
                "not a sky-God court -> Roog remains unaddressed while theft is spoken "
                "to Takhar",
            ),
            (
                "prêtres",
                "old men of certain families who judge theft and sorcery -> kinship "
                "clergy of justice -> \"witch-finder\" is the colonial collapse of the "
                "office",
            ),
            (
                "vol / sorcellerie",
                "theft and sorcery as the two judged questions -> stealing goods and "
                "stealing soul as one department -> modern law splits them; this cult "
                "does not",
            ),
        ),
        "res": res(
            (
                "Exodus 18 (elders judging ordinary cases under a higher law)",
                "Both lodge day-to-day judgment in elders who still stand under a larger "
                "justice they do not invent.",
                "Mosaic elders sit under YHWH's Torah; Takhar's priests pray a "
                "tree-dwelling justice and do not address Roog.",
            ),
            (
                "Lasnet's gisanekal (this collection, unit 13)",
                "Both authorize a specialist of hidden harm rather than leaving soul-crime "
                "or theft to private force.",
                "Gisanekal starts from a death; Takhar's priest starts from a complaint "
                "of stolen goods or sorcery.",
            ),
        ),
    },
    {
        "n": 27,
        "title": "The Lizard Taken to the Smith",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Celui qui a été la victime d'un rapt, fait annoncer par eux au son du "
            "tam-tam qu'il a pris un lézard et qu'il va le porter chez le forgeron. Il "
            "est bien rare que le lendemain matin l'objet volé ne soit pas remis en "
            "place car chaque Sérère est persuadé que les coups donnés par le forgeron "
            "au lézard retentiraient au centuple sur le voleur et entraîneraient bientôt "
            "sa mort."
        ),
        "roman": (
            f"{ROMAN}. Public analogical justice: a lizard is announced, taken to the "
            "smith; blows on the lizard would multiply on the thief. Practice for the "
            "reader is publicity of loss, not harm to an animal."
        ),
        "tr": (
            "The victim of a theft has it announced by the priests to the sound of the "
            "drum that he has taken a lizard and is going to carry it to the smith. It "
            "is rare that the next morning the stolen object is not put back in place, "
            "for each Serer person is persuaded that the blows the smith would give the "
            "lizard would resound a hundredfold on the thief and would soon bring his "
            "death."
        ),
        "comm": (
            "The claim is that public analogical binding can return a stolen object "
            "without a prison. The drum makes the loss civic. The lizard is a stand-in "
            "body. The smith is the transformer of metal, already a threshold person in "
            "West African cosmologies, here the one whose blows would multiply. The "
            "thief, hearing the announcement, prefers to restore the thing rather than "
            "host those blows. Bérenger records this as a curiosity of priests' revenue. "
            "The recoverable philosophy is sharper. Justice here works by publicity plus "
            "homology: a small body stands for a hidden agent, and the village is told. "
            "That is Takhar's department in a concrete rite. This collection will not "
            "teach striking an animal. The usable core is the opposite of private "
            "revenge: you announce, you analogize, you wait overnight. Restoration is "
            "the success, not the death. Existentially, online life is full of lizards "
            "struck in public for sport. This rite is narrower. It aims at the return "
            "of a particular object by frightening a particular thief who still lives "
            "in the same moral weather. You can copy only the announcement and the "
            "overnight wait."
        ),
        "prac": (
            "If something of yours is missing, name the loss out loud to one other "
            "person today. Do not plot a private revenge and do not harm a creature. "
            "Let the naming be the first justice, then wait one night before you act."
        ),
        "terms": kt(
            (
                "lézard",
                "the lizard as analogical body of the thief -> homology, not zoology -> "
                "a mascot reading misses that blows are believed to transfer",
            ),
            (
                "forgeron",
                "the smith as the one whose strikes would multiply -> a transformer of "
                "hidden into visible force -> \"blacksmith\" as mere trade misses the "
                "office in this rite",
            ),
            (
                "tam-tam",
                "the drum that makes the theft public -> justice begins as announcement "
                "-> a silent suspicion would not return the object",
            ),
        ),
        "res": res(
            (
                "West African oaths at the smith's forge (regional structure)",
                "Both treat the smith as a dangerous transformer before whom hidden "
                "wrongs become costly.",
                "Forge-oaths vary by people; Bérenger's Serer instance is specifically "
                "the announced lizard carried toward the hammer.",
            ),
            (
                "2 Samuel 12 (Nathan's analogical ewe-lamb that indicts the thief)",
                "Both use a stand-in creature to make a hidden taking public and "
                "unbearable to the taker.",
                "Nathan speaks a parable to a king under YHWH; the Serer lizard is "
                "drummed toward a smith under Takhar.",
            ),
        ),
    },
    {
        "n": 28,
        "title": "Bante: The Soul Enclosed in a Canari",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Celui qui veut se venger d'un ennemi, vient trouver le Fitaure qui est le "
            "ministre religieux en même temps que le chef d'une agglomération et il "
            "tâche de le décider, à force de cadeaux, à faire le Bante : terrible "
            "opération qui frappe de terreur les plus braves du pays. Au milieu de "
            "maints présents, il a mis un canari (gros vase en terre rouge) vide, si "
            "le Fitaure agrée ce qui lui est offert, il fait diverses cérémonies qui "
            "ont pour but d'enfermer l'âme de l'ennemi dans le canari, et ce vase est "
            "déposé sous un baobab ou un fromager consacré. Celui dont l'âme est ainsi "
            "enfermée dans un canari, meurt peu de temps après."
        ),
        "roman": (
            f"{ROMAN}. Key terms: Bante — enclosing a soul in a canari; Fitaure — "
            "religious-and-civic head. Bérenger's poison-suspicion is colonial "
            "divergence, not Serer doctrine."
        ),
        "tr": (
            "One who wants vengeance on an enemy comes to the Fitaure — religious "
            "minister and head of a settlement at once — and tries, by gifts, to have "
            "him perform the Bante, a terrible operation that strikes terror even in "
            "the bravest of the land. Among the presents is an empty canari, a large "
            "red earthen jar. If the Fitaure accepts, he performs ceremonies whose aim "
            "is to enclose the enemy's soul in the canari, and the jar is placed under "
            "a consecrated baobab or fromager. The one whose soul is thus enclosed dies "
            "not long after."
        ),
        "comm": (
            "The claim is that a soul can be bound in a vessel and parked under a "
            "consecrated tree — and that this possibility is already a politics of fear. "
            "Bante is unit 10's grammar turned to harm. Milk at the baobab binds a house "
            "to a spirit; the canari under the same kind of tree binds a someone against "
            "their will. The empty red jar is not a symbol. In the reported rite it is "
            "a prison of personal life. The tree is the sanctuary of units 3 and 25. "
            "Enclosure plus sanctuary is what makes the brave afraid. Bérenger then "
            "adds his colonial poison-suspicion: perhaps the Fitaure poisons the family "
            "to keep the superstition useful. That sentence is named here as divergence, "
            "not as doctrine. It tells you how the observer needed the rite to be a "
            "fraud. The teaching recoverable without that sneer is already severe. "
            "Binding is morally two-faced. The same cosmology that feeds the dead and "
            "the field can enclose an enemy's soul because souls are personal, local, "
            "and movable. This collection does not teach Bante as a thing to do. It "
            "teaches the terror as evidence of the metaphysics: if souls could not be "
            "housed, a jar under a baobab would be pottery. Existentially, most harm "
            "you will meet is already a small Bante — rumor, exclusion, a file, a "
            "silent campaign — an attempt to put a life in a vessel and set it where "
            "it cannot breathe. The practice is to refuse that office, not to acquire "
            "it."
        ),
        "prac": (
            "Notice one way you have tried to enclose another person's life (a rumor, "
            "a silent punishment, a withheld word). Release one enclosure today: speak "
            "a fair sentence, drop a campaign, or return a freedom. Do not practice "
            "binding a soul."
        ),
        "terms": kt(
            (
                "Bante",
                "the operation of enclosing a soul in a canari under a consecrated tree "
                "-> binding used as fear -> \"hex\" is too folkloric; this is cult-grammar "
                "turned against a someone",
            ),
            (
                "canari",
                "large red earthen jar -> the empty vessel as prison of personal life -> "
                "pottery as hardware (\"fetish\") misses that the jar is a house",
            ),
            (
                "Fitaure",
                "religious minister and civic head of a settlement -> the one who can "
                "accept the gifts and perform the enclosure -> not a mere mayor and not "
                "a mere sorcerer",
            ),
        ),
        "res": res(
            (
                "Aeschylus, binding spells and jar-like constraint of a hated name "
                "(katadesmos, structural)",
                "Both imagine a person constrained by placing a life into a vessel or "
                "formula parked in a sacred place.",
                "Greek katadesmos is often underworld-written; Bante is tree-sanctuary "
                "animism administered by a civic-religious head.",
            ),
            (
                "Mark 5:1–13 (a legion of spirits sent into a herd — souls movable "
                "between vessels)",
                "Both treat personal life as transferable between bodies and containers.",
                "The Gospel scene is exorcism under Jesus' authority; Bante is enclosure "
                "for vengeance, which this collection refuses as practice.",
            ),
        ),
    },
    {
        "n": 29,
        "title": "The Ordeal Drink Is Milder Here",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Les prêtres du dieu Takhar sont aussi chargés de juger les accusations de "
            "sorcellerie; ils examinent les individus incriminés, leur préparent un "
            "breuvage qui a la propriété de les faire mourir si réellement ils sont "
            "sorciers, et qui est simplement rejeté s'ils n'entretiennent aucune "
            "relation avec les esprits infernaux. Seulement, comme à mesure que les "
            "Sérères ont gagné les environs du cap Vert... l'épreuve que ces prêtres "
            "font subir aux accusés a été moins terrible. La mort ne s'en suit que tout "
            "juste assez pour entretenir le bas peuple dans une salutaire crainte de "
            "la divinité."
        ),
        "roman": (
            f"{ROMAN}. Takhar's priests judge sorcery by a drink that kills the guilty "
            "and is rejected by the innocent. Bérenger records the Serer ordeal as "
            "milder than Casamance. The drink is not a practice to copy."
        ),
        "tr": (
            "The priests of the god Takhar are also charged with judging accusations of "
            "sorcery. They examine the accused and prepare a drink that will kill them "
            "if they are truly sorcerers, and that is simply rejected if they keep no "
            "relation with infernal spirits. As the Serer have come toward Cap-Vert, "
            "into opener country, the ordeal has been less terrible than among the "
            "peoples of Casamance. Death follows only just enough to keep a salutary "
            "fear of the divinity."
        ),
        "comm": (
            "The claim is that hidden soul-crime is put to a bodily test, and that Serer "
            "practice in this source is already a milder form of a wider Senegambian "
            "ordeal. Bérenger cannot help sneering at \"salutary fear\" and \"the lower "
            "people.\" That contempt is not the teaching. The teaching is comparative "
            "and philosophical at once. Toward the open Cap-Vert the forest thickens "
            "less, accusations weigh less, and the drink is less often death. Toward "
            "Casamance the same structure is harsher. Geography of sanctuary (unit 25) "
            "and geography of ordeal travel together. Truth about sorcery is not a "
            "rumor the village votes on. It is a sip the body accepts or rejects. This "
            "collection will not teach anyone to drink a deciding poison. Lasnet already "
            "recorded poison and fire beside gisanekal. The usable core is the refusal "
            "of mere talk. An accusation of soul-theft demands a procedure, and the "
            "Serer procedure is recorded as less lethal than their southern neighbors'. "
            "Existentially, online accusation is an ordeal with no priest and no milder "
            "form. The practice is to refuse the sip you want someone else to take, and "
            "to sit with not-knowing rather than demand a body as proof."
        ),
        "prac": (
            "When you next want a test that would settle someone's guilt in a gulp, "
            "refuse that sip. Sit with not-knowing for one hour. Then do one fair act "
            "that does not require a verdict. Do not play with drink, fire, or public "
            "ordeal."
        ),
        "terms": kt(
            (
                "breuvage",
                "the ordeal drink prepared by Takhar's priests -> accepted death if "
                "guilty, rejection if innocent -> not a toast and not a recipe",
            ),
            (
                "Cap-Vert / Casamance",
                "opener country versus forest south -> Bérenger's map of why Serer "
                "ordeal is milder -> geography of trees and geography of fear are one "
                "dossier",
            ),
            (
                "esprits infernaux",
                "Bérenger's gloss for the powers a sorcerer would keep -> colonial "
                "\"infernal\" imports a Christian hell -> the Serer middle is mammam "
                "and pangool, which can harm without being Satan",
            ),
        ),
        "res": res(
            (
                "Numbers 5 (the ordeal drink of bitter water)",
                "Both put a hidden sexual or cultic accusation to a drink whose effect "
                "on the body is taken as the god's verdict.",
                "Numbers is priestly law under YHWH for suspected adultery; Takhar's "
                "drink is sorcery-judgment in a tree-religion that does not address Roog.",
            ),
            (
                "Lasnet's fire-ordeal on the tongue (this collection, unit 13)",
                "Both record a bodily test of the accused in the same people.",
                "Lasnet's iron is gisanekal's search after a death; Bérenger's drink is "
                "Takhar's priests judging a sorcery charge, and he insists it is milder "
                "than Casamance.",
            ),
        ),
    },
    {
        "n": 30,
        "title": "The Offerings No Longer Vanish Overnight",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "On le rend favorable à sa maison en déposant au pied de certains arbres "
            "désignés, des cadeaux de plus ou moins grand prix et, chose bizarre, quel "
            "que soit le volume de l'objet, la grosseur de la bête offerte au Dieu, "
            "l'offrande disparaissait jadis dans la nuit suivante. Mais hélas! les "
            "Dieux s'en vont, peut-on dire, au cap Vert comme ailleurs; aussi, peu à "
            "peu les Sérères sont moins fervents et bien plus, dans nombre d'endroits, "
            "ils sont arrivés à ne plus déposer au pied de l'arbre sacré que les cornes, "
            "les pieds, les entrailles de la bête immolée en l'honneur du Dieu et mangée "
            "par la famille du dévot. Depuis ce temps, ces bas morceaux ne disparaissent "
            "plus et s'amoncellent de plus en plus autour de l'arbre séculaire."
        ),
        "roman": (
            f"{ROMAN}. Tiurakh's gifts once vanished overnight; now only horns, feet, "
            "and entrails are left, and they pile up. \"The gods are leaving\" is a "
            "theological diagnosis. Priest-theft is Bérenger's sneer, named as divergence."
        ),
        "tr": (
            "One renders Tiurakh favorable to one's house by depositing gifts of greater "
            "or lesser price at the foot of certain designated trees. Once, whatever the "
            "size of the object or the beast, the offering would vanish in the following "
            "night. But the gods are leaving, at Cap-Vert as elsewhere. The Serer grow "
            "less fervent, and in many places they now deposit at the foot of the sacred "
            "tree only the horns, the feet, the entrails of the beast offered to the god "
            "and eaten by the devotee's family. Since then those low pieces no longer "
            "disappear; they pile up around the age-old tree."
        ),
        "comm": (
            "The claim is that when the gift is reduced to leftovers, the gods withdraw. "
            "Bérenger cannot resist the priest-theft theory: of course the offerings "
            "used to vanish, the clergy ate them. That suspicion is named as colonial "
            "divergence. It may even be partly worldly fact. It is not the teaching. "
            "The teaching is the sequence he records despite himself. Full gifts vanished "
            "overnight — the forest-sanctuary received them. Then fervor thinned. Then "
            "the house kept the meat and left the gods the waste. Then the waste stayed "
            "and piled. \"Les Dieux s'en vont\" is a theological diagnosis wearing a "
            "French sigh. A religion of increase dies when the house eats as owner and "
            "pays the tree in horns. That is unit 11 inverted. First-fruits always "
            "offered becomes last bits never taken. The age-old tree of unit 25 is still "
            "there; the relation has become a dump. Existentially, this is how most "
            "inherited cults end in a life: not by argument, by leftover. You still "
            "perform a gesture. You keep the feast. The sanctuary receives garbage. "
            "The practice is to notice one offering you have already reduced to horns, "
            "and to restore a first portion or to stop pretending."
        ),
        "prac": (
            "Find one devotion you have reduced to leftovers (thanks after the treat, "
            "a relation you only text, a place you visit as a dump). Either restore a "
            "first portion today or stop the gesture. Do not leave horns and call it "
            "faith."
        ),
        "terms": kt(
            (
                "les Dieux s'en vont",
                "the gods are leaving -> Bérenger's sigh, recoverable as diagnosis -> "
                "not only secularization-as-progress; a relation starved of first-gifts",
            ),
            (
                "cornes / entrailles",
                "horns, feet, entrails left at the tree while the family eats the beast "
                "-> leftover cult -> the opposite of prémices toujours offertes",
            ),
            (
                "Tiurakh",
                "the power of increase who was to receive the whole gift -> when paid in "
                "waste, increase has already been privatized -> prosperity without "
                "offering is the pile around the tree",
            ),
        ),
        "res": res(
            (
                "Malachi 1:7–8 (polluted offerings, leftover animals)",
                "Both diagnose a cult that still brings something to the holy place while "
                "keeping the better portion.",
                "Malachi speaks for YHWH's altar and table; Bérenger records Tiurakh's "
                "tree paid in entrails as the gods depart Cap-Vert.",
            ),
            (
                "Bhagavad Gītā 3.13 again, now in the negative",
                "Both treat eating the offering-share as breaking the cycle of increase.",
                "The Gītā threatens leftover-eaters as thieves; the Serer record shows "
                "the pile of uneaten waste as the visual of gods leaving.",
            ),
        ),
    },
    {
        "n": 31,
        "title": "Fitaure Is Religious and Civic Head",
        "src": "Bérenger-Féraud 1879, Les Sérères — Religion",
        "fr": (
            "Celui qui veut se venger d'un ennemi, vient trouver le Fitaure qui est le "
            "ministre religieux en même temps que le chef d'une agglomération. La "
            "famille qui sait qu'on a fait un Bante contre elle... chacun se hâte de "
            "faire des concessions pour être délivré du danger qui le menace, ce qui "
            "rapporte encore plus d'un profit au Fitaure médiateur naturel du conflit."
        ),
        "roman": (
            f"{ROMAN}. Key term: Fitaure — religious minister and head of a settlement "
            "at once; natural mediator of Bante-conflict. Revenue-sneer is Bérenger's, "
            "not the definition of the office."
        ),
        "tr": (
            "The one who wants vengeance comes to the Fitaure, who is the religious "
            "minister and at the same time the head of a settlement. A family that knows "
            "a Bante has been made against it hurries to make concessions to be delivered "
            "from the danger. The Fitaure is the natural mediator of the conflict."
        ),
        "comm": (
            "The claim is that at village scale there is no split between mayor and "
            "priest. The one who can enclose a soul in a canari is also the civic head. "
            "Fitaure is the word Bérenger records for that joint. Lasnet's lamane holds "
            "the soil and supplies village chiefs; Fitaure names the religious face of "
            "the agglomeration. Read together, Serer public life is land-office plus "
            "cult-office, sometimes in one person. Bérenger sees only a racket: gifts "
            "to start the Bante, gifts to mediate it. That is how a colonial official "
            "sees any unseparated power. The recoverable teaching is older. If ancestor "
            "and land are one cult, the head of a settlement is already standing on a "
            "god. Separating \"politics\" from \"religion\" would be the foreign theory. "
            "Mediation is the humane side of the same office that can terrify. The "
            "Fitaure who can bind can also unbind. That is why the threatened family "
            "runs to him. Existentially, moderns keep inventing \"spiritual\" leaders "
            "with no civic skin and civic leaders with no cult of the ground. This "
            "office refuses the split. You cannot become a Fitaure by mood. You can "
            "notice who in your actual place holds both the keys and the rites, and "
            "you can take one conflict to a mediator who still answers to a ground, "
            "not to a brand."
        ),
        "prac": (
            "Name the person who actually holds both practical authority and a rite of "
            "your place (a landlord who blesses, an elder who also chairs, a parent who "
            "both feeds and prays). Take one small conflict to them as mediator, not as "
            "judge-shopping. If you hold both roles, mediate once today without adding "
            "fear."
        ),
        "terms": kt(
            (
                "Fitaure",
                "religious minister and civic head of an agglomeration -> unseparated "
                "office -> \"chief\" in an administrative file misses the cult; "
                "\"priest\" misses the village",
            ),
            (
                "médiateur naturel",
                "natural mediator of the Bante-conflict -> the same person who can bind "
                "can unbind -> Bérenger hears profit; the structure is that only the "
                "binder can release",
            ),
            (
                "agglomération",
                "the settlement as such -> Fitaure's scale is the clustered families on "
                "a fold of land, not a nation -> Roog still has no mayor",
            ),
        ),
        "res": res(
            (
                "Melchizedek, king of Salem and priest of God Most High (Genesis 14:18)",
                "Both lodge civic headship and cult-office in one figure.",
                "Melchizedek blesses Abraham in the name of a high God; Fitaure administers "
                "tree-sanctuary binding and does not address Roog.",
            ),
            (
                "Lasnet's lamane as village-head pool (this collection, unit 22)",
                "Both grow public office out of a religious relation to land and people.",
                "Lamane is land-master transmitting soil; Fitaure is the named "
                "religious-civic head who can perform Bante.",
            ),
        ),
    },
    {
        "n": 32,
        "title": "They Live Where They Were Born",
        "src": "Bérenger-Féraud 1879, Les Sérères — Mœurs",
        "fr": (
            "Les Sérères sont doux, vivent sur leur sol auquel ils sont extrêmement "
            "attachés et ont aussi peu l'amour de la migration que les Sarakolais l'ont "
            "beaucoup. Ils passent volontiers leur vie là où ils sont nés, groupés par "
            "familles dans un pli de terrain qu'ils ont mis en culture et auquel ils "
            "font rapporter de belles récoltes."
        ),
        "roman": (
            f"{ROMAN}. Ethical temperament of cosaan: live where you were born, grouped "
            "by families in a fold of cultivated land. Little love of migration."
        ),
        "tr": (
            "The Serer are gentle, live on their soil to which they are extremely "
            "attached, and have as little love of migration as the Soninke have much. "
            "They willingly pass their lives where they were born, grouped by families "
            "in a fold of land they have put under cultivation and made to yield fine "
            "harvests."
        ),
        "comm": (
            "The claim is that the good life is staying. Bérenger, who wanted roads and "
            "quiet producers for French commerce, almost blesses this temperament. His "
            "use of it is not the teaching. The teaching is the ethic inside the cult. "
            "A people who name God as sky, address mammam of field and house, pour "
            "first-fruits, bury facing east, and refuse voluntary exile will also "
            "describe the happy life as remaining in the fold of earth that already "
            "knows their dead. Grouped by families is not a demographic note. It is "
            "unit 9 in a landscape sentence: the cult-cell is visible from a hill. "
            "Comparison with the Soninke (Sarakole) love of migration makes the point "
            "by contrast. Senegambia contains both ethics. Serer cosaan is the staying "
            "one. Yield (belles récoltes) is not capitalism; it is Tiurakh answered by "
            "people who did not wander off the bond. Existentially, this unit will "
            "accuse most of its readers. The answer is not to fake a peasant life. It "
            "is to stop calling motion the only adult virtue, and to practice one "
            "form of staying — a field, a street, a dead, a tree — as if the fold of "
            "land could still report a harvest."
        ),
        "prac": (
            "Stay in one actual fold today: one room, one block, one field-edge. Do "
            "one cultivating act there (clean, water, mend, cook) as if yield still "
            "mattered to the dead of that place. Do not plan a departure while you do "
            "it."
        ),
        "terms": kt(
            (
                "sol",
                "the soil they live on and are extremely attached to -> the partner of "
                "the family dead -> \"countryside\" as tourism misses the vow",
            ),
            (
                "pli de terrain",
                "a fold of land grouped by families and put under cultivation -> the "
                "visible cell of ancestor-land cult -> not a nation-state and not a farm "
                "brand",
            ),
            (
                "amour de la migration",
                "love of migration, which the Serer have little of -> the contrasting "
                "ethic (Soninke) proves this is a choice of cosmos, not a lack of roads",
            ),
        ),
        "res": res(
            (
                "Micah 4:4 (each under his vine and fig tree)",
                "Both imagine the good life as staying on a particular cultivated ground "
                "rather than as conquest or flight.",
                "Micah's peace is eschatological under YHWH; Bérenger's Serer staying is "
                "present-tense cosaan on a family fold, with Roog unaddressed.",
            ),
            (
                "Lasnet's jamais volontairement (this collection, unit 17)",
                "Both make non-departure the Serer religious temperament, not a tourist "
                "trait.",
                "Lasnet stresses the sanction (refused burial); Bérenger stresses the "
                "willing life where one was born and the harvest that follows.",
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
        "source_id": f"SEN_ANIM_{n:03d}",
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
            "category": "senegambian-animism",
            "verse": str(n),
            "section": u["src"],
            "cultural_context": NOTE,
            "original_source": u["src"],
            "original_reliability": (
                "SOURCED — French ethnographic report of Serer oral teaching; "
                "Lasnet 1900 / Bérenger-Féraud 1879; OCR cleaned"
            ),
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
        uid = name[:-4].replace("_", ".", 1)
        # files are senegalese_animism_senegalese_animism_001.yml
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

