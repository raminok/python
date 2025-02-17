from flask import Flask, request, render_template
import os
import whisper
import io
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# بارگذاری مدل Whisper
model = whisper.load_model("base")

@app.route('/', methods=['GET', 'POST'])
def upload_audio():
    text = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        # تبدیل فایل صوتی به فرمت مناسب
        audio = AudioSegment.from_file(file)
        audio = audio.set_frame_rate(16000).set_channels(1)  # تنظیمات صوتی برای دقت بالاتر
        audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "converted.wav")
        audio.export(audio_file_path, format="wav")
        
        # پردازش فایل صوتی با Whisper
        result = model.transcribe(audio_file_path)
        text = result["text"]
    
    return render_template('index.html', extracted_text=text)

if __name__ == '__main__':
    app.run(debug=True)
