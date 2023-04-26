from typing import TYPE_CHECKING, ClassVar, Optional
from sqlmodel import Field, Relationship, SQLModel

from common.models.managers import ImageManager

if TYPE_CHECKING:
    from homes.models.models import Home

class Image(SQLModel, table=True):
    """
    This contains data returned from cloudinary.upload for an image
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    public_id: str
    description: Optional[str] = Field(default=None)
    home_id: Optional[int] = Field(default=None, foreign_key="home.id")
    home: Optional["Home"] = Relationship(
            back_populates="images",
            sa_relationship_kwargs=dict(foreign_keys="[Image.home_id]"))

    @classmethod
    def objects(cls) -> ImageManager:
        from ..graphql.types import ImageType
        fields=["id", "url", "public_id", "description", "home_id", "home"]
        return ImageManager(cls, gql_type=ImageType, fields=fields)
