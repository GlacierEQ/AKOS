"""Deterministic human-calibration engine for the PSYSOC-X stone."""

from __future__ import annotations

from .models import AudienceContext, CalibrationProfile


def calibrate(context: AudienceContext) -> CalibrationProfile:
    """Translate explicit audience context into bounded presentation guidance.

    This function does not infer diagnoses, vulnerabilities, protected traits, or
    hidden psychological attributes. It calibrates presentation only from the
    caller-supplied decision context.
    """

    high_stakes = context.stakes in {"high", "critical"}
    privacy_sensitive = context.private_or_sensitive
    humor_mode = _humor_mode(context, high_stakes, privacy_sensitive)
    tone = _tone(context, high_stakes, privacy_sensitive)
    density = _density(context)
    skepticism_response = _skepticism_response(context)
    attention_strategy = _attention_strategy(context)
    logic_order = _logic_order(context)
    memory_anchor = _memory_anchor(context)
    warnings = _warnings(context, high_stakes, privacy_sensitive)
    confidence = _confidence(context)

    return CalibrationProfile(
        attention_strategy=attention_strategy,
        humor_mode=humor_mode,
        tone=tone,
        logic_order=logic_order,
        density=density,
        skepticism_response=skepticism_response,
        memory_anchor=memory_anchor,
        dignity_controls=(
            "describe observable context before interpreting motive",
            "separate likely reception from verified fact",
            "preserve reader agency; do not exploit fear, shame, grief, or dependency",
            "prefer clarity and evidence over pressure",
        ),
        warnings=warnings,
        confidence=confidence,
    )


def render_guidance(profile: CalibrationProfile) -> str:
    order = " -> ".join(profile.logic_order)
    warnings = "; ".join(profile.warnings) if profile.warnings else "none"
    return (
        f"attention={profile.attention_strategy}\n"
        f"tone={profile.tone}\n"
        f"humor={profile.humor_mode}\n"
        f"density={profile.density}\n"
        f"logic={order}\n"
        f"skepticism={profile.skepticism_response}\n"
        f"memory_anchor={profile.memory_anchor}\n"
        f"warnings={warnings}\n"
        f"confidence={profile.confidence}"
    )


def _humor_mode(context: AudienceContext, high_stakes: bool, private: bool) -> str:
    if not context.humor_allowed or context.stakes == "critical" or private:
        return "none"
    if high_stakes or context.emotional_weight >= 7:
        return "restrained-dry-wit-only"
    if context.audience.lower() in {"engineer", "technical reviewer", "developer"}:
        return "dry-technical-wit"
    if context.stakes == "low" and context.emotional_weight <= 3:
        return "light-playful"
    return "subtle-self-aware"


def _tone(context: AudienceContext, high_stakes: bool, private: bool) -> str:
    if context.stakes == "critical" or private:
        return "calm-exact-dignified"
    if high_stakes:
        return "confident-evidence-first"
    if context.skepticism >= 7:
        return "measured-and-falsifiable"
    if context.emotional_weight >= 7:
        return "warm-without-sentimentality"
    return "clear-human-and-assured"


def _density(context: AudienceContext) -> str:
    pressure = context.cognitive_load + context.skepticism
    if pressure >= 15:
        return "progressive-disclosure"
    if pressure >= 9:
        return "compact-with-proof-links"
    return "moderate-with-context"


def _skepticism_response(context: AudienceContext) -> str:
    if context.skepticism >= 8:
        return "lead-with-limits-and-reproducible-proof"
    if context.skepticism >= 5:
        return "pair-each-material-claim-with-evidence"
    return "state-value-then-offer-proof"


def _attention_strategy(context: AudienceContext) -> str:
    if context.evidence_strength <= 3:
        return "lead-with-the-problem-and-name-the-evidence-gap"
    if context.cognitive_load >= 8:
        return "one-concrete-outcome-then-a-three-item-map"
    if context.decision.lower().startswith(("hire", "approve", "fund", "adopt")):
        return "lead-with-decision-relevant-consequence"
    return "lead-with-the-human-problem-before-the-mechanism"


def _logic_order(context: AudienceContext) -> tuple[str, ...]:
    if context.evidence_strength <= 3:
        return ("problem", "known facts", "unknowns", "method", "next proof")
    if context.skepticism >= 7:
        return ("claim boundary", "evidence", "mechanism", "tradeoff", "decision")
    if context.cognitive_load >= 7:
        return ("outcome", "why it matters", "three-part map", "proof", "detail")
    return ("human consequence", "outcome", "mechanism", "proof", "next action")


def _memory_anchor(context: AudienceContext) -> str:
    if context.evidence_strength <= 3:
        return "Use an honest unresolved tension, not a victory slogan."
    if context.skepticism >= 7:
        return "Compress the core invariant into one falsifiable sentence."
    return "Name the transformation in language native to the project."


def _warnings(
    context: AudienceContext,
    high_stakes: bool,
    private: bool,
) -> tuple[str, ...]:
    warnings: list[str] = []
    if high_stakes:
        warnings.append("do not let emotional force outrun evidentiary strength")
    if private:
        warnings.append("remove identifying or sensitive detail not necessary to the decision")
    if context.evidence_strength <= 3:
        warnings.append("do not convert plausible interpretation into fact")
    if context.emotional_weight >= 8:
        warnings.append("avoid humor, triumphalism, and pressure")
    if context.desired_action.lower() in {"buy", "vote", "donate", "confess", "comply"}:
        warnings.append("preserve agency and disclose material uncertainty")
    return tuple(warnings)


def _confidence(context: AudienceContext) -> str:
    if context.evidence_strength >= 8:
        return "high-for-presentation-calibration-not-for-human-prediction"
    if context.evidence_strength >= 5:
        return "medium"
    return "low-evidence-gap-must-remain-visible"
