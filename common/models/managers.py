from cloudinary.uploader import upload_image, destroy
from typing import TYPE_CHECKING, Any, List, Self

from common.graphql.types import ModelImageInput
from common.models.base import BaseManager 

CLOUDINARY_HOMIES_FOLDER = "homies"
if TYPE_CHECKING:
    from common.models.models import Image
    from ..graphql.types import ImageType

class ImageManager(BaseManager):
    value: "Image"
    bulk_values: List["Image"]
    gql_type: "Image"
    bulk_gql: List["ImageType"]
    gql: "ImageType"

    def new(self, input: ModelImageInput) -> Self:
        response = upload_image(input.file, folder=CLOUDINARY_HOMIES_FOLDER)
        return super().new(
                url=response.url,
                public_id=response.public_id,
                description=input.description,
                home_id=input.home_id,
                is_cover=input.is_cover
            )

    def bulk_new(self, images: List[ModelImageInput]) -> Self:
        from .models import Image
        new_images: List[Image] = []
        for image in images:
            result = upload_image(image.file, folder=CLOUDINARY_HOMIES_FOLDER)
            new_image = Image(
                    url=result.url,
                    public_id=str(result.public_id),
                    description=image.description,
                    home_id=image.home_id,
                    is_cover=image.is_cover)
            new_images.append(new_image)
        super().bulk_new(new_images)
        return self

    def get(self, id: int) -> Self:
        return super().get(id=id)

    def delete(self, instance: Any|None=None):
        if not instance and not self.value:
            raise ValueError("no instance to delete were found")
        public_id = instance.public_id if instance else self.value.public_id
        destroy(public_id)
        return super().delete()
