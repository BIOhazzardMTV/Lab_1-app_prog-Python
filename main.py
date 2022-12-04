import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
import os
import time
urllib3.disable_warnings()


def save_img(link, img_name, session):
    try:
        if link.find(".jpg") != -1:
            r = session.get(link, timeout=2, verify=False, allow_redirects=True)
            if r:
                filename = f'{img_name:04}.jpg'
                open(filename, "wb").write(r.content)
                return True
    except Exception:
        print("Timeout")
    return False


def full_save(class_name, num_of_required_pictures):
    print(f'Начало загрузки изображений класса "{class_name}"')
    os.chdir(f'{class_name}')
    if not os.path.isfile(f"info-{class_name}.txt"):
        i = 0
        j = 0
        page_num = 0
    else:
        file = open(f"info-{class_name}.txt", "r")
        i = int(file.readline())
        j = int(file.readline())
        page_num = int(file.readline())
        file.close()
    num_of_uploaded = 0
    n = 29 + 30 * page_num
    session = requests.session()
    response = session.get(f"https://yandex.ru/images/search?p={page_num}&text={class_name}", timeout=2)
    soup = BeautifulSoup(response.text, "lxml")
    num_of_errors_in_a_row = 0
    while num_of_uploaded < num_of_required_pictures:
        time.sleep(0.2)
        data = str(soup.find("div", class_=f"serp-item_pos_{i}"))
        if data.find('"origin":{"') != -1:
            data = data.split('"origin":{"')
            data = data[1].split('"url":"')
            data = data[1].split('"}')
            if save_img(data[0], j, session):
                j += 1
                num_of_uploaded += 1
                num_of_errors_in_a_row = 0
        else:
            num_of_errors_in_a_row += 1
        print(f'{round((100 * num_of_uploaded / num_of_required_pictures), 2)}%')
        if i >= n:
            page_num += 1
            response = session.get(f"https://yandex.ru/images/search?p={page_num}&text={class_name}", timeout=2)
            soup = BeautifulSoup(response.text, "lxml")
            n += 30
        i += 1
        open(f"info-{class_name}.txt", "w+").write(f"{i}\n{j}\n{page_num}")
        if num_of_errors_in_a_row == 10:
            break
    if num_of_uploaded != num_of_required_pictures:
        print(f'Удалось скачать только {num_of_uploaded} шт. изображений класса "{class_name}"'
              f'(требовалось {num_of_required_pictures} шт.) ')
        print("")
    else:
        print(f'Изображения класса "{class_name}" в количестве {num_of_uploaded} шт. успешно завершена!')
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
try:
    full_save('dog', 162)
except Exception:
    print("Error")
