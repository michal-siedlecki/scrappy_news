import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
import pickle

model = loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
cv = pickle.load(open('count_vectorizer.sav', 'rb'))
app = Flask(__name__)
news_num = 5


def getLabel(header):
    header_cv = cv.transform([header])
    return model.predict(header_cv)


class Feed:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    @property
    def getHeaders(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        if self.name == 'Onet':
            divs = soup.find_all(class_="sectionLine sectionLineMax")
            articles_sets = [div.find_all('a') for div in divs]
            onet_headers = []
            for articles in articles_sets:
                for article in articles:
                    if len(onet_headers) <= news_num+1:
                        header = article.find(class_="title").text
                        link = article.attrs.get('href')
                        label = getLabel(header)[0]
                        onet_headers.append((header, link, label))
                    else:
                        return onet_headers
                    
        if self.name == 'W Polityce':
            divs = soup.find_all(class_="nu-lead-articles") + soup.find_all(class_="nu-tile-container nu-main-col--5")
            articles_sets = [div.find_all('a') for div in divs]
            wpolityce_headers = []
            for articles in articles_sets:
                for article in articles:
                    if len(wpolityce_headers) <= news_num+1:
                        header = article.find(class_="short-title").text
                        link = str(self.url[:-1])+str(article.attrs.get('href'))
                        label = getLabel(header)[0]
                        wpolityce_headers.append((header, link, label))
                    else:
                        return wpolityce_headers

        if self.name == 'Wirtualna Polska':
            wrapper = soup.find(class_="sc-1fu2hk8-0 ezOXAO")
            divs = wrapper.find_all('div')
            wp_headers = []
            if len(wp_headers) <= news_num + 1:
                for div in divs[8:20]:
                    if div.a:
                        header = div.text.strip()
                        link = div.a.get('href')
                        label = getLabel(header)[0]
                        wp_headers.append((header, link, label))

            wp_headers = list(set(wp_headers))
            return wp_headers

        
onet = Feed('Onet', 'https://www.onet.pl/')
wp = Feed('Wirtualna Polska', 'https://www.wp.pl/')
wpolityce = Feed('W Polityce', 'https://wpolityce.pl/')

@app.route("/")
@app.route("/home")
def info():

    headers = onet.getHeaders + wpolityce.getHeaders + wp.getHeaders
    return render_template('home.html', headers=headers)


if __name__ == '__main__':

    app.run(debug=True)
