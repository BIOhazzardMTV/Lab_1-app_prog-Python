import requests
from bs4 import BeautifulSoup
import os
import time


def get_url(num, name):
    url = f"https://yandex.ru/images/search?p={num}&text={name}"
    html_page = requests.get(url)
    return html_page


def save_img(link, class_name, img_name):
    try:
        if link.find(".jpg") != -1:
            r = requests.get(link, timeout=1)
            if r:
                os.chdir(f"{class_name}")
                filename = f'{img_name:03}.jpg'
                # print(filename)
                open(filename, "wb",).write(r.content)
                os.chdir("..")
                # print(len(os.listdir(f"{class_name}")))
                return True
        return False
    except requests.exceptions.Timeout:
        print("Time out")


def full_save(class_name):
    page_num = 0
    soup = BeautifulSoup(get_url(page_num, f'{class_name}').text, "lxml")
    n = 29
    i = 0
    j = 0
    while j != 100:
        time.sleep(0.05)
        data = str(soup.find("div", class_=f"serp-item_pos_{i}"))
        data = data.split('origin":')
        data = data[1].split('url":"')
        data = data[1].split('"},')
        print(j, "", data[0])
        if save_img(data[0], f"{class_name}", j):
            print("Success")
            j += 1
        else:
            print("Error")
        if i == n:
            page_num += 1
            soup = BeautifulSoup(get_url(page_num, f'{class_name}').text, "lxml")
            n += 30
        i += 1


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
full_save("cat")
full_save("dog")
# while (len(os.listdir(f"dataset/{class_name}")) != 1000):
