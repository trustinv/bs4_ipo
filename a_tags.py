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
    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")

    category_path = [a.get("href") for a in soup.find_all("a", href=re.compile("view_0[1-5]"))]
    if category_path:
        result = []
        for path_n_query in category_path:
            combined_url = f"{url}/{path_n_query}"
            result.append(combined_url)
        return result


if __name__ == "__main__":
    import a_tags

    code = "B202206162"
    url = "http://www.ipostock.co.kr/view_pg"
    each_full_urls = a_tags.scrape_categories(url, code)
