import React from "react";
import { Link } from "react-router-dom";
import "./HomePage.css";

function HomePage() {
  return (
    <div className="home">

      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-content">
          <h1>Cattle Breed Classifier</h1>
          <p>
            An AI powered system that detects and identifies cattle breeds
            from images. Built to help farmers, researchers, and livestock
            enthusiasts quickly recognize cattle breeds.
          </p>

          <div className="hero-buttons">
            <Link to="/detect" className="btn-primary">
              Start Detection
            </Link>

            <Link to="/breedinfo" className="btn-secondary">
              Explore Breeds
            </Link>
          </div>
        </div>
      </section>


      {/* FEATURES */}
      <section className="features">

        <div className="feature-card">
          <h3>📷 Image Detection</h3>
          <p>
            Upload or capture cattle images and let our AI identify the breed
            instantly.
          </p>
        </div>

        <div className="feature-card">
          <h3>🧠 AI Powered</h3>
          <p>
            Uses deep learning models trained on multiple Indian cattle breeds
            for accurate prediction.
          </p>
        </div>

        <div className="feature-card">
          <h3>📚 Breed Information</h3>
          <p>
            Learn about breed origin, milk production, and characteristics.
          </p>
        </div>

      </section>


      {/* ABOUT */}
      <section className="about">
        <h2>Why This Project?</h2>

        <p>
          India has one of the largest cattle populations in the world.
          Identifying cattle breeds can help improve livestock management,
          dairy production, and breeding practices.
        </p>

        <p>
          This project uses artificial intelligence to simplify breed
          identification and provide useful breed information to farmers
          and students.
        </p>
      </section>


      {/* FOOTER */}
      <footer className="footer">
        <p>© 2026 Cattle Breed Classifier | Built with React + AI</p>
      </footer>

    </div>
  );
}

export default HomePage;