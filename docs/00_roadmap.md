# Project Roadmap — start here

Everything in this folder is a **draft or scaffold**. The project is yours: read, check, change,
and make decisions. Tick things off as you go.

## Phase 1 — Design & prep  (≈ 2–3 weeks)

| # | Task | Where | Done |
|---|------|-------|------|
| 1 | Read the research design; decide which hypotheses to keep (3–5) | `docs/01_research_design.md` | ☐ |
| 2 | Go through all 10 draft questions. For each: check the fact in a reliable source, write the source in `notes`, set `verified=True`. Check the *reasoning* for the incorrect ones sounds convincing. Swap any you don't like. | `experiment/questions.py` | ☐ |
| 3 | Run `python experiment/questions.py` — must show `Unverified : 0` | terminal | ☐ |
| 4 | Ethics checklist with supervisor; adapt consent + parental consent text | `docs/02_consent_and_ethics.md` | ☐ |
| 5 | Paste approved consent text into the app | `experiment/app.py` → `screen_consent()` | ☐ |
| 6 | Start the reading log: one line per paper | `paper/reading_list.md` | ☐ |

## Phase 2 — Build  (≈ 1 week, mostly done)

| # | Task | Where | Done |
|---|------|-------|------|
| 7 | Run the app locally and click through it a few times — check both the polished and plain styles look right (open a new private window for each new participant) | `python3 -m streamlit run experiment/app.py` | ☐ |
| 8 | Set the admin password; check `/?admin=1` works | `experiment/.streamlit/secrets.toml` | ☐ |
| 9 | Take screenshots of a polished and a plain question for Appendix B | `paper/` | ☐ |
| 10 | Put the project on GitHub (from your own laptop, your own account) | `README.md` has the commands | ☐ |
| 11 | Deploy to Streamlit Community Cloud | `docs/03_data_collection.md` §3 | ☐ |

## Phase 3 — Pilot & collect  (≈ 2–3 weeks)

| # | Task | Where | Done |
|---|------|-------|------|
| 12 | Delete the fake `data/responses.csv` | `data/` | ☐ |
| 13 | Pilot with 2–3 people; fix issues; delete pilot rows | `docs/03` §4 | ☐ |
| 14 | Send recruitment message; keep a collection log | `docs/03` §5–6 | ☐ |
| 15 | Download data daily from the admin page | `data/responses_<date>.csv` | ☐ |
| 16 | Close collection at 40–60 (min ~30); final download | | ☐ |

## Phase 4 — Analyse  (≈ 1 week)

| # | Task | Where | Done |
|---|------|-------|------|
| 17 | `python analysis/analysis.py` — read the printed output and `results_summary.md` | `analysis/` | ☐ |
| 18 | Look at each graph and write **one sentence** about what it shows, before reading any stats | `analysis/graphs/` | ☐ |
| 19 | For each hypothesis: supported / partly / not? | | ☐ |
| 20 | Copy cleaned data to `data/anonymized_results.csv` | | ☐ |
| 21 | Optional extras: which single question fooled most people when polished | `summary_by_question.csv` | ☐ |

## Phase 5 — Write up  (≈ 3–4 weeks)

| # | Task | Where | Done |
|---|------|-------|------|
| 22 | Write Methodology first (easiest), then Results, Discussion, Intro, Abstract | `paper/paper_template.md` | ☐ |
| 23 | Literature review from your reading log | | ☐ |
| 24 | `python analysis/export_question_bank.py` → Appendix A | `paper/appendix_a_question_bank.md` | ☐ |
| 25 | Supervisor feedback → revise | | ☐ |
| 26 | Export to PDF as `paper/AI_Trust_Research.pdf`; finish README; push to GitHub | | ☐ |
| 27 | CV line + personal-statement paragraph | below | ☐ |

## CV line (edit once you have results)

> **Independent Research — AI Trust & Information Evaluation** (2026)
> Designed and conducted a 2 × 2 within-subjects experiment (N = __) investigating whether
> confidence scores, reasoning and cited sources inflate trust in AI answers independently of
> their accuracy.
> Built the experimental platform in Python/Streamlit, collected anonymised responses, and analysed
> judgment accuracy, trust and reliance using pandas and non-parametric statistics. Found that
> [one-sentence headline result].

## Rough timeline

Phase 1 → 2 → 3 → 4 → 5 is about **10–12 weeks** if you do a few hours a week. The two things
that can't be rushed are ethics sign-off (Phase 1) and data collection (Phase 3) — start those early.
