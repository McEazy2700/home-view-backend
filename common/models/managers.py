import cloudinary
import cloudinary.api
import cloudinary.uploader
from typing import TYPE_CHECKING, Any, Self
from strawberry.file_uploads import Upload
from common.models.base import BaseManager

from common.types import CloudinaryType

if TYPE_CHECKING:
    from common.models.models import Image
    from ..graphql.types import ImageType

class ImageManager(BaseManager):
    value: "Image"
    gql: "ImageType"

    def new(self, image: Upload, description: str|None=None, home_id: int|None=None) -> Self:
        response: CloudinaryType = CloudinaryType(cloudinary.uploader.upload(image))
        return super().new(url=response.url, public_id=response.public_id, description=description, home_id=home_id)

    def get(self, id: int) -> Self:
        return super().get(id=id)

    def delete(self, instance: Any|None=None):
        if not instance and not self.value:
            raise ValueError("no instance to delete were found")
        public_id = instance.public_id if instance else self.value.public_id
        cloudinary.uploader.destroy(public_id)
        return super().delete()
