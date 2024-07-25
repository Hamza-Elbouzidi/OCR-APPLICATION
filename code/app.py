from flask import Flask, request, jsonify, render_template
import os
import shutil
import magic
from file_to_image import file_to_image
from paddle_to_text import extract_text
from paddle_to_csv import extract_csv
from paddleocr import PaddleOCR
from prompt import ask

app = Flask(__name__)

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

uploads_dir = os.path.join(parent_path, 'uploads')
converted_images_dir = os.path.join(parent_path, 'converted_images')
csv_files_dir = os.path.join(parent_path, 'csv_outputs')

os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(converted_images_dir, exist_ok=True)
os.makedirs(csv_files_dir, exist_ok=True)

ocr = PaddleOCR(lang='fr')

def is_image(file_path):
    try:
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path) in ['image/jpeg', 'image/png']
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')
        return False

def get_images_paths():
    images_paths = []
    for d in os.listdir(converted_images_dir):
        d_path = os.path.join(converted_images_dir, d)
        if os.path.isfile(d_path):
            images_paths.append(d_path)
        else:
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                if os.path.isfile(f_path):
                    images_paths.append(f_path)
    return images_paths

def delete_temp_files():
    paths_to_delete = []
    paths_to_delete.append(os.path.join(parent_path, 'code/__pycache__'))
    for i in os.listdir(uploads_dir):
        paths_to_delete.append(os.path.join(uploads_dir, i))
    for i in os.listdir(converted_images_dir):
        paths_to_delete.append(os.path.join(converted_images_dir, i))
    delete_csv_outputs = False
    if delete_csv_outputs:
        for i in os.listdir(csv_files_dir):
            paths_to_delete.append(os.path.join(csv_files_dir, i))
    for path in paths_to_delete:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'cardData' not in request.form:
        return jsonify({'error': 'No file or card data provided'}), 400

    file = request.files['file']
    card_data = request.form['cardData']

    # Ensure the uploads directory exists
    os.makedirs(uploads_dir, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)

    # Convert documents to images
    file_to_image(uploads_dir, converted_images_dir)

    # Get paths of converted images
    images_paths = get_images_paths()
    
    answer = None
    for image_path in images_paths:
        if is_image(image_path):
            # Perform OCR and extract data
            paddle_output = ocr.ocr(image_path)[0]
            text = extract_text(paddle_output)
            csv = extract_csv(paddle_output, image_path, csv_files_dir)
            
            # Ask the LLM about the extracted data
            answer = ask(card_data, text, csv)
            print(answer)

    delete_temp_files()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
