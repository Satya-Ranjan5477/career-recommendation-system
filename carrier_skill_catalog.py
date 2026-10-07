from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List


DATASET_PATH = Path(__file__).with_name("career_data.csv")


def load_required_skills_by_career(dataset_path: Path = DATASET_PATH) -> Dict[str, List[str]]:
    career_skills: Dict[str, List[str]] = {}

    with dataset_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            career = (row.get("career") or "").strip()
            raw_skills = row.get("skills") or ""
            if not career:
                continue

            bucket = career_skills.setdefault(career, [])
            seen = set(bucket)

            for skill in raw_skills.split(","):
                normalized_skill = " ".join(skill.strip().lower().split())
                if not normalized_skill or normalized_skill in seen:
                    continue
                seen.add(normalized_skill)
                bucket.append(normalized_skill)

    return career_skills


REQUIRED_SKILLS_BY_CAREER = load_required_skills_by_career()
