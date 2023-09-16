from pypdf import PdfReader

from ai_text_demo.utils import relative_path_from_file

PDF_FILE_PATH = relative_path_from_file(__file__, '../ingesting_pdf/data/paper01.pdf')

reader = PdfReader(PDF_FILE_PATH)
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

print(f"Number of pages: {number_of_pages}")
print(f"Text on 1st page: {text}")
print(f"Text on 3rd page: {reader.pages[2].extract_text()}")
