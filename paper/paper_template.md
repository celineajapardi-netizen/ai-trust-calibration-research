# When Should We Trust AI? Investigating Trust Calibration in AI-Generated Information

**Author:** [Your name]
**School:** [School name]
**Supervisor:** [Name]
**Date:** [Month Year]

> **How to use this template.** Each section has (a) what it should contain, (b) a rough length,
> and (c) *prompts in italics* to answer. Delete the guidance as you write. Target length for the
> whole paper: 3,000–5,000 words plus figures. Write the Methodology first (it's the easiest — you
> already know exactly what you did), then Results, then Discussion, then Introduction, and the
> Abstract last.

---

## Abstract

*~200 words. One or two sentences each on: the problem, what you did, the main finding, why it
matters. Write it last.*

---

## 1. Introduction

*~400 words.*

- *Why are people increasingly getting information from AI systems?*
- *What is the risk when an AI answer is wrong but sounds confident? Give one concrete example
  (you could use one of your own incorrect questions, e.g. "212 bones").*
- *What do AI products actually show users today — confidence scores? citations? nothing? —
  and does anyone know whether those signals help?*
- *State in one sentence what this study does.*

## 2. Literature Review

*~800 words. This is where you show you've read what others found. See `paper/reading_list.md`
for a starting set. Organise by theme, not by paper:*

**2.1 Trust and reliance on automation.** *The classic work (Lee & See, 2004; Parasuraman &
Riley, 1997) — trust should be "calibrated" to a system's real capability; over-trust = misuse,
under-trust = disuse. Define calibration here.*

**2.2 Algorithm aversion vs. algorithm appreciation.** *Do people trust algorithms too little
(Dietvorst et al., 2015) or too much (Logg et al., 2019)? Both happen, depending on context.*

**2.3 Confidence displays and explanations.** *Zhang, Liao & Bellamy (2020) found showing
confidence helped calibration in some cases; Bansal et al. (2021) found explanations increased
reliance even when the AI was wrong; Buçinca et al. (2021) on "cognitive forcing".*

**2.4 Uncertainty language in large language models.** *Recent work on whether LLMs expressing
uncertainty ("I'm not sure, but…") reduces over-reliance (Kim et al., 2024; Steyvers et al.,
2025).*

**2.5 Sources and citations.** *Do citations make people trust an answer more even if they don't
check them? (Look for work on "citation as a credibility cue".)*

## 3. Research Gap

*~150 words. Most prior work uses expert decision tasks (medical, loan approval) or lab
participants. Less is known about (a) everyday factual questions, (b) the combined effect of a
confidence number + reasoning + sources presented together, the way chat assistants actually show
them, and (c) the mirror-image question of whether a plain correct answer is *under*-trusted. Say
clearly which of these your study addresses.*

## 4. Research Question

> Do the presentation signals that make an AI answer look trustworthy — a confidence score,
> reasoning and cited sources — change how much people trust it, independently of whether the
> answer is actually correct?

## 5. Hypotheses

*Copy from `docs/01_research_design.md` — the ones you finally chose. Number them H1, H2… and
refer back to them by number in Results and Discussion.*

## 6. Methodology

*~800 words. Enough detail that someone could repeat the study.*

**6.1 Design.** *2 × 2 within-subjects experiment: correctness (correct / incorrect) × presentation
(polished / plain), presentation counterbalanced across participants; dependent variables (judgment
accuracy, trust, confidence, reliance, trust gap). Table of the four cells.*

**6.2 Participants.** *How many started, how many completed (from `analysis/results_summary.md`). How recruited (convenience sample — school, family). Age range if
known. Ethics: consent, anonymity, supervisor approval.*

**6.3 Materials.** *10 questions, five topics, 5 correct / 5 incorrect; how the AI answers were
generated and verified; how the "subtly incorrect" answers were designed; how the reasoning and
sources were written (and made plausible for incorrect answers). Put the full question bank in
Appendix A.*

**6.4 Procedure.** *Welcome → consent → ID → 10 questions in random order → debrief. What
participants answered for each question. Duration. Instruction not to look things up.*

**6.5 Platform.** *Python + Streamlit web app; per-participant randomisation of presentation style; data stored as CSV.
Link to the GitHub repository.*

**6.6 Analysis.** *pandas; descriptive statistics per cell; Wilcoxon signed-rank tests (paired
within participant) for polished vs plain on incorrect answers (H1), correct answers (H2), error
detection (H3) and trust gap (H4); Spearman correlation for confidence vs accuracy (H5). Say why
non-parametric tests (ratings are ordinal; small sample).*

## 7. Results

*~800 words + 4–5 figures. Report, don't interpret (interpretation goes in Discussion). Take the
numbers straight from `analysis/results_summary.md`.*

**7.1 Trust by cell** — Graph 1 (the key graph). *Mean trust in each of the four cells. H1: did
polish raise trust in wrong answers? H2: did plainness lower trust in right answers?*

**7.2 Judgment accuracy** — Graph 2. *Accuracy per cell; H3: were polished errors detected less
often?*

**7.3 Over-trust, under-trust and calibration** — Graph 4. *Rates per style; trust gap per style
(H4).*

**7.4 Reliance** — Graph 3. *"Would you use this answer?" — especially polished-incorrect vs
plain-correct.*

**7.5 Confidence vs accuracy** — Graph 5 (H5).

**7.6 Per question (optional)** — Graph 6. *Which question fooled the most people when polished?*

*For each hypothesis: "H1 was supported / partially supported / not supported."*

## 8. Discussion

*~700 words. Now interpret.*

- *What is the single most important finding? Say it in the first sentence.*
- *Did polish inflate trust in wrong answers (H1)? What does that mean for products that show
  confidence scores and citations?*
- *Were plain correct answers under-trusted (H2)? Is that a problem, or healthy scepticism?*
- *Did the reasoning make errors harder to spot (H3)? Did anyone seem to actually read it?*
- *Which matters more to people — what the answer says, or how it's dressed up (H4)?*
- *How do your results compare with the literature in Section 2? Agree? Disagree? Why might that
  be (different task, participants, population)?*
- *Practical implications: what should an AI interface show?*

## 9. Limitations

*~300 words. Be honest and specific; examiners like this section.*

- *Convenience sample — mostly [students aged X–Y]; not representative.*
- *Sample size — N = __; limited statistical power. Only 10 questions, so each cell has only 2–3 items per participant.*
- *Questions were general-knowledge; results may differ for specialist or high-stakes decisions.*
- *The "AI answers" were presented as text; no interaction, no chance to ask follow-ups.*
- *Confidence values and evidence were designed by the researcher, not generated by a real model.*
- *Self-reported trust vs real behaviour.*
- *Participants may have noticed the two styles and guessed the purpose of the study.*

## 10. Conclusion

*~200 words. Restate the question, the answer your data gives, one implication, one direction for
future work (e.g. real LLM outputs, a larger sample, a version where participants can check the
sources).*

## References

*Use one consistent style (APA 7 is standard for this field). Only cite things you've actually
read at least the abstract of. See `reading_list.md`.*

## Appendix A — Question bank

*Table: id, topic, question, AI answer, actual correctness. (Export from `questions.py`.)*

## Appendix B — Screenshots of a polished and a plain question

## Appendix C — Consent text and debrief
