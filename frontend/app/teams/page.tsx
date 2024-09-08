import React, {useState} from "react";
import axios, {AxiosResponse} from "axios";
import Form from 'react-bootstrap/Form';
import {Team} from "@/app/models/Team";

export default function Teams() {
    const random = 'random';
    const balanced = 'balanced';
    const [criteria, setCriteria] = useState(random);
    const [team, setTeam] = useState<Team>(null);

    const fetchTeams = (e?: React.FormEvent<HTMLFormElement>) => {
        e?.preventDefault();
        axios.get(`http://localhost:8000/teams`, {
            headers: {
                'Accept': 'application/json'
            },
            params: {
                'criteria': criteria
            }
        }).then((resp: AxiosResponse) => {
            const team: Team = resp.data;
            setTeam(team);
        }).catch(console.error);
    }

    return (
        <div>
            {
                <div className={'container'}>
                    <h2 className={'row mb-3'}>Teams</h2>

                    <Form className={'mb-3 form-check row'} onSubmit={fetchTeams}>
                        <span key={`inline-radio`} className="mb-3">
                            <Form.Check
                                onChange={e => setCriteria(random)}
                                inline
                                checked={criteria === random}
                                label="Random"
                                name="criteria"
                                type={'radio'}
                                id={`radio-random`}
                            />
                            <Form.Check
                                onChange={e => setCriteria(balanced)}
                                inline
                                label="Balanced"
                                name="criteria"
                                type={'radio'}
                                id={`radio-balanced`}
                            />
                            <button className={'btn btn-outline-primary'} type={'submit'}>
                                Fetch Teams
                            </button>
                        </span>
                    </Form>

                    <div className="row m-lg-4">
                            Fetch a team of size 3.
                    </div>


                    {team && (
                        <div className={'container'}>
                            <table className={'table'}>
                                <thead>
                                    <tr className={'row'}>
                                        <th scope={'col'} className={'col-1'}>#</th>
                                        <th scope={'col'} className={'col-2'}>Name</th>
                                        <th scope={'col'} className={'col-1'}>Strength</th>
                                        <th scope={'col'} className={'col-1'}>Speed</th>
                                        <th scope={'col'} className={'col-1'}>Power</th>
                                        <th scope={'col'} className={'col-1'}>Intelligence</th>
                                        <th scope={'col'} className={'col-5'}>Image</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {team?.superheroes.map((superhero) => (
                                        <tr key={superhero.id} className={'row'}>
                                            <td className={'col-1'}>{superhero.id}</td>
                                            <td className={'col-2'}>{superhero.name}</td>
                                            <td className={'col-1'}>{superhero.strength}</td>
                                            <td className={'col-1'}>{superhero.speed}</td>
                                            <td className={'col-1'}>{superhero.power}</td>
                                            <td className={'col-1'}>{superhero.intelligence}</td>
                                            <td className={'col-5'}>
                                                <img src={superhero.image_url} className={'hero-img'}/>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>

                                <tfoot>
                                    <tr className={'row'}>
                                        <td className={'col-1'}>Total</td>
                                        <td className={'col-2'}></td>
                                        <td className={'col-1'}>{team?.team_powerstats.strength}</td>
                                        <td className={'col-1'}>{team?.team_powerstats.speed}</td>
                                        <td className={'col-1'}>{team?.team_powerstats.power}</td>
                                        <td className={'col-1'}>{team?.team_powerstats.intelligence}</td>
                                        <td className={'col-5'}></td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>)
                    }
                </div>
            }
        </div>
    );
}
