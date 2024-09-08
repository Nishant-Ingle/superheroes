from pydantic import BaseModel

from backend.models.Image import Image
from backend.models.PowerStats import PowerStats


class SuperheroExternal(BaseModel):
    """
    Class to represent a superhero.
    """
    id: int
    name: str
    powerstats: PowerStats = PowerStats()
    image: Image = Image()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}."
