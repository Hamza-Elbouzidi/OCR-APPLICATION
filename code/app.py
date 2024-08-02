from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import shutil
import magic
from file_to_image import file_to_image
from paddle_to_text import extract_text
from paddle_to_csv import extract_csv
from paddleocr import PaddleOCR
from prompt import ask
import json
from db.db import db, Card

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

uploads_dir = os.path.join(parent_path, 'uploads')
converted_images_dir = os.path.join(parent_path, 'converted_images')
json_files_dir = os.path.join(parent_path, 'json_outputs')
db_path = os.path.join(parent_path, 'code', 'instance', 'cards.db')

os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(converted_images_dir, exist_ok=True)
os.makedirs(json_files_dir, exist_ok=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)

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
        if os.path.isfile(d_path) and is_image(d_path):
                images_paths.append(d_path)
        else:
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                if os.path.isfile(f_path) and is_image(f_path):
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
    cards = Card.query.all()
    app.logger.debug('Cards retrieved: %s', cards)
    for card in cards:
        card.data_ids = json.loads(card.data_ids)
    return render_template('index.html', cards=cards)

@app.route('/admin/cards/add', methods=['POST'])
def add_card():
    title = request.form['title']
    data_ids = json.dumps(request.form.getlist('data_ids'))  # Handle multiple data fields
    new_card = Card(title=title, data_ids=data_ids)
    db.session.add(new_card)
    db.session.commit()
    return redirect(url_for('admin_cards'))

@app.route('/admin/cards/update/<int:card_id>', methods=['POST'])
def update_card(card_id):
    card = Card.query.get(card_id)
    card.title = request.form['title']
    card.data_ids = json.dumps(request.form.getlist('data_ids'))
    db.session.commit()
    return redirect(url_for('admin_cards'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files or 'cardData' not in request.form:
        print('File or cardData missing in request')
        return jsonify({'error': 'No files or card data provided'}), 400

    files = request.files.getlist('files')  # Get the list of files
    card_data_raw = request.form['cardData']
    print(f"Raw card data: {card_data_raw}")  # Print the raw card data for debugging
    
    try:
        card_data = json.loads(card_data_raw)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return jsonify({'error': 'Invalid card data format'}), 400

    if not files:
        return jsonify({'error': 'No files provided'}), 400

    print(f'Received card data: {card_data}')

    for file in files:
        print(f'Received file: {file.filename}')
        # Save the uploaded file
        file_name = os.path.splitext(file.filename)[0]
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(uploads_dir, file.filename)
        i = 1
        if os.path.exists(file_path):
            file_path = os.path.join(uploads_dir, f'{file_name}_{i}{file_ext}')
            i += 1
        file.save(file_path)

    # Convert documents to images
    file_to_image(uploads_dir, converted_images_dir)

    images_paths = get_images_paths()
    for image_path in images_paths:
        paddle_output = ocr.ocr(image_path)[0]
        text = extract_text(paddle_output)
        csv = extract_csv(paddle_output, image_path)

        answer = ask(card_data, text, csv)
        print(answer)
        save_json_file(answer, image_path)

    delete_temp_files()

    # Return a success message
    return jsonify({'message': 'Files processed and uploaded successfully!'}), 200


@app.route('/preview')
def preview():
    json_data = load_json_data()  # Load data for preview route
    return render_template('preview.html', json_data=json_data)

@app.route('/preview/edit')
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
    
    app.run(host='0.0.0.0', port=5000, debug=True)