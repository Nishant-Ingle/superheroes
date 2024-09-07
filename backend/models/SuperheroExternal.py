from typing import Optional
from pydantic import BaseModel, field_validator


class PowerStats(BaseModel):
    """
    Class to represent powerstats of a superhero.
    """
    intelligence: int = 0
    strength: int = 0
    speed: int = 0
    power: int = 0

    @field_validator("intelligence", "strength", "speed", "power", mode="before")
    def validate_powerstats(cls, value):
        if value is None or value == "null":
            return 0
        return int(value)


class Image(BaseModel):
    """
    Class to represent superhero image.
    """
    url: Optional[str] = None


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
