import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from checker import extract_features 

df = pd.read_csv("data.csv", usecols=[0, 1])
print(df.columns)

df.dropna(inplace=True)
df = df[df["password"].apply(lambda x: isinstance(x, str))]

features = df["password"].apply(extract_features).tolist()
X = pd.DataFrame(features)
y = df["strength"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Classification report: ")
print(classification_report(y_test, y_pred))

joblib.dump(model, "password_model.pkl")
print("Model saved as password_model.pkl")
                                
