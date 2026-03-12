import React, { useState } from "react";
import { Link } from "react-router-dom";

function Detect(props) {
  const [cameraType, setCameraType] = useState("environment");

  const startSelectedCamera = async (type) => {
    setCameraType(type);
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: type },
    });
    props.videoRef.current.srcObject = stream;
    props.videoRef.current.play();
  };

  return (
    <>
      {/* Title centered */}
      <h1
        className="detect-title"
        style={{ textAlign: "center", marginBottom: "20px" }}
      >
        Detect Your Cattle Breed
      </h1>

      <div className="upload-container">
        {/* Upload Box */}
        <div className="upload-box">
          <h3>Upload Image</h3>
          <input
            type="file"
            accept="image/*"
            onChange={props.handleFileChange}
          />
          {props.preview && (
            <img
              src={props.preview}
              alt="preview"
              className="preview"
              style={{ width: "100%", borderRadius: "12px", marginTop: "12px" }}
            />
          )}
        </div>

        {/* Camera Box */}
        <div className="camera-box">
          <h3>Use Camera</h3>
          <div className="camera-buttons">
            <button onClick={() => startSelectedCamera("user")}>
              Front Camera
            </button>
            <button onClick={() => startSelectedCamera("environment")}>
              Back Camera
            </button>
          </div>
          <br />
          <video ref={props.videoRef} width="300" height="225"></video>
          <br />
          <div style={{ display: "flex", justifyContent: "center", marginTop: "10px" }}>
            <button onClick={props.capturePhoto}>Capture Photo</button>
          </div>
          <canvas
            ref={props.canvasRef}
            width="300"
            height="225"
            style={{ display: "none" }}
          />
        </div>
      </div>

      {/* Predict Button */}
      <div className="predict-container">
        <button className="predict-btn" onClick={props.handleSubmit}>
          Predict
        </button>
      </div>

      {/* Result */}
      {props.result && (
        <div
          className="result"
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginTop: "30px",
            textAlign: "center",
          }}
        >
          <h3>
            Breed: <span className="breed-name">{props.result.breed}</span>
          </h3>
          <p>Confidence: {props.result.confidence}%</p>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${props.result.confidence}%` }}
            ></div>
          </div>
          <Link
            className="know-more"
            to={`/breed-info/${props.result.breed.toLowerCase()}`}
          >
            Know More About This Breed →
          </Link>
        </div>
      )}
    </>
  );
}

export default Detect;