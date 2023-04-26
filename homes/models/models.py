from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

from homes.models.managers import (
        LGAManager,
        HomeManager,
        StateManager,
        CountryManager,
        LocationManager)

if TYPE_CHECKING:
    from common.models.models import Image

class Country(SQLModel, table=True):
    """
    Refers to a country that could contain many states etc.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    country_code: str = Field(max_length=5, unique=True)
    states: List["State"] = Relationship(back_populates="country")
    
    @classmethod
    def objects(cls) -> CountryManager:
        from homes.graphql.types import CountryType
        fields = ["id", "name", "country_code", "states"]
        return CountryManager(cls, gql_type=CountryType, fields=fields)


class State(SQLModel, table=True):
    """
    Refers to a state that could contain manay LGAs etc.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country_id: int = Field(foreign_key="country.id")
    country: Country = Relationship(
            back_populates="states",
            sa_relationship_kwargs=dict(foreign_keys="[State.country_id]"))
    lgas: List["LGA"] = Relationship(back_populates="state")

    @classmethod
    def objects(cls) -> StateManager: 
        from ..graphql.types import StateType
        fields=["id", "name", "country_id", "country", "lgas"]
        return StateManager(cls, gql_type=StateType, fields=fields)


class LGA(SQLModel, table=True):
    """
    Refers to a local government area that could contaim many location
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    state_id: int = Field(foreign_key="state.id")
    state: State = Relationship(
            back_populates="lgas",
            sa_relationship_kwargs=dict(foreign_keys="[LGA.state_id]"))
    locations: List["Location"] = Relationship(back_populates="lga")

    @classmethod
    def objects(cls) -> LGAManager:
        from ..graphql.types import LGAType
        fields=["id", "name", "state_id", "state", "locations"]
        return LGAManager(cls, gql_type=LGAType, fields=fields)


class Location(SQLModel, table=True):
    """
    Contains all the information for finding a home
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: Optional[str] = Field(default=None)
    longitude: Optional[str] = Field(default=None)
    address: str

    lga_id: Optional[int] = Field(default=None, foreign_key="lga.id")
    lga: Optional[LGA] = Relationship(
            back_populates="locations",
            sa_relationship_kwargs=dict(foreign_keys="[Location.lga_id]"))

    home: Optional["Home"] = Relationship(
            back_populates="location",
            sa_relationship_kwargs=dict(uselist=False))

    @classmethod
    def objects(cls) -> LocationManager:
        from ..graphql.types import LocationType
        fields=["id", "latitude", "logitude", "address", "lga_id", "lga", "home"]
        return LocationManager(cls, gql_type=LocationType, fields=fields)


class Home(SQLModel, table=True):
    """
    This refers to a house or appartment for rent or on sale
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = Field(default=None)
    room_count: int = Field(default=1)
    
    location_id: int = Field(foreign_key="location.id")
    location: Location = Relationship(
            back_populates="home",
            sa_relationship_kwargs=dict(foreign_keys="[Home.location_id]"))
    images: List["Image"] = Relationship(back_populates="home")

    @classmethod
    def objects(cls) -> HomeManager:
        from ..graphql.types import HomeType
        fields=["id", "name", "description", "room_count", "location_id", "location", "images"]
        return HomeManager(cls, gql_type=HomeType, fields=fields)
