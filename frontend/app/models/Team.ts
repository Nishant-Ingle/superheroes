import {Superhero} from "@/app/models/Superhero";
import {PowerStats} from "@/app/models/PowerStats";

export type Team = {
    superheroes: Superhero[];
    team_powerstats: PowerStats;
};