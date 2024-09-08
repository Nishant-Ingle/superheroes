import random

import configparser

from backend.models.PowerStats import PowerStats
from backend.models.Team import Team
from backend.service.SuperheroService import SuperheroService

superhero_service = SuperheroService.get_instance()
config = configparser.ConfigParser()
config.read("../resources/app.properties")
team_size = int(config["DEFAULT"]["team_member_count"])
max_heroes = int(config["DEFAULT"]["max_heroes"])
team_size = min(team_size, max_heroes)


def get_random_team() -> Team:
    superhero_list = superhero_service.get_random_superheroes(team_size)
    combined_team_powerstats = PowerStats()
    for superhero in superhero_list:
        combined_team_powerstats.increment_powerstats(superhero)
    return Team(superheroes=superhero_list, team_powerstats=combined_team_powerstats)


def generate_team(criteria) -> Team:
    return get_balanced_team() if criteria == 'balanced' else get_random_team()


def get_balanced_team() -> Team:
    """
    Get a balanced list of superheroes in terms of powerstats.

    1. Select any superhero randomly.
    2. Check which attribute is lowest for it and select another superhero which has this value highest.
    3. Now again compute the lowest attribute and select another superhero which has this value highest.
    """

    combined_team_powerstats = PowerStats()
    superhero_list = []

    for _ in range(team_size):
        if not superhero_list:
            all_superheroes = superhero_service.get_superheroes()
            idx = random.randint(1, len(all_superheroes))
            first_superhero = superhero_service.get_superhero(idx)
            superhero_list.append(first_superhero)
            combined_team_powerstats.increment_powerstats(first_superhero)
        else:
            team_attr_dict = vars(combined_team_powerstats)
            min_stat = min(team_attr_dict, key=lambda k: team_attr_dict[k])
            next_superhero = superhero_service.get_superhero_by_stat(min_stat, not_in=set(map(lambda t: t.id, superhero_list)))
            superhero_list.append(next_superhero)
            combined_team_powerstats.increment_powerstats(next_superhero)

    return Team(superheroes=superhero_list, team_powerstats=combined_team_powerstats)
