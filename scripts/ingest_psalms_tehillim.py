#!/usr/bin/env python3
"""Ingest a selected Psalter (Tehillim) from the Westminster Leningrad Codex.

Not all 150 psalms — the most poetic and mystical, with Psalm 19 required.
English is a Pratibha rendering from the Masoretic Hebrew (pd_render), cadence
informed by KJV / JPS 1917, not derived from any copyrighted translation.

Hebrew is stored in the original / sanskrit_devanagari slot by corpus convention.
"""
from __future__ import annotations

import html
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data/raw_texts/pd/hebrew/psalms_wlc_openscriptures.xml")
OUT = os.path.join(ROOT, "data/canonical/psalms_tehillim")
SLUG = "psalms_tehillim"
COLL = "Psalms (Tehillim)"
EDITION = "Westminster Leningrad Codex (OpenScriptures WLC, public domain Masoretic Hebrew)"
PROV = (
    "English is a Pratibha rendering (2026) from the Masoretic Hebrew of the "
    "Westminster Leningrad Codex. Cadence informed by public-domain English "
    "(KJV, JPS 1917). Does not follow NIV, NRSV, Alter, or any copyrighted translation."
)
NOTE = (
    "Tehillim — praises — compiled across Iron Age and Second Temple Israel. "
    "Tradition names David; many psalms are anonymous, Korahite, or Asaphite. "
    "This ingest is a lyrical selection, not the whole Psalter."
)

# Ten heroes for mandala + Listen. Psalm 19 must be among them.
HEROES = {8, 19, 23, 36, 42, 46, 63, 91, 131, 139}


def kt(*pairs: tuple[str, str]) -> list[dict]:
    return [{"term": t, "definition": d} for t, d in pairs]


def res(*triples: tuple[str, str, str]) -> list[dict]:
    return [{"citation": c, "resonance": r, "divergence": d} for c, r, d in triples]


def parse_wlc() -> dict[int, dict[int, str]]:
    raw = open(RAW, encoding="utf-8").read()
    out: dict[int, dict[int, str]] = {}
    for vm in re.finditer(r'<verse[^>]*osisID="Ps\.(\d+)\.(\d+)"[^>]*>(.*?)</verse>', raw, re.S):
        ch, vs = int(vm.group(1)), int(vm.group(2))
        body = vm.group(3)
        body = re.sub(r"<note.*?</note>", " ", body, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", body)
        body = html.unescape(body).replace("/", "")
        body = re.sub(r"\s+", " ", body).strip()
        body = body.replace(" ־ ", "־").replace(" ׃", "׃").replace("־ ", "־").strip()
        if body:
            out.setdefault(ch, {})[vs] = body
    return out


def pick_verses(book: dict[int, dict[int, str]], n: int, ranges: list[tuple[int, int]]) -> list[tuple[int, str]]:
    verses = book[n]
    picked: list[tuple[int, str]] = []
    for a, b in ranges:
        for vs in range(a, b + 1):
            if vs not in verses:
                raise KeyError(f"Psalm {n}:{vs} missing from WLC")
            picked.append((vs, verses[vs]))
    return picked


def format_hebrew(n: int, picked: list[tuple[int, str]]) -> str:
    parts: list[str] = []
    prev = None
    for vs, text in picked:
        if prev is not None and vs != prev + 1:
            parts.append("")
        parts.append(f"({n}:{vs}) {text}")
        prev = vs
    return "\n".join(parts)


# vs: inclusive Hebrew verse ranges. Omit to take the whole psalm.
UNITS: list[dict] = [
    {
        "n": 1,
        "title": "The Two Ways",
        "tr": "Happy is the one who has not walked in the counsel of the wicked, nor stood in the way of sinners, nor sat in the seat of scoffers. His delight is in the teaching of YHWH, and in his teaching he murmurs day and night. He is like a tree planted by streams of water, that yields its fruit in its season, and its leaf does not wither; in all that he does, he prospers. Not so the wicked: they are like chaff that the wind drives away. Therefore the wicked will not stand in the judgment, nor sinners in the assembly of the righteous. For YHWH knows the way of the righteous, and the way of the wicked will perish.",
        "comm": "The psalm does not begin with a commandment. It begins with a beatitude: ashrei, the happiness of a life already leaning. The three refusals — walk, stand, sit — are a thickening of company; the alternative is not isolation but a second company, the Torah murmured until it becomes weather. The tree is not a prize for morality. It is what a life looks like when its roots have found a stream that does not depend on the season of the self. Chaff is not an insult. It is grain with the seed gone: motion without weight. The last line is the claim: YHWH yodea, knows, the way — not as surveillance only, but as the intimacy that makes a path real. The wicked way perishes because it was never known that way.",
        "prac": "Before you join the next conversation that feeds on contempt, step outside for one minute. Name the stream you actually want your day rooted in. Then re-enter and refuse one scoff.",
        "terms": kt(
            ("ashrei", "happy / blessed — a condition of alignment, not a mood"),
            ("torah", "teaching; here a stream to murmur in, not a statute to police others with"),
            ("hagah", "to murmur, growl, meditate — Torah as something the mouth keeps working"),
        ),
        "res": res(
            ("Bhagavad Gita 2.55–57", "Both picture a life that does not sit in the seat of agitation.", "The Gita stills desire in the self; Psalm 1 plants the self beside a teaching that comes from another."),
            ("Dhammapada 1–2", "Mind precedes; two paths diverge by what is dwelt on.", "The Dhammapada locates the fork in intention; Psalm 1 locates it in company and murmur."),
        ),
    },
    {
        "n": 8,
        "title": "What Is a Human That You Remember",
        "tr": "YHWH, our Lord, how majestic is your name in all the earth — you who have set your splendor above the heavens. From the mouth of infants and nurslings you have founded strength, because of your foes, to still enemy and avenger. When I see your heavens, the work of your fingers, the moon and the stars you have established — what is a human, that you remember him? And a child of earth, that you attend to him? Yet you have made him lack little from divine beings, and crowned him with glory and honor. You make him rule over the works of your hands; all things you have set under his feet: sheep and oxen, all of them, and also the beasts of the field, birds of the heavens and fish of the sea, what passes the paths of the seas. YHWH, our Lord, how majestic is your name in all the earth.",
        "comm": "The psalm is a gasp that refuses to become either humility-as-self-hatred or dominion-as-license. Under a night sky the speaker shrinks: mah-enosh, what is a human — a mortal, a weak one — that you tizkerenu, remember him. Memory here is not nostalgia. It is the scandal that infinite attention would bother with this brief animal. Then the psalm turns without apology: a little less than elohim, crowned, given the works. The contested claim is that smallness and entrusted rule are the same vision. You do not earn the crown by forgetting you are dust, and you do not honor the dust by pretending the night is empty. The infants who found strength are the psalm's epistemology: praise is not the mature correction of wonder. It is wonder that still has milk on its mouth. The ring composition — majestic name at both ends — holds the paradox so neither pole can run away with the night.",
        "prac": "Tonight look at the actual sky, not a screen of it. Say the question out loud: what is a human, that you remember. Do not answer. Let the unearned attention sit in the chest for ten breaths. Then do one ordinary act of care as if the works were under your feet and not yours.",
        "terms": kt(
            ("enosh", "human as mortal/frail — the word that makes the remembering scandalous"),
            ("tizkerenu", "you remember him — attention as the divine act, not a stored fact"),
            ("elohim", "here, divine beings; the human lacks little from that company, and still is dust"),
        ),
        "res": res(
            ("Qur'an 2:30–33", "The human is made a vicegerent over a creation that already praises.", "The Qur'an stages a heavenly objection; Psalm 8 stages a night-sky shrinking that still accepts the charge."),
            ("Aitareya Upaniṣad 1", "The human is the place the gods enter to see.", "The Upaniṣad is cosmogony; Psalm 8 is lyric astonishment that the cosmogony noticed us."),
        ),
    },
    {
        "n": 16,
        "title": "You Will Not Abandon My Soul to Sheol",
        "tr": "Keep me, God, for I take refuge in you. I said to YHWH: You are my Lord; my good is not apart from you. As for the holy ones who are in the land, and the mighty in whom is all my delight — they multiply their sorrows who run after another. I will not pour their drink-offerings of blood, nor take their names upon my lips. YHWH is my allotted portion and my cup; you yourself hold my lot. The lines have fallen for me in pleasant places; yes, a lovely inheritance is mine. I will bless YHWH who has counseled me; even by night my kidneys instruct me. I have set YHWH before me always; because he is at my right hand, I will not be shaken. Therefore my heart rejoices and my glory exults; even my flesh will dwell in trust. For you will not abandon my soul to Sheol; you will not give your faithful one to see the Pit. You make me know the path of life; fullness of joys is with your face; pleasures in your right hand forever.",
        "comm": "Refuge here is not a bunker. It is a refusal of other names in the mouth. Portion and cup and lot are land-language: the self is treated as a territory whose boundary-lines have already fallen well, so the scramble for another god is a bad real-estate panic. Kidneys instruct at night because the body's deep places know before the argument does. The psalm's mystical turn is the last triad: not abandoned to Sheol, the path of life made known, joys with the face. Survival after death is not argued. Proximity is. The Pit would be the loss of the face, not merely the loss of pulse. To set YHWH before oneself always is a practice of orientation: the right hand is occupied, so shaking has nowhere to start.",
        "prac": "Before sleep, place your right hand on the sternum and name one lesser refuge you ran toward today. Set it down. Ask to be shown the path of life as the next ordinary hour, not as an afterlife brochure.",
        "terms": kt(
            ("menat-helqi", "my allotted portion — the self as a plot already given, not a prize to seize"),
            ("sheol", "the underworld of silence; abandonment there is loss of the Face"),
            ("hasid", "the faithful/covenanted one — loyalty as the reason the Pit does not get the last word"),
        ),
        "res": res(
            ("Acts 2:25–28", "Peter hears this psalm as a refusal of death's finality.", "Luke-Acts reads resurrection; the psalm itself speaks trust that the Face will not let go."),
            ("Kaṭha Upaniṣad 3.14", "The path is sharp as a razor, and it is a path of life.", "Yama teaches a secret; Psalm 16 tastes joys already at the right hand."),
        ),
    },
    {
        "n": 19,
        "title": "A Tent for the Sun",
        "tr": "For the leader. A psalm of David.\nThe heavens recount the glory of El; the firmament tells the work of his hands. Day to day pours out speech; night to night discloses knowledge. There is no speech, there are no words; their voice is not heard. Through all the earth their line has gone out, and their words to the end of the world. In them he has pitched a tent for the sun — and he is like a bridegroom coming out from his chamber; he rejoices like a champion to run the course. From the end of the heavens is his going-forth, and his circuit to their ends; nothing is hidden from his heat.\nThe teaching of YHWH is complete, restoring the life-breath; the testimony of YHWH is trustworthy, making the simple wise. The precepts of YHWH are upright, gladdening the heart; the commandment of YHWH is clear, lighting the eyes. The awe of YHWH is clean, standing forever; the judgments of YHWH are truth; they are righteous together. More to be desired than gold, than much refined gold, and sweeter than honey, than drippings of the comb. Moreover your servant is warned by them; in keeping them there is great consequence. Who can discern wanderings? From hidden things cleanse me. Also from insolent ones keep your servant; let them not rule in me. Then I shall be complete, and clean of great transgression. Let the words of my mouth and the murmur of my heart be toward your pleasure, YHWH, my rock and my kinsman-redeemer.",
        "comm": "Psalm 19 is two luminaries sewn into one lyric, and the seam is the point. First the sky speaks without a mouth: mesapperim, they recount, they enumerate glory — yet ein omer, there is no speech. The paradox is not a riddle for later theology. It is the psalm's epistemology: creation is a testimony that does not use our words, a qav, a measuring-line, stretched through the earth. In that wordless telling God pitches a tent for the sun. The sun is not a deity here. It is a bridegroom and a runner, heat from which nothing hides — glory as exposure. Then, without apology, a second sun: torat YHWH temimah, the teaching complete, meshivat nefesh, turning the life-breath back. Torah does what the sky cannot: it restores a particular soul and lights particular eyes. Gold and honey are not decorations. They name desire. The psalm refuses the split between cosmos and commandment. The same light that circuits the heavens wants the inner wanderings cleansed, because the servant can hear both sermons and still be ruled by zedim, insolent impulses. The last petition is not piety tacked on. Hegyon libbi — the murmur of the heart, the same verbal family as the Torah-murmur of Psalm 1 — must come before the Face as the sky already does. Rock and go'el: not a distant artisan of suns, but the kinsman who has the right to buy you back.",
        "prac": "At first light, stand where you can see sky. For one silent minute listen as if the air were telling, with no words. Then speak one sentence you actually mean. Ask whether that sentence, and the murmur under it, would be acceptable before a listener who already knows it. Keep the sentence or unspeak it.",
        "terms": kt(
            ("qav", "line, cord, measuring-string — the heavens' speech as a survey of the earth, not chatter"),
            ("torah", "teaching; here a second sun that restores nefesh, not 'law' as a fence for other people"),
            ("hegyon", "the heart's murmur/meditation — speech that must match the sky's wordless recounting"),
            ("go'el", "kinsman-redeemer — the one with standing to buy back; God as relative, not only author of heat"),
        ),
        "res": res(
            ("Chāndogya Upaniṣad 3.19 / 1.6", "The sun as the face of the real, a public light that is also an inner light.", "The Upaniṣad identifies sun and Self; Psalm 19 keeps the sun as creature and Torah as the second luminary that restores a soul."),
            ("Heraclitus, DK B1–B2", "The logos is common, though people live as if they had a private understanding.", "Heraclitus' logos is the world's own account; Psalm 19's account is glory of El, then a teaching that can be kept."),
            ("Plotinus, Ennead V.1", "The sun as image of the Good whose light makes seeing possible.", "Plotinus climbs from sun to the One; Psalm 19 descends from sun-circuit to the mouth that still needs cleansing."),
        ),
    },
    {
        "n": 23,
        "title": "You Are With Me",
        "tr": "YHWH is my shepherd; I lack nothing. In green pastures he makes me lie down; beside waters of rest he leads me. He turns my life-breath back; he guides me in right tracks for his name's sake. Even though I walk in a valley of death-shadow, I will not fear harm, for you are with me; your rod and your staff — they comfort me. You arrange a table before me in the face of my foes; you have anointed my head with oil; my cup is an overflowing. Surely goodness and loyalty will pursue me all the days of my life, and I will dwell in the house of YHWH for length of days.",
        "comm": "The first verb is not I follow. It is I do not lack. Shepherding here is provision so complete that craving loses its job. Meshiv nafshi — he turns my life-breath back — is the same restoration Torah worked in Psalm 19, now done by leading, not by statute. The psalm's turn from he to you happens in the valley: theology becomes address when the shadow is close. Rod and staff comfort because they are contact, not because pain has been cancelled. The table in the face of foes is the scandal: nourishment is not postponed until the enemies leave. Hesed pursues — the sheep is not only led; loyalty hunts the wanderer down. Length of days in the house is not a real-estate promise. It is remaining in the presence that made lack impossible in verse 1.",
        "prac": "Walk a familiar stretch as if you were being led, not driving the day. When a lack-thought appears, name it, then ask whether you are in the valley or only afraid of it. Eat one meal without a screen, as a table already set.",
        "terms": kt(
            ("ro'i", "my shepherd — God as the one who feeds and routes, not as a mascot of comfort"),
            ("meshiv nafshi", "he restores/turns back my nefesh — life-breath returned, not a mood lifted"),
            ("hesed", "covenant loyalty that pursues; goodness here is not luck"),
        ),
        "res": res(
            ("John 10:11–14", "The good shepherd knows his own and lays down life.", "John intensifies to death-for; Psalm 23 stays with leading-through."),
            ("Tao Te Ching 8", "Water rests in the low place and nourishes without claim.", "Laozi refuses a shepherd; the psalm wants a You in the valley."),
        ),
    },
    {
        "n": 24,
        "title": "Lift Up Your Heads, O Gates",
        "tr": "The earth is YHWH's and its fullness, the world and those who dwell in it. For he has founded it upon the seas, and established it upon the rivers. Who shall go up to the mountain of YHWH, and who shall stand in his holy place? The clean of palms and pure of heart, who has not lifted up my soul to falsehood, and has not sworn to deceit. He will carry blessing from YHWH, and righteousness from the God of his salvation. This is the generation of those who seek him, who seek your face, Jacob. Lift up your heads, O gates, and be lifted up, O ancient doors, that the King of glory may come in. Who is this King of glory? YHWH, strong and mighty, YHWH mighty in battle. Lift up your heads, O gates, and lift them up, O ancient doors, that the King of glory may come in. Who is he, this King of glory? YHWH of hosts — he is the King of glory.",
        "comm": "Ownership first: the earth is not a stage we built for religion. Then a question of ascent that looks ethical — clean palms, pure heart — until the liturgy explodes into architecture that must grow taller. Gates are told to lift their heads as if stone had a neck. The mystical claim is that the King of glory is incoming, and the thresholds of the world are too low. Seeking the face of Jacob's God and the entry of the warrior-king are one motion: purity is not a ticket you buy to keep glory out; it is the condition of a threshold that can bear an arrival. The repeated question — who is this — keeps glory from becoming a familiar mascot. You have to ask again at the door.",
        "prac": "Stand in an actual doorway of your house. Ask, without irony, who is coming in. Lift the lintel of one cramped expectation — a person, a task — by giving it more room than your first judgment allowed.",
        "terms": kt(
            ("melekh ha-kavod", "King of glory — weight/presence arriving, not a title on a banner"),
            ("naqi kappayim", "clean of palms — hands as the ethics of what you have actually touched"),
            ("selu shearim", "lift up, O gates — architecture commanded to become more than it was"),
        ),
        "res": res(
            ("Revelation 3:20", "A knocking at the door, an entry that requires the threshold to open.", "Revelation is intimate and late; Psalm 24 is processional and cosmic."),
            ("Īśā Upaniṣad 1", "The whole earth is the Lord's, therefore do not grasp.", "The Upaniṣad draws renunciation; Psalm 24 draws a liturgy of incoming glory."),
        ),
    },
    {
        "n": 27,
        "title": "One Thing I Ask",
        "tr": "YHWH is my light and my salvation; whom shall I fear? YHWH is the stronghold of my life; of whom shall I be afraid? When evildoers drew near against me to eat my flesh — my foes and my enemies — they stumbled and fell. If a camp encamp against me, my heart will not fear; if war rise against me, in this I trust. One thing I have asked of YHWH, that I will seek: to dwell in the house of YHWH all the days of my life, to behold the delight of YHWH, and to inquire in his temple. For he will hide me in his shelter in the day of evil; he will conceal me in the concealing of his tent; on a rock he will lift me. And now my head is lifted above my enemies round about, and I will sacrifice in his tent sacrifices of a shout; I will sing and make music to YHWH. Hear, YHWH, my voice — I call; be gracious to me and answer me. To you my heart has said: Seek my face. Your face, YHWH, I will seek. Do not hide your face from me; do not turn your servant aside in anger. You have been my help; do not abandon me, do not forsake me, God of my salvation. Though my father and my mother forsake me, YHWH will gather me in. Teach me your way, YHWH, and lead me on a level path because of those who lie in wait. Do not give me to the throat of my foes, for false witnesses have risen against me, and one who breathes out violence. Had I not trusted to see the good of YHWH in the land of the living — wait for YHWH; be strong, and let your heart be stout; wait for YHWH.",
        "comm": "Fear is answered not with bravery but with light. Then the psalm does something rare: it reduces desire to one request. Dwelling, gazing on no'am — pleasantness, delight — and inquiring in the temple are not three programs. They are one hunger for proximity. The face-seeking is mutual and strange: my heart said Seek my face, then immediately Your face I will seek. The dialogue of faces is the mystical core. Enemies, war, abandoned by father and mother — the one thing is asked inside that weather, not after it. The last line turns the singer into a coach of his own heart: wait, be strong, wait again. Trust to see good in the land of the living refuses both despair and a piety that only cashes out after death.",
        "prac": "Write down the many things you are asking. Strike all but one. For ten minutes seek that one as a face, not as an outcome. When fear returns, say 'in this I trust' and mean the seeking, not the odds.",
        "terms": kt(
            ("ahat", "one thing — desire concentrated until it can meet a face"),
            ("no'am", "delight/pleasantness of YHWH — beauty as the content of gazing, not a side effect"),
            ("baqqeshu fanai", "seek my face — the heart hears itself being summoned to seek"),
        ),
        "res": res(
            ("Luke 10:41–42", "One thing is necessary.", "Martha is busy with many; Psalm 27 is busy with war and still asks one."),
            ("Plotinus, Ennead I.6", "The soul seeks the beautiful by becoming sight.", "Plotinus trains the inner eye; Psalm 27 begs the Face not to hide."),
        ),
    },
    {
        "n": 29,
        "title": "The Voice Over the Waters",
        "tr": "Give to YHWH, sons of gods, give to YHWH glory and strength. Give to YHWH the glory of his name; bow to YHWH in the splendor of holiness. The voice of YHWH is over the waters; the God of glory thunders; YHWH is over many waters. The voice of YHWH in power; the voice of YHWH in splendor. The voice of YHWH breaks cedars; YHWH breaks the cedars of Lebanon. He makes them skip like a calf, Lebanon and Sirion like a young wild ox. The voice of YHWH hews flames of fire. The voice of YHWH makes the wilderness writhe; YHWH makes the wilderness of Kadesh writhe. The voice of YHWH makes hinds calve, and strips forests bare; and in his temple all say: Glory. YHWH sat enthroned at the flood; YHWH sits as king forever. YHWH will give strength to his people; YHWH will bless his people with peace.",
        "comm": "This is theophany as weather. Seven times qol YHWH, the voice, and the voice does what Baal's storm did in older Canaanite poetry — except the psalm commandeers the storm for YHWH and then does the un-Baal-like thing: it ends in shalom for a people. Glory is not an interior feeling. It is cedars snapping, wilderness writhing, fire being hewn. The mystical move is the temple's one word — Glory — as if the only adequate human act in a storm-theophany is to agree. Enthroned at the flood: the ancient water-chaos is a chair. Peace at the end is not a softer god. It is what the same voice gives after it has shown it can break Lebanon.",
        "prac": "In the next thunderstorm, or the next loud weather of your day, do not narrate. Say one word: glory. Afterward, bless one actual person with a concrete peace — a cancelled demand, a made meal, a returned call.",
        "terms": kt(
            ("qol YHWH", "the voice of YHWH — thunder as speech, not metaphor sprinkled on thunder"),
            ("kavod", "glory/weight — what the temple can only confess when the cedars are already breaking"),
            ("mabbul", "the flood — chaos-water as the throne, not the rival"),
        ),
        "res": res(
            ("Rig Veda 1.32 (Indra and Vṛtra)", "Storm-god splits the waters and releases the world.", "Indra's feat is combat; Psalm 29's voice already sits on the flood and then gives peace."),
            ("Mark 4:39", "A voice stills the water.", "Mark's voice is quieting; Psalm 29's voice is the storm itself, then blessing."),
        ),
    },
    {
        "n": 34,
        "title": "Taste and See",
        "vs": [(2, 9)],
        "tr": "I will bless YHWH at every time; his praise is always in my mouth. In YHWH my soul boasts; the humble hear and rejoice. Magnify YHWH with me, and let us exalt his name together. I sought YHWH and he answered me, and from all my terrors he delivered me. They looked to him and were radiant, and their faces were not ashamed. This poor one called, and YHWH heard, and from all his distresses he saved him. The messenger of YHWH camps around those who fear him, and delivers them. Taste and see that YHWH is good; happy is the mighty one who takes refuge in him.",
        "comm": "Taste is a scandal in a religion of hearing. The psalm insists that goodness is not only announced; it is flavored. Radiant faces are the public evidence of a private tasting. The poor one called — this is not a theory of prayer; it is a case. Malakh YHWH encamping is protection pictured as an army of presence, not as exemption from having been terrified. Ashrei again: happiness belongs to the one who takes refuge, which means the tasting happens inside trust, not as a dessert after safety is guaranteed. The invitation is empirical and communal: taste, see, magnify with me.",
        "prac": "Eat one thing slowly enough to taste it. Before the last bite, name a terror you were delivered from — or are still in. Ask whether goodness can be tasted before the story is finished.",
        "terms": kt(
            ("ta'amu u-re'u", "taste and see — knowledge as flavor, not as a conclusion"),
            ("naharu", "they were radiant — the face as the organ of having looked"),
            ("ḥasah", "to take refuge — the condition of the tasting, not a later reward"),
        ),
        "res": res(
            ("1 Peter 2:3", "You have tasted that the Lord is good.", "Peter cites this psalm into a new community; the psalm itself is already a communal tasting."),
            ("Rumi, Mathnawi I (reed)", "The complaint is also a flavor of the lost home.", "Rumi tastes absence; Psalm 34 tastes goodness in deliverance."),
        ),
    },
    {
        "n": 36,
        "title": "In Your Light We See Light",
        "tr": "An oracle of transgression to the wicked within my heart: there is no dread of God before his eyes. For he flatters himself in his own eyes, to find his iniquity and to hate. The words of his mouth are mischief and deceit; he has ceased to act wisely, to do good. Mischief he plots on his bed; he takes his stand on a way that is not good; he does not refuse evil. YHWH, your loyalty is in the heavens, your trustworthiness to the clouds. Your righteousness is like the mountains of God, your judgments a great deep; human and beast you save, YHWH. How precious is your loyalty, God; the children of humankind take refuge in the shadow of your wings. They are saturated from the fat of your house, and from the river of your delights you give them drink. For with you is the fountain of life; in your light we see light. Draw out your loyalty to those who know you, and your righteousness to the upright of heart. Let the foot of pride not come to me, and let the hand of the wicked not make me wander. There the workers of iniquity have fallen; they are thrust down and cannot rise.",
        "comm": "The psalm starts inside a wicked heart's oracle, then climbs into cosmology without changing speakers. Hesed in the heavens, righteousness like mountains, judgments a tehom — the moral qualities of God are treated as geography. Refuge under wings, fat of the house, nahal adanekha — a river of your delights — this is mystical banquet language. Then the line that justifies the whole selection: ki immekha meqor ḥayyim, be'orekha nir'eh or. Light is not a metaphor for information. It is the condition of seeing. We do not possess a private lamp that inspects God. We see light in Light, which means epistemology is participation. Pride's foot and the wicked's hand are the ways a person steps out of that participation and calls it clarity. The fountain is with you — location, not a principle.",
        "prac": "Sit by a window at dusk. Notice that you see the room by a light you did not light. For five minutes refuse to explain yourself to yourself. Ask to see one relationship in that borrowed light, and drop one flattering story you tell on the bed.",
        "terms": kt(
            ("meqor ḥayyim", "fountain of life — life as a spring located with God, not a possession of the organism"),
            ("be'orekha nir'eh or", "in your light we see light — seeing as participation, not as a spectator's privilege"),
            ("nahal adanekha", "the river of your delights — pleasure as a current from the house, not an escape from it"),
        ),
        "res": res(
            ("Plotinus, Ennead V.5", "Intellect sees by the light of the Good, as the eye sees by the sun.", "Plotinus theorizes illumination; Psalm 36 drinks from a river and then states the epistemology."),
            ("John 1:4–9", "The life was the light of humans.", "John identifies Word and light; Psalm 36 keeps fountain and light as God's, in which we see."),
        ),
    },
    {
        "n": 39,
        "title": "I Am a Sojourner",
        "tr": "I said: I will guard my ways, that I not sin with my tongue; I will keep a muzzle on my mouth while the wicked is before me. I was mute with silence; I was still even from good, and my pain was stirred. My heart grew hot within me; in my murmuring a fire burned; I spoke with my tongue: Make me know, YHWH, my end, and the measure of my days, what it is; let me know how fleeting I am. See, you have made my days handbreadths, and my span is as nothing before you; surely all standing-vapor is every human. Surely as a shadow a man walks; surely for vapor they roar; he heaps up and does not know who will gather. And now, what do I wait for, Lord? My hope — it is in you. Deliver me from all my transgressions; do not make me the reproach of the fool. I am mute, I do not open my mouth, for you have done it. Take away your stroke from me; I am finished by the hostility of your hand. With rebukes you discipline a man for iniquity, and you melt like a moth what he desires; surely every human is vapor. Hear my prayer, YHWH, and to my cry give ear; do not be silent at my tears. For I am a sojourner with you, a settler like all my fathers. Look away from me, that I may smile again, before I go and am not.",
        "comm": "This is Qoheleth's hevel inside a prayer. Handbreadths, shadow, vapor, moth-eaten desire — the psalm will not let piety skip the physics of a short life. The muzzle fails; fire makes speech; the speech is a request to know the measure, which is a request to stop pretending to be permanent. Ger anokhi — I am a sojourner with you: alien-resident status is not a complaint against God. It is the accurate visa. The shocking last petition, look away that I may smile, is not atheism. It is the intimacy of a sojourner who knows that the same attention that founds the world can also be too much heat, like Psalm 19's sun. Hope is in you, and also: let me breathe before I go and am not.",
        "prac": "Measure one day as a handbreadth: write three things that will not survive it. Then name the one hope that is not a heap. Speak less today in the presence of someone you usually perform for.",
        "terms": kt(
            ("hevel", "vapor/breath — the same word Qoheleth wears threadbare; here it is prayed, not only diagnosed"),
            ("ger", "sojourner/resident-alien — life with God as a visa, not a deed of permanent ownership"),
            ("tikvati", "my hope — waiting as the only non-vapor investment"),
        ),
        "res": res(
            ("Ecclesiastes 1:2–4", "Vapor, generations, earth that remains.", "Qoheleth stays with the question of gain; Psalm 39 turns vapor into a plea to a You."),
            ("Bhagavad Gita 2.27–28", "Beings unmanifest, manifest, unmanifest.", "The Gita consoles Arjuna for duty; Psalm 39 asks God to look away so a sojourner can smile."),
        ),
    },
    {
        "n": 42,
        "title": "Deep Calls to Deep",
        "tr": "As a deer pants for water-courses, so my being pants for you, God. My being thirsts for God, for the living God; when will I come and see the face of God? My tears have been my bread day and night, while they say to me all day: Where is your God? These things I remember, and I pour out my being upon myself: how I would pass with the throng, leading them to the house of God, with a voice of shouting and thanksgiving, a crowd keeping festival. Why are you cast down, my being, and why in turmoil upon me? Wait for God, for I will yet thank him, salvations of his face. My God, my being is cast down upon me; therefore I remember you from the land of Jordan and Hermon, from Mount Mizar. Deep calls to deep at the voice of your channels; all your breakers and your waves have passed over me. By day YHWH commands his loyalty, and by night his song is with me, a prayer to the God of my life. I will say to God my rock: Why have you forgotten me? Why do I go mourning under the oppression of the enemy? With a breaking in my bones, my foes taunt me, saying all day: Where is your God? Why are you cast down, my being, and why in turmoil upon me? Wait for God, for I will yet thank him, my salvation and my God.",
        "comm": "Thirst is the first theology. The deer is not a decoration; nephesh, the throat-being, pants. Exile from the Face is measured in tears-as-bread and in the taunt Where is your God — a question the psalmist also has. The genius is the split self: he lectures his own nephesh to wait, then admits the nephesh is still down, then lectures again. Memory of the festival crowd is not nostalgia as comfort; it is fuel that also burns. Then the line that opens the deeps: tehom el-tehom qore, deep calls to deep at the voice of your channels. Chaos-water is not only threat. It is correspondence — abyss answering abyss — while breakers pass over. Loyalty by day and a song at night keep covenant inside drowning. Forgetting and waiting share the same poem. The mystical psalm is not the one that has arrived. It is the one that still asks when it will see the face, and teaches its own soul to wait anyway.",
        "prac": "When thirst for God becomes a mood you cannot use, do not upgrade it to a theory. Drink a glass of water slowly. Then speak to your own downcast being out loud, once, as the psalm does: wait. Do not require it to obey on the first asking.",
        "terms": kt(
            ("nephesh", "being/throat-soul — the one that pants, eats tears, and must be talked to"),
            ("tehom el-tehom", "deep calls to deep — abyss in correspondence, not merely in flood"),
            ("yeshua'ot panav", "salvations of his face — rescue as showing, not as extraction from history"),
        ),
        "res": res(
            ("John 4:13–14", "A well whose water becomes a spring.", "John promises un-thirst; Psalm 42 stays thirsty and still waits."),
            ("St. John of the Cross, Dark Night", "The soul's downcast is a path, not a disproof.", "The Carmelite maps stages; Psalm 42 repeats a refrain because the stage will not hold."),
        ),
    },
    {
        "n": 46,
        "title": "Drop, and Know",
        "tr": "God is for us a refuge and strength, a help in troubles, found to be greatly so. Therefore we will not fear though the earth change, and though mountains totter into the heart of the seas. Its waters roar, they foam; mountains quake at its swelling. Selah. A river — its channels gladden the city of God, the holy dwelling of the Most High. God is in her midst; she will not totter; God will help her at the turn of morning. Nations roared, kingdoms tottered; he gave his voice, the earth melts. YHWH of hosts is with us; a fortress for us is the God of Jacob. Selah. Go, behold the works of YHWH, who has set desolations in the earth. He is making wars cease to the end of the earth; the bow he breaks, the spear he snaps, the wagons he burns with fire. Drop, and know that I am God; I will be exalted among the nations, I will be exalted in the earth. YHWH of hosts is with us; a fortress for us is the God of Jacob. Selah.",
        "comm": "Cosmos unravels: earth changing, mountains into the sea's heart. Then a counter-image: a river's channels gladden a city because God is in her midst. The still point is not stoic temperament. It is presence in a place. Nations roar like the waters roared; one voice and the earth melts. The famous line is harpu u-de'u: drop / let go / slack your grip, and know that I am God. Knowledge here is what happens when the hands stop saving the mountains. It is not a seminar. The cessation of war is God's work in the song, not a human peace plan the psalm is congratulating. Exaltation among nations is the public side of the same dropping. Selah keeps interrupting because the body needs a rest in a psalm about not tottering.",
        "prac": "Clench both fists for twenty seconds as if holding the mountains up. Drop. Say: know that I am God. Stay dropped for ten breaths. Then cancel one small war you were about to continue by message.",
        "terms": kt(
            ("harpu", "drop, let go, slacken — the verb under 'be still'; not interior décor, a release of grip"),
            ("u-de'u", "and know — knowledge as the fruit of dropping, not its prerequisite"),
            ("nahar", "a river — ordered water that gladdens, against the sea that swallows mountains"),
        ),
        "res": res(
            ("Meister Eckhart, on Abegescheidenheit", "Detachment makes room for God to be God.", "Eckhart strips the soul; Psalm 46 strips the hands while the city still has a river."),
            ("Dao De Jing 16", "Empty to the utmost; keep stillness at the core.", "Laozi's stillness is return to the root; Psalm 46's stillness is commanded so that God can be known as exalted."),
        ),
    },
    {
        "n": 51,
        "title": "Create a Clean Heart",
        "vs": [(3, 14)],
        "tr": "Be gracious to me, God, according to your loyalty; according to your many compassions blot out my rebellions. Thoroughly wash me from my iniquity, and from my sin cleanse me. For my rebellions I know, and my sin is in front of me always. Against you, you alone, I have sinned, and what is evil in your eyes I have done — so that you are righteous in your speaking, clean in your judging. See, in iniquity I was born, and in sin my mother conceived me. See, you have desired truth in the covered places, and in the closed-in part you make me know wisdom. Un-sin me with hyssop, and I will be clean; wash me, and I will be whiter than snow. Let me hear joy and gladness; let the bones you have crushed rejoice. Hide your face from my sins, and all my iniquities blot out. A clean heart create for me, God, and a steadfast spirit make new inside me. Do not throw me out from your face, and your holy spirit do not take from me. Return to me the joy of your salvation, and a willing spirit sustain me.",
        "comm": "This is not a request for a better mood after a mistake. Lev tahor bera-li — create for me a clean heart — uses bara, the verb of Genesis 1, because the psalmist does not believe the old heart can be polished into innocence. Against you alone is not a denial of harmed neighbors; it is the claim that the real fracture is the Face. Truth in the covered places: God wants emet where the self is most padded. Hyssop is temple-cleaning transferred to a person. The holy spirit here is not yet a later theology's third person; it is God's own ruah as the atmosphere of remaining in the Face. Do not throw me out is the same hunger as Psalm 27, now spoken from guilt rather than war. A willing spirit, nedivah, is generosity of the inner life restored — not grit.",
        "prac": "Name one covered place where you have been padding the truth. Do not advertise the confession. Ask for a created heart, not a repaired reputation. Do one unseen repair toward anyone harmed.",
        "terms": kt(
            ("bara", "create — Genesis-verb; a clean heart is a new creation, not a scrubbed old one"),
            ("tattah emet ba-tuhot", "you desired truth in the covered-in places — wisdom where the self hides"),
            ("ruah qodesh", "holy spirit/breath — God's own atmosphere; exile from it is the real punishment"),
        ),
        "res": res(
            ("Ezekiel 36:26", "A new heart and a new spirit.", "Ezekiel promises a people; Psalm 51 begs it as an individual after a specific collapse."),
            ("Augustine, Confessions II", "Iniquity as a love aimed at nothing.", "Augustine narrates; Psalm 51 petitions the Creator-verb for the heart."),
        ),
    },
    {
        "n": 62,
        "title": "Only in God",
        "tr": "Only toward God is my being silent; from him is my salvation. Only he is my rock and my salvation, my fortress; I will not be greatly shaken. How long will you assault a man, will you crush him, all of you, like a leaning wall, a toppled fence? They have counseled only to thrust him from his height; they delight in a lie; with their mouth they bless, and inside they curse. Selah. Only toward God be silent, my being, for from him is my hope. Only he is my rock and my salvation, my fortress; I will not be shaken. Upon God is my salvation and my glory; the rock of my strength, my refuge, is in God. Trust in him at every time, O people; pour out your heart before him; God is a refuge for us. Selah. Only vapor are the sons of humankind, a lie are the sons of man; in the balances they go up, they are together lighter than vapor. Do not trust in oppression, and in robbery do not become vapor; when wealth bears fruit, do not set the heart. One thing God has spoken, two of these I have heard: that strength belongs to God. And to you, Lord, belongs loyalty, for you pay a man according to his work.",
        "comm": "Akh — only, yes, alone — hammers the psalm. Silence of the nephesh is not emptiness. It is the being no longer arguing with its source. The wall-image is the self under assault, leaning. Then the singer becomes his own choirmaster: only toward God be silent, my being. Vapor again, now on the scales, lighter than breath — a cousin of Psalm 39 and Qoheleth, but the conclusion is trust and poured-out heart, not look-away. Wealth as fruit that must not capture the heart: the psalm is mystical and economic in one breath. One thing spoken, two heard: strength and hesed. The only-God silence is not quietism. It is where payment and loyalty are allowed to be God's, so the heart can be poured.",
        "prac": "Set a two-minute silence in which the only permitted word is 'only.' When a lesser refuge speaks — reputation, money, a leaning wall — return to the word. Then pour out one true sentence of the heart to God, not to an audience.",
        "terms": kt(
            ("akh", "only/alone — the particle that starves rival salvations"),
            ("dumiyyah", "silence/stillness of the being — not muteness as tactic, orientation as rest"),
            ("kiq-hevel", "lighter than vapor — human weight on the divine scales"),
        ),
        "res": res(
            ("Meister Eckhart, on the ground", "The soul is silent where God is the only work.", "Eckhart strips images; Psalm 62 keeps rock, fortress, poured heart."),
            ("Marcus Aurelius 4.3", "Men seek retreats; you can retreat into yourself.", "The emperor's citadel is the ruling reason; Psalm 62's citadel is a God who pays in loyalty."),
        ),
    },
    {
        "n": 63,
        "title": "A Dry Land Without Water",
        "tr": "God, you are my God; I seek you at dawn. My being thirsts for you, my flesh faints for you, in a land dry and faint, without water. So in the holy place I have seen you, seeing your strength and your glory. For your loyalty is better than life; my lips will praise you. So I will bless you in my life; in your name I will lift my palms. As with fat and richness my being is satisfied, and with ringing lips my mouth will praise. When I remember you upon my bed, in the night-watches I murmur of you. For you have been a help for me, and in the shadow of your wings I shout. My being clings after you; your right hand holds me. But those who seek my soul for ruin will go into the depths of the earth. They will be delivered to the power of the sword; they will be a portion for jackals. The king will rejoice in God; everyone who swears by him will exult, for the mouth of those who speak a lie will be stopped.",
        "comm": "Dawn-seeking, thirst, flesh fainting: this is Psalm 42 without the taunt, in a desert that is both geography and soul. Ḥesed is better than life — the most dangerous mystical sentence in the selection. It does not despise life. It ranks loyalty above the organism's continuance, which is either insanity or the beginning of worship. Seeing in the holy place is remembered in a dry land; vision is portable as memory and as night-watch murmur (again hagah). Saturated as with marrow — the desert body is feasted by memory of glory. Davedah nafshi — my being clings after you — while the right hand holds: effort and being-held in one couplet. The violence at the end is the old psalm-world; the mystical core is the clinging in a land without water.",
        "prac": "Wake once this week before the house is loud. Drink nothing for the first three minutes. Let thirst name what it is actually for. Murmur one line of loyalty better than life — not as a death wish, as a ranking — then drink and begin the day.",
        "terms": kt(
            ("ashaharekka", "I seek you at dawn — hunger timed to first light"),
            ("ki-tov ḥasdekha me-ḥayyim", "your loyalty is better than life — the ranking that makes praise possible in a dry land"),
            ("davedah", "clings/sticks after you — nefesh as the one that will not un-adhere"),
        ),
        "res": res(
            ("Psalm 42:2–3", "The same thirst, another geography.", "42 is taunted by 'where is your God'; 63 has already seen in the holy place and carries the seeing into drought."),
            ("Teresa of Ávila, Interior Castle", "The soul faints for a vision it has tasted.", "Teresa maps mansions; Psalm 63 has a bed and night-watches."),
        ),
    },
    {
        "n": 73,
        "title": "Whom Have I in Heaven",
        "vs": [(21, 28)],
        "tr": "When my heart was soured and my kidneys were pierced, I was brutish and I did not know; I was a beast with you. Yet I am always with you; you have held my right hand. With your counsel you will guide me, and afterward you will take me to glory. Whom have I in heaven? And beside you I have not delighted on earth. My flesh and my heart fail; the rock of my heart and my portion is God forever. For see: those far from you will perish; you silence everyone who goes whoring from you. But I — the nearness of God is good to me; I have made the Lord YHWH my refuge, to recount all your works.",
        "comm": "The psalm's long argument with the prosperity of the wicked collapses into beast-knowledge: I was cattle with you, and yet always with you. Held right hand, counsel, then glory — not a career path, a being-taken. Mi-li va-shamayim: whom have I in heaven? The question is not information. It is dispossession of every other treasure. Heart-flesh failing while God is rock-portion: the same paradox as Psalm 16, now after envy has been burned out in the sanctuary (the verses just before this excerpt). Qirvat elohim li-tov — the nearness of God is, for me, the good. Not: nearness produces goods. Nearness is the good. Recounting works is what a person does who has stopped needing the wicked to fail as proof.",
        "prac": "Name one person whose ease has soured your heart. Do not pray they fall. Ask whom you have in heaven until the comparison loses oxygen. Make one nearness-move toward God that is not a request for a better ranking on earth.",
        "terms": kt(
            ("be'ar", "I was a beast — ignorance as cattle-mind, still in God's presence"),
            ("mi-li va-shamayim", "whom have I in heaven — the dispossession that founds delight"),
            ("qirvat elohim", "nearness of God — itself the good, not a means"),
        ),
        "res": res(
            ("Philippians 3:8", "I count all as loss compared with knowing.", "Paul is apostolic accounting; Psalm 73 is a recovered envier."),
            ("Plotinus, Ennead VI.9.11", "There the soul is with the One, having left other loves.", "Plotinus describes union; Psalm 73 still has failing flesh and a portion."),
        ),
    },
    {
        "n": 77,
        "title": "I Remember Your Wonders",
        "vs": [(12, 21)],
        "tr": "I will remember the deeds of Yah; yes, I will remember from of old your wonder. I will meditate on all your work, and on your acts I will murmur. God, in holiness is your way; who is a great god like God? You are the God who works wonder; you have made known your strength among the peoples. You redeemed with your arm your people, the children of Jacob and Joseph. Selah. The waters saw you, God, the waters saw you, they writhed; even the deeps trembled. The clouds poured water; the skies gave voice; even your arrows went about. The voice of your thunder in the whirlwind; lightnings lit the world; the earth trembled and shook. In the sea was your way, and your paths in many waters, and your footprints were not known. You led your people like a flock by the hand of Moses and Aaron.",
        "comm": "Memory is a practice against a mute present (the earlier verses of 77 are insomnia and refused comfort). Wonder of old is not antiquarianism. It is the only available evidence when God feels absent. Then the exodus sea is restaged as theophany: waters see, deeps tremble, footprints unknown. The mystical image is a path in the sea that leaves no print — guidance that cannot be reverse-engineered. Thunder-voice links to Psalm 29. Flock and Moses-Aaron at the end keep the cosmic storm attached to a people being led. Murmur (hagah) again: the mouth works the acts until they become a way through present water.",
        "prac": "Write three wonders older than your current stuckness — not moods, events. Murmur one of them while walking. Ask for a path in today's waters whose footprints you do not get to keep as a technique.",
        "terms": kt(
            ("pele", "wonder — the old act that re-teaches a silent present"),
            ("iqqevotekha lo noda'u", "your footprints were not known — guidance without a reverse-engineerable method"),
            ("ba-yam darkekha", "in the sea was your way — path where paths should drown"),
        ),
        "res": res(
            ("Exodus 15", "The sea as the site of a way.", "The Song of the Sea is victory-present; Psalm 77 is memory when comfort has been refused."),
            ("Dao De Jing 15", "The ancients were murky like water; we cannot track them.", "Laozi praises untraceable sages; Psalm 77 praises untraceable divine footprints in a people's story."),
        ),
    },
    {
        "n": 84,
        "title": "How Lovely Your Dwellings",
        "tr": "How lovely are your dwellings, YHWH of hosts. My being has longed, even been spent, for the courts of YHWH; my heart and my flesh shout to the living God. Even the bird has found a house, and the swallow a nest for herself, where she has set her young — your altars, YHWH of hosts, my king and my God. Happy are those who dwell in your house; still they will praise you. Selah. Happy is the human whose strength is in you, highways in their heart. They pass through the Valley of Baca, they make it a spring; also the early rain wraps it in blessings. They go from strength to strength; each one appears to God in Zion. YHWH, God of hosts, hear my prayer; give ear, God of Jacob. Selah. See, God our shield, and look on the face of your anointed. For better is a day in your courts than a thousand; I have chosen to lie at the threshold of the house of my God rather than dwell in the tents of wickedness. For a sun and a shield is YHWH God; grace and glory he will give. YHWH will not withhold good from those who walk in completeness.",
        "comm": "Longing spent the nephesh; heart and flesh shout — embodiment, not an idea of church. The swallow at the altars is the psalm's tenderness: even a bird is more at home in God than the singer who is still on the road. Highways in the heart: pilgrimage as an interior road-system. Baca, the valley of weeping or balsam, becomes a spring because they pass through — the mystical claim is that tears are hydrology when the heart has highways. Strength to strength, appearing in Zion: arrival is not a single spike. A day in the courts versus a thousand, threshold versus tents of wickedness: preference is ranked like Psalm 63's hesed-better-than-life. Sun and shield: Psalm 19's sun now worn as God, plus protection. Completeness (tamim) is walking, not a scored perfection.",
        "prac": "Walk a real stretch as a highway in the heart. When you pass a dry place (a memory, a street, a mood), treat it as Baca: can it become a spring if you do not camp in it? Choose one threshold act of belonging over a more impressive tent.",
        "terms": kt(
            ("yeshufet", "is spent/is consumed — longing as a cost, not a hobby"),
            ("mesillot bi-lvavam", "highways in their heart — pilgrimage internalized"),
            ("shemesh u-magen", "sun and shield — illumination and protection as one God"),
        ),
        "res": res(
            ("Psalm 19:5–7", "A tent for the sun; here God is the sun.", "19 keeps the sun as creature; 84 dares the metaphor onto YHWH without collapsing creation."),
            ("Augustine, Confessions X (the heart restless)", "Rest is a house, and the way is also love.", "Augustine's rest is in God; Psalm 84 still loves the courts and the swallow's nest."),
        ),
    },
    {
        "n": 90,
        "title": "A Thousand Years in Your Eyes",
        "tr": "A prayer of Moses, the man of God. Lord, you have been a dwelling for us in generation and generation. Before mountains were born, and you writhed the earth and the world, from everlasting to everlasting you are God. You turn the human back to dust and say: Return, children of humankind. For a thousand years in your eyes are like yesterday when it passes, and like a watch in the night. You inundate them; they are sleep. In the morning they are like grass that passes. In the morning it blossoms and passes; by evening it withers and dries. For we are finished by your anger, and by your wrath we are terrified. You have set our iniquities before you, our hidden things in the light of your face. For all our days have turned in your overflowing; we finish our years like a sigh. The days of our years — in them are seventy years, and if with strength eighty years, and their pride is toil and trouble, for it passes quickly and we fly away. Who knows the strength of your anger, and like the fear of you, your overflowing? To number our days, so make us know, that we may bring a heart of wisdom. Turn back, YHWH — how long? — and have compassion on your servants. Satisfy us in the morning with your loyalty, and we will shout and rejoice in all our days. Gladden us according to the days you have afflicted us, the years we have seen evil. Let your work be seen by your servants, and your splendor upon their children. Let the pleasantness of the Lord our God be upon us, and the work of our hands establish for us; and the work of our hands, establish it.",
        "comm": "Moses as named voice: a dwelling (ma'on) before mountains were birthed. Dust and return — Genesis 3 as liturgy. A thousand years as yesterday and a night-watch: time is not denied; it is relativized until panic can become numbering. Numbering days to bring a heart of wisdom is the opposite of denying death. Hidden things in the light of the Face: Psalm 19's sun-heat as moral exposure. Seventy, eighty, toil, we fly — then the turn: satisfy us in the morning with hesed. No'am again, the pleasantness of the Lord upon us, and the work of hands established. The mystical psalm of time does not escape time. It asks that brief work be made to stand, and that morning loyalty arrive before the grass dries.",
        "prac": "Number this day: write its actual length as a fraction of a thousand years. Ask for a heart of wisdom, not for more years. Do one work of the hands as if it could be established — carefully, then released.",
        "terms": kt(
            ("ma'on", "dwelling — God as the house that outlasts mountains"),
            ("limnot yamenu", "to number our days — wisdom as counting, not as infinity-talk"),
            ("no'am", "pleasantness — the same delight Psalm 27 wanted to gaze on, now asked to rest on work"),
        ),
        "res": res(
            ("Ecclesiastes 1:4–5", "Generations go; the earth stands; the sun runs.", "Qoheleth will not cash time for a You; Psalm 90 does, as Moses' prayer."),
            ("2 Peter 3:8", "A thousand years as a day.", "Peter consoles delay; Psalm 90 uses the same math to teach numbering and morning hesed."),
        ),
    },
    {
        "n": 91,
        "title": "The Secret Place",
        "tr": "Whoever sits in the secret of the Most High lodges in the shadow of Shaddai. I will say of YHWH: my refuge and my fortress, my God, I will trust in him. For he will deliver you from the snare of the fowler, from the destroying pestilence. With his pinion he will cover you, and under his wings you will take refuge; a shield and buckler is his trustworthiness. You will not fear the terror of night, nor the arrow that flies by day, nor the pestilence that walks in darkness, nor the destruction that devastates at noon. A thousand will fall at your side, and ten thousand at your right hand; to you it will not draw near. Only with your eyes you will look, and the payment of the wicked you will see. For you — YHWH, my refuge; you have made the Most High your dwelling. Harm will not be allowed to you, and plague will not draw near in your tent. For his messengers he will command for you, to keep you in all your ways. Upon their palms they will carry you, lest your foot strike a stone. On cub and viper you will tread; you will trample young lion and serpent. Because he has clung to me, I will make him escape; I will set him on high, for he has known my name. He will call me and I will answer him; with him I am in trouble; I will deliver him and honor him. With length of days I will satisfy him, and I will let him look on my salvation.",
        "comm": "Seter elyon — the secret/hidden place of the Most High — is the psalm's mystical address. Sitting there is already lodging in Shaddai's shadow. The promises that follow are so absolute they have always been misused as a force field; the psalm itself is more intimate than insurance. The turn to I-voice, then you-voice, then God's own I at the end, is a drama of covering. Immo-anokhi ve-tsarah — with him I am in trouble — is the line that breaks the force-field reading. God is not a remote canopy. God is in the trouble with the one who knows the name. Clinging (hashaq) answers Psalm 63's davedah. Night-terror, noon-destruction: the whole clock of fear is named so it can be un-feared, not so the listener can pretend plagues are imaginary. Length of days and seeing salvation: satisfaction, not adrenaline.",
        "prac": "Sit for seven minutes as if in a secret place — a chair is enough. When a terror of night or a noon-destruction thought arrives, do not argue statistics. Say: with him I am in trouble. Stay seated until the clinging is more interesting than the arrow.",
        "terms": kt(
            ("seter elyon", "the secret of the Most High — hiddenness as address, not as occult"),
            ("tsel shaddai", "shadow of Shaddai — shelter as a name of power, not a dimming"),
            ("immo-anokhi ve-tsarah", "with him I am in trouble — presence inside the pinch, not exemption from it"),
        ),
        "res": res(
            ("Luke 4:10–11", "The devil quotes this psalm at Jesus.", "The misuse proves the force-field reading; Jesus refuses magic; the psalm's own end is 'I am with him in trouble.'"),
            ("Psalm 23:4", "You are with me in the valley.", "23 is shepherding through shadow; 91 is sitting in a secret, then being accompanied in trouble."),
        ),
    },
    {
        "n": 96,
        "title": "Sing to YHWH a New Song",
        "tr": "Sing to YHWH a new song; sing to YHWH, all the earth. Sing to YHWH, bless his name; proclaim from day to day his salvation. Recount among the nations his glory, among all the peoples his wonders. For great is YHWH and greatly praised; he is to be feared above all gods. For all the gods of the peoples are nothings, and YHWH made the heavens. Splendor and majesty are before him; strength and beauty are in his sanctuary. Give to YHWH, families of the peoples, give to YHWH glory and strength. Give to YHWH the glory of his name; carry an offering and come into his courts. Bow to YHWH in the splendor of holiness; tremble before him, all the earth. Say among the nations: YHWH reigns. Yes, the world is established, it will not totter; he will judge the peoples with uprightness. Let the heavens rejoice and the earth be glad; let the sea thunder and its fullness. Let the field exult, and all that is in it; then all the trees of the forest will shout before YHWH, for he comes, for he comes to judge the earth. He will judge the world in righteousness, and peoples in his trustworthiness.",
        "comm": "A new song is not a playlist update. It is praise adequate to a world that is being claimed in public: among the nations, families of peoples. Other gods as elilim, nothings — the psalm is polemic and lyric together. Creation itself is conscripted: sea thundering, field exulting, trees of the forest shouting. Judgment here is not a courtroom dread first; it is the arrival that lets the world stop tottering (echo of Psalm 46). YHWH malakh, YHWH reigns, is the political-mystical core: the established world is a theological statement. Beauty in the sanctuary (oz ve-tif'eret) keeps glory from being only noise.",
        "prac": "Sing or speak one sentence of praise you have not used this month — new, not recycled. Then walk among trees or a field and imagine them as already shouting. Do one public act of fairness as if the world were being judged into stability.",
        "terms": kt(
            ("shir ḥadash", "a new song — praise that matches a newly claimed world"),
            ("elilim", "nothings — the gods of the peoples as un-real, not as interesting rivals"),
            ("YHWH malakh", "YHWH reigns — cosmic politics, not a private warmth"),
        ),
        "res": res(
            ("Psalm 29", "Creation already says glory; here the nations must also sing.", "29 is storm-theophany; 96 is mission and trees shouting at an advent of judgment."),
            ("Isaiah 55:12", "Trees clap; mountains burst into song.", "Isaiah consoles exiles; Psalm 96 conscripts the same trees for a world-judgment hymn."),
        ),
    },
    {
        "n": 103,
        "title": "Bless YHWH, O My Being",
        "vs": [(1, 14)],
        "tr": "Bless YHWH, O my being, and all my inward parts, his holy name. Bless YHWH, O my being, and do not forget all his dealings — who forgives all your iniquity, who heals all your diseases, who redeems your life from the Pit, who crowns you with loyalty and compassions, who satisfies your ornament with good; your youth is renewed like the eagle. YHWH is one who does righteousnesses, and judgments for all the oppressed. He made known his ways to Moses, his acts to the children of Israel. Compassionate and gracious is YHWH, slow of anger and abundant in loyalty. He will not contend forever, and not for all time keep watch. Not according to our sins has he done to us, and not according to our iniquities has he repaid us. For as high as the heavens are above the earth, his loyalty is mighty over those who fear him. As far as east from west, he has distanced our rebellions from us. As a father has compassion on children, YHWH has compassion on those who fear him. For he knows our forming; he is mindful that we are dust.",
        "comm": "The nephesh is commanded to bless, and then the qeravay — inward parts — as if praise must reach the organs. Forgetting dealings is the spiritual disease; the list that follows is a memory-cure: forgive, heal, redeem from the Pit, crown with hesed, renew youth like eagle. Exodus 34's name (compassionate, gracious, slow, abundant in hesed) is quoted into personal liturgy. The spatial metaphors — heavens above earth, east from west — make forgiveness geographic, not mood. Father-compassion plus dust-knowledge: the same God who towers also remembers the forming (yitsrenu), the potter-fact of Genesis 2. Mysticism here is not extra information. It is refusing to forget the dealings, including that we are dust and still crowned.",
        "prac": "Speak to your own inward parts: do not forget. Name five dealings, including one that hurts. End with 'he knows our forming.' Let dust-knowledge cancel one self-punishment that is not the same as repentance.",
        "terms": kt(
            ("barakhi nafshi", "bless, O my being — the self as a choir that must be conducted"),
            ("gomel", "dealings/recompenses — benefits as acts, not as atmosphere"),
            ("yitsrenu", "our forming — dust as remembered fact, the ground of compassion"),
        ),
        "res": res(
            ("Exodus 34:6–7", "The name of compassion and hesed.", "Exodus is revelation after a breach; Psalm 103 is the name sung to the inward parts."),
            ("Psalm 90:3", "Return, children of dust.", "90 numbers days under wrath; 103 numbers the distance of east from west under hesed."),
        ),
    },
    {
        "n": 104,
        "title": "You Withdraw Their Breath",
        "vs": [(1, 4), (24, 30)],
        "tr": "Bless YHWH, O my being. YHWH my God, you are very great; splendor and majesty you have put on. Wrapped in light as a garment, stretching the heavens like a tent-curtain. Who lays in the waters his upper chambers, who makes clouds his chariot, who walks on the wings of the wind, who makes his messengers winds, his ministers a flaming fire.\nHow many are your works, YHWH; all of them in wisdom you have made; the earth is full of your creatures. This sea, great and wide of hands — there are swarming things without number, living things small with great. There ships go; Leviathan, whom you formed to play in it. All of them look to you to give their food in its time. You give to them; they gather. You open your hand; they are satisfied with good. You hide your face; they are terrified. You withdraw their breath; they expire and to their dust they return. You send forth your spirit; they are created, and you renew the face of the ground.",
        "comm": "Light as clothing, heavens as tent-skin: creation as divine dressing, kin to Psalm 19's tent for the sun. Messengers as winds, ministers as fire — the elements are staff. The excerpt's second movement is the most metaphysical ecology in the Psalter: all look to you for food; open hand, satisfied; hide the face, terrified; gather the ruah, they expire to dust; send ruah, they are created, face of the ground renewed. Death and birth are a breathing that belongs to God. Leviathan at play is chaos decommissioned into sport. The mystical claim is that the Face is the climate. Hide it, and the swarming world is already in terror before the dust. This is not a nature-romance. It is dependence sung as praise.",
        "prac": "On an out-breath, imagine the ruah returning. On an in-breath, imagine it sent. Do this for twelve cycles outdoors if you can. Then feed one creature (human or otherwise) as an open-hand imitation, not as a mood.",
        "terms": kt(
            ("oteh-or", "wrapped in light — light as garment, the first 'how' of greatness"),
            ("tosef ruḥam", "you gather their breath — death as divine inhalation"),
            ("teshallaḥ ruḥakha", "you send your spirit — creation as exhalation, ground's face renewed"),
        ),
        "res": res(
            ("Genesis 1–2", "Light, waters, breath of life, dust.", "Genesis narrates a beginning; Psalm 104 recites the same physics as present tense dependence."),
            ("Plotinus, Ennead III.8", "Contemplation as the world's looking toward its source.", "Plotinus' looking is intellective; Psalm 104's looking is hunger for food in its time."),
        ),
    },
    {
        "n": 121,
        "title": "I Lift My Eyes to the Mountains",
        "tr": "A song of the ascents. I lift my eyes to the mountains: from where will my help come? My help is from YHWH, maker of heaven and earth. He will not give your foot to tottering; he who keeps you will not slumber. See, he will not slumber and will not sleep, the keeper of Israel. YHWH is your keeper; YHWH is your shade upon your right hand. By day the sun will not strike you, nor the moon by night. YHWH will keep you from all harm; he will keep your soul. YHWH will keep your going-out and your coming-in, from now until forever.",
        "comm": "The mountains are the wrong answer that the first line almost believes. Help is from the maker of heaven and earth — Psalm 19's cosmos as the resume of the keeper. Not slumbering is the scandal against dying gods and tired guardians. Shade at the right hand: again the sun as threat (19's heat) and God as shade (91's shadow). Sun-stroke and moon-stroke name the whole daily round of harm. Keeping the nephesh, keeping going-out and coming-in: pilgrimage language for an entire life of thresholds. The psalm is short because the theology is a single correction of the gaze, then a covering.",
        "prac": "When you next look at a skyline for help (a job, a person, a peak), finish the sentence: from where. Then name the maker, not the mountain. Walk one going-out and coming-in today as a kept threshold.",
        "terms": kt(
            ("me'ayin yavo ezri", "from where will my help come — the question that unmasks the mountains"),
            ("shomer", "keeper — wakeful guarding, not a sleeping shrine"),
            ("tsel-al-yad yeminekha", "shade at your right hand — protection against the very sun Psalm 19 glorified"),
        ),
        "res": res(
            ("Psalm 19:7", "Nothing hidden from the sun's heat.", "19 praises that heat as glory; 121 asks for shade from the same sky."),
            ("Isaiah 40:28", "The creator of the ends of the earth does not faint.", "Isaiah consoles exiles; Psalm 121 is a traveler's antiphon."),
        ),
    },
    {
        "n": 126,
        "title": "We Were Like Dreamers",
        "tr": "A song of the ascents. When YHWH turned the turning of Zion, we were like dreamers. Then our mouth was filled with laughter, and our tongue with a shout. Then they said among the nations: YHWH has done great things with these. YHWH has done great things with us; we were joyful. Turn, YHWH, our turning, like channels in the Negev. Those who sow in tears will reap with a shout. The one who goes, going and weeping, carrying the bag of seed, will surely come, coming with a shout, carrying his sheaves.",
        "comm": "Hayinu ke-ḥolmim — we were like dreamers — is the mystical center of restoration: joy so large it feels unreal, or exile so deep that return arrives as unreality. The nations notice first; then we agree. Shuvah... et shevitenu — turn our turning — like Negev channels: a dry south waiting for water that re-cuts the wadi. Tears-as-sowing is not a proverb to paste on grief. It is a hydrology of hope: weeping is seed-carrying, not leakage. The doubled verbs (going going, coming coming) are the gait of a person who cannot yet believe the sheaves. Dream-likeness is not dismissed. It is the accurate phenomenology of sudden mercy.",
        "prac": "Name one turning you cannot force. Water it as a Negev channel would be watered — a small real act, not a fantasy of flood. If you are weeping, treat it as seed, not as proof that nothing grows.",
        "terms": kt(
            ("ke-ḥolmim", "like dreamers — joy or return as unreality, faithfully reported"),
            ("afiqim ba-negev", "channels in the Negev — dry land designed for sudden water"),
            ("zar'u be-dim'ah", "they sow in tears — grief as agriculture, not as a dead end"),
        ),
        "res": res(
            ("Isaiah 35", "The desert blossoms; the ransomed return with shouting.", "Isaiah is prophetic future; Psalm 126 is already tasting and still begging another turning."),
            ("Luke 15:11–24", "Return that feels like a dream to the household.", "Luke's father runs; Psalm 126's sower still goes weeping."),
        ),
    },
    {
        "n": 130,
        "title": "Out of the Depths",
        "tr": "A song of the ascents. Out of the depths I have called you, YHWH. Lord, hear my voice; let your ears be attentive to the voice of my supplications. If you keep watch on iniquities, Yah — Lord, who could stand? For with you is forgiveness, so that you may be feared. I have waited for YHWH, my being has waited, and for his word I have hoped. My being for the Lord — more than watchmen for the morning, watchmen for the morning. Wait, Israel, for YHWH, for with YHWH is loyalty, and with him is much redemption. And he will redeem Israel from all his iniquities.",
        "comm": "Mimma'amaqqim — from the deeps, a cousin of tehom — the call is not from a slight dip. Forgiveness is with you so that you may be feared: the logic is not cheap grace. Pardon founds reverence, because a God who only kept score would leave no one standing, and a God who pardons is more, not less, to be feared. Waiting doubled, hope for the word, then the image: more than watchmen for the morning, watchmen for the morning. Dawn is certain and still watched-for; that is what hope feels like. Israel's wait is taught from a personal deep. Much redemption (harbeh immo fedut) answers Psalm 19's go'el: the kinsman-function, now abundant.",
        "prac": "If you are in a depth, do not decorate it. Call from it once, plainly. Then practice watchman-waiting: stay up for literal dawn or sit the last hour of night. Hope for a word, not for a mood.",
        "terms": kt(
            ("ma'amaqqim", "deeps — the place of the call, not a metaphor for a bad week"),
            ("ha-seliḥah", "the forgiveness — located with God, the ground of fear"),
            ("shomerim la-boqer", "watchmen for the morning — hope as a professional waiting, doubled because dawn is sure and still not yet"),
        ),
        "res": res(
            ("Jonah 2", "A call from the deeps of the sea.", "Jonah is inside a fish; Psalm 130 is inside iniquity and still teaching Israel to wait."),
            ("Romans 8:23–25", "We hope for what we do not see, with patience.", "Paul theorizes; Psalm 130 gives the watchman's body."),
        ),
    },
    {
        "n": 131,
        "title": "Like a Weaned Child",
        "tr": "A song of the ascents. Of David. YHWH, my heart is not lifted up, and my eyes are not raised high. I have not gone about in great things, or in wonders too wondrous for me. I have soothed and quieted my being, like a weaned child upon its mother; like the weaned child upon me is my being. Wait, Israel, for YHWH, from now until forever.",
        "comm": "Three verses, and the whole mystical program of the Psalter in a body. Not a lifted heart, not eyes raised — the opposite of the pride-foot in Psalm 36. Great things and wonders too-wondrous: a refusal of spiritual ambition that still leaves wonder to God. Shivviti ve-domamti — I have leveled and silenced my nephesh — like a gamul, a weaned child, on its mother. Weaned, not nursing: this is not fusion. It is a child that no longer screams for the breast and can sit. The being is that child, and also the child is upon me — a strange double: I am the mothered and the one who holds. Israel is then taught the same wait as 130, without the depths-rhetoric. Quiet is the pedagogy.",
        "prac": "Sit as a weaned child: no request for five minutes. When the nephesh lunges at a great thing (a theory, a status, a spiritual experience), soothe it as you would a child who already ate. Do not confuse this with apathy. Wait.",
        "terms": kt(
            ("lo-gavah libbi", "my heart is not lifted — ambition refused as a spiritual posture"),
            ("gamul", "weaned child — closeness without frantic sucking; the image of a quieted being"),
            ("shivviti ve-domamti", "I have soothed and silenced — active quieting, not accidental calm"),
        ),
        "res": res(
            ("Matthew 18:3", "Become as children.", "Matthew wants entry; Psalm 131 specifies weaned, not infantile demand."),
            ("Dao De Jing 10 / 28", "The infant who has not yet learned to smile on command.", "Laozi's infant is uncarved; Psalm 131's child has been weaned — a later, quieter stage."),
        ),
    },
    {
        "n": 133,
        "title": "Dew of Hermon on Zion",
        "tr": "A song of the ascents. Of David. See how good and how pleasant it is, brothers dwelling also together. Like good oil on the head, coming down on the beard, the beard of Aaron, coming down on the collar of his robes. Like the dew of Hermon that comes down on the mountains of Zion — for there YHWH has commanded the blessing: life until forever.",
        "comm": "Tov and na'im — good and pleasant — the same no'am family as 27 and 90. Dwelling together is not morale. It is compared to priestly oil running: consecration as overflow, not as a meeting agenda. Then geography that should not work: Hermon's dew on Zion's mountains, north-water on the southern hill, a hydrological impossibility used as a blessing-image. There — Zion, or the together-dwelling — YHWH has commanded blessing, life until forever. The mystical claim is that communal dwelling is a liturgy with the same downward motion as oil and dew: grace runs; it is not pumped. Life-until-forever is attached to that running, not to an individual's escape.",
        "prac": "Mend one small togetherness today (a shared meal, a repaired tone). Imagine blessing as oil that has to run down, not as a feeling you both must produce. Let the other person speak more than you.",
        "terms": kt(
            ("shevet aḥim gam-yaḥad", "brothers dwelling also together — unity as a place, not a slogan"),
            ("shemen ha-tov", "the good oil — priestly consecration as the metaphor for common life"),
            ("tal ḥermon", "dew of Hermon — impossible water as the picture of commanded blessing"),
        ),
        "res": res(
            ("Acts 2:44–47", "They were together; life was added.", "Acts is a church's beginning; Psalm 133 is a pilgrim lyric with oil and dew."),
            ("Psalm 84:7", "From strength to strength toward Zion.", "84 is the road; 133 is the dwelling at the arrival."),
        ),
    },
    {
        "n": 139,
        "title": "Where Can I Flee from Your Face",
        "vs": [(1, 18)],
        "tr": "For the leader. Of David. A psalm. YHWH, you have searched me and you know. You know my sitting and my rising; you understand my intent from afar. My path and my lying-down you have measured, and all my ways you have familiarized. For there is not a word on my tongue — see, YHWH, you know it all. Behind and before you have besieged me, and you have laid your palm upon me. Too wonderful is the knowledge for me; it is high, I cannot reach it. Where can I go from your spirit? And where from your face can I flee? If I ascend the heavens, there you are; if I make my bed in Sheol, see you. I take up the wings of dawn, I dwell at the hindmost of the sea — even there your hand would lead me, and your right hand would hold me. And I said: surely darkness will crush me, and night will be light around me. Even darkness is not dark for you, and night like day will shine; like darkness, like light. For you yourself acquired my kidneys; you wove me in my mother's womb. I thank you, for I am fearfully distinct; wonderful are your works, and my soul knows it well. My frame was not hidden from you, when I was made in the secret, embroidered in the depths of the earth. My unformed substance your eyes saw, and on your book all of them were written, days they were formed, when there was not one among them. And to me — how precious are your thoughts, God; how massive is their sum. If I count them, they are more than sand; I awake, and I am still with you.",
        "comm": "This is the Psalter's most complete map of inescapable presence — and it begins as knowledge that feels like siege: behind and before you have enclosed me. The question 'where can I flee from your face' is not a tourist's curiosity. It is the last privacy-strategy, and it fails in every direction: heavens, Sheol, dawn-wings, far sea. Darkness will not crush the speaker into hiding; night shines for this You. Then the psalm drops from cosmology into embryology: kidneys acquired, woven in the womb, embroidered in earth's depths, golem (unformed mass) seen. The Face that fills the vertical cosmos also read the unformed days. Precious thoughts more than sand: the singer wakes and is still with you — the same clinging as 63, now after a tour of inescapability. The verses of vengeance that follow in the full psalm are a different register; this ingest keeps the mystical core, where omniscience is first terror and then thanks.",
        "prac": "Try, for one minute, to hide one thought as if the Face were a person in another room. Then admit the failure without self-hatred. Thank the weaver for one particular of your body. Wake tomorrow with 'I am still with you' before the phone.",
        "terms": kt(
            ("anah vaqesh", "where can I flee — the last strategy of privacy, named so it can fail"),
            ("golem", "unformed substance — the self before form, already seen"),
            ("iqeẓ ve-odi immakh", "I awake and I am still with you — presence that survives sleep and sand-counting"),
        ),
        "res": res(
            ("Jeremiah 23:23–24", "Do I not fill heaven and earth?", "Jeremiah is prophetic polemic; Psalm 139 is lyric siege that turns to embroidery and thanks."),
            ("Augustine, Confessions I.2–4", "Where do I call you, if you already fill me?", "Augustine philosophizes presence; Psalm 139 flies to Sheol and the womb."),
        ),
    },
    {
        "n": 148,
        "title": "Praise from Heaven and Earth",
        "tr": "Praise Yah. Praise YHWH from the heavens; praise him in the heights. Praise him, all his messengers; praise him, all his hosts. Praise him, sun and moon; praise him, all stars of light. Praise him, heavens of the heavens, and the waters that are above the heavens. Let them praise the name of YHWH, for he commanded and they were created. He made them stand for all time, forever; a boundary he gave, and they will not cross. Praise YHWH from the earth, sea-monsters and all deeps, fire and hail, snow and smoke, storm-wind doing his word, the mountains and all hills, fruit trees and all cedars, the wild animal and all beasts, creeping thing and bird of wing, kings of the earth and all peoples, princes and all judges of the earth, young men and also young women, old with youths. Let them praise the name of YHWH, for his name alone is exalted; his splendor is over earth and heaven. And he has raised a horn for his people, praise for all his loyal ones, for the children of Israel, a people near to him. Praise Yah.",
        "comm": "Psalm 19's wordless heavens are here given an imperative: praise. The catalogue is a cosmology of voices — sun and moon (19 again), waters above, tanninim and tehomot, fire-hail-snow, cedars, kings, young women, old with youths. Boundary they will not cross: created order as a liturgy of limits. The horn raised for a people near to him keeps the cosmic choir from dissolving Israel into scenery. Nearness (qarov) answers Psalm 73. The mystical Psalter ends its selection not with a private vision but with a universe ordered to praise, and a people called near.",
        "prac": "Speak praise once from the heavens (look up) and once from the earth (touch something). Include one creature you do not usually include. Notice a boundary you are not to cross today, and keep it as praise rather than as crampedness.",
        "terms": kt(
            ("halelu", "praise — an imperative that conscripts suns and judges alike"),
            ("gevul natan", "he gave a boundary — limit as a created good, not as a failure of power"),
            ("am qerovo", "a people near him — election as nearness inside a cosmic choir"),
        ),
        "res": res(
            ("Psalm 19:2–5", "The heavens recount without words; 148 commands them to praise.", "19 is testimony; 148 is a roll-call."),
            ("Francis of Assisi, Canticle of the Creatures", "Brother sun, sister moon.", "Francis names kinship; Psalm 148 names command and boundary."),
        ),
    },
    {
        "n": 150,
        "title": "Let All That Breathes",
        "tr": "Praise Yah. Praise God in his holy place; praise him in the firmament of his strength. Praise him in his mighty acts; praise him according to the abundance of his greatness. Praise him with the blast of the shofar; praise him with harp and lyre. Praise him with drum and dance; praise him with strings and pipe. Praise him with sounding cymbals; praise him with cymbals of shout. Let all that has breath praise Yah. Praise Yah.",
        "comm": "The Psalter's last word is not an argument. It is instrumentation: shofar, harp, drum, dance, cymbals of shout — the body and the workshop conscripted. In the holy place and in the firmament of his strength: Psalm 19's raqia returns as a venue of praise. Kol ha-neshamah — all that has breath — tehillah. Neshamah is Genesis 2's breath of life. The selection ends where 104's ruah-physics and 19's wordless sky and 150's loud instruments agree: if you are breathing, you are already in the choir. The mystical is not a quieter genre than the drum. It is the claim that breath itself is the membership card.",
        "prac": "Use an actual sound today — a clap, a hummed tone, a shofar if you have one, a pipe, a voice. Do not make it pretty. Let breath be praise for ten seconds. Then return to ordinary air as if it were still membership.",
        "terms": kt(
            ("raqia uzzzo", "the firmament of his strength — Psalm 19's sky as a sanctuary balcony"),
            ("kol ha-neshamah", "all that has breath — Genesis-breath as the final choir"),
            ("haleluyah", "praise Yah — the Psalter's last and first word of this ending"),
        ),
        "res": res(
            ("Psalm 19:2", "The firmament tells; 150 tells the firmament to praise.", "19 is cosmic speech; 150 is human and instrumental answering."),
            ("Revelation 5:13", "Every creature in heaven and earth and sea, blessing.", "John sees a throne-vision; Psalm 150 is a temple band and breath."),
        ),
    },
]


def write_unit(book: dict[int, dict[int, str]], u: dict) -> str:
    n = int(u["n"])
    verses = book[n]
    ranges = u.get("vs") or [(min(verses), max(verses))]
    picked = pick_verses(book, n, ranges)
    heb = format_hebrew(n, picked)
    a, b = picked[0][0], picked[-1][0]
    ref = f"{n}:{a}" if a == b else f"{n}:{a}–{b}"
    uid = f"{SLUG}.psalm_{n:03d}"
    hero = n in HEROES
    layers = [
        {"kind": "original", "label": "Original", "body": heb},
        {"kind": "translation", "label": "Pratibha Translation", "body": u["tr"]},
        {"kind": "commentary", "label": "Pratibha Commentary", "body": u["comm"]},
        {"kind": "key_terms", "label": "Key Terms", "items": u["terms"]},
        {"kind": "resonances", "label": "Cross-Tradition Resonances", "items": u["res"]},
        {"kind": "practice", "label": "Practice (Abhyasa)", "body": u["prac"]},
    ]
    unit = {
        "source_id": f"PS_{n:03d}",
        "category": "root_text",
        "work_id": SLUG,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": f"Psalm {n}",
        "title": u["title"],
        "unit_type": "passage",
        "sanskrit_devanagari": heb,
        "commentary": u["comm"],
        "themes": ["psalm", "tehillim", "hebrew", u["title"].lower()],
        "tags": [SLUG, "tehillim", "psalm", "hebrew"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": layers,
        "provenance": {
            "collection": COLL,
            "category": "hebrew",
            "section": f"Psalm {ref}",
            "verse": str(n),
            "psalm_number": n,
            "hebrew_verses": ref,
            "cultural_context": NOTE,
            "original_source": EDITION,
            "original_reliability": f"SOURCED — {EDITION}",
            "english_source": PROV,
            "verification": "Hebrew from OpenScriptures WLC OSIS (Ps.xml); English Pratibha pd_render",
        },
        "translation": u["tr"],
        "abhyasa": u["prac"],
        "practice": u["prac"],
        "original": heb,
    }
    if hero:
        unit["tts_key"] = True
    path = os.path.join(OUT, f"{uid.replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return uid


def build() -> int:
    os.makedirs(OUT, exist_ok=True)
    book = parse_wlc()
    ids = [write_unit(book, u) for u in UNITS]
    heroes = [u["n"] for u in UNITS if u["n"] in HEROES]
    missing = HEROES - set(heroes)
    if missing:
        raise SystemExit(f"Hero psalms not in UNITS: {sorted(missing)}")
    if 19 not in heroes:
        raise SystemExit("Psalm 19 must be a hero")
    print(f"{SLUG}: {len(ids)} units (min 25) · heroes {heroes}")
    return len(ids)


if __name__ == "__main__":
    build()
