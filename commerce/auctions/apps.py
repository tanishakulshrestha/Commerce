from django.apps import AppConfig
import joblib
import os

class AuctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auctions'

    def ready(self):
        from django.conf import settings

        model_path = os.path.join(
            settings.BASE_DIR,
            "auctions",
            "ml",
            "price_model.pkl"
        )

        self.model = joblib.load(model_path)
