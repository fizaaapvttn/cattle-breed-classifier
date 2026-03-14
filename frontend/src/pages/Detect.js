import React, { useState } from "react";
import { Link } from "react-router-dom";

function Detect(props) {

  const [cameraType, setCameraType] = useState("environment");

  /* ---------------- Maintenance Tips ---------------- */

  const maintenanceTips = {
    amritmahal: [
      "Provide high energy feed because it is a strong draught breed.",
      "Needs regular exercise and open grazing areas.",
      "Ensure clean drinking water and periodic veterinary checkups."
    ],
    dangi: [
      "Well suited for rainy climates.",
      "Provide balanced fodder and green grass.",
      "Maintain dry shelter during monsoon season."
    ],
    gir: [
      "Provide green fodder, grains and mineral mixture.",
      "Ensure clean and ventilated shelter.",
      "Regular vaccination and milking management."
    ],
    hallikar: [
      "Strong draught breed used for farming work.",
      "Needs open space for movement.",
      "Provide nutritious feed for maintaining strength."
    ],
    hariana: [
      "Good for both milk and draught work.",
      "Provide balanced nutrition with green fodder.",
      "Regular veterinary care is recommended."
    ],
    "jersey cow female diary": [
      "High milk producing breed requiring protein rich diet.",
      "Provide quality fodder and concentrates.",
      "Maintain proper milking hygiene."
    ],
    kankrej: [
      "Provide sufficient green fodder and clean water.",
      "Needs spacious shelter for large body size.",
      "Regular health monitoring required."
    ],
    khillar: [
      "Very active draught breed requiring open space.",
      "Provide nutritious diet and mineral supplements.",
      "Needs regular physical activity."
    ],
    krishna_valley: [
      "Provide strong nutrition for draught work.",
      "Needs clean housing and open field access.",
      "Regular parasite control."
    ],
    malnad_gidda: [
      "Small breed with low maintenance requirement.",
      "Provide natural grazing and simple fodder.",
      "Suitable for hilly regions."
    ],
    ongole: [
      "Large breed needing high nutrition feed.",
      "Provide spacious and clean shelter.",
      "Regular veterinary care important."
    ],
    rathi: [
      "Good milk producing breed.",
      "Provide balanced feed with mineral mixture.",
      "Ensure proper milking management."
    ],
    red_sindhi: [
      "Provide balanced fodder and concentrate feed.",
      "Protect from extreme heat.",
      "Regular vaccination and parasite control."
    ],
    sahiwal: [
      "High milk producing breed requiring rich diet.",
      "Provide green fodder and protein supplements.",
      "Ensure regular milking routine."
    ],
    tharparkar: [
      "Well adapted to dry climates.",
      "Provide sufficient water and dry fodder.",
      "Regular veterinary checkups."
    ],
    vechur: [
      "Small breed with low feed requirement.",
      "Provide natural grazing and basic shelter.",
      "Regular health monitoring."
    ]
  };

  /* ---------------- Feeding Guide ---------------- */

  const feedingGuide = {
    amritmahal: ["Green fodder like maize or grass.", "Dry fodder such as hay or straw.", "Mineral mixture and plenty of water."],
    dangi: ["Fresh green grass and crop residues.", "Dry fodder like rice straw.", "Mineral supplements and clean water."],
    gir: ["Green fodder such as maize and grass.", "Dry fodder and concentrates.", "Mineral mixture for milk production."],
    hallikar: ["Nutritious green fodder.", "Dry fodder and grains for strength.", "Mineral supplements."],
    hariana: ["Green grass and crop residues.", "Balanced concentrate feed.", "Clean drinking water."],
    "jersey cow female diary": ["High protein feed for milk production.", "Green fodder and grains.", "Mineral mixture and vitamins."],
    kankrej: ["Green fodder like maize and sorghum.", "Dry fodder and concentrate feed.", "Mineral supplements."],
    khillar: ["Strong nutritious fodder.", "Dry fodder and grains.", "Mineral mixture for energy."],
    krishna_valley: ["Green grass and crop residues.", "Dry fodder and concentrates.", "Mineral supplements."],
    malnad_gidda: ["Natural grazing grass.", "Small quantity of dry fodder.", "Clean water supply."],
    ongole: ["Green fodder and legumes.", "Dry fodder and grains.", "Mineral supplements."],
    rathi: ["Green fodder and concentrates.", "Dry fodder such as hay.", "Mineral mixture."],
    red_sindhi: ["Green fodder and concentrate mixture.", "Dry fodder such as straw.", "Mineral mixture and water."],
    sahiwal: ["Protein rich fodder.", "Green grass and grains.", "Mineral supplements."],
    tharparkar: ["Dry fodder suitable for dry regions.", "Green fodder when available.", "Mineral mixture."],
    vechur: ["Natural grazing grass.", "Small quantity of dry fodder.", "Clean drinking water."]
  };

  /* ---------------- Vaccination Schedule ---------------- */

  const vaccinationSchedule = [
    {
      name: "FMD (Foot and Mouth Disease)",
      what: "A highly contagious viral disease affecting cattle, goats, and sheep.",
      symptoms: ["Blisters in mouth and tongue", "Sores on feet and hooves", "Fever and excessive drooling", "Difficulty walking or eating"],
      schedule: "Every 6 months"
    },
    {
      name: "HS (Hemorrhagic Septicemia)",
      what: "A serious bacterial disease common during rainy seasons.",
      symptoms: ["High fever", "Swelling in throat and neck", "Breathing difficulty", "Sudden death in severe cases"],
      schedule: "Once every year"
    },
    {
      name: "BQ (Black Quarter)",
      what: "A bacterial infection mainly affecting young cattle.",
      symptoms: ["Swelling in muscles", "Fever and lameness", "Pain in legs or shoulders", "Gas formation under the skin"],
      schedule: "Once every year"
    },
    {
      name: "Brucellosis",
      what: "A bacterial disease that affects the reproductive system.",
      symptoms: ["Abortion in pregnant cows", "Infertility problems", "Reduced milk production"],
      schedule: "Female calves (4-8 months)"
    },
    {
      name: "Anthrax",
      what: "A dangerous bacterial disease found in contaminated soil.",
      symptoms: ["Sudden high fever", "Bleeding from body openings", "Sudden death"],
      schedule: "In high risk areas"
    }
  ];

  /* ---------------- Start Camera ---------------- */

  const startSelectedCamera = async (type) => {
    setCameraType(type);
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: type } });
    props.videoRef.current.srcObject = stream;
    props.videoRef.current.play();
  };

  return (
    <>

      <h1 className="detect-title" style={{ textAlign: "center", marginBottom: "20px" }}>
        Detect Your Cattle Breed
      </h1>

      <div className="upload-container">

        <div className="upload-box">
          <h3>Upload Image</h3>
          <input type="file" accept="image/*" onChange={props.handleFileChange} />
          {props.preview && (
            <img src={props.preview} alt="preview" className="preview"
              style={{ width: "100%", borderRadius: "12px", marginTop: "12px" }} />
          )}
        </div>

        <div className="camera-box">
          <h3>Use Camera</h3>
          <div className="camera-buttons">
            <button onClick={() => startSelectedCamera("user")}>Front Camera</button>
            <button onClick={() => startSelectedCamera("environment")}>Back Camera</button>
          </div>
          <br />
          <video ref={props.videoRef} width="300" height="225"></video>
          <br />
          <div style={{ display: "flex", justifyContent: "center", marginTop: "10px" }}>
            <button onClick={props.capturePhoto}>Capture Photo</button>
          </div>
          <canvas ref={props.canvasRef} width="300" height="225" style={{ display: "none" }} />
        </div>

      </div>

      <div className="predict-container">
        <button className="predict-btn" onClick={props.handleSubmit}>Predict</button>
      </div>

      {props.result && (
        <div className="result" style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "30px", textAlign: "center", width: "100%", maxWidth: "1100px", margin: "30px auto" }}>

          <h3>Breed: <span className="breed-name">{props.result.breed}</span></h3>
          <p>Confidence: {props.result.confidence}%</p>

          <div className="confidence-bar">
            <div className="confidence-fill" style={{ width: `${props.result.confidence}%` }}></div>
          </div>

          <div className="maintenance" style={{ marginTop: "20px", background: "#f4f8ff", padding: "20px", borderRadius: "12px", width: "100%", maxWidth: "900px" }}>
            <h3>🐄 Cattle Maintenance Tips</h3>
            <ul style={{ textAlign: "left" }}>
              {maintenanceTips[props.result.breed?.toLowerCase()]?.map((tip, index) => <li key={index}>{tip}</li>)}
            </ul>
          </div>

          <div className="maintenance" style={{ marginTop: "20px", background: "#f4f8ff", padding: "20px", borderRadius: "12px", width: "100%", maxWidth: "900px" }}>
            <h3>🌾 Feeding Guide</h3>
            <ul style={{ textAlign: "left", paddingLeft: "20px" }}>
              {feedingGuide[props.result.breed?.toLowerCase()]?.map((food, index) => <li key={index}>{food}</li>)}
            </ul>
          </div>

          <div style={{ marginTop: "20px", background: "#fff6f6", padding: "20px", borderRadius: "12px", width: "95%", maxWidth: "700px" }}>
            <h3>💉 Vaccination Schedule</h3>
            {vaccinationSchedule.map((vaccine, index) => (
              <div key={index} style={{ marginBottom: "15px" }}>
                <h4>{vaccine.name}</h4>
                <p><strong>What it is:</strong> {vaccine.what}</p>
                <p><strong>Symptoms:</strong></p>
                <ul style={{ textAlign: "left", paddingLeft: "20px" }}>
                  {vaccine.symptoms.map((sym, i) => <li key={i}>{sym}</li>)}
                </ul>
                <p><strong>Vaccination Time:</strong> {vaccine.schedule}</p>
              </div>
            ))}
          </div>

          <Link className="know-more" to={`/breed-info/${props.result.breed.toLowerCase()}`}>
            Know More About This Breed →
          </Link>

        </div>
      )}

    </>
  );
}

export default Detect;
