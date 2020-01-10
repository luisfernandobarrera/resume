from app import app
from flask_frozen import Freezer

freezer = Freezer(app)
app.config.update(
    FREEZER_DESTINATION="docs/",
    FREEZER_RELATIVE_URLS=True
)

if __name__ == "__main__":
    freezer.freeze()
