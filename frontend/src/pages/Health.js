import React, { useState } from "react";

const TRANSLATIONS = {
  en: {
    title: "🩺 Cattle Health Diagnosis",
    subtitle: "Enter your cattle's symptoms to get a disease report with care instructions",
    cattleId: "Cattle ID / Name",
    cattleIdPlaceholder: "e.g. HF-042 or Radha",
    breed: "Breed",
    selectBreed: "Select breed",
    selectSymptoms: "Select symptoms",
    symptomHint: "(tap to select, tap again to deselect)",
    symptomsSelected: "symptoms selected",
    symptomSelected: "symptom selected",
    additionalObs: "Additional observations",
    additionalPlaceholder: "Duration of symptoms, feeding behaviour, milk production changes, recent events...",
    generateBtn: "🔍 Generate Health Report",
    generatingBtn: "⏳ Generating Report...",
    errorMsg: "Could not generate report. Please try again.",
    reportTitle: "Diagnosis Report",
    severity: "Severity",
    confidence: "Confidence",
    urgency: "Urgency",
    aboutCondition: "📋 About this condition",
    commonCauses: "Common causes:",
    careInstructions: "🩺 Care instructions",
    medications: "💊 Medications",
    vetWarning: "⚠️ Always consult a vet before administering any medication.",
    prevention: "🛡️ Prevention tips",
    whoToContact: "📞 Whom to contact",
    disclaimer: "⚠️ This report is for informational purposes only. It does not replace professional veterinary advice. Always consult a licensed veterinarian.",
    unknownBreed: "Unknown breed",
    cattle: "Cattle",
    symptoms: [
      "Fever / high temperature", "Loss of appetite", "Lethargy / weakness",
      "Nasal discharge", "Coughing", "Diarrhoea", "Bloating / swollen abdomen",
      "Limping / lameness", "Skin lesions / sores", "Eye discharge",
      "Reduced milk production", "Rapid breathing", "Drooling / salivation",
      "Weight loss", "Swollen lymph nodes", "Abnormal urine",
      "Bleeding / wounds", "Difficulty standing", "Pale gums", "Tremors / convulsions"
    ],
    breeds: [
      "Amritmahal","Dangi","Gir","Hallikar","Hariana",
      "Jersey Cow Female Diary","Kankrej","Khillar","Krishna Valley",
      "Malnad Gidda","Ongole","Rathi","Red Sindhi","Sahiwal","Tharparkar","Vechur"
    ]
  },
  mr: {
    title: "🩺 जनावरांचे आरोग्य निदान",
    subtitle: "जनावराची लक्षणे सांगा आणि रोग अहवाल मिळवा",
    cattleId: "जनावराचा क्रमांक / नाव",
    cattleIdPlaceholder: "उदा. HF-042 किंवा राधा",
    breed: "जात",
    selectBreed: "जात निवडा",
    selectSymptoms: "लक्षणे निवडा",
    symptomHint: "(निवडण्यासाठी दाबा, पुन्हा दाबल्यास रद्द होईल)",
    symptomsSelected: "लक्षणे निवडली",
    symptomSelected: "लक्षण निवडले",
    additionalObs: "इतर निरीक्षणे",
    additionalPlaceholder: "लक्षणे किती दिवसांपासून आहेत, चारा खाणे, दूध उत्पादन, इतर माहिती...",
    generateBtn: "🔍 आरोग्य अहवाल तयार करा",
    generatingBtn: "⏳ अहवाल तयार होत आहे...",
    errorMsg: "अहवाल तयार होऊ शकला नाही. कृपया पुन्हा प्रयत्न करा.",
    reportTitle: "निदान अहवाल",
    severity: "तीव्रता",
    confidence: "खात्री",
    urgency: "तातडी",
    aboutCondition: "📋 या रोगाबद्दल",
    commonCauses: "सामान्य कारणे:",
    careInstructions: "🩺 काळजी कशी घ्यावी",
    medications: "💊 औषधे",
    vetWarning: "⚠️ कोणतेही औषध देण्यापूर्वी नेहमी पशुवैद्यकाचा सल्ला घ्या.",
    prevention: "🛡️ प्रतिबंधक उपाय",
    whoToContact: "📞 कोणाशी संपर्क करावा",
    disclaimer: "⚠️ हा अहवाल केवळ माहितीसाठी आहे. हे व्यावसायिक पशुवैद्यकीय सल्ल्याला पर्याय नाही. नेहमी पशुवैद्यकाचा सल्ला घ्या.",
    unknownBreed: "अज्ञात जात",
    cattle: "जनावर",
    symptoms: [
      "ताप / जास्त तापमान", "चारा न खाणे", "सुस्ती / अशक्तपणा",
      "नाकातून पाणी येणे", "खोकला", "जुलाब", "पोट फुगणे",
      "लंगडणे", "त्वचेवर जखमा / फोड", "डोळ्यांतून पाणी येणे",
      "दूध कमी होणे", "जलद श्वास घेणे", "तोंडातून लाळ गळणे",
      "वजन कमी होणे", "लसीका ग्रंथी सुजणे", "असामान्य लघवी",
      "रक्तस्त्राव / जखमा", "उभे राहण्यास त्रास", "हिरड्या फिक्या पडणे", "थरथर / झटके येणे"
    ],
    breeds: [
      "अमृतमहाल","डांगी","गीर","हळ्ळीकर","हरियाणा",
      "जर्सी गाय","कांकरेज","खिल्लार","कृष्णा व्हॅली",
      "मालनाड गिड्डा","ओंगोल","राठी","रेड सिंधी","साहीवाल","थारपारकर","वेचूर"
    ]
  }
};

const SEVERITY = {
  en: { High: "High", Medium: "Medium", Low: "Low" },
  mr: { High: "जास्त", Medium: "मध्यम", Low: "कमी" }
};

function Health() {
  const [lang, setLang] = useState("en");
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [cattleId, setCattleId] = useState("");
  const [breedInput, setBreedInput] = useState("");
  const [additionalNotes, setAdditionalNotes] = useState("");
  const [healthReport, setHealthReport] = useState(null);
  const [diagnosing, setDiagnosing] = useState(false);

  const t = TRANSLATIONS[lang];

  const toggleSymptom = (sym) => {
    setSelectedSymptoms(prev =>
      prev.includes(sym) ? prev.filter(s => s !== sym) : [...prev, sym]
    );
  };

  // When switching language, clear symptom selection since labels change
  const switchLang = (newLang) => {
    setLang(newLang);
    setSelectedSymptoms([]);
    setHealthReport(null);
  };

 const runDiagnosis = async () => {
    if (!breedInput) {
      alert(lang === "en" ? "Please select a breed first." : "कृपया आधी जात निवडा.");
      return;
    }
    if (selectedSymptoms.length === 0) {
      alert(lang === "en" ? "Please select at least one symptom." : "कृपया किमान एक लक्षण निवडा.");
      return;
    }
    setDiagnosing(true);
    setHealthReport(null);

    // Map Marathi symptoms back to English for backend
    const englishSymptoms = lang === "mr"
      ? selectedSymptoms.map(s => {
          const idx = TRANSLATIONS.mr.symptoms.indexOf(s);
          return idx >= 0 ? TRANSLATIONS.en.symptoms[idx] : s;
        })
      : selectedSymptoms;

    try {
      const res = await fetch("http://127.0.0.1:5000/health-diagnosis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          symptoms: englishSymptoms,
          cattleId: cattleId,
          breed: breedInput,
          notes: additionalNotes,
          lang: lang
        })
      });
      const report = await res.json();
      setHealthReport(report);
    } catch (e) {
      setHealthReport({ error: true });
    }
    setDiagnosing(false);
  };

  const sevStyle = (sev) => {
    const map = {
      "High":   { background: "#fff0f0", color: "#c53030", border: "1px solid #fed7d7" },
      "Medium": { background: "#fffaf0", color: "#c05621", border: "1px solid #feebc8" },
      "Low":    { background: "#f0fff4", color: "#276749", border: "1px solid #c6f6d5" },
    };
    return map[sev] || {};
  };

  const contactIcons = { Emergency: "🚨", Helpline: "📞", Hospital: "🏥" };

  return (
    <div style={{ maxWidth: "860px", margin: "0 auto", padding: "40px 20px 80px", fontFamily: "'Poppins', sans-serif" }}>

      {/* ── Language Toggle ── */}
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "20px" }}>
        <div style={{ display: "flex", background: "rgba(255,255,255,0.95)", borderRadius: "12px", padding: "4px", boxShadow: "0 4px 15px rgba(0,0,0,0.08)", border: "1px solid rgba(0,0,0,0.06)" }}>
          <button
            onClick={() => switchLang("en")}
            style={{
              padding: "8px 20px", borderRadius: "9px", border: "none", cursor: "pointer",
              fontFamily: "'Poppins',sans-serif", fontSize: "14px", fontWeight: "600",
              background: lang === "en" ? "linear-gradient(135deg,#071a2f,#123b63)" : "transparent",
              color: lang === "en" ? "white" : "#555",
              transition: "all 0.2s ease",
              boxShadow: lang === "en" ? "0 4px 12px rgba(7,26,47,0.3)" : "none"
            }}
          >
            🇬🇧 English
          </button>
          <button
            onClick={() => switchLang("mr")}
            style={{
              padding: "8px 20px", borderRadius: "9px", border: "none", cursor: "pointer",
              fontFamily: "'Poppins',sans-serif", fontSize: "14px", fontWeight: "600",
              background: lang === "mr" ? "linear-gradient(135deg,#071a2f,#123b63)" : "transparent",
              color: lang === "mr" ? "white" : "#555",
              transition: "all 0.2s ease",
              boxShadow: lang === "mr" ? "0 4px 12px rgba(7,26,47,0.3)" : "none"
            }}
          >
            🇮🇳 मराठी
          </button>
        </div>
      </div>

      {/* Title */}
      <h1 style={{ textAlign: "center", fontSize: "32px", fontWeight: "700", color: "#071a2f", marginBottom: "8px" }}>
        {t.title}
      </h1>
      <p style={{ textAlign: "center", fontSize: "15px", color: "#555", marginBottom: "32px", lineHeight: "1.6" }}>
        {t.subtitle}
      </p>

      {/* Cattle ID + Breed */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
        <div style={{ background: "rgba(255,255,255,0.95)", borderRadius: "18px", padding: "18px 22px", boxShadow: "0 10px 30px rgba(0,0,0,0.07)", border: "1px solid rgba(0,0,0,0.06)" }}>
          <label style={{ fontSize: "13px", fontWeight: "600", color: "#071a2f", display: "block", marginBottom: "8px" }}>
            {t.cattleId}
          </label>
          <input
            type="text"
            placeholder={t.cattleIdPlaceholder}
            value={cattleId}
            onChange={e => setCattleId(e.target.value)}
            style={{ width: "100%", padding: "10px 14px", border: "1.5px solid #e2e8f0", borderRadius: "10px", fontFamily: "'Poppins',sans-serif", fontSize: "14px", color: "#1a202c", background: "#f8fafc", outline: "none", boxSizing: "border-box" }}
          />
        </div>
        <div style={{ background: "rgba(255,255,255,0.95)", borderRadius: "18px", padding: "18px 22px", boxShadow: "0 10px 30px rgba(0,0,0,0.07)", border: "1px solid rgba(0,0,0,0.06)" }}>
          <label style={{ fontSize: "13px", fontWeight: "600", color: "#071a2f", display: "block", marginBottom: "8px" }}>
            {t.breed} <span style={{ color: "#e53e3e" }}>*</span>
          </label>
          <select
            value={breedInput}
            onChange={e => setBreedInput(e.target.value)}
            style={{ width: "100%", padding: "10px 14px", border: breedInput ? "1.5px solid #e2e8f0" : "1.5px solid #fc8181", borderRadius: "10px", fontFamily: "'Poppins',sans-serif", fontSize: "14px", color: "#1a202c", background: breedInput ? "#f8fafc" : "#fff5f5", outline: "none", boxSizing: "border-box" }}
>
            <option value="">{t.selectBreed}</option>
            {t.breeds.map(b => <option key={b}>{b}</option>)}
          </select>
        </div>
      </div>

      {/* Symptom Chips */}
      <div style={{ background: "rgba(255,255,255,0.95)", borderRadius: "18px", padding: "22px 26px", marginBottom: "16px", boxShadow: "0 10px 30px rgba(0,0,0,0.07)", border: "1px solid rgba(0,0,0,0.06)" }}>
        <label style={{ fontSize: "14px", fontWeight: "600", color: "#071a2f", display: "block", marginBottom: "14px" }}>
          {t.selectSymptoms}{" "}
          <span style={{ fontWeight: "400", color: "#888" }}>{t.symptomHint}</span>
        </label>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(185px, 1fr))", gap: "10px" }}>
          {t.symptoms.map(sym => {
            const on = selectedSymptoms.includes(sym);
            return (
              <div
                key={sym}
                onClick={() => toggleSymptom(sym)}
                style={{
                  display: "flex", alignItems: "center", gap: "9px",
                  padding: "10px 14px",
                  border: on ? "2px solid #123b63" : "1.5px solid #e2e8f0",
                  borderRadius: "10px", cursor: "pointer",
                  fontFamily: "'Poppins',sans-serif", fontSize: "13px",
                  color: on ? "#071a2f" : "#4a5568",
                  background: on ? "rgba(18,59,99,0.08)" : "#f8fafc",
                  fontWeight: on ? "600" : "400",
                  userSelect: "none", transition: "all 0.18s ease",
                }}
              >
                <span style={{
                  width: "9px", height: "9px", borderRadius: "50%", flexShrink: 0,
                  background: on ? "#123b63" : "transparent",
                  border: on ? "2px solid #123b63" : "2px solid #aaa",
                  display: "inline-block",
                }}></span>
                {sym}
              </div>
            );
          })}
        </div>
        {selectedSymptoms.length > 0 && (
          <p style={{ marginTop: "14px", fontSize: "13px", color: "#123b63", fontWeight: "600" }}>
            ✅ {selectedSymptoms.length} {selectedSymptoms.length > 1 ? t.symptomsSelected : t.symptomSelected}
          </p>
        )}
      </div>

      {/* Additional Notes */}
      <div style={{ background: "rgba(255,255,255,0.95)", borderRadius: "18px", padding: "22px 26px", marginBottom: "20px", boxShadow: "0 10px 30px rgba(0,0,0,0.07)", border: "1px solid rgba(0,0,0,0.06)" }}>
        <label style={{ fontSize: "14px", fontWeight: "600", color: "#071a2f", display: "block", marginBottom: "10px" }}>
          {t.additionalObs}
        </label>
        <textarea
          placeholder={t.additionalPlaceholder}
          value={additionalNotes}
          onChange={e => setAdditionalNotes(e.target.value)}
          style={{ width: "100%", minHeight: "90px", padding: "12px 14px", border: "1.5px solid #e2e8f0", borderRadius: "10px", fontFamily: "'Poppins',sans-serif", fontSize: "14px", color: "#1a202c", background: "#f8fafc", resize: "vertical", outline: "none", boxSizing: "border-box" }}
        />
      </div>

      {/* Generate Button */}
      <div style={{ display: "flex", justifyContent: "center", marginBottom: "30px" }}>
        <button
          onClick={runDiagnosis}
          disabled={diagnosing}
          style={{
            padding: "14px 44px", fontSize: "16px", fontFamily: "'Poppins',sans-serif",
            fontWeight: "600", background: diagnosing ? "#999" : "linear-gradient(135deg,#071a2f,#123b63)",
            color: "white", border: "none", borderRadius: "14px",
            cursor: diagnosing ? "not-allowed" : "pointer",
            boxShadow: diagnosing ? "none" : "0 10px 28px rgba(7,26,47,0.4)",
            letterSpacing: "0.3px", transition: "all 0.3s ease",
          }}
        >
          {diagnosing ? t.generatingBtn : t.generateBtn}
        </button>
      </div>

      {/* Error */}
      {healthReport?.error && (
        <p style={{ textAlign: "center", color: "#e53e3e", marginBottom: "20px" }}>
          {t.errorMsg}
        </p>
      )}

      {/* REPORT */}
      {healthReport && !healthReport.error && (
        <div>

          {/* Header Card */}
          <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: "18px", padding: "22px 26px", marginBottom: "14px", boxShadow: "0 12px 32px rgba(0,0,0,0.07)", border: "1px solid rgba(0,0,0,0.05)", display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "16px", flexWrap: "wrap" }}>
            <div>
              <p style={{ fontSize: "12px", color: "#888", margin: "0 0 6px", fontFamily: "'Poppins',sans-serif" }}>
                {cattleId || t.cattle} · {breedInput || t.unknownBreed}
              </p>
              <h2 style={{ fontSize: "26px", fontWeight: "700", color: "#071a2f", margin: "0 0 10px", fontFamily: "'Poppins',sans-serif" }}>
                {healthReport.disease}
              </h2>
              <div style={{ display: "flex", gap: "10px", alignItems: "center", flexWrap: "wrap" }}>
                <span style={{ display: "inline-block", padding: "4px 14px", borderRadius: "20px", fontSize: "12px", fontWeight: "600", fontFamily: "'Poppins',sans-serif", ...sevStyle(healthReport.severity) }}>
                  {t.severity}: {SEVERITY[lang][healthReport.severity] || healthReport.severity}
                </span>
                <span style={{ fontSize: "13px", color: "#666", fontFamily: "'Poppins',sans-serif" }}>
                  {t.confidence}: {healthReport.confidence}
                </span>
              </div>
            </div>
            <div style={{ textAlign: "right", flexShrink: 0 }}>
              <p style={{ fontSize: "12px", color: "#888", margin: "0 0 4px", fontFamily: "'Poppins',sans-serif" }}>{t.urgency}</p>
              <p style={{ fontSize: "13px", fontWeight: "600", color: "#c05621", margin: 0, fontFamily: "'Poppins',sans-serif" }}>
                {healthReport.urgency}
              </p>
            </div>
          </div>

          {/* About */}
          <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: "18px", padding: "20px 26px", marginBottom: "14px", boxShadow: "0 10px 28px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.05)" }}>
            <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#071a2f", margin: "0 0 10px", fontFamily: "'Poppins',sans-serif" }}>{t.aboutCondition}</h4>
            <p style={{ fontSize: "14px", lineHeight: "1.7", color: "#444", margin: 0, fontFamily: "'Poppins',sans-serif" }}>{healthReport.description}</p>
            {healthReport.causes?.length > 0 && (
              <>
                <p style={{ fontSize: "13px", color: "#888", margin: "12px 0 6px" }}>{t.commonCauses}</p>
                <ul style={{ paddingLeft: "20px", margin: 0 }}>
                  {healthReport.causes.map((c, i) => <li key={i} style={{ fontSize: "14px", color: "#444", lineHeight: "1.65", marginBottom: "5px", fontFamily: "'Poppins',sans-serif" }}>{c}</li>)}
                </ul>
              </>
            )}
          </div>

          {/* Care Instructions */}
          <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: "18px", padding: "20px 26px", marginBottom: "14px", boxShadow: "0 10px 28px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.05)" }}>
            <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#071a2f", margin: "0 0 10px", fontFamily: "'Poppins',sans-serif" }}>{t.careInstructions}</h4>
            <ol style={{ paddingLeft: "22px", margin: 0 }}>
              {healthReport.care_instructions?.map((step, i) => <li key={i} style={{ fontSize: "14px", color: "#333", lineHeight: "1.65", marginBottom: "8px", fontFamily: "'Poppins',sans-serif" }}>{step}</li>)}
            </ol>
          </div>

          {/* Medications + Prevention */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "14px", marginBottom: "14px" }}>
            <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: "18px", padding: "20px 26px", boxShadow: "0 10px 28px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.05)" }}>
              <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#071a2f", margin: "0 0 10px", fontFamily: "'Poppins',sans-serif" }}>{t.medications}</h4>
              <ul style={{ paddingLeft: "20px", margin: 0 }}>
                {healthReport.medications?.map((m, i) => <li key={i} style={{ fontSize: "14px", color: "#444", lineHeight: "1.65", marginBottom: "6px", fontFamily: "'Poppins',sans-serif" }}>{m}</li>)}
              </ul>
              <p style={{ fontSize: "12px", color: "#c53030", margin: "12px 0 0", fontStyle: "italic", fontFamily: "'Poppins',sans-serif" }}>
                {t.vetWarning}
              </p>
            </div>
            <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: "18px", padding: "20px 26px", boxShadow: "0 10px 28px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.05)" }}>
              <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#071a2f", margin: "0 0 10px", fontFamily: "'Poppins',sans-serif" }}>{t.prevention}</h4>
              <ul style={{ paddingLeft: "20px", margin: 0 }}>
                {healthReport.prevention?.map((p, i) => <li key={i} style={{ fontSize: "14px", color: "#444", lineHeight: "1.65", marginBottom: "6px", fontFamily: "'Poppins',sans-serif" }}>{p}</li>)}
              </ul>
            </div>
          </div>

          {/* Contacts */}
          <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: "18px", padding: "20px 26px", marginBottom: "14px", boxShadow: "0 10px 28px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.05)" }}>
            <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#071a2f", margin: "0 0 12px", fontFamily: "'Poppins',sans-serif" }}>{t.whoToContact}</h4>
            {healthReport.contacts?.map((c, i) => (
              <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "12px 0", borderBottom: i < healthReport.contacts.length - 1 ? "1px solid #f0f0f0" : "none" }}>
                <div style={{ width: "38px", height: "38px", borderRadius: "50%", background: "#eef2f7", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "18px", flexShrink: 0 }}>
                  {contactIcons[c.type] || "📋"}
                </div>
                <div style={{ flex: 1 }}>
                  <p style={{ margin: "0 0 3px", fontSize: "14px", fontWeight: "600", color: "#071a2f", fontFamily: "'Poppins',sans-serif" }}>{c.name}</p>
                  <p style={{ margin: 0, fontSize: "13px", color: "#666", fontFamily: "'Poppins',sans-serif" }}>{c.note}</p>
                </div>
                <span style={{ fontSize: "11px", padding: "3px 10px", background: "#eef2f7", borderRadius: "20px", color: "#555", fontFamily: "'Poppins',sans-serif", flexShrink: 0, alignSelf: "center" }}>
                  {c.type}
                </span>
              </div>
            ))}
          </div>

          {/* Disclaimer */}
          <div style={{ background: "#fffaf0", border: "1px solid #feebc8", borderRadius: "14px", padding: "14px 20px", fontSize: "13px", color: "#744210", lineHeight: "1.65", fontFamily: "'Poppins',sans-serif", marginBottom: "30px" }}>
            {t.disclaimer}
          </div>

        </div>
      )}

    </div>
  );
}

export default Health;
