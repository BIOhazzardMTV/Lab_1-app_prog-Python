import socket
import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
import ssl
import os
import time


def save_img(link, img_name):
    try:
        if link.find(".jpg") != -1:
            r = requests.get(link, timeout=2)
            if r:
                filename = f'{img_name:04}.jpg'
                open(filename, "wb").write(r.content)
                return True
    except requests.exceptions.Timeout or \
            socket.timeout or \
            urllib3.exceptions.ReadTimeoutError or \
            requests.exceptions.ConnectionError or \
            requests.exceptions.SSLError or \
            urllib3.exceptions.MaxRetryError or \
            ssl.SSLCertVerificationError:
        return False
    return False


def full_save(class_name, num_of_pictures):
    print(f"Начало загрузки изображений класса {class_name}")
    os.chdir(f"{class_name}")
    if not os.path.isfile(f"info-{class_name}.txt"):
        i = 0
        j = 0
    else:
        i = int(open(f"info-{class_name}.txt", "r").readline())
        j = int(open(f"info-{class_name}.txt", "r").readline(2))
    num_of_uploaded = 0
    page_num = 0
    n = 29
    session = requests.session()
    response = session.get(f"https://yandex.ru/images/search?p={page_num}&text={class_name}", timeout=2)
    soup = BeautifulSoup(response.text, "lxml")
    while num_of_uploaded != num_of_pictures:
        time.sleep(0.05)
        data = str(soup.find("div", class_=f"serp-item_pos_{i}"))
        if data.find('"origin":{"') != -1:
            data = data.split('"origin":{"')
            data = data[1].split('"url":"')
            data = data[1].split('"}')
            # print(f"i = {i}; " + f"j = {j}; " + f"page_num = {page_num}  " + f"link : {data[0]}")
            if save_img(data[0], j):
                print(f'{round((100 * num_of_uploaded / num_of_pictures), 2)}%')
                j += 1
                num_of_uploaded += 1
            else:
                print(f'{round((100 * num_of_uploaded / num_of_pictures), 2)}%')
            if i == n:
                page_num += 1
                soup = BeautifulSoup(response.text, "lxml")
                n += 30
        i += 1
        open(f"info-{class_name}.txt", "w+").write(f"{i}\n{j}")
    os.chdir("..")
    print(f'Изображения класса "{class_name}" в количестве {num_of_pictures} шт. успешно завершена!')
    print("")


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
full_save("cat", 11)
time.sleep(0.01)
full_save("dog", 11)
