# Smart Resume Reviewer

## 📄 Overview
**Smart Resume Reviewer** is an AI-powered web application that reviews resumes against a target job role and an optional job description. It provides structured feedback, identifies skill gaps, and generates an improved resume draft using generative AI.

---

## ⭐ Key Highlights (Core Features)
- Accepts resumes via **PDF/TXT upload** or **direct text input**
- Allows users to specify a **target job role**
- Supports an **optional job description** for role-specific analysis
- Extracts text from PDF resumes on the backend
- Uses **Google Gemini AI** to:
  - Generate constructive resume feedback
  - Identify **skills already present** in the resume
  - Detect **important missing skills**
  - Produce an **improved resume draft**
- Returns a **structured JSON response** for reliable frontend rendering
- Dynamic UI updates using JavaScript (no page reloads)
- Clean, responsive, and user-friendly interface

---

## 🛠 Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Flask, Flask-CORS  
- **AI Integration:** Google Gemini API (`gemini-1.5-flash`)  

---

## 🗂 Project Structure
templates/ → index.html
static/ → style.css, script.js
app.py → Flask backend & AI logic
requirements.txt → dependencies


---

## ▶️ Run Locally
```bash
pip install -r requirements.txt
export MY_API_KEY=your_gemini_api_key
python app.py
Open in browser:
http://127.0.0.1:5000/

---

## 🎯 Objective
To build a practical AI-driven resume review tool while gaining hands-on experience with Flask, file handling, frontend–backend integration, and generative AI.

---

⭐ If you find this project useful, feel free to star the repository!

⭐ If you find this project useful, feel free to star the repository!
