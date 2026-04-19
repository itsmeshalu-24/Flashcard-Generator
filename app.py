from flask import Flask, render_template, request, send_file
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph

app = Flask(__name__)

# 🔹 Create flashcards
def create_cards(text):
    sentences = text.split(".")
    cards = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 20:
            question = f"What is: {sentence[:50]}?"
            answer = sentence

            cards.append(f"Q: {question}\nA: {answer}")

        if len(cards) == 5:
            break

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
        pdf_file = request.files.get("pdf")

        # ✅ FIX 1: check file
        if not pdf_file or pdf_file.filename == "":
            return "Please upload a valid PDF"

        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

            # ✅ FIX 2: check empty text
            if not text.strip():
                return "No readable text found in PDF"

            cards = create_cards(text[:3000])
            save_pdf(cards)

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html", cards=cards)


# 🔹 Download route
@app.route("/download")
def download():
    try:
        return send_file("flashcards.pdf", as_attachment=True)
    except:
        return "No PDF generated yet"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
