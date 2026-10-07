import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
le_q = joblib.load(os.path.join(BASE_DIR, "le_q.pkl"))
le_c = joblib.load(os.path.join(BASE_DIR, "le_c.pkl"))
mlb_skills = joblib.load(os.path.join(BASE_DIR, "mlb_skills.pkl"))
mlb_interests = joblib.load(os.path.join(BASE_DIR, "mlb_interests.pkl"))
mlb_traits = joblib.load(os.path.join(BASE_DIR, "mlb_traits.pkl"))
def normalize_list(lst):
    return [x.strip().lower() for x in lst]

def predict_career(q, skills, interests,traits):

    q = le_q.transform([q])[0]

    skills_encoded = mlb_skills.transform([skills])
    interests_encoded = mlb_interests.transform([interests])
    traits_encoded = mlb_traits.transform([traits])
    X = np.hstack(([q], skills_encoded[0], interests_encoded[0],  traits_encoded[0])).reshape(1, -1)


    pred = model.predict(X)
    return le_c.inverse_transform(pred)[0]

