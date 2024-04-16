import json
import requests
from bs4 import BeautifulSoup

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


if __name__ == "__main__":
    i = 0
    main_page = "https://stardewvalleywiki.com/mediawiki/index.php?title=Special:AllPages&hideredirects=1"
    article_pages = {}

    while True:
        # TODO: Add a logic to end this when it reaches the end of the pages
        main_page_html = get_page(main_page)
        article_pages_temp = find_pages(main_page_html)
        old_main_page = main_page
        main_page = BASE_URL + find_next_page(main_page_html)

        article_pages[old_main_page] = article_pages_temp
        save_dict_as_json("article_pages.json", article_pages)

        print(f"#" * 50)
        print(f"Page {i} done!")
        print(f"First 10: " + str(article_pages_temp[:10]))
        print(f"Last 10: " + str(article_pages_temp[-10:]))
        print(f"#" * 50)

        i += 1
