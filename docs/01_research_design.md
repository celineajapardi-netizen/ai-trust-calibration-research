# Phase 1 — Research Design

> **Status:** DRAFT. Read it, argue with it, and rewrite anything you disagree with. These are
> proposals, not decisions. Your supervisor may want changes.

## 1. Research question

**Main question**

> Do the *presentation signals* that make an AI answer look trustworthy — a confidence score,
> reasoning and cited sources — change how much people trust it, independently of whether the
> answer is actually correct?

**Plain-English version (for the website / README)**

> When an AI sounds confident and shows its sources, do people believe it even when it's wrong?
> And when it just gives a plain answer, do they doubt it even when it's right?

## 2. Key concept: trust calibration

*Trust* on its own is not the interesting variable. What matters is whether trust **tracks
accuracy**:

| AI answer is… | Participant trust | What we call it            |
|---------------|-------------------|----------------------------|
| Correct       | High              | Appropriate trust ✅        |
| Incorrect     | Low               | Appropriate distrust ✅     |
| Incorrect     | High              | **Over-trust** ❌ (the dangerous one) |
| Correct       | Low               | **Under-trust** ❌          |

A person is *well calibrated* if their trust in correct answers is clearly higher than their trust
in incorrect answers. In `analysis.py` this is the **trust gap**:

```
trust_gap = mean_trust(correct answers) − mean_trust(incorrect answers)
```

Bigger gap = better calibration. If the gap shrinks when answers are polished, the polish is
raising trust *regardless* of whether the AI is right.

## 3. The design: 2 × 2, within-subjects

Every participant answers the **same 10 questions** (5 with a correct AI answer, 5 with a subtly
incorrect one). Each question is shown in one of two **presentation styles**:

| Style        | What the participant sees                                          |
|--------------|--------------------------------------------------------------------|
| **Polished** | AI answer + "Confidence: 96%" + a paragraph of reasoning + sources |
| **Plain**    | AI answer only                                                     |

For each participant, 5 questions are polished and 5 are plain, chosen at random (with the polished
slots split between correct and incorrect answers as evenly as possible). Across the whole study,
every question appears in both styles about equally often — this is called **counterbalancing**,
and it means differences between styles can't be explained by some questions just being harder.

That gives four cells:

|                  | Polished                              | Plain                                   |
|------------------|---------------------------------------|-----------------------------------------|
| **AI correct**   | control                               | **Under-trust test** — true, but no evidence |
| **AI incorrect** | **Over-trust test** — looks trustworthy, but false | control              |

Why within-subjects (everyone sees both styles) rather than separate groups?

- Each participant acts as their own control, so individual differences (some people trust AI more
  in general) cancel out. That makes the tests much more sensitive with a small sample.
- You can use *paired* statistical tests, which need far fewer participants — 30–40 is genuinely
  enough here, versus 75–100 for a between-groups design.
- It's simpler to explain in the paper.

The one risk: participants might notice that some answers are polished and some aren't, and guess
the purpose. Randomising the order helps. You can ask about this in the debrief ("What did you
think the study was about?") — optional.

## 4. Hypotheses

Write these as predictions you can be **wrong** about. Whatever the data says goes in the Results.

- **H1 (Over-trust).** For *incorrect* AI answers, trust will be higher when the answer is
  polished than when it is plain.
- **H2 (Under-trust).** For *correct* AI answers, trust will be lower when the answer is plain
  than when it is polished.
- **H3 (Error detection).** Participants will identify *incorrect* answers as incorrect less often
  when they are polished than when they are plain — i.e. the polish makes errors harder to spot.
- **H4 (Calibration).** The trust gap (correct − incorrect) will be *smaller* in the polished style
  than in the plain style — polish raises trust across the board rather than helping people tell
  right from wrong.
- **H5 (Self-confidence).** Participants' confidence in their own judgment will be only weakly
  related to whether that judgment was actually correct.

> Optional: keep just H1, H2 and H4 if your supervisor wants a shorter paper. Three clear
> hypotheses are better than five vague ones.

## 5. Variables

**Independent variables (manipulated):**

- *Correctness* of the AI answer — Correct / Incorrect (fixed per question; answer key)
- *Presentation* — polished / plain (randomised per participant per question)

**Controlled:** the same 10 questions and AI answers for everyone; question order randomised;
5 correct / 5 incorrect; two questions per topic (one of each).

**Dependent variables (measured per question):**

| Variable        | Measure                                              | Column       |
|-----------------|------------------------------------------------------|--------------|
| Judgment accuracy | judgment == actual (Unsure counts as incorrect)    | `judged_correctly` |
| Trust           | 1–5 rating                                            | `trust`      |
| Self-confidence | 1–5 rating                                            | `confidence` |
| Reliance        | "Would you use this to make a decision?" Yes/No/Unsure | `reliance` |
| Over-trust      | actual == Incorrect **and** trust ≥ 4                 | `over_trust` |
| Under-trust     | actual == Correct **and** trust ≤ 2                   | `under_trust`|
| Missed error    | actual == Incorrect **and** judgment == Correct       | `missed_error` |
| Trust gap       | mean trust(correct) − mean trust(incorrect), per participant per style | (stats) |

## 6. Design summary (for the Methodology section)

- **Design:** 2 (correctness: correct / incorrect) × 2 (presentation: polished / plain)
  within-subjects experiment, with presentation counterbalanced across participants.
- **Participants:** convenience sample, target **40–60** (minimum ~30), aged 13+ (check with
  supervisor).
- **Materials:** 10 factual questions across five topics, each with an AI-generated answer
  (5 verified correct, 5 verified subtly incorrect), a confidence value (92–98%), a paragraph of
  AI reasoning and two cited sources. For incorrect answers the reasoning and sources were written
  to be plausible.
- **Procedure:** information → consent → anonymous ID → 10 questions in random order → debrief.
  ~5–8 minutes. Participants asked not to look anything up.
- **Analysis:** descriptive statistics per cell; Wilcoxon signed-rank tests (paired, within
  participant) for H1–H4; Spearman correlation for H5. (All in `analysis/analysis.py`.)

## 7. Things to decide with your supervisor

- [ ] Minimum participant age and whether parental consent is needed
- [ ] Whether the debrief should reveal which answers were wrong (good practice, but means
      participants must not share the answers with others)
- [ ] Whether to add one optional question at the end: "What did you think the study was about?"
- [ ] Whether to collect *any* demographics (e.g. "how often do you use AI tools?"). One optional
      question could make a nice extra graph, but keep it anonymous.
- [ ] How long you'll keep the raw data and where it will be stored
