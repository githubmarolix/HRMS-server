import React, { useState,useEffect } from 'react';
import './LandingPage.css';

const LandingPage = () => {
  const [signupData, setSignupData] = useState({
    email: '',
    username: '',
    password: '',
  });

  const [loginData, setLoginData] = useState({
    username: '',
    password: '',
  });

  const handleSignupSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(signupData),
      });

      if (response.ok) {
        // Signup successful, handle success response
        console.log('Signup successful');
      } else {
        // Signup failed, handle error response
        console.error('Signup failed');
      }
    } catch (error) {
      // Handle network or other errors
      console.error('Error occurred while signing up', error);
    }
  };

  const handleLoginSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });

      if (response.ok) {
        // Login successful, handle success response
        console.log('Login successful');
      } else {
        // Login failed, handle error response
        console.error('Login failed');
      }
    } catch (error) {
      // Handle network or other errors
      console.error('Error occurred while logging in', error);
    }
  };

  const handleSignupInputChange = (event) => {
    setSignupData({
      ...signupData,
      [event.target.name]: event.target.value,
    });
  };

  const handleLoginInputChange = (event) => {
    setLoginData({
      ...loginData,
      [event.target.name]: event.target.value,
    });
  };

  return (
    <div className="landing-page">
      <header>
        <h1>Company Name</h1>
      </header>
      <main>
        <section className="signup-section">
          <h2>Sign Up</h2>
          <form onSubmit={handleSignupSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={signupData.username}
              onChange={handleSignupInputChange}
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={signupData.email}
              onChange={handleSignupInputChange}
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={signupData.password}
              onChange={handleSignupInputChange}
            />
            <button type="submit">Sign Up</button>
          </form>
        </section>
        <section className="login-section">
          <h2>Login</h2>
          <form onSubmit={handleLoginSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={loginData.username}
              onChange={handleLoginInputChange}
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={loginData.password}
              onChange={handleLoginInputChange}
            />
            <button type="submit">Login</button>
          </form>
        </section>
      </main>
      <footer>
        <p>&copy; 2023 Marolix HRMS. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
