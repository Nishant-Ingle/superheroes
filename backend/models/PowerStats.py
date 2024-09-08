from pydantic import BaseModel, field_validator

from backend.models.Superhero import Superhero


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

    def increment_powerstats(self, superhero: Superhero):
        for field in vars(self).keys():
            setattr(self, field, getattr(self, field) + getattr(superhero, field))
