from pydantic import BaseModel
from typing import List
from backend.models.Superhero import Superhero
from backend.models.PowerStats import PowerStats


class Team(BaseModel):
    """
    Class representing a team of superheroes.
    """
    superheroes: List[Superhero]
    team_powerstats: PowerStats
