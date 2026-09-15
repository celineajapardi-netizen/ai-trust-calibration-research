# When Should We Trust AI?

**Investigating Trust Calibration in AI-Generated Information** — an independent research project.

AI systems can sound extremely confident even when they are wrong. This study asks whether the
signals that make an AI answer *look* trustworthy — a **confidence score**, **reasoning** and
**cited sources** — change how much people trust it, independently of whether it is actually
correct.

## Research question

> When an AI sounds confident and shows its sources, do people believe it even when it's wrong?
> And when it gives a plain answer, do they doubt it even when it's right?

## How the experiment works

Every participant answers the same **10 questions** — 5 with a correct AI answer and 5 with a
subtly incorrect one. Each question is shown in one of two styles, randomised per participant so
that everyone sees 5 of each:

| Style        | What participants see                                              |
|--------------|--------------------------------------------------------------------|
| **Polished** | AI answer + "Confidence: 96%" + a paragraph of reasoning + sources |
| **Plain**    | AI answer only                                                     |

That gives a 2 × 2 design:

|                  | Polished                         | Plain                              |
|------------------|----------------------------------|------------------------------------|
| **AI correct**   | control                          | **under-trust test** (true, no evidence) |
| **AI incorrect** | **over-trust test** (looks trustworthy, but false) | control          |

For every question, participants report: is the answer correct? (Correct / Incorrect / Unsure),
confidence in that judgment (1–5), trust in the AI answer (1–5), and whether they would use the
answer to make a decision (Yes / No / Unsure).

## Project structure

```
AI-Trust-Research/
├── docs/
│   ├── 00_roadmap.md             # START HERE - every task, all phases
│   ├── 01_research_design.md     # research question, hypotheses, variables
│   ├── 02_consent_and_ethics.md  # ethics checklist, consent + parental templates, debrief
│   └── 03_data_collection.md     # deployment, pilot, recruitment, storage
├── experiment/
│   ├── app.py                    # Streamlit app participants use (+ hidden /?admin=1 dashboard)
│   ├── questions.py              # question bank + answer key (never shown to participants)
│   └── .streamlit/secrets.toml.example
├── data/
│   ├── responses*.csv            # raw responses (git-ignored, private)
│   └── anonymized_results.csv    # published dataset
├── analysis/
│   ├── analysis.py               # 2x2 analysis, paired statistical tests, graphs, results_summary.md
│   ├── make_fake_data.py         # generates fake data to test the analysis
│   ├── export_question_bank.py   # -> paper/appendix_a_question_bank.md
│   └── graphs/
├── paper/
│   ├── paper_template.md         # section-by-section writing guide
│   ├── reading_list.md           # literature review starting points
│   └── AI_Trust_Research.pdf     # final paper
└── README.md
```

## Running it

```bash
pip install -r requirements.txt
```

Run the experiment locally:

```bash
streamlit run experiment/app.py
```

Check the question bank is complete and balanced:

```bash
python experiment/questions.py
```

Run the analysis (after collecting data, or after `python analysis/make_fake_data.py` to test):

```bash
python analysis/analysis.py
```

## Deploying so participants can use a link

The simplest option is [Streamlit Community Cloud](https://streamlit.io/cloud) (free):
push this repo to GitHub, connect it, and point it at `experiment/app.py`.

**Important:** on Community Cloud the local `data/responses.csv` is wiped whenever the app
restarts. Before real data collection either (a) download the CSV regularly, or (b) switch
`save_response()` in `app.py` to write to a Google Sheet (the `st-gsheets-connection` package)
or another persistent store.

## Ethics

Participation is voluntary and anonymous. No names, emails or personal information are collected;
participants receive a random ID such as `P482731`. Consent wording and any parental-consent
requirements are checked with the school supervisor before data collection.

## Researcher dashboard

Open `<app-url>/?admin=1` and enter the admin password (set in `experiment/.streamlit/secrets.toml`,
see the `.example` file) to see how many participants have completed and download the data.

## Where to start

Read `docs/00_roadmap.md` — it lists every task in order with a checkbox.
