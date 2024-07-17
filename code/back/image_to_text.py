input_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\images'

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

def ocr_text(paddle_output):
    try:
        phrases = extract_phrases(paddle_output)
        text_only = ' '.join([phrase for phrase in phrases])
        return text_only
    
    except Exception as e:
        print(f"Error executing the program: {e}")