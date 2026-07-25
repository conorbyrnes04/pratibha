/** Small tradition glyphs for collection filters (works in web + mobile). */

function normalizeKey(name: string): string {
  return name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}

const ICON_RULES: Array<{ pattern: RegExp; icon: string }> = [
  // Daoist corpus — Lao Tzu (Tao Te Ching) and Zhuangzi share one marker
  { pattern: /tao|te.?ching|tao_te_ching|zhuang|chuang|lao.?tzu|chuang_tzu/i, icon: "道" },
  { pattern: /bhagavad|gita/i, icon: "गी" },
  { pattern: /epictetus/i, icon: "ε" },
  { pattern: /phaedo|plato/i, icon: "Π" },
  { pattern: /plotinus|ennead/i, icon: "∞" },
  { pattern: /milarepa|jetsun.?kahbum|tibet.?s.?great.?yogi/i, icon: "ཨ" },
  // Vajrayāna / Buddhist emptiness voices
  { pattern: /tilopa|maha.?mudra|ganges.?mahamudra/i, icon: "ཏི" },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, icon: "प्र" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk/i, icon: "मा" },
  { pattern: /shantideva|śāntideva|bodhicary/i, icon: "बो" },
  { pattern: /chandogya|khandogya|khândogya/i, icon: "छ" },
  { pattern: /upanishad|isavasya|svetasvatara|mandukya/i, icon: "ॐ" },
  // Kashmir Śaiva / Tantra — Yoginīhṛdaya, Vijñāna Bhairava, Spanda, etc.
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|yogini_hrdaya|pratyabhij/i, icon: "श" },
  { pattern: /heraclitus|fragment/i, icon: "λ" },
  { pattern: /parmenides/i, icon: "ἐ" },
  { pattern: /dhammapada|dhammapāda/i, icon: "ध" },
  { pattern: /cloud.?of.?unknowing/i, icon: "◌" },
  // Patañjali Yoga Sūtras — puruṣa–prakṛti duality (Sāṃkhya epistemology)
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, icon: "◐" },
  { pattern: /ibn|arabi|know yourself/i, icon: "◈" },
  { pattern: /confucius|analect/i, icon: "儒" },
  { pattern: /marcus|meditation/i, icon: "◎" },
  { pattern: /rumi|poet/i, icon: "۞" },
  // Dōgen — Zen emptiness / śūnyatā register (distinct from Daoist 道)
  { pattern: /dogen|dōgen|shobogenzo|shōbōgenzō/i, icon: "空" },
  // Meister Eckhart — Christian mysticism (parallel register to Ibn Arabi ◈)
  { pattern: /eckhart|meister_eckhart|abegescheidenheit|abgeschiedenheit/i, icon: "☩" },
  // Pseudo-Dionysius — apophatic theology
  { pattern: /dionysius|areopagite|mystical.?theology|divine.?names|pseudo_dionysius/i, icon: "✦" },
];

export function collectionIcon(name?: string): string {
  const raw = (name || "").trim();
  if (!raw || raw.toLowerCase() === "all") return "✦";
  const key = normalizeKey(raw);
  for (const rule of ICON_RULES) {
    if (rule.pattern.test(raw) || rule.pattern.test(key)) return rule.icon;
  }
  return "✦";
}
