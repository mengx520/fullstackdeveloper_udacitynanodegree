from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__) 
# 6. config flask to a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://panda:mengxuxu520@localhost:5432/todoapp'
# 7. after config we need to create a sql databse in commandline createdb todoapp
# 8. connect with psql todoapp to insert records:todoapp=# INSERT INTO todos (description) VALUES ('To do 1');
# 1.define db object which link sqlalchemy to our app
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# 2. create class
class Todo(db.Model):
  # tablename cannot be capitalized
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  # 3.creating debugging statements
  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'
# 5. sync model with database

# Developing the controller
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # get a json body that were sent as dictionary
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # return to a json object
        return jsonify(body)

# set up a route that listen to home page
@app.route('/')

# create route handler
def index():
    # return a template html file
    # 4. replace dummy data with database
    return render_template(
        'index.html', data=Todo.query.all()
        )

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
