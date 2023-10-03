# !pip install pdfminer.six
# !pip install language-tool-python

from pdfminer.high_level import extract_text
import language_tool_python
from pdf2image import convert_from_path
import pytesseract
import sys

def check_spelling_grammar(text):
    tool = language_tool_python.LanguageTool('en-UK')
    matches = tool.check(text)
    return matches

path = sys.argv[1]

text = extract_text(path)

if text == '\x0c':
    images = convert_from_path(path,500,poppler_path='poppler-23.08.0/Library/bin')

    pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
    text = ''
    for i, image in enumerate(images):
        text = text + pytesseract.image_to_string(image)
        
errors = check_spelling_grammar(text)

c = 0

for error in errors:
    if error.message != 'Add a space between sentences.' and error.message != 'Possible typo: you repeated a whitespace':
        c+=1
        print(f"Possible Error at line {error.context}:\n {error.message}")
        print(f"Suggested corrections for '{error.sentence}': {error.replacements}\n")
    
print(f"{c} mistakes found!")