from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

UPLOAD_FOLDER = "C:\\Users\\koush\\OneDrive\\Pictures\\Desktop\\Flask Tutorial\\uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index4.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if "images[]" not in request.files:
            return redirect(url_for("home"))

        uploaded_files = request.files.getlist("images[]")

        if not any(uploaded_files):
            return redirect(url_for("home"))
        
        total_text = []

        for uploaded_file in uploaded_files:
            if uploaded_file.filename == "":
                continue

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            

            try:
                Image.open(file_path).verify()

                text = pytesseract.image_to_string(Image.open(file_path))

                total_text.append(text)

            except Exception as e:
                return f"Error processing image {uploaded_file.filename}: {e}"
            
        return render_template("info.html", filename=uploaded_file.filename, content=total_text)

    return redirect(url_for("home"))

# if __name__ == "__main__":
#     app.run(debug=True)
