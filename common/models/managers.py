import cloudinary
import cloudinary.api
import cloudinary.uploader
from typing import TYPE_CHECKING, Any, Self
from sqlmodel import Session, select
from strawberry.file_uploads import Upload
from common.models.base import BaseManager

from common.types import CloudinaryType
from core.database import DB_ENGINE

if TYPE_CHECKING:
    from common.models.models import Image

class ImageManager(BaseManager):
    value: "Image"
    def new(self, image: Upload, description: str|None=None, home_id: int|None=None) -> Self:
        from common.models.models import Image
        response: CloudinaryType = CloudinaryType(cloudinary.uploader.upload(image))
        with Session(DB_ENGINE) as session:
            new_image = Image(url=response.url,
                    public_id=response.public_id,
                    description=description,
                    home_id=home_id)
            session.add(new_image)
            new_image.home
            session.commit()
            session.refresh(new_image)
            self.value = new_image
            self.value.home
            return self

    def get(self, id: int) -> Self:
        from .models import Image
        with Session(DB_ENGINE) as session:
            statement = select(Image).where(Image.id==id)
            self.value = session.exec(statement).one()
            self.value.home
            return self

    def delete(self, instance: Any|None=None):
        if not instance and not self.value:
            raise ValueError("no instance to delete were found")
        public_id = instance.public_id if instance else self.value.public_id
        cloudinary.uploader.destroy(public_id)
        return super().delete()
