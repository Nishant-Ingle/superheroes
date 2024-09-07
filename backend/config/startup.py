import configparser
import concurrent.futures
import logging
from typing import List, Tuple

import requests
import sqlite3
from logging import Logger
from backend.models.SuperheroExternal import SuperheroExternal
from backend.service.SuperheroService import SuperheroService

logger: Logger
config: configparser.ConfigParser


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


def fetch_hero(superhero_id: int, hero_api_url: str) -> Tuple | None:
    """
    Fetches a superhero's data from the Superhero API.
    """
    url = f"{hero_api_url}/{superhero_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTPError
        superhero_ext = SuperheroExternal.from_dict(response.json())
        return (superhero_ext.id,
                superhero_ext.name,
                superhero_ext.powerstats.strength,
                superhero_ext.powerstats.speed,
                superhero_ext.powerstats.power,
                superhero_ext.powerstats.intelligence,
                superhero_ext.image.url)

    except requests.exceptions.RequestException as e:
        logging.error("Error fetching hero %s: %s", superhero_id, e)
        return None  # Indicate error for failed requests


def fetch_heroes_on_start(db_name, table_name):
    """
    Fetches all heroes in parallel and stores them as Superhero objects in a list.
    :param table_name:
    """
    max_heroes = int(config["DEFAULT"]["max_heroes"])
    hero_api_url = config["DEFAULT"]["hero_api_url"]

    heroes: List[Tuple] = []
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
    superhero_service.init_superhero_list(heroes)


def create_database(db_name, table_name):
    """
    Create a database and table if not present
    """
    sql_statement = "create table if not exists " + table_name + \
        """ (id integer primary key,
            name text,
            intelligence integer,
            strength integer,
            speed integer,
            power integer,
            image_url text)
        """

    conn = None
    try:
        # Create DB if not present
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Create table if not present
        cursor.execute(sql_statement)

        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def db_ops(db_name, table_name):
    """
    Sqlite DB related config.
    """
    create_database(db_name, table_name)


def perform_startup_tasks():
    """
    Performs tasks required at app startup.
    """
    global config
    config = configparser.ConfigParser()
    config.read("../resources/app.properties")

    db_name = config["DEFAULT"]["db_name"]
    table_name = config["DEFAULT"]["superhero_table_name"]
    db_ops(db_name, table_name)
    log_config()
    logger.info("Starting application backend...")
    fetch_heroes_on_start(db_name, table_name)
    SuperheroService.get_instance().get_superheroes()
