from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import PyPDF2
from docx import Document
import spacy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Helper Functions ---
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        raise Exception(f"PDF processing error: {str(e)}")

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return " ".join([para.text for para in doc.paragraphs if para.text])
    except Exception as e:
        raise Exception(f"DOCX processing error: {str(e)}")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise Exception("spaCy model 'en_core_web_sm' not found. Run 'python -m spacy download en_core_web_sm'")

SKILLS_DATABASE = {
    "python", "flask", "sql", "pandas", "numpy", "tensorflow", "pytorch",
    "scikit-learn", "machine learning", "deep learning", "html", "css", 
    "javascript", "react", "angular", "java", "spring", "docker", 
    "aws", "azure", "git", "django", "mongodb", "tableau", "power bi",
    "linux", "jenkins", "kubernetes", "opencv"
}


def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for token in doc:
        if token.text.lower() in SKILLS_DATABASE:
            skills.add(token.text.lower())
    return list(skills)

def predict_roles(resume_text):
    resume_text = resume_text.lower()

    # --- Weighted role-skill mapping ---
    role_skill_map = {
        "Data Scientist": {
            "python": 2, "pandas": 2, "numpy": 2, 
            "tensorflow": 3, "pytorch": 3, "machine learning": 3,
            "deep learning": 3, "scikit-learn": 2
        },
        "Data Analyst": {
            "python": 1, "sql": 2, "tableau": 2, "power bi": 2,
            "excel": 2, "pandas": 1, "data visualization": 2
        },
        "Frontend Developer": {
            "javascript": 2, "html": 2, "css": 2, 
            "react": 3, "angular": 3, "bootstrap": 1
        },
        "Backend Developer": {
            "java": 2, "c#": 2, "spring": 2, 
            ".net": 2, "flask": 3, "django": 3, "sql": 2
        },
        "DevOps Engineer": {
            "aws": 2, "azure": 2, "docker": 2, 
            "kubernetes": 2, "ci/cd": 2, "jenkins": 2, "linux": 1
        }
    }

    # --- Calculate scores for each role ---
    role_scores = {role: 0 for role in role_skill_map}

    for role, skills in role_skill_map.items():
        for skill, weight in skills.items():
            if skill in resume_text:
                role_scores[role] += weight

    # --- Remove roles with zero score ---
    filtered_roles = {r: s for r, s in role_scores.items() if s > 0}
    if not filtered_roles:
        return [{"role": "No relevant role found", "confidence": 0}]

    # --- Normalize scores into percentages ---
    max_score = max(filtered_roles.values())
    total_score = sum(filtered_roles.values())

    roles_with_confidence = []
    for role, score in filtered_roles.items():
        confidence = round((score / max_score) * 100, 1)
        roles_with_confidence.append({"role": role, "confidence": confidence})

    # --- Sort by confidence descending ---
    roles_with_confidence.sort(key=lambda x: x["confidence"], reverse=True)

    # --- Return top 3 ---
    return roles_with_confidence[:3]

# --- Flask Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Secure the filename and save temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(filepath)
        else:
            return jsonify({"error": "Unsupported file type. Please upload PDF or DOCX."}), 400
        
        # Analyze the text
        roles = predict_roles(text)
        skills = extract_skills(text)
        
        return jsonify({
            "roles": roles[:3],  # Return top 3 roles
            "skills_found": skills,
            "message": "Analysis successful"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        # Clean up the uploaded file
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)