import re

import requests
from bs4 import BeautifulSoup


def _unparan_entry_name(entry_name):
    if "(" in entry_name:
        entry_name = entry_name.replace("(", ",", 1)[:-1]
    return entry_name


def get_word(url):
    word_response = requests.get(url)
    word_soup = BeautifulSoup(word_response.text, "html.parser")

    entry_name = word_soup.find(id="reviewWord").attrs["data-entryname"]

    entry = word_soup.find(id=re.compile("entryTts_JK*"))
    entry_name = entry.text
    kanji_entry = entry.next_sibling
    kanji_name = ""
    kanji_names = []

    if kanji_entry and kanji_entry.name == "em":
        kanji_name = kanji_entry.text
        kanji_name = kanji_name[1:-1]
        kanji_names = kanji_name.split("·")
        kanji_names = [kanji_name for kanji_name
                       in kanji_names
                       if not re.search('[a-zA-Z]', kanji_name)]

    word = ",".join(kanji_names + [entry_name])

    # entry_name = _unparan_entry_name(entry_name)

    meaning_candidate = list(word_soup.find(class_="spot_area").children)[5]
    meaning = meaning_candidate.text if meaning_candidate.name == "p" else ""

    if not meaning:
        meaning = word_soup.find(class_="lst_txt").text

    if meaning[-1] == ".":
        meaning = meaning[:-1]

    print("{}\t{}".format(word, meaning))

    return word, meaning


def get_word_url_list(url):
    page_response = requests.get(url)
    page_soup = BeautifulSoup(page_response.text, "html.parser")

    return [
        word_entry.a.attrs["href"] for index, word_entry
        in enumerate(page_soup.find(class_="lst").contents)
        if index % 2 == 1
    ]


if __name__ == "__main__":
    get_word("https://ja.dict.naver.com/entry/jk/JK000000031197.nhn")
    # get_word_url_list("https://ja.dict.naver.com/jlpt/level-4/parts-0/p24.nhn")
