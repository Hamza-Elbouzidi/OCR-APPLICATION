from file_to_image import file_to_image
from image_to_text import ocr_text
from image_to_csv import ocr_csv
from paddleocr import PaddleOCR
import os
import magic
from prompt import ask

input_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\documents'
images_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\images'
ocr = PaddleOCR(lang='fr')

#requests = 'numero de facture, \ntotals, \nnoms des produits et leurs quantite, \nconditions de paiement, \nadresses, '
requests = 'les noms des clients'


def is_image(file_path):
    try:
        mime = magic.Magic(mime=True)
        if mime.from_file(file_path) == 'image/jpeg' or mime.from_file(file_path) == 'image/png':
            return True
        else:
            return False
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')

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
    file_to_image(input_dir)
    images_paths = get_images_paths()
    for image_path in images_paths:
        if is_image(image_path):
            paddle_output = ocr.ocr(image_path)[0]
            text = ocr_text(paddle_output)
            csv = ocr_csv(image_path, paddle_output)
            print(text)
            print('\n')
            print(csv)
            print('\n\n\n\n')
            os.remove(image_path)
            answer = ask(requests, text, csv)
            print(answer)



if __name__ == '__main__':
    main()