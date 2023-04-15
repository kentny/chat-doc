from flask import Flask, request
from flask_cors import CORS

from backend.ingest import ingest, generate_answer

app = Flask(__name__)
CORS(app)

@app.route("/api/bots", methods=["POST"])
def upload_pdf():
    if "pdfFile" not in request.files:
        return {"error": "PDF file not found"}, 400
    
    pdf_file = request.files["pdfFile"]

    if not pdf_file.filename.endswith(".pdf"):
        return {"error": "Invalid file type"}, 400
    
    pdf_file.save('./uploads/' + pdf_file.filename)

    ingest('./uploads/' + pdf_file.filename)

    return {"message": "PDF file uploaded successfully"}, 200


@app.route("/api/bots", methods=["GET"])
def ask_question():
    question = request.args.get('question')
    print(question)
    answer = generate_answer(question)
    return {"answer": answer}, 200


if __name__ == "__main__":
    app.run()
