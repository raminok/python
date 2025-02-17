# Extract Text from Images using Flask and Tesseract OCR

**Author: Ramin Orak**

from flask import Flask, request, render_template
import pytesseract
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# تعیین مسیر Tesseract برای ویندوز
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    text = ""
    image_data = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        # پردازش تصویر بدون ذخیره‌سازی روی دیسک
        image = Image.open(file)
        text = extract_text(image)
        
        # تبدیل تصویر به base64 برای نمایش در صفحه وب
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)
        image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return render_template('index.html', extracted_text=text, image_data=image_data)

def extract_text(image):
    return pytesseract.image_to_string(image, lang='eng+fra')

# ایجاد فایل index.html در پوشه templates
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Extract Text from Image</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
            background-color: #f4f4f4;
        }
        h2 {
            color: #333;
        }
        form {
            margin: 20px auto;
            padding: 20px;
            background: white;
            display: inline-block;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        input[type="file"] {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: #fff;
        }
        button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: #0056b3;
        }
        .output-container {
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            margin-top: 20px;
            gap: 20px;
        }
        .image-preview {
            max-width: 200px;
            max-height: 200px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        textarea {
            width: 1000%;
            max-width: 800px;
            height: 300px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            overflow-x: hidden;
        }
        .copy-btn {
            margin-top: 10px;
            padding: 10px 20px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .copy-btn:hover {
            background: #218838;
        }
    </style>
    <script>
        function copyText() {
            var textArea = document.getElementById("extractedText");
            textArea.select();
            document.execCommand("copy");
            alert("Text copied to clipboard!");
        }
    </script>
</head>
<body>
    <h2>Upload Image for Text Extraction</h2>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*" required>
        <br>
        <button type="submit">Extract Text</button>
    </form>
    
    {% if image_data %}
    <div class="output-container">
        <img src="data:image/png;base64,{{ image_data }}" class="image-preview" alt="Uploaded Image">
        <div>
            <textarea id="extractedText" readonly>{{ extracted_text }}</textarea>
            <br>
            <button class="copy-btn" onclick="copyText()">Copy Text</button>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

# ذخیره فایل HTML در پوشه templates
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

if __name__ == '__main__':
    app.run(debug=True)
