# from gtts import gTTS
# import os
# def extract_text_from_file(filename):
#     # Check extension
#     ext = os.path.splitext(filename)[1].lower()
    
#     if ext == ".txt":
#         with open(filename, "r", encoding="utf-8") as f:
#             return f.read()
    
#     elif ext == ".pdf":
#         import PyPDF2
#         text = ""
#         with open(filename, "rb") as f:
#             reader = PyPDF2.PdfReader(f)
#             for page in reader.pages:
#                 text += page.extract_text() or ""  
#         return text
    
#     else:
#         raise ValueError("Unsupported file type. Please upload a .txt or .pdf")
# # Convert to speech
# text = extract_text_from_file("input.txt") 
# tts = gTTS(text=text, lang='en')
# tts.save("output.mp3")

from flask import Flask, request, send_file, render_template
from gtts import gTTS
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FILE = "static/output.mp3"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    else:
        raise ValueError("Unsupported file type. Please upload a .txt or .pdf")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_input = request.form.get("text_input", "").strip()
        uploaded_file = request.files.get("file")

        # Validate input
        if uploaded_file and uploaded_file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            text = extract_text_from_file(file_path)
        elif text_input:
            text = text_input
        else:
            return "No input provided!", 400

        # Convert text to speech
        tts = gTTS(text=text, lang='en')
        tts.save(OUTPUT_FILE)

        return render_template("index.html", audio_generated=True)

    return render_template("index.html", audio_generated=False)

if __name__ == "__main__":
    app.run(debug=True)
