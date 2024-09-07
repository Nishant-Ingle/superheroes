'use client'

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

const LoginForm = () => {
    const { register, handleSubmit, errors } = useForm();
    const [errorMessage, setErrorMessage] = useState('');

    const onSubmit = async (data) => {
        try {
            const response = await axios.post('/api/login', data);
            // Handle successful login (e.g., redirect to dashboard)
            console.log('Login successful:', response.data);
        } catch (error) {
            setErrorMessage(error.response?.data?.message || 'Login failed');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input type="text" name="username" placeholder="Username" {...register('username', { required: true })} />
            {errors?.username && <p>Username is required</p>}
            <input type="password" name="password" placeholder="Password" {...register('password', { required: true })} />
            {errors?.password && <p>Password is required</p>}
            <button type="submit">Login</button>
            {errorMessage && <p>{errorMessage}</p>}
        </form>
    );
};

export default LoginForm;