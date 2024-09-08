import {PowerStats} from "@/app/models/PowerStats";

export interface Superhero extends PowerStats{
    id: number;
    name: string;
    image_url: string;
}