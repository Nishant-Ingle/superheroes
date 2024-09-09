'use client'

import './superheroes.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import React, {useState} from 'react';
import { SuperheroTrimmed } from '../models/SuperheroTrimmed';
import axios, {AxiosResponse} from "axios";
import {Superhero} from "@/app/models/Superhero";


export default function Superheroes() {
    const [search, setSearch] = useState('');

    const [opState, setOpstate] = useState('update');
    const emtpySuperhero = {
        id: 0,
        name: '',
        strength: 0,
        speed: 0,
        power: 0,
        intelligence: 0,
        image_url: '',
    } as Superhero;

    const [isHeroFetched, setIsHeroFetched] = useState(false);
    const [currSuperhero, setCurrSuperhero] = useState(emtpySuperhero);
    const [superheroes, setSuperheroes] = useState([] as SuperheroTrimmed[]);
    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => setSearch(e.target.value);
    const handleSuperheroChange = (key, {target: {value}}: React.ChangeEvent<HTMLInputElement>) => {
        currSuperhero[key] = value;
        setCurrSuperhero(currSuperhero);
    };

    const searchHeroes = (e?: React.FormEvent<HTMLFormElement>) => {
        e?.preventDefault();
        axios.get(`http://localhost:8000/superheroes`, {
            headers: {
                'Accept': 'application/json'
            },
            params: {
                'name': search
            }
        }).then((resp: AxiosResponse) => {
            const superheroData: SuperheroTrimmed[] = resp.data;
            // console.log(superheroData.slice(-2))
            if (superheroData.length === 0) {
                alert('No record found !');
            } else {
                setSuperheroes(superheroData);
            }
        }).catch((err) => {
            console.log(err);
            alert('Failed to fetch superheroes');
        });
    };

    const displaySuperheroDetails = (superheroId) => {
        if (currSuperhero.id == superheroId) {
            return;
        }
        setOpstate('update');

        axios.get(`http://localhost:8000/superheroes/${superheroId}`, {
            headers: {
                'Accept': 'application/json'
            }
        }).then((resp: AxiosResponse) => {
            const fetchedSuperhero = resp.data as Superhero
            setCurrSuperhero(fetchedSuperhero)
            setIsHeroFetched(true);
        }).catch((err) => {
            console.log(err);
            alert('Failed to fetch superhero details');
        });
    }

    const submitHero = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    };

    const resetForm = () => setCurrSuperhero(emtpySuperhero);

    const createOrUpdateSuperhero = () => {
        if (currSuperhero?.id === emtpySuperhero.id) {
            alert('Please fill Superhero details');
            return;
        }

        if (opState === 'update') {
            axios.put(`http://localhost:8000/superheroes/${currSuperhero.id}`,
                currSuperhero,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(() => {
                    alert('Superhero updated !')
                    searchHeroes();
            })
            .catch((err) => {
                console.log(err);
                alert('Failed to update superhero');
            });
        } else if (opState === 'create') {
            axios.post(`http://localhost:8000/superheroes/`,
                currSuperhero,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then((resp: AxiosResponse) => {
                    setCurrSuperhero(resp.data);
                    alert('Superhero created !')
                    searchHeroes();
                }).catch((err) => {
                console.log(err);
                alert('Failed to create superhero');
            });
        }
    };


    return (
        <div className={"container"}>
            <form onSubmit={searchHeroes} className={'row'}>
                <h3 className={'display-4 mb-3'}> Superheroes </h3>
                <div className="form-group input-group mb-3">
                    <button id={'superhero-add-btn'}
                            type="button"
                            className={'btn btn-dark col-auto bi bi-plus-lg'}
                            onClick={() => {setOpstate('create'); setIsHeroFetched(true); resetForm();}} />
                    <input
                        id='superhero-name'
                        className={'form-control col-auto'}
                        type="text"
                        placeholder="Enter Superhero name"
                        value={search}
                        onChange={handleSearchChange} />
                    <button id={'superhero-search-btn btn-submit'} type="submit" className={'btn btn-primary col-auto'}>Search</button>
                </div>
            </form>

            {isHeroFetched &&
            (<form className={'form-group input-group mb-3 row'} onSubmit={submitHero}>
                <div className={'container'}>
                    <div className="row">
                        <div className="col-8">

                            {/*ID and Name*/}
                            <div className="input-group mb-3 row">
                                <div className={'col-3'}>
                                    <label htmlFor="hero-id" className="form-label">ID</label>
                                    <input
                                        onChange={(e) => handleSuperheroChange("id", e)}
                                        readOnly={opState === 'update'}
                                        type={"number"}
                                        min={0}
                                        max={1000}
                                        className="input-group-text"
                                        id="hero-id"
                                        defaultValue={currSuperhero?.id}
                                        key={currSuperhero?.id}/>
                                </div>
                                <div className={'col-9'}>
                                    <label htmlFor="hero-name" className="form-label">Name</label>
                                    <input
                                        onChange={(e) => handleSuperheroChange("name", e)}
                                        type={"text"}
                                        size={68}
                                        className="input-group-text"
                                        id="hero-name"
                                        defaultValue={currSuperhero?.name}
                                        key={currSuperhero?.name}/>
                                </div>
                            </div>

                            {/*Powerstats*/}
                            <div className="input-group mb-3 row">
                                <div className={'col-3'}>
                                    <label htmlFor="hero-str" className="form-label">Strength</label>
                                    <input
                                        onChange={(e) => handleSuperheroChange("strength", e)}
                                        type={"number"}
                                        className="input-group-text"
                                        id="hero-str"
                                        defaultValue={currSuperhero?.strength}
                                        key={currSuperhero?.strength}/>
                                </div>
                                <div className={'col-3'}>
                                    <label htmlFor="hero-spd" className="form-label">Speed</label>
                                    <input
                                        onChange={(e) => handleSuperheroChange("speed", e)}
                                        type={"number"}
                                        className="input-group-text"
                                        id="hero-spd"
                                        defaultValue={currSuperhero?.speed}
                                        key={currSuperhero?.speed}/>
                                </div>
                                <div className={'col-3'}>
                                    <label htmlFor="hero-pow" className="form-label">Power</label>
                                    <input
                                        onChange={(e) => handleSuperheroChange("power", e)}
                                        type={"number"}
                                        className="input-group-text"
                                        id="hero-pow"
                                        defaultValue={currSuperhero?.power}
                                        key={currSuperhero?.power}/>
                                </div>
                                <div className={'col-3'}>
                                    <label htmlFor="hero-intl" className="form-label">Intelligence</label>
                                    <input
                                        onChange={(e) => handleSuperheroChange("intelligence", e)}
                                        type={"number"}
                                        className="input-group-text"
                                        id="hero-intl"
                                        defaultValue={currSuperhero?.intelligence}
                                        key={currSuperhero?.intelligence}/>
                                </div>
                            </div>

                            <div className="input-group mb-3 row">
                                <button id={'wl-create-update-btn'} type="submit" className={'btn btn-outline-primary col-2'} onClick={createOrUpdateSuperhero}>
                                    {opState === 'create' ? 'Create': 'Update'}
                                </button>
                                <button id={'reset'} type={'reset'} className={'btn btn-outline-secondary col-2'} onClick={resetForm}>
                                    Reset
                                </button>
                            </div>
                        </div>

                        {/*Image*/}
                        <div className="col-1 offset-1">
                            {
                                currSuperhero.image_url &&
                                <img className={'hero-img'} src={currSuperhero.image_url} />
                            }
                        </div>
                    </div>
                </div>
            </form>)}

            {superheroes.length !== 0 && (
                <div className={'table-responsive container'}>
                    <table className={'table table-hover'}>
                        <thead>
                            <tr className={'row'}>
                                <th scope={'col'} className={'col'}>#</th>
                                <th scope={'col'} className={'col'}>Name</th>
                            </tr>
                        </thead>
                        <tbody>
                            {superheroes.map((superhero) => (
                                <tr key={superhero.id} className={'row'} onClick={() => displaySuperheroDetails(superhero.id)}>
                                    <td scope={'row'} className={'col'}>{superhero.id}</td>
                                    <td className={'col'}>{superhero.name}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>)
            }
        </div>
    );
};