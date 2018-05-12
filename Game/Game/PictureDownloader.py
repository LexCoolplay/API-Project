import requests


def picture_downloader(name):
    response_array = requests.get("https://yandex.ru/images/search?text={}&format=soap".format(name))\
        .text.split("img_href")
    element_of_array = response_array[1][3:]
    img_adr = ""
    i = 0
    while True:
        if element_of_array[i] == '"':
            break
        img_adr += element_of_array[i]
        i += 1
    response = requests.get(img_adr)
    return response.content
