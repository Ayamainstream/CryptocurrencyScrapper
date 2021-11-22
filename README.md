# Scrapper SQLAlchemy cryptocurrency and summarize of the paragraphs
A project for displaying news and their summary about cryptocurrencies on the page and saving it in the database.

## Installation
### Install Flask, SQLAlchemy, requests, transformers, Werkzeug
```
pip install flask, requests, Flask-SQLAlchemy, transformers, Werkzeug
```
Change path in test.py file to path where project located on your system

```python
sys.path.insert(0,'YOUR_PATH')

```
Create table in PostgreSQL by using SQL dump file that locates in this repository.

Change URI password, username and database name in code
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://YOUR_USERNAME:DATABSE_PASSWORD@localhost/DATABASE_NAME'
```
## Usage
```python
from src import db
scrapper.start()
```
## Examples
First you can see login page where you should enter your login and password.

You need to enter the name of the cryptocurrency for which you want to see the news.

![image](https://user-images.githubusercontent.com/72498812/140555750-35d0969b-e68b-4bee-9d76-2636d680c5e7.png)

Then we see result as list of paragraphs:

![image](https://user-images.githubusercontent.com/72498812/140556124-86ed65dc-5b1a-4667-859b-23c4d93ca69c.png)

After that, we insert it into the database:

![image](https://user-images.githubusercontent.com/72498812/140556503-bb261754-3d71-4294-be39-7fa86d4ddfe7.png)

Here we see our paragraphs:

![image](https://user-images.githubusercontent.com/72498812/140556542-35045663-8048-4cf4-9841-3c75a0461e21.png)

If we want choose another cryptocurrency:

![image](https://user-images.githubusercontent.com/72498812/140556814-9ed21e1e-903b-40b9-92f6-e41a9b76e302.png)
![image](https://user-images.githubusercontent.com/72498812/140557264-293b59ab-5e6f-47c2-a9c4-1b305853f073.png)

We see it on our table:

![image](https://user-images.githubusercontent.com/72498812/140557207-a46152e6-3a9d-4044-b4a0-ca987d63231d.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)
