import unittest

from strawberry.file_uploads import Upload
from common.graphql.types import ImageType
from common.models.models import Image
from common.tests.test_models import gen_image_bytes
from common.utils.model_graphql_utils import model_to_strawberry

from utils.tests.preps import clean_up_test_db, set_up_test_db


class TestGraphql(unittest.TestCase):
    def setUp(self) -> None:
        set_up_test_db()
        return super().setUp()

    def test_image_to_image_type(self):
        img_bytes = gen_image_bytes()
        new_image = Image.objects.new(Upload(img_bytes), description="Testing gql")
        image_type = model_to_strawberry(
                ImageType,
                Image, new_image.value,
                ["id", "url", "public_id", "description", "home_id"]
            )
        print({"the_image_type": image_type})


    def tearDown(self) -> None:
        clean_up_test_db()
