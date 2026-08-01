import pytest

from infinity_stones.models import AudienceContext
from infinity_stones.psysoc_x import calibrate, render_guidance


def test_critical_private_context_disables_humor_and_adds_warnings() -> None:
    profile = calibrate(
        AudienceContext(
            audience="family member",
            decision="understand a sensitive event",
            stakes="critical",
            skepticism=7,
            cognitive_load=8,
            emotional_weight=10,
            evidence_strength=5,
            private_or_sensitive=True,
        )
    )
    assert profile.humor_mode == "none"
    assert profile.tone == "calm-exact-dignified"
    assert "avoid humor, triumphalism, and pressure" in profile.warnings
    assert "remove identifying or sensitive detail" in " ".join(profile.warnings)


def test_skeptical_engineer_gets_proof_first_and_dry_wit() -> None:
    profile = calibrate(
        AudienceContext(
            audience="engineer",
            decision="adopt the architecture",
            skepticism=9,
            cognitive_load=6,
            emotional_weight=2,
            evidence_strength=9,
        )
    )
    assert profile.humor_mode == "dry-technical-wit"
    assert profile.logic_order[0] == "claim boundary"
    assert profile.skepticism_response == "lead-with-limits-and-reproducible-proof"


def test_weak_evidence_never_becomes_confident_prediction() -> None:
    profile = calibrate(
        AudienceContext(
            audience="reviewer",
            decision="assess a claim",
            stakes="high",
            skepticism=8,
            cognitive_load=5,
            emotional_weight=5,
            evidence_strength=2,
        )
    )
    assert profile.confidence == "low-evidence-gap-must-remain-visible"
    assert "do not convert plausible interpretation into fact" in profile.warnings
    assert profile.logic_order[:3] == ("problem", "known facts", "unknowns")


def test_context_rejects_out_of_range_scores() -> None:
    with pytest.raises(ValueError, match="skepticism"):
        AudienceContext(audience="x", decision="y", skepticism=11)


def test_render_guidance_is_stable_and_inspectable() -> None:
    profile = calibrate(AudienceContext(audience="recruiter", decision="hire"))
    rendered = render_guidance(profile)
    assert "attention=" in rendered
    assert "logic=" in rendered
    assert "confidence=" in rendered
