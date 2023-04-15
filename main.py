import json
import requests
from bs4 import BeautifulSoup


def get_first_post():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = 'https://bina.az/baki/alqi-satqi/menziller?location_ids%5B%5D=58&location_ids%5B%5D=10&location_ids%5B%5D=190'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')


    articles_cards = soup.find_all('div',class_='items-i')
    new_dict = {}
    for article in articles_cards:
        article_url = f'https://bina.az{article.find("a").get("href")}'
        article_id = article_url.split('/')[-1]
        # resource = requests.get(article_url)
        # soup2 = BeautifulSoup(resource.text, 'lxml')
        # quotes = soup2.find('span', class_='ownership').text
        # if quotes != 'mülkiyyətçi':
        #     continue
        # else:
        article_title = article.find('div', class_="location").text.strip()
        article_price = article.find('div', class_="price").text.strip()
        article_desc = article.find('ul').text.strip()
        article_time = article.find('div', class_="city_when").text.strip()
        new_dict[article_id] = {
                    "article_title" : article_title,
                    "article_price" : article_price,
                    "article_desc" : article_desc,
                    "article_url" : article_url,
                    "article_time" : article_time,
                    "article_id" : article_id
                }

        with open('new_dict.json', 'w', encoding='utf-8') as file:
            json.dump(new_dict, file, indent=4, ensure_ascii=False, )


def check_new_post():
    with open("new_dict.json", encoding='utf-8') as file:
        new_dict = json.load(file)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = 'https://bina.az/baki/alqi-satqi/menziller?location_ids%5B%5D=58&location_ids%5B%5D=10&location_ids%5B%5D=190'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('div', class_='items-i')
    fresh_post = {}
    for article in articles_cards:
        article_url = f'https://bina.az{article.find("a").get("href")}'
        article_id = article_url.split('/')[-1]
        if article_id in new_dict:
            continue
        else:
            article_time = article.find('div', class_="city_when").text.strip()
            if article_time.find('bugün') != -1:
                resource = requests.get(article_url)
                soup2 = BeautifulSoup(resource.text, 'lxml')
                quotes = soup2.find('span', class_='ownership')
                if quotes is None:
                    continue
                else:
                    if quotes.text != 'mülkiyyətçi':
                        continue
                    else:
                        article_title = article.find('div', class_="location").text.strip()
                        article_price = article.find('div', class_="price").text.strip()
                        article_desc = article.find('ul').text.strip()
                        new_dict[article_id] = {
                            "article_title": article_title,
                            "article_price": article_price,
                            "article_desc": article_desc,
                            "article_url": article_url,
                            "article_time": article_time,
                            "article_id": article_id
                        }

                        fresh_post[article_id] = {
                            "article_title": article_title,
                            "article_price": article_price,
                            "article_desc": article_desc,
                            "article_url": article_url,
                            "article_time": article_time,
                            "article_id": article_id
                        }

    with open('new_dict.json', 'w', encoding='utf-8') as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)
    return fresh_post


def main():
    print(check_new_post())

if __name__ == "__main__":
    main()














