import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from google import genai

# Create Gemini client using API key from environment
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
app = Flask(__name__)
CORS(app)  # allow requests from frontend

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/review", methods=["POST"])
def review_resume():
    print("FORM DATA:", request.form)
    print("FILES DATA:", request.files)
    role = request.form.get("role")
    jd = request.form.get("jd", "")
    resume_text = ""

    # Handle resume file or text
    if "resumeFile" in request.files:
        file = request.files["resumeFile"]
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = filename.split(".")[-1].lower()
            if ext == "txt":
                resume_text = file.read().decode("utf-8")
            elif ext == "pdf":
                try:
                    import PyPDF2
                    print("PyPDF2 imported successfully")
                    reader = PyPDF2.PdfReader(file)
                    print("PDF reader created")
                    extracted_pages = []
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            extracted_pages.append(text)

                    resume_text = " ".join(extracted_pages)
                    print("EXTRACTED RESUME TEXT LENGTH:", len(resume_text))
                except Exception as e:
                    print("PDF PARSE ERROR:", str(e))
                    return jsonify({"error": f"Failed to parse PDF: {str(e)}"}), 400
            else:
                return jsonify({"error": "Unsupported file format"}), 400
    else:
        resume_text = request.form.get("resumeText", "")

    if not role or not resume_text.strip():
        return jsonify({"error": "Role and resume text/file required"}), 400

    # Call Gemini API
    prompt = f"""
    You are an AI resume reviewer.
    Target Role: {role}
    Job Description (optional): {jd}
    Resume: {resume_text}

    Return ONLY a valid JSON object with keys:
    - feedback: string (constructive feedback)
    - present: array of strings (skills already in resume)
    - missing: array of strings (important skills missing)
    - improved_resume: string (improved resume draft)
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        text_response = response.text.strip()


        print("Gemini raw response:\n", text_response)  # debug log

        # If Gemini wrapped JSON in a code block, strip it
        if text_response.startswith("```"):
            text_response = text_response.strip("`")
            if text_response.startswith("json"):
                text_response = text_response[4:].strip()

        # Parse JSON safely
        try:
            data = json.loads(text_response)
        except Exception as e:
            print("JSON parse error:", e)
            data = {
                "feedback": text_response,
                "present": [],
                "missing": [],
                "improved_resume": ""
            }

        # normalize response
        safe_data = {
            "feedback": data.get("feedback", ""),
            "present": data.get("present", []),
            "missing": data.get("missing", []),
            "improved_resume": data.get("improved_resume", "")
        }
        if isinstance(safe_data["present"], str):
            safe_data["present"] = [safe_data["present"]]
        if isinstance(safe_data["missing"], str):
            safe_data["missing"] = [safe_data["missing"]]

        return jsonify(safe_data)

        except Exception as e:
            print("GEMINI ERROR:", str(e))   # <-- ADD THIS LINE
            return jsonify({
                "feedback": f"Error while generating response: {str(e)}",
                "present": [],
                "missing": [],
                "improved_resume": ""
            }), 500



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port,debug=True)
