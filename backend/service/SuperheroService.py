import logging
from backend.service.Cache import Cache
from typing import List, Dict, Optional, Tuple

import configparser
import sqlite3

from backend.models.Superhero import Superhero


class SuperheroService:
    """
    Manages superhero operations.
    """

    __instance: 'SuperheroService' = None

    config = configparser.ConfigParser()
    config.read("../resources/app.properties")
    db_name = config["DEFAULT"]["db_name"]
    table_name = config["DEFAULT"]["superhero_table_name"]
    disable_superhero_img_update = bool(config["DEFAULT"]["disable_superhero_img_update"])
    superhero_fields = ["id", "name", "strength", "speed", "power", "intelligence", "image_url"]
    cache = Cache()

    insert_statement = ("insert into " + table_name +
                        "(id, name, strength, speed, power, intelligence, image_url) values(?, ?, ?, ?, ?, ?, ?) " +
                        "on conflict do nothing")

    update_statement = ("update " + table_name +
                        " set name = ?, strength = ?, speed = ?, power = ?, intelligence = ?," +
                        " image_url = ? where id = ?")

    @staticmethod
    def get_instance() -> 'SuperheroService':
        """
        Get singleton instance of SuperheroService.
        """
        if not SuperheroService.__instance:
            SuperheroService.__instance = SuperheroService()
        return SuperheroService.__instance

    def init_superhero_list(self, superheroes: List[Tuple]):
        """
        Initialise superheroes list in the DB.
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            # logging.info(self.insert_statement, superheroes)
            cur.executemany(self.insert_statement, superheroes)
            conn.commit()

    def get_superheroes(self, name: Optional[str] = "") -> List[Dict[str, str]]:
        """
        Get superhero list of dictionaries with key as superhero id and value as superhero name.
        """
        if not self.cache.is_empty():
            return [item for item in self.cache.peek_all() if name in item["name"].lower()]

        select_query = "select id, name from " + self.table_name + " where name like '%" + name + "%'"
        heroes = []
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(select_query)
            rows: list[Superhero] = cur.fetchall()
            logging.info(f"Fetched {len(rows)} superheroes from database.")
            for row in rows:
                superhero_entry = {"id": row[0], "name": row[1]}
                self.cache.put(superhero_entry["id"], superhero_entry)
                heroes.append(superhero_entry)
        return heroes

    def get_superhero(self, superhero_id: int) -> Superhero | None:
        """
        Get superhero details from id.
        """
        select_query = ("select id, name, strength, speed, power, intelligence, image_url from " + self.table_name +
                        " where id = " + str(superhero_id))

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(select_query)
            superhero = cur.fetchone()
            if superhero and len(superhero) == 7:
                dict = {}
                for i, f in enumerate(self.superhero_fields):
                    dict[self.superhero_fields[i]] = superhero[i]
                return Superhero.from_dict(dict)

        return None

    def add_superhero(self, superhero: Superhero) -> bool:
        """
        Add superhero to the list if not present.
        """
        if not self.get_superhero(superhero.id):
            with sqlite3.connect(self.db_name) as conn:
                cur = conn.cursor()
                superhero_tuple = (superhero.id,
                                   superhero.name,
                                   superhero.strength,
                                   superhero.speed,
                                   superhero.power,
                                   superhero.intelligence,
                                   superhero.image_url
                                   if not self.disable_superhero_img_update
                                   else "")
                cur.execute(self.insert_statement, superhero_tuple)
                self.cache.put(superhero.id, {"id": superhero.id, "name": superhero.name})
                return True

        return False

    def update_superhero(self, superhero: Superhero) -> bool:
        """
        Update superhero in the list if present.
        """
        curr_superhero = self.get_superhero(superhero.id)
        if curr_superhero:
            with sqlite3.connect(self.db_name) as conn:
                cur = conn.cursor()

                superhero_tuple = (superhero.name,
                                   superhero.strength,
                                   superhero.speed,
                                   superhero.power,
                                   superhero.intelligence,
                                   superhero.image_url
                                   if not self.disable_superhero_img_update
                                   else curr_superhero.image_url,
                                   curr_superhero.id)
                cur.execute(self.update_statement, superhero_tuple)
                self.cache.put(superhero.id, {"id": superhero.id, "name": superhero.name})
                return True

        return False
