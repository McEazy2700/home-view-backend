import strawberry
from strawberry.file_uploads import Upload
from common.graphql.types import ImageType

from common.models.models import Image


@strawberry.type
class CommonMutations:
    @strawberry.mutation(description="Create a new image")
    def new_image(self, image: Upload, description: str|None=None) -> ImageType:
        return Image.objects.new(image=image, description=description).gql()
