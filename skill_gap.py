from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class SkillGapResult:
    career: str
    matched_skills: List[str]
    missing_skills: List[str]
    readiness_percentage: int
    is_known_career: bool

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def _normalize_skill_name(skill: str) -> str:
    return " ".join(skill.strip().lower().split())


def _normalize_skill_list(skills: Iterable[str] | None) -> List[str]:
    if not skills:
        return []

    normalized_skills: List[str] = []
    seen = set()

    for skill in skills:
        if not isinstance(skill, str):
            continue

        normalized_skill = _normalize_skill_name(skill)
        if not normalized_skill or normalized_skill in seen:
            continue

        seen.add(normalized_skill)
        normalized_skills.append(normalized_skill)

    return normalized_skills


def _normalize_career_skill_map(
    career_skill_map: Mapping[str, Sequence[str]],
) -> Dict[str, List[str]]:
    normalized_map: Dict[str, List[str]] = {}

    for career_name, skills in career_skill_map.items():
        if not isinstance(career_name, str):
            continue
        normalized_map[career_name.strip().lower()] = _normalize_skill_list(skills)

    return normalized_map


def analyze_skill_gap(
    predicted_career: str,
    user_skills: Iterable[str] | None,
    required_skills_by_career: Mapping[str, Sequence[str]],
) -> Dict[str, object]:
    normalized_career = predicted_career.strip() if isinstance(predicted_career, str) else ""
    career_lookup_key = normalized_career.lower()

    normalized_user_skills = set(_normalize_skill_list(user_skills))
    normalized_required_skill_map = _normalize_career_skill_map(required_skills_by_career)

    required_skills = normalized_required_skill_map.get(career_lookup_key)
    if required_skills is None:
        return SkillGapResult(
            career=normalized_career,
            matched_skills=[],
            missing_skills=[],
            readiness_percentage=0,
            is_known_career=False,
        ).to_dict()

    matched_skills = [skill for skill in required_skills if skill in normalized_user_skills]
    missing_skills = [skill for skill in required_skills if skill not in normalized_user_skills]

    readiness_percentage = (
        round((len(matched_skills) / len(required_skills)) * 100)
        if required_skills
        else 100
    )

    return SkillGapResult(
        career=normalized_career,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        readiness_percentage=readiness_percentage,
        is_known_career=True,
    ).to_dict()
