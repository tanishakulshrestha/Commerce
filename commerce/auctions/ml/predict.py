import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "commerce",
    "auctions",
    "ml",
    "price_model.pkl"
)

# 👇 DO NOT load model at import time
_model = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"ML model not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_price(category, title_length, description_length, number_of_images):
    category_map = {
        "Books": 0,
        "Electronics": 1,
        "Fashion": 2,
        "Footwear": 3,
        "Home Decor": 4,
        "Sports": 5
    }

    category = category.strip().title()

    if category not in category_map:
        raise ValueError(f"Unknown category: {category}")

    category_encoded = category_map[category]

    X = np.array([[
        category_encoded,
        title_length,
        description_length,
        number_of_images
    ]])

    model = get_model()   # ✅ lazy load
    return round(float(model.predict(X)[0]), 2)
