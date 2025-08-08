from flask import Flask, request, jsonify
from src.services import file_processor, question_processor

app = Flask(__name__)

@app.route("/api/v1/hackrx/run", methods=["POST"])
def run_hackrx():
    try:
        data = request.get_json()

        # Validate payload
        if not data or "documents" not in data or "questions" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        doc_link = data["documents"]
        questions = data["questions"]

        # Process the document
        response = file_processor.process_document(doc_link)
        print(f"Document processed: {response}")

        answers = []
        for question in questions:
            answer = question_processor.answer(question)
            answers.append(answer)

        return jsonify({"answers": answers})

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
