import os
import magic
from pdf2image import convert_from_path
import shutil
import logging
from PIL import Image
from docx2pdf import convert as docx_to_pdf  # This will be used for DOCX to PDF conversion

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_type(file_path):
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        return file_type
    except Exception as e:
        logging.error(f'Error getting {file_path} file type: {e}')
        return None

def convert_pdf_to_images(pdf_path, output_dir):
    try:
        pages = convert_from_path(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for i, page in enumerate(pages):
            output_path = os.path.join(output_dir, f'{pdf_name}_page_{i + 1}.png')
            page.save(output_path, 'PNG')
    except Exception as e:
        logging.error(f'Error converting {pdf_path} to image: {e}')

def convert_docx_to_images(docx_path, output_dir):
    docx_name = os.path.splitext(os.path.basename(docx_path))[0]
    pdf_path = os.path.join(output_dir, f'{docx_name}.pdf')
    try:
        # Convert DOCX to PDF using docx2pdf
        docx_to_pdf(docx_path, pdf_path)
        convert_pdf_to_images(pdf_path, output_dir)
    except Exception as e:
        logging.error(f'Conversion failed: {e}')
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

def stack_images(dir, name):
    image_files = [f for f in os.listdir(dir) if f.endswith(('png', 'jpg', 'jpeg'))]
    images = [Image.open(os.path.join(dir, img)) for img in image_files]

    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    stacked_image = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for img in images:
        stacked_image.paste(img, (0, y_offset))
        y_offset += img.height

    stacked_image.save(os.path.join(dir, f'{name}.png'))
    for i in image_files:
        os.remove(os.path.join(dir, i))

def process_file(file_path, base_output_dir):
    file_name = os.path.basename(file_path)
    output_dir = os.path.join(base_output_dir, file_name)
    os.makedirs(output_dir, exist_ok=True)
    
    file_type = get_file_type(file_path)
    if file_type in ['image/png', 'image/jpeg']:
        shutil.copy(file_path, output_dir)
    elif file_type == 'application/pdf':
        convert_pdf_to_images(file_path, output_dir)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        convert_docx_to_images(file_path, output_dir)
    else:
        os.rmdir(output_dir)
        logging.error(f'Unsupported file type: {file_type} for file {file_path}')

    stack_images(output_dir, os.path.splitext(file_name)[0])

def file_to_image(input_dir, base_output_dir):
    file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    for file_path in file_paths:
        process_file(file_path, base_output_dir)

if __name__ == '__main__':
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    uploads_dir = os.path.join(parent_path, 'uploads')
    converted_images_dir = os.path.join(parent_path, 'converted_images')
    file_to_image(uploads_dir, converted_images_dir)
