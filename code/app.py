from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import shutil
import magic
import json
from file_to_image import file_to_image
from paddle_to_text import extract_text
from paddle_to_csv import extract_csv
from paddleocr import PaddleOCR
from prompt import ask
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    return render_template('Admin_carte_page.html', cards=cards)

@app.route('/admin/cards/add', methods=['POST'])
def add_card():
    title = request.form.get('title', '').strip()
    json_structure = request.form.get('json_structure', '').strip()
    description = request.form.get('description', '').strip()
    
    if not title or not json_structure:
        return jsonify({'error': 'Title and JSON structure are required'}), 400

    new_card = Card(title=title, json_structure=json_structure, description=description)
    db.session.add(new_card)
    db.session.commit()
    return redirect(url_for('admin_carte_page'))

@app.route('/admin/cards/update/<int:card_id>', methods=['POST'])
def update_card(card_id):
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404

    title = request.form.get('title', '').strip()
    json_structure = request.form.get('json_structure', '').strip()
    description = request.form.get('description', '').strip()

    if not title or not json_structure:
        return jsonify({'error': 'Title and JSON structure are required'}), 400

    card.title = title
    card.json_structure = json_structure
    card.description = description
    db.session.commit()
    return redirect(url_for('admin_carte_page'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files or 'cardData' not in request.form:
        print('File or cardData missing in request')
        return jsonify({'error': 'No files or card data provided'}), 400

    files = request.files.getlist('files')
    card_data_raw = request.form['cardData']

    try:
        card_data = json.loads(card_data_raw)
        if not isinstance(card_data, dict):
            raise ValueError('Invalid card data format')

        json_structure = card_data.get('json_structure', '{}')
        description = card_data.get('description', '')
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Invalid card data format'}), 400

    if not files:
        return jsonify({'error': 'No files provided'}), 400

    for file in files:
        file_name = os.path.splitext(file.filename)[0]
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(uploads_dir, file.filename)
        i = 1
        while os.path.exists(file_path):
            file_path = os.path.join(uploads_dir, f'{file_name}_{i}{file_ext}')
            i += 1
        file.save(file_path)

    file_to_image(uploads_dir, converted_images_dir)

    images_paths = get_images_paths()
    for image_path in images_paths:
        paddle_output = ocr.ocr(image_path)[0]
        text = extract_text(paddle_output)
        csv = extract_csv(paddle_output, image_path)

        answer = ask(json_structure, description, text, csv)
        save_json_file(answer, image_path)

    delete_temp_files()

    return jsonify({'message': 'Files processed and uploaded successfully!'}), 200

@app.route('/preview')
def preview():
    json_data = load_json_data()
    return render_template('preview.html', json_data=json_data)

@app.route('/Admin_login')
def Admin_login():
    return render_template('Admin_login.html')

@app.route('/Admin_créer_carte')
def Admin_créer_carte():
    return render_template('Admin_créer_carte.html')

@app.route('/Admin_carte_page')
def admin_carte_page():
    cards = Card.query.all()
    return render_template('Admin_carte_page.html', cards=cards)

@app.route('/preview/edit')
def edit():
    json_data = load_json_data()
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
