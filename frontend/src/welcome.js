import React from "react";
import { useNavigate } from "react-router-dom";
import "./Welcome.css";

function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="welcome-container">
      <div className="overlay">
        <h1>Welcome</h1>
        <h2>Cattle Breed Detection System</h2>

        <button onClick={() => navigate("/info")}>
          Explore Project
        </button>
      </div>
    </div>
  );
}

export default Welcome;