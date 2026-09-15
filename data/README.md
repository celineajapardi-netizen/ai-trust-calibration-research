# Data

- `responses.csv` — raw responses written by the Streamlit app (one row per question answered).
  This file is git-ignored. Keep it private.
- `anonymized_results.csv` — the cleaned dataset you publish with the paper
  (copy `responses.csv` here once collection is finished and you have checked it contains
  no personal information).

## Columns

| column          | meaning                                                            |
|-----------------|--------------------------------------------------------------------|
| participant_id  | anonymous ID, e.g. P482731                                          |
| position        | 1–10, the order the participant saw the question in                 |
| question_id     | id from `experiment/questions.py`                                   |
| topic           | Science / Computer Science / History / Geography / Environment       |
| actual          | **answer key** – Correct / Incorrect (never shown to participants)  |
| presentation    | polished (answer + confidence + reasoning + sources) / plain (answer only) |
| judgment        | participant: Correct / Incorrect / Unsure                           |
| confidence      | participant confidence in own judgment, 1–5                         |
| trust           | how trustworthy the AI answer seemed, 1–5                           |
| reliance        | would they use the answer to make a decision: Yes / No / Unsure     |
| timestamp_utc   | when the response was submitted                                     |
