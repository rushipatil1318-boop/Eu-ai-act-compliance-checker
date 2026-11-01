"""Builds a Markdown report that the user can download."""
from datetime import date

from src.obligations import get_obligations
from src.rules import FINES, KEY_DATES, LAST_REVIEWED, LINKS


def build_report(answers, result):
    lines = [
        f"# EU AI Act Compliance Report: {answers.system_name}",
        f"*Generated on {date.today().isoformat()}. A learning tool, not legal advice.*",
        "",
        f"**Your role:** {answers.role}",
        f"**General-purpose AI model:** {'Yes' if answers.is_gpai else 'No'}",
        f"**Risk level:** {result.level}",
        "",
    ]

    if answers.description:
        lines += ["## System description", answers.description, ""]

    lines += ["## Why this level?"]
    lines += [f"- {reason}" for reason in result.reasons]

    lines += ["", "## What you need to do"]
    lines += [f"- **{article}**: {text}" for article, text in get_obligations(result, answers)]

    if result.level in FINES:
        lines += ["", "## Possible fines", f"Breaking the rules can cost {FINES[result.level]}."]

    lines += ["", "## Key dates"]
    lines += [f"- {when}: {what}" for when, what in KEY_DATES]

    lines += ["", "## Sources", f"Legal content last reviewed: {LAST_REVIEWED}"]
    lines += [f"- [{title}]({url})" for title, url in LINKS.items()]
    return "\n".join(lines) + "\n"
