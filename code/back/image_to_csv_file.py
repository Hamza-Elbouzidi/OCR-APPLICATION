import cv2
import numpy as np
import pandas as pd 
import tensorflow as tf
from paddleocr import PaddleOCR
import os
import magic

base_output_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\outputs\CSVs'
input_dir = r'D:\Projects\Personal Projects\OCR-APPLICATION\images'

def is_image(file_path):
    try:
        mime = magic.Magic(mime=True)
        if mime.from_file(file_path) == 'image/jpeg' or mime.from_file(file_path) == 'image/png':
            return True
        else:
            return False
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')

def extract_in_array(image_path):
  #extracting all data from table
  ocr = PaddleOCR(lang='fr')
  image = cv2.imread(image_path)
  image_height = image.shape[0]
  image_width = image.shape[1]
  output = ocr.ocr(image_path)[0]

  #sorting paddle output data 
  boxes = [line[0] for line in output]
  texts = [line[1][0] for line in output]
  probabilities = [line[1][1] for line in output]

  #getting table layout with nms
  horiz_boxes = []
  vert_boxes = []

  for box in boxes:
    x_h, x_v = 0,int(box[0][0])
    y_h, y_v = int(box[0][1]),0
    width_h,width_v = image_width, int(box[2][0]-box[0][0])
    height_h,height_v = int(box[2][1]-box[0][1]),image_height

    horiz_boxes.append([x_h,y_h,x_h+width_h,y_h+height_h])
    vert_boxes.append([x_v,y_v,x_v+width_v,y_v+height_v])

  horiz_out = tf.image.non_max_suppression(
      horiz_boxes,
      probabilities,
      max_output_size = 1000,
      iou_threshold=0.1,
      score_threshold=float('-inf'),
      name=None
  )
  horiz_lines = np.sort(np.array(horiz_out))

  vert_out = tf.image.non_max_suppression(
      vert_boxes,
      probabilities,
      max_output_size = 1000,
      iou_threshold=0.1,
      score_threshold=float('-inf'),
      name=None
  )
  vert_lines = np.sort(np.array(vert_out))

  #creating array
  out_array = [["" for i in range(len(vert_lines))] for j in range(len(horiz_lines))]

  #ordering vertical columns
  unordered_boxes = []
  for i in vert_lines:
    unordered_boxes.append(vert_boxes[i][0])

  ordered_boxes = np.argsort(unordered_boxes)

  #filling the array
  def intersection(box_1, box_2):
    return [box_2[0], box_1[1],box_2[2], box_1[3]]

  def iou(box_1, box_2):

    x_1 = max(box_1[0], box_2[0])
    y_1 = max(box_1[1], box_2[1])
    x_2 = min(box_1[2], box_2[2])
    y_2 = min(box_1[3], box_2[3])

    inter = abs(max((x_2 - x_1, 0)) * max((y_2 - y_1), 0))
    if inter == 0:
        return 0
        
    box_1_area = abs((box_1[2] - box_1[0]) * (box_1[3] - box_1[1]))
    box_2_area = abs((box_2[2] - box_2[0]) * (box_2[3] - box_2[1]))
    union = float( box_1_area + box_2_area - inter)

    return inter / union

  for b in range(len(boxes)):
    for i in range(len(horiz_lines)):
      for j in range(len(vert_lines)):
        resultant = intersection(horiz_boxes[horiz_lines[i]], vert_boxes[vert_lines[ordered_boxes[j]]] )
        the_box = [boxes[b][0][0],boxes[b][0][1],boxes[b][2][0],boxes[b][2][1]]
        if(iou(resultant,the_box)>0.1):
          out_array[i][j] = texts[b]
          break

  out_array=np.array(out_array)
  return out_array

def save_to_csv(array, input_file):
      try:
        csv_name = f'{os.path.splitext(os.path.basename(input_file))[0]}'
        output_file_name = f"paddle_{csv_name}.csv"
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
            output_file_name = f"paddle_{csv_name}_{index}.csv"
            output_file_path = os.path.join(output_dir, output_file_name)
            index += 1   

        pd.DataFrame(array).to_csv(output_file_path)
        #print("successful!")
      except Exception as e:
        print(f"Error saving text to file: {e}")

def extract_text(image_path):
    try:
        csv_array = extract_in_array(image_path)
        save_to_csv(csv_array, image_path)
    except Exception as e:
        print(f"Error executing the program: {e}")

def ocr_csv():
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
    ocr_csv()
