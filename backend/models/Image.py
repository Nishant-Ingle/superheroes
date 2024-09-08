from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    """
    Class to represent superhero image.
    """
    url: Optional[str] = None
