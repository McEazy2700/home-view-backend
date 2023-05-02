from typing import List
import strawberry
from common.graphql.types import ImageType, ModelImageInput, NewImageSuccess, NewImagesSuccess

from common.models.models import Image
from common.graphql.types import NewImageInput


@strawberry.type
class CommonMutations:
    @strawberry.mutation(description="Create a new image")
    async def new_image(self, input: NewImageInput) -> NewImageSuccess:
        file = await input.file.read(); #type: ignore
        model_input = ModelImageInput(
                file=file,
                home_id=input.home_id,
                description=input.description,
                is_cover=input.is_cover)
        new_image = Image.objects().new(model_input).gql
        return NewImageSuccess(success=True, image=new_image)

    @strawberry.mutation(description="Create many new images at once")
    async def new_images(self, input: List[NewImageInput]) -> NewImagesSuccess:
        model_inputs: List[ModelImageInput] = []
        for item in input:
            file = await item.file.read(); #type: ignore
            model_input = ModelImageInput(
                    file=file,
                    home_id=item.home_id,
                    description=item.description,
                    is_cover=item.is_cover)
            model_inputs.append(model_input)
        manager = Image.objects()
        print(dir(manager))
        new_images = manager.bulk_new(images=model_inputs).bulk_gql
        return NewImagesSuccess(success=True, images=new_images)
