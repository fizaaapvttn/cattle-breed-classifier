import React, { useState, useRef } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import BreedInfo from "./pages/BreedInfo";
import AboutUs from "./pages/AboutUs";
import "./App.css";

/* ---------------- HOME PAGE COMPONENT ---------------- */
function HomePage(props) {
  const navigate = useNavigate();

const goToBreedInfo = () => {
  if (props.result?.breed) {
    const formattedName = props.result.breed.toLowerCase();

    const breedMap = {
      "jersey cow": "jersey cow female diary",
      "red sindhi": "red_sindhi",
      "krishna valley": "krishna_valley",
      "malnad gidda": "malnad_gidda"
    };

    const breedId = breedMap[formattedName] || formattedName;

    navigate(`/breed-info/${breedId}`);
  }
};
  return (
    <div className="home-page">

      {/* Info Panel */}
      <section className="info-panel">
        <h1>Cattle in India</h1>
        <p>
          India has one of the largest cattle populations in the world, with over 300 million animals.
          Cattle are crucial for milk , and draught power. They are integral to agriculture, economy,
          and culture, supporting millions of rural households.
        </p>

        <div className="info-subsection">
          <h3>Why Farmers Raise Cattle</h3>
          <ul>
            <li>🐄 <b>Milk Production:</b> Provides dairy for households and commercial purposes.</li>
            <li>🚜 <b>Agricultural Work:</b> Bulls and oxen assist in ploughing, transportation, and farm labor.</li>
            <li>🌿 <b>Manure:</b> Organic fertilizer for crops, maintaining soil fertility.</li>
            <li>💰 <b>Income Source:</b> Selling milk, calves, and byproducts generates revenue.</li>
            <li>🙏 <b>Cultural Significance:</b> Certain breeds hold religious and traditional importance.</li>
          </ul>
        </div>

        <div className="info-subsection">
          <h3>Benefits for Rural Communities</h3>
          <p>
            Beyond income, cattle contribute to sustainable farming practices and food security.
            They are part of social and cultural life, supporting festivals, rituals, and local traditions.
          </p>
        </div>

        <div className="info-subsection">
          <h3>Popular Breeds in India</h3>
          <p>
            India has numerous indigenous breeds adapted to local climates. Some well-known breeds include:
            <b> Gir, Sahiwal, Hallikar, Dangi, and Red Sindhi</b>.
          </p>
        </div>

        <div className="info-images">
          <img src="amritmahalcowimg.jpg" alt="Cattle 1" />
          <img src="jerseycowimg.webp" alt="Cattle 2" />
          <img src="tharparkercowimg.jpg" alt="Cattle 3" />
        </div>
      </section>

      {/* Project Panel */}
      <section className="project-panel">
        <h2>About Our Project</h2>
        <p>
          This project uses AI to identify the breed of your cattle from an image.
          Farmers and breeders can quickly get breed info and confidence
          scores, helping manage livestock more efficiently.
        </p>
      </section>

      {/* Upload & Camera Panel */}
      <section className="upload-panel">
        <h2>Check Your Cattle Breed</h2>
        <div className="upload-container">

          {/* Upload */}
          <div className="upload-box">
            <h3>Upload Image</h3>
            <input type="file" onChange={props.handleFileChange} accept="image/*" />
            {props.preview && <img src={props.preview} alt="preview" className="preview" />}
          </div>

          {/* Camera */}
          <div className="camera-box">
            <h3>Use Camera</h3>
            {!props.cameraActive ? (
              <button onClick={props.startCamera}>Start Camera</button>
            ) : (
              <>
                <video ref={props.videoRef} width="300" height="225" />
                <button onClick={props.capturePhoto}>Capture Photo</button>
              </>
            )}
            <canvas ref={props.canvasRef} width="300" height="225" style={{ display: "none" }} />
          </div>
        </div>

        <button onClick={props.handleSubmit} disabled={props.loading}>
          {props.loading ? "Predicting..." : "Predict"}
        </button>

        {/* RESULT SECTION */}
        {props.result && !props.result.error && (
          <div className="result">
            <h3>Breed: {props.result.breed}</h3>
            <p>Confidence: {props.result.confidence}%</p>

            <p className="know-more-link" onClick={goToBreedInfo}>
              Know more about "{props.result.breed}"
            </p>
          </div>
        )}

        {props.result && props.result.error && (
          <div className="error">{props.result.error}</div>
        )}
      </section>

      {/* Popular Breeds Panel */}
      <section className="breeds-panel">
        <h2>Popular Breeds by State</h2>
        <div className="breeds-grid">
          {props.popularBreeds.map((b, i) => (
            <div className="breed-card" key={i}>
              <img src={b.image} alt={b.name} />
              <h4>{b.name}</h4>
              <p>{b.state}</p>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}

/* ---------------- MAIN APP ---------------- */
function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  const startCamera = async () => {
    setCameraActive(true);
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    videoRef.current.play();
  };

  const capturePhoto = () => {
    const context = canvasRef.current.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, 300, 225);
    canvasRef.current.toBlob((blob) => {
      setFile(new File([blob], "camera.jpg", { type: "image/jpeg" }));
      setPreview(URL.createObjectURL(blob));
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select or capture an image!");

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Backend error");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Could not connect to backend" });
    } finally {
      setLoading(false);
    }
  };

  const popularBreeds = [
    { name: "Gir", state: "Gujarat", image: "\\gircowimg.jpg" },
    { name: "Hallikar", state: "Karnataka", image: "\\hallikarcowimg.jpg" },
    { name: "Dangi", state: "Maharashtra", image: "\\dangicowimg.jpg" },
    { name: "Red Sindhi", state: "Sindh/Pakistan", image: "redsindhicowimg.webp" },
    { name: "Sahiwal", state: "Punjab", image: "\\sahiwalcowimg.jpg" },
  ];

  return (
    <Router>
      <nav className="navbar">
        <div className="logo">🐄 Cattle Breed Classifier</div>
        <div className="nav-links">
          <Link to="/">Home</Link>
   	  <a href="#detection">Detection</a>
          <Link to="/breed-info">Breed Info</Link>
          <Link to="/about-us">About Us</Link>
        </div>
      </nav>

      <Routes>
        <Route
          path="/"
          element={
            <HomePage
              handleFileChange={handleFileChange}
              startCamera={startCamera}
              capturePhoto={capturePhoto}
              handleSubmit={handleSubmit}
              preview={preview}
              result={result}
              loading={loading}
              cameraActive={cameraActive}
              videoRef={videoRef}
              canvasRef={canvasRef}
              popularBreeds={popularBreeds}
            />
          }
        />
        <Route path="/breed-info" element={<BreedInfo />} />
        <Route path="/breed-info/:id" element={<BreedInfo />} />
        <Route path="/about-us" element={<AboutUs />} />
      </Routes>
    </Router>
  );
}

export default App;