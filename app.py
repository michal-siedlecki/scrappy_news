import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)
news_num = 3
class Feed:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        

    def getHeaders(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        
        if self.name == 'Onet':
            divs = soup.find_all(class_="sectionLine sectionLineMax")
            articles_sets = [div.find_all('a') for div in divs]
            onet_dic = {'name' : self.name}
     
            for articles in articles_sets:
                for article in articles:
                    if len(onet_dic) <= news_num+1:
                        onet_dic[article.find(class_="title").text] = article.attrs.get('href')
                    else:
                        return onet_dic
           
        
        
        
        if self.name == 'Wirtualna Polska':
            divs = soup.find_all(class_="sc-1fu2hk8-0 jIlknD")
            articles_sets = [div.find_all('a') for div in divs]
            wp_dic = {'name' : self.name}         
            for articles in articles_sets:
                for article in articles:                
                    if len(wp_dic) <= news_num+1:
                        try:
                            wp_dic[article.find_all('div')[1].text] = article.attrs.get('href')
                        except IndexError:
                            wp_dic[article.find('div').text] = article.attrs.get('href')
                    else:
                        return wp_dic
                    
        
        if self.name == 'W Polityce':
            divs = soup.find_all(class_="nu-lead-articles") + soup.find_all(class_="nu-tile-container nu-main-col--5")
            articles_sets = [div.find_all('a') for div in divs]
            wpolityce_dic = {'name' : self.name}
            for articles in articles_sets:
                for article in articles:
                    if len(wpolityce_dic) <= news_num+1:
                        wpolityce_dic[article.find(class_="short-title").text] = str(self.url[:-1])+str(article.attrs.get('href'))
                    else:
                        return wpolityce_dic

        
onet = Feed('Onet', 'https://www.onet.pl/')
wp = Feed('Wirtualna Polska', 'https://www.wp.pl/')
wpolityce = Feed('W Polityce', 'https://wpolityce.pl/')

feed_dic_list = [onet, wp, wpolityce]





@app.route("/")
@app.route("/home")
def info():

    titles_links = []
    for feed in feed_dic_list:
        titles_links.append(feed.getHeaders())    
        
    
    return render_template('home.html', titles_links=titles_links)


if __name__ == '__main__':

    app.run(debug=True)
    

