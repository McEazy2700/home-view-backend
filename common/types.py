from datetime import datetime
from typing import Optional
import strawberry

from strawberry.file_uploads import Upload


@strawberry.input
class NewImageInput:
    file: Upload
    home_id: Optional[int] = None
    description: Optional[str] = None

class CloudinaryType:
    def __init__(self, cloud_res: dict) -> None:
        for key in cloud_res:
            setattr(self, key, cloud_res[key])
        
    bytes: bytes
    created_at: datetime
    format: str
    height: int
    public_id: str
    resource_type: str
    secure_url: str
    signature: str
    type: str
    url: str
    version: int
    width: int

    def __repr__(self) -> str:
        return f"CloudinaryType(secure_url={self.secure_url}, format={self.format}, bytes={self.bytes})"
