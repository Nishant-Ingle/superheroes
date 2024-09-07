import React from 'react';
import { SuperheroTrimmed } from '../models/SuperheroTrimmed';


async function getSuperheroes(): Promise<SuperheroTrimmed[]> {
    const response = await fetch('http://localhost:8000/superheroes');
    const data = await response.json();
    return data as SuperheroTrimmed[];
}


export default async function Page() {
    const superheroes = await getSuperheroes();

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    {superheroes.map((superhero) => (
                        <tr key={superhero.id}>
                            <td>{superhero.id}</td>
                            <td>{superhero.name}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};