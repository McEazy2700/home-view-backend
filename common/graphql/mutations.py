from typing import List
import strawberry
from strawberry.file_uploads import Upload
from common.graphql.types import ImageType

from common.models.models import Image
from common.types import NewImageInput


@strawberry.type
class CommonMutations:
    @strawberry.mutation(description="Create a new image")
    def new_image(self, image: Upload, description: str|None=None) -> ImageType:
        return Image.objects().new(image=image, description=description).gql

    @strawberry.mutation(description="Create many new images at once")
    def new_images(self, input: List[NewImageInput]) -> List[ImageType]:
        return Image.objects().bulk_new(images=input).bulk_gql
