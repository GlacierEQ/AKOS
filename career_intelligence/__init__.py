"""Evidence-bound career intelligence runtime and platform."""

from .builder import BuildResult, build_package, verify_package
from .models import CareerGraph, TargetProfile
from .platform_builder import build_career_platform, verify_career_platform
from .platform_models import JobAnalysis, PlatformBuildResult, ReaderProfile, SkillRecord
from .validation import ValidationIssue, validate_graph

__all__ = [
    "BuildResult",
    "CareerGraph",
    "JobAnalysis",
    "PlatformBuildResult",
    "ReaderProfile",
    "SkillRecord",
    "TargetProfile",
    "ValidationIssue",
    "build_career_platform",
    "build_package",
    "validate_graph",
    "verify_career_platform",
    "verify_package",
]
