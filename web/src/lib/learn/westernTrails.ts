import type { LearningTrack } from "../learningPaths";

/** Off-spine walks for Christian mysticism, Stoicism, and Sufi. */
export const WESTERN_TRAILS: LearningTrack[] = [
  {
    id: "divine-darkness",
    title: "The Divine Darkness",
    level: "Intermediate",
    focus: "Christian mysticism: unknowing as the highest knowing",
    outcome:
      "Stop treating God as an object in the light; leave the thinkable; let detachment make room rather than adding a holier self.",
    description:
      "An eight-gate walk through Dionysius, the Cloud of Unknowing, and Eckhart.",
    arc:
      "We begin where Dionysius begins: the mysteries are veiled in a darkness that is too bright for a mind that still wants to see. Timothy is told to leave sense and intellect. Moses reaches lights and still only sees the place — then plunges into unknowing. Affirmation descends through names; negation strips upward. The Cloud makes that method a day's work: leave what you can think, and let 'I do not know' be the intent. Eckhart names the inner condition the darkness was for — detachment as the one necessary thing, then the poverty that wills, knows, and has nothing, so God is not a possession.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "pd-dazzling-darkness",
        title: "The darkness that is too bright",
        orientation:
          "Before any method of prayer, the light-metaphor has to break. Dionysius will not let you climb toward a visible God.",
        teaching:
          "The Trinity is addressed as beyond essence, beyond divinity, beyond goodness. The summit of the mystical oracles is veiled in a super-luminous darkness of a silence that teaches secrets. The most obscure makes super-manifest what is most radiant; the intangible super-fills eyeless minds. This is not absence. It is excess. If you are still trying to see God as an object in the light, you are already looking the wrong way. The first work is to notice the hunger for a picture — and to let the picture fail without calling the failure a lack of faith.",
        keyIdea: "The brightest thing looks dark to a mind that still wants to see. Darkness here is surplus, not deficit.",
        misconception:
          "That divine darkness means God is missing, or that mysticism begins by imagining a nicer light.",
        passageId: "pseudo_dionysius.pd_001",
        supportingPassageIds: ["pseudo_dionysius.pd_mt_08"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Help me hear dazzling darkness as excess of light, not as God's absence. Where am I still trying to see God as an object?",
        practice:
          "Sit three minutes without manufacturing an image of God. When one appears, let it go. Remain with the not-seeing. Do not improve it into a better image.",
        journalPrompt:
          "Where am I still trying to see God as an object in the light?",
        integration:
          "Not-seeing can be a kind of fullness, not a failure of prayer.",
      },
      {
        id: "pd-leave-intellect",
        title: "Leave the senses and the intellect",
        orientation:
          "The darkness is not a mood you wait for. Timothy is given an act: strip.",
        teaching:
          "Abandon sense-perceptions and intellectual operations, all sensible and intelligible things, beings and non-beings. Be raised unknowingly, as far as possible, toward union with what is beyond all being and knowledge. By unconstrained ecstasy from yourself and all things — having stripped away all and been released from all — you are led to the super-essential ray of the divine darkness. Union is not a finer concept stacked on the last one. People stall here by collecting better thoughts about the unsayable. The instruction is to leave the stack.",
        keyIdea: "Union is a stripping, not a better idea of God.",
        misconception:
          "That approaching God means thinking more carefully, or that leaving the intellect means becoming stupid.",
        passageId: "pseudo_dionysius.pd_mt_02",
        supportingPassageIds: ["pseudo_dionysius.pd_001"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Show me the difference between stacking finer thoughts about God and laying the mind to rest. What does 'leave the intellect' ask me to do today?",
        practice:
          "For one sitting, do not add a thought about God. When a thought arrives, name it intellect and set it down. Stay with the leaving. If you start composing a report of how well you left, that is another thought — set it down too.",
        journalPrompt:
          "What am I still stacking — finer thoughts about the unsayable?",
        integration:
          "You can tell stacking ideas from laying the mind to rest.",
      },
      {
        id: "pd-moses-cloud",
        title: "Moses enters the cloud",
        orientation:
          "Even the high experiences are still a place. The encounter is past them.",
        teaching:
          "Moses is purified, hears trumpets, sees many lights — and still does not meet God. He beholds not Him (for He is invisible) but the place where He dwells. The highest of things seen or thought are still symbolic language of what is subordinate to the One who transcends them. Then he plunges into the darkness of unknowing, renounces all the apprehensions of understanding, and by knowing nothing knows beyond mind. If you treat a confirmation, a vision, a settled mood as arrival, you have stopped at the place. The cloud is after the lights.",
        keyIdea: "The visions were still a place, not the encounter. Unknowing begins when even those are left.",
        misconception:
          "That a powerful spiritual experience is the meeting, or that plunging into darkness means despair.",
        passageId: "pseudo_dionysius.pd_mt_03",
        supportingPassageIds: ["pseudo_dionysius.pd_mt_02"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Help me tell the place where God dwells from God. Which of my 'lights' am I treating as arrival?",
        practice:
          "Name one spiritual light you treat as arrival — an insight, a mood, a confirmation. Step past it. Sit five minutes in the unnamed remainder without asking it to turn into a better light.",
        journalPrompt:
          "Have I mistaken the place where God dwells for God?",
        integration:
          "A good experience can be a place God left, not God.",
      },
      {
        id: "pd-negation-ascends",
        title: "Affirmation descends; negation ascends",
        orientation:
          "Now the method is stated as a direction of travel, not as a mood of mystery.",
        teaching:
          "Hymn the negations in the opposite manner from the affirmations. Affirmations begin from the most primary names and descend through the intermediate to the last things. Negations begin from the last things and strip upward toward the most primary, so that you may know nakedly that unknowing which is veiled by all knowable things in all beings, and see that super-essential darkness hidden by all the light that is in beings. Naming God is not climbing. Naming goes down. Stripping goes up. If you only collect names, you are decorating the descent and calling it a path.",
        keyIdea: "Names go down. Stripping goes up. The summit is what remains when both have been said.",
        misconception:
          "That more names for God get you closer, or that negation is contempt for the world.",
        passageId: "pseudo_dionysius.pd_mt_05",
        supportingPassageIds: ["pseudo_dionysius.pd_mt_08"],
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Walk me through one name I use for God: affirm it, then negate it. What is left, and how is that not nihilism?",
        practice:
          "Take one name you use for God. Affirm it once, slowly. Then negate it once. Sit with what is left when both have been said. Do not rush to a third name to fill the gap.",
        journalPrompt:
          "When I name God, am I climbing or decorating?",
        integration:
          "You can use a name without letting it be the summit.",
      },
      {
        id: "cloud-leave-thinkable",
        title: "Leave what you can think",
        orientation:
          "The Cloud turns Dionysius's method into a day's work: a chosen ignorance, not a failure of study.",
        teaching:
          "Of creatures and their works — yes, and of the works of God himself — you may through grace have fullness of knowing, and think well on them. Of God himself no one can think. Therefore leave all that you can think, and choose for your love that which you cannot think. The cut is not against knowledge of the world. It is against using the thinkable as a ladder to God. Love chooses what thought cannot hold. If you skip this, unknowing stays a Dionysian metaphor and never becomes an act.",
        keyIdea: "Leave the thinkable. Love what thought cannot hold.",
        misconception:
          "That this is anti-intellectual, or that you must stop thinking about the world in order to love God.",
        passageId: "the_cloud_of_unknowing.cloud_01",
        supportingPassageIds: ["pseudo_dionysius.pd_mt_02"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me leave what I can think without despising thought. What thinkable thing am I using as a ladder?",
        practice:
          "For ten minutes, let the mind have the world — tasks, creatures, even holy works. Then leave them. Rest one minute with what you cannot think. When a concept of God returns, it is thinkable: leave it too.",
        journalPrompt:
          "What thinkable thing am I still using as a ladder to God?",
        integration:
          "You can love without a thought-object to hold.",
      },
      {
        id: "cloud-i-do-not-know",
        title: "I do not know",
        orientation:
          "The method is enacted, not explained. The honest answer is the cloud.",
        teaching:
          "How shall I think on him, and what is he? The teacher answers: I do not know. You have brought me with your question into that same darkness, that same cloud of unknowing, that I wish you were in. Naked intent stretches toward God without a picture. The question is not a problem to solve. It is already the place. If you fill 'I do not know' with theology to spare yourself embarrassment, you have left the cloud for a classroom.",
        keyIdea: "The honest 'I do not know' is the work — not the failure before the work.",
        misconception:
          "That unknowing is a gap to be filled with better doctrine, or that it means you have no love.",
        passageId: "the_cloud_of_unknowing.cloud_03",
        supportingPassageIds: ["the_cloud_of_unknowing.cloud_01"],
        theme: "practice",
        chatMode: "question",
        chatPrompt:
          "Stay with me in 'I do not know' without letting it become a pose or a doctrine. What wants to fill the gap?",
        practice:
          "Ask the question once: how shall I think on him, and what is he? Answer only: I do not know. Stay there for twenty breaths without filling the gap with theology. If a sentence arrives, let it pass. Return to not knowing.",
        journalPrompt:
          "Can I let 'I do not know' be the work, not the failure?",
        integration:
          "Unknowing can be an intent, not an embarrassment.",
      },
      {
        id: "eck-detachment",
        title: "The one necessary thing",
        orientation:
          "Eckhart names the inner condition the darkness was for: not a busier holiness, but room.",
        teaching:
          "Every virtue still looks somehow toward creatures. Pure detachment stands free of all creatures. That is why the Lord said to Martha: one thing is necessary. Whoever would be untroubled and pure must have that one thing — detachment — not a more impressive catalogue of excellences. Love, humility, service can still be ways of watching yourself be good. Detachment is not a medal among medals. It is the emptying of the field so God is not competing with a spiritual self-portrait.",
        keyIdea: "Detachment is the field, not a virtue-image. The one necessary thing is the emptying.",
        misconception:
          "That detachment means coldness, or that the highest life is a busier, holier personality.",
        passageId: "meister_eckhart.eck_001",
        supportingPassageIds: ["the_cloud_of_unknowing.cloud_03"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Where am I still using a virtue to look toward creatures — including a spiritual self? What would dropping the portrait look like today?",
        practice:
          "Drop one spiritual self-portrait for the rest of the day — the helpful one, the devout one, the one who is doing well. Do the next ordinary act without it. If you catch yourself checking whether you look detached, that is the portrait returning.",
        journalPrompt:
          "Which virtue am I still using to look toward creatures — including a spiritual self?",
        integration:
          "You can act without a virtue-image watching you act.",
      },
      {
        id: "eck-poverty",
        title: "Wills nothing, knows nothing, has nothing",
        orientation:
          "The path ends not in a richer interior but in poverty that makes room.",
        teaching:
          "That person is poor who wills nothing, knows nothing, and has nothing. This is not anti-thought and not material theatre. To will nothing is to stop using God as a project of yours. To know nothing is to release possessive, image-bound knowing — including 'I have God.' To have nothing is to stand without private spiritual capital: insight, streak, consolation, status. Even the desire to fulfill God's will can remain self-willed if it is held as mine. Poverty is room. Possession is the blockage. The last gate is whether you can be without a store.",
        keyIdea: "Poverty is room for God. Possession — even of holiness — is the blockage.",
        misconception:
          "That spiritual poverty means thinking less of yourself as a personality, or that it is contempt for knowledge.",
        passageId: "meister_eckhart.eck_010",
        supportingPassageIds: ["meister_eckhart.eck_001"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "What spiritual capital am I still defending as mine? Help me set it down without turning poverty into a new identity.",
        practice:
          "Name one thing you have spiritually — an insight, a practice-streak, a consolation. Set it down as not yours. Sit empty for five minutes. Then do the next task without picking it back up as identity.",
        journalPrompt:
          "What spiritual capital am I still defending as mine?",
        integration:
          "You can be without a private store of God.",
      },
    ],
  },
  {
    id: "the-living-saying",
    title: "The Living Saying",
    level: "Intermediate",
    focus: "Christian sayings: the kingdom is not a spectacle; worth is not conferred by the circle",
    outcome:
      "Refuse the calendar and the extra law; keep an unsplit eye; let Desire keep the garment; abide as a branch; stop the circle from conferring worth; want oneness as indwelling, not agreement.",
    description:
      "Nine living sayings from Luke, Thomas, Mary, and John — after the darkness, a mouth.",
    arc:
      "We begin where the Pharisees begin: when is the kingdom coming? Luke refuses observation. Thomas doubles the location — inside and outside — and Mary names the Human One within, then forbids a second Moses. The eye must be single or more lamps will not help; Mary's treasure follows the mind that does not waver. Desire claims the soul and is answered: you saw a garment. The branch does not fruit from itself. Levi tells Peter that worth is the Savior's to confer. John prays the later ones — including the reader — into the same one.",
    estimatedSessions: "9 gates · ~20 min each",
    steps: [
      {
        id: "ls-not-with-observation",
        title: "Not with observation",
        orientation:
          "The first error is a calendar. If you skip this, later sayings become holy sites and timetables.",
        teaching:
          "The question wants a date. He refuses a spectacle you could point at. Observation is the watcher's stance: waiting for a sign so you do not have to enter. Entos hymōn can mean among you or within you — the Greek will not close the case. What it does close is the pointing-away. If you are still asking when, you have already mislocated it. The kingdom will not perform for inspection.",
        keyIdea: "The kingdom does not come with observation. Asking when is already looking the wrong way.",
        misconception:
          "That the kingdom is an event on the horizon, or that watching for signs is a form of faith.",
        passageId: "new_testament_logia.ntl_01",
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Help me hear Luke 17 as a refusal of the spectator's stance, not as a slogan about an inner feeling. Where am I still asking when?",
        practice:
          "Catch one 'when will it come' today — a mood, a news cycle, a spiritual timetable. Drop the when. Look once at what is already within reach, and stay there for ten breaths.",
        journalPrompt:
          "What am I still watching for so I do not have to enter?",
        integration:
          "You can tell postponement-by-watching from presence, and drop one when.",
      },
      {
        id: "ls-inside-and-outside",
        title: "Inside you and outside you",
        orientation:
          "Luke left entos open. Thomas will not let you pick only a cave or only a destination.",
        teaching:
          "If those who lead you say the kingdom is in the sky, the birds will precede you. If in the sea, the fish. The joke is geography as religious direction. The kingdom is inside you and outside you. Self-knowledge here is relational: when you know yourselves you will be known, children of the living Father. Poverty is not empty pockets. It is existing as the not-knowing of that belonging. Do not hear 'within' as a license to ignore the person in front of you, or 'outside' as a pilgrimage that never comes home.",
        keyIdea: "The kingdom is inside you and outside you. Leaders who point to sky or sea mislead.",
        misconception:
          "That the kingdom is a private inner state, or a location you travel to under better guidance.",
        passageId: "gospel_of_thomas.faithful_thom_003",
        supportingPassageIds: ["new_testament_logia.ntl_01"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Show me how inside-and-outside is one location, not two programs. Whom do I still let point me to a sky or a sea?",
        practice:
          "For ten minutes notice one breath, one sound beyond you, one person or creature before you. After each, silently: within and outside. End by naming one act today from belonging rather than lack.",
        journalPrompt:
          "Whom do I still let point me to a sky or a sea?",
        integration:
          "You can refuse a pointed-to elsewhere without collapsing into private spirituality.",
      },
      {
        id: "ls-no-second-moses",
        title: "No second Moses",
        orientation:
          "The Human One is within. The danger is the extra statute that follows a finding.",
        teaching:
          "Peace is to be acquired, not waited for as a mood. Do not be misled by Look over here. The Son of Humanity exists within you — follow is not travel. Then the second blow: do not lay down rules beyond what was given, nor make a law like the lawgiver, lest you be bound by it. A gospel that starts as inner finding can harden, in a week, into a new Moses. Mary will later be accused of inventing teaching. This saying is why: the extra law was already forbidden.",
        keyIdea: "The Human One exists within you. Do not become a second Moses to prove you found him.",
        misconception:
          "That following means going somewhere, or that a new rule is how you protect an inner gospel.",
        passageId: "gospel_of_mary.gom_04",
        supportingPassageIds: ["gospel_of_thomas.faithful_thom_003"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me return to the Human One within without adding a rule to prove I returned. What extra statute am I tempted to lay down?",
        practice:
          "Catch one spiritual 'look over there' — a teacher, a sign, a mood. Return to the Human One as within. Do not add a rule to prove you returned.",
        journalPrompt:
          "What extra rule am I laying down to prove I have found him within?",
        integration:
          "You can return without legislating the return for yourself or anyone else.",
      },
      {
        id: "ls-unsplit-eye",
        title: "The unsplit eye",
        orientation:
          "Location is not enough. The organ of seeing can still be double.",
        teaching:
          "Haplous means single, simple, unmixed — not healthy as a medical compliment. The eye is the body's lamp: attention lights the whole field. An evil eye is the divided, stingy, appraising glance. If the organ of seeing is already dark, more information will not help; the light in you has become darkness, and that is the great dark. You do not need more lamps. You need an unsplit eye.",
        keyIdea: "If the eye is split, more lights will not help. The lamp is the looking.",
        misconception:
          "That you need more teaching, more practices, more lamps — rather than an unsplit eye.",
        passageId: "new_testament_logia.ntl_05",
        supportingPassageIds: ["gospel_of_thomas.faithful_thom_022"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me feel the second glance — comparing, acquiring — as the evil eye, not as intelligence. What would one looking be today?",
        practice:
          "For five minutes look at one thing — a face, a page, a tree — without the second glance that compares or acquires. When the eye splits, name it and return.",
        journalPrompt:
          "Where is my glance already appraising, comparing, acquiring?",
        integration:
          "You can feel the second glance arrive, and come back to one looking.",
      },
      {
        id: "ls-where-the-mind-is",
        title: "Where the mind is",
        orientation:
          "Peter contains Mary's privilege. She relocates treasure from relic and college to unwavering mind.",
        teaching:
          "Peter admits a privilege and immediately contains it: more than the rest of the women. Mary does not debate the containment. She offers what is hidden. Blessedness is not seeing — it is not wavering at the seeing. Where the mind is, there is the treasure. Not where the relic is. Not where the male college is. If the mind wavers, the Lord is a spectacle. If it holds, the vision is a location of wealth.",
        keyIdea: "Where the mind is, there is the treasure. Wavering turns the Lord into a souvenir.",
        misconception:
          "That treasure is a relic, a circle, or a collected vision — rather than unwavering nous.",
        passageId: "gospel_of_mary.gom_06",
        supportingPassageIds: ["new_testament_logia.ntl_05"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Help me hear Mary's treasure as a location of attention, not as a secret the men lacked. Where do I waver and start collecting?",
        practice:
          "When a true thing appears today — a person, a sentence, a silence — notice the waver. Hold the mind there for ten breaths. Do not collect the experience as status.",
        journalPrompt:
          "Do I treat the Lord as a spectacle to collect, or as a place the mind can hold?",
        integration:
          "You can hold a true appearing without turning it into a possession or a rank.",
      },
      {
        id: "ls-i-was-a-garment",
        title: "I was a garment",
        orientation:
          "Unwavering mind still meets the power that claims you because it saw you go up.",
        teaching:
          "Desire claims ownership: you came up through me, so you are mine. The soul answers: I saw you; you did not see me. I was to you a garment. Belonging was a costume-error. Recognition is one-way, and that is enough to leave rejoicing. This is not a campaign against wanting. It is the end of being identified with the heat that mistook a dress for a person.",
        keyIdea: "Desire never knew the wearer. It knew a garment, and called that you.",
        misconception:
          "That this saying is prudery about desire, or that arguing with Desire is how you get free.",
        passageId: "gospel_of_mary.gom_08",
        supportingPassageIds: ["gospel_of_thomas.faithful_thom_037"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Help me answer Desire without a debate. What garment is being mistaken for me today?",
        practice:
          "Name one desire that talks as if you belong to it. Answer, silently: you saw a garment. Walk to the next task without arguing with it.",
        journalPrompt:
          "Which desire is talking as if I belong to it?",
        integration:
          "You can move to the next act without negotiating with a claim that only knew the costume.",
      },
      {
        id: "ls-abide-in-the-vine",
        title: "Abide in the vine",
        orientation:
          "After leaving Desire's claim, fruit can still be attempted as a solo project.",
        teaching:
          "Fruit is not a project of the branch. Apart from me you can do nothing — not less. The I am is the vine; you are already a branch, which is why the command is abide, not become. Effort may be real. Detached from remaining, it is a branch displaying grapes it does not have. Do not hear this as passivity. Hear it as the condition under which an act is not a display.",
        keyIdea: "You are already a branch. The command is remain, not become. Apart from the vine you can do nothing.",
        misconception:
          "That spiritual fruit is produced by effort detached from remaining, or that abiding means not acting.",
        passageId: "new_testament_logia.ntl_26",
        supportingPassageIds: ["new_testament_logia.ntl_25"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Show me the difference between remaining and passivity. Where am I muscling fruit as if the stem were optional?",
        practice:
          "Before one task you usually muscle through, abide for sixty seconds — not as a trick to succeed, as the vine-condition. Then do the task. If it bears, do not take it as the branch's genius.",
        journalPrompt:
          "Where am I muscling fruit as if the stem were optional?",
        integration:
          "You can do one real task from remaining, without awarding the grapes to yourself.",
      },
      {
        id: "ls-if-he-made-her-worthy",
        title: "If he made her worthy",
        orientation:
          "The social cost of the whole walk: Peter becomes the extra law. Levi will not let the circle confer worth.",
        teaching:
          "Peter has become the adversary-power: angry, debating the woman, laying down who may hear. Worth is the Savior's to confer, not Peter's to revoke. Levi restates the love without 'than the rest of the women.' Then the clothing: perfect Humanity. Preach, and do not add a rule. The book ends not with a vision but with a group that can walk out because someone defended the witness. The circle does not confer worth. It can only refuse to revoke it.",
        keyIdea: "If the Savior made her worthy, who are you to reject her? The circle does not confer worth.",
        misconception:
          "That the community decides who may have heard, or that defending a witness requires a new rule.",
        passageId: "gospel_of_mary.gom_12",
        supportingPassageIds: ["gospel_of_mary.gom_04"],
        theme: "compassion",
        chatMode: "explain",
        chatPrompt:
          "Help me hear Levi without turning it into a faction. Where am I the gatekeeper of who may have heard?",
        practice:
          "Where you are the gatekeeper of who may have heard, step aside once. Clothe yourself as Human — do the next ordinary act without the extra rule.",
        journalPrompt:
          "Where am I the gatekeeper of who may have heard?",
        integration:
          "You can let someone else's hearing stand without your permission.",
      },
      {
        id: "ls-that-they-may-be-one",
        title: "That they may be one",
        orientation:
          "The last saying overshoots the room. The later reader is already inside the asking.",
        teaching:
          "He does not ask for these only, but also for those who believe through their word — including you. Oneness is not a team-building goal. It is as you, Father, in me and I in you, and then they in us. Glory is given onward so they may be one as we are one. Perfected into one: completion as union, not as polish. The world's belief is the public fruit of this nesting, not a campaign. Unity here is indwelling, given, so that the world may know love — not agreement.",
        keyIdea: "Oneness is indwelling, patterned on Father-in-Son — not agreement, not a side taking the other.",
        misconception:
          "That Christian unity is agreement, or that the prayer is for them to come over to your side.",
        passageId: "new_testament_logia.ntl_27",
        supportingPassageIds: ["gospel_of_mary.gom_12"],
        theme: "compassion",
        chatMode: "practice",
        chatPrompt:
          "Help me pray that we may be one as they are one, without smuggling in a demand that they convert to my position.",
        practice:
          "Toward one person you split from, ask this much: that we may be one as they are one — not that they come over to your side. Do one repair that matches the prayer.",
        journalPrompt:
          "Am I asking that they come over to my side, or that we be one as they are one?",
        integration:
          "You can want oneness without requiring conversion to your position.",
      },
    ],
  },
  {
    id: "before-the-face",
    title: "Before the Face",
    level: "Intermediate",
    focus: "Tehillim: speak to the Face; thirst, drop, weaned quiet",
    outcome:
      "Speak under the night without turning wonder into anthropology; hear sky and teaching as one light; address You in the valley; pray thirsty; slack the grip before claiming knowledge; cling in a dry land without despising the body; lodge in trouble without a charm; sit weaned; stop demanding a room outside the Face.",
    description:
      "Nine psalms as address — cataphatic speech after darkness and the living saying.",
    arc:
      "After unknowing and the sayings, a mouth remains that must speak to Someone. We begin under the night: what is a human that you remember. Psalm 19 sews two luminaries: a tent for the sun, then Torah that restores a particular soul. The shepherd's You happens in the valley, not after exemption. Thirst is theology; deep calls to deep. Harpu: drop, and know. Clinging in a dry land ranks loyalty above the outcome. The secret place is lodging in trouble, not a force field. A weaned child sits. There is nowhere to flee from the Face.",
    estimatedSessions: "9 gates · ~20 min each",
    steps: [
      {
        id: "ps-what-is-a-human",
        title: "What is a human that you remember",
        orientation:
          "Before two suns or a valley, stand under the night. If you skip the gasp, later praise is a performance.",
        teaching:
          "The psalm is a gasp that refuses two exits: humility-as-self-hatred, and dominion-as-license. Under the night you shrink: what is a human that you remember. Memory here is not nostalgia. It is the scandal that infinite attention would bother with this brief animal. Then the turn without apology: a little less than elohim, crowned, given the works. You do not earn the crown by forgetting you are dust, and you do not honor the dust by pretending the night is empty. Infants who found strength are the epistemology: praise is not the mature correction of wonder. It is wonder that still has milk on its mouth.",
        keyIdea: "Smallness and entrusted work are the same vision. Speak from under the night.",
        misconception:
          "That scale-wonder is self-hatred, or that the crown is license to own the works.",
        passageId: "psalms_tehillim.psalm_008",
        supportingPassageIds: ["psalms_tehillim.psalm_090"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Address the Face with me; do not lecture about God in the third person. Help me hear this gasp under the night as speech, not as anthropology. Where am I still turning wonder into a theory of myself?",
        practice:
          "Stand at a window or under actual sky. Speak the gasp aloud once — what is a human that you remember — without improving it into a theory. Then do one entrusted act with what is already in your hands, as someone crowned who is still dust.",
        journalPrompt:
          "Where am I still turning wonder into a theory of myself?",
        integration:
          "You can feel smallness and entrusted work as one vision, not as a mood swing.",
      },
      {
        id: "ps-tent-for-the-sun",
        title: "A tent for the sun",
        orientation:
          "Two luminaries sewn into one lyric. Skip the seam and you get sky-religion or book-religion.",
        teaching:
          "The heavens recount glory with no speech. In that wordless telling God pitches a tent for the sun: bridegroom, runner, heat from which nothing hides. Then, without apology, a second sun: the teaching of YHWH complete, turning the life-breath back, lighting particular eyes. Torah does what the sky cannot. Gold and honey name desire, not decoration. The same light that circuits the heavens wants the inner wanderings cleansed. The last petition is the murmur of the heart coming before the Face as the sky already does. Rock and kinsman — not a distant artisan of suns.",
        keyIdea: "Hear both sermons. Do not choose a religion of sky or a religion of statute.",
        misconception:
          "That Psalm 19 is two poems glued together, or that Torah is an optional second luminary you could skip.",
        passageId: "psalms_tehillim.psalm_019",
        supportingPassageIds: ["psalms_tehillim.psalm_036"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Model both sermons as one light. Do not let me split cosmos from commandment. Which sermon am I still treating as optional — the sky, or the teaching?",
        practice:
          "Hear one wordless testimony today — heat, bird, sky — for one minute without making a sentence of it. Then perform one commandment-sized act the same day: a truth told, a repair made, a wandering named before the Face.",
        journalPrompt:
          "Which sermon am I still treating as optional — the sky, or the teaching?",
        integration:
          "You can receive the sky and the teaching as one light, not as two optional faiths.",
      },
      {
        id: "ps-you-are-with-me",
        title: "You are with me",
        orientation:
          "After two suns, enter a body that lacks. Shepherding is accompaniment, not exemption.",
        teaching:
          "The first verb is not I follow. It is I do not lack. Shepherding is provision so complete that craving loses its job. The turn from he to you happens in the valley: theology becomes address when the shadow is close. Rod and staff comfort because they are contact, not because pain has been cancelled. The table in the face of foes is the scandal: nourishment is not postponed until the enemies leave. Loyalty hunts the wanderer down. Length of days in the house is remaining in the presence that made lack impossible — not a real-estate promise.",
        keyIdea: "Speak You when the shadow is close. Do not wait for the valley to empty.",
        misconception:
          "That the shepherd is an insurance policy, or that comfort means the valley has been cancelled.",
        passageId: "psalms_tehillim.psalm_023",
        supportingPassageIds: ["psalms_tehillim.psalm_062"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Stay in the second person with me. Help me tell accompaniment from an insurance policy. Where am I still bargaining for exemption instead of speaking You in the valley?",
        practice:
          "In one actual difficulty today, switch from talking about God to three sentences of You. Walk the next hour without bargaining that the difficulty be removed as proof of being shepherded.",
        journalPrompt:
          "Where am I still bargaining for exemption instead of accompaniment?",
        integration:
          "You can tell accompaniment from an insurance policy, and speak You in the valley.",
      },
      {
        id: "ps-deep-calls",
        title: "Deep calls to deep",
        orientation:
          "Address now has to survive absence. If thirst is managed as a mood, later prayer is postponed until you feel better.",
        teaching:
          "Thirst is the first theology. The deer is not decoration; the throat-being pants. Exile from the Face is measured in tears-as-bread and in the taunt Where is your God — a question the singer also has. He lectures his own nephesh to wait, then admits it is still down, then lectures again. Memory of the festival is fuel that also burns. Deep calls to deep: chaos-water is correspondence, abyss answering abyss, while breakers pass over. The mystical psalm is not the one that has arrived. It is the one that still asks when it will see the Face, and teaches its own soul to wait anyway.",
        keyIdea: "Speak thirsty. Do not wait for a better mood to count as prayer.",
        misconception:
          "That thirst is a mood to manage until you feel like praying, or that nostalgia is already the prayer.",
        passageId: "psalms_tehillim.psalm_042",
        supportingPassageIds: ["psalms_tehillim.psalm_077"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Keep this as address, not as a mood report. Help me pray thirsty without waiting to feel better. Where am I still postponing speech until the nephesh is up?",
        practice:
          "When a dry hour comes, speak one sentence to the Face before you manage the mood. Then tell your nephesh once to wait — and notice, without correcting it, if it is still down.",
        journalPrompt:
          "Am I waiting to feel better before I will speak?",
        integration:
          "You can pray thirsty, and tell the difference between waiting and postponing speech.",
      },
      {
        id: "ps-drop-and-know",
        title: "Drop, and know",
        orientation:
          "After thirst, the hands are still saving the mountains. Knowledge arrives after the grip drops.",
        teaching:
          "Cosmos unravels: earth changing, mountains into the sea's heart. The still point is not stoic temperament. It is presence in a place: God in the city's midst, so she does not totter. Nations roar like the waters roared. The famous line is harpu u-de'u: drop, slack your grip, and know that I am God. Knowledge here is what happens when the hands stop saving the mountains. It is not a seminar. Cessation of war is God's work in the song, not a peace plan the psalm is congratulating. Selah keeps interrupting because the body needs a rest in a psalm about not tottering.",
        keyIdea: "Slack first. Knowing is what the drop makes possible.",
        misconception:
          "That stillness is décor, a calm temperament, or a spiritual technique you grip harder.",
        passageId: "psalms_tehillim.psalm_046",
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Do not treat stillness as décor or as a better grip. Model harpu: slack, then know. What am I still gripping so that I will not have to know?",
        practice:
          "Catch one grip that is saving the mountains — a plan, an argument, a spiritual technique held too tight. Slack the hands for one minute. Only then say: know that I am God. Do not improve the minute into a better grip.",
        journalPrompt:
          "What am I still gripping so that I will not have to know?",
        integration:
          "You can tell dropping from décor, and let knowledge come after the slack.",
      },
      {
        id: "ps-dry-land",
        title: "A dry land without water",
        orientation:
          "Dropping is not indifference. Desire remains: flesh fainting, loyalty ranked above the outcome.",
        teaching:
          "Dawn-seeking, thirst, flesh fainting: a desert that is geography and soul. Ḥesed is better than life — the most dangerous mystical sentence in the selection. It does not despise life. It ranks loyalty above the organism's continuance, which is either insanity or the beginning of worship. Seeing in the holy place is remembered in a dry land; vision is portable as memory and as night-watch murmur. My being clings after you, while the right hand holds: effort and being-held in one couplet. Do not spiritualize the dryness away. The mystical core is the clinging in a land without water.",
        keyIdea: "Cling. Do not upgrade dryness into a self-care plan.",
        misconception:
          "That desire for God is a metaphor for self-care, or that ranking loyalty above life means despising the body.",
        passageId: "psalms_tehillim.psalm_063",
        supportingPassageIds: ["psalms_tehillim.psalm_027"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Keep thirst as address, not as a wellness project. Help me cling without despising the body. Have I turned desire for God into a metaphor for taking care of myself?",
        practice:
          "In one dry hour, make one physical clinging gesture — hand closed on nothing, forehead to a wall, sitting still — and speak: your loyalty is better than the outcome I want. Then eat or drink if the body needs it. Do not despise the life.",
        journalPrompt:
          "Have I turned desire for God into a metaphor for taking care of myself?",
        integration:
          "You can desire without turning thirst into a wellness project, and without despising the body.",
      },
      {
        id: "ps-secret-place",
        title: "The secret place",
        orientation:
          "The Psalter's most misused psalm has to be disarmed. Refuge is lodging, not a force field.",
        teaching:
          "The secret place of the Most High is the psalm's mystical address. Sitting there is already lodging in the shadow. The promises that follow are so absolute they have always been misused as a force field. The psalm itself is more intimate than insurance. Night-terror and noon-destruction are named so they can be un-feared, not so plagues can be pretended imaginary. With him I am in trouble — God is not a remote canopy. God is in the trouble with the one who knows the name. Clinging answers the dry land. Length of days is satisfaction, not adrenaline.",
        keyIdea: "Lodge. Do not recite a charm. Be with in the trouble.",
        misconception:
          "That refuge is a talisman or bargain for immunity, or that naming terrors means pretending they are imaginary.",
        passageId: "psalms_tehillim.psalm_091",
        supportingPassageIds: ["psalms_tehillim.psalm_121"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Refuse the force-field reading. Model lodging: with you I am in this. What bargain am I still reciting so that trouble will not be allowed?",
        practice:
          "Recite no protection formula. Sit inside one actual trouble and say only: with you I am in this. Then do the next necessary act without the bargain that the trouble must lift as proof.",
        journalPrompt:
          "What bargain am I still reciting so that trouble will not be allowed?",
        integration:
          "You can tell lodging from a talisman, and stay in trouble without the force-field deal.",
      },
      {
        id: "ps-weaned-child",
        title: "Like a weaned child",
        orientation:
          "After refuge, ambition still lifts the heart toward wonders too-wondrous. Quiet is trained.",
        teaching:
          "Three verses, and the Psalter's program in a body. Not a lifted heart, not eyes raised. Great things and wonders too-wondrous: a refusal of spiritual ambition that still leaves wonder to God. I have leveled and silenced my nephesh like a weaned child on its mother. Weaned, not nursing: this is not fusion. It is a child that no longer screams for the breast and can sit. The being is that child, and also the child is upon me — mothered and holding. Quiet is the pedagogy. Checked-out numbness is a counterfeit of this sit.",
        keyIdea: "Sit weaned. Do not scream for the next breast of experience.",
        misconception:
          "That weaned means infantile spirituality, or that quieted means checked-out numbness.",
        passageId: "psalms_tehillim.psalm_131",
        supportingPassageIds: ["psalms_tehillim.psalm_130"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Model weaned, not nursing and not numb. Help me refuse spiritual ambition without despising wonder. What great spiritual thing am I still screaming for as if it were milk?",
        practice:
          "For ten minutes, do not lift the heart toward a great spiritual project. Sit as a weaned child. When a demand for milk arises — insight, mood, outcome — let it fail. Hold the child. Then do one ordinary task without using it to prove quiet.",
        journalPrompt:
          "What great spiritual thing am I still screaming for as if it were milk?",
        integration:
          "You can tell weaned quiet from infantile fusion and from checked-out numbness.",
      },
      {
        id: "ps-where-can-i-flee",
        title: "Where can I flee from your face",
        orientation:
          "The walk opened under the night that remembers a human. It closes where there is no elsewhere.",
        teaching:
          "The Psalter's most complete map of inescapable presence begins as knowledge that feels like siege: behind and before you have enclosed me. Where can I flee from your face is not curiosity. It is the last privacy-strategy, and it fails in every direction. Darkness will not crush the speaker into hiding; night shines for this You. Then embryology: woven in the womb, the unformed mass seen. The Face that fills the vertical cosmos also read the days not yet formed. You wake and are still with — clinging after a tour of inescapability. Do not make this cute. Omniscience is first terror and then thanks. Surveillance is the counterfeit of this enclosure.",
        keyIdea: "Fleeing is still location inside the address. Speak even here.",
        misconception:
          "That inescapable presence is surveillance, or that it is a cute promise that you are never alone.",
        passageId: "psalms_tehillim.psalm_139",
        supportingPassageIds: ["psalms_tehillim.psalm_016"],
        theme: "recognition",
        chatMode: "practice",
        chatPrompt:
          "Keep this as address, not as a doctrine of omniscience. Do not sweeten it. Help me tell enclosure from surveillance. Where do I still go to get a room God is not in?",
        practice:
          "Name one place you go to hide — a room, a scroll, a plan. Go there or sit as if there. Speak once: even here. Do not sweeten it into you are never alone. Do one act in that place that does not depend on remaining unseen.",
        journalPrompt:
          "Where do I still go to get a room God is not in?",
        integration:
          "You can tell inescapable presence from surveillance, and stop demanding a room outside the Face.",
      },
    ],
  },
  {
    id: "what-is-up-to-you",
    title: "What Is Up to You",
    level: "Beginner",
    focus: "Stoicism: train the ruling faculty on what is actually yours",
    outcome:
      "Draw the division without going limp, train desire so externals cannot wreck you, catch the judgment that authors disturbance, wish the given, play the unchosen part, delay assent to insult, keep death in view, and meet the morning already rehearsed.",
    description:
      "An eight-gate walk through the Enchiridion, closed by Marcus at dawn.",
    arc:
      "The Gītā path borrowed one Enchiridion cut as a guest. This walk is the handbook's own order. First the ontology: some things are up to you. Then desire is trained at the root, because an untrained want is a contract with wretchedness. Disturbance is shown to have one author — your judgment, not the event. Then you wish that things happen as they do; you play the part you did not cast; you insert time before anger. Death stands before the eyes so desire keeps measure. Marcus opens the day by pre-speaking the difficult people, so their weather cannot steal the ruling faculty by surprise.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "stoic-division",
        title: "Some things are up to you",
        orientation:
          "The handbook does not open with calm. It opens with a cut in what exists.",
        teaching:
          "Of existing things, some are up to us and some are not. Up to us: judgment, impulse, desire, aversion — in short, our own doing. Not up to us: body, property, reputation, office — everything that is not our own doing. This is not a mood of not caring, and it is not yet a counsel about action's fruit. It is a map of sovereignty. Suffering comes from staking peace on the second list while calling it the first. The ruling faculty is trained here, before reaction, by withdrawing demand from what was never yours. Freedom is this precision — not a later feeling of being above it all.",
        keyIdea: "The cut is in things, not in your preference for calm. Freedom starts as an accurate map.",
        misconception:
          "That the division means becoming cold or passive, or that it is the same teaching as releasing the fruit of work.",
        passageId: "epictetus_works.epi_enc_001",
        theme: "freedom",
        chatMode: "explain",
        chatPrompt:
          "Help me use the division as a map of sovereignty, not as a mood. Where do I confuse it with not caring, or with releasing a work's result?",
        practice:
          "Take one live upset. Split it into two lists: mine to govern, not mine. Do not soothe yourself. Make the lists honest. Then put your next effort only on the first list.",
        journalPrompt:
          "Where have I staked my peace on what I cannot command?",
        integration:
          "You can draw the boundary without using it as an excuse to go limp.",
      },
      {
        id: "stoic-desire",
        title: "Train desire at the root",
        orientation:
          "The division is useless if desire still signs contracts with what is not yours.",
        teaching:
          "Desire promises attainment; aversion promises escape. Fail the first and you are disappointed; meet the second and you are wretched. Confine aversion to what is contrary to the natural use of your own faculties. If you are averse to sickness, death, or poverty, you will be wretched. For the present, suppress desire: if you desire what is not in your control, you must be disappointed; of what is in your control and laudable, nothing is yet in your possession. Use pursuit and avoidance lightly, with gentleness and reservation. Stoicism is not the absence of preference. It is the refusal to let preference become a hostage situation.",
        keyIdea: "Desire is a contract with disappointment until it is trained. Pursue with reservation.",
        misconception:
          "That a Stoic has no preferences, or that suppressing desire means never trying.",
        passageId: "epictetus_works.ench_02",
        supportingPassageIds: ["epictetus_works.epi_enc_001"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me convert one external desire into reserved pursuit without pretending I want nothing.",
        practice:
          "Name one desire aimed at an external — health-as-guaranteed, praise, a timeline. For today, convert it to reserved pursuit: I will try; I do not demand. When the old contract returns, name it and loosen it.",
        journalPrompt:
          "What am I still desiring that, if it fails, must make me wretched?",
        integration:
          "You can pursue without signing the contract that failure wrecks you.",
      },
      {
        id: "stoic-dogma",
        title: "Disturbance has one author",
        orientation:
          "Now the handbook locates the cause. The event is not innocent, but it is not the author of your soul's weather.",
        teaching:
          "People are disturbed not by things themselves but by their judgments about things. Death is nothing terrible — if it were, it would have appeared so even to Socrates — but the judgment about death, that it is terrible, that is what is terrible. This is not positive thinking. The pragmata are causally inert toward the soul until you assent. The dogma does the harm. If you keep blaming the message, the delay, the other person, you will never find the one place you actually govern: the judgment you are adding.",
        keyIdea: "The thing happened. The judgment did the harm. Disturbance has one author.",
        misconception:
          "That this means events do not matter, or that looking on the bright side is the same teaching.",
        passageId: "epictetus_works.epi_enc_002",
        supportingPassageIds: ["epictetus_works.epi_enc_001"],
        theme: "mind",
        chatMode: "explain",
        chatPrompt:
          "Separate one live disturbance into the event and the judgment I added. Do not let this become a pep talk.",
        practice:
          "Catch one disturbance. Name the thing, then name the judgment you added. Hold them apart for ten breaths before you act. If you cannot find the judgment, you are still fused with it — look again.",
        journalPrompt:
          "What event am I blaming for a disturbance that is actually my judgment?",
        integration:
          "You can point to the judgment as the author, without denying the event.",
      },
      {
        id: "stoic-wish-given",
        title: "Wish that they happen as they do",
        orientation:
          "The given is not a broken promise. It is the material.",
        teaching:
          "Do not demand that things happen as you wish, but wish that they happen as they do happen, and you will go on well. This is not calling every event pleasant, and it is not the Gītā's release of a work's fruit. It is about the arriving fact — already the case — which you are still treating as a debt the world failed to pay. You may still act vigorously where action is yours. You refuse to make flourishing depend on the world having been otherwise. The good person does not rename pain as nice. They stop waiting for a different past before they will live.",
        keyIdea: "The given is material for virtue, not a verdict on you. Wish the actual, then act.",
        misconception:
          "That this is fatalism, or that you must approve of every deed and condition.",
        passageId: "epictetus_works.ench_08",
        supportingPassageIds: ["epictetus_works.epi_enc_001"],
        theme: "freedom",
        chatMode: "practice",
        chatPrompt:
          "Show me how wishing the given differs from passivity and from pretending I like what I do not like.",
        practice:
          "When one thing goes other than planned, say: it happened as it did. Then take the next action that is still yours. Do not rewrite the event first.",
        journalPrompt:
          "What arriving fact am I still treating as a broken promise?",
        integration:
          "You can meet an unwanted fact without waiting for it to become the fact you wanted.",
      },
      {
        id: "stoic-the-part",
        title: "You did not cast the part",
        orientation:
          "Identity wants to renegotiate the role. The handbook will not allow it.",
        teaching:
          "Remember that you are an actor in a drama of whatever kind the Director chooses — short if short, long if long. If you are to play a poor man, play it skillfully; a lame man, a ruler, a private person — the same. This is your business: to play the given part well. The choosing of the part belongs to another. Resentment of the role is a second drama you add, and it is not skill. Skill is in the playing. You are not entitled to the casting, and you are not excused from the acting.",
        keyIdea: "Skill is in the playing, not in the casting. The part is given; the playing is yours.",
        misconception:
          "That you chose your circumstances as a spiritual lesson, or that playing well means enjoying the part.",
        passageId: "epictetus_works.epi_enc_003",
        supportingPassageIds: ["epictetus_works.ench_08"],
        theme: "action",
        chatMode: "practice",
        chatPrompt:
          "Help me name the part I am actually in — not the one I auditioned for — and play the next hour of it without grievance as a side-plot.",
        practice:
          "Name the part you are actually in today. Play the next hour of it skillfully, without a side-commentary of grievance. Skill means the next honest act, not a performance of cheer.",
        journalPrompt:
          "Which role am I resenting as if I had been entitled to cast it?",
        integration:
          "You can do the given role well without confusing it with who chose it.",
      },
      {
        id: "stoic-interval",
        title: "The interval before anger",
        orientation:
          "Insult looks like it comes from outside. The handbook inserts time before you agree.",
        teaching:
          "Not the one who gives ill language or a blow insults you, but the principle which represents these things as insulting. When anyone provokes you, it is your own opinion that provokes you. First, do not be hurried away with the appearance. If you gain time and respite, you will more easily command yourself. Rage needs your assent. The blow happened. The insult is the judgment that you have been diminished and must retaliate. Delay is not stuffing. It is the recovery of the ruling faculty before speech.",
        keyIdea: "Rage needs your assent. Insert time between appearance and action.",
        misconception:
          "That the other person caused your rage, or that the pause means you must tolerate harm.",
        passageId: "epictetus_works.ench_20",
        supportingPassageIds: ["epictetus_works.epi_enc_002"],
        theme: "mind",
        chatMode: "practice",
        chatPrompt:
          "Give me a way to delay assent without becoming a doormat. What does the interval actually protect?",
        practice:
          "The next provocation: feel the appearance, and wait. Ten breaths, or until the body cools one degree. Then choose the response. If you cannot wait, you have found the gate — that is the practice, not a shame.",
        journalPrompt:
          "Where do I fuse appearance, insult, and impulse into one act?",
        integration:
          "You can insert time between appearance and action.",
      },
      {
        id: "stoic-death",
        title: "Keep death before the eyes",
        orientation:
          "Memento mori here is hygiene for desire, not a death-contemplation path.",
        teaching:
          "Let death, exile, and everything that appears frightening stand before your eyes each day — above all, death. Then you will never entertain a base thought, nor desire anything with excess. This is not brooding, and it is not the mixed letting-go sampler. It is measure. What is regularly faced loses its power to surprise, flatter, or govern. Death is the limit that checks petty calculation and runaway wanting. If death in view makes you smaller and theatrical, you are decorating gloom. If it makes you cleaner, you have the use.",
        keyIdea: "The limit clarifies attachment. Keep death in view so desire keeps measure.",
        misconception:
          "That this is morbid rumination, or that remembering death means withdrawing from life.",
        passageId: "epictetus_works.faithful_ench_21",
        supportingPassageIds: ["epictetus_works.epi_enc_002"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me keep death in view as measure, not as gloom. What becomes small? What becomes enough?",
        practice:
          "Once today, look at death as a fact of this life, not as a mood. Ask: what becomes small? What becomes enough? Act from that for one hour. Do not announce it.",
        journalPrompt:
          "What petty calculation or excess desire would die if death stood in view?",
        integration:
          "Death in view makes you cleaner, not smaller.",
      },
      {
        id: "stoic-morning",
        title: "Begin the day already ready",
        orientation:
          "The handbook's disciplines now enter the morning, before the first message.",
        teaching:
          "Begin the morning by saying to yourself: I will encounter the meddlesome, the ungrateful, the arrogant, the deceitful, the envious, the unsocial. This is not bitterness and not cynicism. It is prolégein — pre-speaking — so their appearance cannot steal the ruling faculty by surprise. You do not hope the day will be populated by easy people. You refuse to treat ordinary human weather as a personal verdict. The rehearsal is how Marcus keeps the division live: their character is not yours to govern; yours is. Meet them already ready, and the insult has nowhere to land as theft.",
        keyIdea: "Name the friction before it arrives, and it is not a theft of the day.",
        misconception:
          "That expecting difficult people is bitterness, or that readiness means bracing into hardness.",
        passageId: "marcus_aurelius_meditations.ma_02_01",
        supportingPassageIds: ["epictetus_works.ench_20"],
        theme: "action",
        chatMode: "practice",
        chatPrompt:
          "Help me rehearse tomorrow's difficult people without turning it into contempt. What does readiness protect?",
        practice:
          "Tomorrow morning, before the first message, name three difficult types you are likely to meet. When one arrives, recognize the rehearsal. Keep your own character. Do not collect the encounter as proof that people are terrible.",
        journalPrompt:
          "Whom do I still meet as a personal insult instead of as the day's given material?",
        integration:
          "Another person's weather can arrive without becoming your verdict on the day.",
      },
    ],
  },
  {
    id: "the-beloved-in-plain-sight",
    title: "The Beloved in Plain Sight",
    level: "Intermediate",
    focus: "Sufi: the Beloved is not an object over there; love unmakes the claimant",
    outcome:
      "Stop treating God as a destination; notice the veil of oneness; tell clouding from covering; drop the Sufi costume; walk nearness without geography; let love outrun a piety-badge; lose the arrival-self; meet the king as the company in the mirror.",
    description:
      "An eight-gate walk through Balyānī, Hujwīrī, and ʿAṭṭār — identity, unveiling, then the birds' road.",
    arc:
      "We begin where Balyānī begins: whoever knows himself knows his Lord — not because a traveler reached a deity, but because the self beside God has no being of its own. The veil is oneness itself; nothing other than He hides Him. Hujwīrī will not let unveiling become extra information: two veils, one that lifts and one that seals, then the true Sufi as a change in the seer, not a costume. The hoopoe summons the birds: the king is near, yet we are far; light veils as well as darkness. Love holds a station higher than the badges of faith and heresy. Poverty and annihilation undo the arrival-self. Thirty birds look in the mirror and find Simurgh — the Beloved who was never a king standing apart.",
    estimatedSessions: "8 gates · ~20 min each",
    steps: [
      {
        id: "bls-know-the-lord",
        title: "Know yourself, know the Lord",
        orientation:
          "Before any unveiling or bird-quest, the direction of travel has to reverse. God is not an object you go toward.",
        teaching:
          "Whoso knoweth himself knoweth his Lord. This is not moral inventory and not a nicer psychology of the soul. The “I” that stands beside God has no being of its own; only God truly is. Knowledge of the Lord happens when the self's claim to separate reality is seen through — not when a traveler finally arrives at a deity over there. If you skip this, later stations become tourism toward a hidden king. The nearest thing — your own self — is already the first false distance.",
        keyIdea: "The Lord is known when the claimant is seen through, not when you arrive at an object called God.",
        misconception:
          "That God is an object over there you could travel toward, or that self-knowledge means cataloguing your personality.",
        passageId: "know_yourself_ibn_arabi_balyani.ky_001",
        supportingPassageIds: ["know_yourself_ibn_arabi_balyani.kys_p001"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Model the reversal: God is not an object over there. Help me hear 'know yourself, know the Lord' as a change of direction, not as self-improvement. Where am I still treating God as a destination?",
        practice:
          "Catch one moment you defend an identity — a role, an opinion, a hurt. Ask: what in this claim is truly mine by itself? Leave the question unanswered. Do not manufacture a spiritual conclusion.",
        journalPrompt:
          "Where am I still treating God as an object I could go toward?",
        integration:
          "You can feel the difference between looking for God and noticing the claimant.",
      },
      {
        id: "bls-veil-is-oneness",
        title: "The veil is oneness itself",
        orientation:
          "If nothing other than God has being, nothing other than God can hide God. The curtain is not a created wall.",
        teaching:
          "His veil is only His oneness; nothing veils Him other than He. Matter, distance, ego, even a separate cosmos cannot stand between God and vision if they have no independent being. The Absolute cannot be set before a knower as an object among objects. The curtain you keep trying to lift is the impossibility of objectifying the One. Stop blaming a second thing — the world, the mind, a teacher — for hiding what cannot be placed in front of you.",
        keyIdea: "No second thing hides God. Oneness itself is the screen.",
        misconception:
          "That something other than God veils God — matter, ego, distance, a cosmos standing in the way.",
        passageId: "know_yourself_ibn_arabi_balyani.ky_005",
        supportingPassageIds: ["know_yourself_ibn_arabi_balyani.kys_p007"],
        theme: "recognition",
        chatMode: "explain",
        chatPrompt:
          "Show me how oneness can be a veil without being a created barrier. What image of God am I still trying to stand in front of?",
        practice:
          "When you catch yourself treating God as a distant object to grasp, drop every image — near, far, bright, hidden — for one minute. Say only: nothing veils Him other than He.",
        journalPrompt:
          "What created thing am I still blaming for hiding God?",
        integration:
          "You can stop hunting a created barrier and sit with the not-object.",
      },
      {
        id: "bls-two-veils",
        title: "Two veils before the Truth",
        orientation:
          "Unveiling is now a condition of the heart, not a fact you could collect.",
        teaching:
          "There are two veils. Clouding (ghayn) lifts; covering (rayn) seals. One heart still seeks the Truth and flees falsehood — attributes obscure it, but the orientation remains. Another no longer tells true from false at all. Deeds spread a covering over the heart. More information does not remove that. Kashf is not a larger library. The question is whether you can still desire truth and recoil from a lie you would rather keep.",
        keyIdea: "Unveiling is a condition of seeing, not a pile of facts.",
        misconception:
          "That more information lifts the veil, or that every obscurity is equally removable.",
        passageId: "kashf_al_mahjub.kam_25",
        supportingPassageIds: ["kashf_al_mahjub.kam_24"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Help me tell a clouding I can lift from a covering I would rather not name. Where am I using study as a substitute for wanting the truth?",
        practice:
          "Name one clear truth and one tempting falsehood — an excuse, a softening, a silence. Write each in a sentence. Perform the smaller truthful action before the day ends.",
        journalPrompt:
          "Am I still treating unveiling as a fact I could collect?",
        integration:
          "You can tell clouding you can lift from a covering you would rather not name.",
      },
      {
        id: "bls-true-sufi",
        title: "The true Sufi is not a costume",
        orientation:
          "The handbook now measures Sufism by a change in the seer, not by wool, vocabulary, or a better self.",
        teaching:
          "The true Sufi leaves impurity behind. The women of Egypt first gazed as ordinary subjects, then their human measure was annihilated before Yusuf's beauty, and they cried: this is no human being. The miracle is not the face. It is the altered capacity to see. Wool, technical speech, and a refined identity are still bashariyyat in costume. If you skip this, the bird-quest becomes a spiritual holiday you could narrate. Sufism is the leaving, not the outfit.",
        keyIdea: "Purity is a change in the seer, not a label on the seen.",
        misconception:
          "That Sufism is a costume — wool, jargon, a holier personality — or that beauty is the miracle rather than the seeing.",
        passageId: "kashf_al_mahjub.kam_07",
        supportingPassageIds: ["kashf_al_mahjub.kam_04"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Where am I wearing a Sufi look as proof? Help me tell a change in seeing from a better costume.",
        practice:
          "When something strongly attracts or repels you, pause before naming it. Write one sentence: what this reveals about my present state is… Find the self-protective judgment in that sentence and do not act on it for the rest of the day.",
        journalPrompt:
          "What Sufi look, insight, or posture am I still wearing as proof?",
        integration:
          "You can catch a spiritual costume and set it down without replacing it.",
      },
      {
        id: "bls-near-yet-far",
        title: "Near, yet we are far",
        orientation:
          "The hoopoe converts a monarchic quest into a discipline of dispossession. The king is not a place on a map.",
        teaching:
          "We have a king named Simurgh, dwelling beyond Mount Qaf. He is near, yet we are far from him. A hundred thousand veils of light and darkness screen the throne. Light veils as well as darkness — a spiritual certainty can halt you as surely as ignorance. The road is not miles. Distance is produced by the self that wants to own the vision. Courage here is not travel stamina. It is self-effacement: the claimant who says “I will get the glimpse” is already the obstacle.",
        keyIdea: "The king is near. The claimant is what makes the far.",
        misconception:
          "That the journey is geography, or that a spiritual high is progress rather than a veil of light.",
        passageId: "conference_of_the_birds.cot_01",
        supportingPassageIds: ["conference_of_the_birds.cot_02"],
        theme: "practice",
        chatMode: "explain",
        chatPrompt:
          "Help me hear 'near yet far' as a diagnosis of the possessive self, not as a map. Which veil of light am I treating as arrival?",
        practice:
          "Name one veil of light — a praise, a spiritual feeling, a certainty you treat as arrival. Say it aloud. Then do one quiet helpful act without mentioning it to anyone.",
        journalPrompt:
          "Where am I still treating the Beloved as a destination on a map?",
        integration:
          "You can feel nearness without turning it into a trip you could complete.",
      },
      {
        id: "bls-love-beyond-faith",
        title: "Love beyond faith and unbelief",
        orientation:
          "The lede said love is the way. Here the hoopoe makes that costly: piety is not the ticket.",
        teaching:
          "Whoever has become a lover should not think of his own life. Love holds a station higher than religion and has nothing to do with faith or heresy. This is not permission to despise form. It is the claim that īmān and kufr can become possessions the ego guards — identities you display to remain safe. Love unmakes the measure. If you take “beyond faith” as a new badge, you have only swapped costumes. Exposure to the Beloved is the work; a verdict, pious or accused, is shelter.",
        keyIdea: "Faith as a badge is still self-preservation. Love outruns the verdict.",
        misconception:
          "That piety is the ticket, or that 'beyond faith' means despising ethical and religious form.",
        passageId: "conference_of_the_birds.cot_08",
        supportingPassageIds: ["conference_of_the_birds.cot_17"],
        theme: "practice",
        chatMode: "practice",
        chatPrompt:
          "Where am I using a religious or moral label as shelter? Help me tell love from a new antinomian costume.",
        practice:
          "Write one religious, moral, or intellectual label you feel compelled to defend. Under it, name the fear that makes you defend it. Then do one uncredited act of care without mentioning the label.",
        journalPrompt:
          "Which badge of piety am I still using as a ticket?",
        integration:
          "You can love without using a verdict — pious or accused — as shelter.",
      },
      {
        id: "bls-poverty-annihilation",
        title: "Poverty and annihilation",
        orientation:
          "The last valley refuses the arrival-self. Fanāʾ is not a trophy identity.",
        teaching:
          "Last comes the Valley of Poverty and Annihilation. Shadows vanish under a single ray. Both worlds are forms on the surface of an ocean. Fanāʾ is not death and not a quieter, holier “I.” It is the undoing of the illusion of separation. If return from that oblivion is given, you understand creation — not as a bigger self who made it back. People stall here by collecting annihilation as an achievement. The hallucination is persistent selfhood, including the spiritual kind.",
        keyIdea: "Arrival is not a better identity. It is the end of the claimant.",
        misconception:
          "That arrival confers a better identity, or that annihilation means you disappear as a corpse or a blank.",
        passageId: "conference_of_the_birds.cot_22",
        supportingPassageIds: ["conference_of_the_birds.cot_20"],
        theme: "self",
        chatMode: "practice",
        chatPrompt:
          "Help me tell fanāʾ from a holier costume. What am I still hoping arrival will make me into?",
        practice:
          "Sit ten minutes where you cannot speak or be heard. Do not meditate on a theme. Notice what you reach for to confirm you exist — a thought, a plan, a spiritual report. Let each dissolve. Sit one more minute in what remains. Do not congratulate a new self.",
        journalPrompt:
          "What better self am I still hoping arrival will confer?",
        integration:
          "You can tell loss of the claimant from a quieter, holier costume.",
      },
      {
        id: "bls-thirty-birds",
        title: "Thirty birds in the mirror",
        orientation:
          "The pun closes the walk: Simurgh is sī murgh. The king you wanted as an object does not appear.",
        teaching:
          "The Sun of Majesty is a mirror. Thirty birds find thirty birds. The pun — sī murgh, Simurgh — is the teaching: you do not meet a sovereign standing apart from the company that completed the road. What you see is yourselves, transformed, and still not a possession of the Real. An ant does not lift the Pleiades. The Beloved was in plain sight — as the ones who remained — and still not yours to own. Rūmī's reed complains of the same cut: the music is the wound of separation, not a report from a king next door.",
        keyIdea: "The king is not other than the arrived company, and still not yours to own.",
        misconception:
          "That you will see a king who is not you — an object standing apart — or that the mirror means you simply are God.",
        passageId: "conference_of_the_birds.cot_28",
        supportingPassageIds: ["rumi_mathnawi_yi_manawi.mth_001"],
        theme: "recognition",
        chatMode: "compare",
        chatPrompt:
          "Model the mirror as how to stand, not as an image to admire. Help me hear Simurgh without collapsing into 'I am God' or keeping a king next door. What does the reed's lament add that the birds' arrival does not?",
        practice:
          "Before a mirror, name three roles you usually are. Look one minute without praise or blame. Cross out one role. Do one small action that does not defend it.",
        journalPrompt:
          "Am I still hoping to see a king who is not the one who arrived?",
        integration:
          "You can meet your own face without demanding a king who stands apart from it.",
      },
    ],
  },
];
