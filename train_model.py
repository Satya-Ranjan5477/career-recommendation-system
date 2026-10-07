import pandas as pd
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

df = pd.read_csv("career_data.csv")

# Convert to list
df['skills'] = df['skills'].apply(lambda x: x.split(','))
df['interests'] = df['interests'].apply(lambda x: x.split(','))
df['traits'] = df['traits'].apply(lambda x: x.split(','))

# Encode
mlb_skills = MultiLabelBinarizer()
mlb_interests = MultiLabelBinarizer()
mlb_traits = MultiLabelBinarizer()

skills_encoded = mlb_skills.fit_transform(df['skills'])
interests_encoded = mlb_interests.fit_transform(df['interests'])
traits_encoded = mlb_traits.fit_transform(df['traits'])

le_q = LabelEncoder()
df['qualification'] = le_q.fit_transform(df['qualification'])

le_c = LabelEncoder()
df['career'] = le_c.fit_transform(df['career'])

# Combine
X = np.hstack((df[['qualification']].values, skills_encoded, interests_encoded,traits_encoded))
y = df['career']

model = RandomForestClassifier()
model.fit(X, y)

# Save
joblib.dump(model, "model.pkl")
joblib.dump(le_q, "le_q.pkl")
joblib.dump(le_c, "le_c.pkl")
joblib.dump(mlb_skills, "mlb_skills.pkl")
joblib.dump(mlb_interests, "mlb_interests.pkl")
joblib.dump(mlb_traits, "mlb_traits.pkl")


print("Model trained successfully!")