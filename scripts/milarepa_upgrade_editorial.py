#!/usr/bin/env python3
"""Refresh commentary, key_terms, resonances, and practice for Milarepa pilot units."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANON_DIR = ROOT / "data" / "canonical" / "milarepa_songs"
YAML_DIR = ROOT / "data" / "yaml" / "milarepa_songs"

# Skip MIL_WISDOM_003 — handled by milarepa_upgrade_wisdom_003.py
UPGRADES: dict[str, dict[str, Any]] = {
    "MIL_SORROW_001": {
        "title": "Grace Cools Wrath at the Aunt's Door",
        "insight": "Justified rage does not authorize retaliation when the guru's command binds the disciple.",
        "commentary": """The song's claim is that justified rage does not authorize retaliation when the guru's command binds the disciple. Milarepa inventories every cruelty—the scattered orphans, the mother dead of poverty, the sister wandering, the return to native land as prison—and arrives at the aunt's door with full cause for anger. The counterintuitive move: he names the cause ("Think on it, aunt and uncle") yet petitions for alms rather than revenge, framing his restraint not as weakness but as obedience to Marpa's *bka'*. The dying-insect-at-anthill image reverses expectation: the victim is drawn toward the site of wounding not from masochism but from the exhausted logic of kin and homeland. Kagyü biographies stage this scene as the test of whether Milarepa's black-magic past has truly ripened into dharma; cooling wrath through guru grace (*mar pa'i byin rlabs*) is the proof. Existentially: suffering that would justify breaking vows becomes the very material of vow-keeping.""",
        "key_terms": [
            {
                "term": "byin rlabs",
                "definition": "Etymology: *byin* (bestow) + *rlabs* (waves, overflow) → grace, blessing, empowered influx. The closing plea asks Marpa's grace to cool wrath—not willpower but lineage power transmissible from guru to disciple. Default \"blessing\" misses the wave-like, almost physical descent of grace in Tibetan devotion.",
            },
            {
                "term": "bka'",
                "definition": "Etymology: command, word, speech of authority. Milarepa restrains anger because he is \"fulfilling my guru's commands\"—*bka'* is not generic advice but binding instruction from the lama. The aunt's assault tests whether oral vows outweigh kin rage.",
            },
            {
                "term": "khro ba",
                "definition": "Etymology: anger, wrath, heat. Milarepa admits \"good cause for anger\" yet asks grace to cool his suppliant's wrath. The song does not deny anger's legitimacy; it relocates its resolution from retaliation to guru-devotion.",
            },
            {
                "term": "slong ba",
                "definition": "Etymology: to beg alms, solicit support. Returning to beg at the persecutor's door is the song's dramatic knot: the mendicant needs food for practice from the very kin who ruined his family. Alms become sacrament of vow over vengeance.",
            },
        ],
        "resonances": [
            {
                "citation": "Epictetus, Enchiridion 1",
                "resonance": "Structural homology: Milarepa names injuries yet refrains because a higher binding (guru command) governs response—parallel to Epictetus's insistence that events do not disturb unless judgment assents.",
                "divergence": "Stoic assent is rational self-governance; Milarepa's restraint is devotional obedience and grace-dependent cooling of *khro ba*.",
            },
            {
                "citation": "Bhagavad Gītā 3.19 (action without attachment to fruit)",
                "resonance": "Milarepa acts (begging, practicing) without seizing the fruit of revenge though he has cause—karmic action subordinated to religious vow.",
                "divergence": "Arjuna's frame is cosmic duty in war; Milarepa's is biographical restitution within guru-disciple lineage after crimes of black magic.",
            },
            {
                "citation": "Dōgen, Shōbōgenzō, Genjōkōan",
                "resonance": "Suffering and impermanence are not denied but metabolized into practice rather than consolation—flowers fall amid longing; orphans scatter amid vow.",
                "divergence": "Dōgen's move is epistemological reversal; Milarepa's is narrative biography with explicit persecutor still alive at the door.",
            },
        ],
        "practice": """When someone who injured you speaks sharply, pause before crafting your case. Name internally what happened, then ask whether answering would serve truth or merely cool your injury with their humiliation. If a vow, promise, or discipline binds you, state that binding once—silently or aloud—before you respond or withhold response.""",
    },
    "MIL_ZEAL_002": {
        "title": "Words Do Not Yield True Fruit",
        "insight": "Liberation is agricultural work on the mind; exposition alone cannot harvest it.",
        "commentary": """Milarepa's plough-field song argues that liberation is agricultural work on the mind (*sems kyi zhing*), not intellectual harvest from exposition. The counterintuitive move: after elaborate metaphorical machinery—oxen of undistracted thought, whip of *brtson 'grus*, granary without concepts—the dream-interpretation punchline dismisses words and teaching themselves as insufficient (*tshig gis 'bras bu mi 'byung*). This is not anti-intellectualism but hierarchy of means: faith-water and prayer-rain prepare the field; method and reason plough; karma's sickle reaps; gods roast the grain; yet only meditation's zeal finds the treasure. Evans-Wentz frames it as yogic agriculture; in mahāmudrā oral commentaries the granary \"to which no concept applies\" points at *don dam* fruition stored beyond conceptual fixation. The song counsels a mendicant pleading for successful solitude—consistent with Chapter X's arc of meditation in retreat. Zeal here is neither frenzy nor guilt-driven hustle but sustained *brtson 'grus* applied where language stops yielding.""",
        "key_terms": [
            {
                "term": "brtson 'grus",
                "definition": "Etymology: exertion, diligence, zeal. The whip goading oxen of undistracted thought—*brtson 'grus* is applied force in meditation, not worldly busyness. Evans-Wentz \"zeal and perseverance\" captures the dual aspect: fervor plus endurance.",
            },
            {
                "term": "sems kyi zhing",
                "definition": "Etymology: *sems* (mind) + *zhing* (field). The plough metaphor's ground: mind cultivated like soil. Default \"field of tranquil mind\" preserves the agrarian logic—without tillage, seed and rain accomplish nothing.",
            },
            {
                "term": "don dam",
                "definition": "Etymology: ultimate, supreme truth. Sublime fruits stored in the concept-free granary are *don dam* harvest— fruition that cannot be contained in ordinary categories. The metaphor refuses to name enlightenment as a thing among things.",
            },
            {
                "term": "las kyi bden pa",
                "definition": "Etymology: truth of action, karmic law. The sickle that reaps the noble life—karmic causality as harvesting instrument, not moralistic bookkeeping. Action's truth cuts what hypocrisy and ignorance grew.",
            },
        ],
        "resonances": [
            {
                "citation": "Patañjali, Yoga Sūtra 1.2 (yogaś citta-vṛtti-nirodhaḥ)",
                "resonance": "Both texts subordinate discursive activity to a cultivated stillness that yields fruit words cannot—vṛtti-nirodhaḥ parallels \"words do not yield true fruit.\"",
                "divergence": "Patañjali's framework is systematic darśana; Milarepa's is song-metaphor rooted in mendicant solitude and guru grace.",
            },
            {
                "citation": "Zhuangzi, Book 2 (words vs meaning)",
                "resonance": "Structural homology: language insufficient for the prized catch—fishing nets (words) are not the fish (realization). Milarepa's plough rejects exposition without tillage.",
                "divergence": "Zhuangzi suspends fixed distinctions playfully; Milarepa's field has karmic sickles and gods roasting grain within Buddhist soteriology.",
            },
            {
                "citation": "John of the Cross, Ascent of Mount Carmel II",
                "resonance": "Active meditation must give way to infused knowledge—parallel to zeal in the field versus mere teaching.",
                "divergence": "Christian apophatic mysticism targets union with God; Milarepa's granary stores *don dam* fruits in a Kagyü guru-yogin idiom.",
            },
        ],
        "practice": """Before reading a spiritual text today, spend five minutes on the \"field\"—breath, posture, one sentence of prayer or aspiration. After reading, ask: did I plough or only gather words? If only words, sit five more minutes without summarizing what you read.""",
    },
    "MIL_REPROOF_004": {
        "title": "Solitude Reproves Its Own Restlessness",
        "insight": "Freedom from human company does not free the mind from craving distraction.",
        "commentary": """This is a self-address song (*rang gi sems la glu*): Milarepa speaks to himself in Marpa's voice, reproving the very loneliness solitude induces. The paradox at the center: he chose isolation yet now craves conversation and diversion—exactly what eroticized mind (*yid g.yengs*) would supply. Each imperative chain is somatic: do not walk (feet strike stones), do not raise head (frivolity), do not sleep (*dug lnga* overcome). The counterintuitive move is that freedom from humanity's company does not freedom from mind's restlessness make; solitude intensifies the inner crowd. In Kagyü self-reproof literature, addressing oneself as guru (Dorje Chang in Marpa's form) internalizes the vow-structure without external supervision. The five poisons at the close are not abstract sins but the physiological slide from devotional posture into spaced-out torpor. Reproof is compassion turned inward—harsh syntax as care.""",
        "key_terms": [
            {
                "term": "dben pa",
                "definition": "Etymology: isolation, solitude, separation from crowds. The opening benediction requests successful *dben pa*—yet the song's body exposes solitude's temptation toward distraction. Solitude is achievement, not mood.",
            },
            {
                "term": "yid g.yengs",
                "definition": "Etymology: mental wandering, distraction, scattered attention. \"Do not yield to the desire for distraction\"—*yid g.yengs* is the inner counterpart to the human conversation Milarepa lacks. Solitude without vigilance becomes entertainment-seeking.",
            },
            {
                "term": "dug lnga",
                "definition": "Etymology: five poisons—desire, anger, ignorance, pride, jealousy. Sleep in meditation allows the five poisons to overcome the yogin. The list grounds metaphysics in the drowsy lapse from seat.",
            },
            {
                "term": "rang sems kyi glu",
                "definition": "Etymology: song to one's own mind. Genre marker: Milarepa splits speaker and hearer within one person, using song-form for self-correction. The guru's face (Marpa/Dorje Chang) is internalized as reproving voice.",
            },
        ],
        "resonances": [
            {
                "citation": "Evagrius Ponticus, on acedia in the desert cell",
                "resonance": "Solitude breeds restlessness that seeks escape—Milarepa's \"no reason to seek diversion\" parallels desert fathers' noonday demon.",
                "divergence": "Christian acedia is spiritual sloth toward God; Milarepa's is failure of *dben pa* within tantric guru-yoga discipline.",
            },
            {
                "citation": "Epictetus, Discourses 3.13 (solitude and self-examination)",
                "resonance": "Alone, one must judge one's impressions; Milarepa's somatic commands (seat, head, feet) are anti-distraction technology.",
                "divergence": "Stoic practice is rational audit; Milarepa invokes Dorje Chang and five poisons in Vajrayana somatic vocabulary.",
            },
            {
                "citation": "Dōgen, Fukanzazengi",
                "resonance": "Do not rise from the seat; let go of gaining ideas—parallel to \"do not walk forth; rest content on your seat.\"",
                "divergence": "Dōgen universalizes zazen; Milarepa's reproof is autobiographical self-splitting in a cave hermitage.",
            },
        ],
        "practice": """When boredom or loneliness arises in solitary work, do not reach for conversation or a scroll. Recite one line of self-reproof aloud: \"Do not stir the mind; let it rest.\" Remain seated one minute longer than the impulse to move demands.""",
    },
    "MIL_COMFORTS_005": {
        "title": "Nothing Is Uncomfortable",
        "insight": "Ascetic hardship becomes ease when buddhahood redefines the scale of comfort.",
        "commentary": """Milarepa lists five comforts—hard mattress, cotton quilt, meditation strap, moderated body, clear mind—then declares nothing uncomfortable remains. The counterintuitive claim is ascetic comfort: hardship reframed as ease because the goal (*sang rgyas*) redefines the scale of evaluation. He dismisses pity from worldly visitors (\"Spare me your misplaced pity\") because pity measures comfort against ego's error, not against buddhahood's trajectory. Dragkar-Taso's cave is the laboratory: renunciation of food, clothing, and worldly aims is not deprivation but alignment. When the sun passes and visitors return home, Milarepa enters *ting nge 'dzin*—no time for useless talk. Kagyü hagiography uses this song to invert bourgeois sympathy for the green-skinned yogin: his comfort exceeds palace softness because clinging has been evacuated. Existentially: discomfort is not sensation but conflict between sensation and aim.""",
        "key_terms": [
            {
                "term": "ting nge 'dzin",
                "definition": "Etymology: samādhi, meditative fixation, absorbed concentration. Closing refusal of \"useless talk\" enters *ting nge 'dzin*—not escapism but the quiescent state visitors cannot share. Default \"samadhi\" misses the Tibetan emphasis on unwavering fixity.",
            },
            {
                "term": "bde ba lnga",
                "definition": "Etymology: five comforts. Enumerated ascetic satisfactions—mat, quilt, strap, body, mind—each \"comfortable\" by yogic standards. The song plays on *bde ba* (ease, pleasure) to scandalize worldly pity.",
            },
            {
                "term": "rnal 'byor pa / re pa",
                "definition": "Etymology: yogin; *re pa* (cotton-clad one). Self-designation \"Tibetan yogin called Repa\"—identity tied to Marpa's lineage and cotton robe, not household status.",
            },
            {
                "term": "sang rgyas",
                "definition": "Etymology: awakened, expanded. Self-set task of winning buddhahood reorganizes time: uncertain hour of death makes small talk wasteful. Comfort is measured against awakening, not cushions.",
            },
        ],
        "resonances": [
            {
                "citation": "Katha Upaniṣad 2.1–2 (preyas vs śreyas)",
                "resonance": "Pleasant versus good—worldly pity offers preyas; Milarepa's five comforts serve śreyas (buddhahood).",
                "divergence": "Upanishadic disciple seeks teaching from Death; Milarepa instructs pitying visitors from a cave.",
            },
            {
                "citation": "Epictetus, Discourses 4.6 (rough cloak, hard bed)",
                "resonance": "Philosopher's voluntary hardship as freedom—Milarepa's hard mattress comfortable by aim, not by softness.",
                "divergence": "Stoic comfort is independence from externals; Milarepa's is tantric path to *sang rgyas* with guru devotion.",
            },
            {
                "citation": "Zhuangzi, \"Useless Tree\" (Book 1)",
                "resonance": "What looks miserable thrives because it fails worldly utility—green yogin body useless by palace standards yet victorious.",
                "divergence": "Zhuangzi's uselessness is spontaneous dao; Milarepa's asceticism is vowed, timed, and soteriological.",
            },
        ],
        "practice": """Notice one physical inconvenience today—cold, hunger, stiffness. Before fixing it, ask whether it obstructs your real aim or only your preference. If the latter, bow once mentally and return to your task as Milarepa returns to samādhi when visitors leave.""",
    },
    "MIL_SISTER_006": {
        "title": "Bodhicitta in the Skeleton",
        "insight": "External misery and internal bodhicitta coexist without contradiction.",
        "commentary": """Peta arrives pitying Milarepa's cave, food, and green corpse-like body; he replies that if she could see his mind she would see *byang chub kyi sems* itself. The song's structural move is triple disjunction: dwelling like beast, food like swine, body like skeleton—each would horrify a worldly observer—yet mind rejoices conquering buddhas. Counterintuitive: external misery and internal bodhicitta coexist without contradiction; penance for all sentient beings justifies hardship that looks like madness. The green hue from nettles becomes sign of unchanging practice, not pathology. Milarepa acknowledges melancholy he cannot drive out, yet guru adoration holds steady—honesty without sentimental collapse. For Peta, sorrow is the wrong response; religious penance is the invitation. This is Kagyü pastoral pedagogy: family love redirected through impermanence (*'jig rten gyi dga' sdug mi rtag*) toward practice.""",
        "key_terms": [
            {
                "term": "byang chub kyi sems",
                "definition": "Etymology: mind of awakening, bodhicitta. \"If you could see my mind, it is bodhicitta itself\"—the hidden interior that invalidates exterior pity. Not sentiment but altruistic aim for all beings' liberation.",
            },
            {
                "term": "mi rtag",
                "definition": "Etymology: impermanence, instability. Worldly joys and griefs are impermanent; sister's sorrow attaches to what cannot last. Impermanence is reason for practice, not despair.",
            },
            {
                "term": "dud 'gro",
                "definition": "Etymology: animal realm. Dwelling \"like a jungle beast's lair\"—behavioral resemblance to animal existence while human mind holds bodhicitta. Ascetic exterior mimics lowest realm; interior reverses the mimicry.",
            },
            {
                "term": "ye shes",
                "definition": "Etymology: transcendent knowledge, pristine awareness. Zealous meditation will gain *ye shes* and experience— fruition language beyond mere moral reform. Sister is invited to penance that yields wisdom, not comfort.",
            },
        ],
        "resonances": [
            {
                "citation": "Stoic dichotomy (inner vs outer, Epictetus Enchiridion)",
                "resonance": "Skeleton body vs bodhicitta mind—homology to fortress of inner prohairesis vs externals others pity or envy.",
                "divergence": "Stoic inner is rational assent; Milarepa's inner is *byang chub kyi sems* visible to buddhas, not to kin.",
            },
            {
                "citation": "Bhagavad Gītā 2.11 (wise lament vs wise action)",
                "resonance": "Peta's grief is rebuked as unworthy of the wise—parallel to Krishna correcting Arjuna's sorrow at impermanence.",
                "divergence": "Arjuna's grief is martial; Peta's is familial pity; Milarepa invites penance, not battle.",
            },
            {
                "citation": "Dōgen, \"Being-Time\" (Uji)",
                "resonance": "Green unchanging body-hue as practice-time made visible—outer form bearing duration of meditation.",
                "divergence": "Dōgen's time is phenomenological; Milarepa's green is nettle-diet biography within merit-transfer frame.",
            },
        ],
        "practice": """When someone pities your difficult path, do not argue. Ask whether they can see one inner fact—your aim, vow, or love motivating the hardship. If they cannot, bow and change subject as Milarepa redirects Peta from sorrow toward religious penance.""",
    },
    "MIL_RACE_007": {
        "title": "Ride the Mind-Horse to Buddhahood",
        "insight": "Wild mind must be tacked, fed, and ridden with doctrinally named gear—not generic mindfulness.",
        "commentary": """The mind-horse metaphor systematizes mahāmudrā mind-training as equestrian craft: *gcig tu 'dzin* as lasso, meditation-post as tether, guru's teaching as feed, consciousness-stream as water, emptiness as cold enclosure. The counterintuitive density is tactical—saddle of will, bridle of intellect, rider of watchfulness, arrow of intellect barbed with four immeasurables shot from wisdom's bow to slay selfishness across nations. Worldly happiness is explicitly rejected at the close: the race's finish line is buddhahood, hindquarters leaving samsara behind. Unlike generic \"mindfulness\" metaphors, every tack piece maps to a doctrine: Mahayana altruism as helmet, patience as shield, aspiration as spear. The song asks disciples to judge whether this resembles their idea of happiness—forcing comparison rather than assent. In Kagyü imagery, wind-like mind must be caught or it runs wild through the bodhi-temple of the body.""",
        "key_terms": [
            {
                "term": "sems rta",
                "definition": "Etymology: *sems* (mind) + *rta* (horse). Mind moves like wind through the heart's chamber—must be lassoed or lost. The horse is not enemy but power requiring tack.",
            },
            {
                "term": "gcig tu 'dzin",
                "definition": "Etymology: one-pointedness, single grasp. Lasso to catch the horse—*ekagrata* in Indic terms, one of the named instruments. Without it, mind cannot be tied to meditation-post.",
            },
            {
                "term": "stong pa nyid",
                "definition": "Etymology: emptiness. Enclosure protecting horse from cold—conceptual frame where mind is kept when \"weather\" of reification blows. Not nihilism but protective space in the metaphor system.",
            },
            {
                "term": "tsem med bzhi",
                "definition": "Etymology: four immeasurables—loving-kindness, compassion, joy, equanimity. Arrow feathers barbed with the four—ethicized weaponry slaying selfishness, not enemies.",
            },
        ],
        "resonances": [
            {
                "citation": "Plato, Phaedrus 246a–254e (charioteer and two horses)",
                "resonance": "Psyche as rider managing winged horses—structural homology of intellect guiding volatile motive force toward upward flight.",
                "divergence": "Plato's tripartite soul seeks Forms; Milarepa's tack maps Kagyü doctrines to a race ending in buddhahood.",
            },
            {
                "citation": "Katha Upaniṣad 3.3–9 (chariot metaphor)",
                "resonance": "Self as rider, mind as reins, body as chariot—both traditions weaponize vehicle imagery for spiritual discipline.",
                "divergence": "Upanishadic chariot reaches the atman; Milarepa's horse runs a race leaving samsara's hindquarters behind.",
            },
            {
                "citation": "Zhuangzi, Cook Ding (Book 3)",
                "resonance": "Skillful attunement through repeated practice—tack pieces as cultivated craft, not one-time insight.",
                "divergence": "Zhuangzi's skill is daoist spontaneity; Milarepa's is bodhi-temple architecture with guru-feed and emptiness-enclosure.",
            },
        ],
        "practice": """When attention scatters today, name one \"tack piece\": lasso (single purpose for the next hour), post (breath or seat), feed (one remembered line of teaching), or enclosure (notice the next thought is empty of fixed self). Adjust one piece for two minutes before continuing.""",
    },
    "MIL_DEMON_008": {
        "title": "A Demoness in the Body of an Aunt",
        "insight": "Kin cruelty forged the path; truthful recollection replaces revenge without sentimental merge.",
        "commentary": """Unlike the wisdom song's gift of property, this persecution song memorizes injury without immediate reconciliation—yet still ends with disciplined withdrawal rather than hail-magic. Milarepa catalogs fraud, beatings, near-drowning, forged land theft, uncle's mob, and Zesay's kindly but unreligious visits. The doctrinal naming—*bdud mo* in aunt's body, *srog lcags* severing kin-love—transforms relatives into afflictive forces without denying their humanity. Counterintuitive: he tells aunt to repent and listen, but also sends her away early; compassion here is truthful recollection, not sentimental merge. Zesay's nourishment saved his life yet he minimizes meetings because attachment to kin who reject dharma extends samsara's leash. The song closes Chapter X's persecution arc: kin cruelty forged his path; kin cannot be his resting place. Marpa's kinship (*nged med pas khyed nged du gyis*) frames the orphan's only family as guru-lineage.""",
        "key_terms": [
            {
                "term": "bdud mo",
                "definition": "Etymology: demoness, female obstructing force. \"You are a demoness in the body of an aunt\"—afflictive function named without canceling kinship biology. Māra wears familiar faces.",
            },
            {
                "term": "srog lcags",
                "definition": "Etymology: iron hook of life, life-rope. Kin attachment severed like cut life-cord—persecution destroys familial love that would bind him to revenge cycles.",
            },
            {
                "term": "lo tsA ba",
                "definition": "Etymology: translator—Marpa Lotsawa. Opening homage to Marpa as kin-substitute for the bereft (*nged med*). Guru-lineage replaces clan after clan failed.",
            },
            {
                "term": "a zhang",
                "definition": "Etymology: paternal aunt. Central persecutor throughout Chapter X; here invited to repent and remember. Familiar title (*a zhang*) persists even after demoness naming—complexity of real kin.",
            },
        ],
        "resonances": [
            {
                "citation": "Epictetus, Discourses 4.1 (on toxic associations)",
                "resonance": "Milarepa limits meetings with Zesay and aunt though kindness exists—homology to guarding mind from those who pull toward old life.",
                "divergence": "Stoic withdrawal is cognitive hygiene; Milarepa's is vow-bound retreat after exhaustive narrative of injury.",
            },
            {
                "citation": "Aeschylus, Agamemnon (curse of house)",
                "resonance": "Generational violence in kinship house—Kyanga-Tsa fraud and murderous inheritance echo tragic clan cycles.",
                "divergence": "Greek tragedy ends in doom; Milarepa converts persecution into dharma entry and eventual aunt's repentance elsewhere in biography.",
            },
            {
                "citation": "Dōgen, \"Leave family to seek the Way\" (traditional Zen departure narratives)",
                "resonance": "Attachment to kin who obstruct practice must be cut—Zesay fed him yet cannot be refuge if she rejects religion.",
                "divergence": "Zen departure is often sudden; Milarepa's is decades-long scored recitation with demoness naming.",
            },
        ],
        "practice": """Write one sentence recording a past injury without embellishment or revenge fantasy. Write one sentence on what practice that injury inadvertently forced. If the first sentence only reheats anger, destroy it; keep the second only if it genuinely turns poison into path.""",
    },
}


def _layer(layers: list, kind: str) -> dict | None:
    for layer in layers:
        if layer.get("kind") == kind:
            return layer
    return None


def _strip_embedded_extras(layers: list) -> None:
    for i in range(len(layers) - 1, -1, -1):
        if layers[i].get("kind") in ("key_terms", "resonances"):
            layers.pop(i)


def _insert_after_commentary(layers: list, key_terms: list, resonances: list) -> None:
    insert_at = next(
        (i + 1 for i, l in enumerate(layers) if l.get("kind") == "commentary"),
        len(layers),
    )
    layers.insert(
        insert_at,
        {
            "kind": "key_terms",
            "label": "Key Terms",
            "items": key_terms,
            "layer_provenance": "Original Pratibha key terms",
        },
    )
    layers.insert(
        insert_at + 1,
        {
            "kind": "resonances",
            "label": "Cross-Tradition Resonances",
            "items": resonances,
            "layer_provenance": "Original Pratibha resonances",
        },
    )


def _format_key_terms_md(items: list[dict[str, str]]) -> str:
    lines = ["Key Terms:", ""]
    for item in items:
        lines.append(f"**{item['term']}** — {item['definition']}")
    return "\n".join(lines)


def _format_resonances_md(items: list[dict[str, str]]) -> str:
    lines = ["Cross-Tradition Resonances:", ""]
    for item in items:
        block = f"**{item['citation']}:** {item['resonance']}"
        if item.get("divergence"):
            block += f"\n*Divergence:* {item['divergence']}"
        lines.append(block)
    return "\n\n".join(lines)


def upgrade_doc(doc: dict, data: dict[str, Any]) -> None:
    doc["title"] = data["title"]
    if "unit_label" in doc:
        doc["unit_label"] = data["title"]
    doc["commentary"] = data["commentary"]
    if "insight" in doc or doc.get("source_id"):
        doc["insight"] = data["insight"]
    if "abhyasa" in doc:
        doc["abhyasa"] = data["practice"]
    if "practice" in doc:
        doc["practice"] = data["practice"]
    doc["editorial_maturity"] = "strong_draft"
    doc["editorial_score"] = 82

    layers = doc.get("pratibha_layers")
    if not layers:
        doc["commentary"] = "\n\n".join(
            [
                data["commentary"],
                _format_key_terms_md(data["key_terms"]),
                _format_resonances_md(data["resonances"]),
            ]
        )
        return

    comm = _layer(layers, "commentary")
    if comm:
        comm["body"] = data["commentary"]
        comm["layer_provenance"] = "Original Pratibha commentary; passage-specific Kagyü reading"
    pract = _layer(layers, "practice")
    if pract:
        pract["body"] = data["practice"]

    _strip_embedded_extras(layers)
    _insert_after_commentary(layers, data["key_terms"], data["resonances"])
    doc["pratibha_layers"] = layers


def upgrade_path(path: Path) -> None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    sid = doc.get("source_id") or doc.get("sutra_id", "")
    if sid not in UPGRADES:
        return
    upgrade_doc(doc, UPGRADES[sid])
    path.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    print(f"  editorial: {path.relative_to(ROOT)}")


def main() -> int:
    for sid in UPGRADES:
        slug = sid.lower()
        for base in (CANON_DIR, YAML_DIR):
            p = base / f"milarepa_songs_{slug}.yml"
            if p.exists():
                upgrade_path(p)
    print(f"Refreshed editorial layers for {len(UPGRADES)} units.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
