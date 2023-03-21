import unicodedata
import re

import re

def checkIsRussian(string):
    pattern = re.compile('[\u0400-\u04FF]+')
    russian_string = pattern.findall(string)
    return bool(russian_string)

def checkIsEnglish(string):
    pattern = re.compile('[^a-zA-Z]')
    english_string = pattern.sub('', string)
    return bool(english_string)