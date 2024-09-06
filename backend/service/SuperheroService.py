from typing import List, Dict, Optional

from backend.models.Superhero import Superhero


class SuperheroService:
    """
    Manages superhero operations.
    """

    __instance: 'SuperheroService' = None
    __superheroes: Dict[int, Superhero] = {}

    @staticmethod
    def get_instance() -> 'SuperheroService':
        """
        Get singleton instance of SuperheroService.
        """
        if not SuperheroService.__instance:
            SuperheroService.__instance = SuperheroService()
        return SuperheroService.__instance

    def accept_superhero_list(self, superheroes: List[Superhero]) -> List[Dict[int, Superhero]]:
        """
        Update superheroes list with supplied one.
        """
        self.__superheroes = {superhero.id: superhero for superhero in superheroes}

    def get_superheroes(self, name: Optional[str]) -> List[Dict[int, str]]:
        """
        Get superhero list of dictionaries with key as superhero id and value as superhero name.
        """
        return [{superhero_id: superhero.name} for superhero_id, superhero in self.__superheroes.items()
                if name in superhero.name.lower()]

    def get_superhero(self, superhero_id: int) -> Superhero:
        """
        Get superhero details from id.
        """
        return self.__superheroes.get(superhero_id)

    def add_superhero(self, superhero: Superhero) -> bool:
        """
        Add superhero to the list if not present.
        """
        if superhero.id not in self.__superheroes:
            self.__superheroes[superhero.id] = superhero
            return True

        return False

    def update_superhero(self, superhero: Superhero) -> bool:
        """
        Update superhero in the list if present.
        """
        if superhero.id in self.__superheroes:
            self.__superheroes[superhero.id] = superhero
            return True

        return False
