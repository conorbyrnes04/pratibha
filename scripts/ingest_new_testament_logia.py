#!/usr/bin/env python3
"""Ingest mystical logia of Jesus from the Nestle 1904 Greek gospels.

Paired sibling of `ingest_gospel_of_mary.py` (same family: living sayings).
English is a Pratibha pd_render from Nestle's Koine; ASV 1901 informs cadence
only. Do not crib NIV, NRSV, or any living Bible.
"""
from __future__ import annotations

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/new_testament_logia")
GREEK_DIR = os.path.join(ROOT, "data/raw_texts/pd/greek/nestle1904")
SLUG = "new_testament_logia"
COLL = "Logia of Jesus"
PROV = (
    "English is a Pratibha rendering (2026) from Eberhard Nestle, "
    "Novum Testamentum Graece (1904 — public domain). Cadence informed by the "
    "American Standard Version (1901 — public domain). Not NIV, NRSV, or any "
    "copyrighted Bible."
)
NOTE = (
    "Selected gospel sayings of Jesus on the kingdom within, the single eye, "
    "abiding, and the Word — a living-speech companion to the Gospel of Thomas "
    "and the Gospel of Mary. Not a gospel harmony and not Paul."
)
HEROES = {1, 2, 4, 5, 7, 15, 19, 24, 26, 27}

_OSIS = {"Matthew": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John"}
_FILES = {
    "Matthew": "01-matthew.xml",
    "Mark": "02-mark.xml",
    "Luke": "03-luke.xml",
    "John": "04-john.xml",
}
_GREEK_CACHE: dict[str, dict[str, str]] = {}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


def _parse_book(book: str) -> dict[str, str]:
    if book in _GREEK_CACHE:
        return _GREEK_CACHE[book]
    path = os.path.join(GREEK_DIR, _FILES[book])
    xml = open(path, encoding="utf-8").read()
    verses: dict[str, str] = {}
    parts = re.split(r'<milestone unit="verse" id="([^"]+)"/>', xml)
    for i in range(1, len(parts), 2):
        chunk = parts[i + 1]
        tokens = re.findall(r"<(w)[^>]*>([^<]+)</w>|<(pc)>([^<]*)</pc>", chunk)
        text: list[str] = []
        for tag1, w, tag2, pc in tokens:
            if tag1 == "w":
                text.append(w)
            elif text:
                text[-1] = text[-1] + pc
            else:
                text.append(pc)
        verses[parts[i]] = " ".join(text)
    _GREEK_CACHE[book] = verses
    return verses


def greek_for(book: str, ch: int, start: int, end: int) -> str:
    verses = _parse_book(book)
    osis = _OSIS[book]
    return " ".join(verses[f"{osis}.{ch}.{v}"] for v in range(start, end + 1))


UNITS: list[dict] = [
    {
        "n": 1,
        "title": "The kingdom does not come with observation",
        "book": "Luke",
        "ch": 17,
        "a": 20,
        "b": 21,
        "tr": "Asked by the Pharisees when the kingdom of God is coming, he answered them, The kingdom of God does not come with observation, nor will they say, Look here, or There. For look: the kingdom of God is within you.",
        "comm": "The question wants a calendar. Jesus refuses a spectacle you could point at. Entos hymōn can mean among you or within you — the Greek will not close the case. What it does close is the pointing-away. Observation (paratērēsis) is the watcher’s stance: waiting for a sign so you do not have to enter. Thomas will later say inside and outside; Mary will say the Human One exists within. Luke’s punch is already enough: if you are still asking when, you have already mislocated it. The misconception this gate blocks is that the kingdom is an event on the horizon rather than a presence that will not perform for inspection.",
        "prac": "Catch one ‘when will it come’ today — a mood, a news cycle, a spiritual timetable. Drop the when. Look once at what is already within reach, and stay there for ten breaths.",
        "terms": kt(
            ("βασιλεία", "kingdom — not a later regime; the rule already at issue"),
            ("παρατήρησις", "observation / watching-for-signs — the stance that postpones entry"),
            ("ἐντὸς ὑμῶν", "within / among you — interior and social at once; do not pick only one"),
        ),
        "res": res(
            ("Gospel of Thomas 3", "Leaders who point to sky or sea mislead; the kingdom is inside you and outside you.", "Thomas doubles the location; Luke refuses the spectacle and leaves entos open."),
            ("Gospel of Mary, BG 8502 pp. 8–9", "Do not be misled by Look over here; the Son of Humanity exists within you.", "Mary names the Human One within; Luke names the kingdom. Same refusal of pointing."),
        ),
    },
    {
        "n": 2,
        "title": "Blessed are the poor in spirit",
        "book": "Matthew",
        "ch": 5,
        "a": 3,
        "b": 10,
        "tr": "Blessed are the poor in spirit, for theirs is the kingdom of the heavens. Blessed are those who mourn, for they will be comforted. Blessed are the meek, for they will inherit the earth. Blessed are those who hunger and thirst for righteousness, for they will be filled. Blessed are the merciful, for they will be shown mercy. Blessed are the pure in heart, for they will see God. Blessed are the peacemakers, for they will be called sons of God. Blessed are those persecuted for righteousness, for theirs is the kingdom of the heavens.",
        "comm": "Makarios is not a mood of cheer. It is a verdict on a condition the world does not congratulate. The first and last beatitudes already possess the kingdom — present tense — so poverty of spirit and persecution are not waiting-rooms. Purity of heart is the seeing-condition: katharoi tē kardia, the unmixed inner chamber Matthew will later name as the secret room. The contested claim is that the blessed life is not an achievement stacked on top of a secure self. It is what the emptied, mourning, meek, hungry, merciful, unmixed, peacemaking, and hunted already are. Do not turn this into a personality quiz. It is an architecture of the kingdom from below.",
        "prac": "Name one beatitude you are actually in today (poverty, mourning, hunger — not the one you admire). Do the next ordinary act from inside that condition, without upgrading it.",
        "terms": kt(
            ("μακάριοι", "blessed / fortunate — a verdict, not a feeling of being upbeat"),
            ("πτωχοὶ τῷ πνεύματι", "poor in spirit — emptied of claim, not merely sad"),
            ("καθαροὶ τῇ καρδίᾳ", "pure in heart — unmixed; the organ that sees God"),
        ),
        "res": res(
            ("Gospel of Thomas 54", "Blessed are the poor, for yours is the kingdom of heaven.", "Thomas keeps poor without ‘in spirit’; Matthew interiorizes the poverty."),
            ("Kaṭha Upaniṣad 1.2.23", "This Self is not attained by the weak, nor by much hearing.", "Both refuse force as the door; the Upaniṣad still names a Self to be attained, Matthew a kingdom already theirs."),
        ),
    },
    {
        "n": 3,
        "title": "You are the light of the world",
        "book": "Matthew",
        "ch": 5,
        "a": 14,
        "b": 16,
        "tr": "You are the light of the world. A city set on a mountain cannot be hidden. Nor do they light a lamp and put it under the measuring-basket, but on the lampstand, and it shines for all who are in the house. So let your light shine before people, that they may see your good works and glorify your Father in the heavens.",
        "comm": "You are — not you should become — the light of the world. The city and the lamp are already placed; the only possible failure is covering. Works here are not a résumé. They are what light does when it is not hidden: they make the Father visible, not the ego impressive. John will later have Jesus say I am the light of the world. Matthew gives that sentence to the crowd on the hill. The misconception: that humility means remaining unlit, or that shining means self-display. The lampstand is public; the glory is not yours.",
        "prac": "Do one good act today that you would rather keep under the basket (kindness, truth, repair). Do not announce it. Let the work be the shine.",
        "terms": kt(
            ("φῶς τοῦ κόσμου", "light of the world — identity given, not a later promotion"),
            ("μόδιος", "the measuring-basket — the ordinary cover we put over a lamp"),
            ("καλὰ ἔργα", "good works — what light does in the house, not a private virtue-score"),
        ),
        "res": res(
            ("Gospel of Thomas 24", "There is light within a person of light, and it lights the whole world.", "Thomas locates light within a type of person; Matthew locates it as the crowd’s public being."),
            ("John 8:12", "I am the light of the world; the follower will have the light of life.", "John centers the ‘I am’; Matthew gives the light to ‘you’ as a city that cannot hide."),
        ),
    },
    {
        "n": 4,
        "title": "Pray to the Father who is in secret",
        "book": "Matthew",
        "ch": 6,
        "a": 6,
        "b": 6,
        "tr": "But you, when you pray, go into your inner room, and having shut your door, pray to your Father who is in the secret place; and your Father who sees in the secret place will repay you.",
        "comm": "The inner room (tameion) is a storeroom, not a chapel. Prayer here is not performance for an audience and not a technique stacked on public piety. Shut the door: stop leaking attention outward. The Father is already in the kryptō — the hidden — and sees there. Recompense is not a later prize; it is that the hidden is met by the Hidden. The Cloud of Unknowing will make a practice of this chamber. Matthew already forbids using God as a stage. The misconception: that louder or longer prayer is more real than the closed door.",
        "prac": "Once today, go into an actual room or a pause in the day. Shut the door (or the phone). Pray one sentence to the Father in secret. Do not report it.",
        "terms": kt(
            ("ταμεῖον", "inner room / storeroom — the closed chamber, not the street-corner"),
            ("κρυπτῷ", "the secret / hidden — where the Father already is"),
            ("προσεύχῃ", "when you pray — assumed as practice, then relocated inward"),
        ),
        "res": res(
            ("The Cloud of Unknowing, ch. 3", "A naked intent toward God in a cloud of forgetting of all else.", "The Cloud trains the dart of love; Matthew simply shuts the door."),
            ("Gospel of Thomas 14", "If you pray you will be condemned — public piety can manufacture the stain.", "Thomas warns against prayer as display; Matthew keeps prayer and hides it."),
        ),
    },
    {
        "n": 5,
        "title": "If the eye is single, the body is full of light",
        "book": "Matthew",
        "ch": 6,
        "a": 22,
        "b": 23,
        "tr": "The lamp of the body is the eye. If then your eye is single, your whole body will be full of light. But if your eye is evil, your whole body will be full of darkness. If then the light in you is darkness, how great is the darkness.",
        "comm": "Haplous means single, simple, unmixed — not ‘healthy’ as a medical compliment. The eye is the body’s lamp: attention is what lights the whole field. An evil eye (ponēros) is the divided, stingy, appraising glance. If the organ of seeing is already dark, more information will not help; the light-in-you has become darkness, and that is the great dark. Thomas’s ‘make the two one’ and Mary’s unwavering mind are the same architecture. The misconception: that you need more lights. You need an unsplit eye.",
        "prac": "For five minutes, look at one thing (a face, a page, a tree) without the second glance that compares or acquires. When the eye splits, name it and return.",
        "terms": kt(
            ("ἁπλοῦς", "single / simple / unmixed — the unsplit eye, not mere eyesight"),
            ("λύχνος", "lamp — the eye as the lighting of the whole body"),
            ("πονηρός", "evil (eye) — the stingy, double, appraising look"),
        ),
        "res": res(
            ("Gospel of Thomas 22", "When you make the two one, and the inside like the outside — then you will enter.", "Thomas sequences a unification; Matthew locates the split in the eye itself."),
            ("Gospel of Mary, BG 8502 p. 10", "Where the mind is, there is the treasure; blessed is the one who does not waver.", "Mary’s unwavering nous is Matthew’s single eye under another name."),
        ),
    },
    {
        "n": 6,
        "title": "Ask, seek, knock",
        "book": "Matthew",
        "ch": 7,
        "a": 7,
        "b": 8,
        "tr": "Ask, and it will be given you; seek, and you will find; knock, and it will be opened to you. For everyone who asks receives, and the one who seeks finds, and to the one who knocks it will be opened.",
        "comm": "Three imperatives, three futures that are already the law of this kingdom. This is not a vending-machine promise. Asking, seeking, knocking are the same motion as the single eye and the shut door: a directed need that does not wander. Thomas 2 adds that finding disturbs, then astonishes, then makes one rule. Matthew stops at opened. The contested claim is that the door is not locked from the other side. The failure is not God’s reluctance. It is that we stop knocking because we wanted a spectacle (Luke 17) instead of a door.",
        "prac": "Name one true ask (not a wish-list). Seek it in one concrete place today. Knock once — an email, a confession, a sitting — and do not decorate the wait.",
        "terms": kt(
            ("αἰτεῖτε", "ask — present imperative: keep asking, not once-and-done"),
            ("ζητεῖτε", "seek — motion toward what is not yet in hand"),
            ("κρούετε", "knock — the door is real; passivity is not faith"),
        ),
        "res": res(
            ("Gospel of Thomas 2", "The seeker should not stop until they find; when they find they will be disturbed.", "Thomas adds shock after finding; Matthew promises opening without the disturbance."),
            ("Lalla, ‘I found him in my own house’", "Seeking abroad failed; the found was already home.", "Lalla ends seeking by recognition; Matthew keeps the three verbs in motion."),
        ),
    },
    {
        "n": 7,
        "title": "My yoke is kind, and my burden light",
        "book": "Matthew",
        "ch": 11,
        "a": 25,
        "b": 30,
        "tr": "At that time Jesus said, I thank you, Father, Lord of heaven and earth, that you hid these things from the wise and understanding and revealed them to infants. Yes, Father, for so it was well-pleasing before you. All things have been handed over to me by my Father, and no one knows the Son except the Father, nor does anyone know the Father except the Son and anyone to whom the Son is willing to reveal him. Come to me, all who labor and are heavy-laden, and I will give you rest. Take my yoke upon you and learn from me, for I am meek and lowly in heart, and you will find rest for your souls. For my yoke is kind, and my burden is light.",
        "comm": "Revelation bypasses the credentialed. Infants receive what sophoi cannot. Then the Johannine-sounding claim: mutual knowledge of Father and Son, given as gift. The invitation is not to a lighter ideology. It is to a yoke — still a yoke — that is chrēstos, kind, useful, not cruel. Rest (anapausis) is what Mary’s soul later receives in silence. Labor and burden here are the extra law, the second Moses Mary forbids. The misconception: that following Jesus is a heavier religion. He offers a yoke that does not grind, and a heart from which to learn meekness, not a new performance.",
        "prac": "Name one religious or moral extra you are hauling. Set it down for today. Take one actual task as a kind yoke — done meekly, without the performance.",
        "terms": kt(
            ("νηπίοις", "infants / babes — the ones to whom the hidden is shown"),
            ("ζυγός", "yoke — still a binding; the shock is that it is kind"),
            ("ἀνάπαυσις", "rest — given, then found in the soul under the yoke"),
        ),
        "res": res(
            ("Gospel of Mary, BG 8502 pp. 8–9", "Do not lay down any rule beyond what I gave you, lest you be bound by it.", "Mary forbids the extra statute; Matthew offers a yoke that is not that statute."),
            ("Gospel of Thomas 90", "Come to me, for my yoke is easy and my lordship is mild, and you will find rest.", "Thomas is almost the same saying; Matthew embeds it in hidden-from-the-wise and mutual knowing."),
        ),
    },
    {
        "n": 8,
        "title": "Treasure hidden in the field",
        "book": "Matthew",
        "ch": 13,
        "a": 44,
        "b": 46,
        "tr": "The kingdom of the heavens is like a treasure hidden in the field, which a man found and hid, and from his joy he goes and sells all he has and buys that field. Again, the kingdom of the heavens is like a merchant seeking fine pearls; and finding one pearl of great price, he went and sold all he had and bought it.",
        "comm": "Two findings: accident in a field, and a merchant who was already seeking. Both end in selling everything. Joy, not grim duty, funds the sale. The treasure is hidden — same kryptos as the inner room — and then hidden again by the finder, because it is not for display. Mary: where the mind is, there is the treasure. Here the treasure is a field you have to purchase with your whole portfolio. The misconception: that the kingdom is an add-on you can keep alongside the old goods. You cannot. The pearl costs the rest of the string.",
        "prac": "Name one ‘fine pearl’ you actually found (a practice, a person, a truth). Sell one lesser good today that competes with it — time, a grudge, a vanity purchase.",
        "terms": kt(
            ("θησαυρῷ κεκρυμμένῳ", "treasure hidden — already in the field; finding is not creating"),
            ("μαργαρίτης", "pearl — one, costly; the many goodly pearls were not enough"),
            ("πωλεῖ πάντα", "sells all — joy’s economics, not ascetic bookkeeping"),
        ),
        "res": res(
            ("Gospel of Thomas 76", "The merchant found a pearl and sold the whole load; seek the unfailing treasure.", "Thomas and Matthew share the pearl; Thomas moralizes ‘unfailing,’ Matthew stays in the joy of the sale."),
            ("Gospel of Mary, BG 8502 p. 10", "Where the mind is, there is the treasure.", "Mary locates treasure in unwavering nous; Matthew locates it as a field that costs everything."),
        ),
    },
    {
        "n": 9,
        "title": "Whoever would save their life will lose it",
        "book": "Matthew",
        "ch": 16,
        "a": 24,
        "b": 26,
        "tr": "Then Jesus said to his disciples, If anyone wants to come after me, let them deny themselves and take up their cross and follow me. For whoever wants to save their life will lose it, and whoever loses their life for my sake will find it. For what will a person be profited if they gain the whole world and forfeit their life? Or what will a person give in exchange for their life?",
        "comm": "Psychē is life/soul — the self you are trying to keep intact. Saving it is the strategy that loses it. The cross is not jewelry; it is the instrument already visible in the road ahead. Follow is the same verb as Mary’s Follow him (the Human One within), now given a cost. The world as profit is the evil eye’s ledger. There is no exchange rate for the psychē once forfeited. The misconception: that spirituality is self-improvement of the very self that must be denied. Denial here is not self-hatred. It is refusing to make the psychē the project.",
        "prac": "Notice one move today that is ‘saving your life’ (image, winning, not looking foolish). Drop it once. Take the next true step as if the psychē were not the prize.",
        "terms": kt(
            ("ψυχή", "life / soul / self — what clinging saves and so loses"),
            ("ἀπαρνησάσθω ἑαυτόν", "let them deny themselves — not self-loathing; refusing the self as project"),
            ("σταυρός", "cross — the actual cost of following, not a metaphor for inconvenience"),
        ),
        "res": res(
            ("Gospel of Thomas 55", "Whoever does not hate father and mother, and take up the cross as I do, will not be worthy of me.", "Thomas sharpens to hate/worthy; Matthew stays with lose/find of the psychē."),
            ("Bhagavad Gītā 2.47", "You have a claim to the action, never to its fruits.", "The Gītā releases fruit; Jesus releases the life that was being saved as fruit."),
        ),
    },
    {
        "n": 10,
        "title": "Unless you turn and become as children",
        "book": "Matthew",
        "ch": 18,
        "a": 3,
        "b": 3,
        "tr": "Truly I tell you, unless you turn and become as the little children, you will not enter the kingdom of the heavens.",
        "comm": "Straphēte: turn, convert, reverse. Becoming as children is not cute innocence. It is the infant of 11:25, the one to whom the hidden is shown. Entry is blocked to the unturned adult — the one still watching for the kingdom with observation. Thomas 22 makes the child a unification of two into one. Matthew asks for a turn. The misconception: that maturity in the kingdom is more knowledge. It is a reversal of the knowing-stance that made you unteachable.",
        "prac": "In one conversation today, drop the need to be the adult in the room. Ask a real question. Receive an answer without improving it.",
        "terms": kt(
            ("στραφῆτε", "turn / convert — a reversal, not a mood of sweetness"),
            ("παιδία", "little children — the receptive stature of 11:25’s infants"),
            ("εἰσέλθητε", "you will not enter — the kingdom has a door; unturned adulthood is not it"),
        ),
        "res": res(
            ("Gospel of Thomas 22", "These infants being suckled are like those who enter the kingdom.", "Thomas uses the child as an image of making two one; Matthew uses turning as the condition."),
            ("Matthew 11:25", "Hidden from the wise, revealed to infants.", "Same stature; 18:3 makes it a requirement for entry, not only a fact of revelation."),
        ),
    },
    {
        "n": 11,
        "title": "Where two or three are gathered",
        "book": "Matthew",
        "ch": 18,
        "a": 20,
        "b": 20,
        "tr": "For where two or three are gathered in my name, there I am in the midst of them.",
        "comm": "Presence does not wait for a quorum, a temple, or a hierarchy. Two or three, gathered into the name — into the meaning and claim of who he is — and he is already in the middle. John 14 will intensify this to we will make our abode. Matthew’s version is social and small. The misconception: that Christ is located in the large, the official, or the solitary virtuoso. Midst (en mesō) is a between, like Mary’s nous between soul and spirit. You do not produce him by gathering. You discover he was the middle.",
        "prac": "Sit with one or two people (or a sincere thread) without performing. Gather in the name — meaning, tell the truth. Notice the middle. Do not chair it.",
        "terms": kt(
            ("συνηγμένοι", "gathered — a real together, not a crowd-count"),
            ("εἰς τὸ ἐμὸν ὄνομα", "into my name — into his claim and presence, not a slogan"),
            ("ἐν μέσῳ", "in the midst — the between where he already is"),
        ),
        "res": res(
            ("John 14:23", "We will come to the one who loves and keeps the word, and make our abode.", "John is indwelling of Father and Son in the lover; Matthew is presence in a small gathering."),
            ("Gospel of Thomas 30", "Where there are three gods, they are gods; where two or one, I am with them.", "Thomas is riddling and solitary-capable; Matthew needs at least two."),
        ),
    },
    {
        "n": 12,
        "title": "The seed grows, and he does not know how",
        "book": "Mark",
        "ch": 4,
        "a": 26,
        "b": 29,
        "tr": "So the kingdom of God is as if a man should throw seed on the earth, and should sleep and rise, night and day, and the seed should sprout and lengthen, he does not know how. The earth bears fruit of itself — first the blade, then the ear, then the full grain in the ear. And when the fruit gives itself, at once he sends the sickle, because the harvest has come.",
        "comm": "Mark’s kingdom is agricultural and involuntary. The sower sleeps. Automatē — the earth bears of itself. Knowledge of how is refused. This is the opposite of spiritual engineering. You throw, you sleep, you rise; the stages are the earth’s. Harvest is timing, not technique. The misconception: that you must understand the mechanism of growth to be in the kingdom. The sickle is not anxiety. It is recognizing when the fruit has given itself.",
        "prac": "Throw one seed today (a true word, a practice, an apology). Then sleep — do not check it hourly. When a blade appears, do not yank it into an ear.",
        "terms": kt(
            ("αὐτομάτη", "of itself — the earth’s own bearing, not the sower’s cleverness"),
            ("οὐκ οἶδεν αὐτός", "he himself does not know — ignorance as the honest condition of growth"),
            ("θερισμός", "harvest — when the fruit gives itself, not when you are impatient"),
        ),
        "res": res(
            ("Gospel of Thomas 9", "The sower’s seed: some on the path, some eaten, some that made fruit.", "Thomas stresses mixed soils; Mark stresses that even good growth is not known-how."),
            ("Tao Te Ching 37", "The Way does nothing, yet nothing is left undone.", "Laozi’s wu-wei is cosmic; Mark’s automatē is a field the sleeper does not manage."),
        ),
    },
    {
        "n": 13,
        "title": "What does it profit to gain the whole world?",
        "book": "Mark",
        "ch": 8,
        "a": 34,
        "b": 36,
        "tr": "Calling the crowd with his disciples, he said, If anyone wants to come after me, let them deny themselves and take up their cross and follow me. For whoever wants to save their life will lose it, and whoever loses their life for my sake and the gospel’s will save it. For what does it profit a person to gain the whole world and forfeit their life?",
        "comm": "Mark adds the crowd to the disciples — this is not inner-circle advice — and adds ‘and the gospel’s’ to the losing. The public is implicated. Profit (ōphelei) is the ledger-word. The whole world on one side, the psychē on the other: there is no profit in that trade. Matthew’s parallel is here because Mark’s version is the harsher, more public one. The misconception: that you can keep the world as gain and the soul as a side account. Mark will not open the second account.",
        "prac": "Write down one ‘world-gain’ you are chasing this week. Ask: if this costs the psychē, is it profit? Cancel or shrink one piece of the chase.",
        "terms": kt(
            ("εὐαγγέλιον", "gospel / good news — Mark adds it as the other name of the losing"),
            ("ὠφελεῖ", "profits — the market verb; the soul is not a commodity that survives the trade"),
            ("ὄχλον", "the crowd — the saying is not withheld from the many"),
        ),
        "res": res(
            ("Matthew 16:24–26", "The same lose/find, with ‘in exchange for his life.’", "Matthew is to disciples; Mark pulls the crowd in and names the gospel as co-cause."),
            ("Ecclesiastes 1:3", "What profit for a man in all his labor under the sun?", "Qoheleth finds vanity in labor; Mark finds forfeiture of the psychē in world-gain."),
        ),
    },
    {
        "n": 14,
        "title": "Fear not, little flock",
        "book": "Luke",
        "ch": 12,
        "a": 32,
        "b": 32,
        "tr": "Fear not, little flock, for it is your Father’s good pleasure to give you the kingdom.",
        "comm": "Mikron poimnion: not a triumphant church, a small flock. The kingdom is given because the Father eudokēsen — was well pleased — not because the flock enlarged itself. Luke 17 said the kingdom does not come with observation; here it is gift to the small. Mary’s disciples weep that they cannot go to the Gentiles. This sentence is the counter: smallness is not the obstacle. Fear is. The misconception: that the kingdom is withheld until you are many, safe, or impressive. It is the Father’s pleasure to give it to the little.",
        "prac": "Where you are shrinking from a true small work because it is small, do it. Say, internally: little flock. Do not wait to be a crowd.",
        "terms": kt(
            ("μικρὸν ποίμνιον", "little flock — the honest size; not a failure of mission"),
            ("εὐδόκησεν", "it pleased / he was well-pleased — gift from pleasure, not from your leverage"),
            ("δοῦναι", "to give — the kingdom is given, not seized by observation"),
        ),
        "res": res(
            ("Luke 17:20–21", "The kingdom does not come with observation; it is within you.", "17 locates; 12:32 gives. Together: not a spectacle, and not withheld from the small."),
            ("Gospel of Thomas 107", "The shepherd leaves the ninety-nine for the one lost sheep — the one is the large.", "Thomas inverts size toward the lost one; Luke consoles the flock that knows it is little."),
        ),
    },
    {
        "n": 15,
        "title": "In the beginning was the Word",
        "book": "John",
        "ch": 1,
        "a": 1,
        "b": 5,
        "tr": "In the beginning was the Word, and the Word was with God, and the Word was God. This one was in the beginning with God. All things came to be through him, and without him not even one thing came to be that has come to be. In him was life, and the life was the light of human beings. And the light shines in the darkness, and the darkness did not overtake it.",
        "comm": "Logos is not a later book. It is beginning, relation (pros ton Theon), and identity (Theos ēn ho Logos) without collapsing the with. Life in him is the light of humans — so light is not information; it is living. The darkness does not katelaben: overtake, grasp, comprehend. Failure of the dark is both ontological and epistemic. This is the Johannine ground of every later ‘I am.’ The misconception: that Word means Bible, or that light is a metaphor for being clever. John starts before Moses, before the hill, with a shining the dark cannot seize.",
        "prac": "Before you speak one necessary sentence today, pause. Let the sentence come from life, not from winning. If darkness tries to grasp it (cynicism, display), do not let it.",
        "terms": kt(
            ("Λόγος", "Word / logos — beginning, with-God, and God; not a written volume"),
            ("ζωή", "life — the content of the light, not biological trivia"),
            ("κατέλαβεν", "overtake / grasp / comprehend — what the darkness failed to do to the light"),
        ),
        "res": res(
            ("Genesis 1:1–3", "In the beginning God created; let there be light.", "Genesis has God speaking light into a void; John has the Word as the beginning in which light already lives."),
            ("Plotinus, Ennead V.1", "The Intellectual-Principle is from the One, and is all things as thought.", "Plotinus ranks One–Nous–Soul; John will not rank the Word as a second god, and binds light to a history the dark cannot seize."),
        ),
    },
    {
        "n": 16,
        "title": "The true light lights every human",
        "book": "John",
        "ch": 1,
        "a": 9,
        "b": 13,
        "tr": "The true light, which lights every human, was coming into the world. He was in the world, and the world came to be through him, and the world did not know him. He came to his own, and his own did not receive him. But as many as received him, he gave them authority to become children of God, to those who believe in his name, who were born not of bloods, nor of the will of flesh, nor of the will of a man, but of God.",
        "comm": "Every human is lit — phōtizei panta anthrōpon — before the reception-plot. The tragedy is not that light was scarce. It is that the world made through him did not know him, and his own did not receive. Becoming children is given as exousia, authority, not a mood of niceness. Birth from God is set against bloods, flesh-will, male-will: lineage and desire do not produce this child. Mary’s ‘he made us Human’ is the Coptic cousin. The misconception: that some people have no light, or that child-of-God is an ethnicity. The light is already on everyone; reception is the crisis.",
        "prac": "Treat one person you had written off as unlit as already lit by the true light. Receive them once without the old story. Notice what that does to your own reception.",
        "terms": kt(
            ("τὸ φῶς τὸ ἀληθινόν", "the true light — not a rival lamp; the one that lights every human"),
            ("ἐξουσίαν τέκνα Θεοῦ", "authority to become children of God — a granted stature, not a bloodline"),
            ("οὐκ ἐξ αἱμάτων", "not of bloods — descent and will-of-man are refused as the cause"),
        ),
        "res": res(
            ("Gospel of Thomas 3", "When you know yourselves you will know you are children of the living Father.", "Thomas ties childship to self-knowledge; John ties it to receiving the light the world refused."),
            ("Gospel of Mary, BG 8502 p. 9", "He has prepared us and made us Human.", "Mary’s Human is the stature given to the weeping circle; John’s children of God are born not of bloods."),
        ),
    },
    {
        "n": 17,
        "title": "Born of water and Spirit",
        "book": "John",
        "ch": 3,
        "a": 5,
        "b": 8,
        "tr": "Jesus answered, Truly, truly I tell you, unless someone is born of water and Spirit, they cannot enter the kingdom of God. What is born of the flesh is flesh, and what is born of the Spirit is spirit. Do not marvel that I said to you, You must be born from above. The wind blows where it wills, and you hear its sound, but you do not know where it comes from or where it goes. So is everyone born of the Spirit.",
        "comm": "Anōthen: from above / again. Nicodemus hears a second time; Jesus means origin. Flesh generates flesh; Spirit generates spirit. Water and Spirit are the condition of entry — not observation, not the extra law. Pneuma is wind and Spirit at once: you hear the voice, you do not map the source. Mark’s sower who does not know how is the same honesty. The misconception: that rebirth is a decision you can schedule, or a feeling you can verify. It is a birth whose origin you do not manage, like wind.",
        "prac": "Stand in actual wind or at an open window for one minute. Hear the sound. Do not name where it came from. Ask to be that kind of born, then go do the next task.",
        "terms": kt(
            ("ἄνωθεν", "from above / again — origin, which Nicodemus hears as repetition"),
            ("πνεῦμα", "wind / breath / Spirit — one word; mapped origin is refused"),
            ("γεννηθῇ", "be born — entry is generation, not improvement of flesh"),
        ),
        "res": res(
            ("Matthew 18:3", "Unless you turn and become as children, you will not enter.", "Matthew asks a turn of stature; John asks a birth from above. Both block the unregenerate adult."),
            ("Gospel of Thomas 22", "When you make the two one, you will enter the kingdom.", "Thomas’s entry is unification; John’s is generation by Spirit you cannot map."),
        ),
    },
    {
        "n": 18,
        "title": "God is spirit — worship in spirit and truth",
        "book": "John",
        "ch": 4,
        "a": 23,
        "b": 24,
        "tr": "But an hour is coming, and now is, when the true worshipers will worship the Father in spirit and truth. For the Father also seeks such to worship him. God is spirit, and those who worship must worship in spirit and truth.",
        "comm": "The hour is coming and now is — Johannine time, not a calendar. Place (this mountain / Jerusalem) is already obsolete. Pneuma ho Theos: God is spirit — not a body to locate, not a rite to own. The Father seeks worshipers; the seeking is two-way. Truth (alētheia) here is not sincerity of mood. It is the unhidden, the same as the light the darkness did not grasp. The misconception: that worship is a correct site or a correct feeling. Must (dei) is ontological: spirit-and-truth is the only possible worship of this God.",
        "prac": "In one act of prayer or attention today, drop the question of the right place. Worship as spirit and truth: no audience, no mountain-pride. One true sentence to the Father.",
        "terms": kt(
            ("Πνεῦμα ὁ Θεός", "God is spirit — identity, not a metaphor for vagueness"),
            ("ἀληθείᾳ", "truth / unhiddenness — the how of worship, paired with spirit"),
            ("καὶ νῦν ἐστιν", "and now is — the hour is not postponed to a better temple"),
        ),
        "res": res(
            ("Matthew 6:6", "Pray to the Father in secret, in the inner room.", "Matthew hides prayer spatially; John unbinds worship from mountain and city altogether."),
            ("Gospel of Thomas 113", "The kingdom of the Father is spread out on the earth, and people do not see it.", "Thomas’s kingdom is already spread; John’s worship is already possible now, in spirit."),
        ),
    },
    {
        "n": 19,
        "title": "I am the light of the world",
        "book": "John",
        "ch": 8,
        "a": 12,
        "b": 12,
        "tr": "Again Jesus spoke to them, saying, I am the light of the world. Whoever follows me will not walk in the darkness, but will have the light of life.",
        "comm": "Egō eimi: the divine name-shape. Matthew said you are the light; John has Jesus say I am. Both are needed. Following is the condition of not walking in skotia; having the light of life is not a souvenir of having seen him once. Life’s light (to phōs tēs zōēs) returns to 1:4. The misconception: that this is a slogan of exclusive club-light, or that Matthew’s ‘you are’ and John’s ‘I am’ are a contradiction. The city’s light is participation in this I am. Without following, you have a phrase.",
        "prac": "Walk one ordinary path today as a follower, not as a self-light. When darkness (spite, despair, showing-off) starts to walk you, return to the I am as the light you have, not the light you produce.",
        "terms": kt(
            ("Ἐγώ εἰμι", "I am — the name-shape; not a psychological ‘I feel luminous’"),
            ("τὸ φῶς τῆς ζωῆς", "the light of life — light that is living, from 1:4"),
            ("ἀκολουθῶν", "the one following — motion; light is had on the road"),
        ),
        "res": res(
            ("Matthew 5:14", "You are the light of the world.", "Matthew gives the light to the crowd; John grounds that gift in the I am they follow."),
            ("Gospel of Thomas 24", "There is light within a person of light, and it lights the whole world. If they do not shine, they are darkness.", "Thomas locates light as an inner condition that can fail; John locates it as a person to follow."),
        ),
    },
    {
        "n": 20,
        "title": "The truth will free you",
        "book": "John",
        "ch": 8,
        "a": 31,
        "b": 32,
        "tr": "Jesus said to the Jews who had believed him, If you remain in my word, you are truly my disciples, and you will know the truth, and the truth will free you.",
        "comm": "Menein: remain, abide — the same verb as the vine. Belief is not the end of the sentence. Remaining in the logos makes true disciples; then knowing the truth; then freedom. Alētheia here is not data. It is the unhidden reality of 1:5 and 4:24. Eleutherōsei: will make you free — future, from remaining. The misconception: that a true idea, held once, frees. John sequences stay → know → free. Leave the word, and you have a slogan about freedom.",
        "prac": "Remain in one sentence of this Word for the day (not a feed of sentences). When you leave it, return. At evening, ask whether anything actually freed.",
        "terms": kt(
            ("μείνητε", "if you remain / abide — duration in the word, not a moment of assent"),
            ("ἀλήθεια", "truth — the unhidden; what remaining makes knowable"),
            ("ἐλευθερώσει", "will free — the last of three steps, not a feeling at the start"),
        ),
        "res": res(
            ("John 15:4–5", "Abide in me; apart from me you can do nothing.", "8:31 abides in the word; 15 abides in him as vine. Same menein, tighter union."),
            ("Gospel of Thomas 5", "Know what is before your face, and what is hidden from you will be revealed.", "Thomas reveals by knowing the before-your-face; John frees by remaining in the word."),
        ),
    },
    {
        "n": 21,
        "title": "I and the Father are one",
        "book": "John",
        "ch": 10,
        "a": 30,
        "b": 30,
        "tr": "I and the Father are one.",
        "comm": "Hen esmen: one, neuter — one thing, one reality, not one person collapsing the two. The with of 1:1 is kept; the identity is real. Later 17:21–23 will pray that they may be one as we are one — so this sentence is not a wall around Jesus. It is the pattern of the union he wants for them. The misconception: that this is either a later church formula only, or a simple identity that erases Father and Son. The Greek is careful: one, we-are. Mary’s Human One within is not this sentence, but it is why Levi can say worth is the Savior’s to confer.",
        "prac": "Do not repeat the sentence as a badge. Sit with the two-and-one: relation that is not distance. Let one action today come from that undivided place, not from a private ‘I’ performing for a remote Father.",
        "terms": kt(
            ("ἕν", "one (neuter) — one reality, not a fused biography"),
            ("ἐσμέν", "we are — first person plural; the oneness is lived, not a third object"),
            ("Πατήρ", "Father — the other of the one; not deleted by hen"),
        ),
        "res": res(
            ("John 17:21–23", "That they may all be one, as you, Father, in me and I in you.", "10:30 states the pattern; 17 extends it to those who believe through the word."),
            ("Śiva Sūtra I.1", "Consciousness is the Self.", "The sūtra states identity without a Father–Son polarity; John keeps the relation inside the one."),
        ),
    },
    {
        "n": 22,
        "title": "I am the resurrection and the life",
        "book": "John",
        "ch": 11,
        "a": 25,
        "b": 26,
        "tr": "Jesus said to her, I am the resurrection and the life. The one who believes in me, even if they die, will live, and everyone who lives and believes in me will not die, into the age. Do you believe this?",
        "comm": "Spoken to Martha before the tomb, not after a trick. Resurrection is not only a future event at the last day (which Martha already confesses). It is an I am, now. Dying and living are re-keyed: belief does not cancel biological death; it refuses death as the last word, into the age (eis ton aiōna). The question at the end — do you believe this? — is the practice. The misconception: that this saying postpones life until after death, or that it is only comfort-language. He claims to be the life that death cannot close.",
        "prac": "Where you are postponing life until after a fear is solved, answer Martha’s question once: do you believe this? Then do one living act before the fear is gone.",
        "terms": kt(
            ("ἀνάστασις", "resurrection — here an identity (‘I am’), not only a timetable"),
            ("εἰς τὸν αἰῶνα", "into the age / forever — death is refused as the last horizon"),
            ("πιστεύεις τοῦτο", "do you believe this? — the saying ends as a demand, not a slogan"),
        ),
        "res": res(
            ("John 1:4", "In him was life, and the life was the light of humans.", "The prologue’s life becomes, at a tomb, a question to a grieving sister."),
            ("Gospel of Thomas 11", "The dead are not alive, and the living will not die.", "Thomas states a riddle of two classes; John binds living-and-believing to an I am at a grave."),
        ),
    },
    {
        "n": 23,
        "title": "Whoever has seen me has seen the Father",
        "book": "John",
        "ch": 14,
        "a": 6,
        "b": 10,
        "tr": "Jesus says to him, I am the way and the truth and the life. No one comes to the Father except through me. If you had known me, you would have known my Father also. From now on you know him and have seen him. Philip says to him, Lord, show us the Father, and it is enough for us. Jesus says to him, Have I been with you so long, and you have not known me, Philip? Whoever has seen me has seen the Father. How do you say, Show us the Father? Do you not believe that I am in the Father and the Father is in me? The words I say to you I do not speak from myself; the Father remaining in me does his works.",
        "comm": "Philip wants a theophany beside Jesus. The answer is that the seeing has already happened and was missed. Way, truth, life are not three slogans; they are the one I am that is also the only approach to the Father. ‘Through me’ is not a later brand-check. It is this mutual indwelling: I in the Father, the Father in me, words not from myself. The extra law of ‘show us a further God’ is what Mary forbids as Look over there. The misconception: that Jesus blocks the Father. John says he is the seeing of the Father, missed because we wanted a second showing.",
        "prac": "Catch one ‘show me something more’ (a sign, a better teacher, a mood). Return to what is already in front of you. Ask: have I been with this so long and not known it?",
        "terms": kt(
            ("ἡ ὁδὸς καὶ ἡ ἀλήθεια καὶ ἡ ζωή", "the way and the truth and the life — one I am, not a menu"),
            ("ἑωρακὼς ἐμὲ", "the one having seen me — seeing Jesus as seeing the Father"),
            ("μένων", "remaining / abiding — the Father remaining in him does the works"),
        ),
        "res": res(
            ("Gospel of Mary, BG 8502 pp. 8–9", "Do not be misled by Look over here or Look over there.", "Mary forbids pointing away from the Human One within; John forbids Philip’s request for a further Father."),
            ("John 10:30", "I and the Father are one.", "10:30 states hen; 14:9–10 shows what that does to seeing and to speech."),
        ),
    },
    {
        "n": 24,
        "title": "You in me, and I in you",
        "book": "John",
        "ch": 14,
        "a": 16,
        "b": 20,
        "tr": "And I will ask the Father, and he will give you another Advocate, that he may be with you into the age — the Spirit of truth, whom the world cannot receive, because it neither sees nor knows him. You know him, because he remains with you and will be in you. I will not leave you orphans; I am coming to you. Yet a little, and the world no longer sees me, but you see me. Because I live, you also will live. In that day you will know that I am in my Father, and you in me, and I in you.",
        "comm": "Paraklētos: the one called to the side — another, because Jesus is the first. The world cannot receive this Spirit because it does not see or know; the disciples already know because remaining has started. Orphans is the fear. Coming to you is not a calendar of second arrival only; it is the day of knowing a triple indwelling: I in the Father, you in me, I in you. That is the architecture Mary’s nous-between and Thomas’s inside-and-outside are reaching for. The misconception: that presence ends at death, or that the Spirit is a vague mood the world could also have if it tried. Reception has an organ: remaining.",
        "prac": "When you feel orphaned today, do not hunt a spectacle. Remain. Say the last clause slowly: I in the Father, you in me, I in you. Then do the next act as someone not abandoned.",
        "terms": kt(
            ("Παράκλητον", "Advocate / Paraclete — another called-alongside, not a replacement feeling"),
            ("ὀρφανούς", "orphans — the feared condition; refused by ‘I am coming to you’"),
            ("ὑμεῖς ἐν ἐμοὶ κἀγὼ ἐν ὑμῖν", "you in me and I in you — the day’s knowledge, not a theory"),
        ),
        "res": res(
            ("Gospel of Thomas 3", "The kingdom is inside you and outside you.", "Thomas’s two locations; John’s three: Father, me, you, nested."),
            ("Pratyabhijñāhṛdayam 1", "Consciousness, of its own free will, is the Self of all.", "Kṣemarāja states one Self of all; John keeps Father, Son, Spirit, and the you as a living nest."),
        ),
    },
    {
        "n": 25,
        "title": "We will make our abode with him",
        "book": "John",
        "ch": 14,
        "a": 23,
        "b": 23,
        "tr": "Jesus answered him, If anyone loves me, they will keep my word, and my Father will love them, and we will come to them and make our abode with them.",
        "comm": "Love is not a mood that skips the word. Tērēsei: will keep, guard, watch over the logos. Then the Father’s love, then we will come — Father and Son — and make a monē, an abode, with them. The inner room of Matthew 6 is now occupied. Not a visit. A dwelling. The misconception: that love of Jesus is a feeling that need not keep the word, or that God remains a guest. This is household language. You keep the word; they move in.",
        "prac": "Keep one actual word today (a sentence you already know is his). Guard it when you would rather not. At night, notice whether the day felt like a visit or like someone living there.",
        "terms": kt(
            ("τηρήσει", "will keep / guard — love’s first act toward the word"),
            ("μονήν", "abode / dwelling — not a call, a place they make with you"),
            ("ἐλευσόμεθα", "we will come — Father and Son together; the we of 10:30 in motion"),
        ),
        "res": res(
            ("Matthew 6:6", "Pray to the Father in the secret inner room.", "Matthew’s room is where you go; John’s monē is who comes to stay."),
            ("Gospel of Thomas 3", "When you know yourselves, you will be known.", "Thomas’s being-known is recognition; John’s is Father and Son making a dwelling."),
        ),
    },
    {
        "n": 26,
        "title": "Abide in me, as the branch in the vine",
        "book": "John",
        "ch": 15,
        "a": 4,
        "b": 5,
        "tr": "Abide in me, and I in you. As the branch cannot bear fruit from itself unless it abides in the vine, so neither can you unless you abide in me. I am the vine, you are the branches. The one who abides in me, and I in him, this one bears much fruit, because apart from me you can do nothing.",
        "comm": "Menein again, now botanical. Fruit is not a project of the branch. Chōris emou: apart from me, you can do nothing — not ‘you can do less.’ The I am is the vine; you are already a branch, which is why the command is abide, not become. Matthew’s lamp under the basket was covering light; this is cutting the sap. The misconception: that spiritual fruit is produced by effort detached from remaining. Effort may be real. Detached, it is a branch displaying grapes it does not have.",
        "prac": "Before one task you usually muscle through, abide for sixty seconds — not as a trick to succeed, as the vine-condition. Then do the task. If it bears, do not take it as the branch’s genius.",
        "terms": kt(
            ("μείνατε", "abide / remain — the command; identity as branch is already given"),
            ("ἄμπελος", "vine — the I am as the living stem"),
            ("χωρὶς ἐμοῦ", "apart from me — the condition of doing nothing, not of doing less"),
        ),
        "res": res(
            ("John 8:31–32", "If you remain in my word, you will know the truth, and the truth will free you.", "Word-remaining becomes vine-remaining; freedom becomes fruit."),
            ("Bhagavad Gītā 9.27", "Whatever you do, eat, offer — do it as an offering to me.", "The Gītā offers actions into Kṛṣṇa; John says the branch cannot fruit at all apart from the vine."),
        ),
    },
    {
        "n": 27,
        "title": "That they may all be one",
        "book": "John",
        "ch": 17,
        "a": 20,
        "b": 23,
        "tr": "I do not ask for these only, but also for those who believe in me through their word, that they may all be one, as you, Father, are in me and I in you, that they also may be in us, that the world may believe that you sent me. And the glory you have given me I have given them, that they may be one as we are one — I in them and you in me — that they may be perfected into one, that the world may know that you sent me and loved them as you loved me.",
        "comm": "The prayer overshoots the room: those who will believe through their word — including the later reader. Oneness is not a team-building goal. It is as you, Father, in me and I in you, and then they in us. Glory is given onward so that they may be one as we are one. Tetelēōmenoi eis hen: perfected / completed into one. The world’s belief is the public fruit of this interior nesting, not a marketing campaign. Mary ends with Levi clothing the group in perfect Humanity and going out to preach without an extra law. John ends the logia-set with a prayer that the later ones be completed into the same one. The misconception: that Christian unity is agreement. It is indwelling, given, for the world to know love.",
        "prac": "Toward one person you split from, pray this much: that we may be one as they are one — not that they come over to your side. Do one repair that matches the prayer.",
        "terms": kt(
            ("ἓν ὦσιν", "that they may be one — the asked-for; patterned on Father-in-Son"),
            ("τετελειωμένοι εἰς ἕν", "perfected into one — completion as union, not as polish"),
            ("δόξα", "glory — given onward as the means of their oneness"),
        ),
        "res": res(
            ("John 10:30", "I and the Father are one.", "The pattern stated; 17 asks that believers be drawn into that same hen."),
            ("Gospel of Mary, BG 8502 pp. 18–19", "Clothe yourselves with perfect Humanity… preach, laying down no other rule.", "Mary’s unity is a clothed group going out; John’s is a prayer of nested indwelling for those not yet in the room."),
        ),
    },
]


def write_unit(u: dict) -> str:
    n = int(u["n"])
    uid = f"{SLUG}.ntl_{n:02d}"
    greek = greek_for(u["book"], u["ch"], u["a"], u["b"])
    section = u["book"] + f" {u['ch']}:{u['a']}" + (f"-{u['b']}" if u["a"] != u["b"] else "")
    layers = [
        {"kind": "original", "label": "Original", "body": greek},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"NTL_{n:02d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": section,
        "title": u["title"],
        "unit_type": "logion",
        "commentary": u["comm"],
        "themes": ["kingdom", "indwelling", "logia", "jesus"],
        "tags": [SLUG, "christian", "gospel", "sayings"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "section": section,
            "cultural_context": NOTE,
            "original_source": "Koine Greek, Nestle Novum Testamentum Graece 1904",
            "original_reliability": "SOURCED — Nestle 1904 OSIS of the four gospels",
            "english_source": PROV,
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": greek,
        "sanskrit_devanagari": greek,
        "sanskrit_iast": "Koine Greek (Nestle 1904; see Original layer).",
    }
    if n in HEROES:
        unit["tts_key"] = True
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{uid.replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return uid


def build() -> int:
    ids = [write_unit(u) for u in UNITS]
    print(f"Wrote {len(ids)} units to {OUT}")
    print(f"Heroes: {sorted(HEROES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
