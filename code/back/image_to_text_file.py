import os
from paddleocr import PaddleOCR
import magic

base_output_dir = r'C:\Users\pc\Documents\code\OCR with RAG BACK\outputs\texts'
input_dir = r'C:\Users\pc\Documents\code\OCR with RAG BACK\images'

def is_image(file_path):
    try:
        mime = magic.Magic(mime=True)
        if mime.from_file(file_path) == 'image/jpeg' or mime.from_file(file_path) == 'image/png':
            return True
        else:
            return False
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')

def extract_phrases(image_path):
    try:
        ocr = PaddleOCR(lang='fr')
        output = ocr.ocr(image_path)[0]

        # Sorting paddle output data
        boxes = [line[0] for line in output]
        texts = [line[1][0] for line in output]

        # Grouping text in phrases
        phrases = []
        current_phrase = []
        for i in range(len(texts)):
            word = texts[i]
            x = int(boxes[i][0][0])
            y = int(boxes[i][0][1])
            width = int(boxes[i][2][0] - boxes[i][0][0])
            height = int(boxes[i][2][1] - boxes[i][0][1])

            if current_phrase and (y - current_phrase[-1][2] > height):
                phrase_text = ' '.join([w[0] for w in current_phrase])
                phrases.append(phrase_text + '\n')
                current_phrase = []

            current_phrase.append((word, x, y, width, height))

        # Adding the last phrase if it exists
        if current_phrase:
            phrase_text = ' '.join([w[0] for w in current_phrase])
            phrases.append(phrase_text + '\n')        
        return phrases
    except Exception as e:
        print(f"Error extracting phrases from image '{image_path}': {e}")
        return []
    
def save_text_to_file(text, input_file):
    try:
        if not text:
            raise ValueError("No text to save.")

        file_name, _ = os.path.splitext(os.path.basename(input_file))
        output_file_name = f"paddle_{file_name}.txt"
        parent_dir_name = os.path.basename(os.path.dirname(input_file))

        if os.path.dirname(input_file) == input_dir:
            output_dir = base_output_dir
        else:
            output_dir = os.path.join(base_output_dir, parent_dir_name)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
        
        index = 1
        output_file_path = os.path.join(output_dir, output_file_name)
        while os.path.exists(output_file_path):
            output_file_name = f"paddle_{file_name}_{index}.txt"
            output_file_path = os.path.join(output_dir, output_file_name)
            index += 1
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        print(f"Extracted text saved to file: {output_dir}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

def extract_text(image_path):
    try:
        phrases = extract_phrases(image_path)
        print("\nExtracted phrases from the image:")
        
        text_only = ' '.join([phrase for phrase in phrases])
        save_text_to_file(text_only, image_path)
    except Exception as e:
        print(f"Error executing the program: {e}")

def ocr_text():
    #extract_text(input_dir)
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
