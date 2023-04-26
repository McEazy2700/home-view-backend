import strawberry
from typing import List, Optional

@strawberry.type
class CountryType:
    id: int
    name: str
    country_code: str
    states: List["StateType"]


@strawberry.type
class StateType:
    id: int
    name: str
    country_id: int
    country: CountryType
    lgas: List["LGAType"]


@strawberry.type
class LGAType:
    id: int
    name: str
    state_id: int
    state: StateType
    locations: List["LocationType"]


@strawberry.type
class LocationType:
    id: int
    address: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    lga_id: Optional[int] = None
    lga: Optional[LGAType] = None


@strawberry.input
class NewLocationInput:
    address: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    lga_id: Optional[int] = None


@strawberry.type
class HomeType:
    id: int
    name: str
    description: Optional[str] = None
    room_count: int
    location_id: int
    location: LocationType
    images: List["ImageType"]


@strawberry.input(description="Required input for new home")
class NewHomeInput:
    """
    Required input for new home
    """
    name: str
    description: Optional[str] = None
    room_count: int
    location_id: int


@strawberry.input(description="Required input for new location")
class LocationInput:
    """
    Required input for new location
    """
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address: str
    state_id: int
    lga_id: int

from common.graphql.types import ImageType
