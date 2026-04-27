from flask import Flask, request, jsonify
from flask_cors import CORS
import time

# Initialize the Flask App
app = Flask(__name__)

# Configure CORS to allow your React Native app to connect securely
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- HEALTH CHECK ---
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "AISTUD Backend is running natively"}), 200

# --- 1. SUMMARIZATION ENDPOINT (BART-Base) ---
@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
            
        # Simulate AI model inference time
        time.sleep(2) 

        return jsonify({
            "status": "success",
            "summary": "This is a simulated AI summary. When Phase D is complete, your fine-tuned BART model output will dynamically generate here based on the text you upload."
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. QUIZ GENERATION ENDPOINT (T5-Base) ---
@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
            
        time.sleep(2)

        mock_questions = [
            {
                "id": 1,
                "question": "What is the time complexity of searching for an element in a balanced Binary Search Tree (BST)?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correctAnswer": "O(log n)",
                "explanation": "Because the tree is balanced, every step down cuts the remaining nodes in half."
            },
            {
                "id": 2,
                "question": "Which data structure uses a LIFO (Last In, First Out) principle?",
                "options": ["Queue", "Linked List", "Stack", "Array"],
                "correctAnswer": "Stack",
                "explanation": "A stack operates like a stack of plates; the last plate you put on top is the first one you take off."
            }
        ]

        return jsonify({
            "status": "success",
            "questions": mock_questions
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. FLASHCARDS ENDPOINT (T5-Base) ---
@app.route('/api/flashcards', methods=['POST'])
def generate_flashcards():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
            
        time.sleep(2)

        mock_flashcards = [
            {
                "id": 1,
                "front": "Binary Search Tree (BST)",
                "back": "A node-based tree data structure where the left child is always smaller than the parent, and the right child is always larger."
            },
            {
                "id": 2,
                "front": "LIFO",
                "back": "Last In, First Out. A data management principle where the most recently added item is the first one to be removed (e.g., a Stack)."
            },
            {
                "id": 3,
                "front": "Hash Table",
                "back": "A data structure that implements an associative array abstract data type, allowing for highly efficient O(1) lookups."
            }
        ]

        return jsonify({
            "status": "success",
            "flashcards": mock_flashcards
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    # Running on port 5000 with debug mode ON for local development
    app.run(host='0.0.0.0', port=5000, debug=True)