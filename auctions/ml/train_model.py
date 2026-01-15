import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_excel("commerce_auction_dataset.xlsx")

# Features and target
X = df.drop("final_winning_price", axis=1)
y = df["final_winning_price"]

# Separate column types
categorical_features = ["category"]
numerical_features = [
    "title_length",
    "description_length",
    "number_of_images"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features)
    ]
)

# ML Pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model.fit(X_train, y_train)

# Accuracy
score = model.score(X_test, y_test)
print(f"✅ Model R² Score: {score:.2f}")

# Save model
joblib.dump(model, "price_model.pkl")
print("💾 Model saved as price_model.pkl")
