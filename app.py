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

    def get_headers(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news = soup.find_all(class_=self.selector)

        if self.url == 'https://wiadomosci.onet.pl/':
            return [x.next for x in news[1:(news_num - 1)]]
        elif self.url == 'http://wiadomosci.gazeta.pl/wiadomosci/0,0.html#s=NavLinks':
            return [x.header.h2.text for x in news[:news_num]]
        elif self.url == 'https://www.gazetapolska.pl/':
            return [news[x].ul.li.text.replace("\n", "") for x in range(news_num)]
        else:
            return [x.text for x in news[:news_num]]


onet = Feed('Onet', 'https://wiadomosci.onet.pl/', "driverItemTitle itemAnimation")
wp = Feed('Wirtualna Polska', 'https://www.wp.pl/', "lclzf3-0 egPcYF")
wpolityce = Feed('W Polityce', 'https://wpolityce.pl/', 'short-title')
gazeta = Feed('Gazeta.pl', 'http://wiadomosci.gazeta.pl/wiadomosci/0,0.html#s=NavLinks', 'article')
gazetapolska = Feed('Gazeta Polska', 'https://www.gazetapolska.pl/', 'item-list')

feed_list = [onet, wp, wpolityce, gazeta, gazetapolska]


@app.route("/")
@app.route("/home")
def info():
    for feed in feed_list:
        feed.get_headers()
    
    return render_template('home.html', feed_list=feed_list)


if __name__ == '__main__':

    app.run(debug=True)
    

