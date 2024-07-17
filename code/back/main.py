from file_to_image import file_to_image
from image_to_text import extract_text
from image_to_csv import ocr_csv
from paddleocr import PaddleOCR
import os
import magic
from prompt import ask

input_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\uploads'
images_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\converted_images'
ocr = PaddleOCR(lang='fr')

requests = 'les noms des clients'

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

def main():
    # Convert documents to images
    file_to_image(input_dir)
    
    # Get paths of converted images
    images_paths = get_images_paths()
    
    for image_path in images_paths:
        if is_image(image_path):
            # Perform OCR and extract text
            paddle_output = ocr.ocr(image_path)[0]
            text = extract_text(image_path)  # Call the function to extract text
            csv = ocr_csv(image_path, paddle_output)  # Convert to CSV
            
            print(text)
            print('\n')
            print(csv)
            print('\n\n\n\n')
            
            # Remove the processed image
            #os.remove(image_path)
            
            # Ask the LLM about the extracted data
            answer = ask(requests, text, csv)
            print(answer)

if __name__ == '__main__':
    main()
