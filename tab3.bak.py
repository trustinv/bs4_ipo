import sys

import requests
from bs4 import BeautifulSoup

from agents import get_user_agents


try:
    req_url = "http://www.ipostock.co.kr/view_pg/view_03.asp?code=B202206162&gmenu="
    req = requests.get(
        req_url,
        headers={"User-Agent": get_user_agents()},
        json={"Content-Type": "application/json"},
    )
except Exception:
    sys.exit()

soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")

table = soup.find("table", {"class": "view_tb"})
data = []

for row in table.find_all("tr"):
    cols = []
    for cell in row.find_all("td"):
        cols.append(cell.text)
    data.append(cols)

copy_data = data.copy()
length_criteria = len(data[0])
for i, dt in enumerate(data):
    each_row_length = len(dt)
    if each_row_length == length_criteria:
        dt.pop(0)

final_data = []

for i in range(len(copy_data[0])):
    sublist = []
    sublist.append(copy_data[0][i])
    sublist.append(copy_data[1][i])
    for j in range(2, len(copy_data)):
        sublist.append(int(copy_data[j][i].replace(",", "")))
    final_data.append(sublist)

print(final_data)
