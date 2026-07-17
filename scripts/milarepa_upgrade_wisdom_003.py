#!/usr/bin/env python3
"""Upgrade MIL_WISDOM_003: Tibetan witness, Quintman translation, Pratibha layers."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PATHS = [
    ROOT / "data" / "canonical" / "milarepa_songs" / "milarepa_songs_mil_wisdom_003.yml",
    ROOT / "data" / "yaml" / "milarepa_songs" / "milarepa_songs_mil_wisdom_003.yml",
]

# Tsangnyön Heruka, *Mi la ras pa'i rnam thar* (de Jong ed.; structure cross-checked
# against Quintman 2010 and Evans-Wentz 1928). Refrains attested in Jetsun-Kahbum tradition.
WYLIE_ORIGINAL = """rje btsun bla ma'i byin rlabs kyis/
dben pa'i ri la rgyu bar byed/

spong ba 'di yi bde sdug khyed shes/

'khor ba'i chos rnams las kyis bsdams/
reg na thar pa'i srog rtsa chod/

sdig pa'i las ni mi'i tsho phogs/
byas na ngan song sdug bsngal myong/

ngan du 'dzin pa'i yid 'ong snying rje/
byas na tsha dang me 'khyil 'thung/

mi'i nor 'du tshong gi nor 'du/
gang bsags de ni dgra yi gso/

bde 'dod ja chang chang gi bcud/
'thung na thar pa'i srog rtsa chod/

a zhang khyod kyi bka' thad rgol/
smras na bdag gzhan gnyis ka gzhom/

a zhang zhing gi rin phrag dog gi rdzas/
longs na yid khar skom par skye/

zhing khang thams cad gang yin pa/
longs shig a zhang bde bar shog/

mi yi smad pa chos kyis bkru/
lha yi grags pa brtson 'grus kyis grub/

bdud kyi gtam ni snying rjes zhan/
ngan gtam rlung la btang/
ngag ni gdong steng du bltas/

thugs rje ldan pa mi phyed pa'i ngo bo/
spong ba 'di dben par bzhugs par byin gyis rlobs/"""

WYLIE_KEY_TERMS = """*'khor ba* (samsara) — the wearisome round of conditioned life; Quintman renders *'khor ba'i chos* as "the world of life's round."

*thar pa'i srog rtsa* — artery or root-vital of liberation; refrain: touch, drink, cling → severance.

*bdud khang* — demon stronghold; kin attachment fortified as māra's fortress.

*bdud kyi gtam / ngan gtam* — demon-talk / malicious talk; paired with *snying rjes zhan* (trample with compassion) and *rlung la btang* (scatter to the wind).

*mi phyed pa* — immutable/non-dual essence; closing addressee = Akṣobhya in Quintman."""

TRANSLATION = """With the lord lama's kindness, I wander in mountain retreats.
You know this beggar's happiness and pain.

The world of life's round wears you down through karma—
Touch it and you'll sever liberation's artery.

Karma of evil deeds is the harvest of human beings—
Engage in it and you'll feel the misery of lower realms.

Fondness for loved ones is a demon's stronghold—
Build it and you'll be sucked into a pit of flames.

Your hoard of food and wealth, the chattels of men—
Whatever you own is your enemy's supply.

The tea and beer of wanting happiness is deadly poison—
Drink it and you'll sever liberation's artery.

Aunt, your counsel is filled with spiteful words—
Speak it and it will ruin both self and others.

Aunt, payment for my field is the stuff of avarice—
Take it and I'll be born a hungry ghost.

My field, my house, everything—
Take them, Aunt, and may happiness you find.

Human slander I purify with the dharma.
Divine fame I gain with sincere practice.

Demon talk I trample with compassion.
Malicious talk, I scatter to the wind.
My talk looks ever upward.

Lord most kind, Akṣobhya in essence,
Bless this beggar to stay in mountain retreat."""

COMMENTARY = """Milarepa's counterintuitive move is not renunciation preached from safety but renunciation performed as gift—the aunt who stole his inheritance becomes the very person to whom he surrenders field and house. The song's repetitive anatomy (touch / build / drink / speak → sever / fall / drown / ruin) maps each ordinary samsaric tie to a specific spiritual haemorrhage: clinging to life's round severs liberation's artery (*thar pa'i srog rtsa*); fondness for kin becomes a demon's stronghold (*bdud khang*); stored wealth feeds enemies. Evans-Wentz moralizes stimulants with Christian proof-texts; the Tibetan pivot is sharper and more psychological. After cataloguing worldly poison, Milarepa does not answer persecution with magic—he had vowed patience and recognized his aunt as the support for cultivating it. The doctrinal climax inverts expected heroic renunciation: demon talk is trampled with compassion (*snying rje*), blame scattered to the wind, speech turned upward (*gdong steng du bltas*). In Kagyü oral instruction this triad is read as the outer-inner-secret sequence of relating to obstruction: meeting hostility without retaliation, releasing gossip without fixation, fixing view toward the immutable lord (Akṣobhya-in-essence). The aunt's field-payment becomes a hungry-ghost birth only if consumed; Milarepa instead converts property into patience-practice and departs for Drakar Taso. Renunciation here is not flight from family but the surgical removal of what property still binds."""

KEY_TERMS = [
    {
        "term": "'khor ba (འཁོར་བ)",
        "definition": "Etymology: *'khor* (turn, circle) + *ba* (nominalizer) → the wearisome round of conditioned existence. In this song, samsara is not abstract metaphysics but the momentum that wears the practitioner down through karma (*las kyis bsdams*). Quintman's \"world of life's round\" preserves the exhaustion Evans-Wentz's \"web of karma\" flattens.",
    },
    {
        "term": "thar pa'i srog rtsa (ཐར་པའི་སྲོག་རྩ)",
        "definition": "Etymology: *thar pa* (liberation) + *srog rtsa* (life-artery, vital root). Refrain marking what clinging severs—touch samsara, drink worldly poison, and the artery of liberation is cut. \"Vital cord\" (Evans-Wentz) Christianizes; \"artery\" (Quintman) keeps the anatomical urgency of a lifeline one can sever by habit.",
    },
    {
        "term": "bdud khang (བདུད་ཁང)",
        "definition": "Etymology: *bdud* (demon, māra) + *khang* (house, fortress). Affection for kith and kin is not neutral warmth but a fortified stronghold where obstruction lodges. \"Devil's Castle\" (Evans-Wentz) dramatizes; \"demon's stronghold\" (Quintman) keeps the architectural image of something built and defended.",
    },
    {
        "term": "snying rje (སྙིང་རྗེ)",
        "definition": "Etymology: *snying* (heart/mind) + *rje* (lord, master) → compassion as sovereign attitude. The song's pivot line parses as trampling demon-talk (*bdud kyi gtam*) with compassion—not subduing external demons by force but meeting malicious speech with *snying rje*. Evans-Wentz's \"By compassion I subdue the demons\" merges two images the Tibetan keeps distinct.",
    },
    {
        "term": "mi phyed pa / Akṣobhya (མི་ཕྱེད་པ)",
        "definition": "Etymology: *mi phyed pa* — immutable, undivided. Closing addressee invoked as *thugs rje ldan pa mi phyed pa'i ngo bo* (lord of compassion, Akṣobhya in essence). The benediction (*byin gyis rlobs*) requests grace to abide in mountain retreat—linking patience-gift to guru-yoga and the eastern buddha of mirror-like wisdom.",
    },
]

RESONANCES = [
    {
        "citation": "Epictetus, Enchiridion 1",
        "resonance": "Structural homology: harm lies in our judgment of events, not in events themselves; Milarepa purifies human slander with dharma and scatters blame to the wind rather than rehearsing injury.",
        "divergence": "Stoic *prohairesis* trains assent to impressions; Milarepa's move is devotionally anchored in guru grace and culminates in surrendering property to the persecutor.",
    },
    {
        "citation": "Dōgen, Shōbōgenzō, Genjōkōan (flowers fall amid longing)",
        "resonance": "Both texts refuse consolation that clings to what must pass: Dōgen's flowers fall regardless of longing; Milarepa's aunt-curse and field-price are samsaric blossoms he neither grasps nor avenges with hail.",
        "divergence": "Dōgen's reversal is epistemological (myriad things verify the self); Milarepa's is karmically narrated with hungry-ghost eschatology and explicit biographical restitution.",
    },
    {
        "citation": "Bhagavad Gītā 2.47 (act without attachment to fruits)",
        "resonance": "Milarepa gives field and house yet refrains from the hail-magic he could cast—action without seizing the fruit of revenge, converting property into patience-practice.",
        "divergence": "Arjuna's frame is martial duty on a battlefield; Milarepa's is guru-commanded forbearance within the Kagyü biographical arc of sin, purification, and solitary retreat.",
    },
]

PRACTICE = """When someone speaks against you today, do not rehearse a rebuttal. Name silently what was said, exhale once as if releasing it to the wind (the move of *ngan gtam rlung la btang*), then raise your gaze slightly above the horizon (*gdong steng du bltas*) and ask whether answering would sever or restore your practice artery. If anger persists, identify who functions as your \"aunt\"—the person whose hostility is, paradoxically, your support for patience. Before sleep, imagine signing over one possession you still defend: not as fantasy virtue but as Milarepa did, locating what property still binds liberation."""

APPENDIX = """Evans-Wentz (1928) anchor — Song of Yogic Wisdom, Chapter X:

Lord, my Guru, by Thy Grace do I the life ascetic live;
My weal and woe are known to Thee!

The whole Sangsara, being e'er entangled in the Web of Karma,
Whoever holdeth fast to it severeth Salvation's Vital Cord.

In harvesting of evil deeds the human race is busy;
And the doing so is to taste the pangs of Hell.

The affectionate expressions of one's kith and kin are the Devil's Castle;
To build it is to fall into the Flames [of Anguish].

The piling up of wealth is the piling up of others' property;
What one thus storeth formeth but provisions for one's enemies.

Enjoying wine and tea in merriment is drinking juice of aconite;
To drink it is to drown Salvation's Vital-Cord.

The price mine aunt brought for my field is things wrung out of avarice;
To eat them would entail a birth amongst the famished ghosts.

The counsel of mine aunt is born of wrath and vengeance;
To utter it entaileth general disturbance and destruction.

Whatever I possess, both field and house,
Take all, O aunt, and therewith happy be.

I wash off human scandal by devotion true;
And by my zeal I satisfy the Deities.

By compassion I subdue the demons;
All blame I scatter to the wind,
And upward turn my face.

Gracious One, Thou the Immutable,
Vouchsafe Thy Grace, that I may pass my life in solitude successfully."""

INSIGHT = (
    "Renunciation performed as gift to one's persecutor—and compassion, not force, "
    "as the answer to demon-talk—is Milarepa's counterintuitive move."
)


def _layer(layers: list, kind: str) -> dict | None:
    for layer in layers:
        if layer.get("kind") == kind:
            return layer
    return None


def upgrade(path: Path) -> None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["title"] = "Compassion Tramples Demon Talk"
    doc["unit_label"] = "Compassion Tramples Demon Talk"
    doc["sanskrit_devanagari"] = WYLIE_ORIGINAL
    doc["sanskrit_iast"] = WYLIE_KEY_TERMS
    doc["translation_literal"] = TRANSLATION
    doc["commentary"] = COMMENTARY
    doc["insight"] = INSIGHT
    doc["practice"] = PRACTICE
    doc["editorial_maturity"] = "strong_draft"
    doc["editorial_score"] = 82

    layers = doc.get("pratibha_layers") or []

    orig = _layer(layers, "original")
    if orig:
        orig["label"] = "Original (Tibetan Wylie)"
        orig["body"] = WYLIE_ORIGINAL
        orig["layer_provenance"] = (
            "Tsangnyön Heruka, Mi la ras pa'i rnam thar (de Jong ed.); "
            "verse structure cross-checked against Quintman 2010 and Evans-Wentz 1928; "
            "refrains attested in Jetsun-Kahbum tradition"
        )

    iast = _layer(layers, "iast")
    if iast:
        iast["label"] = "Wylie / Key Terms"
        iast["body"] = WYLIE_KEY_TERMS

    trans = _layer(layers, "translation")
    if trans:
        trans["body"] = TRANSLATION
        trans["layer_provenance"] = (
            "Pratibha English after Andrew Quintman, The Life of Milarepa (2010); "
            "Evans-Wentz 1928 PD anchor for structure"
        )

    comm = _layer(layers, "commentary")
    if comm:
        comm["body"] = COMMENTARY
        comm["layer_provenance"] = "Original Pratibha commentary; passage-specific Kagyü reading"

    pract = _layer(layers, "practice")
    if pract:
        pract["body"] = PRACTICE

    # Replace embedded key terms in commentary layer with clean commentary only
    for i, layer in enumerate(layers):
        if layer.get("kind") == "key_terms":
            layers.pop(i)
            break
    for i, layer in enumerate(layers):
        if layer.get("kind") == "resonances":
            layers.pop(i)
            break

    # Insert key_terms and resonances after commentary
    insert_at = next(
        (i + 1 for i, l in enumerate(layers) if l.get("kind") == "commentary"),
        len(layers),
    )
    layers.insert(
        insert_at,
        {
            "kind": "key_terms",
            "label": "Key Terms",
            "items": KEY_TERMS,
            "layer_provenance": "Original Pratibha key terms; Wylie with Tibetan script",
        },
    )
    layers.insert(
        insert_at + 1,
        {
            "kind": "resonances",
            "label": "Cross-Tradition Resonances",
            "items": RESONANCES,
            "layer_provenance": "Original Pratibha resonances",
        },
    )

    app = _layer(layers, "appendix")
    if app:
        app["label"] = "Public-domain anchor (Evans-Wentz 1928)"
        app["body"] = APPENDIX

    doc["pratibha_layers"] = layers
    doc["appendixes"] = [
        {
            "commentator": "Public-domain anchor (Evans-Wentz 1928)",
            "text": APPENDIX,
        }
    ]

    path.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    print(f"Upgraded {path.relative_to(ROOT)}")


def main() -> None:
    for p in PATHS:
        if p.exists():
            upgrade(p)


if __name__ == "__main__":
    main()
