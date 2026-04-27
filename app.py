from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration
import time
import io
import PyPDF2
import docx

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- BOOT UP THE AI BRAIN ---
print("🧠 Loading AiStud Brain... This might take 10-20 seconds...")
try:
    MODEL_PATH = "./aistud_trained_model"
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
    print("✅ AiStud T5 Brain is Online and Ready!")
except Exception as e:
    print(f"❌ ERROR LOADING MODEL: {e}\nMake sure the folder name is exactly 'aistud_trained_model' and sits next to app.py")

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
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            print(f"📄 Receiving File: {file.filename}")
            return extract_text(file)
            
    if request.is_json:
        return request.json.get('text', '')
        
    if 'text' in request.form:
        return request.form.get('text', '')
        
    return ""

# --- ENDPOINTS ---
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# We keep summarize as mock until we train the BART model!
@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    try:
        raw_text = get_payload_text()
        if not raw_text:
            return jsonify({"error": "No text or readable file provided"}), 400
            
        print(f"✅ Text Extracted: {len(raw_text)} characters.")
        time.sleep(2) 

        return jsonify({
            "status": "success",
            "summary": f"SUCCESS! The server extracted {len(raw_text)} characters. (BART Summarization Model coming soon!)"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- THE REAL AI QUIZ ENDPOINT ---
@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    try:
        raw_text = get_payload_text()
        if not raw_text:
            return jsonify({"error": "No text or readable file provided"}), 400
            
        print(f"✅ Text Extracted: {len(raw_text)} characters.")
        
        # 1. Prepare text (We take the first 1500 chars to prevent RAM overload on your PC)
        input_text = f"generate questions: {raw_text[:1500]}"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        
        # 2. Let the AI generate!
        print("🧠 AI is thinking...")
        outputs = model.generate(input_ids, max_length=128)
        ai_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Raw AI Output: {ai_response}")
        
        # 3. Parse the AI string into standard JSON format
        question_text = "Could not parse question properly."
        options_array = ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
        correct_answer = ""
        
        try:
            # We split the string based on the format we taught it in Colab
            q_part = ai_response.split("Options:")[0].replace("Question:", "").strip()
            opt_part = ai_response.split("Options:")[1].split("Answer:")[0].strip()
            ans_part = ai_response.split("Answer:")[1].strip()
            
            question_text = q_part
            correct_answer = ans_part
            options_array = [o.strip() for o in opt_part.split(",")]
        except Exception as e:
            print(f"Parsing Warning (AI hallucinated format): {e}")
            question_text = ai_response # Fallback to show the raw string if parsing fails

        # 4. Return the dynamically generated data
        return jsonify({
            "status": "success",
            "questions": [
                {
                    "id": 1,
                    "question": question_text,
                    "options": options_array,
                    "correctAnswer": correct_answer,
                    "explanation": "Generated locally by your custom AiStud T5 Engine!"
                }
            ]
        }), 200
        
    except Exception as e:
        print(f"Quiz Generation Error: {e}")
        return jsonify({"error": str(e)}), 500

# Keep Flashcards mock for now
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
                {"id": 1, "front": "Server Connection", "back": "Success! System connected to the backend."},
                {"id": 2, "front": "Next Step", "back": "Connect the Flashcard model."}
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) # Turned off debug to prevent double-loading the heavy AI model