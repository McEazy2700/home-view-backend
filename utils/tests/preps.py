from sqlmodel import SQLModel
from core.database import DB_ENGINE
from core.settings import TESTING


class TestingError(Exception):
    pass

def set_up_test_db():
    if not TESTING:
        raise TestingError(
                "Enviroment is not configured for testing",
                "Try setting TESTING enviroment variable to True"
            ) 
    new_testing = """
    ##########################################
    Setting up testing database
    ##########################################
    """
    print(new_testing)
    SQLModel.metadata.create_all(DB_ENGINE)


def clean_up_test_db():
    cleaning = """
    ##########################################
    Cleaning up testing database
    ##########################################
    """
    print(cleaning)
    SQLModel.metadata.drop_all(DB_ENGINE)
