# Extract Text from Images using Flask and Tesseract OCR

**Author: Ramin Orak - Feb 2025**

This is a simple web application that allows users to upload an image and extract text from it using **Tesseract OCR**. The extracted text is displayed alongside the uploaded image for easy comparison.

## 🚀 Features
- Upload an image and extract text using OCR.
- Preview the uploaded image.
- Copy the extracted text to the clipboard.
- No need to store images on disk.

## 📦 Requirements
Ensure you have the following dependencies installed before running the project:

```bash
pip install flask pytesseract pillow
```
Additionally, install **Tesseract OCR** on your system:

### 🔹 Windows Installation
Download and install **Tesseract OCR** from:
[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

After installation, update the script to include the path:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

### 🔹 Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr -y
```

### 🔹 macOS
```bash
brew install tesseract
```

## 🔧 How to Run
Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

Run the Flask application:
```bash
python server.py
```

Open your browser and visit:
```
http://127.0.0.1:5000/
```

## 📜 Project Structure
```
project-folder/
│── server.py              # Main Flask application
│── templates/
│   ├── index.html      # Web interface
│── README.md           # Documentation
```

## 📝 Usage
1. Click **Upload Image for Text Extraction**.
2. Select an image file (JPG, PNG, etc.).
3. Click **Extract Text**.
4. The extracted text will appear alongside the uploaded image.
5. Click **Copy Text** to copy the extracted text.

## ⚡ Example Screenshot
![doc1](https://github.com/user-attachments/assets/e26b71a1-34c5-4609-a4d5-c7fb3503a1e8)

# After upload an Image

![doc2](https://github.com/user-attachments/assets/a020ec50-fb8a-4fb8-835b-cf1bb8e9b883)


## 📜 License
This project is licensed under the **MIT License**.
