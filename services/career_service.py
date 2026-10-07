from datetime import datetime, timezone
from database.mongodb import students_collection

career_history_collection = students_collection.database["career_recommendations"]


def save_career_recommendation(
    firebase_uid,
    user_id,
    qualification,
    skills,
    interests,
    traits,
    career,
    skill_gap
):
    recommendation = {
        "firebase_uid": firebase_uid,
        "user_id": user_id,
        "qualification": qualification,
        "skills": skills,
        "interests": interests,
        "traits": traits,
        "career": career,
        "skill_gap": skill_gap,
        "created_at": datetime.now(timezone.utc)
    }

    result = career_history_collection.insert_one(recommendation)

    return str(result.inserted_id)


def get_career_recommendation_history(firebase_uid):
    recommendations = list(
        career_history_collection.find(
            {"firebase_uid": firebase_uid}
        ).sort("created_at", -1)
    )

    for recommendation in recommendations:
        recommendation["_id"] = str(recommendation["_id"])

    return recommendations