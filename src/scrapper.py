from flask import Flask, render_template
from flask.helpers import make_response, url_for
from flask import request
from flask.json import jsonify
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from requests import Session, get
import json
from bs4 import BeautifulSoup
from transformers import pipeline
from werkzeug.utils import redirect

summarizer = pipeline('summarization')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASSWORD@localhost/DATABASE'
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
                    c_dict = ''
                    #c_dict = meta['title']
                    for item in soup.find_all('p'):
                        c_dict += item.get_text("|", strip=True)
                        j += 1
                    li.append(c_dict)
                    i += 1
            return li


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    news = db.Column(db.Text, nullable=False, primary_key=False)
    summary = db.Column(db.Text, nullable=False, primary_key=False)

    def __repr__(self):
        return '<News %r>' % self.news


class Users(db.Model):

    tablename = 'users'

    id = db.Column('id', db.Integer, primary_key=True)

    login = db.Column('login', db.String(50))

    password = db.Column('password', db.String(50))

    token = db.Column('token', db.Text)

    def init(self, id, login, password, token):
        self.id = id
        self.login = login
        self.password = password
        self.token = token


app.config['SECRET_KEY'] = 'thisismyflasksecretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return '<h1>There is no token<h1>'
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return '<h1>Hello, Could not verify the token </h1>'

        return f(*args, **kwargs)

    return decorated


@app.route('/coin', methods=['GET', 'POST'])
@token_required
def coin():
    userNews = []
    userSummary = []
    if request.method == 'POST':
        coin = request.form.get('coinName')
        list = Scrapper.get_id(coin)
        for el in list:
            new_ex = News(news=el, summary=summarizer(el, max_length=40, min_length=20,
                                                      do_Sample=False)[0]['summary_text'])
            db.session.add(new_ex)
            db.session.commit()

        for el in News.query.order_by(News.id.desc()).all():
            userNews.append(str(el.news))
            userSummary.append(str(el.summary))
    return render_template('news.html', news=userNews, summary=userSummary)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        userLogin = form["login"]
        password = form["password"]
        users = Users.query.filter_by(login=userLogin).first()
        if users:
            if users.password == password:
                token = jwt.encode({'user': userLogin, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=6000)}, app.config['SECRET_KEY'])
                update_this = Users.query.filter_by(id=users.id).first()
                update_this.token = token.decode('UTF-8')
                db.session.commit()
                return redirect(url_for(f"coin", token=token.decode('UTF-8')))
            else:
                return render_template('login.html')
    return render_template('login.html', isCorrect='is-invalid', incorrectText='Your password or login not valid')

def start():
    app.run(debug=True)

if __name__ == '__main__':
    start()
