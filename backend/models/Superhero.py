from pydantic import BaseModel


class Superhero(BaseModel):
    """
    Class to represent a superhero.
    """
    id: int
    name: str
    strength: int = 0
    speed: int = 0
    power: int = 0
    intelligence: int = 0
    image_url: str = ""

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}."

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)
