# Phase 1 — Consent & Ethics Pack

> **Status:** DRAFT templates. Your school may have its own forms or wording — if so, use theirs.
> Get your supervisor's written OK **before** the first real participant.

## A. Ethics checklist (go through this with your supervisor)

| # | Question | Answer / decision |
|---|----------|-------------------|
| 1 | Does the school require a formal ethics approval form for student research? | |
| 2 | Minimum participant age? (Suggest 13+; some schools require 16+ without parental consent) | |
| 3 | Is parental/guardian consent required for participants under 16 / 18? | |
| 4 | Confirmed: **no** names, emails, dates of birth or free-text boxes are collected | ✅ built into the app |
| 5 | Confirmed: participants can stop at any time by closing the page | ✅ stated in consent |
| 6 | Where will `responses.csv` be stored? Who can access it? | e.g. only on Celine's laptop + one backup; not on GitHub |
| 7 | How long will raw data be kept? | e.g. until the paper is finished + 1 year |
| 8 | Can a participant ask for their data to be deleted? How? | Yes — they quote their ID (e.g. P482731) and you delete those rows |
| 9 | Any risk of harm or distress? | Minimal — general-knowledge questions; no sensitive topics |
| 10 | Deception? | Mild: participants aren't told in advance which answers are wrong, and the reasoning/sources shown with incorrect answers are written to look convincing. They **are** told afterwards (debrief). Standard for this kind of study — mention it to your supervisor explicitly. |
| 11 | Is the debrief acceptable? (see section D) | |
| 12 | Are teachers / school name mentioned anywhere public? Should they be? | |

## B. Participant information sheet (shown on the Consent screen)

Replace the placeholder text in `app.py` → `screen_consent()` with this once approved.

---

**Study title:** How Do People Judge AI Answers?

**Who is running this study?** This is an independent research project by a student at
[School name], supervised by [Supervisor name]. Contact: [school email address].

**What is it about?** The study looks at how people judge information written by AI systems.

**What will I do?** You will see 10 short factual questions, each with an answer written by an AI.
For each one you'll say whether you think the answer is correct, how confident you are, and how
much you trust the answer. It takes about 5–8 minutes. Please don't look anything up.

**Do I have to take part?** No. It's completely voluntary. You can stop at any time by closing the
page, and there is no penalty for stopping.

**Is it anonymous?** Yes. We do not ask for your name, email or any personal details. You'll be
given a random ID like *P482731*. Nobody — including the researcher — can link your answers to you.

**What happens to my answers?** They are stored securely and used only for this project. The
anonymised results will be written up in a research report and may be published on GitHub.

**Can I withdraw my answers later?** Yes. Note your participant ID and email [school email address]
within [two weeks] — we'll delete your rows.

**Under 16?** Please make sure a parent or guardian is happy for you to take part before continuing.

---

**Consent statement (the checkbox):**

> ☐ I have read the information above. I understand that taking part is voluntary and anonymous,
> and I agree to take part.

## C. Parental / guardian consent (if required)

If the school requires it, use a short paper or Google Form **separate from the experiment**, so
that no names end up in the research data:

---

Dear Parent/Guardian,

Your child has been invited to take part in a short (5–8 minute) online study run by a student at
[School] as part of an independent research project supervised by [Supervisor]. The study asks
participants to judge whether answers written by an AI system are correct. It is anonymous — no
names or personal details are collected — and your child may stop at any time.

☐ I give permission for my child to take part.

Parent/guardian name: ____________  Signature: ____________  Date: ________

---

Keep signed forms in a folder at school; they are **never** linked to participant IDs.

## D. Debrief (shown on the Thank-you screen — already in `app.py`)

> Half of the AI answers you saw were correct and half were subtly incorrect. Some answers came
> with a confidence score, reasoning and sources; others were shown on their own. The study looks
> at whether those extra signals make people trust an answer more — even when it is wrong — and
> whether a plain answer is trusted less, even when it is right.
> Please don't share the questions with other people who might take part.

Optional addition (ask supervisor): a link to a page listing which answers were wrong, so
participants leave with the correct facts. Good practice, but only if you're confident
participants won't share it before data collection ends.

## E. Data-handling rules for yourself

1. `data/responses.csv` never goes on GitHub (already in `.gitignore`). Only
   `data/anonymized_results.csv` is published, after you've checked it.
2. Keep one backup copy (e.g. a USB stick or a private cloud folder). Not in a shared folder.
3. If anyone asks to withdraw, delete every row with their participant ID and note the date.
4. When the project is completely finished, delete the raw file according to the retention period
   you agreed in the checklist.
