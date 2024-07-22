import os
import magic
from pdf2image import convert_from_path
import comtypes.client
import shutil

base_output_dir = r'C:\Users\pc\Documents\code\OCR-APPLICATION\converted_images'

def get_file_type(file_path):
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        return file_type
    except Exception as e:
        print(f'Error getting {file_path} file type: {e}')


def convert_pdf_to_images(pdf_path, output_dir):
    try:
        pages = convert_from_path(pdf_path)
        for i, page in enumerate(pages):
            output_path = os.path.join(output_dir, f'page_{i + 1}.png')
            page.save(output_path, 'PNG')
    except Exception as e:
        print(f'Error converting {pdf_path} to image: {e}')

def convert_docx_to_pdf(docx_path, pdf_path):
    try:
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(docx_path)
        doc.SaveAs(pdf_path, FileFormat=17)
        doc.Close()
        word.Quit()
    except Exception as e:
        print(f'Error converting {docx_path} to PDF: {e}')

def convert_docx_to_images(docx_path, output_dir):
    pdf_path = os.path.join(output_dir, 'temp.pdf')
    convert_docx_to_pdf(docx_path, pdf_path)
    convert_pdf_to_images(pdf_path, output_dir)
    os.remove(pdf_path)

def process_file(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
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
        os.removedirs(output_dir)
        print(f'Unsupported file type: {file_type} for file {file_path}')

def file_to_image(input_dir):
    file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    for file_path in file_paths:
        process_file(file_path)

if __name__ == "__main__":
    input_dir = r'C:\Users\pc\Documents\code\OCR-APPLICATION\uploads'
    file_to_image(input_dir)