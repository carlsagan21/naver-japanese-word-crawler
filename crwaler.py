import requests
from bs4 import BeautifulSoup


def _unparan_entry_name(entry_name):
    if "(" in entry_name:
        entry_name = entry_name.replace("(", ",", 1)[:-1]
    return entry_name


def get_word(url):
    word_response = requests.get(url)
    word_soup = BeautifulSoup(word_response.text, "html.parser")

    entry_name = word_soup.find(
        id="reviewWord").attrs["data-entryname"]

    entry_name = _unparan_entry_name(entry_name)

    meaning_candidate = list(word_soup.find(class_="spot_area").children)[5]
    meaning = meaning_candidate.text if meaning_candidate.name == "p" else ""

    print("{}\t{}".format(entry_name, meaning))

    return entry_name, meaning


def get_word_url_list(url):
    page_response = requests.get(url)
    page_soup = BeautifulSoup(page_response.text, "html.parser")

    return [
        word_entry.a.attrs["href"] for index, word_entry
        in enumerate(page_soup.find(class_="lst"))
        if index % 2 == 1
    ]
