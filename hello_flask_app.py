from flask import Flask
# SQLAlchemy is a class we can link to Flask app to use sqlalchemy
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# before connect to db we need to set configuation variable on application 
# postgresql defaultly will pick a DBAPI but you can all add +psycopg2 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://panda:mengxuxu520@localhost:5432/panda'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# link an instance of database that we can interact with in sqlalchemy land to flask app
db = SQLAlchemy(app)

class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  title = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Person ID: {self.id}, name: {self.name}, title:{self.title}>'

db.create_all()

@app.route('/')
def index():
  person = Person.query.first()
  return 'I am ' + person.name + ' the ' + person.title

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)