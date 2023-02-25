"""
Translation app
"""
import os
import time
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator


# function to translate text
def translate_text(text):
    # avoid to many symbols error
    if len(text) <= 5000:
        translation = GoogleTranslator(source='en', target='hi').translate(text)
        return translation
    else:
        # divide the received text into pieces less than 5000
        pieces = [text[i:i+4999] for i in range(0, len(text), 4999)]
        translations = [GoogleTranslator(source='en', target='hi').translate(piece) for piece in pieces]
        return ''.join(translations)


# function to process a file
def process_file(filename):
    # read in the HTML file
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # find all text elements in the HTML
    text_elements = soup.find_all(string=True)

    # loop through the text elements and translate them
    count = 0
    for elem in text_elements:
        # check if the text is in English
        if elem.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            if elem.strip() != '':
                try:
                    # translate the text
                    translated_text = translate_text(elem)

                    # replace the English text with the translated text
                    elem.replace_with(translated_text)

                    # increment the count of translations
                    count += 1

                    # save the translated text after every 30 translations
                    if count % 30 == 0:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(str(soup))

                        # pause for half a second to avoid rate limiting
                        time.sleep(0.5)

                except Exception as e:
                    # catch any exceptions and print an error message
                    print(f'Error translating text: {e}')

    # write out the updated HTML
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))


# function to process a directory
def process_directory(directory):
    # loop through all files and subdirectories in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # check if the file is an HTML file
            if filename.endswith('.html') or filename.endswith('.htm'):
                # process the file
                filepath = os.path.join(root, filename)
                process_file(filepath)


# process the current directory and its subdirectories
process_directory('.')
