from typing import TYPE_CHECKING, List, Self

from sqlmodel import Session, select
from core.database import DB_ENGINE

from common.models.base import BaseManager
#  TODO: Implement filterable queries

if TYPE_CHECKING:
    from homes.models.models import Country, State, LGA, Location, Home
    from ..graphql.types import CountryType, StateType, LGAType, LocationType, HomeType


class CountryManager(BaseManager):
    value: "Country"
    gql: "CountryType"
    bulk_gql: List["CountryType"]
    """
    Conatins all database operations that can be caried out on a Country model
    """

    def new(self, name: str, country_code: str) -> Self:
        name=name.capitalize()
        country_code=country_code.upper()
        return super().new(name=name, country_code=country_code)

    def get(self, id: int|None=None, name: str|None=None, country_code: str|None=None) -> Self:
        if name: name = name.capitalize()
        if country_code: country_code = country_code.upper()
        return super().get(id=id, name=name, country_code=country_code)


class StateManager(BaseManager):
    """
    Conatins all database operations that can be caried out on a State model
    """
    value: "State"
    gql: "StateType"

    def get(self, id: int) -> Self:
        return super().get(id=id)


class LGAManager(BaseManager):
    """
    Conatins all database operations that can be caried out on a LocaGovtArea model
    """
    value: "LGA"
    gql: "LGAType"

    def get(self, id: int) -> Self:
        return super().get(id=id)


class LocationManager(BaseManager):
    """
    Conatins all database operations that can be caried out on a Location model
    """
    value: "Location"
    gql: "LocationType"

    def new(self, address: str,
            lga_id: int|None=None,
            latitude: str|None=None,
            longitude: str|None=None) -> Self:

        from .models import Location
        with Session(DB_ENGINE) as session:
            new_item = Location(
                    lga_id=lga_id,
                    address=address,
                    latitude=latitude,
                    longitude=longitude
                )
            session.add(new_item)
            new_item.lga
            new_item.home
            session.commit()
            session.refresh(new_item)
            self.value = new_item
            self.value.lga
            if self.value.lga: self.value.lga.locations
            self.value.home
            return self


    def get(self, id: int) -> Self:
        from homes.models.models import Location
        with Session(DB_ENGINE) as session:
            statement = select(Location).where(Location.id==id)
            self.value = session.exec(statement).one()
            self.value.lga
            self.value.home
            return self


class HomeManager(BaseManager):
    """
    Conatins all database operations that can be caried out on a Home model
    """
    value: "Home"
    gql: "HomeType"

    def new(self, name: str,
            location_id: int,
            description: str|None=None,
            room_count: int|None=None) -> Self:
        from .models import Home

        with Session(DB_ENGINE) as session:
            new_item = Home(name=name, location_id=location_id, description=description)
            if room_count: new_item.room_count = room_count
            session.add(new_item)
            new_item.location
            new_item.images
            session.commit()
            session.refresh(new_item)
            self.value = new_item
            self.value.location
            self.value.images
            return self

    def get(self, id: int) -> Self:
        from homes.models.models import Home
        with Session(DB_ENGINE) as session:
            statement = select(Home).where(Home.id==id)
            self.value = session.exec(statement).one()
            self.value.location
            self.value.images
            return self
