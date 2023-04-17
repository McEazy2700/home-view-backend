from typing import List, Optional
import strawberry
from homes import models

@strawberry.type
class Image:
    id: int
    public_id: str
    url: str
    description: Optional[str] = None


@strawberry.type
class Home:
    id: int
    location: "Location"
    description: Optional[str] = None
    room_count: int
    cover_photo: Optional["Image"] = None
    images: List["Image"]


@strawberry.type(description="Contains all information about where a home is located.")
class Location:
    """
    Contains all information about where a home is located.
    """
    id: int
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    state: "models.StateType"
    lga: "LGA"
    address: Optional[str] = None


@strawberry.type
class LGA:
    id: int
    name: str
    state: models.StateType

