import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "commerce",
    "commerce",
    "auctions",
    "ml",
    "price_model.pkl"
)

_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_price(category, title_length, description_length, number_of_images):
    model = get_model()

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
        return None

    X = np.array([[
        category_map[category],
        title_length,
        description_length,
        number_of_images
    ]])

    return round(float(model.predict(X)[0]), 2)
