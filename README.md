🧠 AI Resume Role Analyzer

An intelligent Flask-based web application that analyzes resumes (PDF/DOCX), extracts skills using NLP, and recommends the most suitable job roles (like Data Scientist, Analyst, Developer, or DevOps Engineer) with confidence percentages.

![image alt](<img width="1218" height="876" alt="image" src="https://github.com/user-attachments/assets/08877e29-8cde-448c-aa8e-b0d88b39a1bb" />
)

🚀 Features

✅ Upload and analyze resumes in PDF or DOCX format
✅ Extract relevant technical skills using spaCy NLP
✅ Predict top 3 matching job roles based on skills
✅ Confidence score visualization for each role
✅ Clean and modern web interface (HTML, CSS, JavaScript)
✅ Lightweight and easy to deploy

🧩 Tech Stack

Backend: Flask (Python)

Frontend: HTML5, CSS3, Vanilla JavaScript

NLP: spaCy (en_core_web_sm)

Libraries: PyPDF2, python-docx

Model Logic: Rule-based skill weighting

📂 Project Structure
AI-Resume-Role-Analyzer/
│
├── app.py                     # Main Flask app
├── templates/
│   └── index.html             # Frontend page
├── uploads/                   # Temporary file storage
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation

⚙️ Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/Aishwaryabagi/AI-Resume-Role-Analyzer.git
cd AI-Resume-Role-Analyzer


2️⃣ Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Download spaCy model

python -m spacy download en_core_web_sm


5️⃣ Run the app

python app.py


6️⃣ Open in browser

http://127.0.0.1:5000/

📊 How It Works

1️⃣ The user uploads a resume file (PDF/DOCX)
2️⃣ Flask extracts text using PyPDF2 or python-docx
3️⃣ spaCy processes the text to find keywords from a skills database
4️⃣ Each detected skill is scored against predefined role-skill weights
5️⃣ The app displays the top 3 suitable job roles with confidence percentages
6️⃣ Extracted skills are shown as tags on the web interface
