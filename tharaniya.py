# -*- coding: utf-8 -*-
"""tharaniya.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WMrdBrTpGx3rf0UuzGUjTYpfaMQq0O0p
"""

# disease_prediction.py

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Step 1: Load Data
df = pd.read_csv('patient_data.csv')  # Replace with your dataset path

# Step 2: Explore Data
print("First 5 rows:\n", df.head())
print("Missing values:\n", df.isnull().sum())
print("Class distribution:\n", df['disease'].value_counts())

# Step 3: Preprocessing
df.fillna(method='ffill', inplace=True)  # Basic imputation
X = df.drop(['disease', 'patient_id'], axis=1, errors='ignore')
y = df['disease']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Train-test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Step 5: Train Models
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n{name} Performance:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
    plt.title(f'{name} - Confusion Matrix')
    plt.show()

# Step 6: Save Model (Optional)
import joblib
joblib.dump(models['Random Forest'], 'rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Step 7: Predict on New Data
def predict_disease(new_data):
    model = joblib.load('rf_model.pkl')
    scaler = joblib.load('scaler.pkl')
    new_data_scaled = scaler.transform(new_data)
    return model.predict(new_data_scaled)

# Example usage:
# new_patient = pd.DataFrame([[value1, value2, ...]], columns=X.columns)
# prediction = predict_disease(new_patient)
# print("Predicted disease:", prediction)