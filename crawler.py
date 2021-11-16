import requests
import csv
from bs4 import BeautifulSoup as bs
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = bs(html, 'lxml')

    tds = soup.find_all('td', class_="cmc-table__cell--sort-by__name")

    links = []

    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links


def get_page_data(html):
    soup = bs(html, 'lxml')

    try:
        name = soup.find('div', class_='nameSection').find('h2').text.strip()
    except:
        name = ''

    try:
        price = soup.find('div', class_='priceValue').find('span').text.strip()
    except:
        price = ''

    data = {'name': name, 'price': price}
    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'], data['price']))

        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()

    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_links(get_html(url))

    # for index, url in enumerate(all_links):
    #     html = get_html(url)
    #     data = get_page_data(html)
    #     write_csv(data)
    #     print(index + 1)
    
    
    
    with Pool(20) as p:
        p.map(make_all, all_links)
    
    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()