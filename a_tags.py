import re
import time
import requests
from bs4 import BeautifulSoup
from agents import get_user_agents


def scrape_categories(url, code=None):

    url = f"{url}/view_01.asp?code={code}"

    session = requests.Session()
    session.timeout = 3
    while True:
        try:
            req = session.get(url)
            req.encoding = "utf-8"
            print(req.text)
            # req = requests.get(url)
            soup = BeautifulSoup(req.content, "lxml")
            break
        except requests.exceptions.ReadTimeoutError as e:
            print("Request failed, retrying in 5 seconds...")
            print(e)
            time.sleep(0.3)
        except requests.exceptions.ConnectionError as e:
            print("Request failed, retrying in 5 seconds...")
            print(e)
            time.sleep(0.3)
        except requests.exceptions.RequestException as e:
            print("Request failed, retrying in 5 seconds...")
            print(e)
    category_path = [a.get("href") for a in soup.find_all("a", href=re.compile("view_0[1-5]"))]
    if category_path:
        pattern = r"\d+"
        extracted_numbers = [re.search(pattern, item).group() for item in category_path]
        result = [int(number) for number in extracted_numbers]
        return result


if __name__ == "__main__":

    code = "B202010131"
    url = "http://www.ipostock.co.kr/view_pg"
    category_nums = scrape_categories(url, code)
    print(category_nums)
