import re
from bs4 import BeautifulSoup


def cleanText(text):
    """replace ( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+ with space"""
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+", ' ', text).strip()
    return text
