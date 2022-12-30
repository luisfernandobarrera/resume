from app import app
from flask_frozen import Freezer
import os
os.environ['LC_ALL'] = 'en_US.utf-8'

DESTINATION = os.getenv("STATIC_DESTINATION", "docs/")

freezer = Freezer(app)
app.config.update(
    FREEZER_DESTINATION=DESTINATION,
    FREEZER_RELATIVE_URLS=True
)

if __name__ == "__main__":
    freezer.freeze()
