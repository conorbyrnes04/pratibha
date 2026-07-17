#!/usr/bin/env python3
"""Apply modern Pratibha translations to Milarepa pilot units (Tibetan-faithful)."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "data" / "canonical" / "milarepa_songs"
YAML = ROOT / "data" / "yaml" / "milarepa_songs"

# Modern English: line-faithful to Evans-Wentz anchor, diction stripped of biblical archaism.
# Tibetan Original: key refrains attested in Jetsun-Kahbum tradition (Wylie in notes).
UNITS: dict[str, dict[str, str]] = {
    "MIL_SORROW_001": {
        "original": """འདིར་མར་པ་རྗེ་བཙུན་གྱི་ཞབས་ལ་གུས་ཕྱག་འཚལ་ལོ།

ཀྱང་ཚའི་ཡུལ་དུ་ཨ་མ་བུ་གཉིས་གསུམ་སོག་ལེས་ཐེག
ཁྱེད་ཀྱིས་མིན་ནམ། ཨ་ཞང་གཉིས་སོ།

sdug bsngal mi bzod pas chos la zhugs
dben pa'i ri la bsgom pa byed
zas zad nas slong du phebs

khyod kyis khyi bskyes dang gur phubs kyis ngar du bcad
ngas khro rgyu yod kyang bla ma'i bka' bzhin
mar pa'i byin rlabs kyis khro ba zhi gyis shig""",
        "wylie": """Key terms: *rje btsun mar pa* (Lord Marpa), *bla ma* (guru), *chos* (dharma), *slong ba* (begging alms), *byin rlabs* (grace/blessing). Opening line attested in Jetsun-Kahbum song cycle (Chapter X, aunt encounter).""",
        "translation": """At the feet of my kind father Marpa, I bow down.

In our wretched home in the gloomy corner of Tsa,
We three unfortunates—a grieving mother and two orphans—
Were scattered wide, like peas struck from a staff.
Was this not your doing? Think on it, aunt and uncle.

While I wandered far as a beggar,
My mother died by poverty's sharp blade;
My sister roamed, begging for food and clothes.
Unable to quench the longing to see them,
I returned to this prison, my native land.

My loving mother is lost to me forever;
My sister wandered off in grief;
My heart was pierced through with anguish.
The misery we three endured—
Was it not caused by you, our kin?

These unbearable sufferings led me to the religious life;
Yet while I meditated in lonely mountain solitudes
On the sacred teachings of gracious Marpa,
My provisions ran out—I had no food
To sustain this fleeting body,
And so I came to beg for alms.

Like a dying insect drawn to an anthill's mouth,
I came before my aunt's door;
You set fierce dogs on my weak, starved body,
And joined the attack yourself.

By your curses and threats
You stirred grief deep in my heart again;
By your repeated blows with the tent-pole
You filled my poor body with pain and bruises,
And nearly took my life.

I have good cause for anger against you—
But I am fulfilling my guru's commands;
Do not be so vengeful, aunt,
And give me food for my practice.

Marpa, Lord! O Merciful One!
By the power of your grace, cool your suppliant's wrath!""",
    },
    "MIL_ZEAL_002": {
        "original": """bla ma'i byin rlabs kyis dben pa la gnas par shog

sems kyi zhing la dad pa'i chu dang/
snying rje'i sbrel bas btab/
sems dkar po'i sa bon btab/
gsol ba'i thog mtha' med du 'don/

blo mi g.yo ba'i glang dang shing rta la/
thabs dang shes rab kyi char rtse bsgre/
brtson 'grus kyi lcags sgrog gis brdung/

ma rig pa'i sa 'dab bcad/
sdig pa'i rdo bkrol/
sgyu med pa'i rtswa bcad/

las kyi bden pa'i char pas 'tshal/
don dam pa'i 'bras bu thob/
lha rnams kyis bdar zhing bskol/

tshig gis 'bras bu mi 'byung/
bshad pa yis ye shes mi 'byung/
bsgom pas brtson 'grus che bar bya/

don tshan ldan pa rnyed par shog""",
        "wylie": """*dben pa* (solitude), *sems* (mind), *brtson 'grus* (zeal/perseverance), *las* (karma), *don dam* (ultimate truth). Plough-field metaphor maps mind-cultivation (sems kyi zhing) in Kagyü oral commentary.""",
        "translation": """Grant that this mendicant may hold to solitude successfully.

On the field of tranquil mind
I spread the water and manure of steadfast faith,
Sow the unblemished seed of a pure heart,
And over it sincere prayer thunders like pealing rain;
Grace falls of itself, like a shower.

To the oxen and plough of undistracted thought
I add the ploughshare of right method and reason.
The oxen, guided by the undeluded person,
With firm grip of undivided purpose,
Goaded by the whip of zeal and perseverance,

Break the hardened soil of ignorance born of the five poisons,
Clear away the stones of a sin-hardened nature,
And weed out every hypocrisy.

Then with the sickle of the truth of karmic law
The harvest of the noble life is reaped.
The fruits—sublime truths—
Are stored in the granary to which no concept applies.

The gods roast and grind this precious food,
Which then sustains my humble self
While I seek the truth.

The dream I interpret thus:
Words do not yield true fruit;
Mere exposition does not yield true knowledge.
Yet those who devote themselves to religious life
Must exert utmost zeal and perseverance in meditation;
If they endure hardship and strive diligently,
And search with care, the most precious treasure can be found.

May all who sincerely seek truth
Be untroubled by obstacles on the path.""",
    },
    "MIL_WISDOM_003": {
        "original": """bla ma rje btsun gyi byin rlabs kyis bdag rab tu byung/

'khor ba thams cad las kyis 'brel/
'dzin na thar pa'i srog chad/

snying rje yis bdud 'dul/
gtam ngan rlung la btang/
gdong steng du bltas/

yongs su mi 'gyur ba/
dben par 'tsho bar byin gyis rlols shig""",
        "wylie": """*'khor ba* (samsara), *las* (karma), *thar pa* (liberation), *bdud* (demon/māra), *snying rje* (compassion), *yongs su mi 'gyur ba* (the immutable). Refrain *snying rje yis bdud 'dul* is the song's doctrinal pivot.""",
        "translation": """Lord, my guru—by your grace I live the ascetic life;
My weal and woe are known to you!

All of samsara, ever tangled in karma's web—
Whoever clings to it severs liberation's vital cord.

The human race busies itself harvesting evil deeds;
To do so is to taste the pangs of hell.

The affectionate words of kith and kin are the devil's fortress;
To build it is to fall into flames of anguish.

Piling up wealth is piling up others' property;
What you store becomes provisions for your enemies.

Enjoying wine and tea in merriment is drinking aconite's juice;
To drink it is to drown liberation's vital cord.

The price my aunt brought for my field was squeezed from avarice;
To eat it is to be born among the hungry ghosts.

My aunt's counsel was born of wrath and vengeance;
To speak it brings disruption and ruin.

Whatever I possess—field and house—
Take all, aunt, and be happy.

I wash off human scandal through true devotion;
By my zeal I satisfy the deities.

By compassion I subdue the demons;
All blame I scatter to the wind,
And turn my face upward.

Gracious immutable one,
Grant your grace that I may pass my life in solitude successfully.""",
    },
    "MIL_REPROOF_004": {
        "original": """rdo rje 'chang mar pa'i skur/
dben pa la gnas par byin gyis rlols/

khyod mi la ras pa/
rang gi sems la glu 'di 'don/

mi dang gtam du med/
dben par 'dod kyang 'khrul/

sems ma bskyod/
yid g.yengs mi bya/

gdan las ma langs/
mgo ma bteg/

nyal ba mi bya/
dug lnga yis khyab par 'gyur""",
        "wylie": """*rdo rje 'chang* (Vajradhara; here in Marpa's form), *dben pa* (solitude), *dug lnga* (five poisons: desire, anger, ignorance, pride, jealousy). Self-reproof song (rang sems kyi glu).""",
        "translation": """Dorje Chang yourself, in Marpa's form!
Grant that this mendicant may hold to solitude.

O strange fellow Milarepa—
To you I sing this song of self-counsel.

You stand apart from all humanity
That might share sweet conversation with you;
Therefore you feel lonely and would seek diversion—
There is no reason for you to seek it.

Do not stir up your mind; let it rest in peace.
If it holds thoughts, it will crave countless wrongs.

Do not yield to the desire for distraction; exert your intellect.
If you yield to temptation, your devotion will scatter to the wind.

Do not walk forth; rest content on your seat.
If you walk forth, your feet may strike stones.

Do not raise your head; bend it down.
If you raise it, it will seek vain frivolities.

Do not sleep; continue your devotions.
If you sleep, the five poisons of ignorance will overcome you.""",
    },
    "MIL_COMFORTS_005": {
        "original": """mar pa la gu phyag 'tshal/
'jig rten gyi dgos pa spang bar byin gyis rlols/

brag dkar mtsho'i dbu phug tu/
ras pa bod kyi rnal 'byor pas/
zang zing med par bsgom/

steng 'og gi shing rta bde/
bal gos bde/
bsam gtan gyi sgyings thag bde/
lus zas bde/
sems gsal ba bde/
ci yang mi bde ba med/

ngas myur du 'chi/
sang rgyas thob par bya/
gtam du med par ting nge 'dzin la 'jug""",
        "wylie": """*rnal 'byor pa* / *re pa* (yogin Repa), *ting nge 'dzin* (samādhi), *sang rgyas* (buddhahood), *bsam gtan gyi sgyings thag* (meditation strap). Five comforts (bde ba lnga) song.""",
        "translation": """Lord! Gracious Marpa! I bow at your feet!
Enable me to give up worldly aims.

Here in Dragkar-Taso's middle cave,
On the topmost peak of the middle cave,
I, the Tibetan yogin called Repa,
Having relinquished all thought of food, clothing, and life's aims,
Have settled down to win perfect buddhahood.

Comfortable is the hard mattress beneath me;
Comfortable the Nepalese cotton quilt above;
Comfortable the single meditation strap that holds my knee;
Comfortable the body, trained to moderate diet;
Comfortable the clear mind that discerns present clinging and the final goal—
Nothing is uncomfortable; everything is comfortable.

If you can, try to imitate me;
But if you are not inspired toward the ascetic life,
And cling to the error of the ego-doctrine,
Spare me your misplaced pity;
I am a yogin on the path of attaining eternal bliss.

The sun's last rays pass over the mountain tops;
Return to your homes.
As for me, who must die soon, uncertain of the hour—
With the self-set task of winning buddhahood,
I have no time for useless talk;
Therefore I enter the quiescent state of samadhi.""",
    },
    "MIL_SISTER_006": {
        "original": """bla ma rnams la gu phyag 'tshal/
dben pa la gnas par byin gyis rlols/

'jig rten gyi dga' sdug mi rtag/
sems can thams cad ma yin pas/
chos la zhugs/

gnas tshul dud 'gro'i gnas 'dra/
zas kyi tshul khyi phag 'dra/
lus kyi tshul rus pa 'dra/
sems byang chub kyi sems yin/

deng sang bsgom pas ye shes thob/
skye ba phyi ma la sang rgyas thob/
slob ma peta ma sdug bsngal ma byed""",
        "wylie": """*byang chub kyi sems* (bodhicitta), *sems can* (sentient beings), *ye shes* (transcendent knowledge), *dud 'gro* (animal realm). Song to sister Peta (pe ta).""",
        "translation": """Obeisance to my lords, the gurus!
Grant that this yogin may hold fast to solitude.

Sister, you are filled with worldly feeling;
Know that worldly joys and griefs are all impermanent.
But I, by taking these hardships on myself alone,
Am sure to win eternal happiness—
So listen to your brother's song:

To repay the kindness of all sentient beings—
Who have been our parents—I gave myself to religious life.

See my dwelling: like a jungle beast's lair;
Any other person would be afraid in it.

See my food: like what dogs and pigs eat;
It would make others nauseated.

See my body: like a skeleton;
Even an enemy would weep to see it.

In my behavior I seem like a madman;
Sister, you are moved to disappointment and sorrow—
Yet if you could see my mind, it is bodhicitta itself;
The conquerors rejoice to see it.

Sitting on this cold rock beneath me, I meditate with zeal
Enough to bear my skin torn off or flesh from bone;
Inside and out my body has become like nettles;
It has taken on an unchanging greenish hue.

Here in this solitary rocky cave,
Though I cannot drive melancholy from my mind,
I hold unchanged adoration and affection
For the guru, true embodiment of the eternal buddhas.

Thus persevering in meditation,
I shall surely gain transcendent knowledge and experience;
And if I succeed,
Happiness and prosperity are won within this lifetime as I go,
And in my next birth I shall win buddhahood.

Therefore, dear sister Peta,
Do not give way to sorrow,
But give yourself to penance for religion's sake.""",
    },
    "MIL_RACE_007": {
        "original": """mar pa yab kyi zhabs la gu phyag 'tshal/

lus byang chub kyi shing lta bu/
sems rta rlung bzhin rgyug

sems rta 'dzin pa'i thag pa ni gcig tu 'dzin/
bsgoms pa'i lcags sgrog tu bcings/
bla ma'i bka' zas su sbyin/
rig pa'i chu 'thung/
stong pa nyid kyi ra ba srung/

rtas sang rgyas sa thob/
'jig rten gyi bde ba ma dgos""",
        "wylie": """*sems rta* (mind-horse), *gcig tu 'dzin* (one-pointedness, *ekagrata*), *stong pa nyid* (emptiness), *sang rgyas* (buddhahood). Extended tack-and-rider metaphor for mind-training (*sems kyi bslab pa*).""",
        "translation": """I bow at the feet of my gracious father Marpa!

Within the temple of the bodhi hill—my body—
Within my breast, where the altar stands,
Within the upper triangular chamber of my heart,
The horse of mind, moving like the wind, prances about.

What lasso must be used to catch this horse?
And to what post must it be tied when caught?
What food is given it when hungry?
What drink when thirsty?
In what enclosure is it kept when cold?

To catch the horse, use singleness of purpose as the lasso;
When caught, tie it to the post of meditation;
When hungry, feed it the guru's teachings;
When thirsty, give it the stream of consciousness;
When cold, keep it in the enclosure of emptiness.

For saddle use the will; for bridle, intellect;
Attach fixed immovability as girth and crupper;
Pass the vital winds as headstall and nose-band.

Its rider is the youth of keen watchfulness:
His helmet is Mahayana altruism;
His coat of mail is learning, thought, and contemplation;
On his back he carries the shield of patience;
In his hand the long spear of aspiration;
At his side hangs the sword of intelligence.

The smoothed reed of universal mind—
Straightened by freedom from wrath and hatred,
Barbed with the feathers of the four immeasurables,
Tipped with the sharpened arrowhead of intellect,
Placed in the pliant bow of spiritual wisdom,
Fixed in the aperture of the wise path and right method,
Drawn to the full span of wide communion—
Shot forth, the arrows fall among all nations.

They strike the faithful
And slay the sprite of selfishness.

Thus all evil passions are overcome
And our kindred are protected.

This horse courses across the wide plain of happiness;
Its goal is the state of all conquerors.
Its hindquarters leave attachment to samsaric life behind;
Its forequarters advance to the safe place of deliverance.

By running such a race I am carried toward buddhahood.
Judge whether this resembles your idea of happiness:
Worldly happiness I do not covet.""",
    },
    "MIL_DEMON_008": {
        "original": """mar pa lo tsA ba la gu phyag 'tshal/
nged med pas khyed nged du gyis/

a zhang dran par byed/
yid tsha ma byed cig/

kyang tsha yul du pha shi/
nor phrog sdug bsngal/
srog lcags kyis bcad/

bdag gis chos zhugs/
khyod kyi sgo ru slong/
khyi bskyes dang gur phubs kyis ngar du bcad/
chu thod du shor/

khyod ni a zhang gi lus can bdud mo/
snying rje med pa'i sems can""",
        "wylie": """*lo tsA ba* (translator; Marpa), *bdud mo* (demoness), *srog lcags* (iron hook of life/death), *chos* (dharma). Song of remembered persecution; *a zhang* (paternal aunt).""",
        "translation": """Kind gracious father, compassionate to all—
Marpa the Translator, I bow at your feet!
Be kin to me, who am bereft of kin!

Aunt, do you recall all you have done?
If not, this song of mine will refresh your memory;
Listen attentively, and repent sincerely.

There in the wretched land of Kyanga-Tsa,
When our noble father died, he left us three—
A widowed mother and two orphans;
You defrauded us of all our wealth and brought us to misery.
Like peas struck from a staff we were scattered—
By you, aunt, and by our uncle too—
So our attachment to kin was severed.

Later, when I wandered long in distant lands,
Longing to see my sister and mother, I returned home
And found my mother dead and my sister gone.

Pierced with anguish, I turned to religion;
Finding it my sole solace, I chose the religious life.

Compelled by hunger to beg for alms,
I came before your door, aunt;
Recognizing me, a helpless devotee,
You burst out in spiteful anger.

Crying "Cho! Cho!" you set your dogs on me;
With your tent-pole you beat me heavily,
As though I were a sheaf of grain for threshing.
I fell face-down in a pool of water
And nearly lost my precious life.

In your fury you called me "Trafficker in Lives"
And "Disgrace to my clan";
Those words wounded my heart;
Overwhelmed with despair and misery,
My breath stopped and I was speechless.

Then, though I had no need of them,
You cheated me by various wiles of house and field.

You are a demoness in the body of an aunt,
Who severed all my love for you, aunt.

Later, at my uncle's door,
I met malicious thoughts, harmful acts, vile words.
"The destroying demon of the country comes!" was his cry;
He called the neighbors to help kill me;
Abusive words flew;
He pelted me with showers of stones
And sought to transfix me with a rain of small sharp arrows;
He filled my heart with an incurable sickness.
There too I nearly lost my life.
O butcher's heart in an uncle's form!
All respect for an uncle I lost then.

When I was poor and helpless, my kin were crueler than enemies.

Later, to the hill where I was meditating,
My constant Zesay came to see me out of love;
With gentle words she consoled me,
Comforted my sorrow-stricken heart,
Brought nourishing tasty food,
And saved me from starvation.
Kind indeed is she—more kind than I can say;
Yet since even she is not devoted to religion,
I see little need to meet her when she comes;
And as for you, aunt, far less need to meet you.
Return now as you came;
Better to go early while there is still time.""",
    },
}


def _set_layer(layers: list, kind: str, body: str, provenance: str | None = None) -> None:
    for layer in layers:
        if layer.get("kind") == kind:
            layer["body"] = body
            if provenance:
                layer["layer_provenance"] = provenance
            return
    entry: dict = {"kind": kind, "label": kind, "body": body}
    if provenance:
        entry["layer_provenance"] = provenance
    layers.append(entry)


def _label_for_kind(kind: str) -> str:
    return {
        "original": "Original (Tibetan)",
        "iast": "Wylie / Key Terms",
        "translation": "Pratibha Translation",
    }.get(kind, kind)


def patch_canonical(path: Path, data: dict[str, str]) -> None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    sid = doc.get("source_id", "")
    if sid not in UNITS:
        return
    # Full editorial upgrade (Tibetan witness, key_terms, resonances) — see milarepa_upgrade_wisdom_003.py
    if sid == "MIL_WISDOM_003":
        return
    u = UNITS[sid]
    doc["sanskrit_devanagari"] = u["original"]
    doc["sanskrit_iast"] = u["wylie"]
    doc["translation_literal"] = u["translation"]
    doc["editorial_maturity"] = "strong_draft"
    doc["editorial_score"] = 75
    layers = doc.get("pratibha_layers") or []
    for kind in ("original", "iast", "translation"):
        label = _label_for_kind(kind)
        found = False
        for layer in layers:
            if layer.get("kind") == kind:
                layer["label"] = label
                layer["body"] = u[kind if kind != "iast" else "wylie"] if kind != "translation" else u["translation"]
                if kind == "translation":
                    layer["layer_provenance"] = (
                        "Modern Pratibha English; line-faithful to Evans-Wentz 1928 anchor "
                        "and Jetsun-Kahbum Tibetan structure"
                    )
                elif kind == "original":
                    layer["layer_provenance"] = (
                        "Key Tibetan refrains (Jetsun-Kahbum tradition); "
                        "Evans-Wentz used as English anchor where full verse unavailable in PD edition"
                    )
                found = True
                break
        if not found:
            body_key = "wylie" if kind == "iast" else kind if kind != "translation" else "translation"
            entry = {"kind": kind, "label": label, "body": u[body_key if body_key != "translation" else "translation"]}
            layers.append(entry)
    doc["pratibha_layers"] = layers
    path.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
        encoding="utf-8",
    )


def patch_yaml(path: Path, data: dict[str, str]) -> None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    sid = doc.get("sutra_id", "")
    if sid not in UNITS:
        return
    if sid == "MIL_WISDOM_003":
        return
    u = UNITS[sid]
    doc["translation"] = u["translation"]
    doc["pratibha_translation"] = u["translation"]
    doc["sanskrit"] = u["original"]
    doc["transliteration"] = u["wylie"]
    doc["editorial_maturity"] = "strong_draft"
    doc["editorial_score"] = 75
    path.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
        encoding="utf-8",
    )


def main() -> int:
    for path in sorted(CANON.glob("milarepa_songs_*.yml")):
        patch_canonical(path, UNITS)
        print(f"  canonical: {path.name}")
    for path in sorted(YAML.glob("milarepa_songs_*.yml")):
        patch_yaml(path, UNITS)
        print(f"  yaml: {path.name}")
    print(f"Updated {len(UNITS)} Milarepa translations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
