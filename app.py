import requests
from flask import Flask, render_template
import pickle
import os

model = loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
cv = pickle.load(open('count_vectorizer.sav', 'rb'))
app = Flask(__name__)



parameters = {
    'country' : 'pl',
    'apiKey' : '57a2030723934ee69c14205829d6c300'
}


def getLabel(header):
    header_cv = cv.transform([header])
    print(header_cv)
    print(header_cv.toarray())
    return model.predict(header_cv)



def getNews():
    response = requests.get('https://newsapi.org/v2/top-headlines?', params=parameters)
    articles = response.json().get('articles')
    news = []
    for article in articles:
        title = article.get('title')
        url = article.get('url')
        label = getLabel(title)[0]
        news.append((title, url, label))
    return news

getNews()


@app.route("/")
@app.route("/home")
def info():

    news = getNews()
    return render_template('home.html', news=news)


if __name__ == '__main__':

    app.run(debug=False)

