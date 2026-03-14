import React from "react";
import { useNavigate } from "react-router-dom";
import "./OpeningScreen.css";

function OpeningScreen() {

  const navigate = useNavigate();

  const enterApp = () => {
    navigate("/home");
  };

  return (
    <div className="opening-container">
      <div className="opening-card">

        <h1 className="title">Cattle Breed Classifier</h1>

        <p className="subtitle">
          AI powered system to detect cattle breeds from images
        </p>

        <button className="enter-btn" onClick={enterApp}>
          Get Started
        </button>

      </div>
    </div>
  );
}

export default OpeningScreen;