import React, { useState } from "react";
import httpClient from "../../../httpClient";

export const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const registerUser = async () => {
    try {
      const response = await httpClient.post("http://localhost:5000/register", {
        email,
        password,
      });

      // Assuming successful registration, redirect to another page
      console.log("User registered successfully:", response.data);

      window.location.href = "/"; // Redirect to homepage

    } catch (error) {
      if (error.response && error.response.status === 409) {
        alert("User already exists with this email.");
      } else {
        console.error("Registration failed:", error);
        alert("Registration failed. Please try again.");
      }
    }
  };

  return (
    <div>
      <h1>Create an account</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <label>Email: </label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="button" onClick={registerUser}>
          Register
        </button>
      </form>
    </div>
  );
};
