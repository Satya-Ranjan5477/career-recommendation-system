from datetime import datetime, timezone
from database.mongodb import students_collection

quiz_attempts_collection = students_collection.database["quiz_attempts"]


def save_quiz_attempt(
    firebase_uid,
    user_id,
    career,
    score,
    total_questions,
    analysis
):
    percentage = round(score / total_questions * 100, 2) if total_questions else 0

    attempt = {
        "firebase_uid": firebase_uid,
        "user_id": user_id,
        "career": career,
        "score": score,
        "total_questions": total_questions,
        "percentage": percentage,
        "analysis": analysis,
        "completed_at": datetime.now(timezone.utc)
    }

    result = quiz_attempts_collection.insert_one(attempt)
    return str(result.inserted_id)

def get_quiz_history(firebase_uid):
    attempts = list(
        quiz_attempts_collection.find(
            {"firebase_uid": firebase_uid}
        ).sort("completed_at", -1)
    )

    for attempt in attempts:
        attempt["_id"] = str(attempt["_id"])

    return attempts    