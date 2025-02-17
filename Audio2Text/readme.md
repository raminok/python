# Audio to Text Transcription API
**Author: Ramin Orak - Feb 2025**

A Flask-based web application that allows users to upload an audio file and transcribe it into text using OpenAI's Whisper model.

## Features
- Upload an audio file (MP3, WAV, etc.)
- Convert audio to WAV format (16kHz, mono) for better accuracy
- Transcribe speech to text using Whisper
- Display extracted text on the web page

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/audiototext.git
cd audiototext
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Install FFmpeg (Required for audio processing)
- **Windows (Using Chocolatey):**
  ```sh
  choco install ffmpeg
  ```
- **Windows (Using Scoop):**
  ```sh
  scoop install ffmpeg
  ```
- **Linux/macOS:**
  ```sh
  sudo apt-get install ffmpeg  # Ubuntu/Debian
  brew install ffmpeg  # macOS (Homebrew)
  ```

## Usage
### 1. Run the Flask Server
```sh
python server.py
```
By default, the application runs on `http://127.0.0.1:5000/`.

### 2. Open in Browser
Visit `http://127.0.0.1:5000/` and upload an audio file for transcription.

## API Endpoints
- `GET /` - Renders the file upload page.
- `POST /` - Processes the uploaded file and returns transcribed text.

## Project Structure
```
📂 audiototext
├── 📂 uploads             # Directory for storing uploaded files
├── server.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Frontend UI
├── README.md             # Documentation (This file)
```

## Troubleshooting
If you encounter the error:
```sh
TypeError: argument of type 'NoneType' is not iterable
```
Try reinstalling dependencies:
```sh
pip uninstall whisper openai-whisper -y
pip install openai-whisper torch torchaudio ffmpeg
```
Ensure `ffmpeg` is installed and available in the system `PATH`.

## License
This project is licensed under the MIT License. Feel free to modify and distribute.

