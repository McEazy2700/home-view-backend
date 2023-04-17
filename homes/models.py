import strawberry
from typing import ClassVar, Self
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, Session

from core.database import DB_ENGINE


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    public_id: str
    url: str
    description: Optional[str] = None
    home: Optional["Home"] = Relationship(back_populates="cover_photo")
    room_image: Optional["Home"] = Relationship(back_populates="room_images")


class Home(SQLModel, table=True):
    """
    This refers to a house or appartment for rent or on sale
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = None
    room_count: int = Field(default=1)

    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    cover_photo_id: Optional[int] = Field(default=None, foreign_key="image.id")

    location: Optional["Location"] = Relationship(
            back_populates="home", sa_relationship_kwargs=dict(foreign_keys="[Home.location_id]"))
    cover_photo: Optional[Image] = Relationship(
            back_populates="home", sa_relationship_kwargs=dict(foreign_keys="[Home.cover_photo_id]"))
    room_images: List[Image] = Relationship(back_populates="room_image")


class LGA(SQLModel, table=True):
    """
    This referes to a city or local government area
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    state_id: Optional[int] = Field(default=None, foreign_key="state.id")

    state: Optional["State"] = Relationship(back_populates="lgas")
    locations: List["Location"] = Relationship(back_populates="lga")


class State(SQLModel, table=True):
    """
    Represents as state in a country 
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    locations: List["Location"] = Relationship(back_populates="state")
    lgas: List[LGA] = Relationship(back_populates="state")


    class Manager:
        def __init__(self) -> None:
            self.value: State
            
        def new(self, name: str) -> Self:
            with Session(DB_ENGINE) as session:
                new_state = State(name=name)
                session.add(new_state)
                session.commit()
                session.refresh(new_state)
                self.value = new_state
                return self

        def gql(self) -> "StateType":
            return StateType.from_pydantic(self.value)

    object: ClassVar[Manager] = Manager()


@strawberry.experimental.pydantic.type(State, all_fields=True)
class StateType:
    pass


class Location(SQLModel, table=True):
    """
    This contains all the information for finding a home
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address: str

    state_id: Optional[int] = Field(default=None, foreign_key="state.id")
    lga_id: Optional[int] = Field(default=None, foreign_key="lga.id")

    home: Optional[Home] = Relationship(back_populates="location")
    state: Optional[State] = Relationship(
            back_populates="locations", sa_relationship_kwargs=dict(foreign_keys="[Location.state_id]"))
    lga: Optional[LGA] = Relationship(
            back_populates="locations", sa_relationship_kwargs=dict(foreign_keys="[Location.lga_id]"))



