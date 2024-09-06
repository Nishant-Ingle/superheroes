import configparser
import concurrent.futures
import logging
import requests
from logging import Logger
from backend.models.Superhero import Superhero
from backend.service.SuperheroService import SuperheroService

logger: Logger


def log_config():
    """
    Configure logging.
    """
    global logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger('logger')


def fetch_hero(superhero_id: int, hero_api_url: str) -> Superhero | None:
    """
    Fetches a superhero's data from the Superhero API.
    """
    url = f"{hero_api_url}/{superhero_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTPError
        return Superhero.from_dict(response.json())
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching hero %s: %s", superhero_id, e)
        return None  # Indicate error for failed requests


def fetch_heroes_on_start():
    """
    Fetches all heroes in parallel and stores them as Superhero objects in a list.
    """
    config = configparser.ConfigParser()
    config.read("../resources/app.properties")

    max_heroes = int(config["DEFAULT"]["max_heroes"])
    hero_api_url = config["DEFAULT"]["hero_api_url"]

    heroes = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_hero, superhero_id, hero_api_url) for superhero_id in range(1, max_heroes + 1)]

        for future in concurrent.futures.as_completed(futures):
            try:
                hero = future.result()
                if hero:
                    heroes.append(hero)
            except Exception as e:
                print(e)

    logger.info("Successfully fetched %s heroes.", len(heroes))
    superhero_service = SuperheroService.get_instance()
    superhero_service.accept_superhero_list(heroes)


def perform_startup_tasks():
    """
    Performs tasks required at app startup.
    """
    log_config()
    fetch_heroes_on_start()
