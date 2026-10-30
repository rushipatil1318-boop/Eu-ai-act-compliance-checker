"""The brain of the project: turns questionnaire answers into a risk level.

The logic follows the same order as the AI Act itself:
banned practices -> high-risk -> transparency -> minimal risk.
"""
from dataclasses import dataclass, field

from src.obligations import TRANSPARENCY
from src.rules import ANNEX_III_AREAS, PROHIBITED

PROHIBITED_LEVEL = "Prohibited"
HIGH = "High risk"
LIMITED = "Limited risk"
MINIMAL = "Minimal risk"


@dataclass
class Answers:
    """Everything the user tells us about their AI system."""
    system_name: str = "My AI system"
    description: str = ""
    role: str = "Provider"
    is_gpai: bool = False
    prohibited: list = field(default_factory=list)
    annex_i_product: bool = False
    annex_iii_areas: list = field(default_factory=list)
    does_profiling: bool = False
    narrow_task: bool = False
    talks_to_people: bool = False
    generates_content: bool = False
    emotion_or_biometric: bool = False
    deepfake_or_public_text: bool = False


@dataclass
class Result:
    """What the classifier found out."""
    level: str
    reasons: list
    transparency: list = field(default_factory=list)
    exemption_used: bool = False


def _transparency_duties(a):
    # Article 50 duties can apply on top of ANY risk level (except banned systems)
    return [TRANSPARENCY[key] for key in TRANSPARENCY if getattr(a, key)]


def classify(a):
    # Step 1: a banned practice beats everything else
    if a.prohibited:
        reasons = [f"Banned practice (Art. 5): {PROHIBITED[key]}" for key in a.prohibited]
        return Result(PROHIBITED_LEVEL, reasons)

    transparency = _transparency_duties(a)

    # Step 2: high-risk because it is part of a regulated product (Annex I)
    if a.annex_i_product:
        reason = ("It is (or is a safety component of) a product under EU product-safety law "
                  "that needs a third-party conformity assessment (Art. 6(1), Annex I).")
        return Result(HIGH, [reason], transparency)

    # Step 3: high-risk because of its use area (Annex III)
    if a.annex_iii_areas:
        areas = [ANNEX_III_AREAS[key] for key in a.annex_iii_areas]
        reasons = [f"Used in an Annex III area: {area}" for area in areas]

        # Profiling people is ALWAYS high-risk, no exemption possible (Art. 6(3))
        if a.does_profiling:
            reasons.append("It profiles natural persons, so the Art. 6(3) exemption cannot be used.")
            return Result(HIGH, reasons, transparency)

        # Art. 6(3): a narrow helper task may be exempt from the high-risk label
        if a.narrow_task:
            reasons.append("It only does a narrow or preparatory task, so the Art. 6(3) exemption may apply.")
            level = LIMITED if transparency else MINIMAL
            return Result(level, reasons, transparency, exemption_used=True)

        return Result(HIGH, reasons, transparency)

    # Step 4: no high-risk trigger found
    if transparency:
        return Result(LIMITED, ["It has transparency duties under Art. 50."], transparency)

    return Result(MINIMAL, ["No banned, high-risk or transparency trigger was found."], transparency)
