import sys
import requests
from bs4 import BeautifulSoup
from tabs import tab1, tab2, tab3, tab4, tab5
from agents import get_user_agents


def scrate_categories():
    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers={"User-Agent": get_user_agents()})
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")


if __name__ == "__main__":
    import a_tags

    code = "B202206162"
    url = "http://www.ipostock.co.kr/view_pg"
    categories = a_tags.scrape_categories(url, code)
    result1 = tab1.scrape_ipostock(categories[0])
    result2 = tab2.scrape_ipostock(categories[1])
    result3 = tab3.scrape_ipostock(categories[2])
    result4 = tab4.scrape_ipostock(categories[3])
    result5 = tab5.scrape_ipostock(categories[4])
