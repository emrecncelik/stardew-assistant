import json
import requests
from bs4 import BeautifulSoup

# TODO: Download html content of all pages extracted

GET_ARTICLE_NAMES = False
DOWNLOAD_ARTICLE_PAGES = True
BASE_URL = "https://stardewvalleywiki.com"


def get_page(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        print("Failed to retrieve HTML. Status code:", response.status_code)
        return None


def find_pages(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    li_elements = soup.find("ul", {"class": "mw-allpages-chunk"}).find_all(
        "a", recursive=True
    )
    return [li.get("href") for li in li_elements]


def find_next_page(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    nav_element = soup.find("div", {"class": "mw-allpages-nav"}).find_all("a")[-1]
    return nav_element.get("href")


def save_dict_as_json(filename: str, data: dict) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)


def read_json_as_dict(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def save_html(filename: str, html_content: str) -> None:
    with open(filename, "w") as f:
        f.write(html_content)


def read_html(filename: str) -> BeautifulSoup:
    with open(filename, "r") as f:
        return BeautifulSoup(f.read(), "html.parser")


if __name__ == "__main__":

    if GET_ARTICLE_NAMES:
        i = 0
        main_page = "https://stardewvalleywiki.com/mediawiki/index.php?title=Special:AllPages&hideredirects=1"
        article_pages = {}

        while True:
            # TODO: Add a logic to end this when it reaches the end of the pages
            # TODO: Maybe respect a little and add sleep time?
            # TODO: This gets 1990 pages, wiki says 1992. Why?
            main_page_html = get_page(main_page)
            article_pages_temp = find_pages(main_page_html)
            old_main_page = main_page
            main_page = BASE_URL + find_next_page(main_page_html)

            article_pages[old_main_page] = article_pages_temp
            save_dict_as_json("data/article_pages.json", article_pages)

            print(f"#" * 50)
            print(f"Page {i} done!")
            print(f"First 10: " + str(article_pages_temp[:10]))
            print(f"Last 10: " + str(article_pages_temp[-10:]))
            print(f"#" * 50)

            i += 1

    if DOWNLOAD_ARTICLE_PAGES:
        article_names = read_json_as_dict("data/article_pages.json")
        article_pages = []

        for a in article_names.values():
            article_pages.extend(a)

        del article_names

        for i, page in enumerate(article_pages):
            if i < 269:
                continue
            print(f"#" * 50)
            print(f"Downloading page {i} of {len(article_pages)}: {page}")
            html_content = get_page(BASE_URL + page)
            page = page.replace("/", "")
            save_html(f"data/article_pages/{page}.html", html_content)
            print(f"Page {i} done!")
            print(f"#" * 50)
