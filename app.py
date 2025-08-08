from flask import Flask, request, jsonify
import asyncio
from src.services import file_processor, question_processor
import os

app = Flask(__name__)

os.environ['API_KEY']="test_key"
API_KEY = os.enivorn.get('API_KEY')

@app.route("/api/v1/hackrx/run", methods=["POST"])
def run_hackrx():
    try:
        # Check Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split("Bearer ")[-1].strip()
        if token != API_KEY:
            return jsonify({"error": "Invalid API key"}), 403

        data = request.get_json()

        # Validate payload
        if not data or "documents" not in data or "questions" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        doc_link = data["documents"]
        questions = data["questions"]

        # Run async functions in Flask
        response = asyncio.run(file_processor.process_document(doc_link))
        print(f"Document processed: {response}")

        answers = []
        for question in questions:
            answer = asyncio.run(question_processor.answer(question))
            answers.append(answer)

        return jsonify({"answers": answers})

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
