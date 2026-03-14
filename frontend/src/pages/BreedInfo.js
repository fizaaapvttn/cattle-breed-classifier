import React, { useState } from "react";
import "./BreedInfo.css";
import { useParams } from "react-router-dom";
import { useEffect } from "react";
const breeds = [
  {
    id: "amritmahal",
    name: "Amritmahal",
    origin: "Karnataka",
    type: "Draught",
    milkPerDay: "1–3 liters",
    milkPerLactation: "500–800 liters",
    lifespan: "12–15 years",
    weight: "340–400 kg",
    climate: "Dry and semi-arid",
    usedFor: "Heavy agricultural work and transport",
    special: "Very strong and excellent endurance",
    image: "/amritmahalcowimg.jpg"
  },
  {
    id: "dangi",
    name: "Dangi",
    origin: "Maharashtra",
    type: "Dual Purpose",
    milkPerDay: "2–5 liters",
    milkPerLactation: "600–1200 liters",
    lifespan: "12–15 years",
    weight: "300–350 kg",
    climate: "Heavy rainfall regions",
    usedFor: "Milk and ploughing",
    special: "Highly disease resistant",
    image: "/dangicowimg.jpg"
  },
  {
    id: "gir",
    name: "Gir",
    origin: "Gujarat",
    type: "Dairy",
    milkPerDay: "10–15 liters",
    milkPerLactation: "2000–3000 liters",
    lifespan: "12–15 years",
    weight: "385–475 kg",
    climate: "Hot and dry",
    usedFor: "High-quality A2 milk production",
    special: "Top indigenous dairy breed",
    image: "/gircowimg.jpg"
  },
  {
    id: "hallikar",
    name: "Hallikar",
    origin: "Karnataka",
    type: "Draught",
    milkPerDay: "1–3 liters",
    milkPerLactation: "500–700 liters",
    lifespan: "12–15 years",
    weight: "300–350 kg",
    climate: "Dry regions",
    usedFor: "Fast ploughing",
    special: "Very agile and energetic",
    image: "/hallikarcowimg.jpg"
  },
  {
    id: "hariana",
    name: "Hariana",
    origin: "Haryana",
    type: "Dual Purpose",
    milkPerDay: "8–10 liters",
    milkPerLactation: "1500–2500 liters",
    lifespan: "12–15 years",
    weight: "400–500 kg",
    climate: "North Indian plains",
    usedFor: "Milk and farming",
    special: "Strong and productive",
    image: "/harianacowimg3.jpg"
  },
  {
    id: "jersey cow female diary",
    name: "Jersey",
    origin: "Jersey Island (UK)",
    type: "Dairy",
    milkPerDay: "15–25 liters",
    milkPerLactation: "4000–6000 liters",
    lifespan: "15–20 years",
    weight: "400–450 kg",
    climate: "Moderate climates",
    usedFor: "Commercial dairy farming",
    special: "High butterfat milk (5%)",
    image: "/jerseycowimg.jpeg"
  },
  {
    id: "kankrej",
    name: "Kankrej",
    origin: "Gujarat",
    type: "Dual Purpose",
    milkPerDay: "8–12 liters",
    milkPerLactation: "1800–2600 liters",
    lifespan: "12–15 years",
    weight: "500–550 kg",
    climate: "Hot and dry",
    usedFor: "Milk and heavy draught work",
    special: "Strong curved horns",
    image: "/kankrejcowimg (2).jpg"
  },
  {
    id: "khillar",
    name: "Khillar",
    origin: "Maharashtra",
    type: "Draught",
    milkPerDay: "2–4 liters",
    milkPerLactation: "500–800 liters",
    lifespan: "12–15 years",
    weight: "350–400 kg",
    climate: "Dry zones",
    usedFor: "Traditional farming",
    special: "Tall and muscular body",
    image: "/khillarcowimg.jpg"
  },
  {
    id: "krishna_valley",
    name: "Krishna Valley",
    origin: "Karnataka & Maharashtra",
    type: "Draught",
    milkPerDay: "3–6 liters",
    milkPerLactation: "800–1200 liters",
    lifespan: "12–15 years",
    weight: "550–650 kg",
    climate: "River basin areas",
    usedFor: "Heavy ploughing",
    special: "Large and powerful breed",
    image: "/krishnavalleycowimg.jpg"
  },
  {
    id: "malnad_gidda",
    name: "Malnad Gidda",
    origin: "Karnataka",
    type: "Dairy",
    milkPerDay: "2–4 liters",
    milkPerLactation: "500–1000 liters",
    lifespan: "15 years",
    weight: "200–250 kg",
    climate: "Hilly and humid regions",
    usedFor: "Low maintenance dairy farming",
    special: "Smallest indigenous cattle of Karnataka",
    image: "/malnadgiddacowimg.jpg"
  },
  {
    id: "ongole",
    name: "Ongole",
    origin: "Andhra Pradesh",
    type: "Dual Purpose",
    milkPerDay: "5–8 liters",
    milkPerLactation: "1000–1500 liters",
    lifespan: "12–15 years",
    weight: "600–700 kg",
    climate: "Tropical",
    usedFor: "Breeding and farming",
    special: "Exported worldwide for breeding",
    image: "/ongolecowimg.png"
  },
  {
    id: "rathi",
    name: "Rathi",
    origin: "Rajasthan",
    type: "Dairy",
    milkPerDay: "8–10 liters",
    milkPerLactation: "1500–3000 liters",
    lifespan: "12–15 years",
    weight: "350–450 kg",
    climate: "Arid regions",
    usedFor: "Milk production in desert areas",
    special: "Excellent heat tolerance",
    image: "/rathicowimg.jpg"
  },
  {
    id: "red_sindhi",
    name: "Red Sindhi",
    origin: "Sindh region",
    type: "Dairy",
    milkPerDay: "8–12 liters",
    milkPerLactation: "2000–3000 liters",
    lifespan: "12–15 years",
    weight: "325–400 kg",
    climate: "Hot climates",
    usedFor: "Heat tolerant dairy farming",
    special: "Reddish brown coat",
    image: "/redsindhicowimg.webp"
  },
  {
    id: "sahiwal",
    name: "Sahiwal",
    origin: "Punjab",
    type: "Dairy",
    milkPerDay: "10–16 liters",
    milkPerLactation: "2000–3500 liters",
    lifespan: "12–15 years",
    weight: "400–500 kg",
    climate: "Hot regions",
    usedFor: "Commercial dairy farming",
    special: "Calm temperament and high milk yield",
    image: "/sahiwalcowimg.jpg"
  },
  {
    id: "tharparkar",
    name: "Tharparkar",
    origin: "Rajasthan",
    type: "Dual Purpose",
    milkPerDay: "8–10 liters",
    milkPerLactation: "1800–2600 liters",
    lifespan: "12–15 years",
    weight: "400–500 kg",
    climate: "Desert regions",
    usedFor: "Milk and drought farming",
    special: "Highly drought resistant",
    image: "/tharparkercowimg.jpg"
  },
  {
    id: "vechur",
    name: "Vechur",
    origin: "Kerala",
    type: "Dairy",
    milkPerDay: "2–4 liters",
    milkPerLactation: "500–1000 liters",
    lifespan: "15–18 years",
    weight: "130–150 kg",
    climate: "Humid regions",
    usedFor: "Small-scale dairy farming",
    special: "Smallest cattle breed in the world",
    image: "/vechurcowimg.jpg"
  }
];
function BreedInfo() {
 const { id } = useParams();
const [selectedBreed, setSelectedBreed] = useState(null);
    useEffect(() => {
    if (id) {
      const found = breeds.find((b) => b.id === id);
      if (found) {
        setSelectedBreed(found);
      }
    }
  }, [id]);

  return (
    <div className="breedinfo-container">
      <div className="breed-grid">
        {breeds.map((breed) => (
          <div
            className="breed-card"
            key={breed.id}
            onClick={() => setSelectedBreed(breed)}
          >
            <img src={breed.image} alt={breed.name} />
            <h2>{breed.name}</h2>
          </div>
        ))}
      </div>

      {/* Popup Modal */}
      {selectedBreed && (
        <div className="modal-overlay" onClick={() => setSelectedBreed(null)}>
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <span
              className="close-btn"
              onClick={() => setSelectedBreed(null)}
            >
              ✖
            </span>

            <img
              src={selectedBreed.image}
              alt={selectedBreed.name}
              className="modal-image"
            />

            <h2>{selectedBreed.name}</h2>
            <p><strong>Origin:</strong> {selectedBreed.origin}</p>
            <p><strong>Type:</strong> {selectedBreed.type}</p>
            <p><strong>Milk Per Day:</strong> {selectedBreed.milkPerDay}</p>
            <p><strong>Milk Per Lactation:</strong> {selectedBreed.milkPerLactation}</p>
            <p><strong>Lifespan:</strong> {selectedBreed.lifespan}</p>
            <p><strong>Weight:</strong> {selectedBreed.weight}</p>
            <p><strong>Climate:</strong> {selectedBreed.climate}</p>
            <p><strong>Used For:</strong> {selectedBreed.usedFor}</p>
            <p><strong>Special:</strong> {selectedBreed.special}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default BreedInfo;
