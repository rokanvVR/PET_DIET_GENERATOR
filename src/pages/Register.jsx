import { useState } from "react";
import API from "../api";

export default function Register({ setPage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      await API.post("/register", null, {
        params: { email, password },
      });

      alert("Registered successfully");
      setPage("login");
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Register</h2>
      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <br /><br />
      <input
        placeholder="Password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />
      <button onClick={handleRegister}>Register</button>
      <p onClick={() => setPage("login")} style={{ cursor: "pointer" }}>
        Already have an account? Login
      </p>
    </div>
  );
}