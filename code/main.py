from file_to_image import file_to_image
from image_to_text import extract_text
from image_to_csv import extract_csv
from paddleocr import PaddleOCR # type: ignore
import os
import magic # type: ignore
import shutil
from prompt import ask

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

input_dir = os.path.join(parent_path, 'uploads')
images_dir = os.path.join(parent_path, 'converted_images')
csv_dir = os.path.join(parent_path, 'csv_outputs')
os.makedirs(images_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

ocr = PaddleOCR(lang='fr')

requests = 'totals hors tva'

def is_image(file_path):
    try:
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path) in ['image/jpeg', 'image/png']
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')
        return False

def get_images_paths():
    images_paths = []
    for d in os.listdir(images_dir):
        d_path = os.path.join(images_dir, d)
        if os.path.isfile(d_path):
            images_paths.append(d_path)
        else:
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                if os.path.isfile(f_path):
                    images_paths.append(f_path)
    return images_paths

def delete_temp_files():
    # List temp paths
    paths_to_delete = []
    paths_to_delete.append(os.path.join(parent_path, 'code/__pycache__'))
    for i in os.listdir(input_dir):
        paths_to_delete.append(os.path.join(input_dir, i))
    for i in os.listdir(images_dir):
        paths_to_delete.append(os.path.join(images_dir, i))
    delete_csv_outputs = False   # to be deleted later
    if delete_csv_outputs:
        for i in os.listdir(csv_dir):
            paths_to_delete.append(os.path.join(csv_dir, i))
    # Delete temp paths
    for path in paths_to_delete:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

def main():
    # Convert documents to images
    file_to_image(input_dir)
    
    # Get paths of converted images
    images_paths = get_images_paths()
    
    for image_path in images_paths:
        if is_image(image_path):
            # Perform OCR and extract data
            paddle_output = ocr.ocr(image_path)[0]
            text = extract_text(paddle_output)  # Call the function to extract text
            csv = extract_csv(image_path, paddle_output)  # Convert to CSV
            
            # preview OCR outputs
            print(text)
            print('\n')
            print(csv)
            print('\n\n\n\n')
            
            # Ask the LLM about the extracted data
            # answer = ask(requests, text, csv)
            # print(answer)
    delete_temp_files()

if __name__ == '__main__':
    main()