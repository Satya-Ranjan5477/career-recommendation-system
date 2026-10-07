from flask import Flask, render_template, request,jsonify, session ,redirect, send_from_directory
from werkzeug.utils import secure_filename
from carrier_skill_catalog import REQUIRED_SKILLS_BY_CAREER
from predict import predict_career
from quiz_data import get_random_questions
from career_path_data import career_paths
from skill_gap import analyze_skill_gap
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
from pymongo import MongoClient
from datetime import datetime, timezone
from career_path_data import career_paths
from database.mongodb import students_collection
from services.quiz_service import (save_quiz_attempt,get_quiz_history)
from services.student_service import (
    save_student as save_student_to_db,
    get_student_by_uid
)
from services.career_service import (
    save_career_recommendation,
    get_career_recommendation_history
)
career_progress_collection = students_collection.database["career_progress"]
# Index for fast and unique career-progress lookup
career_progress_collection.create_index(
    [
        ("firebase_uid", 1),
        ("career", 1)
    ],
    unique=True
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def firebase_config():
    return {
      "apiKey": os.getenv("FIREBASE_API_KEY"),
      "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
      "projectId": os.getenv("FIREBASE_PROJECT_ID"),
      "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
      "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
      "appId": os.getenv("FIREBASE_APP_ID")
    }

        
@app.route("/")
def home():
    return render_template ('index.html')


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template ('dashboard.html',firebase_config=firebase_config())


@app.route("/login")
def login():
    return render_template ('login.html',firebase_config=firebase_config())


@app.route("/register")
def register():
    return render_template ('register.html',firebase_config=firebase_config())


@app.route('/form')
def form():
    if "user_id" not in session:
        return redirect("/login")
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():

    if "firebase_uid" not in session:
        return jsonify({
            "error": "Please log in again"
        }), 401

    q = request.form.get("qualification")

    if not q:
        return jsonify({
            "error": "Qualification is required"
        }), 400

    skills = request.form.getlist('skills[]')
    interests = request.form.getlist('interests[]')
    traits = request.form.getlist('traits[]')    


    career = predict_career(q, skills, interests,traits)
    skill_gap = analyze_skill_gap(
        predicted_career=career,
        user_skills=skills,
        required_skills_by_career=REQUIRED_SKILLS_BY_CAREER,
    )

    # ✅ store career in session
    normalized_traits = {trait.strip().lower() for trait in traits if isinstance(trait, str) and trait.strip()}
    trait_bonus = 0

    if 'analytical' in normalized_traits:
        trait_bonus += 5
    if 'problem solving' in normalized_traits:
        trait_bonus += 5
    if 'logical thinking' in normalized_traits:
        trait_bonus += 4
    if 'creativity' in normalized_traits:
        trait_bonus += 3
    if 'curiosity' in normalized_traits:
        trait_bonus += 2

    base_score = skill_gap.get('readiness_percentage', 0)
    readiness_score = min(base_score + trait_bonus, 100)
    skill_gap['readiness_score'] = readiness_score
    skill_gap['readiness_percentage'] = readiness_score
    total_skills = len(skill_gap.get('matched_skills', [])) + len(skill_gap.get('missing_skills', []))

    
    session['career'] = career
    session['skill_gap'] = skill_gap
    session['traits'] = traits
    session['interests'] = interests
    session['total_skills'] = total_skills
    
    # Save the career recommendation in MongoDB
    if "firebase_uid" in session and "user_id" in session:
        try:
            save_career_recommendation(
                firebase_uid=session["firebase_uid"],
                user_id=session["user_id"],
                qualification=q,
                skills=skills,
                interests=interests,
                traits=traits,
                career=career,
                skill_gap=skill_gap
            )
        except Exception:
            app.logger.exception(
                "Failed to save career recommendation"
            )

    return render_template(
        'result.html',
        career=career,
        skill_gap=skill_gap,
        traits=traits,
        interests=interests,
        total_skills=total_skills
    )
@app.route('/result')
def result():

    if "user_id" not in session:
        return redirect("/login")

    career = None
    skill_gap = {}
    traits = []
    interests = []
    total_skills = 0

    # Quiz data
    quiz_attempts = []
    latest_quiz_attempt = None
    previous_quiz_attempt = None

    firebase_uid = session.get("firebase_uid")

    # --------------------------------------------------
    # LOAD LATEST CAREER RECOMMENDATION
    # --------------------------------------------------

    if firebase_uid:

        try:

            history = get_career_recommendation_history(
                firebase_uid
            )

            if history:

                latest = history[0]

                career = latest.get("career")
                skill_gap = latest.get("skill_gap") or {}
                traits = latest.get("traits") or []
                interests = latest.get("interests") or []

                total_skills = (
                    len(skill_gap.get("matched_skills", []))
                    + len(skill_gap.get("missing_skills", []))
                )

        except Exception:

            app.logger.exception(
                "Could not load previous career recommendation"
            )

    # --------------------------------------------------
    # FALLBACK TO SESSION
    # --------------------------------------------------

    if not career:

        career = session.get("career")

        skill_gap = (
            session.get("skill_gap") or {}
        )

        traits = session.get(
            "traits",
            []
        )

        interests = session.get(
            "interests",
            []
        )

        total_skills = session.get(
            "total_skills",
            0
        )

    # --------------------------------------------------
    # LOAD QUIZ HISTORY FROM MONGODB
    # --------------------------------------------------

    if firebase_uid:

        try:

            quiz_attempts = get_quiz_history(
                firebase_uid
            )

            # Only attempts for this career
            if career:

                career_attempts = [
                    attempt
                    for attempt in quiz_attempts
                    if attempt.get("career") == career
                ]

            else:

                career_attempts = []

            # Newest attempt
            if len(career_attempts) >= 1:

                latest_quiz_attempt = career_attempts[0]

            # Previous attempt
            if len(career_attempts) >= 2:

                previous_quiz_attempt = career_attempts[1]

        except Exception:

            app.logger.exception(
                "Could not load quiz history"
            )

    # --------------------------------------------------
    # SAVE CURRENT RECOMMENDATION IN SESSION
    # --------------------------------------------------

    if career:

        session["career"] = career
        session["skill_gap"] = skill_gap
        session["traits"] = traits
        session["interests"] = interests
        session["total_skills"] = total_skills

    # --------------------------------------------------
    # SEND DATA TO RESULT.HTML
    # --------------------------------------------------

    return render_template(
        "result.html",

        career=career,

        skill_gap=skill_gap,

        traits=traits,

        interests=interests,

        total_skills=total_skills,

        latest_quiz_attempt=latest_quiz_attempt,

        previous_quiz_attempt=previous_quiz_attempt
    )




@app.route("/quiz")
def quiz_page():
    if "user_id" not in session:
        return redirect("/login")
    career = request.args.get("career")
    return render_template("quiz.html", career=career)



@app.route("/get-quiz/<career>", methods=["GET"])
def get_quiz(career):

    # User must be logged in
    if "user_id" not in session:
        return jsonify({
            "error": "Please log in again"
        }), 401

    # Validate career
    if not career:
        return jsonify({
            "error": "Career is required"
        }), 400

    # Check whether career exists in our career data
    if career not in career_paths:
        return jsonify({
            "error": "Invalid career"
        }), 400

    try:

        questions = get_random_questions(career)

        return jsonify(questions), 200

    except Exception:

        app.logger.exception(
            "Error loading quiz questions"
        )

        return jsonify({
            "error": "Could not load quiz questions"
        }), 500

@app.route("/save-quiz-attempt", methods=["POST"])
def save_quiz_attempt_route():
    if "firebase_uid" not in session or "user_id" not in session:
        return jsonify({"error": "Please log in again"}), 401

    data = request.get_json(silent=True) or {}

    career = data.get("career")
    score = data.get("score")
    total = data.get("total")
    analysis = data.get("analysis", [])

    if not career or score is None or total is None:
        return jsonify({"error": "Missing quiz result"}), 400

    if (
        not isinstance(score, int)
        or isinstance(score, bool)
        or not isinstance(total, int)
        or isinstance(total, bool)
        or total <= 0
        or score < 0
        or score > total
    ):
        return jsonify({"error": "Invalid quiz score"}), 400

    if not isinstance(analysis, list):
        return jsonify({"error": "Invalid quiz analysis"}), 400

    try:
        attempt_id = save_quiz_attempt(
            firebase_uid=session["firebase_uid"],
            user_id=session["user_id"],
            career=career,
            score=score,
            total_questions=total,
            analysis=analysis
        )

        return jsonify({
            "message": "Quiz attempt saved successfully",
            "attempt_id": attempt_id
        }), 201

    except Exception:
        app.logger.exception("Failed to save quiz attempt")
        return jsonify({"error": "Could not save quiz attempt"}), 500  

@app.route("/quiz-history", methods=["GET"])
def quiz_history():
    if "firebase_uid" not in session:
        return jsonify({"error": "Please log in again"}), 401

    try:
        history = get_quiz_history(
            session["firebase_uid"]
        )

        return jsonify(history), 200

    except Exception:
        app.logger.exception("Failed to retrieve quiz history")

        return jsonify({
            "error": "Could not retrieve quiz history"
        }), 500          

@app.route("/career-recommendation-history", methods=["GET"])
def career_recommendation_history():
    if "firebase_uid" not in session:
        return jsonify({
            "error": "Please log in again"
        }), 401

    try:
        history = get_career_recommendation_history(
            session["firebase_uid"]
        )

        return jsonify(history), 200

    except Exception:
        app.logger.exception(
            "Failed to retrieve career recommendation history"
        )

        return jsonify({
            "error": "Could not retrieve career recommendation history"
        }), 500
    

@app.route("/career-path")
def career_path():

    if "user_id" not in session:
        return redirect("/login")

    selected_career = (
        request.args.get("career")
        or session.get("career")
        or ""
    )

    career_history = []

    firebase_uid = session.get("firebase_uid")

    if firebase_uid:

        try:

            recommendations = get_career_recommendation_history(
                firebase_uid
            )

            career_history = list(dict.fromkeys(
                item.get("career")
                for item in recommendations
                if item.get("career")
            ))

            # If no career came from URL/session,
            # use latest MongoDB recommendation
            if not selected_career and recommendations:

                latest = recommendations[0]

                selected_career = \
                    latest.get("career", "")

                session["career"] = selected_career

                session["skill_gap"] = \
                    latest.get("skill_gap") or {}

                session["traits"] = \
                    latest.get("traits") or []

                session["interests"] = \
                    latest.get("interests") or []

        except Exception:

            app.logger.exception(
                "Failed to load career history"
            )

    # Fallback
    if not career_history and session.get("career"):

        career_history = [
            session["career"]
        ]

    return render_template(
        "career_path.html",

        selected_career=selected_career,

        career_history=career_history
    )

@app.route("/get-path/<career>")
def get_path(career):

    # ---------------------------------
    # 1. Check login
    # ---------------------------------
    if "firebase_uid" not in session:
        return jsonify({
            "error": "Please log in again"
        }), 401

    # ---------------------------------
    # 2. Validate career
    # ---------------------------------
    if not career or career not in career_paths:
        return jsonify({
            "error": "Invalid career"
        }), 400

    try:

        return jsonify(
            career_paths[career]
        ), 200

    except Exception:

        app.logger.exception(
            "Failed to load career path"
        )

        return jsonify({
            "error": "Could not load career path"
        }), 500
@app.route("/get-career-progress/<career>", methods=["GET"])
def get_career_progress(career):

    # ---------------------------------
    # 1. Check login
    # ---------------------------------
    firebase_uid = session.get("firebase_uid")

    if not firebase_uid:
        return jsonify({
            "error": "Please log in again"
        }), 401

    # ---------------------------------
    # 2. Validate career
    # ---------------------------------
    if not career or career not in career_paths:
        return jsonify({
            "error": "Invalid career"
        }), 400

    try:

        # ---------------------------------
        # 3. Find progress ONLY for this user
        # ---------------------------------
        progress = career_progress_collection.find_one({
            "firebase_uid": firebase_uid,
            "career": career
        })

        # ---------------------------------
        # 4. No progress yet
        # ---------------------------------
        if not progress:
            return jsonify({
                "completed_steps": []
            }), 200

        completed_steps = progress.get(
            "completed_steps",
            []
        )

        # Make sure stored data is a list
        if not isinstance(completed_steps, list):
            completed_steps = []

        return jsonify({
            "completed_steps": completed_steps
        }), 200

    except Exception:

        app.logger.exception(
            "Error loading career progress"
        )

        return jsonify({
            "error": "Could not load career progress"
        }), 500


@app.route("/save-career-progress/<career>", methods=["POST"])
def save_career_progress(career):

    # ---------------------------------
    # 1. Check login
    # ---------------------------------
    firebase_uid = session.get("firebase_uid")

    if not firebase_uid:
        return jsonify({
            "error": "Please log in again"
        }), 401

    # ---------------------------------
    # 2. Validate career
    # ---------------------------------
    if not career or career not in career_paths:
        return jsonify({
            "error": "Invalid career"
        }), 400

    # ---------------------------------
    # 3. Read JSON data
    # ---------------------------------
    data = request.get_json(silent=True) or {}

    completed_steps = data.get(
        "completed_steps",
        []
    )

    # ---------------------------------
    # 4. Validate list
    # ---------------------------------
    if not isinstance(completed_steps, list):
        return jsonify({
            "error": "Invalid progress data"
        }), 400

    try:

        # ---------------------------------
        # 5. Get total number of steps
        # ---------------------------------
        total_steps = len(
            career_paths[career].get("steps", [])
        )

        # ---------------------------------
        # 6. Keep only valid integer indexes
        # ---------------------------------
        valid_steps = []

        for step in completed_steps:

            if isinstance(step, int) and not isinstance(step, bool):

                if 0 <= step < total_steps:
                    valid_steps.append(step)

        # Remove duplicates and sort
        completed_steps = sorted(
            set(valid_steps)
        )

        # ---------------------------------
        # 7. Save progress for this user
        # ---------------------------------
        now = datetime.now(timezone.utc)

        career_progress_collection.update_one(
            {
                "firebase_uid": firebase_uid,
                "career": career
            },
            {
                "$set": {
                    "completed_steps": completed_steps,
                    "updated_at": now
                },

                "$setOnInsert": {
                    "firebase_uid": firebase_uid,
                    "career": career,
                    "created_at": now
                }
            },
            upsert=True
        )

        # ---------------------------------
        # 8. Send response
        # ---------------------------------
        return jsonify({
            "message": "Career progress saved successfully",
            "completed_steps": completed_steps
        }), 200

    except Exception:

        app.logger.exception(
            "Error saving career progress"
        )

        return jsonify({
            "error": "Could not save career progress"
        }), 500


@app.route("/set-user", methods=["POST"])
def set_user():
    data = request.get_json(silent=True) or {}

    firebase_uid = data.get("firebase_uid")
    user_id = data.get("user_id")
    name = data.get("name")
    email = data.get("email")

    if not all([firebase_uid, user_id, name, email]):
        return jsonify({
            "error": "Missing user information"
        }), 400

    try:
        save_student_to_db(firebase_uid, user_id, name, email)

        session["firebase_uid"] = firebase_uid
        session["user_id"] = user_id

        return jsonify({
            "message": "User saved successfully",
            "user_id": user_id
        }), 200

    except Exception:
        app.logger.exception("Failed to save student")

        return jsonify({
            "error": "Unable to save student information"
        }), 500

@app.route("/get-student-profile", methods=["GET"])
def get_student_profile():
    firebase_uid = session.get("firebase_uid")

    if not firebase_uid:
        return jsonify({
            "error": "Please log in first"
        }), 401

    student = get_student_by_uid(firebase_uid)

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    return jsonify({
        "user_id": student.get("user_id"),
        "name": student.get("name"),
        "email": student.get("email")
    }), 200        

@app.route("/upload-profile-photo", methods=["POST"])
def upload_profile_photo():
    firebase_uid = session.get("firebase_uid")

    if not firebase_uid:
        return jsonify({"error": "Please log in again"}), 401

    if "photo" not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400

    photo = request.files["photo"]

    if photo.filename == "":
        return jsonify({"error": "No photo selected"}), 400

    try:
        result = cloudinary.uploader.upload(
            photo,
            folder="career_mitra/profile_photos",
            public_id=firebase_uid,
            overwrite=True,
            resource_type="image"
        )

        photo_url = result.get("secure_url")

        if not photo_url:
            return jsonify({"error": "Could not get image URL"}), 500

        students_collection.update_one(
            {"firebase_uid": firebase_uid},
            {
                "$set": {
                    "profile_photo_url": photo_url,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        return jsonify({
            "message": "Profile photo uploaded successfully",
            "photo_url": photo_url
        }), 200

    except Exception:
        app.logger.exception("Failed to upload profile photo")
        return jsonify({"error": "Could not upload profile photo"}), 500
@app.route("/get-profile-photo", methods=["GET"])
def get_profile_photo():

    firebase_uid = session.get("firebase_uid")

    if not firebase_uid:
        return jsonify({
            "error": "Please log in first"
        }), 401

    try:
        student = get_student_by_uid(firebase_uid)

        if not student:
            return jsonify({
                "photo_url": None
            }), 200

        return jsonify({
            "photo_url": student.get("profile_photo_url")
        }), 200

    except Exception:
        app.logger.exception("Failed to load profile photo")

        return jsonify({
            "error": "Could not load profile photo"
        }), 500




@app.route("/save-student", methods=["POST"])
def save_student():
    data = request.get_json(silent=True) or {}

    firebase_uid = data.get("firebase_uid")
    user_id = data.get("user_id")
    name = data.get("name")
    email = data.get("email")

    if not all([firebase_uid, user_id, name, email]):
        return jsonify({
            "error": "Student details are incomplete"
        }), 400

    now = datetime.now(timezone.utc)

    try:
        students_collection.update_one(
            {"firebase_uid": firebase_uid},
            {
                "$set": {
                    "user_id": user_id,
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

        return jsonify({
            "message": "Student profile saved successfully",
            "user_id": user_id
        }), 200

    except Exception as e:
        app.logger.exception("Unable to save student profile")

        return jsonify({
            "error": "Unable to save student profile"
        }), 500

@app.route("/resume")
def resume():
    if "user_id" not in session:
        return redirect("/login")
    career = session.get("career")
    return render_template('resume.html', career=career)
  

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)