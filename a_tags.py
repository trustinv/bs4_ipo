import re
import sys
import requests
from bs4 import BeautifulSoup
from agents import get_user_agents


def scrape_categories(url, code=None):

    try:

        req = requests.get(
            url=f"{url}/view_01.asp?code={code}", headers={"User-Agent": get_user_agents()}
        )
    except Exception:
        sys.exit()
    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")

    category_path = [a.get("href") for a in soup.find_all("a", href=re.compile("view_0[1-5]"))]
    if category_path:
        pattern = r"\d+"
        extracted_numbers = [re.search(pattern, item).group() for item in category_path]
        result = [int(number) for number in extracted_numbers]
        return result


if __name__ == "__main__":

    code = "B202206162"
    url = "http://www.ipostock.co.kr/view_pg"
    category_nums = scrape_categories(url, code)
    print(category_nums)
