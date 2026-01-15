import joblib
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "price_model.pkl")
model = joblib.load(model_path)
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

    X = np.array([[category_encoded,
                   title_length,
                   description_length,
                   number_of_images]])

    return round(model.predict(X)[0], 2)
