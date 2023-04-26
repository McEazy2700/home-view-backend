from typing import Optional
import strawberry

@strawberry.type
class ImageType:
    id: int
    url: str
    public_id: str
    description: Optional[str] = None
    home_id: Optional[int] = None
    home: Optional["HomeType"] = None


@strawberry.input
class PageInput:
    limit: Optional[int] = None
    offset: Optional[int] = None

from homes.graphql.types import HomeType
