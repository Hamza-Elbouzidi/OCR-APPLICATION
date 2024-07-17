import os
from paddleocr import PaddleOCR
import magic

base_output_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\outputs\converted_txt'
input_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\converted_images'

def is_image(file_path):
    try:
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path) in ['image/jpeg', 'image/png']
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')
        return False

def extract_phrases(ocr_output):
    try:
        boxes = [line[0] for line in ocr_output]
        texts = [line[1][0] for line in ocr_output]

        phrases = []
        current_phrase = []
        for i in range(len(texts)):
            word = texts[i]
            x = int(boxes[i][0][0])
            y = int(boxes[i][0][1])
            width = int(boxes[i][2][0] - boxes[i][0][0])
            height = int(boxes[i][2][1] - boxes[i][0][1])

            if current_phrase and (y - current_phrase[-1][2] > height):
                phrases.append(' '.join([w[0] for w in current_phrase]) + '\n')
                current_phrase = []

            current_phrase.append((word, x, y, width, height))

        if current_phrase:
            phrases.append(' '.join([w[0] for w in current_phrase]) + '\n')
        return phrases
    
    except Exception as e:
        print(f"Error extracting phrases: {e}")
        return []

def save_text_to_file(text, input_file):
    try:
        if not text:
            raise ValueError("No text to save.")

        file_name, _ = os.path.splitext(os.path.basename(input_file))
        output_file_name = f"{file_name}.txt"  # Changed here
        parent_dir_name = os.path.basename(os.path.dirname(input_file))

        output_dir = base_output_dir if os.path.dirname(input_file) == input_dir else os.path.join(base_output_dir, parent_dir_name)
        os.makedirs(output_dir, exist_ok=True)

        index = 1
        output_file_path = os.path.join(output_dir, output_file_name)
        while os.path.exists(output_file_path):
            output_file_name = f"{file_name}_{index}.txt"  # Changed here
            output_file_path = os.path.join(output_dir, output_file_name)
            index += 1
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        print(f"Extracted text saved to file: {output_file_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

def extract_text(image_path):
    try:
        ocr = PaddleOCR(lang='fr')
        ocr_output = ocr.ocr(image_path)[0]
        phrases = extract_phrases(ocr_output)

        print("\nExtracted phrases from the image:")
        text_only = ' '.join(phrases)
        save_text_to_file(text_only, image_path)
        return text_only
    except Exception as e:
        print(f"Error extracting text from image '{image_path}': {e}")

def ocr_text():
    images_paths = []
    for d in os.listdir(input_dir):
        d_path = os.path.join(input_dir, d)
        if os.path.isfile(d_path):
            images_paths.append(d_path)
        else:
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                if os.path.isfile(f_path):
                    images_paths.append(f_path)

    for image_path in images_paths:
        if is_image(image_path):
            extract_text(image_path)

if __name__ == "__main__":
    ocr_text()
