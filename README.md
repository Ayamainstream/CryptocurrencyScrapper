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

![login](https://user-images.githubusercontent.com/72498812/142920616-3a7787fa-c0c7-4366-9326-63a5b90efce8.png)

Then you need to enter the name of the cryptocurrency for which you want to see the news and summary.

![Screenshot_1](https://user-images.githubusercontent.com/72498812/142920767-dceeea45-0116-47f7-b3af-0a27072b545e.png)

Then we see result as two list of paragraphs:

![Screenshot_2](https://user-images.githubusercontent.com/72498812/142920954-7c695e03-85ac-444b-97f6-0134ff68cbe4.png)

After that, we insert it into the database and we see on our table:

![image](https://user-images.githubusercontent.com/72498812/142921482-9de5690a-bd62-4cc1-92a8-a90f15bbaac2.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)
