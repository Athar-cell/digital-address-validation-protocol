🚀 AAVA – Address Authentication & Validation Agency
Hybrid ML + DIGIPIN + Rule Engine for Secure National Address Validation

Built for DHRUVA & Digital Address Project, Government of India

🧭 Overview

AAVA (Address Authentication & Validation Agency) is a hybrid AI + rule-based engine that validates any Indian address using:

DIGIPIN (National 4m x 4m geospatial grid)

ML/NLP semantic validation

Rule-based administrative checks

Geospatial consistency metrics

Behavioral signals from AIUs (delivery success)

This project implements a real-world prototype of the validation layer proposed in the Digital Address Project (DAP) and aligns with the DHRUVA framework.

✨ Key Features
🔹 1. DIGIPIN Validation

Decodes DIGIPIN → extracts centroid → validates geographic correctness.

🔹 2. NLP-Based Address Parsing

Extracts:

house number

locality

sector

district

PIN code

landmark

Uses lightweight regex + rule-based NLP.

🔹 3. ML Semantic Similarity

Powered by Sentence Transformers / IndicBERT embeddings
Checks if address text and geo-location “semantically match”.

🔹 4. Rule Engine

Hard validations:

PIN–district mismatch

Locality mismatch

Invalid DIGIPIN

Boundary errors

🔹 5. Confidence Score (0–100)

Weighted hybrid metric:

C = 0.4 * RuleScore + 0.4 * MLScore + 0.2 * GeoScore

🔹 6. Interactive Web UI

A lightweight web app where user enters:

DIGIPIN

Address Text

And receives:

Parsed metadata

ML scores

Rule failures

Final confidence

System decision

🖥️ Tech Stack
Component	Technology
Backend	Python (FastAPI / Flask optional)
ML	Sentence Transformers / Indic NLP
UI	HTML + TailwindCSS
Geospatial	DIGIPIN reverse decoder
Storage (optional)	SQLite / JSON
Deployment	Docker or local run
📂 Repository Structure
📦 aava-address-validation-engine
 ┣ 📁 src
 │   ┣ digipin_decoder.py
 │   ┣ ml_engine.py
 │   ┣ rule_engine.py
 │   ┣ geo_engine.py
 │   ┣ confidence.py
 │   ┣ validate.py
 │   ┗ utils.py
 ┣ 📁 examples
 │   ┗ sample_inputs.json
 ┣ README.md
 ┣ requirements.txt
 ┗ run.py

🧪 Running the Engine
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the engine with sample inputs
python run.py --file examples/sample_inputs.json

3️⃣ Output

The engine returns:

Parsed fields

ML similarity

Rule score

Geo score

Final confidence

Decision

Reasons

Example output:

{
  "digipin": "39J49LL8T4",
  "address_text": "Dak Bhawan, 77, Sansad Marg, New Delhi, 110001",
  "rule_score": 28.0,
  "ml_score": 35.33,
  "geo_score": 5.0,
  "confidence": 65.83,
  "decision": "Needs Attention"
}

🌐 Running the Web App
Start local server:
python -m http.server 8000

Open browser:
http://localhost:8000/web/index.html


You’ll see a clean UI:

Enter DIGIPIN

Enter Address

Click Validate

Output appears on screen with color-coded results.

🔬 Validation Flow (Architecture)
User Input → NLP Parsing
           → Rule Engine → Scores
           → ML Similarity → Scores
           → Geo Engine → Scores
           ---------------------------
                   ↓
         Confidence Score (0–100)
                   ↓
              Final Decision

📊 Decision Thresholds
Confidence	Decision
95–100	Auto-Approved
85–94	High Confidence
70–84	Verified
55–69	Needs Attention
<55	Physical Verification Required
📦 Sample Use-Cases
🛒 E-commerce

Avoid delivery failures.

🏦 Banking (KYC)

Prevent fake/mismatched addresses.

🚨 Emergency Services

Accurate location mapping.

🛂 Government

Address-based service delivery.

⚖️ License

MIT Licence — free for commercial & research use.

🧑‍💻 Author

Athar Sharma
B.Tech CSE | Data Science | AI
DIT University

⭐ Support the Project

Give a ⭐ star on GitHub if this helped you!
