import React from "react";
import "./AboutUs.css";

export default function AboutUs() {
  return (
    <div className="about-container">
      <h1 className="about-title">Cattle Breed Classifier</h1>

      <div className="panel-grid">

        {/* Project Overview */}
        <div className="panel">
          <h2>📌 Project Overview</h2>
          <p>
            Cattle AI 2026 is an AI-powered cattle breed identification system 
            designed to assist farmers and breeders in accurately detecting 
            Indian cattle breeds using deep learning.
          </p>
        </div>

        {/* Technologies Used */}
        <div className="panel">
          <h2>🧠 Technologies Used</h2>
          <ul>
            <li>Frontend: React.js, CSS</li>
            <li>Backend: Flask (Python)</li>
            <li>Deep Learning: TensorFlow, Keras</li>
            <li>Model Architecture: EfficientNetB0</li>
            <li>Libraries: NumPy, OpenCV, Matplotlib</li>
          </ul>
        </div>

        {/* Dataset */}
        <div className="panel">
          <h2>📊 Dataset Details</h2>
          <ul>
            <li>Total Classes: 16 cattle breeds</li>
            <li>Data Split: 80% Training, 20% Validation</li>
            <li>Image Preprocessing: Resizing, Normalization</li>
            <li>Data Augmentation: Flip, Rotation, Zoom</li>
          </ul>
        </div>

        {/* Model Training */}
        <div className="panel">
          <h2>🏋️ Model Training</h2>
          <ul>
            <li>Transfer Learning using EfficientNet</li>
            <li>Optimizer: Adam</li>
            <li>Loss Function: Categorical Crossentropy</li>
            <li>Epochs: Multiple trials for refinement</li>
          </ul>
        </div>

        {/* Model Refinement */}
        <div className="panel">
          <h2>🔬 Model Refinement</h2>
          <ul>
            <li>Fine-tuned top layers</li>
            <li>Added Dropout to reduce overfitting</li>
            <li>Used EarlyStopping & Learning Rate Reduction</li>
          </ul>
        </div>

        {/* Performance */}
        <div className="panel">
          <h2>📈 Model Performance</h2>
          <ul>
            <li>Initial Accuracy: ~ 31%</li>
            <li>Improved after augmentation & tuning</li>
            <li>Evaluated using Confusion Matrix</li>
            <li>Metrics: Precision, Recall, F1-score</li>
	    <li>Current Accuracy: ~ 61% </li>

          </ul>
        </div>

        {/* Confusion Matrix */}
        <div className="panel">
          <h2>📉 Confusion Matrix Analysis</h2>
          <p>
            The confusion matrix helped identify breed misclassifications. 
            Similar-looking breeds were improved by enhancing dataset quality 
            and fine-tuning the model further.
          </p>
        </div>

        {/* Future Scope */}
        <div className="panel">
          <h2>🚀 Future Enhancements</h2>
          <ul>
            <li>Mobile App Integration</li>
            <li>Cloud deployment</li>
            <li>Health prediction module</li>
          </ul>
        </div>

      </div>
    </div>
  );
}