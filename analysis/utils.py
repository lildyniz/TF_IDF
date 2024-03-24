import re
import textract


def get_text_content(file):
    text = textract.process(file.file.path, encoding='ascii')
    text = text.decode()
    return re.sub(r'[^\w\s]', ' ', text.lower())