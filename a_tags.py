import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from agents import get_user_agents


async def scrape_categories(url, code=None):
    url = f"{url}/view_01.asp?code={code}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print("Request failed, retrying in 5 seconds...")
        print(e)
        await asyncio.sleep(0.3)

    category_path = [a.get("href") for a in soup.find_all("a", href=re.compile("view_0[1-5]"))]
    if category_path:
        pattern = r"\d+"
        extracted_numbers = [re.search(pattern, item).group() for item in category_path]
        result = [int(number) for number in extracted_numbers]
        return result


if __name__ == "__main__":

    async def main():
        async with aiohttp.ClientSession() as session:
            code = "B202010131"
            url = "http://www.ipostock.co.kr/view_pg"
            category_nums = await scrape_categories(url, code)
            print(category_nums)

    asyncio.run(main())
