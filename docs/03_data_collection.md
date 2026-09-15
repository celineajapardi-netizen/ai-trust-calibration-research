# Phase 3 — Deployment, Pilot & Data Collection

## 1. Before you deploy — the go-live checklist

- [ ] All 10 questions verified (`python experiment/questions.py` shows `Unverified : 0`)
- [ ] Consent text in `app.py` replaced with the approved wording (docs/02)
- [ ] Supervisor has signed off on ethics
- [ ] `data/responses.csv` deleted (it currently contains **fake** test data)
- [ ] Admin password set (see §2)
- [ ] Pilot test done (§4)

## 2. Setting the admin password

The app has a hidden researcher page at `<your-app-url>/?admin=1` that shows how many people
have started/completed and lets you download the CSV. It needs a password.

**Locally:** create `experiment/.streamlit/secrets.toml` (this file is git-ignored):

```toml
ADMIN_PASSWORD = "choose-something-long"
```

**On Streamlit Community Cloud:** app → Settings → Secrets → paste the same line.

## 3. Deploying to Streamlit Community Cloud (free)

1. Push the project to GitHub (raw data is excluded automatically by `.gitignore`).
2. Go to https://share.streamlit.io → **New app** → pick the repo, branch `main`,
   main file `experiment/app.py`.
3. Add the secret from §2. Deploy. You get a URL like `https://celine-ai-trust.streamlit.app`.
4. Open `<url>/?admin=1` and check the dashboard loads.

**The storage problem, and how to handle it.** Community Cloud's file system is temporary: if the
app restarts (it sleeps after inactivity, or restarts on every git push), `responses.csv` is lost.
Three options, simplest first:

| Option | Effort | When to use |
|--------|--------|-------------|
| **Download often** via the admin page (every day during collection; and **never push to GitHub while collecting**). `analysis.py` merges every `responses*.csv` file it finds in `data/`. | none | Small study, short collection window (1–2 weeks) — probably fine for you |
| **Google Sheets backend** using `st-gsheets-connection`. Replace `save_response()` with a call that appends a row to a sheet. | ~1 hour | If collection runs for weeks or you can't check daily |
| **Run the app on a laptop at school** with participants using it in person. Data stays local. | none | If you're recruiting in a classroom anyway |

If you go with option 1, a good habit: download in the morning and evening and save as
`data/responses_2026-10-03_am.csv`, etc.

## 4. Pilot test (2–3 people, before real recruitment)

Ask each pilot participant to talk out loud while doing it, and note:

- [ ] Was any question wording confusing?
- [ ] Did any "incorrect" answer seem *obviously* wrong (too easy)? Did its reasoning sound convincing?
- [ ] Did any "correct" answer seem suspicious (too hard)?
- [ ] Did they notice that some answers were polished and some plain? Did they guess the purpose?
- [ ] How long did it take? (aim 5–8 min)
- [ ] Any technical glitches — back button, refresh, phone screen size?

Fix, **delete the pilot rows** from the data, then go live. Pilot data is not research data.

## 5. Recruitment message (adapt to taste)

> Hi! I'm doing an independent research project on how people judge information written by AI,
> and I need participants. It's a 5–8 minute anonymous online task — you read 10 short AI
> answers and say whether you think each is right. No sign-up, no personal details.
>
> Link: [URL]
>
> Please don't discuss the questions with others who might do it — it would affect the results.
> Thank you so much!

Where to recruit (convenience sample — say so in the paper):

- your year group / classes (ask a teacher to share the link)
- family and family friends
- clubs, sports teams
- a school newsletter or noticeboard

Aim: **40–60 participants**. Minimum workable: ~30 (the within-subjects design needs far fewer
people than a between-groups design would). If "started" is much higher than "completed" on the
dashboard, people are dropping out mid-way — check whether something is confusing.

## 6. During collection

- Check the dashboard daily; download the CSV.
- Keep a short **log** (date, how many participants, anything unusual, e.g. "shared link with
  Year 12 on 3 Oct"). You'll want this for the Methodology section.
- Don't change questions or wording after the first real participant. If you must, note the
  date and exclude earlier participants for that question.

## 7. Closing collection

1. Final download from the admin page.
2. Merge/clean: `python analysis/analysis.py` prints how many participants were dropped for not
   finishing.
3. Copy the cleaned file to `data/anonymized_results.csv` — open it and confirm there's nothing
   identifying (there shouldn't be — the app never collects any).
4. Take the app offline (Streamlit Cloud → delete app, or just stop sharing the link).
