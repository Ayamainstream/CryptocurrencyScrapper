from typing import Sequence
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from requests import Request, Session, get
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/News'
db = SQLAlchemy(app)

class Scrapper:
    def get_id(currency_name):
        headers = {
            'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': '7344cc03-0292-4fac-a191-b1371f9e2b3a',
        }
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        data = json.loads(response.text)
        id = ""
        for i in data['data']:
            if i['name']:
                name = i['name']
                symbol = i['symbol']
                if name.upper() == currency_name.upper() or symbol == currency_name.upper():
                    id = i['id']
        if id == "":
            print("The currency does not exist!")
            exit()
        else:
            url = f"https://api.coinmarketcap.com/content/v3/news?coins={id}&page=1&size=10"
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
            }

            req = get(url, headers)
            text = req.json()
            data = text['data']
            i = 1
            li = []
            for n in data:
                if n['meta']:
                    meta = n['meta']
                    req = get(meta['sourceUrl'], headers=headers)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")
                    j = 1
                    c_dict = meta['title']
                    # for item in soup.find_all('p'):
                    #     c_dict['Paragraph ' + str(j)] = item.get_text("|", strip=True)
                    #     j += 1
                    li.append(c_dict)
                    i += 1
            return li

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    news = db.Column(db.Text, nullable=False, primary_key=False)

    def __repr__(self):
        return '<News %r>' % self.news


@app.route('/coin', methods=['GET', 'POST'])
def coin():
    counter = 0
    newsName = ''
    if request.method == 'POST':
        coin = request.form.get('coin')
        list = Scrapper.get_id(coin)
        new_ex = News(news=list)
        counter += 1
        db.session.add(new_ex)
        db.session.commit()

        for el in list:
            newsName += f'<p>{el}</p>'

    return '''
           <form method="POST">
               <div><label>Coin name: <input type="text" name="coin"></label></div>
               <input type="submit" value="Submit">
           </form> ''' + newsName

def start():
    app.run(debug=True)

if __name__ == '__main__':
    start()


