import requests
from bs4 import BeautifulSoup
import urllib.parse

level = 5
parts = 0  # every
pages = 1


def get_word(url):
    word_response = requests.get(url)
    word_soup = BeautifulSoup(word_response.text, "html.parser")

    entryname = word_soup.find(id="reviewWord").attrs["data-entryname"]
    meaning_candidate = list(word_soup.find(
        class_="spot_area").children)[5]
    meaning = meaning_candidate.text if meaning_candidate.name == "p" else ""

    print("{}\t{}".format(entryname, meaning))

    return entryname, meaning


if __name__ == "__main__":
    with open("jlpt-level-{}-parts-{}.txt".format(level, parts), "w") as f:
        for page in range(1, pages + 1):
            base_url = "https://ja.dict.naver.com"
            list_page_url = "/jlpt/level-{}/parts-{}/p{}.nhn".format(
                level, parts, page)

            page_response = requests.get(
                urllib.parse.urljoin(base_url, list_page_url))
            page_soup = BeautifulSoup(page_response.text, "html.parser")

            word_url_list = [word_entry.a.attrs["href"] for index, word_entry in enumerate(
                page_soup.find(class_="lst")) if index % 2 == 1]

            for word_url in word_url_list:
                entryname, meaning = get_word(
                    urllib.parse.urljoin(base_url, word_url))

                f.write("{}\t{}\n".format(entryname, meaning))
