"""
AI Trust Experiment - Streamlit app

Flow:  Welcome -> Consent -> Participant ID -> 10 questions -> Thank you

Design: every participant sees all 10 questions. Five are shown "polished"
(answer + confidence + reasoning + sources) and five "plain" (answer only).
Which five is randomised per participant - see assign_presentation().

Run locally with:
    python -m streamlit run experiment/app.py      (python3 on Mac)

Researcher dashboard:  <app-url>/?admin=1
"""
from __future__ import annotations

import csv
import os
import random
import string
from datetime import datetime, timezone

import streamlit as st

from questions import QUESTIONS, unverified_ids

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

STUDY_TITLE = "How Do People Judge AI Answers?"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
RESPONSES_FILE = os.path.join(DATA_DIR, "responses.csv")

CSV_COLUMNS = [
    "participant_id",
    "position",        # 1..10, the order this participant saw the question in
    "question_id",
    "topic",
    "actual",          # answer key: Correct / Incorrect (never shown to participant)
    "presentation",    # polished / plain
    "judgment",        # participant: Correct / Incorrect / Unsure
    "confidence",      # 1-5
    "trust",           # 1-5
    "reliance",        # Yes / No / Unsure
    "timestamp_utc",
]

PRESENTATIONS = {
    "polished": "AI answer + confidence score + reasoning + sources",
    "plain": "AI answer only",
}

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def generate_participant_id() -> str:
    """Anonymous ID like P482731 - no personal information."""
    return "P" + "".join(random.choices(string.digits, k=6))


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CSV_COLUMNS).writeheader()


def assign_presentation() -> dict:
    """
    Decide which questions this participant sees polished and which plain.

    Half of the questions are polished. To keep the 2x2 balanced we split the
    polished slots between correct and incorrect answers as evenly as possible
    (e.g. with 5 correct / 5 incorrect: 3+2 or 2+3, chosen at random).
    Returns {question_id: "polished" | "plain"}.
    """
    correct = [q["id"] for q in QUESTIONS if q["actual"] == "Correct"]
    incorrect = [q["id"] for q in QUESTIONS if q["actual"] == "Incorrect"]
    random.shuffle(correct)
    random.shuffle(incorrect)

    n_polished = len(QUESTIONS) // 2
    n_from_correct = n_polished // 2 + (random.randint(0, 1) if n_polished % 2 else 0)
    n_from_correct = min(n_from_correct, len(correct))
    n_from_incorrect = min(n_polished - n_from_correct, len(incorrect))

    polished = set(correct[:n_from_correct] + incorrect[:n_from_incorrect])
    return {q["id"]: ("polished" if q["id"] in polished else "plain") for q in QUESTIONS}


def save_response(row: dict):
    ensure_data_file()
    with open(RESPONSES_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CSV_COLUMNS).writerow(row)


def init_state():
    if "stage" not in st.session_state:
        st.session_state.stage = "welcome"
        st.session_state.participant_id = None
        st.session_state.presentation = {}   # question_id -> polished/plain
        st.session_state.order = []          # shuffled list of question dicts
        st.session_state.q_index = 0


def go(stage: str):
    st.session_state.stage = stage
    st.rerun()


def admin_password() -> str | None:
    """Admin password from Streamlit secrets or the ADMIN_PASSWORD env var."""
    try:
        if "ADMIN_PASSWORD" in st.secrets:
            return st.secrets["ADMIN_PASSWORD"]
    except Exception:
        pass
    return os.environ.get("ADMIN_PASSWORD")


# --------------------------------------------------------------------------- #
# Admin dashboard
# --------------------------------------------------------------------------- #


def screen_admin():
    """Researcher-only page: open the app with ?admin=1 in the URL."""
    st.title("Researcher dashboard")
    pw = admin_password()
    if not pw:
        st.error(
            "No admin password is set. Add ADMIN_PASSWORD to experiment/.streamlit/secrets.toml "
            "(see secrets.toml.example) or set the ADMIN_PASSWORD environment variable, then restart."
        )
        return
    entered = st.text_input("Password", type="password")
    if entered != pw:
        st.info("Enter the admin password to view the dashboard.")
        return

    if not os.path.exists(RESPONSES_FILE):
        st.warning("No responses yet.")
        return

    import pandas as pd

    df = pd.read_csv(RESPONSES_FILE)
    per_p = df.groupby("participant_id")["question_id"].nunique()
    n_started = len(per_p)
    n_complete = int((per_p == len(QUESTIONS)).sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Started", n_started)
    c2.metric("Completed", n_complete)
    c3.metric("Rows", len(df))

    st.subheader("Responses per cell (actual × presentation)")
    cell = df.pivot_table(index="actual", columns="presentation", values="participant_id",
                          aggfunc="count", fill_value=0)
    st.dataframe(cell, use_container_width=True)

    st.subheader("Download data")
    with open(RESPONSES_FILE, "rb") as f:
        st.download_button(
            "Download responses.csv",
            f.read(),
            file_name=f"responses_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv",
        )
    st.caption(
        "On Streamlit Community Cloud the file is wiped when the app restarts - "
        "download it regularly and keep the copies in data/; analysis.py merges them."
    )


# --------------------------------------------------------------------------- #
# Participant screens
# --------------------------------------------------------------------------- #


def screen_welcome():
    st.title(STUDY_TITLE)
    if unverified_ids():
        st.warning(
            f"**Researcher note - not ready for real participants.** "
            f"{len(unverified_ids())} question(s) have not been verified yet "
            f"(ids {unverified_ids()}). Check each fact and set `verified=True` in questions.py. "
            "This banner disappears automatically once all are verified."
        )
    st.markdown(
        f"""
        Thank you for your interest in this study.

        You will be shown **{len(QUESTIONS)} short factual questions**, each with an answer written by
        an AI assistant. Sometimes the AI also shows how confident it is and explains its reasoning;
        sometimes it just gives the answer. For each one, you'll be asked whether you think the
        answer is correct and how much you would trust it.

        - It takes about **5-8 minutes**.
        - There are no right or wrong ways to respond - we want your honest judgment.
        - Please **do not look anything up** while taking part.

        Click **Next** to read the consent information.
        """
    )
    if st.button("Next", type="primary"):
        go("consent")


def screen_consent():
    st.title("Consent")
    st.markdown(
        """
        **TODO: replace this with the consent wording approved by your teacher/supervisor
        (see docs/02_consent_and_ethics.md).**

        - Participation is voluntary. You can stop at any time by closing this page.
        - Your responses are **anonymous**. We do not collect your name, email or any personal details.
          You will be given a random ID such as *P482731*.
        - The anonymised data will be used for an independent student research project and may be
          published in a report and on GitHub.
        - If you are under 16, please make sure a parent or guardian is happy for you to take part.
        """
    )
    agree = st.checkbox("I have read the information above and I agree to take part.")
    if st.button("Continue", type="primary", disabled=not agree):
        go("assign")


def screen_assign():
    """Assign an ID + presentation styles, shuffle the questions, then show the ID."""
    if st.session_state.participant_id is None:
        st.session_state.participant_id = generate_participant_id()
        st.session_state.presentation = assign_presentation()
        order = list(QUESTIONS)
        random.shuffle(order)
        st.session_state.order = order
        st.session_state.q_index = 0

    st.title("Your participant ID")
    st.markdown("Your anonymous participant ID is:")
    st.markdown(f"## `{st.session_state.participant_id}`")
    st.markdown(
        "You don't need to remember it, but you can write it down if you might want to ask "
        "for your responses to be removed later."
    )
    if st.button("Start the questions", type="primary"):
        go("experiment")


def render_ai_answer(q: dict, presentation: str):
    st.markdown("#### Question")
    st.markdown(f"**{q['question']}**")

    st.markdown("#### AI assistant's answer")
    with st.container(border=True):
        st.markdown(f"🤖 {q['ai_answer']}")

        if presentation == "polished":
            st.markdown(f"**Confidence:** {q['ai_confidence']}%")
            st.markdown("**Reasoning**")
            st.markdown(q["reasoning"])
            st.markdown("**Sources**")
            st.markdown(q["sources"])


def screen_experiment():
    order = st.session_state.order
    i = st.session_state.q_index
    total = len(order)

    if i >= total:
        go("done")
        return

    q = order[i]
    presentation = st.session_state.presentation[q["id"]]

    st.progress(i / total, text=f"Question {i + 1} of {total}")
    render_ai_answer(q, presentation)

    st.markdown("#### Your judgment")
    with st.form(key=f"form_{q['id']}", clear_on_submit=True):
        judgment = st.radio(
            "1. Is the AI's answer correct?",
            ["Correct", "Incorrect", "Unsure"],
            index=None,
            horizontal=True,
        )
        confidence = st.radio(
            "2. How confident are you in your judgment?  (1 = Not confident, 5 = Very confident)",
            [1, 2, 3, 4, 5],
            index=None,
            horizontal=True,
        )
        trust = st.radio(
            "3. How trustworthy is the AI's answer?  (1 = Not trustworthy, 5 = Very trustworthy)",
            [1, 2, 3, 4, 5],
            index=None,
            horizontal=True,
        )
        reliance = st.radio(
            "4. Would you use this answer to make a decision?",
            ["Yes", "No", "Unsure"],
            index=None,
            horizontal=True,
        )
        submitted = st.form_submit_button("Next question", type="primary")

    if submitted:
        if None in (judgment, confidence, trust, reliance):
            st.warning("Please answer all four questions before continuing.")
            return

        save_response(
            {
                "participant_id": st.session_state.participant_id,
                "position": i + 1,
                "question_id": q["id"],
                "topic": q["topic"],
                "actual": q["actual"],
                "presentation": presentation,
                "judgment": judgment,
                "confidence": confidence,
                "trust": trust,
                "reliance": reliance,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        )
        st.session_state.q_index += 1
        st.rerun()


def screen_done():
    st.title("Thank you! 🎉")
    st.markdown(
        f"""
        You have completed the study. Your responses have been recorded under ID
        `{st.session_state.participant_id}`.

        **What was this study about?**
        Half of the AI answers you saw were correct and half were subtly incorrect. Some answers
        came with a confidence score, reasoning and sources; others were shown on their own. The
        study looks at whether those extra signals make people trust an answer more - even when it
        is wrong - and whether a plain answer is trusted less, even when it is right.

        Please **don't share the questions** with other people who might take part, so that their
        responses stay fair.

        You can now close this page.
        """
    )


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main():
    st.set_page_config(page_title=STUDY_TITLE, page_icon="🤖", layout="centered")
    init_state()

    if st.query_params.get("admin") == "1":
        screen_admin()
        return

    stage = st.session_state.stage
    if stage == "welcome":
        screen_welcome()
    elif stage == "consent":
        screen_consent()
    elif stage == "assign":
        screen_assign()
    elif stage == "experiment":
        screen_experiment()
    elif stage == "done":
        screen_done()


if __name__ == "__main__":
    main()
