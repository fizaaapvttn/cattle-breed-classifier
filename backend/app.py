from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from keras.applications.efficientnet import preprocess_input
from keras.preprocessing import image
import numpy as np
import os
from io import BytesIO
import json

app = Flask(__name__)
CORS(app)

MODEL_PATH = r"C:\Users\Nishita\Desktop\typ\cattle_fixed.keras"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = load_model(MODEL_PATH, custom_objects={"preprocess_input": preprocess_input})

class_labels = [
    "amritmahal", "dangi", "gir", "hallikar", "hariana", "jersey cow female diary",
    "kankrej", "khillar", "krishna_valley", "malnad_gidda", "ongole", "rathi",
    "red_sindhi", "sahiwal", "tharparkar", "vechur"
]

# ─── Contacts ────────────────────────────────────────────────────────────────

CONTACTS_EN = [
    {"type": "Emergency", "name": "Local government veterinary officer (Pashu Chikitsak)", "note": "Contact immediately for severe or worsening cases"},
    {"type": "Helpline",  "name": "Kisan Call Centre - 1800-180-1551",                    "note": "Free 24x7 helpline for farmers in India"},
    {"type": "Hospital",  "name": "Nearest veterinary college or district animal hospital","note": "For advanced diagnosis, lab tests and treatment"}
]

CONTACTS_MR = [
    {"type": "आणीबाणी",    "name": "स्थानिक सरकारी पशुवैद्यक अधिकारी (पशुचिकित्सक)", "note": "गंभीर किंवा बिघडणाऱ्या प्रकरणांसाठी लगेच संपर्क करा"},
    {"type": "हेल्पलाइन", "name": "किसान कॉल सेंटर - 1800-180-1551",                  "note": "भारतातील शेतकऱ्यांसाठी मोफत २४x७ हेल्पलाइन"},
    {"type": "रुग्णालय",  "name": "जवळचे पशुवैद्यकीय महाविद्यालय किंवा जिल्हा पशु रुग्णालय", "note": "प्रगत निदान, प्रयोगशाळा चाचण्या आणि उपचारांसाठी"}
]

# ─── Disease Database ─────────────────────────────────────────────────────────

DISEASE_DB = [
    {
        "keywords": ["fever", "drooling", "salivation", "blisters", "sores", "limping", "lameness", "difficulty standing", "nasal discharge"],
        "en": {
            "disease": "Foot and Mouth Disease (FMD)",
            "severity": "High",
            "description": "Foot and Mouth Disease is a highly contagious viral infection affecting cattle. It causes painful blisters in the mouth, tongue, and feet making eating and walking very difficult. Immediate isolation and veterinary care is essential to prevent spread.",
            "causes": ["Highly contagious virus spread through contact", "Infected animals or contaminated feed", "Poor vaccination history"],
            "care_instructions": ["Isolate the affected animal immediately from the herd", "Provide soft feed and clean drinking water", "Clean and disinfect the blisters with antiseptic solution", "Call the government veterinary officer immediately"],
            "medications": ["Antiseptic mouth wash for blisters", "Anti-fever medication prescribed by vet"],
            "prevention": ["Vaccinate every 6 months with FMD vaccine", "Maintain proper hygiene in the shed", "Avoid contact with unknown cattle"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "खुरपका-तोंडपका रोग (FMD)",
            "severity": "High",
            "description": "खुरपका-तोंडपका हा अत्यंत संसर्गजन्य विषाणूजन्य रोग आहे. यामुळे तोंड, जीभ आणि पायांवर वेदनादायक फोड येतात ज्यामुळे खाणे आणि चालणे कठीण होते. प्रसार टाळण्यासाठी लगेच वेगळे करणे आणि पशुवैद्यकीय काळजी आवश्यक आहे.",
            "causes": ["संसर्गजन्य विषाणू संपर्काद्वारे पसरतो", "संक्रमित जनावरे किंवा दूषित चारा", "लसीकरणाचा इतिहास नसणे"],
            "care_instructions": ["बाधित जनावराला लगेच कळपातून वेगळे करा", "मऊ चारा आणि स्वच्छ पाणी द्या", "फोडांवर जंतुनाशक द्रावणाने स्वच्छ करा", "सरकारी पशुवैद्यक अधिकाऱ्याला लगेच बोलवा"],
            "medications": ["फोडांसाठी जंतुनाशक तोंड धुण्याचे द्रावण", "पशुवैद्यकाने सांगितलेले ताप कमी करणारे औषध"],
            "prevention": ["दर ६ महिन्यांनी FMD लस द्या", "गोठ्यात योग्य स्वच्छता राखा", "अनोळखी जनावरांशी संपर्क टाळा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["fever", "swollen", "swollen lymph nodes", "rapid breathing", "breathing difficulty", "lethargy", "weakness", "nasal discharge"],
        "en": {
            "disease": "Hemorrhagic Septicemia (HS)",
            "severity": "High",
            "description": "Hemorrhagic Septicemia is a serious bacterial disease common during monsoon season in India. It causes high fever, swelling in the throat and neck, and severe breathing difficulty. It can be fatal within 24 hours if untreated.",
            "causes": ["Pasteurella multocida bacteria", "Stress during rainy season", "Poor nutrition and weak immunity"],
            "care_instructions": ["Call the veterinary officer immediately", "Move the animal to a dry and well-ventilated shelter", "Do not stress the animal — keep it calm", "Provide clean water and light feed"],
            "medications": ["Oxytetracycline injection (by vet)", "Sulfonamide drugs (by vet)"],
            "prevention": ["Annual HS vaccination before monsoon", "Maintain dry and clean shelter", "Avoid waterlogged areas"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "घटसर्प (HS)",
            "severity": "High",
            "description": "घटसर्प हा भारतात पावसाळ्यात सामान्य असलेला गंभीर जिवाणूजन्य रोग आहे. यामुळे तीव्र ताप, घसा आणि मान सुजणे आणि श्वास घेण्यास त्रास होतो. उपचार न केल्यास २४ तासांत मृत्यू होऊ शकतो.",
            "causes": ["Pasteurella multocida जिवाणू", "पावसाळ्यात ताण", "कमकुवत पोषण आणि रोगप्रतिकारशक्ती"],
            "care_instructions": ["पशुवैद्यक अधिकाऱ्याला लगेच बोलवा", "जनावराला कोरड्या आणि हवेशीर गोठ्यात हलवा", "जनावराला ताण देऊ नका — शांत ठेवा", "स्वच्छ पाणी आणि हलका चारा द्या"],
            "medications": ["ऑक्सिटेट्रासायक्लिन इंजेक्शन (पशुवैद्यकाकडून)", "सल्फोनामाइड औषधे (पशुवैद्यकाकडून)"],
            "prevention": ["पावसाळ्यापूर्वी वार्षिक HS लस द्या", "कोरडा आणि स्वच्छ गोठा राखा", "पाणी साचलेल्या भागात चराणे टाळा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["swollen", "fever", "lameness", "limping", "difficulty standing", "lethargy", "weakness", "bleeding"],
        "en": {
            "disease": "Black Quarter (BQ)",
            "severity": "High",
            "description": "Black Quarter is a bacterial disease mainly affecting young cattle aged 6 months to 2 years. It causes sudden swelling in muscles of the legs and shoulders with gas formation under the skin. It progresses very rapidly and can be fatal.",
            "causes": ["Clostridium chauvoei bacteria from soil", "Grazing in contaminated fields", "Injury or wound exposure to soil"],
            "care_instructions": ["Call the vet immediately — this is life-threatening", "Keep the animal in a clean dry place", "Do not massage or press the swollen area", "Isolate from other animals"],
            "medications": ["Penicillin injection (by vet only)", "Anti-toxin serum (by vet only)"],
            "prevention": ["Annual BQ vaccination", "Avoid grazing in low-lying waterlogged fields", "Clean wounds immediately"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "एकटांगी / फऱ्या रोग (BQ)",
            "severity": "High",
            "description": "एकटांगी हा जिवाणूजन्य रोग प्रामुख्याने ६ महिने ते २ वर्षे वयाच्या तरुण जनावरांना होतो. यामुळे पाय आणि खांद्याच्या स्नायूंमध्ये अचानक सूज येते आणि त्वचेखाली वायू तयार होतो. हा रोग वेगाने वाढतो आणि प्राणघातक असू शकतो.",
            "causes": ["मातीतील Clostridium chauvoei जिवाणू", "दूषित शेतात चराणे", "जखम किंवा मातीशी संपर्क"],
            "care_instructions": ["पशुवैद्यकाला लगेच बोलवा — हे जीवघेणे आहे", "जनावराला स्वच्छ कोरड्या जागी ठेवा", "सुजलेल्या भागावर मालिश किंवा दाब देऊ नका", "इतर जनावरांपासून वेगळे करा"],
            "medications": ["पेनिसिलिन इंजेक्शन (फक्त पशुवैद्यकाकडून)", "अँटी-टॉक्सिन सीरम (फक्त पशुवैद्यकाकडून)"],
            "prevention": ["वार्षिक BQ लसीकरण", "सखल पाणी साचलेल्या शेतात चराणे टाळा", "जखमा लगेच स्वच्छ करा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["reduced milk production", "swollen", "fever", "lethargy", "abnormal urine", "loss of appetite"],
        "en": {
            "disease": "Mastitis (Udder Infection)",
            "severity": "Medium",
            "description": "Mastitis is an infection of the udder commonly seen in dairy cattle. It causes reduced and abnormal milk production, swelling of the udder, and fever. It is one of the most common diseases in dairy breeds like Gir, Sahiwal and Jersey.",
            "causes": ["Bacterial infection due to poor milking hygiene", "Injury to the udder", "Contaminated milking equipment"],
            "care_instructions": ["Milk the affected quarter frequently to drain infected milk", "Clean the udder with warm water before and after milking", "Apply prescribed antibiotic ointment to the teat", "Consult a vet for antibiotic treatment"],
            "medications": ["Intramammary antibiotic tubes (by vet)", "Anti-inflammatory drugs (by vet)"],
            "prevention": ["Maintain strict milking hygiene", "Dip teats in antiseptic after milking", "Regular udder examination"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "कासदाह (Mastitis)",
            "severity": "Medium",
            "description": "कासदाह हा दुभत्या जनावरांमध्ये आढळणारा कासेचा संसर्ग आहे. यामुळे दूध कमी होते, कास सुजते आणि ताप येतो. गीर, साहीवाल आणि जर्सी यांसारख्या दुधाळ जातींमध्ये हा सर्वात सामान्य रोग आहे.",
            "causes": ["दूध काढण्याच्या अस्वच्छतेमुळे जिवाणू संसर्ग", "कासेला इजा", "दूषित दूध काढण्याची उपकरणे"],
            "care_instructions": ["संक्रमित दूध काढण्यासाठी वारंवार दूध काढा", "दूध काढण्यापूर्वी आणि नंतर कोमट पाण्याने कास स्वच्छ करा", "सांगितलेले प्रतिजैविक मलम सड्यावर लावा", "प्रतिजैविक उपचारांसाठी पशुवैद्यकाचा सल्ला घ्या"],
            "medications": ["इंट्रामॅमरी प्रतिजैविक नळ्या (पशुवैद्यकाकडून)", "दाहविरोधी औषधे (पशुवैद्यकाकडून)"],
            "prevention": ["दूध काढण्याची कठोर स्वच्छता राखा", "दूध काढल्यानंतर सड्यांना जंतुनाशकात बुडवा", "नियमित कास तपासणी"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["bloating", "swollen abdomen", "rapid breathing", "difficulty standing", "lethargy", "loss of appetite"],
        "en": {
            "disease": "Bloat (Tympany)",
            "severity": "High",
            "description": "Bloat is a dangerous condition where gas accumulates in the rumen causing the left side of the abdomen to swell. It causes severe discomfort, breathing difficulty and can be fatal within hours if not treated quickly.",
            "causes": ["Eating too much green fresh legumes or wet grass", "Sudden change in diet", "Obstruction in the food pipe"],
            "care_instructions": ["Make the animal stand with front legs higher than back legs on a slope", "Walk the animal slowly to stimulate gas release", "Massage the left side of the abdomen gently", "Call vet immediately if the animal cannot breathe properly"],
            "medications": ["Turpentine oil with edible oil 150ml as emergency", "Anti-bloat drench prescribed by vet"],
            "prevention": ["Avoid sudden change in feed", "Do not feed wet or frost-covered grass", "Limit fresh legume grazing"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "पोट फुगणे (Bloat)",
            "severity": "High",
            "description": "पोट फुगणे ही एक धोकादायक स्थिती आहे ज्यात रुमेनमध्ये वायू जमा होतो आणि पोटाची डावी बाजू फुगते. यामुळे तीव्र अस्वस्थता, श्वास घेण्यास त्रास होतो आणि वेळेत उपचार न केल्यास काही तासांत मृत्यू होऊ शकतो.",
            "causes": ["जास्त हिरव्या ताज्या शेंगा किंवा ओले गवत खाणे", "चाऱ्यात अचानक बदल", "अन्ननलिकेत अडथळा"],
            "care_instructions": ["जनावराचे पुढचे पाय मागच्या पायांपेक्षा उंचावर ठेवा", "वायू सुटण्यासाठी जनावराला हळू चालवा", "पोटाच्या डाव्या बाजूला हळुवारपणे मालिश करा", "जनावर नीट श्वास घेत नसल्यास लगेच पशुवैद्यकाला बोलवा"],
            "medications": ["आणीबाणीत खाद्यतेलासह तारपीन तेल १५०मिली", "पशुवैद्यकाने सांगितलेले अँटी-ब्लोट द्रावण"],
            "prevention": ["चाऱ्यात अचानक बदल टाळा", "ओले किंवा दंव पडलेले गवत देऊ नका", "ताज्या शेंगांचे चराणे मर्यादित करा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["diarrhoea", "loss of appetite", "lethargy", "weakness", "weight loss", "abnormal urine"],
        "en": {
            "disease": "Diarrhoea (Scours)",
            "severity": "Medium",
            "description": "Diarrhoea in cattle can be caused by infection, parasites, or sudden feed change. It leads to severe dehydration and weight loss especially in calves. Prompt treatment is important to prevent dehydration.",
            "causes": ["Bacterial or viral infection", "Intestinal parasites", "Sudden change in feed or contaminated water"],
            "care_instructions": ["Provide oral rehydration solution — mix 1 litre water with salt and sugar", "Give clean fresh water frequently", "Reduce green fodder and give dry hay", "Consult vet if diarrhoea persists more than 2 days"],
            "medications": ["Oral Rehydration Salts (ORS)", "Electrolyte solution", "Antibiotic as prescribed by vet"],
            "prevention": ["Provide clean drinking water", "Deworm cattle every 6 months", "Avoid sudden feed changes"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "जुलाब (Diarrhoea)",
            "severity": "Medium",
            "description": "जनावरांमध्ये जुलाब संसर्ग, परजीवी किंवा चाऱ्यातील अचानक बदलामुळे होऊ शकतो. यामुळे तीव्र निर्जलीकरण आणि वजन कमी होते, विशेषतः वासरांमध्ये. निर्जलीकरण टाळण्यासाठी त्वरित उपचार महत्त्वाचे आहे.",
            "causes": ["जिवाणू किंवा विषाणू संसर्ग", "आतड्यातील परजीवी", "चाऱ्यात अचानक बदल किंवा दूषित पाणी"],
            "care_instructions": ["तोंडावाटे पुनर्जलीकरण द्रावण द्या — १ लिटर पाण्यात मीठ आणि साखर मिसळा", "वारंवार स्वच्छ ताजे पाणी द्या", "हिरवा चारा कमी करा आणि कोरडे गवत द्या", "जुलाब २ दिवसांपेक्षा जास्त राहिल्यास पशुवैद्यकाचा सल्ला घ्या"],
            "medications": ["तोंडावाटे पुनर्जलीकरण क्षार (ORS)", "इलेक्ट्रोलाइट द्रावण", "पशुवैद्यकाने सांगितलेले प्रतिजैविक"],
            "prevention": ["स्वच्छ पिण्याचे पाणी द्या", "दर ६ महिन्यांनी जंत काढण्याचे औषध द्या", "चाऱ्यात अचानक बदल टाळा"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["coughing", "nasal discharge", "rapid breathing", "fever", "lethargy", "loss of appetite", "eye discharge"],
        "en": {
            "disease": "Respiratory Infection (Pneumonia)",
            "severity": "Medium",
            "description": "Respiratory infections including pneumonia are common in cattle kept in poorly ventilated sheds. Symptoms include coughing, nasal discharge and high fever. Young calves and recently moved animals are most vulnerable.",
            "causes": ["Bacterial or viral infection", "Poor ventilation in shed", "Sudden weather change or cold stress"],
            "care_instructions": ["Move animal to a well-ventilated dry shelter", "Keep the animal warm during cold weather", "Provide nutritious feed and clean water", "Consult vet for antibiotic treatment"],
            "medications": ["Oxytetracycline (by vet)", "Tylosin injection (by vet)", "Vitamin C supplement"],
            "prevention": ["Ensure proper ventilation in cattle shed", "Vaccinate against common respiratory viruses", "Avoid overcrowding"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "श्वसन संसर्ग (न्यूमोनिया)",
            "severity": "Medium",
            "description": "न्यूमोनियासह श्वसन संसर्ग खराब हवेशीर गोठ्यातील जनावरांमध्ये सामान्य आहे. लक्षणांमध्ये खोकला, नाकातून स्त्राव आणि तीव्र ताप यांचा समावेश आहे. तरुण वासरे आणि नुकतीच हलवलेली जनावरे सर्वाधिक असुरक्षित असतात.",
            "causes": ["जिवाणू किंवा विषाणू संसर्ग", "गोठ्यात खराब वायुवीजन", "अचानक हवामान बदल किंवा थंडीचा ताण"],
            "care_instructions": ["जनावराला हवेशीर कोरड्या गोठ्यात हलवा", "थंड हवामानात जनावराला उबदार ठेवा", "पौष्टिक चारा आणि स्वच्छ पाणी द्या", "प्रतिजैविक उपचारांसाठी पशुवैद्यकाचा सल्ला घ्या"],
            "medications": ["ऑक्सिटेट्रासायक्लिन (पशुवैद्यकाकडून)", "टायलोसिन इंजेक्शन (पशुवैद्यकाकडून)", "व्हिटॅमिन C पूरक"],
            "prevention": ["गोठ्यात योग्य वायुवीजन सुनिश्चित करा", "सामान्य श्वसन विषाणूंविरुद्ध लस द्या", "गर्दी टाळा"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["skin lesions", "sores", "weight loss", "loss of appetite", "eye discharge", "lethargy", "bleeding"],
        "en": {
            "disease": "External Parasites / Skin Infection",
            "severity": "Low",
            "description": "Skin infections and external parasites like ticks, lice and mange mites are common in Indian cattle. They cause skin lesions, hair loss, and irritation. If untreated they can lead to anaemia and reduced productivity.",
            "causes": ["Tick and lice infestation", "Fungal infection", "Poor hygiene and overcrowding"],
            "care_instructions": ["Wash the affected areas with medicated shampoo", "Apply prescribed acaricide or anti-fungal ointment", "Clean and disinfect the cattle shed", "Separate affected animals from the herd"],
            "medications": ["Ivermectin injection (by vet)", "Butox spray for ticks and lice", "Anti-fungal ointment"],
            "prevention": ["Regular tick and lice control treatment", "Maintain clean shed", "Regular grooming"],
            "urgency": "Seek vet within 1 week"
        },
        "mr": {
            "disease": "बाह्य परजीवी / त्वचा संसर्ग",
            "severity": "Low",
            "description": "भारतीय जनावरांमध्ये गोचीड, उवा आणि खरजेचे माइट्स यांसारखे बाह्य परजीवी सामान्य आहेत. यामुळे त्वचेवर जखमा, केस गळणे आणि खाज येते. उपचार न केल्यास अशक्तपणा आणि उत्पादन कमी होऊ शकते.",
            "causes": ["गोचीड आणि उवांचा प्रादुर्भाव", "बुरशीजन्य संसर्ग", "खराब स्वच्छता आणि गर्दी"],
            "care_instructions": ["बाधित भाग औषधी शँपूने धुवा", "सांगितलेले गोचीडनाशक किंवा अँटी-फंगल मलम लावा", "गोठा स्वच्छ आणि निर्जंतुक करा", "बाधित जनावरांना कळपापासून वेगळे करा"],
            "medications": ["आयव्हरमेक्टिन इंजेक्शन (पशुवैद्यकाकडून)", "गोचीड आणि उवांसाठी बुटॉक्स स्प्रे", "अँटी-फंगल मलम"],
            "prevention": ["नियमित गोचीड आणि उवा नियंत्रण उपचार", "स्वच्छ गोठा राखा", "नियमित स्वच्छता"],
            "urgency": "१ आठवड्यात पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["pale gums", "weight loss", "lethargy", "weakness", "loss of appetite", "reduced milk production"],
        "en": {
            "disease": "Anaemia / Internal Parasites",
            "severity": "Medium",
            "description": "Anaemia in cattle is often caused by heavy internal parasite burden like roundworms and liver flukes. It causes pale gums, weakness and significant weight loss. Deworming and iron supplementation are the main treatments.",
            "causes": ["Heavy worm burden in the gut", "Blood-sucking parasites like ticks", "Nutritional deficiency"],
            "care_instructions": ["Consult vet for deworming injection or oral dose", "Provide iron-rich feed like green leafy fodder", "Improve overall nutrition with mineral mixture", "Check and treat for tick infestation"],
            "medications": ["Albendazole dewormer (by vet)", "Iron dextran injection (by vet)", "Mineral mixture supplement"],
            "prevention": ["Deworm every 6 months", "Rotate grazing areas", "Control ticks and lice regularly"],
            "urgency": "Seek vet within 1 week"
        },
        "mr": {
            "disease": "अशक्तपणा / अंतर्गत परजीवी",
            "severity": "Medium",
            "description": "जनावरांमध्ये अशक्तपणा अनेकदा गोलकृमी आणि यकृत किडे यांसारख्या अंतर्गत परजीवींमुळे होतो. यामुळे हिरड्या फिक्या पडतात, अशक्तपणा येतो आणि वजन कमी होते. जंत काढणे आणि लोह पूरक हे मुख्य उपचार आहेत.",
            "causes": ["पोटात जड कृमींचा भार", "गोचीडसारखे रक्त शोषणारे परजीवी", "पोषणाची कमतरता"],
            "care_instructions": ["जंत काढण्याचे इंजेक्शन किंवा तोंडावाटे डोससाठी पशुवैद्यकाचा सल्ला घ्या", "हिरव्या पालेभाज्यांसारखा लोहयुक्त चारा द्या", "खनिज मिश्रणाने एकूण पोषण सुधारा", "गोचीड प्रादुर्भाव तपासा आणि उपचार करा"],
            "medications": ["अल्बेंडाझोल जंतनाशक (पशुवैद्यकाकडून)", "आयर्न डेक्स्ट्रान इंजेक्शन (पशुवैद्यकाकडून)", "खनिज मिश्रण पूरक"],
            "prevention": ["दर ६ महिन्यांनी जंत काढा", "चराणे क्षेत्र बदलत राहा", "नियमितपणे गोचीड आणि उवा नियंत्रण करा"],
            "urgency": "१ आठवड्यात पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["tremors", "convulsions", "difficulty standing", "lethargy", "weakness", "reduced milk production"],
        "en": {
            "disease": "Milk Fever (Hypocalcaemia)",
            "severity": "High",
            "description": "Milk fever is common in high-producing dairy cows after calving. Low blood calcium causes muscle tremors, inability to stand and convulsions. It requires immediate calcium supplementation by the vet.",
            "causes": ["Low blood calcium after calving", "High milk production draining calcium", "Nutritional imbalance before calving"],
            "care_instructions": ["Call the vet immediately for calcium injection", "Keep the animal lying on its chest not on its side", "Keep the animal warm and comfortable", "Monitor breathing and consciousness closely"],
            "medications": ["Calcium borogluconate IV injection (vet only)", "Oral calcium gel as follow-up"],
            "prevention": ["Feed calcium-rich diet before and after calving", "Provide mineral mixture regularly", "Monitor high-yielding cows after calving"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "दूध ताप (Milk Fever)",
            "severity": "High",
            "description": "दूध ताप प्रसूतीनंतर जास्त दूध देणाऱ्या गायींमध्ये सामान्य आहे. रक्तातील कॅल्शियम कमी झाल्याने स्नायूंमध्ये थरथर, उभे राहण्यास असमर्थता आणि झटके येतात. पशुवैद्यकाकडून तात्काळ कॅल्शियम पूरक आवश्यक आहे.",
            "causes": ["प्रसूतीनंतर रक्तातील कॅल्शियम कमी होणे", "जास्त दूध उत्पादनामुळे कॅल्शियम खर्च होणे", "प्रसूतीपूर्वी पोषण असंतुलन"],
            "care_instructions": ["कॅल्शियम इंजेक्शनसाठी पशुवैद्यकाला लगेच बोलवा", "जनावराला कुशीवर नाही तर छातीवर झोपवा", "जनावराला उबदार आणि आरामदायक ठेवा", "श्वास आणि चेतना जवळून निरीक्षण करा"],
            "medications": ["कॅल्शियम बोरोग्लुकोनेट IV इंजेक्शन (फक्त पशुवैद्यकाकडून)", "फॉलो-अपसाठी तोंडावाटे कॅल्शियम जेल"],
            "prevention": ["प्रसूतीपूर्वी आणि नंतर कॅल्शियमयुक्त आहार द्या", "नियमितपणे खनिज मिश्रण द्या", "प्रसूतीनंतर जास्त दूध देणाऱ्या गायींवर लक्ष ठेवा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["fever", "bleeding", "wounds", "sudden death", "swollen", "difficulty standing", "rapid breathing"],
        "en": {
            "disease": "Anthrax",
            "severity": "High",
            "description": "Anthrax is a deadly bacterial disease caused by Bacillus anthracis found in contaminated soil. It causes sudden high fever, bleeding from body openings and rapid death. It is a zoonotic disease meaning it can spread to humans.",
            "causes": ["Bacillus anthracis spores in soil", "Grazing in anthrax-prone areas", "Contaminated water sources"],
            "care_instructions": ["Do NOT touch the carcass — call authorities immediately", "Isolate all animals in the herd immediately", "Call government veterinary officer immediately", "Do not open the carcass as it releases deadly spores"],
            "medications": ["Penicillin injection in early stages (vet only)", "Anthrax antiserum (vet only)"],
            "prevention": ["Annual anthrax vaccination in high-risk areas", "Do not graze near flood-prone areas", "Report sudden deaths to veterinary authorities"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "गाळफोड (Anthrax)",
            "severity": "High",
            "description": "गाळफोड हा दूषित मातीत आढळणाऱ्या Bacillus anthracis मुळे होणारा घातक जिवाणूजन्य रोग आहे. यामुळे अचानक तीव्र ताप, शरीराच्या छिद्रांतून रक्तस्त्राव आणि झपाट्याने मृत्यू होतो. हा झुनोटिक रोग आहे म्हणजे तो मानवांमध्ये पसरू शकतो.",
            "causes": ["मातीतील Bacillus anthracis बीजाणू", "गाळफोड-प्रवण भागात चराणे", "दूषित पाण्याचे स्रोत"],
            "care_instructions": ["मृत जनावराला हात लावू नका — लगेच अधिकाऱ्यांना कळवा", "कळपातील सर्व जनावरांना लगेच वेगळे करा", "सरकारी पशुवैद्यक अधिकाऱ्याला लगेच बोलवा", "मृत जनावर उघडू नका कारण त्यातून घातक बीजाणू बाहेर पडतात"],
            "medications": ["सुरुवातीच्या टप्प्यात पेनिसिलिन इंजेक्शन (फक्त पशुवैद्यकाकडून)", "गाळफोड अँटीसीरम (फक्त पशुवैद्यकाकडून)"],
            "prevention": ["जास्त धोका असलेल्या भागात वार्षिक गाळफोड लसीकरण", "पूर-प्रवण भागाजवळ चराणे टाळा", "अचानक मृत्यू पशुवैद्यकीय अधिकाऱ्यांना कळवा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["reduced milk production", "weight loss", "lethargy", "swollen lymph nodes", "abnormal urine"],
        "en": {
            "disease": "Brucellosis (Contagious Abortion)",
            "severity": "High",
            "description": "Brucellosis is a bacterial disease that causes abortion in pregnant cows, infertility and reduced milk production. It is a zoonotic disease that can spread to humans through raw milk.",
            "causes": ["Brucella abortus bacteria", "Contact with aborted fetus or placenta", "Drinking contaminated water"],
            "care_instructions": ["Isolate the affected animal immediately", "Do not touch aborted material with bare hands", "Disinfect the area where abortion occurred", "Report to government veterinary officer"],
            "medications": ["No effective treatment — control by vaccination and culling", "Supportive care by vet"],
            "prevention": ["Vaccinate female calves at 4-8 months with Brucella vaccine", "Test and cull positive animals", "Do not feed raw milk to calves"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "ब्रुसेलोसिस (संसर्गजन्य गर्भपात)",
            "severity": "High",
            "description": "ब्रुसेलोसिस हा जिवाणूजन्य रोग आहे जो गाभण गायींमध्ये गर्भपात, वंध्यत्व आणि दूध कमी होण्यास कारणीभूत ठरतो. हा झुनोटिक रोग आहे जो कच्च्या दुधातून मानवांमध्ये पसरू शकतो.",
            "causes": ["Brucella abortus जिवाणू", "गर्भपात झालेल्या गर्भ किंवा वारेशी संपर्क", "दूषित पाणी पिणे"],
            "care_instructions": ["बाधित जनावराला लगेच वेगळे करा", "उघड्या हाताने गर्भपात झालेल्या साहित्याला हात लावू नका", "गर्भपात झालेल्या जागेचे निर्जंतुकीकरण करा", "सरकारी पशुवैद्यक अधिकाऱ्याला कळवा"],
            "medications": ["प्रभावी उपचार नाही — लसीकरण आणि कळपातून काढून उपाय", "पशुवैद्यकाकडून सहाय्यक काळजी"],
            "prevention": ["४-८ महिन्यांच्या मादी वासरांना ब्रुसेला लस द्या", "सकारात्मक जनावरे तपासा आणि कळपातून काढा", "वासरांना कच्चे दूध देऊ नका"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["fever", "swollen lymph nodes", "eye discharge", "nasal discharge", "lethargy", "weakness", "pale gums", "rapid breathing"],
        "en": {
            "disease": "Theileriosis (Corridor Disease)",
            "severity": "High",
            "description": "Theileriosis is a tick-borne blood parasite disease very common in India. It causes high fever, swollen lymph nodes, eye and nasal discharge and anaemia. Exotic breeds like Jersey and Holstein are more susceptible.",
            "causes": ["Theileria parasite transmitted by ticks", "High tick burden on animal", "Movement of cattle from tick-free to tick-infested areas"],
            "care_instructions": ["Remove all ticks from the animal immediately", "Apply tick control spray on the entire body", "Keep the animal in a cool shaded area", "Call vet for specific anti-theilerial treatment"],
            "medications": ["Buparvaquone injection (Butalex) — vet only", "Oxytetracycline supportive (vet only)", "Anti-fever and vitamin supplements"],
            "prevention": ["Regular tick control every 2-3 weeks", "Spray cattle shed with acaricide", "Quarantine new animals before mixing with herd"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "थायलेरिओसिस (गोचीड ताप)",
            "severity": "High",
            "description": "थायलेरिओसिस हा भारतात खूप सामान्य असलेला गोचीडजन्य रक्त परजीवी रोग आहे. यामुळे तीव्र ताप, लसीका ग्रंथी सुजणे, डोळे व नाकातून स्त्राव आणि अशक्तपणा होतो. जर्सी आणि होल्स्टीनसारख्या विदेशी जाती अधिक असुरक्षित आहेत.",
            "causes": ["गोचीडांद्वारे पसरणारा थायलेरिया परजीवी", "जनावरावर जास्त गोचीड", "गोचीडमुक्त भागातून गोचीडग्रस्त भागात जनावरे हलवणे"],
            "care_instructions": ["जनावरावरील सर्व गोचीड लगेच काढा", "संपूर्ण शरीरावर गोचीड नियंत्रण स्प्रे लावा", "जनावराला थंड सावलीच्या ठिकाणी ठेवा", "विशिष्ट उपचारांसाठी पशुवैद्यकाला बोलवा"],
            "medications": ["ब्युपार्वाक्वोन इंजेक्शन (बुटालेक्स) — फक्त पशुवैद्यकाकडून", "ऑक्सिटेट्रासायक्लिन सहाय्यक (पशुवैद्यकाकडून)", "ताप कमी करणारे आणि व्हिटॅमिन पूरक"],
            "prevention": ["दर २-३ आठवड्यांनी नियमित गोचीड नियंत्रण", "गोठ्यावर गोचीडनाशक स्प्रे करा", "नवीन जनावरांना कळपात मिसळण्यापूर्वी वेगळे ठेवा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["skin lesions", "sores", "fever", "nasal discharge", "eye discharge", "swollen lymph nodes", "reduced milk production", "weight loss"],
        "en": {
            "disease": "Lumpy Skin Disease (LSD)",
            "severity": "High",
            "description": "Lumpy Skin Disease is a viral disease that causes characteristic nodules on the skin all over the body. It spreads through biting insects and causes fever, skin nodules, reduced milk production and weight loss. It has caused major outbreaks across India in recent years.",
            "causes": ["Lumpy skin disease virus spread by mosquitoes and biting flies", "Direct contact with infected animals", "Contaminated equipment or feed"],
            "care_instructions": ["Isolate affected animals from the herd immediately", "Report to local veterinary authority", "Apply antiseptic on skin nodules to prevent secondary infection", "Provide nutritious feed and clean water"],
            "medications": ["Supportive treatment with anti-fever and antibiotics (vet)", "Lumpy skin disease vaccine"],
            "prevention": ["Vaccinate with LSD vaccine", "Control mosquitoes and biting insects", "Quarantine new animals for 28 days before mixing"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "ढेकूण रोग (Lumpy Skin Disease)",
            "severity": "High",
            "description": "ढेकूण रोग हा विषाणूजन्य रोग आहे जो संपूर्ण शरीरावर त्वचेवर गाठी निर्माण करतो. तो चावणाऱ्या कीटकांद्वारे पसरतो आणि ताप, त्वचेवर गाठी, दूध कमी होणे आणि वजन कमी होणे यास कारणीभूत ठरतो. अलिकडच्या वर्षांत भारतभर मोठ्या प्रमाणावर उद्रेक झाले आहेत.",
            "causes": ["डास आणि चावणाऱ्या माश्यांद्वारे पसरणारा ढेकूण रोग विषाणू", "संक्रमित जनावरांशी थेट संपर्क", "दूषित उपकरणे किंवा चारा"],
            "care_instructions": ["बाधित जनावरांना लगेच कळपातून वेगळे करा", "स्थानिक पशुवैद्यकीय अधिकाऱ्याला कळवा", "दुय्यम संसर्ग टाळण्यासाठी गाठींवर जंतुनाशक लावा", "पौष्टिक चारा आणि स्वच्छ पाणी द्या"],
            "medications": ["ताप कमी करणारे आणि प्रतिजैविकांसह सहाय्यक उपचार (पशुवैद्यक)", "ढेकूण रोग लस"],
            "prevention": ["LSD लस द्या", "डास आणि चावणारे कीटक नियंत्रित करा", "नवीन जनावरांना मिसळण्यापूर्वी २८ दिवस वेगळे ठेवा"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["coughing", "weight loss", "lethargy", "weakness", "reduced milk production", "rapid breathing", "loss of appetite"],
        "en": {
            "disease": "Tuberculosis (Bovine TB)",
            "severity": "High",
            "description": "Bovine Tuberculosis is a chronic bacterial disease caused by Mycobacterium bovis. It causes progressive weight loss, chronic coughing and reduced milk production. It is a serious zoonotic disease that can spread to humans through raw milk.",
            "causes": ["Mycobacterium bovis bacteria", "Inhalation of droplets from infected animals", "Drinking contaminated raw milk"],
            "care_instructions": ["Isolate the suspected animal immediately", "Contact government veterinary officer for tuberculin test", "Do not consume raw milk from the animal", "Follow government guidelines for TB-positive animals"],
            "medications": ["No practical treatment in cattle — test and cull policy", "Government compensation may be available"],
            "prevention": ["Regular tuberculin testing of herd", "Pasteurise all milk before consumption", "Maintain biosecurity on farm"],
            "urgency": "Seek vet within 1 week"
        },
        "mr": {
            "disease": "क्षयरोग (Bovine TB)",
            "severity": "High",
            "description": "बोवाइन क्षयरोग हा Mycobacterium bovis मुळे होणारा दीर्घकालीन जिवाणूजन्य रोग आहे. यामुळे हळूहळू वजन कमी होते, सततचा खोकला आणि दूध उत्पादन कमी होते. हा गंभीर झुनोटिक रोग आहे जो कच्च्या दुधातून मानवांमध्ये पसरू शकतो.",
            "causes": ["Mycobacterium bovis जिवाणू", "संक्रमित जनावरांच्या थेंबांचे श्वसन", "दूषित कच्चे दूध पिणे"],
            "care_instructions": ["संशयित जनावराला लगेच वेगळे करा", "ट्युबरक्युलिन चाचणीसाठी सरकारी पशुवैद्यक अधिकाऱ्याशी संपर्क करा", "जनावराचे कच्चे दूध पिऊ नका", "TB-सकारात्मक जनावरांसाठी सरकारी मार्गदर्शक तत्त्वांचे पालन करा"],
            "medications": ["जनावरांमध्ये व्यावहारिक उपचार नाही — चाचणी आणि कळपातून काढण्याचे धोरण", "सरकारी नुकसानभरपाई उपलब्ध असू शकते"],
            "prevention": ["कळपाची नियमित ट्युबरक्युलिन चाचणी", "सेवनापूर्वी सर्व दूध पाश्चरायझ करा", "शेतावर जैवसुरक्षा राखा"],
            "urgency": "१ आठवड्यात पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["diarrhoea", "weight loss", "lethargy", "weakness", "reduced milk production", "loss of appetite", "pale gums"],
        "en": {
            "disease": "Johne's Disease (Paratuberculosis)",
            "severity": "Medium",
            "description": "Johne's Disease is a chronic intestinal infection causing persistent diarrhoea and progressive weight loss despite normal appetite. It mainly affects adult cattle and has no effective treatment.",
            "causes": ["Mycobacterium avium subspecies paratuberculosis", "Ingestion of contaminated feed or water", "Infected cows spreading to calves"],
            "care_instructions": ["Isolate animals with persistent diarrhoea", "Provide highly digestible feed and clean water", "Consult vet for confirmation test", "Cull confirmed positive animals to protect herd"],
            "medications": ["No effective cure — supportive care only", "Electrolytes and nutritional support"],
            "prevention": ["Test herd regularly for Johne's disease", "Separate calves from adult cows at birth", "Maintain strict hygiene in calf rearing"],
            "urgency": "Seek vet within 1 week"
        },
        "mr": {
            "disease": "जोन्स रोग (Paratuberculosis)",
            "severity": "Medium",
            "description": "जोन्स रोग हा तीव्र आतड्याचा संसर्ग आहे ज्यामुळे सामान्य भूक असूनही सतत जुलाब आणि हळूहळू वजन कमी होते. हे प्रामुख्याने प्रौढ जनावरांना प्रभावित करते आणि त्यावर कोणताही प्रभावी उपचार नाही.",
            "causes": ["Mycobacterium avium subspecies paratuberculosis", "दूषित चारा किंवा पाणी खाणे-पिणे", "संक्रमित गायींकडून वासरांमध्ये पसरणे"],
            "care_instructions": ["सतत जुलाब असलेल्या जनावरांना वेगळे करा", "सहज पचणारा चारा आणि स्वच्छ पाणी द्या", "पुष्टी चाचणीसाठी पशुवैद्यकाचा सल्ला घ्या", "कळप संरक्षित करण्यासाठी सकारात्मक जनावरे काढा"],
            "medications": ["प्रभावी इलाज नाही — केवळ सहाय्यक काळजी", "इलेक्ट्रोलाइट्स आणि पोषण सहाय्य"],
            "prevention": ["जोन्स रोगासाठी कळपाची नियमित चाचणी", "जन्माच्या वेळी वासरांना प्रौढ गायींपासून वेगळे करा", "वासरू संगोपनात कठोर स्वच्छता राखा"],
            "urgency": "१ आठवड्यात पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["reduced milk production", "loss of appetite", "lethargy", "weakness", "weight loss", "tremors"],
        "en": {
            "disease": "Ketosis (Acetonaemia)",
            "severity": "Medium",
            "description": "Ketosis occurs in high-producing dairy cows in early lactation when energy demand exceeds intake. The animal has sweet acetone smell in breath, reduced milk and loss of appetite. It requires energy supplementation.",
            "causes": ["Negative energy balance after calving", "Insufficient energy-dense feed", "High milk production draining body reserves"],
            "care_instructions": ["Drench with propylene glycol 200-300ml twice daily", "Increase energy-dense concentrates in the diet", "Consult vet for glucose injection if severe", "Monitor body condition score regularly"],
            "medications": ["Propylene glycol oral drench", "Glucose IV injection (vet only)", "Vitamin B12 injection"],
            "prevention": ["Feed balanced energy diet before and after calving", "Monitor body condition score at calving", "Avoid over-fat cows at calving"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "किटोसिस (Acetonaemia)",
            "severity": "Medium",
            "description": "किटोसिस जास्त दूध देणाऱ्या गायींमध्ये प्रसूतीनंतर लवकर होतो जेव्हा ऊर्जेची मागणी सेवनापेक्षा जास्त असते. जनावराच्या श्वासात गोड एसीटोनचा वास येतो, दूध कमी होते आणि भूक कमी होते. ऊर्जा पूरक आवश्यक आहे.",
            "causes": ["प्रसूतीनंतर नकारात्मक ऊर्जा संतुलन", "अपुरे ऊर्जाघन चारा", "जास्त दूध उत्पादनामुळे शरीराचे साठे कमी होणे"],
            "care_instructions": ["दिवसातून दोनदा प्रोपिलीन ग्लायकोल २००-३०० मिली द्या", "आहारात ऊर्जाघन खुराक वाढवा", "गंभीर असल्यास ग्लुकोज इंजेक्शनसाठी पशुवैद्यकाचा सल्ला घ्या", "शरीर स्थिती स्कोर नियमितपणे निरीक्षण करा"],
            "medications": ["प्रोपिलीन ग्लायकोल तोंडावाटे द्रावण", "ग्लुकोज IV इंजेक्शन (फक्त पशुवैद्यकाकडून)", "व्हिटॅमिन B12 इंजेक्शन"],
            "prevention": ["प्रसूतीपूर्वी आणि नंतर संतुलित ऊर्जा आहार द्या", "प्रसूतीच्या वेळी शरीर स्थिती स्कोर निरीक्षण करा", "प्रसूतीच्या वेळी जास्त जाड गायी टाळा"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["eye discharge", "nasal discharge", "lethargy", "loss of appetite", "fever"],
        "en": {
            "disease": "Eye Infection (Pink Eye / IBK)",
            "severity": "Low",
            "description": "Infectious Bovine Keratoconjunctivitis (Pink Eye) is a common bacterial eye infection causing watery eye discharge, cloudiness of the eye and sensitivity to light. It spreads rapidly in a herd especially during summer and dusty conditions.",
            "causes": ["Moraxella bovis bacteria", "Spread by face flies", "Dust, bright sunlight and wind irritation"],
            "care_instructions": ["Keep the animal in a shaded area away from bright sunlight", "Clean eye discharge gently with clean wet cloth", "Apply antibiotic eye ointment prescribed by vet", "Control flies around the animal"],
            "medications": ["Oxytetracycline eye ointment", "Penicillin injection for severe cases (vet)", "Anti-fly spray"],
            "prevention": ["Control face flies with insecticide", "Provide shade in summer", "Vaccinate if available in your region"],
            "urgency": "Seek vet within 1 week"
        },
        "mr": {
            "disease": "डोळ्यांचा संसर्ग (गुलाबी डोळा)",
            "severity": "Low",
            "description": "संसर्गजन्य बोवाइन केराटोकंजंक्टिव्हायटिस (गुलाबी डोळा) हा सामान्य जिवाणूजन्य डोळा संसर्ग आहे ज्यामुळे पाणीदार डोळा स्त्राव, डोळ्याचा ढगळपणा आणि प्रकाशाची संवेदनशीलता होते. उन्हाळ्यात आणि धुळीच्या परिस्थितीत कळपात वेगाने पसरतो.",
            "causes": ["Moraxella bovis जिवाणू", "चेहऱ्यावरील माश्यांद्वारे पसरणे", "धूळ, तेज सूर्यप्रकाश आणि वाऱ्याची जळजळ"],
            "care_instructions": ["जनावराला तेज सूर्यप्रकाशापासून दूर सावलीत ठेवा", "स्वच्छ ओल्या कापडाने डोळ्यांचा स्त्राव हळुवारपणे स्वच्छ करा", "पशुवैद्यकाने सांगितलेले प्रतिजैविक डोळ्याचे मलम लावा", "जनावराभोवती माश्या नियंत्रित करा"],
            "medications": ["ऑक्सिटेट्रासायक्लिन डोळ्याचे मलम", "गंभीर प्रकरणांसाठी पेनिसिलिन इंजेक्शन (पशुवैद्यक)", "माशीविरोधी स्प्रे"],
            "prevention": ["कीटकनाशकाने चेहऱ्यावरील माश्या नियंत्रित करा", "उन्हाळ्यात सावली द्या", "तुमच्या प्रदेशात उपलब्ध असल्यास लस द्या"],
            "urgency": "१ आठवड्यात पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["skin lesions", "sores", "weight loss", "lethargy"],
        "en": {
            "disease": "Ringworm (Dermatophytosis)",
            "severity": "Low",
            "description": "Ringworm is a fungal skin infection causing circular areas of hair loss with crusty grey skin patches. It is common in young cattle during winter and spreads easily to other animals and humans by contact.",
            "causes": ["Trichophyton fungus", "Contact with infected animals or contaminated equipment", "Overcrowding and poor ventilation"],
            "care_instructions": ["Isolate affected animals from the herd", "Wear gloves when handling — it can spread to humans", "Apply antifungal ointment or iodine solution on patches", "Clean and disinfect all equipment and shed"],
            "medications": ["Griseofulvin oral medication (vet)", "Natamycin spray (vet)", "Iodine solution topical application"],
            "prevention": ["Maintain proper ventilation and reduce overcrowding", "Disinfect equipment regularly", "Quarantine new animals"],
            "urgency": "Seek vet within 1 week"
        },
        "mr": {
            "disease": "गजकर्ण (Ringworm)",
            "severity": "Low",
            "description": "गजकर्ण हा बुरशीजन्य त्वचा संसर्ग आहे ज्यामुळे राखाडी खपल्यांसह केस गळण्याचे गोल भाग होतात. हिवाळ्यात तरुण जनावरांमध्ये सामान्य आहे आणि संपर्काद्वारे इतर जनावरांमध्ये आणि मानवांमध्ये सहज पसरतो.",
            "causes": ["Trichophyton बुरशी", "संक्रमित जनावरांशी किंवा दूषित उपकरणांशी संपर्क", "गर्दी आणि खराब वायुवीजन"],
            "care_instructions": ["बाधित जनावरांना कळपातून वेगळे करा", "हाताळताना हातमोजे घाला — ते मानवांमध्ये पसरू शकते", "खपल्यांवर अँटीफंगल मलम किंवा आयोडीन द्रावण लावा", "सर्व उपकरणे आणि गोठा स्वच्छ आणि निर्जंतुक करा"],
            "medications": ["ग्रिसेओफुल्विन तोंडावाटे औषध (पशुवैद्यक)", "नाटामायसिन स्प्रे (पशुवैद्यक)", "आयोडीन द्रावण स्थानिक वापर"],
            "prevention": ["योग्य वायुवीजन राखा आणि गर्दी कमी करा", "उपकरणे नियमितपणे निर्जंतुक करा", "नवीन जनावरांना वेगळे ठेवा"],
            "urgency": "१ आठवड्यात पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["abnormal urine", "difficulty standing", "lethargy", "loss of appetite", "weight loss", "swollen abdomen"],
        "en": {
            "disease": "Urinary Tract Infection / Urolithiasis",
            "severity": "Medium",
            "description": "Urolithiasis involves formation of stones in the urinary tract causing blockage especially in male cattle. It causes straining to urinate, dribbling urine, abdominal pain and if untreated can cause bladder rupture.",
            "causes": ["High phosphorus and low calcium diet", "Inadequate water intake", "Grain-heavy diet without roughage"],
            "care_instructions": ["Encourage the animal to drink plenty of water", "Call vet immediately if the animal is straining to urinate", "Do not feed grain-heavy diet", "Provide fresh green fodder and hay"],
            "medications": ["Smooth muscle relaxants (vet only)", "Surgical removal of stones in severe cases (vet)", "Ammonium chloride to acidify urine"],
            "prevention": ["Ensure adequate water supply always", "Balance calcium to phosphorus ratio in diet", "Add ammonium chloride to diet of feedlot cattle"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "मूत्रमार्ग संसर्ग / खडे",
            "severity": "Medium",
            "description": "यूरोलिथियासिसमध्ये मूत्रमार्गात खडे तयार होतात ज्यामुळे विशेषतः नर जनावरांमध्ये अडथळा होतो. यामुळे लघवी करण्यास त्रास, लघवी थेंब थेंब पडणे, पोटदुखी होते आणि उपचार न केल्यास मूत्राशय फुटू शकते.",
            "causes": ["जास्त फॉस्फरस आणि कमी कॅल्शियम आहार", "अपुरे पाणी पिणे", "चोथ्याशिवाय जड धान्य आहार"],
            "care_instructions": ["जनावराला भरपूर पाणी पिण्यास प्रोत्साहित करा", "जनावर लघवी करण्यास त्रास देत असल्यास लगेच पशुवैद्यकाला बोलवा", "जड धान्य आहार देऊ नका", "ताजा हिरवा चारा आणि गवत द्या"],
            "medications": ["स्नायू शिथिल करणारी औषधे (फक्त पशुवैद्यकाकडून)", "गंभीर प्रकरणांमध्ये शस्त्रक्रियेद्वारे खडे काढणे (पशुवैद्यक)", "लघवी आम्लीकरणासाठी अमोनियम क्लोराइड"],
            "prevention": ["नेहमी पुरेसा पाण्याचा पुरवठा सुनिश्चित करा", "आहारात कॅल्शियम-फॉस्फरस प्रमाण संतुलित करा", "फीडलॉट जनावरांच्या आहारात अमोनियम क्लोराइड घाला"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["loss of appetite", "lethargy", "weight loss", "difficulty standing", "bloating", "swollen abdomen"],
        "en": {
            "disease": "Hardware Disease (Traumatic Reticuloperitonitis)",
            "severity": "Medium",
            "description": "Hardware disease occurs when cattle accidentally swallow sharp metal objects like nails or wire which then pierce the stomach wall. It causes sudden loss of appetite, reluctance to move and abdominal pain.",
            "causes": ["Swallowing of nails, wire or metal pieces with feed", "Grazing near construction sites", "Poor feed quality with metal contamination"],
            "care_instructions": ["Stop all feed immediately and consult vet", "Keep the animal standing on a slope with front higher", "Do not stress or move the animal unnecessarily", "Vet may use a magnet to attract the metal piece"],
            "medications": ["Rumen magnet administration (vet)", "Antibiotics for infection (vet)", "Surgery in severe cases"],
            "prevention": ["Use feed magnets in the rumen as prevention", "Keep grazing areas free of metal debris", "Check feed and hay for metal contamination"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "धातू गिळण्याचा रोग (Hardware Disease)",
            "severity": "Medium",
            "description": "धातू गिळण्याचा रोग तेव्हा होतो जेव्हा जनावरे चुकून खिळे किंवा तार यांसारख्या धारदार धातूच्या वस्तू गिळतात ज्या नंतर पोटाची भिंत छेदतात. यामुळे अचानक भूक न लागणे, हालचाल करण्यास नकार आणि पोटदुखी होते.",
            "causes": ["चाऱ्यासह खिळे, तार किंवा धातूचे तुकडे गिळणे", "बांधकाम स्थळांजवळ चराणे", "धातू दूषिततेसह खराब चाऱ्याची गुणवत्ता"],
            "care_instructions": ["सर्व चारा लगेच थांबवा आणि पशुवैद्यकाचा सल्ला घ्या", "जनावराला पुढचा भाग उंच असलेल्या उतारावर उभे ठेवा", "जनावराला अनावश्यक ताण देऊ नका किंवा हलवू नका", "पशुवैद्यक धातूचा तुकडा आकर्षित करण्यासाठी चुंबक वापरू शकतात"],
            "medications": ["रुमेन चुंबक प्रशासन (पशुवैद्यक)", "संसर्गासाठी प्रतिजैविक (पशुवैद्यक)", "गंभीर प्रकरणांमध्ये शस्त्रक्रिया"],
            "prevention": ["प्रतिबंध म्हणून रुमेनमध्ये चाऱ्याचे चुंबक वापरा", "चराणे क्षेत्र धातूच्या मलब्यापासून मुक्त ठेवा", "धातू दूषिततेसाठी चारा आणि गवत तपासा"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["limping", "lameness", "difficulty standing", "swollen", "sores", "skin lesions"],
        "en": {
            "disease": "Hoof Rot (Foot Rot)",
            "severity": "Medium",
            "description": "Foot rot is a bacterial infection between the toes of cattle causing severe lameness, swelling and foul-smelling lesions. It is common during monsoon when cattle stand in muddy wet conditions for long periods.",
            "causes": ["Fusobacterium necrophorum bacteria", "Wet and muddy conditions causing skin damage between toes", "Wounds or cracks in hoof"],
            "care_instructions": ["Clean the affected foot thoroughly with clean water", "Apply antiseptic spray or copper sulphate solution between toes", "Keep the animal on dry ground", "Consult vet for antibiotic treatment"],
            "medications": ["Oxytetracycline injection (vet)", "Penicillin injection (vet)", "Zinc sulphate foot bath"],
            "prevention": ["Maintain dry and clean cattle shed", "Trim hooves regularly", "Use foot bath with zinc or copper sulphate solution"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "खुरांचा सडणे (Hoof Rot)",
            "severity": "Medium",
            "description": "खुरांचा सडणे हा जनावरांच्या बोटांमधील जिवाणूजन्य संसर्ग आहे ज्यामुळे तीव्र लंगडणे, सूज आणि दुर्गंधीयुक्त जखमा होतात. पावसाळ्यात जेव्हा जनावरे बराच वेळ चिखलात उभी राहतात तेव्हा हे सामान्य असते.",
            "causes": ["Fusobacterium necrophorum जिवाणू", "ओल्या आणि चिखलाच्या परिस्थितीमुळे बोटांमधील त्वचेला इजा", "खुरांमधील जखमा किंवा भेगा"],
            "care_instructions": ["बाधित पाय स्वच्छ पाण्याने नीट स्वच्छ करा", "बोटांमध्ये जंतुनाशक स्प्रे किंवा कॉपर सल्फेट द्रावण लावा", "जनावराला कोरड्या जमिनीवर ठेवा", "प्रतिजैविक उपचारांसाठी पशुवैद्यकाचा सल्ला घ्या"],
            "medications": ["ऑक्सिटेट्रासायक्लिन इंजेक्शन (पशुवैद्यक)", "पेनिसिलिन इंजेक्शन (पशुवैद्यक)", "झिंक सल्फेट पाय स्नान"],
            "prevention": ["कोरडा आणि स्वच्छ गोठा राखा", "नियमितपणे खुरे छाटा", "झिंक किंवा कॉपर सल्फेट द्रावणाने पाय स्नान वापरा"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["swollen", "fever", "lethargy", "weakness", "difficulty standing", "loss of appetite"],
        "en": {
            "disease": "Navel Ill (Umbilical Infection in Calves)",
            "severity": "Medium",
            "description": "Navel ill is a bacterial infection of the umbilical cord stump in newborn calves. It causes swelling, pain and fever and can spread to joints and internal organs if not treated early.",
            "causes": ["Bacterial infection entering through wet umbilical cord", "Dirty calving environment", "Failure to disinfect navel at birth"],
            "care_instructions": ["Clean the navel area with iodine tincture 3-4 times daily", "Keep the calf in a clean dry area", "Ensure the calf receives colostrum within first hour of birth", "Consult vet if swelling does not reduce in 2 days"],
            "medications": ["Iodine solution for navel dressing", "Penicillin injection (vet)", "Anti-inflammatory drugs (vet)"],
            "prevention": ["Dip navel in 7% iodine solution immediately after birth", "Ensure clean dry calving area", "Feed colostrum within 6 hours of birth"],
            "urgency": "Seek vet within 48 hours"
        },
        "mr": {
            "disease": "नाभी संसर्ग (वासरांमध्ये)",
            "severity": "Medium",
            "description": "नाभी संसर्ग हा नवजात वासरांमधील नाळेच्या स्टंपचा जिवाणूजन्य संसर्ग आहे. यामुळे सूज, वेदना आणि ताप येतो आणि लवकर उपचार न केल्यास सांधे आणि अंतर्गत अवयवांमध्ये पसरू शकतो.",
            "causes": ["ओल्या नाळेतून जिवाणू संसर्ग", "अस्वच्छ प्रसूती वातावरण", "जन्माच्या वेळी नाभी निर्जंतुक न करणे"],
            "care_instructions": ["नाभी भाग दिवसातून ३-४ वेळा आयोडीन टिंचरने स्वच्छ करा", "वासरांना स्वच्छ कोरड्या जागी ठेवा", "वासराला जन्मानंतर पहिल्या तासात चीक मिळेल याची खात्री करा", "२ दिवसात सूज कमी न झाल्यास पशुवैद्यकाचा सल्ला घ्या"],
            "medications": ["नाभी ड्रेसिंगसाठी आयोडीन द्रावण", "पेनिसिलिन इंजेक्शन (पशुवैद्यक)", "दाहविरोधी औषधे (पशुवैद्यक)"],
            "prevention": ["जन्मानंतर लगेच नाभी ७% आयोडीन द्रावणात बुडवा", "स्वच्छ कोरडे प्रसूती क्षेत्र सुनिश्चित करा", "जन्मानंतर ६ तासांच्या आत चीक द्या"],
            "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
        }
    },
    {
        "keywords": ["tremors", "convulsions", "difficulty standing", "rapid breathing", "lethargy", "loss of appetite"],
        "en": {
            "disease": "Grass Tetany (Hypomagnesaemia)",
            "severity": "High",
            "description": "Grass Tetany occurs when cattle graze on lush green grass low in magnesium. It causes muscle tremors, convulsions and can lead to death if untreated. It is most common in lactating cows in spring season.",
            "causes": ["Low magnesium in lush grass pastures", "High potassium in fertilised pastures blocking magnesium absorption", "Lactating cows with high magnesium demand"],
            "care_instructions": ["Call vet immediately — this is an emergency", "Keep the animal calm and away from bright light", "Do not restrain a convulsing animal forcefully", "Vet will administer magnesium injection under skin"],
            "medications": ["Magnesium sulphate subcutaneous injection (vet only)", "Calcium-magnesium solution IV (vet only)"],
            "prevention": ["Supplement magnesium in feed or water during spring grazing", "Avoid sudden turnout onto lush green pasture", "Feed magnesium-rich hay alongside green grazing"],
            "urgency": "Seek vet within 24 hours"
        },
        "mr": {
            "disease": "गवत टेटनी (Hypomagnesaemia)",
            "severity": "High",
            "description": "गवत टेटनी तेव्हा होतो जेव्हा जनावरे मॅग्नेशियम कमी असलेल्या हिरव्यागार गवतावर चरतात. यामुळे स्नायूंमध्ये थरथर, झटके येतात आणि उपचार न केल्यास मृत्यू होऊ शकतो. वसंत ऋतूत दूध देणाऱ्या गायींमध्ये हे सर्वात सामान्य आहे.",
            "causes": ["हिरव्यागार गवत चराणात मॅग्नेशियम कमी", "खतयुक्त चराणात जास्त पोटॅशियम मॅग्नेशियम शोषण रोखते", "जास्त मॅग्नेशियम मागणी असलेल्या दूध देणाऱ्या गायी"],
            "care_instructions": ["पशुवैद्यकाला लगेच बोलवा — ही आणीबाणी आहे", "जनावराला शांत आणि तेज प्रकाशापासून दूर ठेवा", "झटके येणाऱ्या जनावराला जबरदस्तीने रोखू नका", "पशुवैद्यक त्वचेखाली मॅग्नेशियम इंजेक्शन देतील"],
            "medications": ["मॅग्नेशियम सल्फेट त्वचेखाली इंजेक्शन (फक्त पशुवैद्यकाकडून)", "कॅल्शियम-मॅग्नेशियम द्रावण IV (फक्त पशुवैद्यकाकडून)"],
            "prevention": ["वसंत ऋतूतील चराणादरम्यान चारा किंवा पाण्यात मॅग्नेशियम पूरक द्या", "हिरव्यागार कुरणावर अचानक सोडणे टाळा", "हिरव्या चराणासोबत मॅग्नेशियमयुक्त गवत द्या"],
            "urgency": "२४ तासांत पशुवैद्यकाकडे जा"
        }
    }
]

# ─── Diagnosis Function ───────────────────────────────────────────────────────

def diagnose(symptoms, lang="en"):
    symptoms_lower = [s.lower() for s in symptoms]

    def score(disease):
        count = 0
        for kw in disease["keywords"]:
            for sym in symptoms_lower:
                if kw in sym or sym in kw:
                    count += 1
        return count

    scored = [(score(d), d) for d in DISEASE_DB]
    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_disease = scored[0]

    contacts = CONTACTS_MR if lang == "mr" else CONTACTS_EN

    if best_score == 0:
        if lang == "mr":
            return {
                "disease": "सामान्य आरोग्य समस्या",
                "confidence": "Low",
                "severity": "Medium",
                "description": "नोंदवलेल्या लक्षणांच्या आधारे विशिष्ट रोग ओळखता आला नाही. योग्य तपासणी आणि निदानासाठी कृपया पशुवैद्यक अधिकाऱ्याचा सल्ला घ्या.",
                "causes": ["अनेक संभाव्य कारणे", "पशुवैद्यकाकडून शारीरिक तपासणी आवश्यक", "पोषण किंवा संसर्गजन्य असू शकते"],
                "care_instructions": ["जनावराला कळपातून वेगळे करा", "स्वच्छ पाणी आणि चांगला चारा द्या", "बिघडणाऱ्या लक्षणांसाठी जनावरावर जवळून लक्ष ठेवा", "तपासणीसाठी स्थानिक पशुवैद्यकाशी संपर्क करा"],
                "medications": ["पशुवैद्यकीय तपासणीनंतर सांगितल्याप्रमाणे"],
                "prevention": ["नियमित लसीकरण", "योग्य पोषण आणि स्वच्छ पाणी", "नियमित पशुवैद्यकीय तपासणी"],
                "contacts": contacts,
                "urgency": "४८ तासांत पशुवैद्यकाकडे जा"
            }
        else:
            return {
                "disease": "General Health Issue",
                "confidence": "Low",
                "severity": "Medium",
                "description": "Based on the symptoms reported, a specific disease could not be identified. Please consult a veterinary officer for a proper physical examination and diagnosis.",
                "causes": ["Multiple possible causes", "Requires physical examination by a vet", "May be nutritional or infectious"],
                "care_instructions": ["Isolate the animal from the herd", "Ensure clean water and good quality feed", "Monitor the animal closely for worsening symptoms", "Contact your local vet for examination"],
                "medications": ["As prescribed by veterinarian after examination"],
                "prevention": ["Regular vaccination", "Proper nutrition and clean water", "Routine veterinary checkups"],
                "contacts": contacts,
                "urgency": "Seek vet within 48 hours"
            }

    confidence = "High" if best_score >= 3 else "Medium" if best_score >= 2 else "Low"
    data = best_disease[lang] if lang in best_disease else best_disease["en"]

    return {
        "disease": data["disease"],
        "confidence": confidence,
        "severity": data["severity"],
        "description": data["description"],
        "causes": data["causes"],
        "care_instructions": data["care_instructions"],
        "medications": data["medications"],
        "prevention": data["prevention"],
        "contacts": contacts,
        "urgency": data["urgency"]
    }


@app.route("/")
def home():
    return "Backend is running!"


# ─── Breed Prediction ────────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    file = request.files["image"]
    try:
        img = image.load_img(BytesIO(file.read()), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        pred_index = int(np.argmax(preds))
        confidence = float(np.max(preds) * 100)
        return jsonify({"breed": class_labels[pred_index], "confidence": round(confidence, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── Health Diagnosis ────────────────────────────────────────────────────────
@app.route("/health-diagnosis", methods=["POST"])
def health_diagnosis():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms", [])
        lang     = data.get("lang", "en")

        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        report = diagnose(symptoms, lang)
        return jsonify(report)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("HEALTH DIAGNOSIS ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)