import requests
from bs4 import BeautifulSoup
import os
import time


def get_url(num, name):
    url = f"https://yandex.ru/images/search?p={num}&text={name}"
    html_page = requests.get(url)
    return html_page


if not os.path.isdir("dataset"):
    os.mkdir("dataset")
    os.chdir("dataset")
    os.mkdir("cat")
    os.mkdir("dog")
else:
    os.chdir("dataset")
    if not os.path.isdir("cat"):
        os.mkdir("cat")
    if not os.path.isdir("dog"):
        os.mkdir("dog")
page_num = 0
soup = BeautifulSoup(get_url(page_num, 'cat').text, "lxml")
for i in range(0, 30):
    time.sleep(0.5)
    data = str(soup.find("div", class_=f"serp-item_pos_{i}"))
    data = data.split('origin":')
    data = data[1].split('url":"')
    data = data[1].split('"},')
    print(i,"",data[0])
