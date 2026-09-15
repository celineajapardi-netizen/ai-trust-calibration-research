"""
Export the question bank as a markdown table for Appendix A of the paper.

    python analysis/export_question_bank.py   ->  paper/appendix_a_question_bank.md
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiment"))
from questions import QUESTIONS  # noqa: E402

OUT = os.path.join(ROOT, "paper", "appendix_a_question_bank.md")

lines = [
    "# Appendix A — Question bank",
    "",
    "| # | Topic | Question | AI answer | Actual | AI conf. |",
    "|---|-------|----------|-----------|--------|----------|",
]
for q in QUESTIONS:
    lines.append(
        f"| {q['id']} | {q['topic']} | {q['question']} | {q['ai_answer']} | {q['actual']} | {q['ai_confidence']}% |"
    )
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {OUT}")
