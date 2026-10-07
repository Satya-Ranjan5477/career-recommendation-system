from database.mongodb import students_collection
from datetime import datetime, timezone


def save_student(firebase_uid, student_id, name, email):
    now = datetime.now(timezone.utc)

    students_collection.update_one(
        {"firebase_uid": firebase_uid},
        {
            "$set": {
                "student_id": student_id,
                "name": name,
                "email": email,
                "updated_at": now
            },
            "$setOnInsert": {
                "firebase_uid": firebase_uid,
                "created_at": now
            }
        },
        upsert=True
    )


def get_student_by_uid(firebase_uid):
    return students_collection.find_one(
        {"firebase_uid": firebase_uid},
        {"_id": 0}
    )