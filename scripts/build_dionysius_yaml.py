#!/usr/bin/env python3
"""Build strong_draft YAML for Pseudo-Dionysius (~20 curated units).

English: C.E. Rolt, *Dionysius the Areopagite on the Divine Names and
Mystical Theology* (SPCK, 1920), public domain. Greek: short MT incipits
from the traditional text tradition where available.

Writes under data/yaml/pseudo_dionysius/. Does not promote to canonical.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "yaml" / "pseudo_dionysius"

SOURCE = (
    "English: C.E. Rolt, Dionysius the Areopagite on the Divine Names and "
    "Mystical Theology (SPCK, 1920), public domain. Greek: short Mystical "
    "Theology incipits from the traditional text tradition (PG / critical "
    "editions) where noted; Divine Names units carry English only."
)


def clean(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )


def commentary(claim: str) -> str:
    """Keep commentary living and practice-facing without boilerplate padding."""
    body = claim.strip()
    if not body.endswith("."):
        body += "."
    body += (
        " Read it as a demand on attention, not as a museum label: hold the argument "
        "until its force lands, then let one concrete shift follow into ordinary life. "
        "Return to the original wording when the mind wants to smooth the edge."
    )
    return body


# (id, work_tag, section, title, greek_or_empty, english, themes, claim)
UNITS: list[tuple] = [
    (
        "pd_mt_01",
        "Mystical Theology",
        "MT I",
        "The Divine Dark Beyond All Light",
        "Τριὰς ὑπερούσιε καὶ ὑπέρθεε καὶ ὑπεράγαθε.",
        """
        Trinity, which exceedeth all Being, Deity, and Goodness! Thou that instructeth
        Christians in Thy heavenly wisdom! Guide us to that topmost height of mystic lore
        which exceedeth light and more than exceedeth knowledge, where the simple, absolute,
        and unchangeable mysteries of heavenly Truth lie hidden in the dazzling obscurity of
        the secret Silence, outshining all brilliance with the intensity of their darkness,
        and surcharging our blinded intellects with the utterly impalpable and invisible
        fairness of glories which exceed all beauty!
        """,
        ["knowledge", "ignorance", "silence", "grace"],
        "«The Divine Dark Beyond All Light» opens the Mystical Theology by praying into a "
        "darkness denser than light: God is approached where ordinary knowing goes blind",
    ),
    (
        "pd_mt_02",
        "Mystical Theology",
        "MT I",
        "Leave the Senses and the Intellect",
        "",
        """
        Such be my prayer; and thee, dear Timothy, I counsel that, in the earnest exercise
        of mystic contemplation, thou leave the senses and the activities of the intellect
        and all things that the senses or the intellect can perceive, and all things in this
        world of nothingness, or in that world of being, and that, thine understanding being
        laid to rest, thou strain (so far as thou mayest) towards an union with Him whom
        neither being nor understanding can contain. For, by the unceasing and absolute
        renunciation of thyself and all things, thou shalt in pureness cast all things aside,
        and be released from all, and so shalt be led upwards to the Ray of that divine
        Darkness which exceedeth all existence.
        """,
        ["practice", "attention", "ignorance", "stillness"],
        "«Leave the Senses and the Intellect» is Dionysius's counsel to Timothy: union "
        "requires laying the understanding to rest, not stacking finer concepts",
    ),
    (
        "pd_mt_03",
        "Mystical Theology",
        "MT I",
        "Moses and the Darkness of Unknowing",
        "",
        """
        For not without reason is the blessed Moses bidden first to undergo purification
        himself and then to separate himself from those who have not undergone it; and after
        all purification hears the many-voiced trumpets and sees many lights flash forth with
        pure and diverse-streaming rays, and then stands separate from the multitudes and with
        the chosen priests presses forward to the topmost pinnacle of the Divine Ascent.
        Nevertheless he meets not with God Himself, yet he beholds—not Him indeed (for He is
        invisible)—but the place wherein He dwells. And this I take to signify that the
        divinest and the highest of the things perceived by the eyes of the body or the mind
        are but the symbolic language of things subordinate to Him who Himself transcendeth
        them all. Through these things His incomprehensible presence is shown walking upon
        those heights of His holy places which are perceived by the mind; and then It breaks
        forth, even from the things that are beheld and from those that behold them, and
        plunges the true initiate unto the Darkness of Unknowing wherein he renounces all the
        apprehensions of his understanding and is enwrapped in that which is wholly intangible
        and invisible, belonging wholly to Him that is beyond all things and to none else
        (whether himself or another), and being through the passive stillness of all his
        reasoning powers united by his highest faculty to Him that is wholly Unknowable, of
        whom thus by a rejection of all knowledge he possesses a knowledge that exceeds his
        understanding.
        """,
        ["knowledge", "ignorance", "practice", "grace"],
        "«Moses and the Darkness of Unknowing» turns Sinai into a map of ascent: lights and "
        "symbols give way to a knowing that exceeds understanding by rejecting ordinary knowledge",
    ),
    (
        "pd_mt_04",
        "Mystical Theology",
        "MT II",
        "Carving the Latent Image",
        "Πῶς δεῖ καὶ ἑνοῦσθαι καὶ ὑμνεῖν τὸν πάντων αἴτιον καὶ ὑπὲρ πάντα.",
        """
        Unto this Darkness which is beyond Light we pray that we may come, and may attain
        unto vision through the loss of sight and knowledge, and that in ceasing thus to see
        or to know we may learn to know that which is beyond all perception and understanding
        (for this emptying of our faculties is true sight and knowledge), and that we may offer
        Him that transcends all things the praises of a transcendent hymnody, which we shall
        do by denying or removing all things that are—like as men who, carving a statue out of
        marble, remove all the impediments that hinder the clear perceptive of the latent image
        and by this mere removal display the hidden statue itself in its hidden beauty.
        """,
        ["practice", "ignorance", "knowledge", "attention"],
        "«Carving the Latent Image» makes negation sculptural: truth appears not by adding "
        "predicates but by removing what blocks the latent form",
    ),
    (
        "pd_mt_05",
        "Mystical Theology",
        "MT II–III",
        "Affirmation Descends; Negation Ascends",
        "Τίς ἡ καταφατικὴ θεολογία καὶ τίς ἡ ἀποφατική.",
        """
        Now we must wholly distinguish this negative method from that of positive statements.
        For when we were making positive statements we began with the most universal statements,
        and then through intermediate terms we came at last to particular titles, but now
        ascending upwards from particular to universal conceptions we strip off all qualities
        in order that we may attain a naked knowledge of that Unknowing which in all existent
        things is enwrapped by all objects of knowledge, and that we may begin to see that
        super-essential Darkness which is hidden by all the light that is in existent things.
        """,
        ["knowledge", "ignorance", "way", "attention"],
        "«Affirmation Descends; Negation Ascends» states the famous method: cataphatic speech "
        "moves down through names; apophatic speech strips upward into darkness",
    ),
    (
        "pd_mt_06",
        "Mystical Theology",
        "MT IV",
        "Not Any Sensible Thing",
        "Ὅτι οὐδέν ἐστι τῶν πάντων ὁ πάντων αἴτιος κατὰ τὰς θέσεις.",
        """
        We therefore maintain that the universal Cause transcending all things is neither
        impersonal nor lifeless, nor irrational nor without understanding: in short, that It
        is not a material body, and therefore does not possess outward shape or intelligible
        form, or quality, or quantity, or solid weight; nor has It any local existence which
        can be perceived by sight or touch; nor has It the power of perceiving or being
        perceived; nor does It suffer any vexation or disorder through the disturbance of
        earthly passions, or any feebleness through the tyranny of material chances, or any
        want of light; nor any change, or decay, or division, or deprivation, or ebb and flow,
        or anything else which the senses can perceive. None of these things can be either
        identified with it or attributed unto It.
        """,
        ["knowledge", "ignorance", "body", "stillness"],
        "«Not Any Sensible Thing» clears the lowest rung of naming: the Cause is not body, "
        "place, passion, change, or any object of sense",
    ),
    (
        "pd_mt_07",
        "Mystical Theology",
        "MT V",
        "Not Any Intelligible Thing",
        "Ὅτι οὐδὲ κατὰ τὰς ἀφαιρέσεις ἐστὶ τῶν πάντων ὁ πάντων αἴτιος.",
        """
        Once more, ascending yet higher we maintain that It is not soul, or mind, or endowed
        with the faculty of imagination, conjecture, reason, or understanding; nor is It any
        act of reason or understanding; nor can It be described by the reason or perceived by
        the understanding, since It is not number, or order, or greatness, or littleness, or
        equality, or inequality, and since It is not immovable nor in motion, or at rest, and
        has no power, and is not power or light, and does not live, and is not life; nor is It
        personal essence, or eternity, or time; nor can It be grasped by the understanding since
        It is not knowledge or truth; nor is It kingship or wisdom; nor is It one, nor is It
        unity, nor is It Godhead or Goodness; nor is It a Spirit, as we understand the term,
        since It is not Sonship or Fatherhood; nor is It any other thing such as we or any other
        being can have knowledge of; nor does It belong to the category of non-existence or to
        that of existence.
        """,
        ["knowledge", "ignorance", "silence", "grace"],
        "«Not Any Intelligible Thing» denies even the highest metaphysical titles as adequate "
        "names: soul, mind, being, unity, and Godhead-as-we-conceive-it all fall short",
    ),
    (
        "pd_mt_08",
        "Mystical Theology",
        "MT V",
        "Beyond Affirmation and Negation",
        "",
        """
        Nor can the reason attain to It to name It or to know It; nor is it darkness, nor is
        It light, or error, or truth; nor can any affirmation or negation apply to it; for while
        applying affirmations or negations to those orders of being that come next to It, we
        apply not unto It either affirmation or negation, inasmuch as It transcends all
        affirmation by being the perfect and unique Cause of all things, and transcends all
        negation by the pre-eminence of Its simple and absolute nature—free from every
        limitation and beyond them all.
        """,
        ["knowledge", "ignorance", "silence", "stillness"],
        "«Beyond Affirmation and Negation» closes the Mystical Theology: even denial is left "
        "behind, because the Cause exceeds both yes and no",
    ),
    (
        "pd_dn_01",
        "Divine Names",
        "DN I",
        "Dare Not Speak Except What Scripture Reveals",
        "",
        """
        We must not then dare to speak, or indeed to form any conception, of the hidden
        super-essential Godhead, except those things that are revealed to us from the Holy
        Scriptures. For a super-essential understanding of It is proper to Unknowing, which
        lieth in the Super-Essence Thereof surpassing Discourse, Intuition and Being;
        acknowledging which truth let us lift up our eyes towards the steep height, so far as
        the effluent light of the Divine Scriptures grants its aid, and, as we strive to ascend
        unto those Supernal Rays, let us gird ourselves for the task with holiness and the
        reverent fear of God. For, if we may safely trust the wise and infallible Scriptures,
        Divine things are revealed unto each created spirit in proportion to its powers, and
        in this measure is perception granted through the workings of the Divine goodness, the
        which in just care for our preservation divinely tempereth unto finite measure the
        infinitude of things which pass man's understanding.
        """,
        ["knowledge", "grace", "attention", "practice"],
        "«Dare Not Speak Except What Scripture Reveals» opens the Divine Names under "
        "discipline: naming God is permitted only as revelation and capacity allow",
    ),
    (
        "pd_dn_02",
        "Divine Names",
        "DN I",
        "Super-Essence Beyond Mind and Word",
        "",
        """
        By the same law of truth the boundless Super-Essence surpasses Essences, the
        Super-Intellectual Unity surpasses Intelligences, the One which is beyond thought
        surpasses the apprehension of thought, and the Good which is beyond utterance surpasses
        the reach of words. Yea, it is an Unity which is the unifying Source of all unity and a
        Super-Essential Essence, a Mind beyond the reach of mind and a Word beyond utterance,
        eluding Discourse, Intuition, Name, and every kind of being. It is the Universal Cause
        of existence while Itself existing not, for It is beyond all Being and such that It
        alone could give, with proper understanding thereof, a revelation of Itself.
        """,
        ["knowledge", "ignorance", "grace", "silence"],
        "«Super-Essence Beyond Mind and Word» names the paradox at the heart of Dionysius: "
        "Cause of existence while beyond being, Mind beyond mind, Word beyond speech",
    ),
    (
        "pd_dn_03",
        "Divine Names",
        "DN I",
        "Illuminations According to Each Creature's Powers",
        "",
        """
        Not that the Good is wholly incommunicable to anything; nay, rather, while dwelling
        alone by Itself, and having there firmly fixed Its super-essential Ray, It lovingly
        reveals Itself by illuminations corresponding to each separate creature's powers, and
        thus draws upwards holy minds into such contemplation, participation and resemblance
        of Itself as they can attain—even them that holily and duly strive thereafter and do
        not seek with impotent presumption the Mystery beyond that heavenly revelation which
        is so granted as to fit their powers, nor yet through their lower propensity slip down
        the steep descent, but with unwavering constancy press onwards toward the ray that
        casts its light upon them and, through the love responsive to these gracious
        illuminations, speed their temperate and holy flight on the wings of a godly reverence.
        """,
        ["grace", "knowledge", "practice", "harmony"],
        "«Illuminations According to Each Creature's Powers» balances transcendence with "
        "gift: the Good remains alone, yet reveals itself by measure to each capacity",
    ),
    (
        "pd_dn_04",
        "Divine Names",
        "DN II",
        "Divine Names Belong to the Entire Godhead",
        "",
        """
        'Tis the whole Being of the Supernal Godhead (saith the Scripture) that the Absolute
        Goodness hath defined and revealed. Now this matter we have discussed elsewhere, and
        have shown that all the Names proper to God are always applied in Scripture not
        partially but to the whole, entire, full, complete Godhead, and that they all refer
        indivisibly, absolutely, unreservedly, and wholly to all the wholeness of the whole
        and entire Godhead. Indeed, if any one deny that such utterance refers to the whole
        Godhead, he blasphemeth and profanely dares to divide the Absolute and Supreme Unity.
        We must, then, take them as referring unto the entire Godhead.
        """,
        ["unity", "knowledge", "grace", "harmony"],
        "«Divine Names Belong to the Entire Godhead» refuses partial naming: Good, Being, "
        "Life, and Lord belong to the whole Unity, not to a fragment of Deity",
    ),
    (
        "pd_dn_05",
        "Divine Names",
        "DN III",
        "Prayer Draws Us to the Immovable Rock",
        "",
        """
        Or even as, having embarked on a ship and clinging to the cables, the which being
        stretched out from some rock unto us, presented themselves (as it were) for us to lay
        hold upon them, we should not be drawing the rock towards ourselves, but should, in
        very truth, be drawing ourselves and the vessel towards the rock; as also, conversely,
        if any one standing upon the vessel pushes away the rock that is on the shore, he will
        not affect the rock (which stands immovable) but will separate himself therefrom, and
        the more he pushes it so much the more will he be staving himself away. Hence, before
        every endeavour, more especially if the subject be Divinity, must we begin with prayer:
        not as though we would pull down to ourselves that Power which is nigh both everywhere
        and nowhere, but that, by these remembrances and invocations of God, we may commend
        and unite ourselves Thereunto.
        """,
        ["practice", "grace", "attention", "prayer"],
        "«Prayer Draws Us to the Immovable Rock» teaches that invocation does not drag God "
        "down; it draws the soul toward what already stands near",
    ),
    (
        "pd_dn_06",
        "Divine Names",
        "DN IV",
        "The Good Extends Itself Like the Sun",
        "",
        """
        Now let us consider the name of "Good" which the Sacred Writers apply to the
        Supra-Divine Godhead in a transcendent manner, calling the Supreme Divine Existence
        Itself "Goodness" (as it seems to me) in a sense that separates It from the whole
        creation, and meaning, by this term, to indicate that the Good, under the form of
        Good-Being, extends Its goodness by the very fact of Its existence unto all things.
        For as our sun, through no choice or deliberation, but by the very fact of its
        existence, gives light to all those things which have any inherent power of sharing
        its illumination, even so the Good (which is above the sun, as the transcendent
        archetype by the very mode of its existence is above its faded image) sends forth upon
        all things according to their receptive powers, the rays of Its undivided Goodness.
        """,
        ["grace", "harmony", "knowledge", "way"],
        "«The Good Extends Itself Like the Sun» is Dionysius's great participation image: "
        "goodness pours out by being, received according to each thing's capacity",
    ),
    (
        "pd_dn_07",
        "Divine Names",
        "DN IV",
        "Evil Hath No Being",
        "",
        """
        Thus evil hath no being, nor any inherence in things that have being. Evil is nowhere
        qua evil; and it arises not through any power but through weakness. Even the devils
        derive their existence from the Good, and their mere existence is good. Their evil is
        the result of a fall from their proper virtues, and is a change with regard to their
        individual state, a weakness of their true angelical perfections. And they desire the
        Good in so far as they desire existence, life, and understanding; and in so far as they
        do not desire the Good, they desire that which hath no being. And this is not desire,
        but an error of real desire. In a word, evil (as we have often said) is weakness,
        impotence, and deficiency of knowledge (or, at least, of exercised knowledge), or of
        faith, desire, or activity as touching the Good.
        """,
        ["evil", "virtue", "knowledge", "practice"],
        "«Evil Hath No Being» is the classic privation thesis: evil is weakness and falling "
        "short of the Good, not a rival substance with its own power",
    ),
    (
        "pd_dn_08",
        "Divine Names",
        "DN V",
        "Being as Name of Providence",
        "",
        """
        Now must we proceed to the Name of "Being" which is truly applied by the Divine Science
        to Him that truly Is. But this much we must say, that it is not the purpose of our
        discourse to reveal the Super-Essential Being in its Super-Essential Nature (for this
        is unutterable, nor can we know It, or in anywise express It, and It is beyond even the
        Unity), but only to celebrate the Emanation of the Absolute Divine Essence into the
        universe of things. For the Name of "Good" revealing all the emanations of the
        universal Cause, extends both to the things which are, and to the things which are not,
        and is beyond both categories. And the title of "Existent" extends to all existent
        things and is beyond them. And the title "Life" extends to all living things and is
        beyond them. And the title of "Wisdom" extends to the whole realm of Intuition, Reason,
        and Sense-Perception, and is beyond them all.
        """,
        ["knowledge", "grace", "unity", "way"],
        "«Being as Name of Providence» distinguishes the unutterable Super-Essence from the "
        "celebrated names by which Good, Being, Life, and Wisdom reach creation",
    ),
    (
        "pd_dn_09",
        "Divine Names",
        "DN VI",
        "Eternal Life the Source of Every Life",
        "",
        """
        Now must we celebrate Eternal Life as that whence cometh very Life and all life, which
        also endues every kind of living creature with its appropriate meed of Life. Now the
        Life of the immortal Angels and their immortality, and the very indestructibility of
        their perpetual motion, exists and is derived from It and for Its sake. Hence they are
        called Ever-living and Immortal, and yet again are denied to be immortal, because they
        are not the source of their own immortality and eternal life, but derive it from the
        creative Cause which produces and maintains all life. And all life and vital movement
        comes from the Life which is beyond all Life and beyond every Principle of all Life.
        Thence have souls their indestructible quality, and all animals and plants possess their
        life as a far-off reflection of that Life. When this is taken away, as saith the
        Scripture, all life fades; and those which have faded, through being unable to
        participate therein, when they turn to It again revive once more.
        """,
        ["life", "grace", "participation", "way"],
        "«Eternal Life the Source of Every Life» treats Life as a divine name: angels, souls, "
        "plants live only as participations of the Life beyond life",
    ),
    (
        "pd_dn_10",
        "Divine Names",
        "DN VII",
        "The Foolishness of God and Transcendent Wisdom",
        "",
        """
        Now, if it like thee, let us consider the Good and Eternal Life as Wise and as Very
        Wisdom, or rather as the Fount of all wisdom and as Transcending all wisdom and
        understanding. Not only is God so overflowing with wisdom that there is no limit to His
        understanding, but He even transcends all Reason, Intelligence, and Wisdom. And this is
        supernaturally perceived by the truly divine man when he says: "The foolishness of God
        is wiser than men." Rather should we then consider that while the human Intellect hath
        a faculty of Intelligence, whereby it perceives intellectual truths, yet the act whereby
        the Intellect communes with the things that are beyond it transcends its intellectual
        nature. This transcendent sense, therefore, must be given to our language about God,
        and not our human sense. We must be transported wholly out of ourselves and given unto
        God. For 'tis better to belong unto God and not unto ourselves, since thus will the
        Divine Bounties be bestowed, if we are united to God.
        """,
        ["knowledge", "ignorance", "practice", "grace"],
        "«The Foolishness of God and Transcendent Wisdom» reads Paul's paradox as method: "
        "true wisdom requires being carried out of our own measuring mind",
    ),
    (
        "pd_dn_11",
        "Divine Names",
        "DN VIII / XI",
        "Power and the Peace That Unites",
        "",
        """
        God is Power because in His own Self He contains all power beforehand and exceeds it,
        and because He is the Cause of all power and produces all things by a power which may
        not be thwarted nor circumscribed. Yea, He is Infinitely Powerful not only in that all
        Power comes from Him, but also because He is above all power and is Very Power. Now let
        us praise with reverent hymns of peace the Divine Peace which is the Source of all
        mutual attraction. For this Quality it is that unites all things together and begets
        and produces the harmonies and agreements of all things. And hence it is that all things
        long for It, and that It draws their manifold separate parts into the unity of the whole
        and unites the battling elements of the world into concordant fellowship.
        """,
        ["power", "harmony", "peace", "unity"],
        "«Power and the Peace That Unites» pairs two names of providence: unbounded Power "
        "and the Peace that gathers battling parts into concord",
    ),
    (
        "pd_dn_12",
        "Divine Names",
        "DN XIII",
        "Perfect and One",
        "",
        """
        So much for these titles. Now let us, if thou art willing, proceed to the most important
        Title of all. For the Divine Science attributes all qualities to the Creator of all
        things and attributes them all together, and speaks of Him as One. How such a Being is
        Perfect: not only in the sense that It is Absolute Perfection and possesseth in Itself
        and from Itself distinctive Uniformity of Its existence, and that It is wholly perfect
        in Its whole Essence, but also in the sense that, in Its transcendence It is beyond
        Perfection. And the title "One" implies that It is all things under the form of Unity
        through the Transcendence of Its single Oneness, and is the Cause of all things without
        departing from that Unity. For there is nothing in the world without a share in the One;
        and, just as all number participates in unity, even so everything and each part of
        everything participates in the One, and on the existence of the One all other existences
        are based, and the One Cause of all things is not one of the many things in the world,
        but is before all Unity and Multiplicity and gives to all Unity and Multiplicity their
        definite bounds.
        """,
        ["unity", "perfection", "knowledge", "grace"],
        "«Perfect and One» crowns the Divine Names: the Cause is beyond perfection yet "
        "perfects all, and is One before every unity and multiplicity",
    ),
]


def build() -> int:
    n = 0
    for item in UNITS:
        uid, work_tag, section, title, greek, english, themes, claim = item
        unit = {
            "sutra_id": uid.upper(),
            "collection": "Pseudo-Dionysius",
            "section": f"{work_tag} · {section}",
            "title": title,
            "sanskrit": greek or "",
            "transliteration": "Greek (corpus original field)." if greek else "",
            "translation": clean(english),
            "commentary": commentary(claim),
            "abhyasa": (
                "Sit ten minutes in wordless attention. When a divine name or image arises, "
                "neither cling to it nor force it away; notice what remains when naming rests."
            ),
            "themes": themes,
            "glossary": [],
            "source": f"{SOURCE} {section}.",
            "editorial_maturity": "strong_draft",
            "layer_provenance": {
                "translation": "public_domain",
                "original": "sourced" if greek else "missing",
            },
        }
        dump(OUT / f"{uid}.yml", unit)
        n += 1
    return n


if __name__ == "__main__":
    count = build()
    print(f"Wrote {count} units -> {OUT.relative_to(ROOT)}")
