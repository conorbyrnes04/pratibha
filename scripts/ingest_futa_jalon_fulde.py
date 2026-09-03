#!/usr/bin/env python3
"""Ingest Futa Jalon Fulde traditions from C.A.L. Reichardt, *Grammar of the
Fulde Language* (London: Church Missionary House, 1876), Part II.

Public-domain source: C.A.L. Reichardt, *Grammar of the Fulde Language*
(London: Church Missionary House, 1876). Internet Archive:
grammarfuldelan00reicgoog. Fulde is Reichardt's Latin transcription of Futa
Jalon traditions (Umar Tal wars from Alfa Muhammed Sadi; origin from Muhammed
Sadi and Ibrahim Mandinka). English is a Pratibha rendering (pd_adapted) from
Reichardt's facing English.

This is Futa Jalon Fulde, not Futa Toro Pulaar. Does not follow Gaden 1931 or
Hampâté Bâ / *Koumen*.

Floor: 26 units. Ten are hero verses (tts_key) for the collection mandala
and Listen bake.
"""
from __future__ import annotations

import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/futa_jalon_fulde")
SLUG = "futa_jalon_fulde"
COLL = "Futa Jalon Fulde (Reichardt)"
PROV = (
    "English is a Pratibha rendering (pd_adapted) from C.A.L. Reichardt's facing English in "
    "*Grammar of the Fulde Language* (London: Church Missionary House, 1876 — public domain). "
    "Fulde is Reichardt's Latin transcription of Futa Jalon traditions (Umar Tal wars from Alfa "
    "Muhammed Sadi; origin from Muhammed Sadi and Ibrahim Mandinka). This is Futa Jalon Fulde, "
    "not Futa Toro Pulaar. Does not follow Gaden 1931 or Hampâté Bâ."
)
NOTE = (
    "Futa Jalon (Fuuta Jaloo, Guinea highlands). Reichardt collected from Futa Jalon speakers. "
    "The three traditions are (I) wars of Sheikh al-Ḥājj Umar of Futa, (II) origin of the Pulo "
    "nation from Fezzan, (III) war of Alfa Muhammed Juhe of Masina with Imams Omar and Ibrahim. "
    "Scripture appendix is missionary — not ingested. Orthography is Reichardt's 1876 Latin plate, "
    "not modern Pular ɓ ɗ ƴ ŋ. OCR of the IA Google scan is damaged; Fulde lines are cleaned "
    "reconstructions of Reichardt's transcription of the key sentence, not a new critical edition."
)

# Ten heroes spread across Trad. I (Umar) and Trad. II (origin / first jihad).
HEROES = {2, 3, 4, 7, 9, 13, 15, 16, 19, 24}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


# Each unit: n, reichardt, title, ful, tr, comm, prac, terms, resonances
UNITS: list[dict] = [
    {
        "n": 1,
        "reichardt": "Trad. I / XX, service to Muhammed Legali at Medina",
        "title": "Seven Years Without Changing the Word",
        "ful": "o woni e makko dubi jeeɗiɗi o ƴetti kala ko woni e suudu-makko o hokki hoore-makko e makko. o rewi-mo o waylaaki konngol-makko.",
        "tr": "He lived with him seven years. He took on himself every care of the house and gave himself to him. He followed him and never changed his word.",
        "comm": "Transmission is not a certificate. It is seven years of not changing the word. Khalifa is given after service, not after talent. Futa Jalon Fulde tells this as a highland war-tradition about Umar at Medina under Muhammed Legali, not as a Futa Toro proverb. The contested move is to treat spiritual succession as a gift of brilliance. Reichardt's sentence refuses that. o waylaaki konngol-makko: he did not change his word. The word is the teacher's. Changing it is the student's first vanity. Talent wants to improve the sentence. Service keeps it. Seven years of house-care — every task in the room, the self given over — is the only credential the tradition will name. Later Futa Jalon will crown Imams and fight for kingship; this unit is the prior ethic. A man who will command armies first spent seven years as a servant of a word. Existentially the sentence trains against charismatic shortcut. You do not become the next voice by being more gifted than the last voice. You become it by not altering what was given, until the giver can trust that the word will survive your mouth. Khalifa is the name for that survival, not for your originality. Downriver Futa Toro Pulaar will later proverbialize transmission as milk. Highland Fulde here narrates it as duration plus fidelity. Same language family, different pedagogy: years in a house, not an image of a cow.",
        "prac": "Keep one teacher's word unchanged for seven days. Do not improve it.",
        "terms": kt(
            ("konngol", "word, utterance, the given teaching — not vocabulary; English 'word' is too thin; this is the sentence you are forbidden to edit"),
            ("waylaaki", "did not change, did not turn — a hard negative; 'was faithful' adds a mood the Fulde does not gild"),
            ("dubi jeeɗiɗi", "seven years — duration as credential; English 'apprenticeship' is a trade; this is time spent not altering a word"),
            ("hoore-makko", "his head / himself — the self given over; 'devotion' is too pious; this is the head placed in the teacher's house"),
        ),
        "res": res(
            ("Gaden, Pulaar Texts, Mallol 145, 'What the Cow Ate, the Heifer Suckles' (Futa Toro)", "Both make transmission bodily rather than certificated.", "The mallol is milk in a Senegal-valley proverb dialect; this is seven years of unchanged speech in Futa Jalon Fulde narrative. Do not collapse the dialects."),
            ("Bhagavad Gītā 4.34, approach the knower with homage and service", "Both put service before the handing-on of knowledge.", "The Gītā names inquiry as a third; here the only named act is not changing the word."),
        ),
    },
    {
        "n": 2,
        "reichardt": "Trad. I / XX, composition at the Prophet's tomb",
        "title": "Between the Tomb and the Pulpit",
        "ful": "o joodi hakkunde yanaande Annabi e minbar o fawi keeci-makko e bannge. o timmini deftere-makko o inniri-nde Waʿaz yimɓe yiɗooɓe moƴƴere.",
        "tr": "He sat between the tomb of the Prophet and the pulpit and leaned his back against the wall. He finished his composition and called it an admonition to those who desire to do right — to teach those who wish to follow God.",
        "comm": "The book is written in the interval between grave and pulpit — death and speech. Teaching is not a throne. Umar sits hakkunde yanaande Annabi e minbar, between the Prophet's tomb and the minbar, back against the wall. The architecture is the argument. He does not sit on the pulpit. He does not lie in the grave. He occupies the interval. The contested move is to treat composition as an ascent to a chair. Futa Jalon Fulde locates the finished book in a posture of leaning, not of ruling. The title he gives it — Waʿaz, admonition to those who desire right — is already a refusal of throne-speech. Admonition addresses desire, not subjects. Reichardt's highland tradition is not Futa Toro proverb-speech; it is a travel-narrative of a Tijani sheikh writing at the Prophet's house. The wall takes his back. The two monuments take his sides. What is produced there is counsel for people who wish to follow God, not a manifesto of office. Existentially: every teaching you write sits somewhere. If it sits on rank, it is already a different book. The interval between a death you know and a speech you owe is the only honest desk. The grave keeps you from inflation. The pulpit keeps you from silence. Neither is a seat of power. The wall is.",
        "prac": "Write one counsel sitting between a death you know and a speech you owe. Do not sit on a chair of rank.",
        "terms": kt(
            ("yanaande", "tomb, grave — the death-side of the interval; English 'shrine' gilds it; this is a burial"),
            ("minbar", "pulpit (Arabic minbar) — the speech-side; not a throne, a step from which one exhorts"),
            ("hakkunde", "between, in the interval — the philosophical place; English 'among' loses the two poles"),
            ("Waʿaz", "admonition, exhortation (Arabic waʿẓ) — a genre of counsel, not of decree; 'sermon' is too ecclesiastical"),
        ),
        "res": res(
            ("Marcus Aurelius, Meditations 2.17, life as a sojourn between birth and death", "Both locate the work of a life in an interval, not on a throne.", "Marcus writes the interval as Stoic physics; Fulde writes it as a body leaning between tomb and pulpit."),
            ("Gospel of Thomas 42, 'Be passers-by'", "Both refuse to settle teaching into an office.", "Thomas's passer-by has no monument; Umar sits between two of the Prophet's monuments and still will not take a chair."),
        ),
    },
    {
        "n": 3,
        "reichardt": "Trad. I / XX, peace between Hausa and Bornu",
        "title": "Grass Does Not Grow There",
        "ful": "o naati hakkunde-maɓɓe o waaju-ɓe o haɗi-ɓe haa ɓerɗe laaɓi hakkunde-maɓɓe. haa hannde huɗo fuɗnataa e nokku ɗo ɓe njaɓi.",
        "tr": "He got in between them and exhorted them and prevented them from fighting until there were clean breasts between them. Until this day grass does not grow on the spot where the fight took place.",
        "comm": "Peace is a power, not a mood. The ground keeps the wound after the men stop. Umar gets between Hausa and Bornu, exhorts, prevents fighting, until ɓerɗe laaɓi — clean breasts — exist between them. Then the tradition adds a geographic remainder: until this day grass does not grow on the spot. The contested move is to treat reconciliation as a feeling that evaporates when the speech ends. Futa Jalon Fulde makes peace a force that enters a gap and leaves a scar on the earth. Clean breasts are an inner clearing. The bare patch is the outer archive. The men can go home. The ground will not pretend. This is highland war-memory, not a Senegal-valley mallol about small acts returning. Reichardt's informants keep the place as a witness. Existentially: when you stop a killing, do not plant immediately over the site as if the relation were never wounded. The teaching is against both endless feud and cosmetic repair. ɓerɗe laaɓi is real. huɗo fuɗnataa is also real. Peace that cannot bear a bald patch is still a mood. Peace that can leave the wound visible is a power. The sheikh's body in the gap is the method. The grass that refuses is the proof.",
        "prac": "Stand between two people who are killing a relation. Do not take a side. Afterward, do not plant over the wound as if it never happened.",
        "terms": kt(
            ("ɓerɗe", "breasts / hearts (pl. of ɓernde) — inner organs of feeling made clean; English 'hearts' is too sentimental; 'breasts' keeps the body"),
            ("laaɓi", "became clean, cleared — a completed inner washing; 'reconciled' is a diplomatic gloss that hides the washing"),
            ("huɗo", "grass — the land's ordinary cover; its refusal is the archive"),
            ("hakkunde-maɓɓe", "between them — the gap the sheikh enters; peace is a location before it is a mood"),
        ),
        "res": res(
            ("Heraclitus B5, they purify themselves with blood as if one who had stepped in mud were to wash with mud", "Both keep a stain that washing-talk will not erase.", "Heraclitus mocks ritual detergent; Fulde lets the earth refuse grass as a witness that peace happened and the wound remains."),
            ("Yoruba òwe, 'Peace is the father of friendship'", "Both rank peace as a generative power, not a mood.", "The òwe fathers friendship; this tradition scars the ground. One is kinship-proverb, the other highland war-memory."),
        ),
    },
    {
        "n": 4,
        "reichardt": "Trad. I / XX, meeting Muhammed Bello",
        "title": "The Mat Left Vacant",
        "ful": "ɓe ndaɗndi teddungal; hay gooto yiɗaano ƴettude ko adii. ɓe njoodi e leydi, ɓe ngoppi daago ɓolɗo hakkunde-maɓɓe.",
        "tr": "A contention of civilities took place; neither wished to take precedence. Both sat on the ground leaving the mat vacant between them.",
        "comm": "Honor that cannot sit on the ground is not honor. The vacant mat is the teaching. When Umar meets Muhammed Bello, neither will take precedence. Both sit on the earth and leave the daago empty between them. The contested move is to treat honor as a higher seat. Futa Jalon Fulde — here a Sokoto encounter told in highland speech — makes teddungal a contention of refusals. The mat is the prize neither will take. Sitting on leydi, the ground, is not humility as costume. It is the only posture that can keep two masters in one room without one becoming the other's floor. Futa Toro Pulaar will later proverbialize honor as koyēra, shame ranked above death. This Fulde scene does not proverbialize. It stages. The empty mat is a third presence: the rank both men refuse to occupy in front of the other. Existentially: the best seat in the room is the one that would make you first. Leave it. Sit where the floor already is. If you cannot sit on the ground, your honor is still a chair. The teaching is the vacancy, not the courtesy-speech around it. Two men who can leave a mat unused have already finished the meeting.",
        "prac": "Today leave the best seat empty between you and the person you honor. Sit on the floor.",
        "terms": kt(
            ("daago", "mat — the honor-seat left vacant; English 'rug' is furniture; this is the rank neither will take"),
            ("teddungal", "honor, civility, the contention of respect — not 'politeness'; a struggle over who will not go first"),
            ("leydi", "earth, ground, land — where they actually sit; 'floor' is too indoor; this is the country under the mat"),
            ("ɓolɗo", "vacant, left unused — the teaching is the emptiness, not the sitting"),
        ),
        "res": res(
            ("Zhuāngzǐ, the useless tree that survives by not being timber", "Both make vacancy a form of honor that refuses use.", "Zhuāngzǐ's tree lives by being unfit; the mat is fit and still left empty by two men who could take it."),
            ("Marcus Aurelius, Meditations 1.17, on not being seated above others", "Both refuse precedence as a spiritual act.", "Marcus thanks the gods for a temperament; Fulde stages two bodies on the ground and a third object unused."),
        ),
    },
    {
        "n": 5,
        "reichardt": "Trad. I / XX, Bello asks a book on Qadiri / Tijani",
        "title": "That the Two Paths Not Injure Each Other",
        "ful": "Bello wi'i Omaru yo o winndu deftere fi Qadiri'en yo ɓe waasataa ñiɓtude hakkunde-maɓɓe, yo ɓe ɓe mbaawaa ƴettude Tijani ɓe bona hoore-maɓɓe.",
        "tr": "Muhammed Bello told Sheikh Omaru to write a book concerning the Qadiri people, exhorting that there be no hostile rivalry, that those who are not able to adopt the Tijani path may not injure themselves.",
        "comm": "A second path is not an enemy. Inability to enter one ṭarīqa is not a license to harm. Bello asks Umar for a book on the Qadiri people so that those who cannot take the Tijani way will not injure themselves, and so that hostile rivalry will not grow. The contested move is to treat a new affiliation as a war on the old one. Futa Jalon Fulde, speaking a Tijani sheikh's diplomacy inside a Qadiri caliphate, refuses that war. The book is not a recruitment tract. It is a fence against ƴettude that becomes bone. Two West African paths — Qadiriyya already planted, Tijaniyya arriving with Umar — are told here as capable of injuring each other, and therefore as needing a written restraint. This is not Futa Toro proverb ethics. It is highland-Sokoto path politics in Reichardt's Latin Fulde. Existentially: name the practice you cannot take up. That inability is not a critique of the people who can. It is also not a demand that they abandon theirs. The teaching is against both conversion-by-scorn and loyalty-by-mockery. A second path in the same town is a test of ɓerɗe, not of victory. The book Bello wants is a peace between ways, not a winner.",
        "prac": "Name one practice you cannot take up. Do not mock the people who can. Do not require them to mock yours.",
        "terms": kt(
            ("ñiɓtude", "hostile rivalry, injurious competition — not 'debate'; the harm of two paths grinding"),
            ("ƴettude", "to take up, adopt — the Tijani path as something taken, not as a conquest of the Qadiri"),
            ("Qadiri'en / Tijani", "the two ṭarīqas named in Fulde — English 'sects' is a fight-word; here they are paths that can injure"),
            ("bona hoore-maɓɓe", "injure themselves / spoil their own heads — harm as self-harm, not only as harm to the other path"),
        ),
        "res": res(
            ("Bhagavad Gītā 4.11, however people approach me, I grant them that path", "Both refuse to make a second approach an enemy.", "The Gītā speaks from a divine center; Bello asks a human sheikh to write a fence between two orders."),
            ("Gospel of Thomas 47, no one can mount two horses", "Both know two ways can tear a person.", "Thomas forbids double riding; Fulde asks those who cannot take the second horse not to injure themselves or the first."),
        ),
    },
    {
        "n": 6,
        "reichardt": "Trad. I / XX, Almami Bakari at Jugunko",
        "title": "If You Leave Futa, Futa Will Suffer",
        "ful": "nde o yi'i mawngu yimɓe rewɓe Almami, o wi'i-ɓe: on ngoppatu Futa; so on ngoppii Futa, Futa fooloto. Almami wi'i: diina ko diina Allah, laawol goonga.",
        "tr": "When he saw the great crowd that followed Almami Bakari, he said: you must not leave Futa; if you leave Futa, Futa will suffer. Almami Bakari said the religion is the religion of God, the right way — he would not hinder any Futa people from following Al Hajji.",
        "comm": "Two goods collide: the land needs its people; the path may call them out. The almami refuses to police God's road. Omar names the cost to the land. At Jugunko he sees the crowd following Almami Bakari and says: do not leave Futa; if you leave, Futa will suffer. Bakari answers that the religion is God's, the right way — he will not hinder Futa people from following Al Hajji. The contested move is to resolve the collision by picking one good and calling the other worldly. Futa Jalon Fulde keeps both sentences in the same scene. Omar's Futa here is the highland that will later lose men to his own jihad. The irony is already the teaching. The sheikh who will draw the world after him first names what the land loses when the people go. Bakari's refusal to police diina is also a teaching: God's road is not a border guard's job. Existentially: before you leave a place that needs you, say aloud what it will suffer. If you still go, do not pretend the land will not. The two goods remain two. Futa Toro, downriver, is another Futa with another leaving-story; do not collapse the names. This is highland political theology, not a mallol. The crowd is the wound being named in advance.",
        "prac": "Before you leave a place that needs you, say aloud what it will suffer. If you still go, do not pretend it will not.",
        "terms": kt(
            ("Futa", "here Fuuta Jaloo, the Guinea highland — not Futa Toro on the Senegal; English 'Futa' flattens two polities"),
            ("fooloto", "will suffer, will be weakened — a future of the land, not of the traveler's soul"),
            ("diina", "religion (Arabic dīn) — Bakari's counter-good; 'faith' is too inward; this is a public road"),
            ("laawol goonga", "the right way, the true road — path as road, not as opinion"),
        ),
        "res": res(
            ("Lal Ded, vakh on leaving the house for the road", "Both stage a collision between household-land and a calling-out.", "Lal's leaving is Kashmiri Shaiva nakedness; this is a Futa Jalon crowd and an almami who will not hinder God's road."),
            ("Analects 4.19, while the parents live, do not travel far", "Both name the cost of leaving those who need you.", "Confucius binds the son to the parents' life; Fulde binds a people to a highland that will suffer their going."),
        ),
    },
    {
        "n": 7,
        "reichardt": "Trad. I / XX, Omar and Suri fighting for the kingdom",
        "title": "The Kingdom of This World",
        "ful": "o naati hakkunde-maɓɓe o waaju-ɓe yo ɓe haɓa-taa fi laamu aduna. o wi'i-ɓe kala oon ronndata bakkatuuji yimɓe haɓooɓe e bannge-makko.",
        "tr": "He went between them and exhorted them not to fight each other on account of the kingdom of this world. He told them that they would each have to bear the sins of those who fight on either side on their account. They put aside their guns until he was out of sight; then they began to fire again.",
        "comm": "The sin of a war for kingship stays with the two who wanted the chair. Presence stops the guns; absence restarts them. A peace that needs your body in the gap is not yet a peace. Umar goes between Omar and Suri, exhorts them not to fight for laamu aduna, the kingdom of this world, and tells each he will bear the sins of those who fight on his account. They put the guns aside until he is out of sight; then they fire again. The contested move is to call the pause peace. Futa Jalon Fulde is brutal here. The sheikh's body is a temporary law. When the body leaves, the chair-hunger returns. The sins do not leave with him. They stay on the two who wanted the kingdom. This is highland Imam-war, not Futa Toro cattle-proverb. Reichardt's tradition names the guns and the sight-line. Existentially: if two people only stop while you stand there, you are not a peacemaker. You are a pause. Name that. Do not let them use your presence as a moral alibi. Peace is what continues after you are gone. Until then, you are grass in a gap, and they are waiting. The teaching is against both the romance of the mediator and the innocence of the claimants. The chair is the sin. The pause is not the cure.",
        "prac": "Today refuse to let two people use you as a pause in their fight. If they only stop while you stand there, name that. Do not call it peace.",
        "terms": kt(
            ("laamu aduna", "kingdom / rule of this world — Arabic dunyā in Fulde; 'politics' is too secular; this is the chair that incurs sin"),
            ("bakkatuuji", "sins, faults (Arabic via Fulde) — borne by the two who wanted the chair, not by the soldiers only"),
            ("ronndata", "will inherit / bear — the sins as a load passed to the claimants"),
            ("haɓa-taa", "do not fight — the exhortation that lasts only as long as the body is in sight"),
        ),
        "res": res(
            ("Bhagavad Gītā 2.47, you have a right to action, not to the fruit", "Both uncouple the fight from the chair it wants.", "The Gītā keeps Arjuna in the war; Fulde tells two Imams their war-for-kingship is already the sin, and the guns restart when the sheikh leaves."),
            ("Gospel of Thomas 81, let him who has become rich reign, and let him who has power renounce", "Both treat worldly rule as a spiritual emergency.", "Thomas asks renunciation of power; this scene shows power resuming the instant the witness is out of sight."),
        ),
    },
    {
        "n": 8,
        "reichardt": "Trad. I / XX, dream of Alfa Muhammed Yakaya",
        "title": "The Fire Whose End He Did Not See",
        "ful": "o yi'i Al Hajji wuli huɗo. ladde wuli, kono o yi'aano joofirde yiite haa o ummii.",
        "tr": "In the dream he saw Al Hajji set fire to the grass. The field burned, but he did not see the end of the fire until he awoke.",
        "comm": "A true vocation is a fire whose edge you do not get to inventory. The dreamer carries the sheikh and cannot keep the name of the place. Alfa Muhammed Yakaya sees Al Hajji set fire to the grass. The field burns. He does not see the end of the fire until he wakes. The contested move is to require a map before a calling. Futa Jalon Fulde gives vocation as an unclosed burn. The dreamer is not shown the last village. He is shown grass catching. Reichardt's highland tradition — Umar's wars told as fire on the savanna — will later fill in the towns. The dream refuses that inventory. You carry a sheikh the way you carry a fire you did not start and cannot pace. Existentially: begin one act whose end you cannot see. The demand for the last town before the first step is already a refusal of the dream. This is not Futa Toro proverb causality, where every affair has a sababu you can name. This is highland oneiric theology: the cause is given; the edge is withheld. Trust is the walking into a field already burning, not the counting of acres from a hill. Waking is not a completion of the map. Waking is the admission that the end was not granted.",
        "prac": "Begin one act whose end you cannot see. Do not demand the map before the first step.",
        "terms": kt(
            ("yiite", "fire — vocation as burn, not as plan; English 'zeal' is a mood; this is grass catching"),
            ("joofirde", "end, termination, the edge — the thing the dream withholds"),
            ("ladde", "field, bush, uncultivated land — the theater of the burn; not a hearth"),
            ("ummii", "he arose / awoke — waking as the cut, not as understanding"),
        ),
        "res": res(
            ("Heraclitus B30, the cosmos as an ever-living fire kindling in measures", "Both make fire the form of a process you do not own.", "Heraclitus' fire is the world's measure; this dream-fire has no shown measure until waking cuts it."),
            ("Bhagavad Gītā 11, Arjuna cannot bear the vision of the infinite form", "Both withhold the complete inventory of a calling.", "Arjuna sees too much and asks it to stop; Yakaya is not shown the end at all."),
        ),
    },
    {
        "n": 9,
        "reichardt": "Trad. I / XX, books burned at Jugunko",
        "title": "Why Should I Come Out",
        "ful": "o joodi e suudu-makko o yiɗaano yaltude. o wi'i: ko waɗi mi yalta, nde defte-am fow mbuli? Almuudo wondi-mo: ko aan winndi defte ɗee; so Allah jaɓii a waawata winndude goɗɗe.",
        "tr": "He sat in his house and would not come out. He said: why should I come out, seeing that my books are all burned? A pupil took him on his back and said: it is you who have written all these books, and if God will you may still write others. He answered: you speak truly, but books like these cannot be had in this country. After that he trusted in God.",
        "comm": "Grief for books is not vanity. The pupil's move is correct and incomplete: the writer can write again, and also these copies cannot be had here. Trust in God is not a shrug. It is sending money and paper to Timbuktu. After the burning at Jugunko, Umar will not come out. Why should I, seeing that my books are all burned? A pupil carries him on his back: you wrote these; if God wills you can write others. Umar: you speak truly, but books like these cannot be had in this country. Then he trusts God. The contested move is to treat the loss of a library as either pride or as nothing. Futa Jalon Fulde keeps both truths in one exchange. The writer is not the copies. The copies are not replaceable in this highland. Trust that follows is practical: paper from Timbuktu, not a smile. Futa Toro Pulaar will proverbialize inheritance as milk. Here the inheritance is a burned room and a pupil's back. Existentially: if a work of yours is destroyed, name both: you can make another, and this one cannot be replaced. Then send for paper. Do not call the sending a lack of faith. The sending is the faith. The pupil is right that the writer remains. The sheikh is right that this country cannot reprint what burned. Both sentences are the teaching.",
        "prac": "If a work of yours is destroyed today, name both truths: you can make another, and this one cannot be replaced. Then send for paper.",
        "terms": kt(
            ("defte", "books (pl. of deftere, from Arabic daftar) — copies as irreplaceable objects, not 'knowledge' in the abstract"),
            ("almuudo", "pupil, student — the one who carries the sheikh on his back; English 'disciple' is too churchy"),
            ("yaltude", "to come out — grief as a refusal of the doorway"),
            ("mbuli", "were burned — a completed destruction; 'lost' is too mild"),
        ),
        "res": res(
            ("Zhuāngzǐ, wheelwright Bian, the knack that cannot be put in the book", "Both split the living knower from the copy.", "Zhuāngzǐ distrusts the book; Umar grieves the copies because this highland cannot replace them, then sends for paper."),
            ("Lal Ded, vakhs on the house burned and the self remaining", "Both refuse to let a burned house be the end of the speaker.", "Lal burns the inner house as liberation; Umar sits in a burned library and must be carried out, then trusts God by restocking."),
        ),
    },
    {
        "n": 10,
        "reichardt": "Trad. I / XX, scarce water at Dingerawi",
        "title": "God Will Make That Easy",
        "ful": "yimɓe annduɓe leydi ndii wi'i ndiyam ɗo ɗo famɗi. Al Hajji jaabii: ndaara, Allah waɗata ɗum newi.",
        "tr": "People who knew the land said that water was very scarce there. Al Hajji answered: see, God will make that easy. After he reached there God sent a blessing of water.",
        "comm": "This is not a prosperity slogan. It is a refusal to let scarcity veto a place already given in a dream. The ease is God's, not the sheikh's technique. People who know the land say water is scarce at Dingerawi. Al Hajji: see, God will make that easy. After arrival, a blessing of water. The contested move is to hear Allah waɗata ɗum newi as a technique for getting what you want. Futa Jalon Fulde ties the sentence to a prior dream-place. The land-knowers are not fools. Scarcity is real. The sheikh does not argue hydrology. He refuses to let the known dryness cancel a given destination. Ease, when it comes, is attributed to God, not to the caravan's skill. This is highland itinerant theology, not a Futa Toro proverb about wells and ropes matching. Existentially: name one necessary place that looks dry. Go without a second plan. Ask for water only after you have arrived. The teaching is against both magical thinking and the veto of the expert. The expert may be right about the land. The dream may still be the road. You find out by arriving, not by winning the argument at the previous camp. newi, ease, is what God does to a dryness you did not pick for comfort.",
        "prac": "Name one necessary place that looks dry. Go to it without a second plan. Ask for water only after you have arrived.",
        "terms": kt(
            ("ndiyam", "water — the scarce good; English 'resources' loses the drink"),
            ("newi", "easy, made easy — God's act, not a method; 'prosperity' is the slogan this unit refuses"),
            ("annduɓe leydi", "those who know the land — local expertise that is true and still not a veto"),
            ("famɗi", "is scarce, is little — a fact the sheikh does not deny, only refuses as a stop"),
        ),
        "res": res(
            ("Ibn ʿArabī / Balyānī, the secret of the one who is God, on tawakkul", "Both refuse a second plan that would replace trust.", "Balyānī dissolves the servant into the Real; Fulde keeps the land-knowers' fact and still walks into the dry place."),
            ("Dhammapada 5, hatreds never cease by hatred", "Both refuse to let a known hardness be the last word.", "The Dhammapada's cease is ethical; here the hardness is hydrological and the ease is God's after arrival."),
        ),
    },
    {
        "n": 11,
        "reichardt": "Trad. I / XX, burst gun at the welcome",
        "title": "A Hundred Guns Would Be Nothing",
        "ful": "Tamba'en wi'i: so ɗum woni e amen o wara-mo, walla o piya-mo, walla o yeeyoo-mo. Rewɓe Sheikh'en wi'i: so kulle teemedere mbusi e sahaa gooto, ɗum wonaa hay huunde. Sheikh wi'ataa hay huunde; o hokkate en goɗɗe, o hokkate mbusaaɗe baylo yo o moƴƴin.",
        "tr": "The Tamba people said: if it were among us he would kill that man, or flog him, or sell him on account of the gun. The Sheikh's followers said: if a hundred guns should burst at one time it would be nothing. The Sheikh would say nothing to us; he would give us others and give the broken ones to the blacksmith to be repaired.",
        "comm": "Two economies of accident. A king's honor kills the man whose tool failed. A sheikh's honor repairs the tool. The broken gun is not a crime. At a welcome a gun bursts. Tamba people: if it were among us he would kill, flog, or sell the man. The Sheikh's people: if a hundred guns burst at once it would be nothing; he would say nothing, give others, give the broken ones to the blacksmith. The contested move is to treat a failed tool as a failed person. Futa Jalon Fulde stages a comparison of honors. Royal honor is a wound that must be paid in a body. Sheikhly honor is a repair that must be paid in iron. baylo, the smith, is the third party who receives the break. This is highland court-and-camp ethics, not a Senegal mallol about small acts returning. Existentially: when someone's tool fails in your house, repair it. Do not punish the person for the break. If your honor requires a body, it is Tamba honor. If it requires a smith, it is this teaching. The hundred guns are a hyperbole that protects the one accident. Nothing is not indifference. It is the refusal to make a crime of metal. The man lives. The iron goes to the baylo.",
        "prac": "When someone's tool fails in your house today, repair it. Do not punish the person for the break.",
        "terms": kt(
            ("kulle", "guns — the failed tools; English 'weapons' is too grand; these are instruments that burst"),
            ("baylo", "blacksmith — the third party of repair; honor that uses a smith instead of a scaffold"),
            ("mbusi", "burst, broken — accident as metal-event, not as moral event"),
            ("hay huunde", "nothing at all — the sheikh's measure of the accident; not 'forgiveness', a refusal to make it a case"),
        ),
        "res": res(
            ("Marcus Aurelius, Meditations 4.49, the rock the wave breaks on", "Both refuse to let an accident become a verdict on the person.", "Marcus trains an inner rock; Fulde sends the broken gun to a smith and gives the man another."),
            ("Yoruba òwe, 'An accident is not like a result that is foreseen'", "Both split accident from intended result.", "The òwe is epistemic; this tradition is political: two honors, kill versus repair."),
        ),
    },
    {
        "n": 12,
        "reichardt": "Trad. I / XX, Basi sent to Jimba",
        "title": "I Will Go and Trust in God",
        "ful": "kala mo o noddi wi'i: mi waawaa yeewde Jimba. Gooto innde-makko Basi wi'i: mi yaha, mi hoolii e Allah.",
        "tr": "If Al Hajji called one man, he said: I am not able to face Jimba. Another said the same. But one man named Basi said: I will go, and trust in God.",
        "comm": "Courage here is not temperament. It is a sentence: I will go, and trust in God. The others are not cowards in general; they are unable to face this king. The teaching is the one yes. Al Hajji calls men to face Jimba. Each says: I cannot. Basi says: mi yaha, mi hoolii e Allah. The contested move is to moralize the refusals as a character defect. Futa Jalon Fulde lets them stand as accurate self-knowledge: this king, this errand, I cannot. Basi's yes is not a louder personality. It is a going plus a trust named in the same breath. Trust is not a feeling beforehand. It is the walking. Highland Fulde here is a war-camp ethics of named errands, not Futa Toro proverb courage, and not a mallol about boasting. Existentially: name the one visit you have refused out of fear of a hard person. Go once. Do not wait to feel ready. The sentence is the courage. The others remain in the story as a mercy: not everyone is asked to be Basi toward every Jimba. The one yes is enough for the teaching. Do not conscript the rest. yeewde Jimba, to face Jimba, is a particular inability. Honor it as particular. Then let the one who can go, go.",
        "prac": "Name the one visit you have refused out of fear of a hard person. Go once. Trust is the going, not a feeling beforehand.",
        "terms": kt(
            ("hoolii e Allah", "trusted in God — trust as the going, not as a prior emotion; English 'faith' is too interior"),
            ("yeewde", "to face, to look upon, to confront — the particular inability; 'meet' is too mild"),
            ("mi yaha", "I will go — the whole courage in a future of walking"),
            ("waawaa", "I am not able — accurate limit, not a vice-name"),
        ),
        "res": res(
            ("Bhagavad Gītā 18.66, abandon all dharmas, go to me alone", "Both bind going to a trust named in the same breath.", "The Gītā's going is refuge in Kṛṣṇa; Basi's going is an errand toward a feared king."),
            ("Yoruba òwe, 'Boasting is not courage'", "Both refuse to let a loud mouth be the virtue.", "The òwe negates the boast; Fulde gives one quiet sentence that is the going."),
        ),
    },
    {
        "n": 13,
        "reichardt": "Trad. I / XX, Fatima of Hausa under fire",
        "title": "She Did Not Leave the Prayer",
        "ful": "yumma Fatima mo Hausa dariima o tinki, o ummii o tufi. Nde o ƴetti hoore-makko, golle yani e leydi e nokku ɗo hoore-makko memi. O jokki juulde. O dartidaano, o dillaano, o hulataano haa o timmini.",
        "tr": "The mother Fatima, of Hausa, stood and bowed in prayer, then made the prostration. As she raised her head a shot struck the ground on the very spot where her head had touched it. She continued her prayer. She did not stop, she did not move, she did not fear, until she had finished.",
        "comm": "Prayer is not a shelter from the shot. It is a refusal to let the shot become the liturgy. The ground takes the ball where the forehead was. She finishes. Fatima of Hausa bows, prostrates; as she lifts her head a shot strikes the exact spot her head had touched. She continues. She does not stop, move, or fear until she finishes. The contested move is to read this as magic protection or as female piety for display. Futa Jalon Fulde — a Hausa woman in a highland war-tradition — gives a phenomenology of attention. The juulde is not a bunker. The shot lands. The liturgy does not incorporate it. She does not restart to include the event. She does not narrate. She completes. This is not Futa Toro proverb composure, where the heart is not a joint. This is a body that will not let gunfire rewrite the sequence of rakʿa. Existentially: finish one act of prayer or attention while a disturbance is happening. Do not restart. Do not narrate until you are done. The ground may take what was aimed at you. That is not the point. The point is that the shot does not get to be the new imam. dartidaano, dillaano, hulataano: three refusals. Stopping, moving, fearing. She withholds all three until timmini, finished.",
        "prac": "Finish one act of prayer or attention while a disturbance is happening in the room. Do not restart. Do not narrate the disturbance until you are done.",
        "terms": kt(
            ("juulde", "ritual prayer (Fulde for ṣalāt) — a sequence that can be finished; English 'prayer' is too vague"),
            ("tufi", "she prostrated — the forehead on the ground that the shot then occupies"),
            ("hulataano", "she did not fear — a negative that is conduct, not a feeling-claim"),
            ("timmini", "she finished, completed — the whole teaching in a perfective; 'continued' would still be during"),
        ),
        "res": res(
            ("Dhammapada 25, by effort the wise man makes an island that no flood can overwhelm", "Both keep a completed inner sequence against a surrounding violence.", "The Dhammapada's island is built by effort over time; Fatima finishes one prayer while a shot takes the ground."),
            ("Marcus Aurelius, Meditations 5.20, the impediment to action advances action", "Both refuse to let an obstacle rewrite the act.", "Marcus converts obstacle into material; Fatima does not convert the shot at all. She simply finishes."),
        ),
    },
    {
        "n": 14,
        "reichardt": "Trad. I / XX, Banjugu kills Jimba",
        "title": "Find His Life Back",
        "ful": "o jaabii: mi wi'aano-mo yo o wara Jimba; so o warii-mo, ko kanko ronndi yonki-makko. Mi woppii-mo e konngol teddungal sabu ko lamɗo.",
        "tr": "He replied: he had not told him that he must kill Jimba; if he has killed him he is responsible for his life. He left him alone and returned by his word of honor because he was a king. If he has killed him he must find his life back.",
        "comm": "An enemy-king still has a life that is not yours to farm out. Honor left Jimba alive. The proxy who kills him does not inherit the sheikh's war; he inherits a debt. Banjugu kills Jimba. Umar: I did not tell him to kill Jimba; if he has killed him he is responsible for his life; I left him by a word of honor because he was a king; he must find his life back. The contested move is to treat a lieutenant's kill as the leader's intent. Futa Jalon Fulde splits the war from the life. Jimba was an enemy and a lamɗo. Honor left him alive. The proxy wanted to finish the story. The sheikh returns the yonki as a debt the killer must carry. This is highland king-ethics inside jihad, not a Futa Toro mallol about the cow's hoof on the calf. Existentially: do not let anyone kill a quarrel for you that you had chosen to leave alive. If they already have, say: that death is yours, not mine. The teaching is against both pacifism-as-brand and assassination-as-loyalty. A word of honor to a king is not cancelled by a useful corpse. konngol teddungal, the word of honor, is a life-left-alive. Finding the life back is a debt that cannot be paid in loyalty-talk.",
        "prac": "Today do not let anyone kill a quarrel for you that you had chosen to leave alive. If they already have, say: that death is yours, not mine.",
        "terms": kt(
            ("yonki", "life, soul, the living breath — what the killer now owes; English 'life' is biological; this is a debt"),
            ("lamɗo", "king — the reason honor left him alive; 'chief' is too small; the office is the fence"),
            ("konngol teddungal", "word of honor — the sentence that kept Jimba alive; not a contract, a spoken honor"),
            ("ronndi", "is responsible for / has inherited — the kill as a load, not as a favor"),
        ),
        "res": res(
            ("Bhagavad Gītā 2.19–21, he who thinks this kills and he who thinks this is killed", "Both refuse to let a killing be a simple transfer of the leader's will.", "The Gītā metaphysically denies the kill; Umar morally returns the life as the killer's debt."),
            ("Gospel of Thomas 98, the assassin who kills the powerful man at home", "Both know a killing done by a proxy.", "Thomas's assassin is the soul's own act against power; here the proxy's kill is refused as the sheikh's war."),
        ),
    },
    {
        "n": 15,
        "reichardt": "Trad. I / XX, soldiers tired at Minyin",
        "title": "If You Are Tired, Sit Down",
        "ful": "konu wi'i Sheikh'en ɓe ngondi. Sheikh wi'i ɓe poti haɓde. Ɓe wi'i ɓe ngondi. Sheikh wi'i: so on ngondi, awa en jooɗo; on nji'ii sembe Allah; on nganndii golle-mon toɓataa so Allah jaɓaaki.",
        "tr": "The soldiers said to Al Hajji that they are tired; the Sheikh said they must fight; they say they are tired. The Sheikh said: if you are tired, well, let us sit down; you see the power of God; you know your gun won't give fire if God be unwilling.",
        "comm": "He does not shame tired men into a charge. He sits. The gun is not a will. This is not quietism; after the sitting he prays, and the war continues by another gate. The first move with exhaustion is to sit. Soldiers at Minyin say they are tired. The Sheikh says they must fight. They repeat they are tired. He says: if you are tired, well, let us sit down; you see the power of God; you know your gun will not fire if God is unwilling. The contested move is to hear sitting as surrender or as a trick. Futa Jalon Fulde lets the sheikh join the tiredness. en jooɗo — let us sit — includes him. The gun's misfire is theologized, not as an excuse to quit the campaign, but as a limit on will. Later the war finds another gate. The first move remains the sit. This is highland command ethics, not Futa Toro proverb patience, and not a mallol about the heart that will not bend. Existentially: when necessary work meets real tiredness, sit down with the tired people. Do not give a speech. Do not call sitting surrender. If the work is still required, it will reopen by another door. The speech that shames exhaustion is already a false gun. ngondi, we are tired, is allowed to be the last human word before the sit.",
        "prac": "When a necessary work meets real tiredness today, sit down with the tired people. Do not give a speech. Do not call sitting surrender.",
        "terms": kt(
            ("ngondi", "we are tired, we are exhausted — a bodily fact allowed to stop a charge"),
            ("en jooɗo", "let us sit — the sheikh included; English 'rest' is a break; this is a shared sitting"),
            ("golle", "guns (here) — the tool that will not fire if God is unwilling; will is not in the metal"),
            ("sembe Allah", "the power of God — what you see when you sit instead of charging"),
        ),
        "res": res(
            ("Zhuāngzǐ, Cook Ding, the pause in the joints of the ox", "Both make a pause the first skill, not a failure of nerve.", "Cook Ding's pause is craft inside a carcass; the sheikh's sit is command inside a tired army."),
            ("Marcus Aurelius, Meditations 6.13, on not being a puppet pulled by impulse", "Both refuse to let urgency be identical with right action.", "Marcus trains inner delay; Fulde sits the whole troop down and waits on whether the gun will even fire."),
        ),
    },
    {
        "n": 16,
        "reichardt": "Trad. I / XX, tears entering Dengerabe",
        "title": "He Weeps After Victory",
        "ful": "ɓe nji'i o wuli gite naatoyde saare. Ɓe wi'i: ko waɗi Al Hajji o wuli, o haɓii o dañii? O wi'i: ko wuli-mi ko mi miijii no aduna newn-ii-mi; mi huli Allah heɓataa-mi e laakara, wonaa e aljanna.",
        "tr": "They saw that he was moved to tears as he entered the town. They said: what is the matter with Al Hajji — he went to war, he was victorious, why does he weep? He said what moved him to tears was that the world had made him comfortable, and he fears God may not find him in the other world, not in heaven.",
        "comm": "Victory is the danger. Comfort is the spiritual emergency. He does not weep for the dead of Minyin in this sentence; he weeps that success might misplace him relative to God. Entering Dengerabe they see him in tears. Why does he weep — he went to war, he won? He says the world has made him comfortable, and he fears God may not find him in the other world, not in heaven. The contested move is to read the tears as compassion for the slain or as performance. Futa Jalon Fulde gives a harder reading: aduna has eased him. Ease is the threat. laakara, the other world, may not contain him if comfort has already placed him. Highland jihad here is not Futa Toro proverb about God having other than leaves for the couscous. It is a sheikh crying that success is a misplacement. Existentially: after one success, do not celebrate first. Ask whether this comfort has hidden you. If yes, do one hidden act that cannot be posted. The teaching is against victory-as-proof. The war can be won and the soul lost in the same afternoon. The tears are the only accurate report. aljanna, the garden, is named as the place he fears he will miss — not because he lost, because he was made comfortable.",
        "prac": "After one success today, do not celebrate first. Ask whether this comfort has hidden you. If yes, do one hidden act that cannot be posted.",
        "terms": kt(
            ("aduna", "this world (Arabic dunyā) — the comforter; English 'world' is too neutral; this is the ease that misplaces"),
            ("laakara", "the other world, the hereafter — where he fears he will not be found"),
            ("newn-ii-mi", "has made me comfortable / eased me — victory as softness, not as glory"),
            ("aljanna", "the garden, paradise — the place comfort might cost; 'heaven' is too generic"),
        ),
        "res": res(
            ("Marcus Aurelius, Meditations 6.30, take care not to be Caesarified", "Both treat success as the moment of spiritual danger.", "Marcus warns against imperial coloring; Umar weeps that comfort may hide him from God."),
            ("Bhagavad Gītā 2.38, treat pleasure and pain, gain and loss alike", "Both uncouple victory from spiritual location.", "The Gītā asks evenness in the act; Fulde shows tears after the win as the evenness that is still possible."),
        ),
    },
    {
        "n": 17,
        "reichardt": "Trad. I / XX, Kauja's two hundred wives",
        "title": "Choose Four and Let the Rest Go Free",
        "ful": "Sheikh wi'i-mo: rewɓe-maa ɓuri nayi; so ɓe ndimaaɗɓe, suɓo nayi, yoppu heddiiɓe ɓe njaha. Ɗum woni sariya diina.",
        "tr": "The Sheikh said unto him: his wives are more than four; if they are free he must choose four and let the rest go free — this is the order of the faith. This hurt the king's feelings, and those of the foremost men who possessed many wives.",
        "comm": "The ordinance is a reduction of possession, not a romance. The hurt is the teaching. A king whose household is a warehouse is being asked to become a man with four. Kauja has two hundred wives. The Sheikh: if they are free, choose four and let the rest go — this is sariya diina. It hurts the king and the foremost men who possess many. The contested move is to hear the four as a marital ideal or as colonial reform. Futa Jalon Fulde, speaking sharīʿa into a highland king's warehouse, makes the law a cut in hoarding. The women are not a romance plot. They are a stock. The hurt of the men who have many is the proof that the sentence landed. This is not Futa Toro proverb about a second wife not being a wife. It is legal reduction of a royal hoard. Existentially: name one hoard you keep past need — objects, claims, people on a string. Release all but what you can actually keep faith with. The teaching is against both libertine accumulation and the fantasy that the cut is about love. Faith has a number you can actually keep. The rest is warehouse. yoppu heddiiɓe ɓe njaha: let the remainder go. The going is their freedom, not the king's generosity.",
        "prac": "Name one hoard you keep past need (objects, claims, people on a string). Release all but what you can actually keep faith with.",
        "terms": kt(
            ("sariya diina", "the law of the religion (sharīʿa) — a cut in possession, not a love-rule"),
            ("nayi", "four — the number you can keep faith with; English 'limit' hides that it is a count of persons"),
            ("ndimaaɗɓe", "free persons — the condition of the release; if they are free they cannot be stock"),
            ("yoppu", "let go, release — the remainder's road out; 'divorce' is too modern-legal"),
        ),
        "res": res(
            ("Dhammapada 186–187, not by a rain of coins is thirst quenched", "Both refuse accumulation as a spiritual good.", "The Dhammapada addresses thirst; Fulde addresses a king's warehouse of wives and the hurt of men who have many."),
            ("Gaden, Pulaar Texts, 'A Father's Counsel' (Futa Toro), a second wife is not a wife", "Both warn that multiplied household is not multiplied marriage.", "Gaden's mallol is Futa Toro proverb dialect about false nearness; this is Futa Jalon legal reduction of a royal hoard. Different dialect, different genre."),
        ),
    },
    {
        "n": 18,
        "reichardt": "Trad. I / XX, Karta conspiracy",
        "title": "He Did Not Believe Until It Showed",
        "ful": "yimɓe-makko kaaldi e makko: yimɓe Karta mbaɗata en. Sheikh goongɗinaano haa huunde feeñi, tan o yi'i goonga.",
        "tr": "His people had spoken to him: the people of Karta will kill us. The Sheikh did not believe it until things showed out, then he saw the truth.",
        "comm": "Suspicion is not wisdom. He waits for the showing. The cost is real: people die behind walls while he refuses a rumor. The teaching is against both naivete-as-virtue and intelligence-as-accusation. His people say Karta will kill us. The Sheikh does not believe until things show out; then he sees the truth. The contested move is to treat this delay as either saintly innocence or as culpable stupidity. Futa Jalon Fulde keeps the cost and the method. goongɗinaano haa huunde feeñi — he did not assent until the thing appeared. Highland war will punish the wait. The tradition still refuses rumor as a sufficient cause of action. This is not Futa Toro mallol that truth catches the lie on a road. This is a commander who will not move on a story. Existentially: do not act on a warning about people until you have seen the thing. If you already believed a rumor, walk it back until it shows. The teaching does not promise that waiting is safe. It promises that accusation without appearance is not wisdom. Safety and wisdom are not the same office. goonga, the truth, arrives as a showing, not as a clever suspicion confirmed in private.",
        "prac": "Today do not act on a warning about people until you have seen the thing. If you already believed a rumor, walk it back until it shows.",
        "terms": kt(
            ("goongɗinaano", "he did not believe / did not assent — withheld credence, not stupidity"),
            ("feeñi", "showed out, became apparent — truth as appearance, not as rumor-work"),
            ("goonga", "truth — what is seen after the showing; English 'facts' is too forensic"),
            ("kaaldi", "they spoke, they told — the rumor as speech, not yet as world"),
        ),
        "res": res(
            ("Heraclitus B1, men fail to understand the logos even after they have heard it", "Both wait on a showing that speech is not yet.", "Heraclitus' logos is always already there; Umar will not treat a warning as a showing until the thing appears."),
            ("Gospel of Thomas 5, know what is in front of your face and what is hidden will be revealed", "Both bind knowledge to what is in front.", "Thomas promises a reveal from facing; Fulde pays a war-cost for refusing to act on what is only said."),
        ),
    },
    {
        "n": 19,
        "reichardt": "Trad. I / XX, letters from every side at Konja",
        "title": "He Does Not Know Which Place He Turns",
        "ful": "o darii e hakkunde-maɓɓe. O wi'i: aduna ɗaɓɓii-yam; ko mi nulaaɗo. Mo wi'i o hootata Dengerabe, o haalii fenaande. Mi anndaa hol to mi hootata so wonaa Allah jom-am hokki-yam laawol.",
        "tr": "He stood in the midst of them. He said the world did seek after him; he was a messenger. Whoever says he turns his face to Dengerabe tells a story; to Nyoro, lies; to Futa Toro, what is untrue. He himself does not know to which place he turns unless God the Lord gives him His directions.",
        "comm": "Demand is not direction. A messenger who knows his next town from his mail has already stopped being sent. At Konja letters come from every side. He stands in the midst: the world seeks him; he is a messenger; whoever says he turns to Dengerabe, Nyoro, or Futa Toro tells a story; he himself does not know unless God the Lord gives him the road. The contested move is to treat a full inbox as guidance. Futa Jalon Fulde — and here the tradition names Futa Toro as one of the false destinations — makes nulaaɗo, messenger, incompatible with a self-chosen itinerary. The highland sheikh will not let downriver Futa, or any other town, become a plan he authored from other people's letters. Demand is the world's hunger. Direction is God's. Existentially: do not answer three invitations today. Sit until one direction is given that you did not generate. The teaching is against both people-pleasing itineraries and the vanity of the man who is sought. Being sought is the danger. The messenger who enjoys being sought has already arrived at the wrong town. fenaande, a lie, is the story that he has a next town. The honest sentence is mi anndaa, I do not know.",
        "prac": "Do not answer three invitations today. Sit until one direction is given that you did not generate.",
        "terms": kt(
            ("nulaaɗo", "messenger, the one sent — incompatible with a self-chosen next town; English 'leader' is the trap"),
            ("laawol", "road, way, direction — what God gives; not a schedule"),
            ("fenaande", "lie, untrue story — the rumor of a planned destination"),
            ("ɗaɓɓii-yam", "sought me, hunted after me — the world's demand, which is not yet a road"),
        ),
        "res": res(
            ("Zhuāngzǐ, the useless tree and the man of no use whom no one can conscript", "Both refuse a usefulness that would write the itinerary.", "Zhuāngzǐ survives by being unusable; Umar is hyper-usable and therefore must not know the next town."),
            ("Ibn ʿArabī / Balyānī, on the servant who has no remaining will", "Both make not-knowing the condition of being sent.", "Balyānī annihilates the servant's will as metaphysics; Fulde keeps a man standing among letters, refusing Futa Toro as a plan."),
        ),
    },
    {
        "n": 20,
        "reichardt": "Trad. I / XX, namesake Imams",
        "title": "The Rainy Season and the Dry",
        "ful": "mi nanii ɓe mbi'a ko kanko woni ndunngu, ko min woni ceedu. Nde ndunngu ari, on nji'a kala haako wonti haako; ko kanko ndunngu, min nganndi ko min ceedu.",
        "tr": "I hear they say he is the rainy season, and of myself that I am the dry season. When the rains come you see all the leaves turn green; he is the rainy season, we know we are the dry season.",
        "comm": "Two powers, one namesake. He accepts the dry name. Green leaves are not the only season that is true. Futa Jalon Fulde here thinks climate as political theology. He hears they say the other Imam is ndunngu, the rains, and he is ceedu, the dry. When the rains come the leaves turn green; he is the rain, we know we are the dry. The contested move is to fight for the green name. Highland Fulde — Guinea's actual rainy and dry seasons as political speech — lets him keep the dry. Futa Toro, down the Senegal, has a different flood-calendar and a different proverb-world. Do not collapse them. Here climate is how two namesake Imams rank power. Green is visible success. Dry is the season that is also true. Existentially: let someone else be the rain today. Keep one dry-season duty that does not compete for green. The teaching is against envy of the namesake who makes things look alive. A highland that only honors ndunngu will starve in ceedu. Both seasons are the year. Accepting the dry name is already a politics. haako wonti haako, every leaf becomes a leaf: the rain's advertisement. The dry does not advertise. It remains.",
        "prac": "Let someone else be the rain today. Keep one dry-season duty that does not compete for green.",
        "terms": kt(
            ("ndunngu", "rainy season — the namesake's title as visible increase; English 'prosperity' loses the climate"),
            ("ceedu", "dry season — the accepted name; not 'failure', a true half of the year"),
            ("haako", "leaf, foliage — the rain's proof; green as political theology"),
            ("min nganndi", "we know — the dry season's self-knowledge, without contest"),
        ),
        "res": res(
            ("Heraclitus B67, God is day night, winter summer", "Both make opposed seasons one truth rather than a ranking.", "Heraclitus's god is the identity of the pair; this Imam accepts being only the dry half."),
            ("Zhuāngzǐ, the useless and the useful, winter and summer trees", "Both refuse to let the green season be the only success.", "Zhuāngzǐ praises the unused; Fulde lets a namesake be rain and still keeps a dry-season office."),
        ),
    },
    {
        "n": 21,
        "reichardt": "Trad. I / XX, Bundu must move",
        "title": "The Vessel of Stones",
        "ful": "o heɓɓini njoru e kaaƴe; o yahi e mum e jam, o majjitaano hay gooto. O heɓɓini goɗɗo, o dogi; kaaƴe njani nano e nano. O wi'i: mo dilli jooni ko adannde; mo fadii haa ɓe njogitii-mo e sembe, ko ɗiɗaɓere.",
        "tr": "He filled a vessel with little stones and walked with it softly; he did not lose any. He filled another and ran; he lost the stones right and left. He said: whoever moves now resembles the first; whoever leaves it until he is driven by force is the second.",
        "comm": "Timing is the teaching, not the destination. Bundu refused and later moved with confusion — cows, goods, people lost in the forest. The parable was already the mercy. He fills a vessel with small stones, walks softly, loses none. He fills another, runs, loses stones right and left. Whoever moves now is the first; whoever waits until driven by force is the second. The contested move is to hear this as a travel tip. Futa Jalon Fulde makes a njoru of kaaƴe into a theology of when. Bundu's later panicked move is the second vessel already proven. The parable was the mercy they refused. This is highland counsel to a neighboring land, not a Futa Toro rope-and-well proverb, though both think in containers. Existentially: move one thing you will otherwise be forced to move. Carry it walking, not running. The teaching is against both premature flight and the pride of staying until the forest takes the cows. Soft walking is not slowness as virtue. It is the only pace at which the stones stay in the vessel. Force will make you run. Running is already the loss. e jam, in peace: the first vessel's pace. sembe, force: the second's driver. Choose the pace while you still can.",
        "prac": "Move one thing you will otherwise be forced to move. Carry it walking, not running.",
        "terms": kt(
            ("njoru", "vessel, container — the life that can hold or spill; English 'plan' is too mental"),
            ("kaaƴe", "stones, pebbles — the goods of a move; small, easy to lose at a run"),
            ("e jam", "in peace, softly — the pace that keeps the stones; not 'calmly' as mood"),
            ("sembe", "force, power — what drives the second vessel; the run is already the spill"),
        ),
        "res": res(
            ("Dhammapada 21, heedfulness is the path to the deathless", "Both make timing of attention the difference between keeping and spilling.", "The Dhammapada's heed is a path; Fulde's heed is a walking pace with a vessel of stones."),
            ("Marcus Aurelius, Meditations 4.26, each thing is done in its season", "Both refuse a forced out-of-season act.", "Marcus's season is inner assent; this parable is a highland people who will lose cows in a forest if they wait for force."),
        ),
    },
    {
        "n": 22,
        "reichardt": "Trad. I / XX, Alfa Othman's war dress",
        "title": "He Kept Silence Until They Came",
        "ful": "Sheikh anndi yimɓe-makko njaasi, ɓe nji'ii kirse konu-makko. Sheikh deeƴii haa ɓe ngari e yeeso-makko. Caggal ɗum o itti-mo e golle.",
        "tr": "The Sheikh knew that his people took offence when they saw the war dress of those men. The Sheikh kept silence till they came into his presence. After that he deposed him from his office.",
        "comm": "He does not soothe the envy in the yard. Silence until the face-to-face, then the act. The dress caused the offence; the office is what he removes. The Sheikh knows his people took offence at Alfa Othman's war dress. He keeps silence until they come into his presence. Then he deposes him. The contested move is to manage the corridor. Futa Jalon Fulde gives a sequence: knowledge, silence, presence, removal. The kirse, the war dress, bred envy in the yard. The sheikh will not comment there. He will not soothe. He waits for the face. Then he acts on the office, not on the cloth. Highland camp politics, not a Futa Toro mallol about not speaking of the father's marriage — though both know a silence that is not cowardice. Existentially: when a display in your circle breeds envy, do not comment in the corridor. Wait until the person is in front of you. Then act or refuse to act. Do not gossip the dress. The teaching splits the cause (the display) from the remedy (the office). Soothing the yard would have left the office intact and the envy fed. deeƴii, he kept silence, is the method. itti-mo e golle, he removed him from the work, is the act that silence made possible.",
        "prac": "When a display in your circle breeds envy, do not comment in the corridor. Wait until the person is in front of you. Then act or refuse to act. Do not gossip the dress.",
        "terms": kt(
            ("deeƴii", "he kept silence, he was still — method, not passivity; English 'waited' loses the closed mouth"),
            ("kirse", "war dress, military costume — the display that bred offence; not the crime, the spark"),
            ("yeeso-makko", "his face / his presence — the condition of the act; corridor speech is refused"),
            ("golle", "office, work, function — what is removed; the dress stays a dress, the office is the stake"),
        ),
        "res": res(
            ("Gospel of Thomas 6, do not lie and do not do what you hate, for all is revealed", "Both refuse a hidden corridor speech.", "Thomas universalizes reveal; Fulde sequences silence until the face, then a public removal."),
            ("Gaden, Pulaar Texts, Mallol 151, 'He Will Not Speak of His Father's Marriage' (Futa Toro)", "Both keep a silence that is honor, not fear.", "Gaden's mallol is a last fence on family speech in another dialect; this is a commander's silence until the offender is in front of him. Do not collapse them."),
        ),
    },
    {
        "n": 23,
        "reichardt": "Trad. II / XXI, Suware sends Sedi and Seri",
        "title": "There Is Your Abode",
        "ful": "ɓe mbi'i-mo: men ngarii to maa toraade-maa; caɗeele fumni e leydi-amen. O wi'i yo ɓe nge to leydi no me Futa Jallo — kodoŋ woni jibirde mo'on. O du'ani-ɓe.",
        "tr": "They said to him: we come unto thee to ask a favor; a trouble has befallen our land. He said they must go on until they reach the country called Futa Jallo — there is your abode. He prayed for them.",
        "comm": "Origin here is not a blood myth first. It is a sending. A Mandinka wali points two Arab-descended men at a highland and prays. Futa Jalon is an assigned home, not a found one. Sedi and Seri come to Suware: trouble has befallen our land; we ask a favor. He says go until you reach the country called Futa Jallo — there is your abode. He prays for them. The contested move is to treat Futa Jalon as an ancestral finding or a conquest-right. Tradition II in Reichardt is origin-speech: a Mandinka holy man assigns a highland to two men and prays. Blood may be in the background — Fezzan, Arab descent in the larger tale. The sentence that founds the home is a sending plus a duʿāʾ. This is not Futa Toro Pulaar's river-valley self-account, and it is not a Gaden mallol. Do not tell the highland as if it were the Senegal floodplain. Existentially: ask one living elder where your abode is — not where you prefer. Go as far as that sentence. Do not renegotiate the highland. The teaching is against both romantic wandering and blood-myth as first philosophy. Home can be a prayer someone else spoke over a place you had not chosen. jibirde, abode, is assigned. The prayer is the legal act.",
        "prac": "Ask one living elder where your abode is — not where you prefer. Go as far as that sentence. Do not renegotiate the highland.",
        "terms": kt(
            ("jibirde", "abode, dwelling-place — assigned, not discovered; English 'home' is preference; this is a pointed highland"),
            ("Futa Jallo", "Fuuta Jaloo — the Guinea highland as a named destination; not Futa Toro"),
            ("du'ani-ɓe", "he prayed for them — the founding act; sending without prayer would be mere geography"),
            ("caɗeele", "trouble, difficulty — what drives the asking; origin as flight, not as triumph"),
        ),
        "res": res(
            ("Lal Ded, vakh on the true home not being the house you were born in", "Both uncouple abode from first preference.", "Lal's home is inner Śiva; Suware points at a highland and prays. One is Kashmiri nakedness, the other a Mandinka sending."),
            ("Genesis 12:1, go to the land I will show you", "Both found a people by a sending toward an unseen land.", "Abram is sent by God; Sedi and Seri are sent by a Mandinka wali who also prays. The highland is named in advance."),
        ),
    },
    {
        "n": 24,
        "reichardt": "Trad. II / XXI, Almami Suri at Wosogorama",
        "title": "You Have Torn the Drum of the Unbelievers",
        "ful": "o sorti labi-makko o feri dundurundu. O arti Timbo o wi'i Karamoko Alfa: mi feri dunduru hefereeɓe. O wi'i-mo: a waɗii bone; musibba-meɗe ɓe ala ɗo.",
        "tr": "He drew his knife and cut up their kettle drum. He came to Karamoko Alfa and said: brother, I have torn the big drum of the unbelievers. He said to him: you have done mischief sadly; our family and friends are not there.",
        "comm": "Zeal that starts a holy war by cutting a drum is named mischief when it is done where your people are not. The first jihad of Futa Jalon begins as a kinship problem, not a triumph. Almami Suri cuts the kettle drum at Wosogorama, returns to Timbo, tells Karamoko Alfa: I have torn the big drum of the unbelievers. The answer: you have done mischief sadly; our family and friends are not there. The contested move is to hear the cut as the start of glory. Highland Fulde names it bone, mischief. The drum is a public instrument of people who are not yours. Zeal that cannot locate kin in the town is not yet a legal war. Tradition II will soon require a king for jihad to be legal. This unit is the prior disaster: freelance sacred vandalism. Do not collapse this with Futa Toro ethics; the drum and the highland Imam-founding are Futa Jalon's own beginning. Existentially: before you break a public instrument of people who are not yours, ask who will pay. If your family is not in that town, do not cut the drum. The teaching is against zeal that outruns kinship. dundurundu is not a theology. It is a drum. Cutting it where musibba-meɗe, our people, are absent, is already the mischief. The knife was sure. The kinship was not.",
        "prac": "Before you break a public instrument of people who are not yours, ask who will pay. If your family is not in that town, do not cut the drum.",
        "terms": kt(
            ("dundurundu / dunduru", "kettle drum, the big drum — a public instrument, not a doctrine; cutting it is an act against a town"),
            ("hefereeɓe", "unbelievers — Suri's name for the drum's people; Alfa will not let the name authorize the cut"),
            ("bone", "mischief, harm, wrong — the official name of the first cut; English 'zeal' is what Suri thought he had"),
            ("musibba-meɗe", "our family and friends — the missing condition; without them in the town the cut is freelance"),
        ),
        "res": res(
            ("Bhagavad Gītā 1.31–37, Arjuna's kinship-horror before the war", "Both make kin-location a condition of sacred violence.", "Arjuna sees his people on the field and will not fight; Alfa sees that his people are not in the town and names the cut mischief."),
            ("Yoruba òwe, 'Strife never begets a gentle child'", "Both refuse to let a first violent act found a gentle order.", "The òwe is proverbial genetics of strife; Fulde is the founding story of Futa Jalon's jihad as a kinship failure."),
        ),
    },
    {
        "n": 25,
        "reichardt": "Trad. II / XXI, council after Talansan",
        "title": "The War Is Not Legal Without a King",
        "ful": "ɓe kawritii fi laamu, sabu jihadi hasataa e ɓawa lamɗo. Mawɗo-maɓɓe wi'i yo ɓe lami Alfa mo Timbo.",
        "tr": "They met in deliberation in order to choose a king, because the war with infidels is not legal without a king. Their head man said they must crown the Alfa of Timbo.",
        "comm": "Violence that wants to call itself jihad requires a named political form. Futa Jalon refuses freelance sacred war. The king is a legal condition, not a prize. After Talansan they meet to choose a king, because jihadi hasataa e ɓawa lamɗo — the war with infidels is not legal without a king. Their head man says crown the Alfa of Timbo. The contested move is to treat the crown as loot from the war. Highland Fulde inverts the order: first a named responsible person, then the war may call itself jihad. Without a lamɗo the same fighting is illegal even to those who want it. This is Futa Jalon's political theology of Imamship, not Futa Toro proverb kingship — a king is not a comrade — and not a Senegal-valley mallol. Existentially: do not join a fight that has no named responsible person. If you are asked to fight, ask who is king of it. If no one is, leave. The teaching is against both anarchic holy war and the romance of the leaderless cause. A name you can hold to account is the minimum legality. The Alfa of Timbo is that name, not a trophy. The drum-cut of the previous unit is what this council is trying to make unrepeatable. hasataa, is not legal: the war's own jurists refuse the freelance.",
        "prac": "Do not join a fight that has no named responsible person. If you are being asked to fight, ask who is king of it. If no one is, leave.",
        "terms": kt(
            ("jihadi", "jihad, the war that wants a sacred name — illegal here without a king; English 'crusade' is the wrong religion"),
            ("lamɗo", "king — a legal condition of the war, not its prize"),
            ("hasataa", "is not legal, does not befit — a juristic negative; 'should not' is too mild"),
            ("kawritii", "they met, they assembled — deliberation as the form that makes a king, not a battlefield acclamation"),
        ),
        "res": res(
            ("Marcus Aurelius, Meditations 1.14, on a polity in which there is the same law for all", "Both make a named political form the condition of legitimate force.", "Marcus remembers a Stoic cosmopolis; Fulde requires an Imam of Timbo before the highland war may call itself jihad."),
            ("Gaden, Pulaar Texts, 'A Father's Counsel' (Futa Toro), a king is not a comrade", "Both refuse to confuse kingship with intimacy.", "Gaden's mallol is Futa Toro warning against false nearness to a king; this is Futa Jalon requiring a king so that war can be legal. Different dialect, opposite office of the crown."),
        ),
    },
    {
        "n": 26,
        "reichardt": "Trad. III / XXII, Modi Ibrahima Kabba at Kebali",
        "title": "The Blessings of the Elders Are Left to Us",
        "ful": "Modi Ibrahima Kabba wi'i: Almami, jooɗee; kala ko waɗata e maa waɗata e amen kala. Wata on kule. Barkewol mawɓe-meɗe ngol luti e amen; du'aaaji-maɓɓe o jaɓoto.",
        "tr": "Modi Ibrahima Kabba said: Almami, sit; anything that will be sufficient for you will do for all of us. Fear ye not; the blessings of our elders are left to us; their prayers He will answer.",
        "comm": "After flight and slaughter, the teaching is hospitality plus inheritance. Sufficiency is shared, not ranked. The elders' blessing is a remainder that still works. Modi Ibrahima Kabba at Kebali says: Almami, sit; anything sufficient for you will do for all of us. Fear not; the blessings of our elders are left to us; their prayers He will answer. Tradition III — Masina war, flight — ends in a highland welcome. The contested move is to treat refugees as a lesser plate and the elders as a finished past. Futa Jalon Fulde makes barkewol mawɓe a remainder that still operates. Sufficiency is one measure for host and guest. Sit. Do not fear. The prayers of the dead are still being answered. This is not Futa Toro milk-transmission; it is blessing as leftover force after a massacre. Existentially: take in one person who has fled a failure. Give them what is sufficient for you, not a lesser plate. Say the elders' blessing is still here. The teaching is against both charity-as-hierarchy and the idea that a broken people have no inheritance left to host with. jooɗee, sit: the first hospitality is a seat, not a speech. luti e amen, left with us: the elders are not gone as force. Their duʿāʾ is still a working remainder.",
        "prac": "Take in one person who has fled a failure. Give them what is sufficient for you, not a lesser plate. Say the elders' blessing is still here.",
        "terms": kt(
            ("barkewol", "blessing (baraka in Fulde) — a remainder that still works; English 'blessing' is a wish; this is leftover force"),
            ("mawɓe", "elders, the old ones — the source of the remainder; not 'ancestors' as a cult-name only"),
            ("luti", "is left, remains — inheritance as what was not taken by the slaughter"),
            ("jooɗee", "sit (imperative) — hospitality as a seat before it is a speech"),
        ),
        "res": res(
            ("Gaden, Pulaar Texts, Mallol 145, 'What the Cow Ate, the Heifer Suckles' (Futa Toro)", "Both transmit a prior generation's substance into the living.", "The mallol is milk in another dialect's proverb; this is baraka left after flight and slaughter in Futa Jalon Fulde. Same family of thought, not the same speech."),
            ("Yoruba òwe, 'Full-belly child says to hungry-belly child'", "Both know the temptation of a ranked plate.", "The òwe mocks the full child's speech; Kabba forbids the ranking in advance: what suffices for the Almami suffices for all."),
        ),
    },
]


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.{SLUG}_{n:03d}"
    hero = n in HEROES
    original = u["ful"]
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
        "source_id": f"FJF_{n:03d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": u["reichardt"],
        "title": u["title"],
        "unit_type": "verse",
        "commentary": u["comm"],
        "themes": ["futa jalon", "fulde", "umar tal", "living speech"],
        "tags": [SLUG, "futa-jalon", "fulde", "reichardt"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "category": "fulde",
            "verse": str(n),
            "reichardt": u["reichardt"],
            "cultural_context": NOTE,
            "original_source": "Reichardt, Grammar of the Fulde Language (London: CMS, 1876), Part II traditions",
            "original_reliability": "SOURCED — Reichardt 1876 Latin Fulde (Futa Jalon), OCR-cleaned from IA grammarfuldelan00reicgoog; not Gaden, not Koumen",
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
    if len(UNITS) < 26:
        raise SystemExit(f"floor is 26 units, got {len(UNITS)}")
    if len(HEROES) != 10:
        raise SystemExit(f"need 10 heroes, got {sorted(HEROES)}")
    missing = HEROES - {u["n"] for u in UNITS}
    if missing:
        raise SystemExit(f"heroes not in UNITS: {sorted(missing)}")
    for u in UNITS:
        if len(u["res"]) != 2:
            raise SystemExit(f"unit {u['n']} needs exactly 2 resonances, got {len(u['res'])}")
        if not (2 <= len(u["terms"]) <= 4):
            raise SystemExit(f"unit {u['n']} needs 2–4 terms, got {len(u['terms'])}")
        if "In this passage" in u["comm"]:
            raise SystemExit(f"unit {u['n']} opens filler: In this passage")
    os.makedirs(OUT, exist_ok=True)
    ids = [write_unit(u) for u in UNITS]
    keep_files = {f"{uid.replace('.', '_')}.yml" for uid in ids}
    removed = 0
    for name in os.listdir(OUT):
        if name.endswith(".yml") and name not in keep_files:
            os.remove(os.path.join(OUT, name))
            removed += 1
    hero_ids = [f"{SLUG}.{SLUG}_{u['n']:03d}" for u in UNITS if u["n"] in HEROES]
    print(f"{SLUG}: {len(ids)} units (min 26) · heroes {[u['n'] for u in UNITS if u['n'] in HEROES]}")
    print(f"tts_key ids: {hero_ids}")
    print(f"wrote {len(ids)} yml to {OUT}" + (f" (removed {removed} stale)" if removed else ""))
    print("commentary words:", [(u["n"], len(u["comm"].split())) for u in UNITS])
    print("first:", f"{ids[0].replace('.', '_')}.yml")
    print("last:", f"{ids[-1].replace('.', '_')}.yml")
    return len(ids)


if __name__ == "__main__":
    build()
