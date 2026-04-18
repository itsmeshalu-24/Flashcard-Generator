from flask import Flask, render_template, request, send_file
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph

app = Flask(__name__)

# 🔹 Create flashcards
def create_cards(text):
    sentences = text.split(".")
    cards = []

    for i in range(min(5, len(sentences))):
        sentence = sentences[i].strip()

        if len(sentence) > 20:
            question = f"What is: {sentence[:50]}?"
            answer = sentence

            cards.append(f"Q: {question}\nA: {answer}")

    return "\n\n".join(cards)


# 🔹 Save flashcards as PDF
def save_pdf(cards):
    pdf = SimpleDocTemplate("flashcards.pdf", pagesize=letter)
    content = []

    for line in cards.split("\n"):
        content.append(Paragraph(line))

    pdf.build(content)


# 🔹 Main route
@app.route("/", methods=["GET", "POST"])
def home():
    cards = ""

    if request.method == "POST":
        pdf_file = request.files["pdf"]

        reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        cards = create_cards(text[:3000])
        save_pdf(cards)

    return render_template("index.html", cards=cards)


# 🔹 Download route
@app.route("/download")
def download():
    return send_file("flashcards.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)