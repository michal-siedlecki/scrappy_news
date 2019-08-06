import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)
news_num = 6

class Feed:
    def __init__(self, name, url, selector):
        self.name = name
        self.url = url
        self.selector = selector


class Feed:
    def __init__(self, name, url, selector):
        self.name = name
        self.url = url
        self.selector = selector


onet = Feed('onet', 'https://wiadomosci.onet.pl/', "driverItemTitle itemAnimation")


def pull(url, selector):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_=selector)

    if url == 'https://wiadomosci.onet.pl/':
        return [x.next for x in news[1:(news_num - 1)]]
    elif url == 'http://wiadomosci.gazeta.pl/wiadomosci/0,0.html#s=NavLinks':
        return [x.header.h2.text for x in news[:news_num]]
    elif url == 'class_="item-list':
        return [news[x].ul.li.text.replace("\n", "") for x in range(news_num)]
    else:
        return [x.text for x in news[:news_num]]


print(pull(onet.url, onet.selector))


'''
def onet_list():
    page = requests.get("https://wiadomosci.onet.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_="driverItemTitle itemAnimation")
    return [x.next for x in news[1:(news_num-1)]]


def wpolityce_list():
    page = requests.get("https://wpolityce.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_="short-title")
    return [x.text for x in news[:news_num]]


def wp_list():
    page = requests.get("https://www.wp.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_="lclzf3-0 egPcYF")
    return [x.text for x in news[:news_num]]


def gazeta_list():
    page = requests.get("http://wiadomosci.gazeta.pl/wiadomosci/0,0.html#s=NavLinks")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_="article")
    return [x.header.h2.text for x in news[:news_num]]


def gazetapolska_list():
    page = requests.get("https://www.gazetapolska.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_="item-list")
    return [news[x].ul.li.text.replace("\n", "") for x in range(news_num)]


@app.route("/")
@app.route("/home")
def info():
    feed_list = [onet_list(), wpolityce_list(), wp_list(), gazeta_list(), gazetapolska_list()]
    return render_template('home.html', feed_list=feed_list)


if __name__ == '__main__':
    app.run(debug=True)
    
    '''
