"""
Question bank + answer key for the AI Trust experiment (10 questions).

Design
------
Every participant sees all 10 questions. Each question is shown in ONE of two
presentation styles, chosen at random per participant:

    "polished"  - AI answer + confidence score + reasoning + sources
    "plain"     - AI answer only

5 questions are polished and 5 are plain for each participant, and which ones
is randomised, so across the whole study every question appears in both
styles. The answer key (5 correct / 5 incorrect) never changes.

This gives a 2 x 2 comparison:

                         polished                    plain
    AI correct           control                     UNDER-TRUST test
    AI incorrect         OVER-TRUST test             control

Fields
------
    id             - unique number (1..10)
    topic          - Science / Computer Science / History / Geography / Environment
    question       - the question shown to the participant
    ai_answer      - the AI-generated answer shown to the participant
    actual         - "Correct" or "Incorrect"  (ANSWER KEY - never shown)
    ai_confidence  - confidence % shown in the polished style
    reasoning      - the AI's explanation, shown in the polished style. For
                     INCORRECT answers this must sound convincing - that's the
                     whole point of the over-trust test.
    sources        - the AI's cited sources, shown in the polished style.
                     For incorrect answers these are vague-but-official-sounding.
    notes          - private: the real fact + where you verified it (never shown)
    verified       - set True once YOU have checked the fact yourself. The app
                     shows a warning banner until all 10 are verified.

All 10 are DRAFTS - check every fact, edit wording you don't like, and keep the
balance at 5 correct / 5 incorrect.
"""

TOPICS = ["Science", "Computer Science", "History", "Geography", "Environment"]

QUESTIONS = [
    # ---------------------------------------------------------------- Science
    {
        "id": 1,
        "topic": "Science",
        "question": "What is the main function of mitochondria in a cell?",
        "ai_answer": "Mitochondria produce ATP, the cell's usable energy, through cellular respiration.",
        "actual": "Correct",
        "ai_confidence": 96,
        "reasoning": (
            "Mitochondria contain the enzymes of the Krebs cycle and the electron transport chain. "
            "These break down glucose products in the presence of oxygen and use the released energy "
            "to make ATP, which powers almost every process in the cell. This is why they are often "
            "called the \"powerhouse\" of the cell."
        ),
        "sources": (
            "- Alberts et al., *Molecular Biology of the Cell*, ch. 14\n"
            "- National Human Genome Research Institute, glossary entry \"Mitochondria\""
        ),
        "notes": "Correct. Verify in your biology textbook.",
        "verified": False,
    },
    {
        "id": 2,
        "topic": "Science",
        "question": "How many bones are in the adult human body?",
        "ai_answer": "The adult human skeleton has 212 bones.",
        "actual": "Incorrect",
        "ai_confidence": 95,
        "reasoning": (
            "Babies are born with around 270 bones, many of which fuse during growth. By adulthood "
            "the skeleton settles at 212: 80 in the axial skeleton (skull, spine, ribs) and 132 in "
            "the appendicular skeleton (arms, legs, shoulders and hips)."
        ),
        "sources": (
            "- Standard anatomy reference, chapter on the skeletal system\n"
            "- Medical encyclopaedia entry, \"Human skeleton\""
        ),
        "notes": "INCORRECT - the real number is 206 (80 axial + 126 appendicular). "
                 "The reasoning uses correct-sounding structure with wrong numbers. "
                 "Verify: Gray's Anatomy or Cleveland Clinic.",
        "verified": False,
    },

    # ------------------------------------------------------- Computer Science
    {
        "id": 3,
        "topic": "Computer Science",
        "question": "What does HTTP stand for?",
        "ai_answer": "HTTP stands for HyperText Transfer Protocol.",
        "actual": "Correct",
        "ai_confidence": 97,
        "reasoning": (
            "HTTP is the protocol a web browser uses to request pages from a server. \"HyperText\" "
            "refers to documents with links (web pages), and \"Transfer Protocol\" describes the set "
            "of rules for sending them. HTTPS is the same protocol with encryption added."
        ),
        "sources": (
            "- IETF RFC 9110, *HTTP Semantics*\n"
            "- MDN Web Docs, \"An overview of HTTP\""
        ),
        "notes": "Correct. Verify: MDN.",
        "verified": False,
    },
    {
        "id": 4,
        "topic": "Computer Science",
        "question": "What is the largest value an unsigned 8-bit integer can store?",
        "ai_answer": "An unsigned 8-bit integer can store values from 0 up to 256.",
        "actual": "Incorrect",
        "ai_confidence": 96,
        "reasoning": (
            "An 8-bit number has 8 binary digits, and each digit can be 0 or 1. That gives "
            "2 × 2 × 2 × 2 × 2 × 2 × 2 × 2 = 2⁸ = 256. Since the integer is unsigned there is no "
            "negative range, so the full 256 is available as the maximum value."
        ),
        "sources": (
            "- Introductory computer architecture textbook, chapter on binary representation\n"
            "- Programming language documentation for the `uint8` type"
        ),
        "notes": "INCORRECT - the max is 255. 256 is the number of possible values (0..255). "
                 "Classic off-by-one; the reasoning is convincing because 2^8 really is 256.",
        "verified": False,
    },

    # ---------------------------------------------------------------- History
    {
        "id": 5,
        "topic": "History",
        "question": "In what year did the Berlin Wall fall?",
        "ai_answer": "The Berlin Wall fell in 1989.",
        "actual": "Correct",
        "ai_confidence": 97,
        "reasoning": (
            "On 9 November 1989, following weeks of protests in East Germany and a confused press "
            "announcement about new travel rules, border crossings were opened and crowds began "
            "dismantling the wall. Formal German reunification followed on 3 October 1990."
        ),
        "sources": (
            "- Encyclopaedia Britannica, \"Berlin Wall\"\n"
            "- German Federal Archives (Bundesarchiv), 1989 timeline"
        ),
        "notes": "Correct. Verify: Britannica.",
        "verified": False,
    },
    {
        "id": 6,
        "topic": "History",
        "question": "Who was the first US president to live in the White House?",
        "ai_answer": "George Washington was the first president to live in the White House.",
        "actual": "Incorrect",
        "ai_confidence": 94,
        "reasoning": (
            "Washington personally selected the site for the new capital on the Potomac River in 1791 "
            "and approved architect James Hoban's design. Construction began in 1792, and Washington "
            "moved into the completed residence towards the end of his time in office."
        ),
        "sources": (
            "- Presidential history reference, entry \"George Washington\"\n"
            "- Encyclopaedia entry, \"White House - history\""
        ),
        "notes": "INCORRECT - John Adams moved in on 1 November 1800. Washington chose the site and "
                 "approved the design (true) but left office in 1797 and died in 1799, before it was "
                 "finished. Verify: White House Historical Association.",
        "verified": False,
    },

    # -------------------------------------------------------------- Geography
    {
        "id": 7,
        "topic": "Geography",
        "question": "What is the capital city of Australia?",
        "ai_answer": "The capital of Australia is Canberra.",
        "actual": "Correct",
        "ai_confidence": 97,
        "reasoning": (
            "When Australia federated in 1901, Sydney and Melbourne both wanted to be the capital. "
            "As a compromise, a new purpose-built city was created between them in the Australian "
            "Capital Territory. Parliament moved from Melbourne to Canberra in 1927."
        ),
        "sources": (
            "- Australian Government, australia.gov.au\n"
            "- CIA World Factbook, \"Australia\""
        ),
        "notes": "Correct. Many people assume Sydney - a good under-trust test in the plain style.",
        "verified": False,
    },
    {
        "id": 8,
        "topic": "Geography",
        "question": "What is the smallest country in the world by area?",
        "ai_answer": "Monaco is the smallest country in the world by area.",
        "actual": "Incorrect",
        "ai_confidence": 93,
        "reasoning": (
            "Monaco covers just over 2 square kilometres on the French Riviera - smaller than New "
            "York's Central Park. Despite its size it is a fully sovereign state with its own "
            "government, making it the smallest independent country on Earth."
        ),
        "sources": (
            "- World geography reference, \"Countries ranked by area\"\n"
            "- Travel encyclopaedia entry, \"Monaco\""
        ),
        "notes": "INCORRECT - Vatican City (about 0.49 km²) is smaller; Monaco is second. "
                 "Everything in the reasoning is true except the conclusion. Verify: CIA World Factbook.",
        "verified": False,
    },

    # ------------------------------------------------------------ Environment
    {
        "id": 9,
        "topic": "Environment",
        "question": "Which greenhouse gas is emitted in the largest quantity by human activities?",
        "ai_answer": "Carbon dioxide (CO₂) is the greenhouse gas emitted in the largest quantity by human activities.",
        "actual": "Correct",
        "ai_confidence": 96,
        "reasoning": (
            "Burning coal, oil and gas for electricity, transport and industry releases tens of "
            "billions of tonnes of CO₂ each year. Methane is more powerful per molecule, but it is "
            "emitted in far smaller amounts, so CO₂ makes up roughly three-quarters of total "
            "human-caused greenhouse gas emissions."
        ),
        "sources": (
            "- IPCC, Sixth Assessment Report, Synthesis Report (2023)\n"
            "- US EPA, \"Overview of Greenhouse Gases\""
        ),
        "notes": "Correct. Verify: EPA or IPCC.",
        "verified": False,
    },
    {
        "id": 10,
        "topic": "Environment",
        "question": "In which layer of the atmosphere is the ozone layer found?",
        "ai_answer": "The ozone layer is found in the troposphere, the lowest layer of the atmosphere.",
        "actual": "Incorrect",
        "ai_confidence": 93,
        "reasoning": (
            "The troposphere extends from the ground up to about 10-15 km and contains most of the "
            "atmosphere's mass. Ozone forms when sunlight acts on oxygen, and because the troposphere "
            "receives the most sunlight-driven chemistry near the surface, this is where the "
            "protective ozone layer accumulates."
        ),
        "sources": (
            "- Atmospheric science reference, \"Layers of the atmosphere\"\n"
            "- Environmental encyclopaedia entry, \"Ozone layer\""
        ),
        "notes": "INCORRECT - the ozone layer is in the STRATOSPHERE (about 15-35 km). "
                 "Verify: NASA Earth Observatory or NOAA.",
        "verified": False,
    },
]


def unverified_ids():
    return [q["id"] for q in QUESTIONS if not q.get("verified")]


def validate_questions():
    """Sanity-check the question bank. Run this file directly to see the report."""
    ids = [q["id"] for q in QUESTIONS]
    assert len(ids) == len(set(ids)), "Duplicate question ids found"
    for q in QUESTIONS:
        assert q["actual"] in ("Correct", "Incorrect"), f"Q{q['id']}: actual must be Correct/Incorrect"
        assert q["topic"] in TOPICS, f"Q{q['id']}: unknown topic {q['topic']}"
        assert 0 <= q["ai_confidence"] <= 100, f"Q{q['id']}: confidence must be 0-100"
        for key in ("reasoning", "sources"):
            assert q.get(key), f"Q{q['id']}: missing {key}"

    n_correct = sum(q["actual"] == "Correct" for q in QUESTIONS)
    n_incorrect = len(QUESTIONS) - n_correct
    unverified = unverified_ids()

    print(f"Total questions : {len(QUESTIONS)}")
    print(f"Correct         : {n_correct}")
    print(f"Incorrect       : {n_incorrect}")
    print(f"Unverified      : {len(unverified)}  {unverified if unverified else ''}")
    for topic in TOPICS:
        qs = [q for q in QUESTIONS if q["topic"] == topic]
        c = sum(q["actual"] == "Correct" for q in qs)
        print(f"  {topic:<20} {len(qs)} questions  ({c} correct, {len(qs) - c} incorrect)")
    if n_correct != n_incorrect:
        print("WARNING: correct/incorrect counts are not balanced.")


if __name__ == "__main__":
    validate_questions()
