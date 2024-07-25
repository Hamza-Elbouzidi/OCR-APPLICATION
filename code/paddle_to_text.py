def extract_phrases(paddle_output):
    try:
        # Sorting paddle data
        boxes = [line[0] for line in paddle_output]
        texts = [line[1][0] for line in paddle_output]

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
        print(f"Error extracting phrases from image: {e}")
        return []

def extract_text(paddle_output):
    try:
        phrases = extract_phrases(paddle_output)
        text_only = ' '.join([phrase for phrase in phrases])
        return text_only
    
    except Exception as e:
        print(f"Error executing the program: {e}")

def main(): #to be deleted
    ocr = PaddleOCR(lang='fr')
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
       paddle_output = ocr.ocr(image_path)[0]
       print(extract_text(paddle_output))

if __name__ == '__main__': #to be deleted
    import os
    from paddleocr import PaddleOCR # type: ignore
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(parent_path, 'converted_images')
    main()