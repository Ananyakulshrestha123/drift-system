import { useState } from "react";
import axios from "axios";
import "./Login.css"; // Import the CSS file

function Login({ setLoggedIn }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!username || !password) {
      setError("Please fill in both fields.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });
      if (res.data.success) {
        setLoggedIn(true);
      } else {
        setError(res.data.message || "Login failed");
      }
    } catch (err) {
      setError("Server error or incorrect credentials.");
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <input
        className="login-input"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        className="login-input"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {error && <p className="login-error">{error}</p>}
      <button onClick={handleLogin} className="login-button">Login</button>
    </div>
  );
}

export default Login;
