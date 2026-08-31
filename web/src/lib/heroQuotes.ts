/**
 * Curated hero lines — four or five of the strongest sentences per text.
 * Shown when a collection mandala opens; they rotate while the gate is held.
 * Keep each line short enough to sit inside the mandala (roughly 28–140 chars).
 */

type QuoteBank = {
  pattern: RegExp;
  quotes: string[];
};

const HERO_QUOTES: QuoteBank[] = [
  {
    pattern: /bhagavad/i,
    quotes: [
      "You have a right to action, never to its fruits.",
      "The Self is never born, nor does it ever die.",
      "Yoga is skill in action.",
      "Beings are unmanifest in their beginning, manifest in their middle, unmanifest again in their end.",
      "I am the taste in water, the light of the sun and moon.",
    ],
  },
  {
    pattern: /astavakra|ashtavakra|a[sṣ][tṭ][aā]vakra/i,
    quotes: [
      "You are not the body, nor is the body yours. You are awareness.",
      "If you detach yourself from identification with the body, you will rest in your own nature.",
      "Liberation is not a future event. It is the nature of the one who sees.",
      "The world is a painting on the canvas of awareness.",
      "Desirelessness, simple knowing, and stillness — this is liberation.",
    ],
  },
  {
    pattern: /ch[aā]ndogya|khandogya/i,
    quotes: [
      "Tat tvam asi — that thou art.",
      "In the beginning this was Being, one without a second.",
      "The finest essence — that is the Self of this whole world.",
      "As rivers flowing into the ocean lose name and form, so the knower, freed from name and form, enters the divine.",
      "As by knowing one lump of clay, all that is made of clay is known.",
    ],
  },
  {
    pattern: /isavasya|[iī][sś][aā]v[aā]sya|isha.?upani/i,
    quotes: [
      "All this, whatsoever moves in this moving world, is pervaded by the Lord.",
      "He who sees all beings in the Self, and the Self in all beings, shrinks from nothing.",
      "Into blinding darkness enter those who worship ignorance; into greater darkness those who delight in knowledge alone.",
      "The face of truth is covered with a golden lid.",
      "He who knows both knowledge and ignorance together crosses death through the one and attains immortality through the other.",
    ],
  },
  {
    pattern: /katha|ka[tṭ]ha/i,
    quotes: [
      "The Self is not attained by the weak, nor by the careless, nor by mere austerity.",
      "Know the Self as the rider, the body as the chariot, the intellect as the charioteer.",
      "Arise, awake, seek the great ones and learn.",
      "That which is never heard of, nor thought, nor known — from that all this has sprung.",
      "The ancient one is not born, does not die; unborn, eternal, he is not slain when the body is slain.",
    ],
  },
  {
    pattern: /brihadaranyaka|b[rṛ]had[aā]ra[nṇ]yaka/i,
    quotes: [
      "Lead me from the unreal to the real, from darkness to light, from death to immortality.",
      "Neti, neti — not this, not this.",
      "When the Self is seen, heard, thought of, and known, all this is known.",
      "As a lump of salt thrown into water dissolves, so the Self has neither inside nor outside.",
      "This Self is dearer than a son, dearer than wealth, dearer than all else.",
    ],
  },
  {
    pattern: /mundaka|mu[nṇ][dḍ]aka/i,
    quotes: [
      "Two birds, companions, cling to the same tree; one eats the fruit, the other looks on without eating.",
      "Truth alone conquers, not falsehood.",
      "This Self cannot be attained by instruction, nor by intellect, nor by much learning.",
      "When he who is hidden in all beings is seen, the knots of the heart are cut.",
      "Take the bow of the Upaniṣad, set on it the arrow sharpened by meditation, and pierce the imperishable.",
    ],
  },
  {
    pattern: /mandukya|m[aā][nṇ][dḍ][uū]kya|gaudapada|gau[dḍ]ap[aā]da/i,
    quotes: [
      "Aum: this whole world is that syllable.",
      "The fourth is not inward knowing, not outward knowing, not both — unseen, ungraspable, the Self.",
      "There is no dissolution, no birth, none in bondage, no seeker, no one liberated.",
      "The world of duality is mere māyā; the non-dual alone is the truth.",
      "Turiya is the cessation of phenomena — peaceful, auspicious, non-dual.",
    ],
  },
  {
    pattern: /svetasvatara|[sś]vet[aā][sś]vatara/i,
    quotes: [
      "Hear, you who know Brahman: the God who stands in fire, in water, who has entered the whole world.",
      "He is the one who makes the one seed manifold.",
      "The Self, smaller than the small, greater than the great, is hidden in the heart of the creature.",
      "Knowing that God, one is released from all fetters.",
      "He is fire, he is the sun, he is the wind, he is the moon.",
    ],
  },
  {
    pattern: /patanjali|pata[nñ]jali|yoga.?s[uū]tra/i,
    quotes: [
      "Yoga is the stilling of the turnings of the mind.",
      "Then the seer rests in its own true form.",
      "Practice becomes firmly grounded when it is cultivated for a long time, without interruption, with care.",
      "Īśvara is a special self, untouched by afflictions, karma, and their ripening.",
      "When the mind is colored by the object, the object is known.",
    ],
  },
  {
    pattern: /ha[tṭ]ha.?yoga|pradipika|pradīpikā/i,
    quotes: [
      "Haṭha is a stairway for those who would climb to the height of rāja yoga.",
      "When the breath wanders, the mind is unsteady; when the breath is still, the mind is still.",
      "As salt dissolves in water, so the mind that has entered the Self becomes one with it.",
      "The yogi who is freed from all thought remains as if dead to the world — that is liberation.",
      "When the nāḍīs are purified, the body becomes light, the fire of digestion kindles, and the inner sound is heard.",
    ],
  },
  {
    pattern: /[sś]iva.?sa[mṃ]hit[aā]|shiva.?samhita/i,
    quotes: [
      "In this body is the sacred Ganges, here the sun and moon, here the holy places — why go elsewhere?",
      "When the sleeping kuṇḍalinī is awakened, the way to liberation opens.",
      "The mind is the cause of bondage and the mind is the cause of liberation.",
      "He who knows the self as the witness of all, remaining unattached, is free.",
      "The lotus of the heart is the dwelling of the Self; there the yogi should rest.",
    ],
  },
  {
    pattern: /vijnana.?bhairava|vij[nñ][aā]na.?bhairava/i,
    quotes: [
      "Bhairava is not found in ritual, nor in pilgrimage, nor in the recitation of mantras.",
      "When the breath is held at the end of inhalation or exhalation, the terrific one is revealed.",
      "If one contemplates the universe as a painting, the supreme awakening dawns.",
      "The bliss that arises when two gazes meet — that too is the meditation.",
      "Wherever the mind finds satisfaction, there, just there, contemplate the Self.",
    ],
  },
  {
    pattern: /siva.?s[uū]tra|[sś]iva.?s[uū]tra|shiva.?sutra/i,
    quotes: [
      "Caitanyam ātmā — consciousness itself is the Self.",
      "Knowledge is bondage.",
      "The unfolding of the center is the way.",
      "By union with the power of the will, the world appears.",
      "The waking world is a play of awareness; dream is its inner theatre.",
    ],
  },
  {
    pattern: /spanda/i,
    quotes: [
      "The spanda is the slight movement of the unmoving.",
      "That in which the universe shines, and which shines in the universe — that is the throb.",
      "When the yogi finds the spanda, he stands as the enjoyer of the arising and dissolving of all.",
      "Even in anger, even in joy, even in a sudden fright — there the spanda can be seized.",
      "Established in the throb, one is never a victim of the next thought.",
    ],
  },
  {
    pattern: /pratyabhij/i,
    quotes: [
      "Consciousness, of its own free will, unfolds the universe upon its own screen.",
      "The Self is already accomplished; recognition is not a becoming.",
      "When one knows 'I am Śiva,' the world is no longer a cage.",
      "Independence is the very nature of awareness.",
      "When the Lord is recognized as one's own Self, the universe becomes a play.",
    ],
  },
  {
    pattern: /tantras[aā]ra|abhinavagupta/i,
    quotes: [
      "The heart is the resting place of all, and from the heart all this shines forth.",
      "Recognition is not gained; it is uncovered.",
      "The universe is the overflowing of one's own consciousness.",
      "He who tastes the aesthetic flash (camatkāra) tastes the Self.",
      "Nothing exists that is not Śiva; to know this is to be free.",
    ],
  },
  {
    pattern: /yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini/i,
    quotes: [
      "The heart of the yoginī is the triangle of desire, knowledge, and action.",
      "She who is the pulse of the three cities dwells as one's own awareness.",
      "The śrīcakra is not drawn on the ground; it is the body of consciousness.",
      "When the mantra is known as one's own throb, the goddess is no other.",
      "The bindu is the secret of the three; in it the goddess rests.",
    ],
  },
  {
    pattern: /vajracchedik|diamond.?s[uū]tra/i,
    quotes: [
      "A bodhisattva should produce a mind that does not dwell anywhere.",
      "This is how to contemplate this fleeting world: a star at dawn, a bubble in a stream.",
      "Those who see me by form, who seek me by sound — they walk a false path.",
      "The Tathāgata cannot be seen by means of the possession of attributes.",
      "All composed things are like a dream, a phantom, a drop of dew, a flash of lightning.",
    ],
  },
  {
    pattern: /heart.?s[uū]tra/i,
    quotes: [
      "Form is emptiness; emptiness is form.",
      "Gone, gone, gone beyond, gone completely beyond — awakening, svāhā.",
      "No old age and death, and also no end of old age and death.",
      "All dharmas are marked by emptiness — not born, not destroyed, not stained, not pure.",
      "There is no suffering, no origination, no stopping, no path.",
    ],
  },
  {
    pattern: /dhammapada/i,
    quotes: [
      "Mind precedes all things; mind is their chief; they are mind-made.",
      "Better than a thousand hollow words is one word that brings peace.",
      "Hatred is never appeased by hatred; by non-hatred alone is it appeased.",
      "You yourself must strive. The Buddhas only point the way.",
      "Drop by drop is the water pot filled; likewise the sage fills himself with good.",
    ],
  },
  {
    pattern: /nagarjuna|n[aā]g[aā]rjuna|madhyamaka|mulamadhyamaka/i,
    quotes: [
      "Whatever is dependently arisen, that is explained to be emptiness.",
      "There is not the slightest difference between saṃsāra and nirvāṇa.",
      "I prostrate to the Perfect Buddha, the best of teachers, who taught that whatever is dependently arisen is unceasing, unborn.",
      "If nirvāṇa were something, it would be conditioned. If it were nothing, how could it be nirvāṇa?",
      "Emptiness wrongly grasped is like picking up a poisonous snake.",
    ],
  },
  {
    pattern: /shantideva|[sś][aā]ntideva|bodhicary/i,
    quotes: [
      "All the suffering in the world comes from seeking pleasure for oneself. All the happiness comes from seeking pleasure for others.",
      "Where would I find enough leather to cover the earth? But leather on the soles of my shoes is enough.",
      "If the problem can be solved, why worry? If it cannot be solved, worrying will do no good.",
      "As long as space remains, as long as sentient beings remain, may I too remain to dispel the miseries of the world.",
      "May I be a guard for those who are protectorless, a guide for those who journey on the road.",
    ],
  },
  {
    pattern: /d[oō]gen|shobogenzo|sh[oō]b[oō]genz[oō]/i,
    quotes: [
      "To study the Buddha Way is to study the self. To study the self is to forget the self.",
      "Time is not a line. The time of a pine is a pine; the time of a bamboo is a bamboo.",
      "If you cannot find the truth right where you are, where else do you expect to find it?",
      "A fish swims in the ocean, and no matter how far it swims, there is no end to the water.",
      "Enlightenment is like the moon reflected in water. The moon does not get wet, nor is the water broken.",
    ],
  },
  {
    pattern: /milarepa/i,
    quotes: [
      "The more I meditate, the more unmistakable the nature of mind becomes.",
      "In the gap between two thoughts, the innate face of mind is seen.",
      "When I look, I find nothing. When I rest, it is vividly present.",
      "Do not seek the Buddha elsewhere; he is the one who is looking.",
      "My religion is to live and die without regret.",
    ],
  },
  {
    pattern: /tilopa|maha.?mudra/i,
    quotes: [
      "Do not imagine, do not think, do not analyze, do not meditate, do not reflect — rest naturally.",
      "Like a river flowing into the ocean, let the mind rest in its own place.",
      "Mahāmudrā is not a thing to be attained; it is the nature of what is already looking.",
      "Cut the root of a tree and the branches wither. Cut the root of mind and all appearance is freed.",
      "Look at the mind; there is nothing to see. Seeing nothing, see its nature.",
    ],
  },
  {
    pattern: /tao.?te.?ching|dao.?de.?jing|lao.?tzu/i,
    quotes: [
      "The way that can be spoken is not the constant Way.",
      "The sage does nothing, yet nothing is left undone.",
      "Know the white, keep the black; be a pattern to the world.",
      "Heaven and earth are not kind; they treat the ten thousand things as straw dogs.",
      "Returning is the movement of the Way; yielding is its function.",
    ],
  },
  {
    pattern: /chuang|zhuang/i,
    quotes: [
      "Once I, Zhuang Zhou, dreamed I was a butterfly. Or was I a butterfly dreaming I was Zhuang Zhou?",
      "The perfect man uses his mind like a mirror — it grasps nothing, it refuses nothing.",
      "You cannot speak of ocean to a well-frog.",
      "Forget the years, forget distinctions. Leap into the boundless and make it your home.",
      "The torch of chaos and doubt — this is what the sage steers by.",
    ],
  },
  {
    pattern: /confucius|analect/i,
    quotes: [
      "The Master said: To learn and at due times to repeat what one has learnt, is that not after all a pleasure?",
      "Do not impose on others what you yourself do not desire.",
      "The junzi is not a utensil.",
      "When I walk along with two others, they may serve me as my teachers.",
      "Is it not a joy to have friends come from afar?",
    ],
  },
  {
    pattern: /zhongyong|doctrine of the mean/i,
    quotes: [
      "What Heaven confers is called the nature; accordance with this nature is called the Way.",
      "Equilibrium is the great root of the world; harmony is the universal path.",
      "Sincerity is the Way of Heaven; to become sincere is the Way of the human.",
      "The Way is not far from the human. If a person takes a way far from the human, it cannot be the Way.",
      "The junzi is watchful over himself when he is alone.",
    ],
  },
  {
    pattern: /heraclitus/i,
    quotes: [
      "You cannot step twice into the same river.",
      "The unseen harmony is stronger than the seen.",
      "Nature loves to hide.",
      "The way up and the way down are one and the same.",
      "Listening not to me but to the Logos, it is wise to agree that all things are one.",
    ],
  },
  {
    pattern: /parmenides/i,
    quotes: [
      "What is, is; what is not, is not.",
      "It is the same thing to think and to be.",
      "Being is ungenerated and imperishable, whole, unique, unmoved, and complete.",
      "Never shall this prevail: that things that are not, are.",
      "Look upon what is absent as if it were steadfastly present to the mind.",
    ],
  },
  {
    pattern: /epictetus/i,
    quotes: [
      "Some things are up to us, and some things are not up to us.",
      "It is not things that disturb us, but our judgments about things.",
      "Do not seek to have events happen as you wish, but wish them to happen as they do.",
      "If you want to improve, be content to be thought foolish and stupid.",
      "Make the best use of what is in your power, and take the rest as it happens.",
    ],
  },
  {
    pattern: /marcus|meditations/i,
    quotes: [
      "The universe is transformation; life is opinion.",
      "Waste no more time arguing what a good man should be. Be one.",
      "You have power over your mind — not outside events. Realize this, and you will find strength.",
      "What is not good for the hive is not good for the bee.",
      "Soon you will have forgotten all; soon all will have forgotten you.",
    ],
  },
  {
    pattern: /phaedo|plato/i,
    quotes: [
      "The one aim of those who practice philosophy in the proper manner is to practice for dying and death.",
      "Cebes, I believe that the soul is immortal and imperishable.",
      "We shall part from here as from a prison.",
      "If the soul is immortal, it requires our care not only for this time, but for all time.",
      "Crito, we owe a cock to Asclepius. Pay it and do not neglect it.",
    ],
  },
  {
    pattern: /plotinus|ennead/i,
    quotes: [
      "Never did the eye see the sun unless it had first become sunlike.",
      "Withdraw into yourself and look. If you do not find yourself beautiful yet, act as the creator of a statue.",
      "The One is all things and no one of them.",
      "We are always around it, but we do not always look.",
      "Cut away everything.",
    ],
  },
  {
    pattern: /eckhart/i,
    quotes: [
      "The eye with which I see God is the same eye with which God sees me.",
      "Detachment is the best of all, for it makes us one with God.",
      "God is a word, an unspoken word.",
      "The just man serves neither God nor creatures, for he is free.",
      "The shell must be cracked apart if what is in it is to come out.",
    ],
  },
  {
    pattern: /dionysius|areopagite|mystical.?theology|divine.?names/i,
    quotes: [
      "Leave behind the senses and the operations of the intellect; leave behind all things, and stretch toward union with the unknown.",
      "The cause of all is itself no one of all.",
      "Into the dark beyond all light, we pass, unseeing and unknowing.",
      "It is not soul or mind, nor number or order, nor greatness or smallness.",
      "The higher we soar, the more our words are confined to the ideas we are contemplating.",
    ],
  },
  {
    pattern: /cloud.?of.?unknowing/i,
    quotes: [
      "Beat upon that thick cloud of unknowing with a sharp dart of longing love.",
      "By love He may be gotten and holden; but by thought never.",
      "Look that nothing live in thy working mind but a naked intent stretching unto God.",
      "Humble prayer continues to pierce the cloud; thought cannot.",
      "God may well be loved, but not thought.",
    ],
  },
  {
    pattern: /gospel.?of.?thomas/i,
    quotes: [
      "The kingdom is inside you, and it is outside you.",
      "Split a piece of wood; I am there. Lift the stone, and you will find me there.",
      "If you bring forth what is within you, what you bring forth will save you.",
      "The one who seeks should not stop until they find. When they find, they will be disturbed.",
      "Jesus said: Become passers-by.",
    ],
  },
  {
    pattern: /course in miracles|acim/i,
    quotes: [
      "Nothing real can be threatened. Nothing unreal exists. Herein lies the peace of God.",
      "I am not a body. I am free. For I am still as God created me.",
      "Forgiveness is the key to happiness.",
      "Teach only love, for that is what you are.",
      "You who want peace can find it only by complete forgiveness.",
    ],
  },
  {
    pattern: /ecclesiastes|qoheleth/i,
    quotes: [
      "Vanity of vanities, says Qoheleth; vanity of vanities, all is vanity.",
      "To every thing there is a season, and a time to every purpose under heaven.",
      "The race is not to the swift, nor the battle to the strong.",
      "Fear God, and keep his commandments: for this is the whole of the human.",
      "The dust returns to the earth as it was, and the spirit returns to God who gave it.",
    ],
  },
  {
    pattern: /ibn|arabi|balyani|know yourself/i,
    quotes: [
      "He who knows himself knows his Lord.",
      "There is nothing in existence but God.",
      "You are not you; you are He, without you.",
      "The world is imagination within imagination — and the Real is the one who imagines.",
      "The Real is the mirror; you are the form that appears in it.",
    ],
  },
  {
    pattern: /rumi|r[uū]m[iī]|mathnawi|mathnaw[iī]/i,
    quotes: [
      "The wound is the place where the Light enters you.",
      "You were born with wings. Why prefer to crawl through life?",
      "Silence is the language of God; all else is poor translation.",
      "Don't get lost in your pain; know that one day your pain will become your cure.",
      "Try to appear as you are, or be as you appear.",
    ],
  },
  {
    pattern: /eastman|soul of the indian|ohiyesa/i,
    quotes: [
      "The native soul was not a wanderer; it was at home in the Great Mystery.",
      "Silence is the cornerstone of character.",
      "In the life of the Indian there was only one inevitable duty — the duty of prayer.",
      "The first American mingled with his pride a singular humility.",
      "It was not a religion of one day, but of every day, of every act.",
    ],
  },
  {
    pattern: /zitkala|old indian legends/i,
    quotes: [
      "Iktomi, the avaricious, is a spider still.",
      "The old legends were not told to fill an hour, but to shape a people.",
      "Under the listening stars the stories walked again.",
      "What the firelight knows, the page can only borrow.",
      "Iktomi is always hungry, always clever, and always caught in his own web.",
    ],
  },
  {
    pattern: /johnson|yoruba.?faith|yoruba.?religion/i,
    quotes: [
      "Olódùmarè is the origin of all that is, and of all that will be.",
      "The òrìṣà are not rivals of the One; they are faces of the One in the world.",
      "Character is the shining of a person; without it, ritual is empty.",
      "Ifá does not speak to flatter; Ifá speaks so that the path may be walked.",
      "The Yoruba say that character is the finest beauty of a person.",
    ],
  },
  {
    pattern: /yoruba|[oò]we/i,
    quotes: [
      "The world is a marketplace; heaven is home.",
      "Slowly, slowly the pepper becomes ripe.",
      "The river that forgets its source will dry up.",
      "What an elder sees while seated, a child cannot see even from the top of a tree.",
      "When the drumbeat changes, the dance must change also.",
    ],
  },
  {
    pattern: /kabbalah|zohar|yetzirah|sephiroth|sefirot/i,
    quotes: [
      "Ten sefirot of nothingness, twenty-two foundation letters.",
      "The Infinite is not a thing among things; it is that from which things arise.",
      "As above, so below — the tree is one.",
      "He engraved and carved and created His world in thirty-two mysterious paths of wisdom.",
      "Before the emanations were emanated, there was only the Infinite.",
    ],
  },
];

export const HERO_QUOTE_DWELL_MS = 18_000;

function uniqueLines(lines: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const raw of lines) {
    const line = raw.replace(/\s+/g, " ").trim();
    if (line.length < 24 || line.length > 160) continue;
    const key = line.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(line);
  }
  return out;
}

/** Curated lines for a collection, else a short fallback list from the catalog. */
export function heroQuotesFor(collection: string, fallback: string[] = []): string[] {
  const raw = (collection || "").trim();
  if (!raw || raw.toLowerCase() === "all") return [];
  for (const row of HERO_QUOTES) {
    if (row.pattern.test(raw)) return row.quotes;
  }
  return uniqueLines(fallback).slice(0, 5);
}

/** First sentences from catalog translations, filtered to mandala length. */
export function catalogQuoteCandidates(lines: string[]): string[] {
  return uniqueLines(lines).slice(0, 5);
}

/** Next index in a random walk — never the line already showing. */
export function nextHeroQuoteIndex(current: number, length: number): number {
  if (length < 2) return 0;
  const step = Math.floor(Math.random() * (length - 1));
  return step >= current ? step + 1 : step;
}
