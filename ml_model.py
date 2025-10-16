import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

# Load features
df = pd.read_csv('processed_features.csv')

# Features and target
X = df[['CPU_avg', 'Memory_avg', 'Disk_avg', 'InputActive']]
y = df['Idle']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on test set
y_pred = clf.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")
print("Confusion Matrix:\n", cm)

# Save model
joblib.dump(clf, 'idle_predictor.pkl')
print("Model saved as idle_predictor.pkl")
