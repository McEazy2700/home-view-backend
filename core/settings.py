from decouple import config
import cloudinary
cloudinary.config(
    cloud_name=str(config("CLOUDINARY_CLOUD_NAME")),
    api_key=str(config("CLOUDINARY_API_KEY")),
    api_secret=str(config("CLOUDINARY_API_SECRET")),
    secure=True
)

TESTING:bool = config("TESTING") == "True"
TEST_DB_URL = str(config("TEST_DB_URL"))
PROD_DB_URL = str(config("PROD_DB_URL"))

DB_URL = TEST_DB_URL if TESTING else PROD_DB_URL
