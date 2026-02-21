import { useState } from "react";
import API from "../api";

export default function Login({ setPage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await API.post("/login", null, {
        params: { email, password },
      });

      localStorage.setItem("token", res.data.access_token);
      window.location.reload();
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Login</h2>
      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <br /><br />
      <input
        placeholder="Password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />
      <button onClick={handleLogin}>Login</button>
      <p onClick={() => setPage("register")} style={{ cursor: "pointer" }}>
        Don't have an account? Register
      </p>
    </div>
  );
}