#!/usr/bin/env python3
"""Ingest pre-Islamic Fulɓe / Peul practice from public-domain ethnography.

Collection: pulaar_tradition — remainder cult of the herd, pulaaku reserve,
clan yettôdé, and social form as recorded by Lasnet (1900), Crozals (1883),
Reclus (as cited), and Delafosse–Gaden (1913 chronicle for social form).

Hampâté Bâ 1961 (Koumen / Gueno) is not used. English is a Pratibha
rendering (pd_adapted). Original is the French observer sentence.
Key Terms carry Pulaar when the source names them or later PD sources do.

Floor: 28 units. Ten are hero verses (tts_key) for the collection mandala
and Listen bake.
"""
from __future__ import annotations

import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/pulaar_tradition")
SLUG = "pulaar_tradition"
COLL = "Pulaar Tradition"
PROV = (
    "English is a Pratibha rendering (pd_adapted) from Alexandre Lasnet, "
    "*Une mission au Sénégal* (1900); L. de Crozals as quoted there / in the "
    "1883 Peul notices; Élisée Reclus as cited by Lasnet on *boolâtrie*; and "
    "Maurice Delafosse with Henri Gaden, *Chroniques du Foûta sénégalais* "
    "(Siré-Abbâs-Soh, 1913) where the chronicle is used for social form not "
    "for Islamic law. Hampâté Bâ 1961 is not used."
)
NOTE = (
    "Pulaar (Fulfulde) is the language of the Fulɓe (Peul, Foulah, Fulani). "
    "By 1900 most groups known to European observers were Muslim. Pre-Islamic "
    "practice survives in the PD record as remaining pagan pastoral pockets "
    "whose only cult is the herd, and as remnants inside Islam: herd-love, "
    "spirit-warding at birth, green-leaf greeting of the dead, cow bridewealth, "
    "the mother's counsel, clan yettôdé and ancestor interdit. There is no "
    "indigenous written scripture. These layers restore the claim without "
    "colonial contempt. Racial anthropology, costume catalogs, and surgical "
    "detail are refused. Observer slurs (hypocrite, thief) are inverted as "
    "error. The 1961 Koumen cosmology is not used."
)

# Ten hero units — mandala quotes + pre-baked Listen.
HEROES = {1, 2, 3, 7, 8, 9, 10, 11, 14, 17}

THEMES = ["fulbe", "cattle", "pulaaku", "senegambia"]


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


# Each unit: n, title, fr (Original), tr, comm, prac, terms, resonances
UNITS: list[dict] = [
    {
        "n": 1,
        "title": "The Remaining Cult Is the Herd",
        "src": "Crozals, Les Peulhs (1883), citing Bayol; Lasnet 1900, Peuls",
        "fr": (
            "Même aujourd'hui, on trouve dans le Wassallah et le Kankan des Peulhs "
            "nomades qui n'ont qu'un culte, celui de leurs troupeaux, qu'ils font "
            "prospérer le mieux qu'ils peuvent, sans se préoccuper du lendemain."
        ),
        "tr": (
            "Even today, in Wassallah and Kankan, one finds nomad Peuls who have "
            "only one cult: that of their herds. They make the herds prosper as "
            "best they can, without concern for tomorrow."
        ),
        "comm": (
            "The remaining religion is not a missing temple. It is a single cult "
            "with a living object: the herd. Crozals, compiling Park, Mollien, and "
            "Bayol, hunts for idolatry among the Fulɓe and cannot find a shrine. "
            "What he finds instead, among the last openly pagan nomads of the Upper "
            "Niger hinterland, is one relation of care. \"Only one cult\" (n'ont "
            "qu'un culte) is the philosophical sentence. Cows are not carved as "
            "idols. Crozals says in the next breath that image-worship among the "
            "Peuls is an exception of the poorest and most isolated. The center is "
            "not a statue. The center is nagge — the cow as the being you keep alive."
            "\n\n"
            "\"Without concern for tomorrow\" is not improvidence. It is the "
            "pastoral present tense. The herd is fed, watered, moved, and protected "
            "today. Cosmology, if it exists, is not stored in a book; it is stored "
            "in the continued life of the animals. Later Fulɓe literature will name "
            "a creator and an ur-cow. These 1883 pages do not. They record what a "
            "public-domain observer could still see: where Islam has not yet "
            "replaced the old center, the center is cattle."
            "\n\n"
            "The teaching cuts two modern errors. One is that a people without a "
            "temple has no religion. The other is that \"animism\" must mean a "
            "crowded pantheon. Here the world is already full, but the cult is "
            "single. You do not collect gods. You keep the herd alive. That keeping "
            "is the rite. Pulaaku later names the honor-code around this life; the "
            "1883 sentence is older and plainer: one cult, the herd."
        ),
        "prac": (
            "Today, take one living being that depends on you — a person, an animal, "
            "a plant — and make its prospering the whole of the rite. Do not add a "
            "prayer on top. Do not postpone care until a better cosmology arrives. "
            "The cult is the keeping."
        ),
        "terms": kt(
            ("nagge", "Pulaar cow / cattle — the cult-object Crozals could not name; later PD sources use nagge / na'i for the living center the French called troupeaux"),
            ("culte des troupeaux", "cult of the herds — Crozals/Bayol's name for the last pagan liturgical center; cattle-raising as mere economy misses why they reached for a religious word"),
            ("pulaaku", "Fulɓe-ness: reserve, endurance, shame-honor — not in Crozals; the later name for the ethic that keeps the herd-cult from becoming mere stock-breeding"),
            ("sans se préoccuper du lendemain", "without concern for tomorrow — pastoral present, not fecklessness; planning is the next pasture"),
        ),
        "res": res(
            ("Vedic go, cow as wealth-and-rite", "Both locate the sacred in living cattle rather than in a manufactured image.", "Vedic ritual is a named sacrifice with priests and meter; this Pulaar remainder has no temple and no recorded hymn in the PD sources — only the prospering of the herd."),
            ("Serer first-fruits at the baobab (this corpus)", "Both refuse to empty the near world for a distant God.", "Serer practice pours milk and millet at a tree or stone; remaining pagan Fulɓe, in this sentence, have no other cult than the animals themselves."),
        ),
    },
    {
        "n": 2,
        "title": "The Primitive Cult Was Cattle-Worship",
        "src": "Reclus as cited by Lasnet, Une mission au Sénégal (1900), Peuls",
        "fr": (
            "D'après Reclus, leur culte primitif aurait été la boolâtrie et dans "
            "leur mahométisme actuel on peut encore relever beaucoup de coutumes "
            "qui témoignent de leurs anciennes pratiques. La propreté qu'ils "
            "observent dans leurs bouveries a quelque chose de religieux."
        ),
        "tr": (
            "According to Reclus, their primitive cult appears to have been "
            "cattle-worship (boolâtrie), and in their present Islam many customs "
            "can still be read that witness to their ancient practices. The "
            "cleanliness they observe in their cattle-pens has something religious "
            "about it."
        ),
        "comm": (
            "Pre-Islamic Pulaar religion is mostly visible as remainder. Reclus "
            "does not claim to have watched a Fulɓe cow-temple. He infers a prior "
            "cult from what Islam did not erase. Lasnet repeats the sentence almost "
            "verbatim in 1900, which tells you how thin the ethnographic file still "
            "was. There is no Gueno here, no initiation cave, no milk-cosmogony. "
            "There is a European -latry word, boolâtrie, coined from Latin bos on "
            "the model of idolâtrie, and then a concrete rite: the cattle-pen is "
            "kept as if it were a holy place."
            "\n\n"
            "\"Something religious\" (quelque chose de religieux) in the cleanliness "
            "of the bouveries is the philosophical hinge. Hygiene can be merely "
            "practical. Reclus sees that it is not merely practical. The pen is "
            "where the cult-object lives. To keep it clean is to keep the relation "
            "intact. Conversion to Islam changes the Friday and the prayer-direction; "
            "it does not empty the pen of its older gravity. \"Primitive\" in 1887 "
            "French is an evolutionary ranking. The usable sense is prior: the "
            "cattle-relation is older than the mosque, and still standing."
            "\n\n"
            "Existentially the teaching is about what conversion does not convert. "
            "A new confession can rename the sky and still leave the daily shrine "
            "standing. If you want the pre-Islamic Pulaar world, do not start with "
            "a reconstructed myth. Start with the place that is still treated as "
            "if it were sacred: the enclosure of the herd."
        ),
        "prac": (
            "Clean one place that keeps what you live from — kitchen, stall, desk, "
            "threshold — as if the cleanliness were already a rite. Do not add "
            "incense. Notice whether the care feels merely practical or whether it "
            "has something religious in it. That notice is the remnant."
        ),
        "terms": kt(
            ("boolâtrie", "Reclus's coinage from Latin bos, ox, on the model of idolâtrie — a scholar's -latry, not a Pulaar autonym; idolatry of cows overstates images; the next clause (clean pens, surviving customs) is the actual content"),
            ("bouveries", "cattle-pens, byres — the built form of the cult; barn is too agricultural-European; this is the enclosure that still receives guests as a mark of respect"),
            ("nagge", "the cow as the being the pen is kept for — Pulaar does not need boolâtrie; it needs the clean enclosure of nagge"),
            ("culte primitif", "primitive cult — chronological claim: Islam is later; cattle-relation is earlier; primitive as ranking is refused, prior is kept"),
        ),
        "res": res(
            ("Hebrew mishkan, care of the holy enclosure", "Both treat the kept enclosure as a religious fact, not a shed.", "The tabernacle is portable because God dwells there; the Fulɓe pen is holy because the herd lives there."),
            ("Shinto shrine sweeping", "Both locate reverence in cleanliness before any spoken doctrine.", "Shinto cleanliness has kami and a shrine lineage; Reclus has no named spirit of the pen — only something religious."),
        ),
    },
    {
        "n": 3,
        "title": "The Herd Decides the Path",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Ce sont les besoins de leurs troupeaux qui déterminent leurs "
            "déplacements; quand les pâturages d'une région sont épuisés, ils vont "
            "plus loin et, si c'est nécessaire, changent plusieurs fois dans la "
            "même année."
        ),
        "tr": (
            "It is the needs of their herds that determine their displacements. "
            "When the pastures of a region are exhausted, they go farther, and if "
            "necessary they change several times in the same year."
        ),
        "comm": (
            "The world is not a map on which cattle are cargo. The world is a "
            "network of pasture, water, and milk, and human motion is a function "
            "of that network. \"The needs of their herds determine their "
            "displacements\" is a metaphysics of path. You do not choose a "
            "destination and then bring the cows. The cows' thirst and hunger "
            "choose. Later Pulaar names the move egga, transhumance, and the camp "
            "wuro; Lasnet does not. He records the structure: the herd's need is "
            "the law of motion."
            "\n\n"
            "Changing several times in one year is not restlessness. It is "
            "fidelity to a living body that cannot eat last season's grass. A "
            "sedentary spirituality will hear this as lack of place. The pastoral "
            "claim is the opposite: place is wherever the herd can still live. "
            "When the pasture is exhausted, staying is the betrayal. The path is "
            "not a pilgrimage toward a shrine. The path is the next water."
            "\n\n"
            "Existentially the teaching is against a spirituality that leaves the "
            "body of the world unmanaged. If your path is only inward, the riverbank "
            "stays a cliff and the milk dries. Here the path is a decision the "
            "living make for you, and you honor it by moving. The later units on "
            "the ramp, the dummy calf, and affection greater than children are "
            "the same ontology told as single acts. This unit is the law those "
            "acts obey: the herd decides."
        ),
        "prac": (
            "Before you move today — house, job, opinion — ask what living need is "
            "actually choosing the displacement. Let that need, not the map, decide "
            "the next hour. If nothing living is choosing, you are moving as cargo, "
            "not as a herder."
        ),
        "terms": kt(
            ("besoins de leurs troupeaux", "needs of their herds — the law of motion; economic necessity is true and too thin; Lasnet places this sentence inside mœurs, not inside a chapter on markets"),
            ("egga", "later Pulaar for transhumance — not in Lasnet; the structure he records is the herd's need as path"),
            ("wuro", "camp, the temporary human place that follows nagge rather than founding a town"),
            ("déplacements", "displacements — not travel-as-leisure; the group is a function of pasture"),
        ),
        "res": res(
            ("Īśāvāsya Upaniṣad 1, īśā vāsyam idam sarvam", "Both refuse to treat the living world as dead property you arrange at will.", "The Upaniṣad covers the world with the Lord; this passage covers the path with the herd's need."),
            ("Zhuāngzǐ, wandering", "Both prefer a mobile life that does not stockpile a single address as the real.", "Zhuāngzǐ's wandering is a freedom from fixed use; Fulɓe mobility in this source is bound to pasture and water."),
        ),
    },
    {
        "n": 4,
        "title": "Pagan Pockets Were Still Attested",
        "src": "Crozals, Les Peulhs (1883), citing Park and Mollien; Lasnet 1900",
        "fr": (
            "La majorité de la race est convertie à l'islamisme, cependant beaucoup "
            "d'agglomérations du Sénégal et de la Haute-Gambie sont encore "
            "fétichistes, tièdos; leur nombre diminue chaque jour avec les progrès "
            "constants de l'islamisme. À la fin du XVIIIe siècle la conversion des "
            "différents groupes Peulhs n'est pas complète. Il arrive que dans un "
            "même État, à côté des Peulhs musulmans formant la masse, une minorité "
            "païenne s'est maintenue."
        ),
        "tr": (
            "The majority of the people is converted to Islam; nevertheless many "
            "settlements of Senegal and the Upper Gambia are still fetishist, "
            "tiedo; their number diminishes each day with the constant progress of "
            "Islam. At the end of the eighteenth century the conversion of the "
            "different Peul groups is not complete. In one and the same state, "
            "beside the Muslim Peuls who form the mass, a pagan minority has held on."
        ),
        "comm": (
            "Pre-Islamic Pulaar practice is not a hypothesis projected backward "
            "from a twentieth-century myth. It is a demographic fact in the travel "
            "literature of 1799–1820, still summarized in 1883 and 1900. Conversion "
            "is incomplete. In one state two Fulɓe populations coexist. Lasnet's "
            "word fétichistes is the colonial file-name; tiedo (tièdo) is the "
            "Senegambian word for those who have not taken Islam. Park's "
            "\"superstitions\" is contempt and should not be adopted as teaching. "
            "What it marks is attachment to an older cult that Islam had not "
            "replaced."
            "\n\n"
            "Crozals's larger book is about Muslim Fulɓe empire. This paragraph is "
            "his admission that the empire did not cover the whole people. The "
            "Jolof Peuls are reported as entirely pagan around 1800. Pagan villages "
            "stand within two days of Timbo, the theocratic capital of Futa Jallon. "
            "The remainder is the warrant for every other unit in this collection: "
            "cattle-cult, spirit-warding, green-leaf greeting, clan interdit. They "
            "are not folklore inside Islam only. They are what the last pagans were "
            "still doing, and what Muslims still do without calling it a second "
            "religion."
            "\n\n"
            "Existentially the teaching is against the myth of total conversion. "
            "A tradition is allowed to have a remainder. The remainder is where the "
            "older ontology is still practiced rather than remembered. Do not "
            "despise your own unconverted remainder as leftover superstition. It "
            "is often the only honest cult you still have."
        ),
        "prac": (
            "Name one older practice in your own life that a later conversion — "
            "religious, professional, or intellectual — did not actually erase. "
            "Keep it for one day as the remainder that tells the truth about what "
            "you still serve."
        ),
        "terms": kt(
            ("tièdo / tiedo", "Senegambian name for those who have not taken Islam — Lasnet's fétichistes is the colonial file-word; tiedo is the local demographic"),
            ("minorité païenne", "pagan minority — Crozals's name for Fulɓe who have not taken Islam; Delafosse's later animist is cleaner; fetishist is Lasnet's worse one"),
            ("Fouta-Toro / Fouta-Djallon", "the Muslim imamates; the map of remainder is not far from the mosque — the old cult still has a village"),
            ("anciennes superstitions", "Park via Crozals: ancient superstitions — the older cult under a traveler's insult; the usable content is ancient and attached, not superstition"),
        ),
        "res": res(
            ("Late antique pagans beside Christian empire", "Both show conversion as a patchwork inside one people, not a clean replacement.", "Mediterranean paganism left temples and texts; Pulaar paganism in these sources leaves herds, villages, and a named remainder, not a written liturgy."),
            ("Serer resistance to conversion in Lasnet (this corpus)", "Both Senegambian cases show Islam as incomplete overlay.", "Serer sources in this corpus still describe a living public religion; Fulɓe paganism is already a minority report beside the imamate."),
        ),
    },
    {
        "n": 5,
        "title": "Bridewealth Is Always Named in Cows",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mariage",
        "fr": (
            "La dot est proportionnelle à la fortune du mari et l'honore d'autant "
            "qu'elle est plus élevée : pour une jeune fille, elle peut aller "
            "jusqu'à quinze vaches, à dix pour une femme déjà mariée; cette dot "
            "est toujours exprimée en vaches."
        ),
        "tr": (
            "The bridewealth is proportional to the husband's fortune and honors "
            "him the more as it is higher: for a young woman it may go as far as "
            "fifteen cows, ten for a woman already married. This bridewealth is "
            "always expressed in cows."
        ),
        "comm": (
            "Cattle are not only food and motion; they are the language of honor "
            "in alliance. Lasnet is describing marriage regulated by the laws of "
            "the Qur'an, with a marabout reciting prayers. Inside that Islamic "
            "frame the dowry-word is still bovine. You may pay in money, sheep, or "
            "cloth, but you name the gift in cows. The pre-Islamic measure survives "
            "as the unit of speech. That is how a cult remains after the temple is "
            "gone: it becomes the currency of respect."
            "\n\n"
            "\"Honors him the more as it is higher\" is a ranking that can become "
            "vanity. The philosophical core is prior to the vanity. A people whose "
            "primitive cult was the herd will measure a binding of families in the "
            "same beings that determine the path. Fifteen cows is not a price-tag "
            "on a woman in the market sense Lasnet's achetée wants. It is the herd "
            "acknowledging a new household. Later Pulaar names bridewealth sadaaki "
            "(from Arabic ṣadāq) when the frame is Islamic; Lasnet's ethnographic "
            "fact is that the unit of honor remains nagge even when payment is "
            "substituted."
            "\n\n"
            "Existentially the teaching is about what you still count when you "
            "think you have changed religions. If your sacred is cattle, your "
            "contracts will speak cow even on a mosque day. Ask what unit you "
            "always express things in — money, credentials, time, attention. That "
            "unit is your remaining cult."
        ),
        "prac": (
            "Take one obligation you owe a person — thanks, help, repair. Name it "
            "in the unit that is actually sacred to you, not in the unit that is "
            "convenient. Then give a piece of that, not a substitute that keeps "
            "the name empty."
        ),
        "terms": kt(
            ("dot ... toujours exprimée en vaches", "bridewealth always expressed in cows — the cow as unit of speech, even when payment is substituted; European dowry (goods the bride brings) is the wrong direction"),
            ("nagge", "cow, specifically, not generic livestock — milk-life, not meat-wealth only; substituting sheep or cloth is allowed; substituting the name is not"),
            ("sadaaki", "later Pulaar bridewealth (from Arabic ṣadāq) — Islamic legal name; Lasnet's fact is that the measure remains bovine"),
            ("l'honore", "honors him — bridewealth as honor, not only transfer; pulaaku later names honor-shame; Lasnet has the structure without the word"),
        ),
        "res": res(
            ("Vedic bride-gift and cattle as dakṣiṇā", "Both make cattle the measurable form of a sacred bond.", "Vedic cattle-gift is priestly and hymnic; Fulɓe cattle-gift here is affinal and remains so under Qur'anic law."),
            ("Aristotle on timē (honor)", "Both treat honor as something that must be publicly measured.", "Greek honor is civic and martial; this honor is pastoral and nuptial."),
        ),
    },
    {
        "n": 6,
        "title": "Ward the Spirits Until the Seventh Day",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Accouchement",
        "fr": (
            "Comme chez les autres musulmans le baptême a lieu le septième jour "
            "après la naissance et la mère porte jusque-là un poignard destiné à "
            "écarter les mauvais esprits."
        ),
        "tr": (
            "As among other Muslims, the naming takes place on the seventh day "
            "after birth, and until then the mother wears a dagger meant to keep "
            "off the evil spirits."
        ),
        "comm": (
            "The week between birth and name is a spiritually open interval. "
            "Islam's seventh-day naming did not abolish the older danger; it only "
            "scheduled its close. Lasnet calls the ceremony a baptism because he "
            "is writing for French readers. It is the Muslim name-giving — later "
            "Pulaar simmol / innde. Beside it, not instead of it, the mother is "
            "armed. A dagger is a poor tool against a spirit if you think in "
            "mosque categories. It is a precise tool if you think, as the remnant "
            "does, that the unnamed child and the newly delivered mother are "
            "exposed to persons who are not flesh."
            "\n\n"
            "This is the same structure Delafosse names for West African animism "
            "generally: the near world is populated by free souls that can act, "
            "and the living take measures. The measure here is metal worn on the "
            "body. The seventh day does not only confer a name; it ends a vigil. "
            "Pre-Islamic Pulaar practice, in the only form this source can show it "
            "at the cradle, is apotropaic: keep the spirits off until the child is "
            "spoken into the human group."
            "\n\n"
            "Existentially the teaching is that beginnings are not safe by default. "
            "A birth is not yet a belonging. Belonging waits on a rite, and until "
            "the rite the world is leaky. You do not have to accept Lasnet's dagger "
            "as your object. You do have to notice which of your own beginnings "
            "you treat as spiritually unguarded, as if a new life, a new love, or "
            "a new work needed no vigil."
        ),
        "prac": (
            "If something in your life is newly born — a project, a recovery, a "
            "household — keep a seven-day vigil. Do not announce it as finished on "
            "day one. Each day, perform one small warding act: a boundary, a "
            "silence, a refusal of premature display. On the seventh day, give it "
            "a name out loud."
        ),
        "terms": kt(
            ("mauvais esprits", "evil spirits — Lasnet's French for harmful non-human persons around birth; not the Islamic jinn as a learned category, and not a psychology of bad mood; a populated interval between birth and name"),
            ("poignard", "dagger worn by the mother until day seven — apotropaic metal; weapon as crime-tool is the wrong picture; this is a ward, like an amulet that happens to be a blade"),
            ("simmol / innde", "later Pulaar naming — Lasnet's baptême is the Islamic seventh-day name-giving; the remnant is the need for a ward until the naming"),
            ("septième jour", "seventh-day naming, Islamic in Lasnet's framing — the scheduled end of exposure"),
        ),
        "res": res(
            ("Greek amphidromia and Roman name-day", "Both treat the days after birth as incomplete belonging.", "Classical rites walk the child or purify the house; this remnant arms the mother."),
            ("Serer mammam (this corpus)", "Both populate the near world with addressable, dangerous powers.", "Serer address the spirits with libation; this Fulɓe remnant drives them off with a blade until the name is given."),
        ),
    },
    {
        "n": 7,
        "title": "Honor Is Impassibility",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Circoncision",
        "fr": (
            "Pendant toute l'opération les jeunes gens doivent conserver "
            "l'impassibilité la plus grande; il y aurait déshonneur à se plaindre. "
            "Le soir, ils écoutent les légendes et les fables de leurs gardiens."
        ),
        "tr": (
            "Through the whole operation the young men must keep the greatest "
            "impassibility; it would be dishonor to complain. In the evening they "
            "listen to the legends and fables of their guardians."
        ),
        "comm": (
            "Pain is not the teaching. The teaching is that a public ordeal is the "
            "place where honor is either kept or lost, and that the keeping looks "
            "like stillness. Dishonor is not the cut. Dishonor is the complaint. "
            "Lasnet's chapter is a colonial medical description of circumcision; "
            "this unit refuses the surgical content and keeps the philosophical "
            "rule that the description accidentally recorded. Threshold, not anatomy."
            "\n\n"
            "This is as close as the PD ethnography comes to pulaaku without naming "
            "it. Reserve, self-mastery, the refusal to make inner weather into "
            "noise: Lasnet sees it on the initiation ground and also, elsewhere, in "
            "the continual gravity of the adult Peul who rarely dances. The evening "
            "of legends is the other half of initiation. Impassibility without "
            "transmission would be only toughness. The guardians tell the stories "
            "that make the boys into a people. Pre-Islamic and Islamic Fulɓe both "
            "circumcise; what the remnant shares with the older world is not the "
            "knife but the school: seclusion, elder speech, a body that must not "
            "betray itself."
            "\n\n"
            "Existentially the teaching is not seek pain. It is: when you are "
            "already in a necessary difficulty, do not add the second wound of "
            "display. Keep the face. Then, in the evening, listen. Initiation that "
            "is only endurance is brutality. Initiation that is endurance plus "
            "story is how a tradition reproduces."
        ),
        "prac": (
            "Choose one necessary difficulty you are already in. For one day, do "
            "not advertise it and do not complain of it. In the evening, listen to "
            "someone older tell a story — live, if you can — as if endurance "
            "without transmission were incomplete."
        ),
        "terms": kt(
            ("pulaaku", "Fulɓe-ness: reserve, endurance, shame-honor — Lasnet does not use the word; he records the visible rule: impassibility, and the seclusion-school of legends"),
            ("impassibilité", "impassibility, the face that does not leak pain — honor as composure; stoicism is a fair gloss if you remember it is public and communal here, not a private Roman notebook"),
            ("déshonneur", "dishonor in complaining — shame as social ontology; later semteende (reserve, shame); Lasnet has the sanction without the Pulaar word"),
            ("gardiens", "elder guardians of the seclusion-house — transmitters, not only nurses of wounds; the office is to speak the people into the next generation"),
        ),
        "res": res(
            ("Stoic apatheia", "Both treat the uncomplaining face as a form of freedom.", "Stoic impassibility is an inward judgment about what is up to us; Fulɓe impassibility here is honor before witnesses."),
            ("Kashmir Śaiva vīra (heroic) posture", "Both demand a steadiness that does not flinch.", "The tantric hero's steadiness is in consciousness amid appearance; this steadiness is in a social body that must not shame the group."),
        ),
    },
    {
        "n": 8,
        "title": "Greet the Dead with Green Leaves",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Funérailles",
        "fr": (
            "Chaque fois que des Peuls en voyage rencontrent une tombe ou un "
            "cimetière, ils jettent en passant une poignée d'herbes ou de feuilles "
            "vertes, sorte de salut qu'ils adressent aux trépassés."
        ),
        "tr": (
            "Every time Peuls on a journey meet a tomb or a cemetery, they throw "
            "as they pass a handful of grass or green leaves, a kind of greeting "
            "they address to those who have gone over."
        ),
        "comm": (
            "The dead remain addressable, and the correct address from a pastoral "
            "people is green plant-matter thrown in passing. Lasnet wants this to "
            "be generic Islam: respect, tombs, the eastward face of the grave. The "
            "specific gesture is not generic. A handful of herbes or feuilles "
            "vertes is what you would give a living herd. The greeting to the dead "
            "is forage. The ancestor is still, in the remnant logic, a being who "
            "can be met on the road and who understands the gift of grass."
            "\n\n"
            "\"In passing\" (en passant) matters. This is not a festival of the "
            "dead and not a sacrifice that stops the caravan. Mobility continues; "
            "relation continues inside mobility. Nomad respect cannot always be a "
            "vigil at a fixed grave. It can be a toss of green as you go by. The "
            "dead do not require you to become sedentary. They require that you "
            "not pass them as if they were stones."
            "\n\n"
            "Existentially the teaching is a correction to both amnesia and "
            "ostentation. You do not have to build a shrine at every loss. You do "
            "have to refuse to walk past the dead as scenery. Give them something "
            "living and green, and keep moving. That is pastoral piety. The next "
            "unit on sacrilege is the negative of this greeting: what you must not "
            "do to a tomb is the other face of the same address."
        ),
        "prac": (
            "On one walk today, when you pass a cemetery, a roadside memorial, or "
            "even a tree that marks a death you know, do not pass as if it were "
            "scenery. Stop long enough to set down something green — a leaf, a "
            "blade of grass. Greet, do not speechify, and go on."
        ),
        "terms": kt(
            ("poignée d'herbes ou de feuilles vertes", "handful of grass or green leaves — forage as greeting; flowers on a grave is the nearest European picture and still too garden; this is pasture thrown to the dead"),
            ("salut", "greeting, salute — the dead are met as persons on the road; offering is true; greeting is more exact: you acknowledge, you do not bargain"),
            ("trépassés", "those who have passed over — the dead as having gone a way, not as having become nothing; the same root of passage as the travelers who greet them"),
            ("en voyage", "on a journey — the rite belongs to mobility; a sedentary memorial mass is another religion's tempo"),
        ),
        "res": res(
            ("Serer speaking into the ear of the dead (this corpus)", "Both refuse to treat the corpse-side of the world as mute.", "Serer speech is intimate and at the body; Fulɓe greeting is a toss of green from the road."),
            ("Homeric choai, drink-offerings to the dead", "Both give the dead a portion of the living world's goods.", "Greek libation is wine and blood at a pit; this portion is pasture."),
        ),
    },
    {
        "n": 9,
        "title": "Consult the Mother Before a Great Act",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mariage / mœurs",
        "fr": (
            "La femme peule est beaucoup plus considérée que chez les autres "
            "peuplades du Sénégal, elle exerce souvent un grand ascendant sur son "
            "mari et, malgré la latitude que donne à celui-ci le Coran, il est rare "
            "qu'elle laisse pénétrer une seconde femme dans sa case; elle est "
            "respectée et très écoutée de ses enfants, un Peul n'accomplit jamais "
            "une action importante sans consulter sa mère."
        ),
        "tr": (
            "The Peul woman is held in much higher regard than among the other "
            "peoples of Senegal. She often exerts a great ascendancy over her "
            "husband, and despite the latitude the Qur'an gives him it is rare that "
            "she lets a second wife into her house. She is respected and closely "
            "listened to by her children. A Peul never accomplishes an important "
            "action without consulting his mother."
        ),
        "comm": (
            "This is a decision-procedure, not a compliment in a colonial ranking "
            "of \"the status of women.\" Lasnet is comparing ethnic files. Strip "
            "the ranking. What remains is a rule of counsel: before a great act, "
            "ask the mother. Islam's legal polygamy is in the same paragraph and "
            "is described as practically checked by the wife. The deeper remnant "
            "is maternal consultation as a condition of action. Authority is not "
            "only the almamy, the marabout, or the ardo. Authority is the woman "
            "from whom one was born, still speaking."
            "\n\n"
            "In a cattle-people this is not a sentimental exception to patriarchy; "
            "it is how a mobile household keeps a memory that is not written. The "
            "mother is the one who has seen the herd, the marriages, the failures. "
            "To act without her is to act without the household's archive. "
            "Pre-Islamic West African social philosophy, as Delafosse will say of "
            "clans generally, runs through ancestors. This sentence makes the "
            "living mother the nearest ancestor who can still answer."
            "\n\n"
            "Existentially the teaching is against heroic solitude. An important "
            "action that cannot survive being told to one's mother is probably "
            "vanity. Consultation is not permission-as-infantilism. It is the test "
            "that the act belongs to a line and not only to a mood."
        ),
        "prac": (
            "Before one important action this week, consult a living elder woman "
            "in your line — mother, aunt, teacher — and tell her the act in plain "
            "speech. Do not perform the consultation as theater. Change the act if "
            "her hearing finds it thinner than you thought."
        ),
        "terms": kt(
            ("consulter sa mère", "consult one's mother — the condition of a great act; ask mom as joke misses that Lasnet says never (jamais) and important action"),
            ("ardo", "political-military chief — one of the public authorities this rule still outranks for a founding act; the mother is nearer than the office"),
            ("ascendant", "the wife's ascendancy over the husband — practical authority inside a Qur'anic frame that legally favors the man; the house is not the Qur'an's diagram"),
            ("action importante", "important action — the threshold at which counsel becomes mandatory; daily acts may be free; founding acts are not"),
        ),
        "res": res(
            ("Confucian filial consultation", "Both make the parent a living source of right action.", "Confucian counsel is often paternal and ritualized as xiao; this sentence specifies the mother."),
            ("Delphic counsel before a great act", "Both refuse to let a founding decision be merely private.", "Delphi is an oracle of the god; here the oracle is the mother."),
        ),
    },
    {
        "n": 10,
        "title": "The Clan Honor-Name and the Ancestor's Interdit",
        "src": "Delafosse, Les civilisations négro-africaines (1925); social form also in Delafosse–Gaden, Chroniques du Foûta sénégalais (1913)",
        "fr": (
            "De l'accord unanime des indigènes interrogés à cet égard, il résulte "
            "que c'est l'ancêtre du clan qui aurait institué ce nom et cet interdit "
            "et aurait solennellement transmis l'un et l'autre à tous ses "
            "descendants à venir. Ailleurs, par exemple chez les Peuls, on "
            "opposera les Dialloubé aux Hanhanbé, c'est-à-dire les gens du clan "
            "Diallo aux gens du clan Kan. Les diverses langues en usage dans "
            "l'Afrique noire désignent en général le nom de clan par une expression "
            "que l'on pourrait traduire par « terme honorifique » ou « titre de "
            "noblesse », comme diamou (ce qui grandit) en mandingue ou yettôdé (ce "
            "qui honore) en peul. L'interdit a été institué par l'ancêtre en même "
            "temps que le nom de clan."
        ),
        "tr": (
            "By the unanimous agreement of those questioned on this point, it is "
            "the ancestor of the clan who instituted this name and this prohibition "
            "and solemnly transmitted both to all descendants to come. Among the "
            "Peuls, for example, one opposes the Dialloubé to the Hanhanbé — the "
            "people of clan Diallo to the people of clan Kan. The languages of "
            "Black Africa generally call the clan name by an expression one might "
            "translate as \"honorific term\" or \"title of nobility,\" such as "
            "diamou (\"that which enlarges\") in Manding or yettôdé (\"that which "
            "honors\") in Peul. The prohibition was instituted by the ancestor at "
            "the same time as the clan name."
        ),
        "comm": (
            "Identity is a double gift from an ancestor: a name that honors, and a "
            "prohibition that binds. Delafosse is writing a pan-West-African "
            "theory; he pauses on the Fulɓe because they illustrate the structure "
            "without always wearing the clan name as a surname in daily address. "
            "You still say Dialloubé against Hanhanbé when you need to name a "
            "people. Yettôdé means \"that which honors.\" To call someone by the "
            "clan name is to say they have known ancestors. The interdit is not a "
            "random food taboo. It is usually the species that saved the ancestor, "
            "or the object bound up with the founding escape. You do not eat or "
            "harm what saved the one who made you a people."
            "\n\n"
            "This is the pre-Islamic Fulɓe social cosmology that the cattle-cult "
            "units do not yet reach. Herds explain motion, milk, and bridewealth. "
            "Clan interdit explains why the human group is not just a herd of "
            "humans. An ancestor acted, was saved, named the name, and laid a "
            "forever-avoidance on the descendants. Islam can add a silsila of "
            "marabouts; it does not have to erase Diallo and Kan. The 1913 Futa "
            "chronicle is used here only for this social form, not for Islamic "
            "law. The remainder is kinship as liturgy."
            "\n\n"
            "Existentially the teaching is that you are not a self-invented "
            "individual with preferences. You are a descendant under a name and "
            "under a refusal. The refusal is the more philosophical half. Anyone "
            "can wear a proud name. The interdit is the name's cost: there is a "
            "living kind you will not destroy, because your ancestor's life came "
            "through it."
        ),
        "prac": (
            "Name one prohibition you actually live by that you did not invent — "
            "a food you will not eat, a cruelty you will not do, a place you will "
            "not spoil — because someone before you bound you. Keep it today on "
            "purpose, as if the ancestor were still the legislator. If you cannot "
            "name any such prohibition, you are living as if you had no yettôdé."
        ),
        "terms": kt(
            ("yettôdé", "Pulaar that which honors — the clan honor-name; not a nickname and not a European surname; to address someone by it is homage, affirming that the person has known ancestors"),
            ("interdit", "ancestor-instituted avoidance (animal, plant, object) — often the helper-species of the founding story; taboo is usable if you keep the ancestor as legislator; totem is what Delafosse warns against"),
            ("Dialloubé / Hanhanbé", "people of Diallo vs people of Kan — Fulɓe clan as collective, even when the name is not stacked on the personal name in daily speech"),
            ("ancêtre du clan", "the clan ancestor who instituted name and prohibition together — the legislator of identity; without this figure the honor-name is just branding"),
        ),
        "res": res(
            ("Israelite tribes and food laws", "Both bind a people by ancestor-given name plus prohibition.", "Torah prohibitions are theistic and written; clan interdit is ancestral and oral, often tied to a rescue-story of a particular species."),
            ("Confucian surname and ancestral hall", "Both treat the name as honor that must be lived up to.", "The Chinese name is patrilineal ritual with tablets; yettôdé is a spoken honorific whose partner-institution is an avoidance, not a tablet."),
        ),
    },
    {
        "n": 11,
        "title": "Affection for the Herd Greater Than for Children",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Sans cesse au milieu de leurs troupeaux, ils les connaissent "
            "admirablement et s'en font aimer, d'ailleurs ils ont pour eux une "
            "véritable affection, plus grande souvent que pour leurs propres enfants."
        ),
        "tr": (
            "Always in the midst of their herds, they know them admirably and make "
            "themselves loved by them; they have for the animals a true affection, "
            "often greater than for their own children."
        ),
        "comm": (
            "Care is the rite. Lasnet wants a gasp: these people love cows more "
            "than children. The colonial sentence is sensational. The philosophical "
            "reading is colder. In a pastoral ontology the herd is the continuing "
            "body of the group. Children matter; the herd is how children eat, how "
            "bridewealth is named, how the path is chosen. Affection greater than "
            "for children is not a ranking of persons as disposable. It is a "
            "ranking of what must not be allowed to die if the people are to "
            "remain a people. The scandal is the observer's. The teaching is that "
            "love can be liturgical without being cute."
            "\n\n"
            "\"True affection\" (véritable affection) and \"make themselves loved\" "
            "(s'en font aimer) are two directions of the same relation. Knowledge "
            "is not inventory. They know the animals admirably because they live "
            "in the midst of them, and the animals answer. Nagge is not stock. "
            "Nagge is a being you can be loved by. That is why later sources can "
            "call the old cult boolâtrie without ever finding a cow-idol: the cult "
            "is this two-way care."
            "\n\n"
            "Existentially the teaching refuses a spirituality that reserves love "
            "for the human face and treats every other life as instrument. If the "
            "being that feeds you cannot be loved, your cult is already empty. "
            "You do not have to outrank your children. You do have to notice which "
            "non-human life you treat as if it could not love you back, and whether "
            "that refusal is wisdom or a thinned world."
        ),
        "prac": (
            "Give one living non-human being — animal, tree, patch of ground — a "
            "full act of care today, done as if it could love you back. Do not "
            "narrate it as metaphor. Do the care. That is the rite."
        ),
        "terms": kt(
            ("affection véritable", "true affection — Lasnet's word for a love that outranks even children in his ranking; do not moralize it as cruelty to children; read it as the herd being the group's ongoing life"),
            ("s'en font aimer", "make themselves loved by the herd — knowledge as two-way; the animals are not mute property"),
            ("nagge", "the cow as the being this affection is for — not a pet and not a unit of meat"),
            ("pulaaku", "the honor-code that will later name reserve around this love so it does not become display"),
        ),
        "res": res(
            ("Christian Good Shepherd", "Both make care of the flock the image of right relation.", "The Gospel metaphor points past sheep to persons; Lasnet's Fulɓe point at the cattle as the actual center of care."),
            ("Zhuāngzǐ's butcher Ding", "Both locate mastery in knowing a living body's grain so well that relation becomes easy.", "Ding's ox is already for the blade; the Fulɓe ox is for continued life, milk, and motion."),
        ),
    },
    {
        "n": 12,
        "title": "Cut a Ramp So the Cattle Can Drink",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Pour les faire abreuver ils ne se contentent pas de les conduire vers "
            "les bords les moins escarpés, mais ils leur font une route en taillant "
            "un plan incliné de façon à faciliter l'accès de la rivière."
        ),
        "tr": (
            "To water them they do not merely lead them to the least steep banks; "
            "they cut them a road, carving a ramp so the river can be reached."
        ),
        "comm": (
            "Affection that will not cut the bank is sentiment. The Fulɓe rite in "
            "this sentence is earthwork. They do not wait for a gentle slope to "
            "appear. They make a road (ils leur font une route) by carving an "
            "inclined plane so the cattle can drink. The river is there. Access is "
            "not. Care is the difference between a cliff and a path. This is "
            "liturgy in soil: the sacred-economic body of the herd must reach water, "
            "and the human task is to remove the unnecessary steepness."
            "\n\n"
            "\"They do not content themselves\" (ils ne se contentent pas) is the "
            "moral verb. The easy piety would be to lead the animals to the least "
            "bad bank and call it enough. The remnant cult does more. It alters "
            "the land so the dependent life can drink without injury. Engineering "
            "is the wrong European word if it means a project detached from love. "
            "This is how affection looks when it has tools."
            "\n\n"
            "Existentially the teaching is against a care that stays in feeling. "
            "If a being you claim to serve cannot reach what it needs, your "
            "affection is a report, not a rite. Cut the ramp. The path-unit said "
            "the herd decides the displacement. This unit says you still have to "
            "make the last yards possible with your hands."
        ),
        "prac": (
            "Remove one unnecessary steepness between a dependent life and water, "
            "food, rest, or you. A form, a step, a locked door, a delayed reply. "
            "Cut one ramp today. Do not announce it as kindness. Let the easier "
            "access be the whole of the act."
        ),
        "terms": kt(
            ("plan incliné", "the carved ramp to water — a made path for the sacred-economic body of the herd; engineering misses that this is how affection looks when it has tools"),
            ("abreuver", "to water the herd — the verb of the rite; not a chore appended to religion; the religion is this verb"),
            ("faire une route", "to make them a road — the cattle are given a way, not merely driven to a brink"),
            ("nagge", "the drinkers for whom the bank is cut — the cult-object as a body that thirsts"),
        ),
        "res": res(
            ("Isaiah 40:3–4, make straight a highway", "Both treat path-making as a religious act, not mere travel logistics.", "Isaiah prepares a road for God; the Fulɓe cut a road for the herd — the cult-object is the thirsty animal, not the arriving Lord."),
            ("Daoist wuwei and the low water", "Both honor water as the place life must reach.", "Wuwei prefers not to force the bank; this remnant forces the bank so the cattle are not forced."),
        ),
    },
    {
        "n": 13,
        "title": "The Dummy Calf-Skin Keeps the Milk",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Quand une vache a perdu son veau, pour que son lait ne tarisse point "
            "ils font un mannequin avec la peau de l'animal et n'hésitent pas à "
            "la téter eux-mêmes."
        ),
        "tr": (
            "When a cow has lost her calf, so that her milk will not dry they make "
            "a dummy from the animal's skin and do not hesitate to suckle her "
            "themselves."
        ),
        "comm": (
            "Death is not allowed to stop the relation. The calf has died. The "
            "cow's body is about to close. The remnant cult answers with a device: "
            "a mannequin of the calf's own skin, and if needed the herder's mouth "
            "where the calf's mouth was. The dummy is not a fetish that one "
            "worships. It is a stand-in that keeps milk, which is life, from "
            "drying because a particular body has gone. Pre-Islamic Pulaar practice, "
            "as this passage can recover it, is full of such devices. They look "
            "like husbandry. They are husbandry as cult."
            "\n\n"
            "\"So that her milk will not dry\" (pour que son lait ne tarisse point) "
            "is the purpose-clause that makes the act philosophical. The aim is "
            "not to deny death and not to harvest a resource from a grieving "
            "animal as if grief were nothing. The aim is continuity of the gift. "
            "Milk is how the herd feeds the camp. A dried cow is a closed shrine. "
            "The skin-dummy is an anti-drying rite: keep the cow in relation after "
            "the calf is gone."
            "\n\n"
            "Existentially the teaching is against a piety that abandons a relation "
            "when its first form dies. When the obvious recipient is gone, do you "
            "let the gift dry, or do you make a stand-in honest enough that the "
            "source can still give? The dummy is strange. The drying is worse. "
            "Lasnet's \"they do not hesitate\" is his shock. The herder's lack of "
            "hesitation is the ethic: dignity is keeping the milk, not keeping "
            "your mouth unused."
        ),
        "prac": (
            "Where a gift in your life is drying because its first recipient is "
            "gone — a skill no one asks for, a care with no obvious home — make "
            "one honest stand-in today so the gift can still move. Do not wait "
            "for the original form to return."
        ),
        "terms": kt(
            ("mannequin", "calf-skin dummy to keep milk flowing — a stand-in that preserves relation after death; not an idol; an anti-drying rite"),
            ("lait", "milk — life as a flow that can tarry or dry; the remnant cult is a technology against drying"),
            ("tarisse", "dry up — the danger the rite answers; a closed udder is a closed shrine"),
            ("nagge", "the cow whose gift must not stop — the cult-object as a body that can refuse if the relation is broken"),
        ),
        "res": res(
            ("Egyptian opening-of-the-mouth for the dead", "Both use a device so a life-function does not stop at a death.", "The Egyptian rite opens the dead to eat in the next world; this Fulɓe rite keeps the living cow giving in this one."),
            ("Serer first-fruits of milk (this corpus)", "Both treat milk as a religious good, not only a food.", "Serer milk is poured to spirits; this milk is kept flowing by a skin-stand-in after a calf's death."),
        ),
    },
    {
        "n": 14,
        "title": "Never Sell Calves or Cows, Only Oxen",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Commerce",
        "fr": (
            "Dans leurs marchés ils ne se défont que des bœufs, jamais des veaux "
            "ni des vaches, autant d'ailleurs par affection que par intérêt, car "
            "ils sont très attachés à leurs animaux."
        ),
        "tr": (
            "In their markets they part only with oxen, never with calves or cows, "
            "as much from affection as from interest, for they are deeply attached "
            "to their animals."
        ),
        "comm": (
            "The market is allowed a surplus male. It is not allowed the "
            "reproductive body. Calves and cows do not leave. Oxen may. Lasnet "
            "sees both affection and interest and, for once, does not force you "
            "to choose. The two are the same structure: the herd's future is not "
            "merchandise. What can be sold is what the cult can spare without "
            "drying the source. A people whose remaining cult is the herd will "
            "have a market ethic that looks like stubbornness to a trader and like "
            "liturgy to anyone who has read the boolâtrie sentence."
            "\n\n"
            "\"Never\" (jamais) is the philosophical word. Not rarely, not unless "
            "the price is high. The cow and the calf are outside the bargain. "
            "Bridewealth can name fifteen cows; the market cannot take a cow. The "
            "difference is that bridewealth keeps nagge inside the alliance of "
            "households, while sale to Sarakole, Tukulor, or Wolof speculators "
            "sends her out of the people. The ox can go. The mother-line of the "
            "herd cannot."
            "\n\n"
            "Existentially the teaching is about what you will not monetize. "
            "Everyone has a market. The question is whether anything in your life "
            "is marked never. If everything is for sale at the right price, you "
            "have no remaining cult. Affection and interest here are not two "
            "motives. They are one refusal: the source-body stays."
        ),
        "prac": (
            "Name one thing you will not sell — a tool, a promise, a living tie, "
            "an hour. Keep the refusal today when a convenient offer appears. If "
            "you cannot name a never, you are living as if you had only oxen and "
            "no cows."
        ),
        "terms": kt(
            ("veaux ni des vaches", "calves nor cows — the unsaleable reproductive body of the herd; oxen are the only licit market flesh"),
            ("bœufs", "oxen — the surplus male who may leave; not the mother, not the young"),
            ("affection ... intérêt", "affection and interest — Lasnet's pair; do not split them; the cult and the economy are one refusal"),
            ("nagge", "the cow who does not go to market — the same being bridewealth names and sale is forbidden to take"),
        ),
        "res": res(
            ("Vedic prohibition on selling the cow of the household", "Both mark the reproductive cow as outside ordinary trade.", "Vedic unsaleability is often priestly and hymnic; this rule is a market sentence spoken over Fulɓe stalls."),
            ("Hebrew firstlings and the unsacrificed dam", "Both distinguish the young and the mother from what may be alienated.", "Biblical law is theistic command; this never is affection-and-interest as a single pastoral law."),
        ),
    },
    {
        "n": 15,
        "title": "Women Carry the Milk",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Commerce",
        "fr": (
            "Leur principal revenu est dans les troupeaux ; ils ont des bœufs et "
            "des moutons en grand nombre [...] Ils vendent aussi du lait et du "
            "beurre que les femmes peules portent dans des outres en cuir ou de "
            "grandes calebasses ; pour leur consommation particulière ils n'usent "
            "comme les Maures que de petit lait. [...] d'autant mieux considérés "
            "qu'ils en ont davantage et sont plus habiles à les soigner."
        ),
        "tr": (
            "Their principal revenue is in the herds; they have oxen and sheep in "
            "great number. They also sell milk and butter, which Peul women carry "
            "in leather skins or large calabashes; for their own consumption they "
            "use, like the Moors, only sour milk. They are the better considered "
            "the more they have and the more skilled they are at caring for them."
        ),
        "comm": (
            "The herd is wealth and honor, and the visible carrier of that wealth "
            "is a woman with a calabash. Lasnet's commerce chapter wants a revenue "
            "line. What he records is a gendered liturgy of milk. Men are better "
            "considered the more animals they have and the more skilled they are "
            "at care. Women carry the milk and the butter to the place where the "
            "surplus becomes exchange. The camp itself drinks petit lait, sour "
            "milk — the thinner remainder. The rich part of the gift walks to "
            "market on a woman's head or hip."
            "\n\n"
            "This is not a lesson that women are porters and men are owners. It "
            "is a lesson that honor (considérés) is skill at care, and that the "
            "cult's product is milk, not meat. A people who will not sell cows "
            "will still sell what the cow gives. The woman who carries the skin "
            "or the calabash is the public face of boolâtrie after conversion: "
            "Islam may own Friday; the milk-road still belongs to the herd."
            "\n\n"
            "Existentially the teaching is that honor and care are one count. You "
            "are not more considered because you hoard. You are more considered "
            "because you have more life in your keeping and you know how to keep "
            "it. Ask who in your household actually carries the gift to the world, "
            "and whether you have mistaken the carrier for a servant of the cult "
            "instead of its priest."
        ),
        "prac": (
            "Carry one gift you usually let someone else carry — food, a message, "
            "a payment, a care — all the way to its recipient today. Do it as the "
            "public face of what you live from, not as an errand."
        ),
        "terms": kt(
            ("lait et beurre", "milk and butter — the cult's surplus; meat is not the sentence; milk is"),
            ("considérés", "considered, honored — honor as a function of herd-size and skill at care, not of speech"),
            ("petit lait", "sour milk, the camp's own drink — the rich part walks out; the thin part stays"),
            ("nagge", "the source whose milk women carry — wealth and honor in one living body"),
        ),
        "res": res(
            ("Vedic go-dohana, the milking as rite", "Both make milking and the gift of milk a public religious-economic act.", "Vedic milking is often a priestly morning office; here the public carrier is the Peul woman on the path to market."),
            ("Serer milk poured at the baobab (this corpus)", "Both treat milk as the matter of relation, not only of diet.", "Serer milk is offered upward to spirits; Fulɓe milk in this sentence is carried outward as wealth that still honors the herd."),
        ),
    },
    {
        "n": 16,
        "title": "Do Not Confess Wealth",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Économe et défiant, il n'avoue jamais sa richesse par crainte d'être "
            "volé ; très hypocrite et très retors, il ne conclut rien sans avoir "
            "longuement réfléchi et être sûr de son fait."
        ),
        "tr": (
            "Thrifty and wary, he never confesses his wealth for fear of being "
            "robbed. He concludes nothing without having reflected at length and "
            "being sure of his ground."
        ),
        "comm": (
            "Do not confess the herd. Lasnet's next words are hypocrite and "
            "trickster — observer-error. What he actually saw is a refuse of "
            "display. A pastoral people whose wealth is walking animals does not "
            "owe a census to the stranger, the taxer, or the raider. \"He never "
            "avows his wealth\" (il n'avoue jamais sa richesse) is pulaaku as "
            "economy: reserve is not a lie about the world; it is a refusal to "
            "make the cult-object into a target. Fear of being robbed is the "
            "practical clause. The philosophical clause is never: wealth that "
            "must be spoken is already half lost."
            "\n\n"
            "The slur hypocrite is what a colonial officer calls a man who will "
            "not open his ledger. The usable teaching is the long reflection "
            "before any conclusion, and the silence about the count of cows. "
            "Bridewealth is named in cows inside the alliance. The market is told "
            "only about oxen. The stranger is told nothing. These are not three "
            "ethics. They are one grammar of what may be said about nagge."
            "\n\n"
            "Existentially the teaching is against the modern duty to narrate "
            "your assets — followers, income, attainments — as if silence were "
            "fraud. Some silences are the remaining cult. If you cannot keep a "
            "number unspoken, you have no herd, only a shop-window. Reflect long. "
            "Conclude when you are sure. Do not confess the count."
        ),
        "prac": (
            "Today, when asked how much you have — money, plans, progress — give "
            "no number. Keep one real good unspoken. Notice the itch to avow. "
            "That itch is the stranger already inside the camp."
        ),
        "terms": kt(
            ("n'avoue jamais sa richesse", "never confesses his wealth — reserve as pastoral law, not hypocrisy; the observer's slur is refused"),
            ("pulaaku", "the honor-code of reserve — later name for the face that does not display the herd"),
            ("défiant", "wary, distrustful — Lasnet's temperament-word; the usable sense is that the cult-object is not public information"),
            ("longuement réfléchi", "having reflected at length — the other half of the sentence; silence plus slowness, not cunning-as-vice"),
        ),
        "res": res(
            ("Matthew 6:3–4, do not let the left hand know", "Both refuse the public confession of the good you hold.", "Matthew hides alms from praise; this Fulɓe silence hides the herd from seizure — same reserve, different predator."),
            ("Stoic inner citadel", "Both treat the inner count as not owed to the forum.", "The Stoic hides judgments; the Fulɓe herder hides cows. One is a soul-practice; the other is a people-practice around nagge."),
        ),
    },
    {
        "n": 17,
        "title": "Gravity Is the Honor-Face",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Fervent musulman mais non fanatique, il affecte une gravité "
            "continuelle, danse rarement (les femmes ne dansent jamais) et méprise "
            "les plaisirs bruyants des autres populations."
        ),
        "tr": (
            "A fervent Muslim but not a fanatic, he keeps a continual gravity, "
            "dances rarely (the women never dance), and disdains the noisy "
            "pleasures of the other peoples."
        ),
        "comm": (
            "Honor has a face, and the face is gravity. Lasnet writes affecte une "
            "gravité continuelle as if it were a pose. The remnant reading is "
            "pulaaku: reserve as the way a cattle-people refuse to leak inner "
            "weather into noise. Dancing rarely is not joylessness. It is the "
            "same impassibility that initiation already taught as déshonneur to "
            "complain. The herd-cult produces a public body that does not "
            "advertise itself. Continual gravity is how that body walks through "
            "a village of louder cults."
            "\n\n"
            "\"The women never dance\" must not be taught as a lesson against "
            "women. It is Lasnet's gendered observation of the same reserve. If "
            "pulaaku is shame-honor and self-mastery, then the women of the camp "
            "are not being denied a pleasure as inferiors; they are being "
            "described as the stricter keepers of the honor-face. Handle the "
            "sentence as ethnography of semteende, not as a rule that women "
            "should be still while men may move. The philosophical claim is "
            "reserve, not misogyny. A tradition that consults the mother before "
            "every great act is not a tradition whose women are ornaments."
            "\n\n"
            "Existentially the teaching is that not every joy needs a noise. "
            "Disdain for noisy pleasures can become pride, and Lasnet is happy "
            "to record pride. The usable core is smaller: keep a gravity that "
            "does not require the room to know how you feel. If your honor "
            "depends on being seen celebrating, you have already sold the face "
            "the herd-cult was keeping."
        ),
        "prac": (
            "For one social hour today, keep continual gravity: no performance of "
            "mood, no extra noise to prove you belong. Do not police anyone else's "
            "dance. Keep your own face. That is the honor-form, not a ban on women."
        ),
        "terms": kt(
            ("pulaaku", "Fulɓe-ness — reserve, endurance, shame-honor; Lasnet's gravité continuelle is the visible rule without the name"),
            ("gravité continuelle", "continual gravity — the honor-face; not joylessness; completeness of form"),
            ("semteende", "later Pulaar shame-reserve — the inner hinge of not leaking; women never dance is Lasnet's gendered note on this, not a ranking of persons"),
            ("plaisirs bruyants", "noisy pleasures — what the remnant refuses; disdain can curdle into pride; the teaching is reserve, not contempt for neighbors"),
        ),
        "res": res(
            ("Stoic gravity of the sage", "Both treat composure as a public ethic, not a private mood.", "Stoic gravity is a judgment about impressions; Fulɓe gravity here is a people-face around the herd and the mother."),
            ("Zen dignity of ordinary walking", "Both refuse noisy display as a mark of realization.", "Zen dignity is emptiness walking; this dignity is pulaaku walking — shame-honor, not no-self."),
        ),
    },
    {
        "n": 18,
        "title": "The Fetishists Still Till",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Dans les régions fertiles comme celles que l'on rencontre en Gambie, "
            "en Casamance, dans le haut Sénégal, ils sont devenus agriculteurs et "
            "cultivent leurs lougans tout en élevant leur bétail avec le plus "
            "grand soin. Il est bon d'ajouter que ce sont ordinairement les "
            "fétichistes qui se livrent à ces travaux, les musulmans étant trop "
            "orgueilleux pour travailler la terre."
        ),
        "tr": (
            "In fertile regions such as those of the Gambia, Casamance, and the "
            "upper Senegal, they have become farmers and cultivate their fields "
            "while still raising their cattle with the greatest care. It is well "
            "to add that it is ordinarily the fetishists who give themselves to "
            "this work, the Muslims being too proud to work the land."
        ),
        "comm": (
            "The old center still has dirt on its hands. Lasnet's fétichistes is "
            "the colonial word for those who have not taken Islam — the same "
            "remainder the tiedo sentence named. They till. They also raise the "
            "cattle with the greatest care. Conversion, in this paragraph, has "
            "produced a pride that will not touch the earth. The remnant has not "
            "forgotten that a people who live from herd and field must still "
            "stoop. Pride that will not till is not pulaaku. Pulaaku is reserve. "
            "This pride is a new honor that has detached itself from the cult-object."
            "\n\n"
            "\"Too proud to work the land\" is Lasnet's comparison, and it can be "
            "read as a slur on Muslims or as a slur on pagans. Refuse both. The "
            "philosophical move is the remainder: where the old cult is still "
            "practiced, labor and cattle-care are one life. Where the new "
            "confession has become a rank, the land is left to someone else. The "
            "lougan (field) beside the herd is the settled form of boolâtrie in "
            "fertile Senegambia — not a betrayal of nomadism, but the same care "
            "when pasture does not force a move."
            "\n\n"
            "Existentially the teaching is that a converted identity can become "
            "too fine to do the work that still feeds it. If your new name will "
            "not stoop, it is not a deeper religion. It is a costume. Keep one "
            "contact with the dirt that your pride has started to outsource."
        ),
        "prac": (
            "Do one necessary earth-work today that your present identity considers "
            "beneath it — wash, carry, dig, mend, cook. Do it as the fetishist "
            "who still tills, not as a favor. Notice the pride that wanted to "
            "delegate it."
        ),
        "terms": kt(
            ("fétichistes", "Lasnet's file-word for the unconverted — the remainder who still till; not a lesson in \"fetishism\"; a demographic of the old center"),
            ("lougans", "fields, cultivated plots — the settled companion of the herd in fertile Casamance and upper Senegal"),
            ("trop orgueilleux", "too proud — conversion as a rank that drops the earth; pulaaku is not this pride"),
            ("plus grand soin", "greatest care — even as farmers they raise cattle as the undropped cult"),
        ),
        "res": res(
            ("Genesis 2–3, tilling after the garden", "Both bind human work to the ground that feeds.", "Genesis tills under a curse; this remnant tills as the unconverted center, while the converted have become too proud."),
            ("Benedictine ora et labora", "Both refuse a religion that will not put its hands to the field.", "The monastery theorizes work as prayer; Lasnet's fetishists simply still do the work the new rank has dropped."),
        ),
    },
    {
        "n": 19,
        "title": "Ardo and Tamsir",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Organisation sociale",
        "fr": (
            "Les grandes agglomérations de Peuls sont organisées, comme au "
            "Fouta-Djallon, en républiques théocratiques ayant à leur tête un "
            "almamy qui exerce le pouvoir temporel et religieux en prenant "
            "l'opinion des anciens et des notables ; chaque district a un chef "
            "politique et militaire, ardo, et un chef religieux, tamsir, nommés "
            "par l'almamy."
        ),
        "tr": (
            "The great Peul agglomerations are organized, as in Futa Jallon, into "
            "theocratic republics headed by an almamy who exercises temporal and "
            "religious power while taking the opinion of the elders and notables. "
            "Each district has a political and military chief, ardo, and a "
            "religious chief, tamsir, named by the almamy."
        ),
        "comm": (
            "Power here is split on purpose. The almamy holds both temporal and "
            "religious office at the top, but he takes the opinion of elders, and "
            "under him the district is two offices: ardo (political, military) and "
            "tamsir (religious). Lasnet is describing the imamate as he found it. "
            "The usable social form is older than the particular Islamic titles: "
            "a cattle-people will not let one man be the only mouth. The herd "
            "decides the path; the people decide by pairing force with speech "
            "about the sacred."
            "\n\n"
            "Ardo is the Pulaar word the source actually names. It is not a "
            "generic chief. It is the political-military office of a district, "
            "still standing after the satigui of Futa Toro was suppressed. Tamsir "
            "(Lasnet's tamsir / tamsii) is the religious counterpart. The pair is "
            "the teaching. A cult of the herd that has entered Islam does not "
            "become a single sword. It becomes a two-headed district under an "
            "almamy who must still hear the anciens."
            "\n\n"
            "Existentially the teaching is against the fantasy of the solitary "
            "founder. If you hold both the sword and the prayer in one person and "
            "will not take anyone's opinion, you are not more traditional than "
            "the Fulɓe imamate. You are less. Split the office. Hear the elders. "
            "Name an ardo for the move and a tamsir for the meaning."
        ),
        "prac": (
            "On one decision today, split the office: let one person (or one hour) "
            "handle the force of the act, and another handle what the act means. "
            "Do not let a single mood be both ardo and tamsir. Take one elder's "
            "opinion before you close."
        ),
        "terms": kt(
            ("ardo", "Pulaar political-military chief of a district — named by the almamy; not a generic chief; the force-office of the pair"),
            ("tamsir", "religious chief of a district — Lasnet's tamsir / tamsii; the speech-office beside the ardo"),
            ("almamy", "imam-head of the theocratic republic — holds both powers at the top but must take the opinion of elders"),
            ("anciens et notables", "elders and notables — the counsel the almamy is not free to skip"),
        ),
        "res": res(
            ("Roman consuls and pontifex", "Both split or pair force with sacred speech so one mouth is not the whole city.", "Rome's pair is civic and priestly in a written constitution; ardo and tamsir are district offices under an almamy who still hears elders."),
            ("Confucian wang and shi", "Both refuse to let military command be the only authority.", "The Chinese pair is king and scholar-ritualist; the Fulɓe pair is pastoral-military ardo and religious tamsir in a cattle republic."),
        ),
    },
    {
        "n": 20,
        "title": "Satigui Before El Hadj Omar",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Organisation sociale",
        "fr": (
            "Le chef des Peuls du Fouta-Toro portait autrefois le titre de satigui, "
            "bien avant El Hadj Omar, sa fonction a été supprimée ; chaque tribu "
            "a conservé son ardo et son tamsir, les chefs de village sont sous "
            "leurs ordres ; ces fonctions sont devenues héréditaires et ne peuvent "
            "sortir de la première caste."
        ),
        "tr": (
            "The chief of the Peuls of Futa Toro formerly bore the title satigui, "
            "well before El Hadj Omar; his office has been suppressed. Each tribe "
            "has kept its ardo and its tamsir; the village chiefs are under their "
            "orders. These offices have become hereditary and cannot leave the "
            "first caste."
        ),
        "comm": (
            "A title can die and the pair of offices remain. Satigui is the old "
            "name of the Futa Toro chief, older than the jihad of El Hadj Omar "
            "(ʿUmar Tall). Lasnet is careful: well before. The 1913 chronicle of "
            "Siré-Abbâs-Soh, used here only for social form, remembers the same "
            "depth — a Fulɓe political name that Islam later overwrote. The "
            "function was suppressed. What was not suppressed is the tribal pair: "
            "ardo and tamsir, with village chiefs under them. Conversion can "
            "remove a crown and still leave the district grammar standing."
            "\n\n"
            "Heredity and first caste are Lasnet's colonial ranking of a "
            "pastoral aristocracy. Do not teach caste-contempt as the lesson. "
            "The usable claim is continuity under a new confession. The satigui "
            "is gone. The ardo is not. A people whose remaining cult is the herd "
            "will keep the offices that still serve motion, counsel, and the "
            "sacred even when the highest title has been abolished by a reformer. "
            "The chronicle is not used here for Islamic law. It is used for this "
            "fact of form: names change; the pair remains."
            "\n\n"
            "Existentially the teaching is about what you keep when a reform "
            "erases your favorite title. If the only thing that made you a people "
            "was the high name, the reform wins. If you still have an ardo and a "
            "tamsir — a force and a meaning, a move and a counsel — the people "
            "are not gone. Let the satigui die. Keep the pair."
        ),
        "prac": (
            "Name one title you have already lost — a job, a role, a reputation. "
            "Today, keep the work the title used to name, without the name. Do "
            "not rebuild the crown. Keep the pair of acts the crown was covering."
        ),
        "terms": kt(
            ("satigui", "old title of the Futa Toro Fulɓe chief, before El Hadj Omar — a political name the jihad suppressed; the district pair outlived it"),
            ("ardo", "the political-military office each tribe kept after the satigui was abolished"),
            ("tamsir", "the religious office kept beside the ardo — the other half of what the high title could not take with it"),
            ("El Hadj Omar", "ʿUmar Tall — the reformer after whom the satigui no longer stands; used here only to date the older title, not to teach his law"),
        ),
        "res": res(
            ("Israel after the last judge, before the kings", "Both remember a political form older than the later central office.", "Israel's memory becomes kingship; Futa Toro's satigui is suppressed and the older pair (ardo, tamsir) remains."),
            ("Japanese tennō and shogun", "Both show a high name that can recede while working offices continue.", "The tennō remains as symbol; the satigui is abolished. The Fulɓe remainder is the tribal pair, not an empty throne."),
        ),
    },
    {
        "n": 21,
        "title": "Never Sell the Breeding Stock",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Commerce",
        "fr": (
            "Ils ont un assez grand nombre de bœufs porteurs bien dressés et "
            "qu'ils conduisent par un anneau passé dans la cloison nasale ; ces "
            "animaux constituent leur monture la plus fréquente [...] les Peuls "
            "s'en défont rarement. Dans leurs marchés ils ne se défont que des "
            "bœufs, jamais des veaux ni des vaches."
        ),
        "tr": (
            "They have a good number of well-trained pack oxen, led by a ring "
            "through the nasal septum; these animals are their most usual mount. "
            "The Peuls rarely part with them. In their markets they part only "
            "with oxen, never with calves or cows."
        ),
        "comm": (
            "There is a second never inside the first. Calves and cows do not "
            "sell because they are the mother-line. Pack oxen rarely sell because "
            "they are the people's feet. Lasnet's bœufs porteurs are not meat "
            "waiting for a buyer. They are the mount, led by a nose-ring, the "
            "body that makes displacement possible when pasture fails. To sell "
            "the breeding stock is to sell the future. To sell the pack oxen is "
            "to sell the path. Both refusals are the same cult: nagge as what "
            "must remain if the group is to remain."
            "\n\n"
            "\"Rarely part with them\" (s'en défont rarement) is weaker than "
            "jamais and still a law. The market may take a surplus ox. It may "
            "not take the trained body that carries the camp. A spirituality that "
            "sells its means of motion for a good price has already chosen to "
            "become sedentary cargo. The herd-cult will not make that bargain. "
            "Affection and interest, again, are one."
            "\n\n"
            "Existentially the teaching is: do not sell the thing that lets you "
            "move. People sell their rest, their tools, their teachers, their "
            "animals of burden, and then wonder why they cannot change pasture. "
            "Keep the breeding line. Keep the pack. The ox that is only meat is "
            "the only ox the market is owed."
        ),
        "prac": (
            "Name the one tool, animal, practice, or relationship that is your "
            "pack ox — the thing that lets you move. Refuse one offer to part "
            "with it today, even a flattering one. The market may have your "
            "surplus. It may not have your feet."
        ),
        "terms": kt(
            ("bœufs porteurs", "pack oxen — the mount of a cattle-people; rarely sold because they are the path, not the surplus"),
            ("anneau", "nose-ring — the instrument of leading, not of ownership-as-cruelty; the animal is conducted, not dragged as cargo"),
            ("s'en défont rarement", "rarely part with them — the second never, weaker in grammar, same in cult"),
            ("nagge", "the living capital that must not be alienated — mother-line and mount together"),
        ),
        "res": res(
            ("Homeric horses of the kings, not for trade", "Both mark the trained animal of motion as outside ordinary sale.", "Homeric horses are aristocratic prestige; Fulɓe pack oxen are the camp's ordinary feet."),
            ("Daoist uncarved block that is not sold as timber", "Both refuse to turn the source-body into merchandise.", "Laozi's block is unused potential; the pack ox is used every day and still not sold."),
        ),
    },
    {
        "n": 22,
        "title": "Tomb Profanation Is Sacrilege",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Funérailles",
        "fr": (
            "Les Peuls ont, comme tous les Musulmans, beaucoup de respect pour "
            "les morts ; profaner une tombe est un sacrilège."
        ),
        "tr": (
            "The Peuls have, like all Muslims, much respect for the dead. To "
            "profane a tomb is a sacrilege."
        ),
        "comm": (
            "The negative of the green-leaf greeting is a hard word: sacrilège. "
            "Lasnet frames it as generic Islam. The Fulɓe intensification is "
            "pastoral. A people who throw forage to the dead as they pass will "
            "treat the disturbance of a grave as more than bad manners. Profanation "
            "is the opposite of salut. One act acknowledges the trépassés as "
            "persons on the road. The other treats the tomb as a thing that can "
            "be opened, used, or mocked. Sacrilege means the dead are still "
            "inside the cult, not outside it as scenery."
            "\n\n"
            "\"Like all Muslims\" is the observer's leveling. Keep the leveling "
            "as a date — this is recorded inside Islam — and keep the specific "
            "gravity. In a mobile world the grave is one of the few fixed points. "
            "The camp can be abandoned; the tomb cannot be treated as abandoned "
            "property. That is why the greeting is in passing and the prohibition "
            "is absolute. You may not stay. You may not violate."
            "\n\n"
            "Existentially the teaching is that some places are not available "
            "for your project. A grave is not a resource. If you can turn every "
            "fixed point of the dead into use, you have no ancestors, only land. "
            "Yettôdé said the ancestor legislates a living avoidance. This unit "
            "says the ancestor also legislates an unmoveable spot. Do not profane "
            "it. Greet it, and go."
        ),
        "prac": (
            "Today, leave one place of the dead untouched that you might have "
            "used — a shortcut across a cemetery, a joke at a memorial, a "
            "photograph for display. Pass, greet if you can, and do not take."
        ),
        "terms": kt(
            ("sacrilège", "sacrilege — profanation of a tomb as a religious crime, not a civic nuisance; the dead remain inside the cult"),
            ("profaner", "to profane — the opposite of the green-leaf salut; treating the grave as available"),
            ("tombe", "tomb — one of the few fixed points in a mobile pastoral world; the camp may be left; this may not be used"),
            ("trépassés", "those who have gone over — still owed a greeting and a prohibition, not only a memory"),
        ),
        "res": res(
            ("Antigone, the unburied brother", "Both treat violence to the dead as a religious rupture, not a policy dispute.", "Antigone defies the city to bury; this unit forbids the living to open what is already buried."),
            ("Serer refusal to treat the dead as mute (this corpus)", "Both keep the corpse-side of the world under law.", "Serer law is speech into the ear; Fulɓe law here is a ban on profanation plus a toss of green."),
        ),
    },
    {
        "n": 23,
        "title": "The East Was the Cradle",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — origins",
        "fr": (
            "Quant aux Peuls eux-mêmes, ils se considèrent comme tout à fait "
            "distincts des nègres et se donnent pour berceau le Founangui, (pays "
            "de l'est) qu'ils quittèrent quand la région n'eut plus assez de "
            "pâturages pour nourrir leurs troupeaux. Quelle que soit l'origine "
            "des Peuls, leur migration à travers le continent africain [...] est "
            "antérieure à l'islamisme, car aujourd'hui une grande partie de leur "
            "population est encore fétichiste."
        ),
        "tr": (
            "As for the Peuls themselves, they hold themselves quite distinct and "
            "give as their cradle Founangui, the country of the east, which they "
            "left when the region no longer had enough pasture to feed their "
            "herds. Whatever the origin of the Peuls, their migration across the "
            "African continent is earlier than Islam, for today a great part of "
            "their population is still fetishist."
        ),
        "comm": (
            "Origin is a pasture story, not a race story. Lasnet's chapter opens "
            "with European fantasies — Egypt, a lost Roman legion — which this "
            "unit refuses. What the Fulɓe tell him is Founangui, the country of "
            "the east, left when the grass failed. The first displacement is "
            "already the law of unit 3: the herd's need decides the path. "
            "Self-account is not a skull-index. Self-account is: we were where "
            "the cattle could eat, and then we were not."
            "\n\n"
            "\"Earlier than Islam\" (antérieure à l'islamisme) is the "
            "chronological claim that warrants the whole collection. Migration "
            "is old enough that a great part is still unconverted. The remainder "
            "is not a footnote to the imamate. The imamate is a later form of a "
            "people who already moved for nagge. Distinctness, in the usable "
            "sense, is occupational and liturgical — herders with one cult — not "
            "the racial ranking Lasnet's physical-anthropology pages try to "
            "install. Those pages are skipped."
            "\n\n"
            "Existentially the teaching is that your true origin-story is the "
            "first time you left because something living could not eat. Nations "
            "prefer a glorious cradle. The Fulɓe sentence is poorer and truer: "
            "the east was enough, then it was not, and the herd walked. If your "
            "myth of beginning has no hunger in it, it is a costume."
        ),
        "prac": (
            "Write one sentence of origin that names a lack — a pasture that "
            "failed, a work that ended, a place that could not feed you — and "
            "the move that followed. Keep that sentence today as your Founangui. "
            "Do not upgrade it into a proud genealogy."
        ),
        "terms": kt(
            ("Founangui", "country of the east — the Fulɓe autonym for the cradle; not Egypt, not Rome; a pasture that failed"),
            ("pâturages", "pastures — the true cause of the first migration; origin as hunger of the herd"),
            ("antérieure à l'islamisme", "earlier than Islam — the chronological warrant for reading a pre-Islamic remainder"),
            ("nagge", "the cattle whose hunger wrote the first path out of the east"),
        ),
        "res": res(
            ("Abraham leaving Canaan/Haran for pasture and promise", "Both begin a people with a departure caused by life that must be fed.", "Abraham's departure is commanded by God; the Fulɓe departure is commanded by exhausted grass."),
            ("Daoist uncarved beginning", "Both prefer a poor origin to a legendary ancestry.", "Laozi's beginning is metaphysical; Founangui is a named east the cattle could no longer keep."),
        ),
    },
    {
        "n": 24,
        "title": "They Make Themselves Loved",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Les Peuls se distinguent des autres races de l'Afrique par leurs "
            "mœurs de bergers. Sans cesse au milieu de leurs troupeaux, ils les "
            "connaissent admirablement et s'en font aimer."
        ),
        "tr": (
            "The Peuls distinguish themselves from the other peoples of Africa by "
            "their manners as shepherds. Always in the midst of their herds, they "
            "know them admirably and make themselves loved by them."
        ),
        "comm": (
            "Knowledge here is not a list of marks on the ear. It is a life spent "
            "in the midst (sans cesse au milieu) until the animals love you back. "
            "Lasnet's first philosophical sentence on Peul manners is this: they "
            "are shepherds, they know, they are loved. Distinction is occupational "
            "and relational, not anatomical. The physical-anthropology pages that "
            "follow in his book are skipped as contempt. This sentence is kept as "
            "teaching. To know admirably is already a rite. To be loved by the "
            "known is the rite's success."
            "\n\n"
            "\"Make themselves loved\" (s'en font aimer) puts agency on the "
            "herder without making the cow an object. You can fail at this. You "
            "can live in the midst and still not be loved, if you are only a "
            "driver. The remnant cult is the opposite of driving. It is a "
            "two-way recognition: the human knows the animal; the animal accepts "
            "the human. Boolâtrie without this clause would be a European word "
            "for stock-breeding. With this clause it is a relation."
            "\n\n"
            "Existentially the teaching is that mastery without being loved is "
            "only control. If the lives you claim to know do not want you near "
            "them, you do not know them yet. Stay in the midst longer. Change "
            "your hands. Do not add a theory of shepherdhood on top of a relation "
            "that has not yet answered."
        ),
        "prac": (
            "Spend one uninterrupted hour in the midst of a life you claim to "
            "know — a person, an animal, a work. Do not improve it. See whether "
            "you are wanted there. If not, change the hands, not the story."
        ),
        "terms": kt(
            ("mœurs de bergers", "manners of shepherds — Lasnet's distinction-word; occupational and liturgical, not racial"),
            ("s'en font aimer", "make themselves loved — the success-condition of knowing; the herd answers"),
            ("sans cesse au milieu", "always in the midst — knowledge as presence, not as periodic inspection"),
            ("nagge", "the beings whose love is the measure of the herder's knowledge"),
        ),
        "res": res(
            ("John 10:14, I know my own and my own know me", "Both make knowing and being known the definition of the shepherd.", "The Gospel's shepherd is the Christ; this shepherd is a Fulɓe herder whose cult-object is the herd itself."),
            ("Upaniṣadic tat tvam asi as recognition", "Both treat real knowledge as a two-way identity, not a catalogue.", "The Upaniṣad recognizes the Self; this sentence recognizes the cow as a being that can love you back."),
        ),
    },
    {
        "n": 25,
        "title": "The House Is Left Behind",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Habitations",
        "fr": (
            "Les Peuls étant nomades et se déplaçant suivant les besoins de leurs "
            "troupeaux n'ont guère d'installation bien définitive ; leurs cases "
            "sont des paillottes rondes [...] souvent ce sont de simples gourbis "
            "en paille faits de paillassons mobiles fabriqués par les femmes ; "
            "lorsqu'ils se déplacent, ils les abandonnent complètement et vont "
            "reconstruire plus loin."
        ),
        "tr": (
            "The Peuls, being nomads and moving according to the needs of their "
            "herds, have almost no lasting installation. Their huts are round "
            "straw houses; often they are simple straw shelters of movable mats "
            "made by the women. When they move, they abandon them completely and "
            "go rebuild farther on."
        ),
        "comm": (
            "The house is not the shrine. The herd is. When the pasture fails, "
            "the hut is abandoned completely (ils les abandonnent complètement) "
            "and built again farther on. Women make the mats; the mats move or "
            "are left. Lasnet notes that in Futa Jallon, where the land can feed "
            "the cattle without displacement, one finds thick-walled houses and "
            "verandas. Settlement is the exception that proves the law: when the "
            "herd does not force a path, the house may thicken. When the herd "
            "forces a path, the house is straw."
            "\n\n"
            "This is the architectural form of unit 3. A spirituality that "
            "confuses the sacred with real estate will hear abandonment as "
            "poverty. The remnant cult hears it as fidelity. You do not owe the "
            "walls a vigil if the animals cannot eat. Villages are clean and "
            "undefended — Lasnet says they present no defense — because the "
            "wealth can walk and the shrine is not a granary you must fortify. "
            "The clean pen, not the hut, is the place that has something "
            "religious in it."
            "\n\n"
            "Existentially the teaching is: leave the room that no longer feeds "
            "the life you serve. People stay in houses, jobs, and identities out "
            "of respect for walls. The Fulɓe sentence is colder and kinder. "
            "Abandon the hut. Rebuild farther on. The cult walked first."
        ),
        "prac": (
            "Abandon one installation today that you have been maintaining out of "
            "habit — a folder, a corner, a plan that no longer feeds what you "
            "actually keep alive. Leave it completely. Rebuild the needed piece "
            "farther on, lighter."
        ),
        "terms": kt(
            ("gourbis", "straw shelters of movable mats — the house as a thing women make and the group can leave"),
            ("abandonnent complètement", "abandon completely — fidelity to the herd, not failure at housing"),
            ("besoins de leurs troupeaux", "needs of their herds — the same law that decides the path now decides the walls"),
            ("wuro", "later Pulaar camp — the human place that follows nagge; not in Lasnet; the structure is this abandonment"),
        ),
        "res": res(
            ("Hebrew mishkan, the portable dwelling", "Both refuse to let holiness require a permanent house.", "The tabernacle is portable because God travels; the Fulɓe hut is leavable because the herd travels."),
            ("Daoist unfixed dwelling", "Both prefer a life that can be set down.", "Zhuāngzǐ's unfixedness is freedom from use; this unfixedness is obedience to pasture."),
        ),
    },
    {
        "n": 26,
        "title": "A Free Man Would Derogate",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Industrie",
        "fr": (
            "Les Peuls font d'habiles artisans, malheureusement un homme libre "
            "croirait déroger en s'occupant d'autre chose que de ses troupeaux "
            "ou de ses cultures ; aussi les ouvriers qu'ils possèdent sont-ils "
            "le plus souvent des étrangers, Toucouleurs en majorité, et "
            "jouissent-ils de peu de considération."
        ),
        "tr": (
            "The Peuls make skilled artisans; unfortunately a free man would think "
            "he derogated by occupying himself with anything other than his herds "
            "or his fields. So the workers they have are most often foreigners, "
            "Tukulor in the majority, and they enjoy little consideration."
        ),
        "comm": (
            "The old center is still the only work that does not feel like a fall. "
            "Lasnet's malheureusement and his note that artisans enjoy little "
            "consideration are colonial caste-gossip. Do not teach contempt for "
            "smiths, weavers, or griots. The Bambados griots, he says later, are "
            "a category apart. The usable claim is narrower and older: a free "
            "Fulɓe person's work is the herd and, in fertile country, the field. "
            "Every other craft is socially marked as not-the-cult. That marking "
            "can become injustice. The philosophical remainder is that the cult "
            "still knows which labor is its own."
            "\n\n"
            "\"Would think he derogated\" (croirait déroger) is honor-language. "
            "Pulaaku here is occupational: you do not leave nagge for a trade. "
            "The same people who will not sell cows will not become the people "
            "who make the knife, except the redsmiths (abharbéy) who work gold "
            "and silver and remain Peul. Iron is left to others. The herd-cult "
            "keeps its hands on animals and earth, and lets the rest of the "
            "workshop stand beside it without becoming it."
            "\n\n"
            "Existentially the teaching is not \"despise makers.\" It is: know "
            "which work is your remaining cult, and do not abandon it for a "
            "livelihood that only looks like status. If you have left the one "
            "labor that still feels like a rite, you have already derogated, "
            "whatever your new title is. Return a hand to the herd or the field "
            "— the life you actually keep."
        ),
        "prac": (
            "Give one hour today to the labor that is actually your cult — the "
            "care, the field, the keeping — and refuse one piece of work that "
            "only looks like status. Do not despise anyone else's craft. Keep "
            "your own from derogating."
        ),
        "terms": kt(
            ("déroger", "to derogate, to fall from rank — honor as staying with herd and field; do not teach this as contempt for artisans"),
            ("homme libre", "free man — the pastoral subject whose work is nagge and lougan; caste-language is Lasnet's; the cult-claim is occupational"),
            ("troupeaux ou de ses cultures", "herds or fields — the two licit labors of the old center"),
            ("pulaaku", "honor that can curdle into pride about work; the usable core is not leaving the cult-labor"),
        ),
        "res": res(
            ("Plato's Republic, one man one work", "Both assign a people a proper labor and treat leaving it as a fall.", "Plato's fall is civic injustice; this fall is leaving the herd-cult for a marked trade. Do not import Plato's contempt."),
            ("Benedictine refusal of idleness", "Both treat a named labor as the religious life of a community.", "The monastery theorizes all work as prayer; the Fulɓe remnant theorizes one work — herd and field — as the work that does not derogate."),
        ),
    },
    {
        "n": 27,
        "title": "Long Reflection Before Any Bargain",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Mœurs. Coutumes",
        "fr": (
            "Il ne conclut rien sans avoir longuement réfléchi et être sûr de "
            "son fait, n'hésitant pas d'ailleurs à rouler de son mieux ceux qui "
            "traitent avec lui."
        ),
        "tr": (
            "He concludes nothing without having reflected at length and being "
            "sure of his ground — and he does not hesitate to get the better of "
            "those who deal with him."
        ),
        "comm": (
            "Slowness is the ethic; \"trickster\" is the observer's insult. "
            "Lasnet wants a character sketch: hypocrite, cunning, he will roll "
            "you if he can. Invert the slur. What the sentence actually teaches "
            "is a decision-rule: conclude nothing until you have reflected at "
            "length and are sure of your fact. A people who never confess wealth, "
            "never sell cows, and consult the mother before a great act will not "
            "close a bargain at the stranger's tempo. The colonial officer "
            "experiences that slowness as fraud. The remnant experiences it as "
            "not being hurried off the path the herd already chose."
            "\n\n"
            "\"Sure of his fact\" (sûr de son fait) is the complement of "
            "impassibility. At the threshold you do not complain. At the market "
            "you do not rush. Both are pulaaku: the face and the pace do not "
            "leak. Getting the better of a counterpart can become theft; refuse "
            "that as teaching. Keep the long reflection. A cattle-people whose "
            "wealth walks away if you guess wrong has reasons to be slow that "
            "a cash-trader does not share."
            "\n\n"
            "Existentially the teaching is against the modern virtue of closing "
            "fast. If you conclude in order to seem decisive, you have already "
            "sold the cow. Reflect until you are sure. The stranger's impatience "
            "is not a moral claim on you. It is his tempo. You are not required "
            "to adopt it."
        ),
        "prac": (
            "Delay one conclusion today that you were about to make at someone "
            "else's pace — a purchase, a yes, a send. Reflect until you are sure "
            "of the fact. Then conclude, or refuse. Do not roll anyone. Be slow."
        ),
        "terms": kt(
            ("longuement réfléchi", "having reflected at length — the decision-rule; not cunning-as-vice"),
            ("sûr de son fait", "sure of his ground — the close-condition; haste is the real derogation"),
            ("pulaaku", "reserve of pace as well as of face — slowness as honor"),
            ("conclut rien", "concludes nothing — the never of speech in the market, kin to never confessing wealth"),
        ),
        "res": res(
            ("Stoic delay of assent", "Both refuse to conclude while the impression is still rushing you.", "Stoic delay is about inner judgments; this delay is about a bargain that could cost nagge."),
            ("Confucian caution in speech and compact", "Both treat a hasty yes as a moral failure.", "Confucian caution is civic sincerity; Fulɓe caution is pastoral — the herd cannot be unsaid."),
        ),
    },
    {
        "n": 28,
        "title": "Honor Is Skill at Care",
        "src": "Lasnet, Une mission au Sénégal (1900), Peuls — Commerce",
        "fr": (
            "Ils sont très attachés à leurs animaux, s'en occupent eux-mêmes, "
            "d'autant mieux considérés qu'ils en ont davantage et sont plus "
            "habiles à les soigner."
        ),
        "tr": (
            "They are deeply attached to their animals, tend them themselves, and "
            "are the better considered the more they have and the more skilled "
            "they are at caring for them."
        ),
        "comm": (
            "Honor is not a speech. Honor is a count of living bodies plus a "
            "skill. Lasnet's considérés is the same honor bridewealth measures "
            "in cows and initiation measures in impassibility. Here the measure "
            "is explicit: the more animals, and the more able at care (plus "
            "habiles à les soigner). Possession without skill is not the full "
            "sentence. Skill without animals is not either. The remnant cult "
            "joins them. You tend them yourselves (s'en occupent eux-mêmes). "
            "Delegated care is already a thinning of honor."
            "\n\n"
            "This is boolâtrie without the Latin word. Reclus saw something "
            "religious in the clean pen. Lasnet sees honor in the hand that "
            "knows how to keep the animal alive. Pulaaku is often taught as "
            "reserve and shame. This unit adds the missing half: competence. "
            "A grave face over a dying calf is not honor. The ramp, the dummy "
            "skin, the unsold cow, the carried milk — those are honor as skill. "
            "The collection ends where it began. The remaining cult is the herd, "
            "and the remaining honor is being good at the cult."
            "\n\n"
            "Existentially the teaching is against honor as display and against "
            "care as a feeling. If you want to be considered, have more life in "
            "your keeping and be more able at keeping it. Tend it yourself. The "
            "mother you consult, the ancestor's interdit, the green leaves on "
            "the road — all of them assume a person whose hands still know the "
            "animals. Without that skill the rest is costume."
        ),
        "prac": (
            "Tend one living thing yourself today — do not delegate the care. "
            "Do the skilled act, not the gesture. Let honor be the improvement "
            "in your hands, not the story you tell about being a caring person."
        ),
        "terms": kt(
            ("habiles à les soigner", "skilled at caring for them — honor as competence, not as speech or face alone"),
            ("considérés", "considered, honored — the public measure: more life in keeping, more skill at keeping"),
            ("s'en occupent eux-mêmes", "tend them themselves — delegated care thins the cult"),
            ("pulaaku", "reserve plus this competence — shame-honor without skill is only a face"),
        ),
        "res": res(
            ("Aristotle, aretē as excellence in a function", "Both make honor a skill in a proper work, not a title.", "Aristotle's excellence is civic and rational; this excellence is pastoral — the function is keeping nagge alive."),
            ("Zen care of the ordinary thing", "Both locate dignity in how a thing is tended, not in talk about tending.", "Zen care is emptiness in the hand; Fulɓe care is the herd in the hand, and the honor-count that follows."),
        ),
    },
]


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.{SLUG}_{n:03d}"
    hero = n in HEROES
    original = u["fr"]
    layers = [
        {"kind": "original", "label": "Original", "body": original},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"PULAAR_{n:03d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": u["title"],
        "title": u["title"],
        "unit_type": "teaching_passage",
        "commentary": u["comm"],
        "themes": list(THEMES),
        "tags": [SLUG, *THEMES],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "section": u.get("src", "Peuls"),
            "category": "fulbe-pastoral",
            "verse": str(n),
            "cultural_context": NOTE,
            "original_source": u.get("src", "Lasnet 1900 / Crozals 1883"),
            "original_reliability": (
                "SOURCED — French observer sentence from Lasnet 1900, Crozals 1883, "
                "Reclus as cited, or Delafosse–Gaden 1913 for social form; Hampâté Bâ 1961 not used"
            ),
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": original,
    }
    if hero:
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
        stem = name[: -len(".yml")]
        # pulaar_tradition_pulaar_tradition_001.yml → pulaar_tradition.pulaar_tradition_001
        prefix = f"{SLUG}_{SLUG}_"
        uid_from_name = f"{SLUG}.{SLUG}_{stem[len(prefix):]}" if stem.startswith(prefix) else ""
        if uid_from_name not in keep:
            os.remove(os.path.join(OUT, name))
            removed += 1
    short = [u["comm"] for u in UNITS if len(u["comm"].split()) < 150]
    if short:
        raise SystemExit(f"commentary below 150 words on {len(short)} unit(s)")
    ids_sorted = [f"{SLUG}.{SLUG}_{u['n']:03d}" for u in UNITS]
    heroes = [f"{SLUG}.{SLUG}_{n:03d}" for n in sorted(HEROES)]
    print(f"{SLUG}: {len(keep)} units (floor 26) · tts_key {heroes}" + (f" · removed {removed} stale" if removed else ""))
    for uid in ids_sorted:
        print(f"  {uid}")
    return len(keep)


if __name__ == "__main__":
    raise SystemExit(0 if build() >= 26 else 1)
