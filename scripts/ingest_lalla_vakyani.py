#!/usr/bin/env python3
"""Ingest Lal Ded (Lallā Vākyāni) from Grierson & Barnett 1920.

Public-domain source: Sir George Grierson & Lionel D. Barnett,
*Lallā-Vākyāni, or The Wise Sayings of Lal Ded* (RAS Monograph XVII, 1920).
English is a Pratibha rendering from Grierson (archaisms lifted; sense kept).
Kashmiri romanization is Grierson's recension, lightly regularized.

Minimum ingest for this tradition: 32 vakhs (floor is 25). Ten are hero verses
(tts_key) for the collection mandala and Listen bake.
"""
from __future__ import annotations

import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/lalla_vakyani")
SLUG = "lalla_vakyani"
COLL = "Lallā Vākyāni"
PROV = (
    "English is a Pratibha rendering from Sir George Grierson & Lionel D. Barnett, "
    "*Lallā-Vākyāni* (Royal Asiatic Society, 1920 — public domain). Kashmiri follows "
    "Grierson's recension (Dharam Das Darvesh / Mukund Ram Shastri), lightly regularized. "
    "Does not follow any copyrighted modern translation."
)
NOTE = (
    "Lal Ded (Lalleshwari, Lallā Yogīśvarī, 14th c. Kashmir) spoke Kashmiri vakhs — "
    "short oral verses of recognition — from inside popular Śaiva yoga, not as a "
    "systematic treatise. Hindu and Muslim Kashmiris both keep her on the tongue."
)

# Ten hero verses (Grierson numbers) — mandala quotes + pre-baked Listen.
HEROES = {1, 3, 4, 5, 7, 48, 49, 94, 99, 103}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


# Each unit: n, title, kashmiri, translation, commentary, practice, terms, resonances
UNITS: list[dict] = [
    {
        "n": 1,
        "title": "Nothing but the Weal Remains",
        "kash": "abhyāsena layam yāte dṛśye śūnyatvam āgate /\nsārirūpaṃ śiṣyate tac chānte śūnye 'py anāmayam /\nyuhuy wopadesh ekuy, bata",
        "tr": "When by repeated practice of yoga the whole expanse of the visible universe has risen into absorption; when the qualified universe has merged in the Ether; when the ethereal Void itself has dissolved — then nothing but the Weal remains. Brahmin, the true teaching is this alone.",
        "comm": "The vakh does not climb a ladder of states to add a last prize. It subtracts until even the Void — the first shimmer of manifestation, sky mistaken for God — is allowed to go. What remains is named anāmaya, the Weal: not a pleasant mood, but consciousness without the bruise of limitation. The contested move is to refuse both the world-as-real and emptiness-as-goal. Śaiva yoga here is a controlled de-thickening: first the wide expanse is seen as emanation, then even the seeing-as-void is dropped. Lalla is not teaching nihilism. She is teaching that every named station, including śūnya, is still a costume of the nameless. The last line is a slap at scholastic pride: the doctrine is not a second thing beside this remainder. If you still have a doctrine in your hand after the Void dissolves, you have not finished the practice.",
        "prac": "Sit until the room feels like a single field. Name three layers you can drop: objects, the space they sit in, the sense of being a watcher of that space. After each drop, ask whether anything still hurts. Stay with what does not.",
        "terms": kt(
            ("anāmaya", "the unbruised; Weal — consciousness without the wound of limitation, not a heavenly aftertaste"),
            ("śūnya", "the ethereal Void; first staged emptiness, still short of the Supreme"),
            ("abhyāsa", "repeated practice that makes the visible rise back into absorption"),
        ),
        "res": res(
            ("Śiva Sūtra I.1, caitanyam ātmā", "Both end in consciousness as what remains when objects and even their absence are refused.", "The sūtra states identity; Lalla narrates the subtractive yoga that lands there."),
            ("Plotinus, Ennead VI.9", "The soul sheds form until it stands in the One beyond intellect.", "Plotinus climbs by likeness to the Good; Lalla dissolves even the Void that yoga itself produces."),
        ),
    },
    {
        "n": 2,
        "title": "Not Even Śiva Dwells There",
        "kash": "wākh man kol-akol no ate /\nmauni mudrā ati na praveś /\nrozan śiv śakti na ate /\nmāy yeli kũh ta suy wopadesh",
        "tr": "There is there no word, and no thought of mind. There is there no family of creation and no transcendence of that family. Not by vow of silence, not by mystic gestures, is there entry there. Śiva and his Śakti do not dwell there. If something remains, that is what the teaching teaches.",
        "comm": "Lalla locates the real beyond the whole toolkit of her own religion. Kula and akula, silence and mudrā, even the paired names Śiva–Śakti — all are refused as tickets. The shock is not atheism. It is that the personal God and his power still have form and name, and the remainder has neither. Entry is not an attainment produced by technique. Techniques can at best exhaust the seeker until the seeking itself is seen through. The last line is precise: the teaching is not a proposition about the remainder; the remainder is the teaching. If you still need a method to get there, you are still in the realm where methods work.",
        "prac": "Take one technique you trust — a mantra, a silence-vow, a gesture. Do it once, then set it down. Sit without a method for three minutes. Notice the itch to pick the tool back up. That itch is the kula still asking to be saved.",
        "terms": kt(
            ("kula", "the 'family': soul, matter, space, time, elements — the whole created set"),
            ("akula", "what transcends the family; still a pair-term, still not the remainder"),
            ("mudrā", "mystic attitude of the body; here refused as a door"),
        ),
        "res": res(
            ("Meister Eckhart, on Abegescheidenheit", "Even God as named must be left if the ground is to be bare.", "Eckhart detaches from creatures for God's sake; Lalla detaches from Śiva-Śakti for the unnamed Weal."),
            ("Tao Te Ching 1", "The named is not the eternal name.", "Laozi warns at the threshold of speech; Lalla names the concrete religious tools that fail."),
        ),
    },
    {
        "n": 3,
        "title": "I Found Him in My Own House",
        "kash": "lal loli drāyes lola rē /\nśēdan lūbtum dyēni kyoli rāth /\nwuchum pōluṭi panani garē /\nsuy mē rotum nēc̣atur tu sāth",
        "deva": "लल लोलि द्रायास लोल रे\nशेदान लूब्तुम द्यनि क्योलि राथ\nवुछुम पोलुटि पननि गरे\nसुय मे रोटुम निचतुर तु साथ",
        "tr": "With passionate longing I, Lalla, went forth. Seeking and searching I passed the day and night. Then I saw in my own house a learned man — and that was my lucky star and my lucky moment, when I laid hold of him.",
        "comm": "Pilgrimage is the first religion Lalla outgrows. She burns the days looking abroad, then the guru appears as her own Self in her own house — which means, in her own body-soul, not in a shrine. The contested claim is that the preceptor is not missing; the looking-elsewhere is the missing. Kashmiri Śaivism calls this pratyabhijñā: recognition, not acquisition. The 'learned man' is not a historical teacher smuggled into the lyric. He is the Self recognized as teacher, the moment the search collapses into the searcher. Lucky star and lucky moment are not astrology. They mark the suddenness: grace feels like timing because effort had been facing the wrong direction. Grasp him, she says — not admire the insight. Recognition that is not seized evaporates back into seeking.",
        "prac": "Stop the next outward search for a better state. Place a hand on your sternum. Ask, without moving: who has been looking? Stay until the looker is more obvious than the looked-for.",
        "terms": kt(
            ("panani garē", "in my own house — the body-soul as the shrine the pilgrim kept leaving"),
            ("pōluṭi", "the learned man; the Self appearing as guru in recognition"),
            ("pratyabhijñā", "recognition of what was never lost; Lalla's whole path in one turn"),
        ),
        "res": res(
            ("Luke 17:21", "The kingdom is within you, not in a geography of holy sites.", "Luke frames an announcement; Lalla frames a failed pilgrimage that accidentally succeeds."),
            ("Pratyabhijñāhṛdayam sūtra 1", "Consciousness of its own free will is the Self of all.", "Kṣemarāja states the metaphysics; Lalla tells the biographical cost of not knowing it yet."),
        ),
    },
    {
        "n": 4,
        "title": "The Lamp Blazed in the Bellows",
        "kash": "damah dam korumas daman-hālē /\nprazalyom dīpi ta nanyēyem zāth /\nanda nyūrum prakāś mbar bholum /\ngati rotum ta kurumas thaph",
        "deva": "दमह दम कोरुमस दमन-हाले\nप्रजल्योम दीपि त नन्येयम जाथ\nअंद न्यूरुम प्रकाश म्बर भोलुम\nगति रोटुम त कुरुमस थफ",
        "tr": "Slowly, slowly, I stopped my breath in the bellows-pipe of my throat. Thereby the lamp of knowledge blazed up within me, and my true nature was revealed. I winnowed my inner light forth, so that in the darkness itself I could seize the truth and hold it tight.",
        "comm": "Breath here is not wellness. It is the bellows that had been blowing the flame out. Slow the pipe, and the dim wick of knowing becomes a lamp; the lamp does not create the Self, it shows zāth, own-being, already there. Then comes the second move, easy to miss: she does not hoard the light in a private cave. She winnows it abroad until darkness itself is the place of grasping. Kashmiri yoga often stops at inner blaze. Lalla insists the blaze must suffuse the whole field, including what still looks like night. Holding tight is not clinging to an experience. It is refusing to let the old search start again once recognition has a handhold. The darkness is not the enemy after this; it is the medium in which the seized truth stays.",
        "prac": "Breathe more slowly than you think you need, for twelve breaths, attention at the throat. When a small brightness of knowing appears, do not close your eyes to keep it. Open them and see whether the room can carry it.",
        "terms": kt(
            ("daman-hāl", "bellows-pipe: the breath-channel as the instrument that either starves or feeds the lamp"),
            ("zāth", "true nature, own-being — revealed, not manufactured, when the lamp blazes"),
            ("prakāś", "inner light of consciousness; here winnowed outward until night itself holds it"),
        ),
        "res": res(
            ("Haṭha Yoga Pradīpikā 2, on prāṇāyāma", "Both treat breath as the wick-control of inner fire.", "The Pradīpikā is a ladder of techniques; Lalla tells one autobiographical blaze and its ethical sequel: winnow it into the dark."),
            ("Gospel of Thomas 24", "There is light within a person of light, and it lights up the whole world.", "Thomas states a condition; Lalla gives the somatic trigger and the seizing."),
        ),
    },
    {
        "n": 5,
        "title": "He Whose Mind Is Free of Duality",
        "kash": "par toy pan yem' tōm' māne /\ndyēn rāth yem' tōm' samān /\nyem' tōm' advay man tōpoth /\ntamiy dyuṭhuy sura-guru-nāth",
        "deva": "पर तोय पन येमि तोमि माने\nद्येन राथ येमि तोमि समान\nयेमि तोमि अद्वय मन तोपोथ\nतमिय द्युठुय सुर-गुरु-नाथ",
        "tr": "He who has deemed another and himself the same; he who has deemed the day of joy and the night of sorrow alike; he whose mind has become free from duality — he, and he alone, has seen the Lord of the chiefest of gods.",
        "comm": "Non-duality is not a theory that people are interchangeable. It is the collapse of the two-ness that makes God an object over there and pain a verdict on me. Day and night named as joy and sorrow tell you the stakes: this is not metaphysics about substances, it is the end of mood as ontology. Only then is the Lord seen — sura-guru-nāth, the teacher of gods — which means the Supreme is not seen by a purified spectator. The seer has to lose the very contrast that made seeing-a-Lord possible. The contested move is exclusivity: he alone. Lalla will not let a dualistic devotee claim the vision. Love of God as other is still night and day. The verse is a test, not a comfort.",
        "prac": "When the next mood swing arrives, name it day or night without correcting it. Then look for the one to whom it is happening. Stay until the looker is not on either side of the swing.",
        "terms": kt(
            ("advaya", "non-dual; the mind no longer split between self/other, joy/sorrow"),
            ("sura-guru-nāth", "Lord of the chiefest of gods — Lalla's name for the Supreme beyond the personal deity"),
        ),
        "res": res(
            ("Aṣṭāvakra Gītā 1.11", "You are not the body; you are awareness — the same refusal of two-ness.", "Aṣṭāvakra speaks to a king already able to hear; Lalla speaks as a woman who had to burn the pilgrimage first."),
            ("Heraclitus B57–B67", "Day and night are one.", "Heraclitus names the logos of opposites; Lalla makes the pairing a criterion of vision."),
        ),
    },
    {
        "n": 6,
        "title": "Alive, They Have Gained Release",
        "kash": "yimav cyun tim zīvanē /\ncidānanda jñāna-rūpah prakāś /\nwekmis saṃsāras pānthas /\natah gandih ṭhīth-ṭhīth dith",
        "tr": "They who have gained the Knowledge-light of that Self which is compact of pure spirit and bliss — they, while still alive, have gained release from earthly births. But to the tangled net of continual rebirth, ignorant fools have added knot by knot in hundreds.",
        "comm": "Jīvanmukti is stated without apology: release is not a post-mortem diploma. The Knowledge-light is not information about the Self; it is the Self as light, cidānanda, knowing-bliss. The second half is cruel on purpose. The unreleased do not merely fail to cut the net. They keep knotting it — each righteous effort, each identity, each next birth-plan. Lalla's fools are often the religiously busy. The verse splits the world into two crafts: those who see, and those who macramé saṃsāra.",
        "prac": "List three 'good' efforts you are using to become free later. For each, ask whether it is a cut in the net or another knot. Drop one knot today without replacing it.",
        "terms": kt(
            ("jīvanmukti", "liberation while alive; not a result that waits on death"),
            ("cidānanda", "consciousness-bliss, the Self as light rather than as an object of light"),
        ),
        "res": res(
            ("Bhagavad Gītā 5.19", "Even here, birth is overcome by those whose mind is equal.", "The Gītā ties equality to the gunas; Lalla ties it to a light that makes further knotting look insane."),
            ("Śiva Sūtra I.2", "Knowledge itself can bind.", "Both warn that knowing-about is not the Knowledge-light."),
        ),
    },
    {
        "n": 7,
        "title": "Thou Art I, I Am Thou",
        "kash": "nātha nā pan nā par zānum /\nsadāy lōdum yih kōdeh /\nṭhūk ṭhūk myul nā zānum /\nṭhūk kus ṭhūk kus chuh sandeh",
        "deva": "नाथ ना पन ना पर जानुम\nसदाय लोडुम यिह कोदेह\nठूक ठूक म्युल ना जानुम\nठूक कुस ठूक कुस छुह संदेह",
        "tr": "Lord, I have not known myself or other than myself. Continually I have mortified this vile body. That Thou art I, that I am Thou, that these are joined in one — I knew not. It is doubt to say 'Who am I?' and 'Who art Thou?'",
        "comm": "The confession is not humility theater. It is a diagnosis of the whole path of self-torture: she wore the body out by works because she did not know the identity. 'Thou art I / I am Thou' is not poetry for union of two lovers. It is the collapse of the grammatical two. The last line is the blade. The famous spiritual questions — who am I, who is God — are named as sandeh, doubt, the fatal doubt. Inquiry that keeps two pronouns in play is still the disease. Kashmiri recognition does not answer 'who am I?' with a better definition. It ends the need to ask by ending the split that made the question. Mortification without this is just another knot in verse 6's net.",
        "prac": "Write 'Who am I?' and 'Who art Thou?' on paper. Sit with both until they feel like one confusion, not two noble questions. Then stop writing answers. Feel the body that was being punished to solve them.",
        "terms": kt(
            ("sandeh", "doubt — here the very questions 'who am I / who are You' as the bondage"),
            ("nātha", "Lord; the addressee who is then shown to be the speaker"),
        ),
        "res": res(
            ("Balyānī / Ibn ʿArabī, Know Yourself", "He who knows himself knows his Lord — identity, not resemblance.", "The Sufi treatise argues; Lalla confesses the years of mortification that the ignorance cost."),
            ("Chāndogya Upaniṣad 6.8, tat tvam asi", "That thou art.", "Uddālaka teaches a son by stages; Lalla accuses her own prior practice of having missed the sentence."),
        ),
    },
    {
        "n": 8,
        "title": "By Whatever Name He Bear",
        "kash": "śiv wā keśev wā jina wā /\nkamalaja-nāth nām dōram yuh /\nml abali kōstan bhawa-rōg /\nwā su wā su wā su wā",
        "tr": "Let Him bear the name of Śiva, or of Keśava, or of the Jina, or of the Lotus-born Lord, whatever name he bear. May he take from me, sick woman that I am, the disease of the world — whether He be he, or he, or he, or he.",
        "comm": "This is not modern pluralism pasted onto the fourteenth century. It is a sick woman asking any true name to do one job: take bhava-roga, the disease of becoming. Śiva, Viṣṇu, Jina, Brahmā are not ranked. They are alternative masks of the one who can actually cure. The last stutter — whether He be he or he or he — is theologically serious. If the remainder of verses 1–2 has no name, then clinging to one sectarian name is just another form of the disease. Lalla will use whatever name opens the door, and she will not pretend the door belongs to the name.",
        "prac": "Speak one divine name you actually use. Then speak one you refuse. Ask both to take the same disease — the itch to become someone. Notice which name your pride defends.",
        "terms": kt(
            ("bhava-roga", "the disease of worldly becoming; saṃsāra as illness, not as scenery"),
            ("Keśava", "Viṣṇu; here one interchangeable name of the nameless healer"),
        ),
        "res": res(
            ("Bhagavad Gītā 7.21", "Whatever form a devotee worships with faith, I make that faith steady.", "Kṛṣṇa claims the other forms as his; Lalla asks any form to perform the cure and will not decide in advance."),
            ("Qurʾān 17:110", "Call upon Allah or the Merciful — to Him belong the most beautiful names.", "Both refuse name-wars; Lalla's tone is medical, not liturgical."),
        ),
    },
    {
        "n": 9,
        "title": "When Mind Disappeared, Nothing Was Left",
        "kash": "sūra gol ta prakāś āv zūnē /\nzandēr gol ta motuy cith /\ncith gol ta kẽh-ti nā kune /\ngay khūr khāwak nabh vemrith",
        "tr": "When the sun disappeared, then came the moonlight. When the moon disappeared, then only mind remained. When — absorbed in the Infinite — mind disappeared, then nothing anywhere was left. Earth, ether, and sky all took their departure.",
        "comm": "Sun and moon are not astronomy. In this yoga they are the two poles of the central channel, heat and nectar, right and left, until even those lights go out and only citta is left as a witness. Then the witness is taken. The last inventory — earth, ether, sky — is the world-picture packing its bags. Lalla is not describing a faint. She is describing the same remainder as verse 1, now told as a sequence of vanishings instead of a doctrinal punchline. If you stop at moonlight, you have a beautiful meditation. If you stop at mind, you have philosophy. The vakh is only finished when there is nowhere left to stand, including the standing of mind.",
        "prac": "Watch one sunset of attention: outer light, then inner glow, then the watcher. Let each go when it goes. Do not rebuild a world in the gap.",
        "terms": kt(
            ("zūn", "moonlight; the upper nectar-pole after solar fire recedes"),
            ("cith", "mind as last witness, still too much to be the Infinite"),
        ),
        "res": res(
            ("Māṇḍūkya Upaniṣad, turīya", "Waking, dream, and sleep vanish into the fourth.", "The Upaniṣad maps states; Lalla maps yogic lights until even the mapper is gone."),
            ("Pseudo-Dionysius, Mystical Theology", "The ascent leaves behind every light and every word.", "Dionysius climbs a hierarchy; Lalla watches sun, moon, and mind fail in that order."),
        ),
    },
    {
        "n": 14,
        "title": "Śiva Is the Horse",
        "kash": "śiv gur tu keśav palānas /\nbrahmā pāyiran ṭolases /\nyogi yoga-kali parzānes /\nkus dev aswāwār peth cades",
        "tr": "Śiva is the horse. Zealously employed upon the saddle is Viṣṇu, and upon the stirrup, Brahmā. The yogi, by the art of his yoga, will recognize who is the god that will mount upon him as the rider.",
        "comm": "Even Śiva-tattva, first flash of the Supreme in the universe, is only the horse. The trimūrti are tack. The question is who rides. Lalla will not let theology stop at a named God, however supreme in the manuals. The yogi's job is recognition of the rider — the nameless of verse 15 — not better worship of the mount. The image is almost comic: the whole pantheon as furniture of a journey whose passenger has not been admitted. That comedy is the teaching.",
        "prac": "Name the God or principle you actually serve. Ask: is this the rider, or the horse I have decorated? Do not answer with a better name. Wait for the sense of being ridden.",
        "terms": kt(
            ("Śiva-tattva", "first phase of the Supreme in manifestation — still a horse, not the rider"),
            ("asvār", "the rider; the unnamed God who mounts the whole theistic apparatus"),
        ),
        "res": res(
            ("Kaṭha Upaniṣad 1.3", "The Self is the rider, body the chariot.", "The Upaniṣad moralizes the team; Lalla puts even Śiva in the traces."),
            ("Verse 15 of this recension", "The rider is named as the unobstructed sound in the Void.", "14 asks; 15 answers. Keep them together."),
        ),
    },
    {
        "n": 15,
        "title": "The God Who Has No Name",
        "kash": "anāhath kha-swarūph śūnyas /\nyes nāv na ranga na goth na rūph /\naham-vimarśe nāda-binduy yes won /\nsuy dev aswāwār peth cades",
        "tr": "The ever-unobstructed sound, the principle of absolute vacuity, whose abode is the Void; which has no name, nor colour, nor lineage, nor form; which they declare is transformed into Sound and Dot by its own reflection on itself — that alone is the god that will mount upon him.",
        "comm": "Here is the rider of verse 14. Anāhata: the unstruck sound, OM as vibration that no one utters. Its home is the Void in the forehead's thousand-petaled rest. Nothing can be predicated — and then Lalla predicates the one process that matters: aham-vimarśa, I-consciousness reflecting on itself, splitting into nāda and bindu, cry and point of light. The Supreme is not a mute blank. It is self-aware emptiness that appears as sound and spark when yoga first glimpses it. The god who mounts is not a person climbing onto a horse. It is this self-reflection taking the yogi as its vehicle.",
        "prac": "Listen for the hum that is there when you are not humming. Do not turn it into a mantra you own. Let it be unstruck. If a tiny sense of 'I' flares, notice it as the Dot, not as you.",
        "terms": kt(
            ("anāhata", "unstruck / unobstructed sound; the syllable that utters itself"),
            ("nāda-bindu", "sound and point of light; first tremor of the Supreme noticing itself"),
            ("aham-vimarśa", "I-reflection; consciousness bending back upon itself"),
        ),
        "res": res(
            ("Vijñāna Bhairava, on the gap between breaths", "The Void is entered at a seam, not as an object.", "The Tantra gives 112 doors; this vakh names the one rider behind all doors."),
            ("Lalla vakh 1", "The Void itself must dissolve into the Weal.", "15 still speaks the language of Void and sound; 1 will not let you camp there."),
        ),
    },
    {
        "n": 40,
        "title": "The Mantra of Silence",
        "kash": "man puśu ta bāwa-icchā puśūn /\nbhāwak kusum lāg'zes pūze /\nswānanda-pūr dizes zalaci dōm /\nmauna-mantra śaṅkar-swātma wūze",
        "tr": "The mind is the man, and pure desire is the woman, that bring wreaths. Offer the flowers of devotion in His worship. Make the nectar of the moon stream over Him as ritual water. By the mystic formula of silence the Śiva-Self will become manifest.",
        "comm": "Formal pūjā is rewritten as inner anthropology. Mind and will are the two who string the garland; devotion's flowers are not bought; the moon-nectar is the sahasrāra's own drip, not Ganges water in a cup. Then the only mantra left is mauna, silence. The Śiva-Self does not appear because you said the right syllables. It appears when the verbal engine stops pretending to be worship. Lalla is not anti-ritual. She is anti-outsourcing: if the rite is not happening as mind, will, and silence, it is costume.",
        "prac": "Offer one ordinary act — pouring water, lighting a lamp — without words. Let the silence be the formula. See whether devotion is in the gesture or in the commentary you want to add.",
        "terms": kt(
            ("mauna-mantra", "the formula of silence; not a quieter word, the end of wording as worship"),
            ("Śaṅkara-swātma", "the Śiva-Self; the deity as one's own ātman, not as a statue"),
        ),
        "res": res(
            ("Īśāvāsya Upaniṣad 1", "All this is to be covered by the Lord — worship as covering, not as transaction.", "The Upaniṣad legislates a stance; Lalla recasts the whole pūjā kit as psychology."),
            ("The Cloud of Unknowing", "Beat upon the cloud with a dart of love, not with many words.", "Both demote speech; the Cloud keeps a God-over-there; Lalla wants the Śiva-Self to show as self."),
        ),
    },
    {
        "n": 46,
        "title": "He Is Nigh to Thee",
        "kash": "suy chuh hasān suy chuh treśān /\nsuy chuh ṭhūkān suy chuh jṛmbān /\nsuy chuh tīrthas nērith nērith /\nparzān tamiy zi chuh nizh nēṛe",
        "tr": "He it is who laughs, who sneezes, who coughs, who yawns. He it is who ceaselessly bathes in holy pools. He it is who is an ascetic, naked from year's end to year's end. Recognize that verily He is nigh to thee.",
        "comm": "The kingdom is not within as a secret feeling. It is the one who is already doing your most embarrassing physiology. Laugh, sneeze, cough, yawn — the verse picks acts no one claims as spiritual. Then it adds the professional holy man: the pilgrim and the naked ascetic. Same He. The contested claim is identity in the trivial, not only in the sacred career. If you only find God in the ascetic's nakedness, you have missed him in the yawn. Recognition (parzān) is the verb. Proximity is not spatial. He is nigh because he is the one living your life, including the life you use to look for him.",
        "prac": "The next time you yawn or laugh, do not spiritualize it. Just notice: this too is happening in the same awareness that wants a holy state. Stay for one breath in that sameness.",
        "terms": kt(
            ("parzān", "recognize — not infer, not believe; catch Him in the act already underway"),
            ("nizh nēṛe", "nigh to thee; nearness as identity, not as approaching a shrine"),
        ),
        "res": res(
            ("Vijñāna Bhairava, yuktis on ordinary acts", "Sneezing, laughter, and sudden fear are listed as doors.", "The Tantra catalogues techniques; Lalla collapses pilgrim and yawn into one He."),
            ("Luke 17:21", "The kingdom of God is within you.", "Shared nearness; Lalla insists on coughs, not only on interiority."),
        ),
    },
    {
        "n": 47,
        "title": "A Lake Too Small for a Mustard Seed",
        "kash": "yeth saras sars-phol nā vētsy /\ntath sari nēkhaliy pān cen /\nmṛg śṛgāl gaṇḍ zala-hasti /\nzen nā ten ta totuy pen",
        "tr": "It is a lake so tiny that a mustard seed finds no room in it. Yet from that lake does every one drink water. And into it do deer, jackals, rhinoceroses, and sea-elephants keep falling, falling, almost before they have time to be born.",
        "comm": "The universe as grand is the first joke. Compared with the Self it is a puddle that cannot hold a mustard seed — and still everyone drinks from it, and every beast of appetite falls in before it has even finished being born. Life, measured against the Weal, has no duration. Rebirth is not a long epic. It is a slapstick of falling. The verse does not say the world is evil. It says it is negligible, and that neglect is the beginning of freedom. Take the world as enormous and you will organize a religion to manage it. Take it as this lake and the panic looks overproduced.",
        "prac": "Hold a mustard seed or a grain of rice. Let it be the whole visible world. Drink a sip of water and notice the mismatch: you live on what cannot contain you. Walk away without solving it.",
        "terms": kt(
            ("sar", "lake; here the cosmos as a puddle against the Self"),
            ("sars-phol", "mustard seed; the standard Indian atom of smallness, still too big for this lake"),
        ),
        "res": res(
            ("Chāndogya Upaniṣad 6.12", "The banyan's seed is invisible, yet the tree is that.", "Uddālaka uses smallness as essence; Lalla uses smallness as insult to cosmic pretension."),
            ("Ecclesiastes 1", "All is vapour, a chasing of wind.", "Both deflate duration; Qoheleth stays in lament, Lalla in a comic menagerie."),
        ),
    },
    {
        "n": 48,
        "title": "Bolts Were on His Door",
        "kash": "lal lōh lāyis ṭaḍan ta gwāran /\nwuṣum hyotumas toś rōṭumas baran /\nmē-ti kalganeye zi zāmas tath",
        "deva": "लल लोह लायिस टडन त ग्वारन\nवुछुम ह्योतुमस तोश रोटुमस बरन\nमे-ति कलगनिये जि जामस तथ",
        "tr": "I, Lalla, wearied myself seeking for Him and searching. I laboured and strove even beyond my strength. I began to look for Him, and lo, I saw that bolts were on His door. And even in me, as I was, longing became fixed — and there, where I was, I gazed upon Him.",
        "comm": "Effort reaches a locked door, and the lock is the point. Human striving cannot force the Supreme; the barred door is grace's first honest appearance. Then the verse turns: she does not go home defeated. She stands in the longing itself, unimproved, and the gazing happens there. The He who was behind bolts is seen in the one who stopped picking the lock. This is not quietism as laziness. It is the end of spiritual athletics. Kashmiri teaching often says recognition cannot be produced. Lalla shows the production failing in the first person, which is the only way the teaching becomes true. Longing that remains after effort dies is not a feeling to cultivate. It is what is left when there is nothing left to do — and that remainder sees.",
        "prac": "Name one spiritual effort you are using as a crowbar. Set it down for one hour. Stay in the unfinished wanting without improving it. If vision comes, it will come where you actually are, not where the effort was aiming.",
        "terms": kt(
            ("baran", "bolts on the door; the failure of force as the first true seeing"),
            ("kalgan", "longing fixed in the unimproved person; desire after the death of technique"),
        ),
        "res": res(
            ("Lalla vakh 3", "The same search, earlier: He was in the house.", "3 finds the guru inside; 48 finds the barred door and looks anyway. Both kill pilgrimage, from two sides."),
            ("The Cloud of Unknowing", "You cannot think your way to God; beat on the cloud with love.", "The Cloud still strikes; Lalla's bolts teach her to stop striking and gaze from the longing."),
        ),
    },
    {
        "n": 49,
        "title": "Then the Name of Lalla Spread",
        "kash": "mal wondi zālum /\nhṛdayas kalgan zālum /\nteli lal nāv drām /\nyeli ḍali trōvumas taph",
        "deva": "मल वोंदि ज़ालुम\nहृदयस कलगन ज़ालुम\nतेलि लल नाव द्राम\nयेलि डलि त्रोवुमस तफ",
        "tr": "Foulness I burnt from my soul. My heart, with its desires, I slew. And then did my name of Lalla spread abroad, when I sat just there, with bended knee.",
        "comm": "Reputation is the last thing the verse is about, and the first thing listeners grab. The name spreads after the heart-desire is slain and the body sits — ḍali, bended knee, humility as posture, not as brand. She does not go out to become Lalla. She burns mal, the soul's grime, and the world starts saying the name. Sequence is doctrine: purification, then stillness, then the name as echo, never as project. Sitting 'just there' points back to verse 48's 'where I was.' The prophetess is a by-product of having nowhere else to go. If you reverse the order — spread the name, then try to sit — you get a career.",
        "prac": "Do not improve your name today. Burn one small falseness you use to be seen. Then sit as you are, knees soft, for five minutes, with no audience, including the inner one.",
        "terms": kt(
            ("mal", "foulness / stain of the heart; what must burn before a name is true"),
            ("ḍali", "bended knee; the posture of waiting after effort has died"),
        ),
        "res": res(
            ("Tao Te Ching 7", "The sage puts himself last and is first.", "Laozi states a paradox of rulership; Lalla states a biography of a woman whose fame arrived as residue."),
            ("Matthew 6:6", "Pray in secret, and your Father who sees in secret will reward.", "Both hide the act; Lalla's 'reward' is a name she did not go seeking."),
        ),
    },
    {
        "n": 50,
        "title": "Seven Times I Saw the World a Void",
        "kash": "trāy nengi sarah sar saw /\nakh nengi saras anihajay /\nharamukh kausar akh sūm saras /\nsati nengi saras śūnyākār",
        "tr": "Three times I remember a lake overflowing. Once I remember seeing in the firmament the only existing place. Once I remember seeing a bridge from Harmukh to Kausar. Seven times I remember seeing the whole world a void.",
        "comm": "Memory of former lives is not offered as occult credential. It is what knowledge does to time: kalpas become countable because they are no longer owned. Harmukh and Kausar are Kashmir's own mountain and lake, turned into a bridge across dissolution. The last count — seven voids — is the punch. The world has already been empty, repeatedly. Your present solidity is a local habit. Lalla speaks as someone who has watched the set struck and rebuilt. That is why verse 47's puddle is funny rather than tragic.",
        "prac": "Look at a landscape you think of as permanent. Say: I have seen this gone. Not as a belief. As a permission to hold it more lightly for the rest of the walk.",
        "terms": kt(
            ("śūnyākār", "having the form of void; the world remembered as already dissolved"),
            ("kalpa", "a day of Brahmā; the unit of cosmic forgetting Lalla claims to remember across"),
        ),
        "res": res(
            ("Bhagavad Gītā 8.17–19", "Those who know day and night of Brahmā see the worlds dissolve and return.", "Kṛṣṇa teaches cosmology; Lalla reports it as autobiographical memory."),
            ("Marcus Aurelius 9.28", "The universe is transformation.", "The emperor generalizes; Lalla counts lakes."),
        ),
    },
    {
        "n": 51,
        "title": "Hardly Is Śiva to Be Found",
        "kash": "śōbhawān ras-bhar zāy mājē /\nwombas dith dith tīḍen pẽd /\nbaras peth peth āy ta wōth /\ndurlabh śiva, tas dhyān kar",
        "tr": "Comely and full of sap they were born from the mother, after causing many a pang to her womb. Again and again they came and waited at that door. Hardly, in sooth, is Śiva to be found. Meditate therefore on the teaching.",
        "comm": "Birth is gorgeous and expensive, and still the soul lines up at the same door again. The refrain that will bind the next verses — durlabha śiva — is not pessimism. It is rationing: a human birth is the rare chance, and most of it is spent being born prettily. Meditate on the teaching means: stop treating incarnation as a spa. The womb-pang is the price of a ticket that people then forget they hold.",
        "prac": "Remember one difficulty of being in a body today — hunger, fatigue, a scar. Thank it as the price of a ticket. Then spend ten minutes of the ticket on the teaching, not on improving the body's display.",
        "terms": kt(
            ("durlabha", "hard to find; Śiva as rare, not as universally obvious feeling"),
        ),
        "res": res(
            ("Dhammapada 182", "Hard is it to obtain birth as a human.", "Both ration incarnation; the Buddhist verse aims at the path, Lalla at Śiva who hides in the obvious."),
            ("Lalla 48", "The door is bolted.", "51 waits at a birth-door; 48 at God's door. Same queue, two meanings."),
        ),
    },
    {
        "n": 52,
        "title": "The Same Rock",
        "kash": "yih śīl chuh pīṭh ta pahan /\nyih śīl chuh pṛthvī-khaṇḍ /\nyih śīl chuh myāni grāṭas /\ndurlabh śiva, tas dhyān kar",
        "tr": "The same rock that serves for a pedestal or for a pavement is really but part of a district of the earth. Or the same rock may become a millstone for a handsome mill. Hardly, in sooth, is Śiva to be found. Meditate therefore on the teaching.",
        "comm": "Function is not essence. Pedestal, paving-stone, millstone — one rock, three careers, none of them the stone. Śiva is missed the way the rock is missed: we worship the use. Meditation on the teaching is a refusal to let role exhaust being. The mill that grinds your life is still the mountain.",
        "prac": "Pick an object you use (phone, cup, doorstep). Name three jobs it could have. Then look at it as none of those jobs. That looking is the verse.",
        "terms": kt(
            ("śīl", "rock; substance outlasting the offices we assign it"),
        ),
        "res": res(
            ("Chāndogya 6.1, clay and pots", "By knowing one lump of clay, all that is made of clay is known.", "Uddālaka teaches material cause; Lalla teaches that uses hide the cause."),
            ("Zhuangzi, the useless tree", "Use is what gets you cut down.", "Zhuangzi saves the tree by uselessness; Lalla saves the rock by seeing through use."),
        ),
    },
    {
        "n": 53,
        "title": "The Sun Does Not Glow for the Good Land Only",
        "kash": "sūra kina wuth nā prath diśi /\nsūra kina wuth nā khāṣi bhūmi /\nvaruṇa kina ath nā prath garē /\ndurlabh śiva, tas dhyān kar",
        "tr": "Does not the sun cause everything to glow in every region? Does it cause only each good land to glow? Does not Varuṇa enter into every house? Hardly, in sooth, is Śiva to be found. Meditate therefore on the teaching.",
        "comm": "Election is the error. The sun does not pick virtuous real estate. Water does not skip the unclean house. If Śiva is like these, then the search for a special precinct is already the miss. Durlabha then means: hard to find because too evenly given, not because scarce. People look in the 'good land' of peak experience and holy company, while the ordinary house is already wet with Varuṇa.",
        "prac": "Stand in the least sacred corner of your home. Admit: if the sun reaches here, the teaching reaches here. Do not upgrade the corner. Receive it.",
        "terms": kt(
            ("Varuṇa", "lord of waters; here the permeating wetness that respects no threshold"),
        ),
        "res": res(
            ("Matthew 5:45", "He makes his sun rise on the evil and on the good.", "Shared indiscriminate giving; Jesus moralizes neighbors, Lalla moralizes the search for a special site."),
            ("Īśāvāsya 1", "All this is covered by the Lord.", "Both deny vacant lots; Lalla asks two rhetorical questions to shame the seeker."),
        ),
    },
    {
        "n": 54,
        "title": "The Same Woman",
        "kash": "yih zanan chē māj dits dūdh /\nyih zanan chē vōhni nēthar /\nyih zanan chē ṭhag jān khyāv /\ndurlabh śiva, tas dhyān kar",
        "tr": "The same woman is a mother, and gives milk to her babe. The same woman, as a wife, has her special character. The same woman, as a deceiver, ends by taking thy life. Hardly, in sooth, is Śiva to be found. Meditate therefore on the teaching.",
        "comm": "Śakti is not a safe mother. She nurses, she binds in marriage, she kills. One woman, three offices — like the rock of verse 52, like the sun of 53. To find Śiva you have to stop hiring the Goddess for only the milk. The verse is not misogyny. It is a warning against sentimental Śāktism: the power that feeds you is the power that ends you, and both are the same. Meditation is learning to meet that sameness without picking a favorite mask.",
        "prac": "Think of a force in your life that has both nourished and threatened you — work, love, the body. Stop splitting it into two gods. Bow once to the undivided woman.",
        "terms": kt(
            ("śakti", "power in act; here the one woman who nurses, weds, and slays"),
        ),
        "res": res(
            ("Śvetāśvatara Upaniṣad 4.10", "Know māyā as Prakṛti, and the Lord as māyin.", "Both refuse a tame feminine; the Upaniṣad theorizes, Lalla gives three roles in one body."),
            ("Heraclitus, war is father and king", "The same force feeds and destroys.", "Heraclitus praises strife; Lalla keeps the tenderness of milk inside the danger."),
        ),
    },
    {
        "n": 71,
        "title": "Why Did You Sink in That Ocean?",
        "kash": "māyē kith gaṭkh bhawa-saras /\nūṭh wath tsāṭith āy andh-kūp /\nkāl peth yama-dūt kṛṣi nith /\nmaraṇa-bhay kas nēri tath",
        "tr": "In thy illusion why did you sink in the stream of the ocean of existence? When you had destroyed the high-banked road, there came before you the slough of spiritual darkness. At the appointed time Yama's apparitors will drag you off in woeful plight. Who can take from you the fear of death?",
        "comm": "The ocean is optional, that is the insult. You sank, you cut the causeway, you chose the slough. Death-fear is not a natural given. It is the interest on that choice. Who can take it from you? Not a palliation, not a heaven-policy. Only the recognition that the sinker was never the Self who cannot drown. Lalla will answer this in later vakhs (the dawn, the Friend, the cotton-cloth). Here she lets the question hang as a hook in the throat.",
        "prac": "When fear of death appears, do not soothe it. Ask Lalla's question: why did I sink? Answer with one concrete clinging, not with a philosophy. Loosen that clinging one notch.",
        "terms": kt(
            ("bhawa-sar", "ocean of becoming; existence as a current you can fall into"),
            ("yama-dūt", "Death's messengers; the unarguable appointment"),
        ),
        "res": res(
            ("Kaṭha Upaniṣad I, Naciketas", "Death is the teacher; fear is the unasked question.", "Naciketas chooses to ask; Lalla accuses the listener of having already fallen."),
            ("Lalla 73 and 75", "The same refrain: who takes the fear of death?", "A sequence, not a slogan. Stay for the answers."),
        ),
    },
    {
        "n": 73,
        "title": "Which of These Is Lasting?",
        "kash": "rāj cāmara chatra rath siṃhās /\nsukh kēl nāṭya tūla-śayyā /\nyith saṃsāras kyā chuh sthir /\nmaraṇa-bhay kith nēri tath",
        "tr": "A royal fly-whisk, sunshade, chariot, throne; happy revels, the pleasures of the theatre, a bed of cotton down — bethink you which of these is lasting in this world. And how can it take from you the fear of death?",
        "comm": "Luxury is listed as a failed afterlife insurance. None of it is lasting, and therefore none of it can lift maraṇa-bhaya. The theatre is especially sharp: even performed joy is in the catalogue of toys. Lalla is not an ascetic snob. She is doing subtraction again. If it cannot meet death, it is not medicine. Keep it as furniture if you like. Do not ask it to save you.",
        "prac": "Pick the comfort you most use against dread (a plan, a purchase, a show). Enjoy it once honestly as comfort. Then admit it cannot take the fear. Look for what can.",
        "terms": kt(
            ("maraṇa-bhaya", "fear of death; the test every pleasure fails in this cluster of vakhs"),
        ),
        "res": res(
            ("Ecclesiastes 2", "I built, I planted, I gathered — all vapour.", "Qoheleth inventories from the throne; Lalla inventories and then asks about death-fear directly."),
            ("Epictetus, Enchiridion 1", "Some things are up to you.", "Stoic triage; Lalla's triage is harsher: even the royal kit is not up to the fear."),
        ),
    },
    {
        "n": 75,
        "title": "Pierce Through the Sun's Disk",
        "kash": "karm dwy kāraṇ trē /\ntith kunḍala-yoga abhyās /\nparas lōkas labhakh mānak /\nūṭh khaś sūra-bimba tsāṭ",
        "tr": "Works two there are, and causes three. On them practise the kumbhaka-yoga. Then in another world you will gain the mark of honour. Arise, mount, pierce through the sun's disk. Then will the fear of death flee from you.",
        "comm": "Here the death-fear question gets a yogic answer, not a moral one. Kumbhaka, the held breath, is the mount. Piercing the solar disk is the old image of exit through the brahmarandhra, the crown — not suicide, but the path the breath takes when it is no longer a servant of the body's panic. Honour in another world is almost sarcastic beside the last command: get up, climb, pierce. Lalla will not soothe. She gives a gate. The fear flees because the one who feared was the one who had never left the disk of ordinary sun, ordinary time.",
        "prac": "One round only: inhale, hold just until fear of the hold appears, exhale. At the hold, imagine the ordinary sun as a lid. Do not force. Notice the fear as a lid-guardian, not as truth.",
        "terms": kt(
            ("kumbhaka", "the held breath; yoga's pause in which the solar lid can be pierced"),
            ("sūra-bimba", "the sun's disk; the last visible seal of limited life"),
        ),
        "res": res(
            ("Īśāvāsya 15", "The face of truth is covered with a golden lid.", "Both pierce a solar cover; the Upaniṣad prays Pūṣan to open it, Lalla tells you to climb."),
            ("Haṭha Yoga Pradīpikā on kumbhaka", "Retention as the stair to rāja yoga.", "Manual vs vakh: one catalogues, one commands in the second person against death-fear."),
        ),
    },
    {
        "n": 78,
        "title": "Who Sleeps, and Who Is Awake?",
        "kash": "kus chuh nendri kus chuh jāgān /\nkyāh sar chuh rōzān tsāṭān /\nkyāh dīzi haras pūzā /\nkyāh pad labakh param",
        "tr": "Who is he that is wrapped in sleep, and who is he that is awake? What lake is that which continually oozes away? What is that which a man may offer in worship to Hara? What is that supreme station to which you will attain?",
        "comm": "A riddle-vakh, four questions, answered in the following verse in Grierson: mind sleeps and, past the kula, wakes; the five organs are the leaking lake; silence (or the mind itself) is the offering; the station is the leftover Weal. Even without the answer-verse, the form matters. Lalla teaches by interrogation, like a Upanishadic father, but in the market tongue. If you answer too fast, you have filled the leak with concepts. The questions are the practice.",
        "prac": "Hold the four questions in order, one minute each, without answering. Let the leaky lake be felt as attention running out the senses. Offer that noticing to Hara without a gift in your hand.",
        "terms": kt(
            ("Hara", "Śiva as seizer of what is offered; here the one who can receive a non-object"),
            ("nendri / jāgān", "asleep / awake — not bed-states, two positions of mind toward the kula"),
        ),
        "res": res(
            ("Praśna and Kena Upaniṣads", "Wisdom as a battery of questions.", "Sanskrit school dialogue; Lalla's riddle is meant to be carried in the mouth by anyone."),
            ("Gospel of Thomas 2", "Let the one who seeks not stop until he finds.", "Both keep the seeker in motion; Thomas promises rest, Lalla promises a station you cannot name in advance."),
        ),
    },
    {
        "n": 93,
        "title": "I, Lalla, Am Ever New",
        "kash": "ātmā nōwuy canda nōwuy /\nzalamay dyuṭkum nāwam-nōwuy /\nyēna petha lali mē tan man nōwom /\ntana lal lōh nāwam-nōwuy chuh",
        "tr": "The soul is ever new and new; the moon is ever new and new. So saw I the waste of waters ever new and new. But since I, Lalla, scoured my body and my mind, I, Lalla, am ever new and new.",
        "comm": "Novelty is usually saṃsāra's trick: new bodies, new moons, new floods. Lalla claims a different newness — the scoured self, illusion washed off, so that 'Lalla' is no longer a repeating costume. The moon was always the same moon waxing. The soul was always the same soul transmigrating. After the scouring, the sameness is known, and that knowing is the only real new. The verse steals the world's favorite adjective and baptizes it.",
        "prac": "Wash your face as if washing the mind. Say: not a new me, the same me without yesterday's grime. Go into the next hour as that.",
        "terms": kt(
            ("nāwam-nōwuy", "ever new; first the world's recycling, then recognition's freshness"),
        ),
        "res": res(
            ("2 Corinthians 5:17", "If anyone is in Christ, new creation.", "Both claim a newness that is not costume; Paul locates it in Christ, Lalla in scoured body-mind."),
            ("Lalla 50", "She has already seen the waste of waters.", "50 remembers dissolutions; 93 becomes the one who is new after them."),
        ),
    },
    {
        "n": 94,
        "title": "From Without, Enter the Inmost Part",
        "kash": "goran wonunam kunuy watsun /\nnebra dopnam andar āsyun /\nsuy gam lali wōkh ta watsun /\ntaway hyotum nanga natsun",
        "deva": "गोरन वोनुनम कुनुय वत्सुन\nनेबर दोपनम अंदर आस्युन\nसुय गम ललि वोख त वत्सुन\nतवय ह्योतुम नंग नत्सुन",
        "tr": "My teacher spoke to me but one precept. He said: from without, enter the inmost part. That became a rule and a precept for me — and therefore naked I began to dance.",
        "comm": "One precept, not a curriculum. Outer world counted as illusion, thought restricted to the inner Self — and the biographical explosion is nudity and dance, the tāṇḍava of a woman who has stopped dressing for the world because the world has been seen through. Modern readers want this to be feminism or scandal. Lalla wants it to be ontology: when externals are priced at zero, cloth is just another external. The dance copies Śiva's cosmic dance not as performance art but as surrendered identity. She does not recommend exhibition. She reports what recognition did to shame. If your 'inner turn' still manages a reputation, it is not this precept yet.",
        "prac": "For one hour, drop one outer covering you use to be someone — a tone of voice, a title, an outfit of competence. Do not replace it. Notice the impulse to dance or to hide. Both are information.",
        "terms": kt(
            ("watsun", "precept / vakh; here the single word that undoes the rest"),
            ("nanga natsun", "naked dance; tānḍava as the body's confession that the outer has no further claim"),
        ),
        "res": res(
            ("Śiva as Naṭarāja", "The cosmos is his dance; the devotee who knows this joins it.", "Mythic icon; Lalla's dance is a Kashmiri woman's actual abandoned clothing."),
            ("Milarepa, songs of the cotton-clad", "Another saint whose garment became a teaching.", "Milarepa keeps a cloth; Lalla drops even that. Divergence is the point."),
        ),
    },
    {
        "n": 97,
        "title": "For a Moment, Draupadī",
        "kash": "akh tsūj dyuṭum nār-dān prazalān /\nakh tsūj dyuṭum nā nār nā dhuh /\nakh tsūj dyuṭum pāṇḍavēn hinz māj /\nakh tsūj dyuṭum krum-hinz pōph",
        "tr": "For a moment I saw a cooking-hearth ablaze. For a moment I saw neither fire nor smoke. For a moment I saw the mother of the Pāṇḍavas. For a moment I saw an aunt of a potter's wife.",
        "comm": "Status is a flicker. Empress of the epic and potter's aunt occupy the same instant-theatre of rebirth. The hearth blazes and is gone, fire and smoke alike. Lalla's most homely metaphysics: grand narrative and village kinship are both tsūj, a moment. The vakh is famous in Kashmir because everyone already knows both women. Nobody is safe inside a role. If you are currently the blaze, you will be the absence of smoke. If you are the aunt, you have already been Draupadī.",
        "prac": "Watch one role you are playing today go on and off like a hearth. Do not prefer Draupadī. Do not pity the aunt. Feel the one who saw both.",
        "terms": kt(
            ("tsūj", "a moment; the unit of all glory and all obscurity"),
        ),
        "res": res(
            ("Bhagavad Gītā 2.28", "Unmanifest, manifest, unmanifest again.", "The Gītā consoles Arjuna with cosmology; Lalla consoles no one — she swaps an empress for an aunt."),
            ("Zhuangzi, skull and butterfly", "Identity will not sit still.", "Zhuangzi dreams; Lalla cooks."),
        ),
    },
    {
        "n": 99,
        "title": "Now It Is Dawn — Seek the Friend",
        "kash": "gāfilo pāda tul vēga /\ngāś āv, yār anun /\npañkh kar, pakh tul /\ngāś āv, yār anun",
        "deva": "गाफिलो पाद तुल वेग\nगाश आव यार अनुन\nपंख कर पख तुल\nगाश आव यार अनुन",
        "tr": "Heedless one! Speedily lift your foot and set forth. Now it is dawn. Seek the Friend. Make yourself wings. Lift the winged feet. Now it is dawn. Seek the Friend.",
        "comm": "Dawn is initiation, not a pretty sky. Gāfil, the heedless — Arabic sitting in a Śaiva mouth — is the one who slept through the only hour that matters. The Friend (yār) is the Supreme as companion, the same nearness as verse 46, now urgent. Wings are not fantasy. They are the sudden lightness when the foot actually lifts. The refrain is a drum. Lalla addresses herself and every sleeper. If you wait for more credentials, the dawn will have been another day you slept. Seeking the Friend is not a future lifestyle. It is the next movement of a foot that has been nailed to the bed of habit.",
        "prac": "At the next literal dawn or the next waking from distraction, stand up before the mind finishes its list. Take one actual step as if toward a friend who is already in the room. Do not decorate the step.",
        "terms": kt(
            ("yār", "the Friend; the Supreme as intimate, not as distant judge"),
            ("gāfil", "heedless; the sleeper who misses dawn as the hour of setting out"),
        ),
        "res": res(
            ("Rūmī, the reed and the Friend", "The cry is for the beloved who is also the origin.", "Rūmī sings absence; Lalla shouts a departure time."),
            ("Dhammapada 21", "Heedfulness is the path of the deathless.", "Shared urgency; the Dhammapada stays in discipline, Lalla in friendship."),
        ),
    },
    {
        "n": 100,
        "title": "Give Breath to the Bellows",
        "kash": "damah dī daman-hālē /\nlohār wagi yith /\nteli loh bani sōn /\ngāś āv, yār anun",
        "tr": "Give breath to the bellows, even as the blacksmith does. Then will your iron turn to gold. Now it is dawn. Seek the Friend.",
        "comm": "Alchemical haṭha in one couplet, then the same dawn-refrain. The bellows is still the throat of verse 4; the iron is the untransmuted mind-body; gold is not wealth. It is the Friend-nature showing in what had been ore. Lalla borrows the smithy because everyone in the valley has heard the bellows. No esoteric diagram required. Breath plus heat plus patience, then the refrain: do it now.",
        "prac": "Twelve slow breaths as a smith works a bellows: steady, not dramatic. At the end, look at one dull worry and ask whether it is still iron. Seek the Friend in whatever has begun to gleam.",
        "terms": kt(
            ("loh / sōn", "iron / gold; the unworked life and its transmuted nature, not a market miracle"),
        ),
        "res": res(
            ("Lalla 4", "The same bellows, earlier, as lamp-kindling.", "4 reveals true nature; 100 transmutes metal. Same breath, two crafts."),
            ("Taoist inner alchemy", "Lead into gold as a map of essence.", "Chinese alchemy is a long art; Lalla gives the smith and the dawn in four lines."),
        ),
    },
    {
        "n": 102,
        "title": "I Went Forth as a Cotton-Flower",
        "kash": "lal bāyis pānas pambas-phol /\nchōk wun thaph thaph dits /\nphīriṣhin tūla khyāl kēnjē /\nōlum tūla wāva-gāras thaph",
        "tr": "I, Lalla, went forth in the hope of blooming like a cotton-flower. Many a kick did the cleaner and the carder give me. Gossamer made from me did the spinning-woman lift from the wheel, and a hanging kick I received in the weaver's work-room.",
        "comm": "The soul volunteers to be useful and is processed. Cleaner, carder, spinner, weaver — a Kashmiri industrial theology of suffering. Lalla does not romanticize pain. She tracks it as stages toward the garment of verse 103. If you stop at the kicks, you become bitter cotton. If you consent to being worked, you become cloth. The hope of blooming is innocent and insufficient. Blooming is what the plant wanted; the teaching wants thread.",
        "prac": "Name the 'kick' you are in (a job, a grief, a discipline). Ask: am I still trying to be a flower, or am I willing to be fiber? Do the next hour as fiber without self-pity.",
        "terms": kt(
            ("pambas-phol", "cotton-flower; the naive wish to be beautiful rather than useful to the way"),
        ),
        "res": res(
            ("Lalla 103", "The washerman and the tailor finish the metaphor.", "Read as one poem in two vakhs."),
            ("John 15, the vine and the pruning", "Fruit requires cutting.", "The Gospel prunes to remain in Christ; Lalla is carded to become a garment of the Supreme."),
        ),
    },
    {
        "n": 103,
        "title": "Then I Obtained the Way of the Supreme",
        "kash": "dob yeli chkovinas doṭ-kanē-peth /\nsaz ta sāban mōṭhnam /\nsūc yeli phirithnam kani-kani /\nada lali mē prāvum parama-gath",
        "deva": "दोब येलि छकोविनस दोट-कने-पेथ\nसज त साबन मोठनम\nसूच येलि फिरिथनम कनि-कनि\nअद ललि मे प्रावुम परम-गथ",
        "tr": "When the washerman dashed me on the washing-stone, he rubbed me much with fuller's earth and soap. When the tailor worked his scissors on me, piece by piece — then I, Lalla, obtained the way of the Supreme.",
        "comm": "The way is not granted to the intact. Scissors last. The Self that wanted to remain one pretty flower has to be cut to size for a use it does not choose. Parama-gath, the supreme station, arrives as the end of the textile process, not as an exception to it. Kashmiris still say they cannot parse every metaphor in this pair; Lalla may have meant that too: you do not need to understand the kicks while they are happening. You need to last until the garment. The contested claim is that violence of formation is not evidence of being off the path. It is the path's ordinary machinery. Comfort-spirituality cannot survive this vakh. Neither can a spirituality of pure suddenness that denies the carding. Recognition, for Lalla, includes being made into something that can be worn by the Supreme — a life fitted, not a life preserved.",
        "prac": "Where you feel 'cut to pieces,' stop asking to be put back as you were. Ask what garment this cutting is for. Do one small act of cooperation with the tailor — a truthful word, a dropped vanity — not as self-harm, as fitting.",
        "terms": kt(
            ("parama-gath", "the supreme station / way; the end of the cotton's ordeal, not a bypass of it"),
            ("sūc", "the tailor's shears; discriminative cutting that finishes the soul as cloth"),
        ),
        "res": res(
            ("Lalla 102", "The carding and weaving; 103 is the wash and the cut.", "One metaphor. Do not separate blooming from scissors."),
            ("Romans 9:21", "The potter has right over the clay.", "Paul argues sovereignty; Lalla speaks as the cloth, in the first person, after the shears."),
        ),
    },
]


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.{SLUG}_{n:03d}"
    hero = n in HEROES
    original = u.get("deva") or u["kash"]
    layers = [
        {"kind": "original", "label": "Original", "body": original},
        {"kind": "iast", "label": "Romanization", "body": u["kash"]},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"LV_{n:03d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": f"Vakh {n}",
        "title": u["title"],
        "unit_type": "verse",
        "commentary": u["comm"],
        "themes": ["recognition", "kashmir shaiva", "vakh", "lalla"],
        "tags": [SLUG, "kashmir-shaiva", "lal-ded", "vakh"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "category": "kashmir-shaiva",
            "verse": str(n),
            "grierson_number": n,
            "cultural_context": NOTE,
            "original_source": "Grierson & Barnett, Lallā-Vākyāni (1920)",
            "original_reliability": "SOURCED — Grierson recension (RAS 1920); Kashmiri lightly regularized from the 1920 romanization",
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": original,
        "transliteration": u["kash"],
    }
    if u.get("deva"):
        unit["sanskrit_devanagari"] = u["deva"]
        unit["sanskrit_iast"] = u["kash"]
    if hero:
        unit["tts_key"] = True
    path = os.path.join(OUT, f"{uid.replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return uid


def build() -> int:
    os.makedirs(OUT, exist_ok=True)
    ids = [write_unit(u) for u in UNITS]
    heroes = [u["n"] for u in UNITS if u["n"] in HEROES]
    print(f"{SLUG}: {len(ids)} units (min 25) · heroes {heroes}")
    return len(ids)


if __name__ == "__main__":
    build()
