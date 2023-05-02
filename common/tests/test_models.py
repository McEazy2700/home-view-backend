import io
import unittest
from PIL import Image as PilImage

from common.graphql.types import ModelImageInput
from common.models.models import Image

from utils.tests.preps import clean_up_test_db, set_up_test_db

def gen_image_bytes() -> bytes:
    img = PilImage.new(mode="RGBA", size=(200, 200))
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="PNG")
    byte_arr = byte_arr.getvalue()
    return byte_arr


class TestModels(unittest.TestCase):
    def setUp(self) -> None:
        set_up_test_db()

    def test_new_image(self):
        img_bytes = gen_image_bytes()
        img = Image.objects().new(ModelImageInput(file=img_bytes, description="test image"))
        self.assertEqual(img.value.description, "test image")
        img.delete()


    def tearDown(self) -> None:
        clean_up_test_db()
