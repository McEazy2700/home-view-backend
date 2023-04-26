import unittest

from sqlalchemy.exc import NoResultFound
from strawberry.file_uploads import Upload
from common.models.models import Image

from utils.tests.preps import clean_up_test_db, set_up_test_db
from homes.models.models import Country, Location, State, LGA, Home


class TestNewModels(unittest.TestCase):
    def setUp(self) -> None:
        set_up_test_db()

    def test_country_model(self) -> None:
        """
        Contains all tests related to the country model
        """
        def test_create_country():
            country = Country.objects().new(name="Nigeria", country_code="NGN")
            self.assertEqual(country.value.name, "Nigeria")
            self.assertEqual(country.value.country_code, "NGN")

        def test_get_country():
            country = Country.objects().get(name="Nigeria")
            self.assertEqual(country.value.name, "Nigeria")

        def test_delete_country():
            Country.objects().get(country_code="NGN").delete()

            # Check if deleted row still exists
            self.assertRaises(NoResultFound, lambda: Country.objects().get(country_code="Ngn"))


        test_create_country()
        test_get_country()
        test_delete_country()


    def test_state_models(self):
        """
        Contains all tests related to the state model
        """
        def test_create_state():
            country = Country.objects().new(name="Japan", country_code="JPN")
            assert country.value.id is not None
            new_state = State.objects().new(name="Tokyo", country_id=country.value.id)
            self.assertEqual(new_state.value.name, "Tokyo")

        def test_get_state():
            state = State.objects().get(id=1)
            self.assertIsNotNone(state.value.country)

        def test_get_states_from_country():
            country = Country.objects().get(country_code="jpn")
            self.assertGreater(len(country.value.states), 0)

        test_create_state()
        test_get_state()
        test_get_states_from_country()


    def test_lga_model(self):
        """
        Contains all tests related to the lga model
        """
        def test_new_lga():
            new_country = Country.objects().new("Japan", "JPN")
            assert new_country.value.id is not None
            new_state = State.objects().new(name="Tokyo", country_id=new_country.value.id)
            assert new_state.value.id is not None
            LGA.objects().new(name="Manji", state_id=new_state.value.id)

        def test_get_lga():
            new_lga = LGA.objects().get(id=1)
            self.assertEqual(new_lga.value.name, "Manji")

        def test_get_lga_from_states():
            new_states = State.objects().get(id=1)
            self.assertGreater(len(new_states.value.lgas), 0)

        test_new_lga()
        test_get_lga()
        test_get_lga_from_states()


    def test_location_model(self):
        """
        Contains all tests related to the location model
        """
        def test_new_location():
            new_country = Country.objects().new(name="Japan", country_code="jpn")
            assert new_country.value.id is not None

            new_state = State.objects().new(name="Tokyo", country_id=new_country.value.id)
            assert new_state.value.id is not None
            
            new_lga = LGA.objects().new(name="Manji", state_id=new_state.value.id)
            new_location = Location.objects().new(address="Manji Tokyo", lga_id=new_lga.value.id)
            self.assertEqual(new_location.value.address, "Manji Tokyo")

        def test_get_location():
            location = Location.objects().get(id=1)
            assert location.value.lga is not None
            self.assertEqual(location.value.lga.name, "Manji")

        def test_get_location_from_lga():
            lga = LGA.objects().get(id=1)
            self.assertGreater(len(lga.value.locations), 0)

        test_new_location()
        test_get_location()
        test_get_location_from_lga()


    def test_home_model(self):
        """
        Contains all tests related to the home model
        """
        from common.tests.test_models import gen_image_bytes
        def test_new_home():
            new_country = Country.objects().new(name="Japan", country_code="jpn")
            assert new_country.value.id is not None

            new_state = State.objects().new(name="Tokyo", country_id=new_country.value.id)
            assert new_state.value.id is not None
            
            new_lga = LGA.objects().new(name="Manji", state_id=new_state.value.id)
            new_location = Location.objects().new(address="Manji Tokyo", lga_id=new_lga.value.id)
            assert new_location.value.id is not None

            new_home = Home.objects().new(name="Home for the cool kids", location_id=new_location.value.id)
            assert new_home.value.id is not None
            img_bytes = gen_image_bytes()
            Image.objects().new(Upload(img_bytes), description="home image", home_id=new_home.value.id)

        def test_get_home():
            home = Home.objects().get(id=1)
            self.assertEqual(home.value.location.address, "Manji Tokyo")
            self.assertGreater(len(home.value.images), 0)
            Image.objects().get(id=1).delete()

        def test_get_home_from_location():
            location = Location.objects().get(id=1)
            assert location.value.home is not None
            self.assertEqual(location.value.home.name, "Home for the cool kids")

        test_new_home()
        test_get_home()
        test_get_home_from_location()

    def tearDown(self) -> None:
        clean_up_test_db()
