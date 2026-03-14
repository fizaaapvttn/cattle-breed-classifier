import React, { useState, useRef } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
import BreedInfo from "./pages/BreedInfo";
import AboutUs from "./pages/AboutUs";
import "./App.css";
import Detect from "./pages/Detect";
import OpeningScreen from "./pages/OpeningScreen";
import Health from "./pages/Health";   // ← NEW

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

  const goToDetect = () => {
    navigate("/detect");
  };

  return (
    <div className="home-page">

      {/* Info Panel */}
      <section className="info-panel">
        <h1>Cattle in India</h1>

        <p>
          India has one of the largest cattle populations in the world, with over 300 million animals.
          Cattle are crucial for milk, and draught power. They are integral to agriculture, economy,
          and culture, supporting millions of rural households.
        </p>

        <div className="info-subsection">
          <h3>Why Farmers Raise Cattle</h3>
          <ul>
            <li>🐄 <b>Milk Production:</b> Provides dairy for households and commercial purposes.</li>
            <li>🚜 <b>Agricultural Work:</b> Bulls and oxen assist in ploughing, transportation, and farm labor.</li>
            <li>🌿 <b>Manure:</b> Organic fertilizer for crops.</li>
            <li>💰 <b>Income Source:</b> Selling milk and calves generates revenue.</li>
            <li>🙏 <b>Cultural Significance:</b> Some breeds hold religious importance.</li>
          </ul>
        </div>

        <div className="info-images">
          <img src="amritmahalcowimg.jpg" alt="Cattle 1" />
          <img src="jerseycowimg.jpeg" alt="Cattle 2" />
          <img src="tharparkercowimg.jpg" alt="Cattle 3" />
        </div>
      </section>

      {/* Project Panel */}
      <section className="project-panel">
        <h2>About Our Project</h2>
        <p>
          Our project uses Artificial Intelligence to detect cattle breeds
          from uploaded images or camera input.
        </p>
        <div className="about-detect-btn">
          <Link to="/detect">
            <button>Detect Cattle Breed</button>
          </Link>
        </div>
      </section>

      {/* Popular Breeds */}
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


/* ---------------- NAVBAR LAYOUT ---------------- */

function Layout({ children }) {

  const location = useLocation();

  return (
    <>
      {location.pathname !== "/" && (

        <nav className="navbar">

          <div className="logo">🐄 Cattle Breed Classifier</div>

          <div className="nav-links">
            <Link to="/home">Home</Link>
            <Link to="/detect">Detection</Link>
            <Link to="/breed-info">Breed Info</Link>
            <Link to="/health">Health</Link>   {/* ← NEW */}
            <Link to="/about-us">About Us</Link>
          </div>

        </nav>

      )}

      {children}

    </>
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

  /* -------- FILE UPLOAD -------- */
  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    if (!selected.type.startsWith("image/")) {
      alert("Please upload an image file");
      return;
    }
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  /* -------- CAMERA START -------- */
  const startCamera = async () => {
    setCameraActive(true);
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    videoRef.current.play();
  };

  /* -------- CAPTURE PHOTO -------- */
  const capturePhoto = () => {
    const context = canvasRef.current.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, 300, 225);
    canvasRef.current.toBlob((blob) => {
      if (!blob) return;
      const imageFile = new File([blob], "camera.jpg", { type: "image/jpeg" });
      setFile(imageFile);
      setPreview(URL.createObjectURL(blob));
    });
  };

  /* -------- SEND TO BACKEND -------- */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select or capture an image!");
      return;
    }
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

  /* -------- BREED LIST -------- */
  const popularBreeds = [
    { name: "Gir",       state: "Gujarat",          image: "/gircowimg.jpg" },
    { name: "Hallikar",  state: "Karnataka",         image: "/hallikarcowimg.jpg" },
    { name: "Dangi",     state: "Maharashtra",       image: "/dangicowimg.jpg" },
    { name: "Red Sindhi",state: "Sindh/Pakistan",    image: "/redsindhicowimg.webp" },
    { name: "Sahiwal",   state: "Punjab",            image: "/sahiwalcowimg.jpg" }
  ];

  return (
    <Router>
      <Layout>
        <Routes>

          <Route path="/" element={<OpeningScreen />} />

          <Route
            path="/home"
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

          <Route
            path="/detect"
            element={
              <Detect
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
              />
            }
          />

          <Route path="/breed-info"      element={<BreedInfo />} />
          <Route path="/breed-info/:id"  element={<BreedInfo />} />
          <Route path="/health"          element={<Health />} />   {/* ← NEW */}
          <Route path="/about-us"        element={<AboutUs />} />

        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
