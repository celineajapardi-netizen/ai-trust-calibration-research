"""
Analysis of the AI Trust experiment data (2 x 2 within-subjects design).

    rows   : actual        = Correct / Incorrect   (answer key)
    cols   : presentation  = polished / plain

Reads  : every data/responses*.csv  (duplicates from repeated downloads are removed)
Writes : analysis/summary_by_cell.csv
         analysis/summary_by_question.csv
         analysis/results_summary.md      <- numbers + test results, ready to quote in the paper
         analysis/graphs/*.png

Run with:
    python analysis/analysis.py        (python3 on Mac)
"""
from __future__ import annotations

import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")  # save to files, don't open windows
import matplotlib.pyplot as plt
import pandas as pd

try:
    from scipy import stats
    HAVE_SCIPY = True
except ImportError:  # pragma: no cover
    HAVE_SCIPY = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_DIR = os.path.join(OUT_DIR, "graphs")

sys.path.insert(0, os.path.join(ROOT, "experiment"))
from questions import QUESTIONS  # noqa: E402

N_QUESTIONS = len(QUESTIONS)
CELLS = [("Correct", "polished"), ("Correct", "plain"), ("Incorrect", "polished"), ("Incorrect", "plain")]
CELL_LABELS = {
    ("Correct", "polished"): "Correct + polished\n(control)",
    ("Correct", "plain"): "Correct + plain\n(under-trust test)",
    ("Incorrect", "polished"): "Incorrect + polished\n(over-trust test)",
    ("Incorrect", "plain"): "Incorrect + plain\n(control)",
}
COLORS = {"polished": "#4C72B0", "plain": "#DD8452"}


# --------------------------------------------------------------------------- #
# Loading & cleaning
# --------------------------------------------------------------------------- #


def load_data() -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(DATA_DIR, "responses*.csv")))
    if not files:
        raise SystemExit("No data/responses*.csv files found.")
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    before = len(df)
    df = df.drop_duplicates(subset=["participant_id", "question_id"], keep="last")
    print(f"Loaded {len(files)} file(s), {before} rows, {len(df)} after removing duplicates.")

    n_per_participant = df.groupby("participant_id")["question_id"].nunique()
    complete = n_per_participant[n_per_participant == N_QUESTIONS].index
    dropped = len(n_per_participant) - len(complete)
    if dropped:
        print(f"Dropping {dropped} participant(s) who did not complete all {N_QUESTIONS} questions.")
    df = df[df["participant_id"].isin(complete)].copy()

    df["judged_correctly"] = (df["judgment"] == df["actual"]).astype(int)   # Unsure counts as wrong
    df["relied"] = (df["reliance"] == "Yes").astype(int)
    df["over_trust"] = ((df["actual"] == "Incorrect") & (df["trust"] >= 4)).astype(int)
    df["under_trust"] = ((df["actual"] == "Correct") & (df["trust"] <= 2)).astype(int)
    df["missed_error"] = ((df["actual"] == "Incorrect") & (df["judgment"] == "Correct")).astype(int)
    return df


# --------------------------------------------------------------------------- #
# Tables
# --------------------------------------------------------------------------- #


def summary_by_cell(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["actual", "presentation"])
    out = pd.DataFrame(
        {
            "responses": g.size(),
            "accuracy": g["judged_correctly"].mean(),
            "mean_trust": g["trust"].mean(),
            "mean_confidence": g["confidence"].mean(),
            "reliance_rate": g["relied"].mean(),
            "missed_error_rate": g["missed_error"].mean(),
            "over_trust_rate": g["over_trust"].mean(),
            "under_trust_rate": g["under_trust"].mean(),
        }
    ).reindex(CELLS)
    # over/under-trust only make sense in their own row
    out.loc[("Correct", slice(None)), ["missed_error_rate", "over_trust_rate"]] = float("nan")
    out.loc[("Incorrect", slice(None)), ["under_trust_rate"]] = float("nan")
    return out.round(3)


def summary_by_question(df: pd.DataFrame) -> pd.DataFrame:
    piv = df.pivot_table(index=["question_id", "topic", "actual"], columns="presentation",
                         values=["trust", "judged_correctly"], aggfunc="mean")
    piv.columns = [f"{a}_{b}" for a, b in piv.columns]
    return piv.round(3)


def per_participant_cells(df: pd.DataFrame) -> pd.DataFrame:
    """One row per participant with mean trust / accuracy in each of the 4 cells.
    Every participant has data in every cell, so tests can be paired."""
    t = df.pivot_table(index="participant_id", columns=["actual", "presentation"], values="trust", aggfunc="mean")
    a = df.pivot_table(index="participant_id", columns=["actual", "presentation"], values="judged_correctly", aggfunc="mean")
    t.columns = [f"trust_{x}_{y}" for x, y in t.columns]
    a.columns = [f"acc_{x}_{y}" for x, y in a.columns]
    return pd.concat([t, a], axis=1).dropna()


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #


def run_stats(df: pd.DataFrame) -> list[str]:
    lines = []
    if not HAVE_SCIPY:
        lines.append("scipy is not installed - run `pip install scipy` to get the statistical tests.")
        return lines

    pp = per_participant_cells(df)
    n = len(pp)
    lines.append(f"All tests are paired within participants (n = {n}). Wilcoxon signed-rank unless stated.")
    lines.append("")

    def wilcoxon_line(label, a, b):
        try:
            w, p = stats.wilcoxon(a, b)
            return f"{label}: mean {a.mean():.2f} vs {b.mean():.2f} (diff {a.mean() - b.mean():+.2f}), W = {w:.1f}, p = {p:.3f}"
        except ValueError as e:  # all differences zero
            return f"{label}: could not test ({e})"

    # H1 - over-trust: on INCORRECT answers, is trust higher when polished than plain?
    lines.append("H1 Over-trust - " + wilcoxon_line(
        "trust in INCORRECT answers, polished vs plain",
        pp["trust_Incorrect_polished"], pp["trust_Incorrect_plain"]))

    # H2 - under-trust: on CORRECT answers, is trust lower when plain than polished?
    lines.append("H2 Under-trust - " + wilcoxon_line(
        "trust in CORRECT answers, polished vs plain",
        pp["trust_Correct_polished"], pp["trust_Correct_plain"]))

    # H3 - does polish hurt error detection?
    lines.append("H3 Error detection - " + wilcoxon_line(
        "accuracy on INCORRECT answers, polished vs plain",
        pp["acc_Incorrect_polished"], pp["acc_Incorrect_plain"]))

    # H4 - calibration: trust gap (correct - incorrect) in each style
    gap_polished = pp["trust_Correct_polished"] - pp["trust_Incorrect_polished"]
    gap_plain = pp["trust_Correct_plain"] - pp["trust_Incorrect_plain"]
    lines.append("H4 Calibration - " + wilcoxon_line(
        "trust gap (correct minus incorrect), polished vs plain", gap_polished, gap_plain))
    lines.append(f"    A bigger gap = trust tracks accuracy better. Polished gap {gap_polished.mean():+.2f}, "
                 f"plain gap {gap_plain.mean():+.2f}.")

    # H5 - self-confidence vs accuracy
    r, p = stats.spearmanr(df["confidence"], df["judged_correctly"])
    lines.append(f"H5 Self-confidence vs accuracy - Spearman rho = {r:.3f}, p = {p:.3f} (all responses)")

    lines.append("")
    lines.append("Interpretation guide: p < 0.05 is conventionally 'statistically significant'. With a small "
                 "sample a non-significant result means 'we could not detect a difference', not 'there is "
                 "no difference' - say this in the Limitations section.")
    return lines


# --------------------------------------------------------------------------- #
# Graphs
# --------------------------------------------------------------------------- #


def _grouped_bars(summary, column, title, ylabel, filename, ylim):
    """Two groups (Correct / Incorrect) x two bars (polished / plain)."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = [0, 1]
    w = 0.36
    for k, pres in enumerate(["polished", "plain"]):
        vals = [summary.loc[(act, pres), column] for act in ["Correct", "Incorrect"]]
        pos = [xi + (k - 0.5) * w for xi in x]
        ax.bar(pos, vals, w, label=pres.capitalize(), color=COLORS[pres])
        for p_, v in zip(pos, vals):
            if pd.notna(v):
                ax.text(p_, v, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(["AI answer CORRECT", "AI answer INCORRECT"])
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(title="Presentation")
    plt.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, filename), dpi=150)
    plt.close(fig)


def graph_1_trust(summary):
    _grouped_bars(summary, "mean_trust", "Graph 1 - Trust by correctness and presentation",
                  "Mean trust (1-5)", "1_trust_by_cell.png", (1, 5))


def graph_2_accuracy(summary):
    _grouped_bars(summary, "accuracy", "Graph 2 - Judgment accuracy by correctness and presentation",
                  "Proportion judged correctly", "2_accuracy_by_cell.png", (0, 1))


def graph_3_reliance(summary):
    _grouped_bars(summary, "reliance_rate", "Graph 3 - 'Would you use this answer?' by cell",
                  "Proportion answering Yes", "3_reliance_by_cell.png", (0, 1))


def graph_4_over_under(summary):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    labels = ["Over-trust\n(AI wrong, trust ≥ 4)", "Under-trust\n(AI right, trust ≤ 2)"]
    vals = {
        "polished": [summary.loc[("Incorrect", "polished"), "over_trust_rate"],
                     summary.loc[("Correct", "polished"), "under_trust_rate"]],
        "plain": [summary.loc[("Incorrect", "plain"), "over_trust_rate"],
                  summary.loc[("Correct", "plain"), "under_trust_rate"]],
    }
    w = 0.36
    for k, pres in enumerate(["polished", "plain"]):
        pos = [i + (k - 0.5) * w for i in range(2)]
        ax.bar(pos, vals[pres], w, label=pres.capitalize(), color=COLORS[pres])
        for p_, v in zip(pos, vals[pres]):
            ax.text(p_, v, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Proportion of responses")
    ax.set_title("Graph 4 - Over-trust and under-trust")
    ax.legend(title="Presentation")
    plt.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "4_over_under_trust.png"), dpi=150)
    plt.close(fig)


def graph_5_confidence_vs_accuracy(df):
    acc = df.groupby("confidence")["judged_correctly"].mean()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(acc.index, acc.values, marker="o", color="#8172B2")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 1)
    ax.set_xlabel("Participant's confidence in own judgment (1-5)")
    ax.set_ylabel("Proportion judged correctly")
    ax.set_title("Graph 5 - Are confident participants actually more accurate?")
    for x_, y_ in zip(acc.index, acc.values):
        ax.text(x_, y_ + 0.02, f"{y_:.2f}", ha="center")
    plt.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "5_confidence_vs_accuracy.png"), dpi=150)
    plt.close(fig)


def graph_6_per_question(byq):
    fig, ax = plt.subplots(figsize=(9, 4.8))
    labels = [f"Q{qid}\n{act[:3]}" for qid, _, act in byq.index]
    x = range(len(labels))
    w = 0.38
    ax.bar([i - w / 2 for i in x], byq["trust_polished"], w, label="Polished", color=COLORS["polished"])
    ax.bar([i + w / 2 for i in x], byq["trust_plain"], w, label="Plain", color=COLORS["plain"])
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(1, 5)
    ax.set_ylabel("Mean trust (1-5)")
    ax.set_title("Graph 6 - Trust per question (Cor = correct answer, Inc = incorrect answer)")
    ax.legend()
    plt.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "6_trust_per_question.png"), dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Results summary (markdown)
# --------------------------------------------------------------------------- #


def write_results_summary(df, summary, byq, stat_lines):
    n = df["participant_id"].nunique()
    s = summary
    ip, ipl = s.loc[("Incorrect", "polished")], s.loc[("Incorrect", "plain")]
    cp, cpl = s.loc[("Correct", "polished")], s.loc[("Correct", "plain")]

    md = [
        "# Results summary (auto-generated by analysis.py)",
        "",
        f"Generated from **{n} complete participants** ({len(df)} responses, {N_QUESTIONS} questions each).",
        "Copy the numbers into the paper; write the interpretation yourself.",
        "",
        "## Headline numbers",
        "",
        f"- **Over-trust test (incorrect answers):** trust was {ip['mean_trust']:.2f} when polished vs "
        f"{ipl['mean_trust']:.2f} when plain. Participants missed the error "
        f"{ip['missed_error_rate']:.0%} of the time when polished vs {ipl['missed_error_rate']:.0%} when plain.",
        f"- **Under-trust test (correct answers):** trust was {cpl['mean_trust']:.2f} when plain vs "
        f"{cp['mean_trust']:.2f} when polished. Under-trust rate {cpl['under_trust_rate']:.0%} (plain) vs "
        f"{cp['under_trust_rate']:.0%} (polished).",
        f"- **Reliance:** would use a polished *incorrect* answer {ip['reliance_rate']:.0%} of the time, "
        f"a plain *correct* answer {cpl['reliance_rate']:.0%} of the time.",
        f"- **Calibration:** trust gap (correct − incorrect) = {cp['mean_trust'] - ip['mean_trust']:+.2f} "
        f"when polished, {cpl['mean_trust'] - ipl['mean_trust']:+.2f} when plain.",
        "",
        "## Summary by cell",
        "",
        summary.to_markdown(),
        "",
        "## Per question",
        "",
        byq.to_markdown(),
        "",
        "## Statistical tests",
        "",
        *[f"- {l}" if l else "" for l in stat_lines],
        "",
        "## Graphs",
        "",
        "- `graphs/1_trust_by_cell.png` - the key graph",
        "- `graphs/2_accuracy_by_cell.png`",
        "- `graphs/3_reliance_by_cell.png`",
        "- `graphs/4_over_under_trust.png`",
        "- `graphs/5_confidence_vs_accuracy.png`",
        "- `graphs/6_trust_per_question.png`",
    ]
    path = os.path.join(OUT_DIR, "results_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    return path


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main():
    os.makedirs(GRAPH_DIR, exist_ok=True)
    df = load_data()
    print(f"\nParticipants: {df['participant_id'].nunique()}   Rows: {len(df)}\n")

    summary = summary_by_cell(df)
    byq = summary_by_question(df)

    print("=== Summary by cell (actual x presentation) ===")
    print(summary.to_string())
    print("\n=== Per question ===")
    print(byq.to_string())

    stat_lines = run_stats(df)
    print("\n=== Statistical tests ===")
    print("\n".join(stat_lines))

    summary.to_csv(os.path.join(OUT_DIR, "summary_by_cell.csv"))
    byq.to_csv(os.path.join(OUT_DIR, "summary_by_question.csv"))

    graph_1_trust(summary)
    graph_2_accuracy(summary)
    graph_3_reliance(summary)
    graph_4_over_under(summary)
    graph_5_confidence_vs_accuracy(df)
    graph_6_per_question(byq)

    path = write_results_summary(df, summary, byq, stat_lines)
    print(f"\nGraphs saved to {GRAPH_DIR}")
    print(f"Results summary written to {path}")


if __name__ == "__main__":
    main()
