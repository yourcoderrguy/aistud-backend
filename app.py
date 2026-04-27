from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import io
import PyPDF2
import docx

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- HELPER: TEXT EXTRACTION ENGINE ---
def extract_text(file_storage):
    filename = file_storage.filename.lower()
    raw_text = ""
    
    try:
        if filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file_storage)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    raw_text += text + "\n"
        elif filename.endswith('.docx'):
            doc = docx.Document(file_storage)
            for para in doc.paragraphs:
                raw_text += para.text + "\n"
        else:
            raw_text = file_storage.read().decode('utf-8', errors='ignore')
            
        return raw_text.strip()
    except Exception as e:
        print(f"Extraction Error: {e}")
        return ""

# --- ROUTER HELPER: HANDLE INCOMING DATA ---
def get_payload_text():
    # 1. Did the phone send a file?
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            print(f"📄 Receiving File: {file.filename}")
            return extract_text(file)
            
    # 2. Did the phone send pure JSON text?
    if request.is_json:
        return request.json.get('text', '')
        
    # 3. Did the phone send text alongside a file in a form?
    if 'text' in request.form:
        return request.form.get('text', '')
        
    return ""

# --- ENDPOINTS ---
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    try:
        raw_text = get_payload_text()
        if not raw_text:
            return jsonify({"error": "No text or readable file provided"}), 400
            
        print(f"✅ Text Extracted: {len(raw_text)} characters.")
        time.sleep(2) # Simulate AI Processing

        return jsonify({
            "status": "success",
            "summary": f"SUCCESS! The server extracted {len(raw_text)} characters from your input. When BART is trained, it will summarize this data here."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    try:
        raw_text = get_payload_text()
        if not raw_text:
            return jsonify({"error": "No text or readable file provided"}), 400
            
        print(f"✅ Text Extracted: {len(raw_text)} characters.")
        time.sleep(2)

        return jsonify({
            "status": "success",
            "questions": [
                {
                    "id": 1,
                    "question": f"The server read {len(raw_text)} characters. What is the time complexity of a BST?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                    "correctAnswer": "O(log n)",
                    "explanation": "Because the tree is balanced."
                }
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/flashcards', methods=['POST'])
def generate_flashcards():
    try:
        raw_text = get_payload_text()
        if not raw_text:
            return jsonify({"error": "No text or readable file provided"}), 400
            
        print(f"✅ Text Extracted: {len(raw_text)} characters.")
        time.sleep(2)

        return jsonify({
            "status": "success",
            "flashcards": [
                {"id": 1, "front": "Server Connection Status", "back": f"Success! Read {len(raw_text)} characters from your file/text."},
                {"id": 2, "front": "Next Step", "back": "Begin fine-tuning the AI models in Google Colab."}
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)