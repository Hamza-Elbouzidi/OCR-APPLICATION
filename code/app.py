from flask import Flask, request, jsonify, render_template, redirect, url_for, request
import os
import shutil
import magic
from file_to_image import file_to_image
from paddle_to_text import extract_text
from paddle_to_csv import extract_csv
from paddleocr import PaddleOCR
from prompt import ask
import json

app = Flask(__name__)

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

uploads_dir = os.path.join(parent_path, 'uploads')
converted_images_dir = os.path.join(parent_path, 'converted_images')
json_files_dir = os.path.join(parent_path, 'json_outputs')

os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(converted_images_dir, exist_ok=True)
os.makedirs(json_files_dir, exist_ok=True)

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

def save_json_file(text, image_path):
    json_name = f'{os.path.splitext(os.path.basename(image_path))[0]}'
    output_file_name = f"{json_name}.json"
    index = 1
    output_file_path = os.path.join(json_files_dir, output_file_name)
    while os.path.exists(output_file_path):
        output_file_name = f"{json_name}_{index}.json"
        output_file_path = os.path.join(json_files_dir, output_file_name)
        index += 1   

    start_index = text.find('{')
    end_index = text.rfind('}') + 1

    if start_index != -1 and end_index != -1:
        json_content = text[start_index:end_index]
        try:
            data = json.loads(json_content)
            with open(output_file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return output_file_path
        except json.JSONDecodeError:
            return {}
    return {}

def load_json_data():
    json_data = {}
    for filename in os.listdir(json_files_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(json_files_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                file_data = json.load(file)
                json_data[filename] = file_data
    return json_data

def delete_temp_files():
    paths_to_delete = []
    paths_to_delete.append(os.path.join(parent_path, 'code/__pycache__'))
    for i in os.listdir(uploads_dir):
        paths_to_delete.append(os.path.join(uploads_dir, i))
    for i in os.listdir(converted_images_dir):
        paths_to_delete.append(os.path.join(converted_images_dir, i))
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
    if 'files' not in request.files or 'cardData' not in request.form:
        print('File or cardData missing in request')
        return jsonify({'error': 'No files or card data provided'}), 400

    files = request.files.getlist('files')  # Get the list of files
    card_data = request.form['cardData']

    if not files:
        return jsonify({'error': 'No files provided'}), 400

    print(f'Received card data: {card_data}')

    for file in files:
        print(f'Received file: {file.filename}')
        # Save the uploaded file
        file_path = os.path.join(uploads_dir, file.filename)
        file.save(file_path)

        # Convert documents to images
    file_to_image(uploads_dir, converted_images_dir)

    # Get paths of converted images
    images_paths = get_images_paths()
    global json_paths
    json_paths = []
    for image_path in images_paths:
        if is_image(image_path):
            # Perform OCR and extract data
            paddle_output = ocr.ocr(image_path)[0]
            text = extract_text(paddle_output)
            csv = extract_csv(paddle_output, image_path)

            # Ask the LLM about the extracted data
            # answer = ask(card_data, text, csv)
            # print(answer)
            json_paths.append(save_json_file(answer, image_path))
    delete_temp_files()
    return redirect(url_for('preview'))

@app.route('/preview')
def preview():
    json_data = load_json_data()  # Load data for preview route
    return render_template('preview.html', json_data=json_data)

@app.route('/edit')
def edit():
    json_data = load_json_data()  # Load data for edit route
    return render_template('edit.html', json_data=json_data)

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    for filename, content in data.items():
        filepath = os.path.join(json_files_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
    return jsonify({"message": "Data saved successfully!"})

if __name__ == '__main__':
    # json_path = r'c:\Users\pc\Documents\code\1\OCR-APPLICATION\json_outputs\test.json'
    answer = """
    I will extract the requested information with precision and accuracy. Here are the results in JSON format:

    ```
    {
    "invoice_id": "INV2024-0001",
    "client": {
        "name": "Alice Martin",
        "company": "Tech Solutions",
        "contact": {
        "email": "alice.martin@techsolutions.com",
        "phone": "+33 1 98 76 54 32"
        },
        "address": "789 Business Rd., Tech City"
    },
    "date": "2024-07-26",
    "due_date": "2024-08-09",
    "items": [
        {
        "description": "Software Development",
        "quantity": 50,
        "unit_price": "100 €",
        "total": "5 000 €"
        },
        {
        "description": "UI/UX Design",
        "quantity": 20,
        "unit_price": "80 €",
        "total": "1 600 €"
        },
        {
        "description": "Project Management",
        "quantity": 15,
        "unit_price": "120 €",
        "total": "1 800 €"
        }
    ],
    "subtotal": "8 400 €",
    "tax": "1 680 €",
    "total_due": "10 080 €",
    "payment_terms": "Payment due within 14 days of invoice date.",
    "notes": "Thank you for your business. Please contact us if you have any questions about this invoice.",
    "attachments": [
        {
        "type": "pdf",
        "url": "https://example.com/invoice2024-0001.pdf"
        },
        {
        "type": "image",
        "url": "https://example.com/receipt2024-0001.png"
        }
    ]
    }
    ```

    I have carefully extracted the requested information without modifying or adding any values. I have only extracted the exact information specified in the provided text and CSV files, and presented it in a concise JSON format.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)