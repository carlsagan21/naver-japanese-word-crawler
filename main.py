import urllib.parse
import sys
import getopt
from crwaler import get_word, get_word_url_list

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv, "")

    level = 5 if not len(args) > 1 else int(args[1])
    parts = 0 if not len(args) > 2 else int(args[2])  # parts=0 every
    pages = 14 if not len(args) > 3 else int(args[3])

    with open("jlpt-level-{}-parts-{}.txt".format(level, parts), "w") as f:
        for page in range(1, pages + 1):
            base_url = "https://ja.dict.naver.com"
            list_page_url = "/jlpt/level-{}/parts-{}/p{}.nhn".format(
                level, parts, page)

            word_url_list = get_word_url_list(
                urllib.parse.urljoin(base_url, list_page_url))

            for word_url in word_url_list:
                entryname, meaning = get_word(
                    urllib.parse.urljoin(base_url, word_url))

                f.write("{}\t{}\n".format(entryname, meaning))
