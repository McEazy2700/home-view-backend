import cloudinary
import cloudinary.api
import cloudinary.uploader
from typing import TYPE_CHECKING, Any, List, Self, cast
from sqlmodel import Session
from strawberry.file_uploads import Upload
from common.models.base import BaseManager

from common.types import CloudinaryType, NewImageInput
from core.database import DB_ENGINE

if TYPE_CHECKING:
    from common.models.models import Image
    from ..graphql.types import ImageType

class ImageManager(BaseManager):
    value: "Image"
    bulk_values: List["Image"]
    gql_type: "Image"
    bulk_gql: List["ImageType"]
    gql: "ImageType"

    def new(self, image: Upload, description: str|None=None, home_id: int|None=None) -> Self:
        response = cloudinary.uploader.upload_image(image)
        return super().new(url=response.url, public_id=response.public_id, description=description, home_id=home_id)

    def bulk_new(self, images: List[NewImageInput]) -> Self:
        from .models import Image
        new_images: List[Image] = []
        for image in images:
            result = cloudinary.uploader.upload_image(image.file)
            new_image = Image(
                    url=result.url,
                    public_id=str(result.public_id),
                    description=image.description,
                    home_id=image.home_id)
            new_images.append(new_image)

        with Session(DB_ENGINE) as session:
            session.add_all(new_images)
            session.commit()
            for image in new_images:
                session.refresh(image)
        self.bulk_values = new_images
        images_gql = list(map(lambda img: self.__parse_gql(img), new_images))
        self.bulk_gql = cast(List[ImageType], images_gql)
        return self

    def get(self, id: int) -> Self:
        return super().get(id=id)

    def delete(self, instance: Any|None=None):
        if not instance and not self.value:
            raise ValueError("no instance to delete were found")
        public_id = instance.public_id if instance else self.value.public_id
        cloudinary.uploader.destroy(public_id)
        return super().delete()
