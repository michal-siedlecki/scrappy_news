import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def onet_list():
    page = requests.get("https://wiadomosci.onet.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_ = "driverItemTitle itemAnimation")
    return [x.next for x  in news[1:5]]


def wpolityce_list():
    page = requests.get("https://wpolityce.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_ = "short-title")
    return [x.text for x in news[:4]]


def wp_list():
    page = requests.get("https://www.wp.pl/")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all(class_ = "lclzf3-0 egPcYF")
    return [x.text for x in news[:4]]


@app.route("/")
@app.route("/home")
def info():
    feed_list = [onet_list(), wpolityce_list(), wp_list()]
    return render_template('home.html', feed_list=feed_list)


if __name__ == '__main__':
    app.run(debug=True)
