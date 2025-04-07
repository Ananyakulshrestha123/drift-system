import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Home from "./components/home";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            loggedIn ? <Navigate to="/home" /> : <Login setLoggedIn={setLoggedIn} />
          }
        />
        <Route
          path="/home"
          element={
            loggedIn ? <Home /> : <Navigate to="/" />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
