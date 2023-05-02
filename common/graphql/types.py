import strawberry
from typing import Any, List, Optional
from strawberry.file_uploads import Upload

@strawberry.type
class ImageType:
    id: int
    url: str
    public_id: str
    is_cover: bool = False
    description: Optional[str] = None
    home_id: Optional[int] = None
    home: Optional["HomeType"] = None


@strawberry.type
class NewImagesSuccess:
    success: bool
    images: List[ImageType]


@strawberry.type
class NewImageSuccess:
    success: bool
    image: ImageType


@strawberry.input
class NewImageInput:
    file: Upload
    is_cover: Optional[bool] = False
    home_id: Optional[int] = None
    description: Optional[str] = None

class ModelImageInput:
    def __init__(self, file: Any,
                 is_cover: bool|None=False,
                 home_id: int|None=None,
                 description: str|None=None) -> None:
        self.file: Any = file
        self.is_cover: Optional[bool] = is_cover
        self.home_id: Optional[int] = home_id
        self.description: Optional[str] = description
        


@strawberry.input
class PageInput:
    limit: Optional[int] = None
    offset: Optional[int] = None

from homes.graphql.types import HomeType
