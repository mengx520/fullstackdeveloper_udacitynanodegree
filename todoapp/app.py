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
  completed = db.Column(db.Boolean, nullable=False, default=False)
  # adding foreign key to the child model
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
  

  # 3.creating debugging statements
  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# creat TodoList model as parent model and adding foreign key to the child Todo model
class TodoList(db.Modle):
    __tablename__='todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

class 



# 5. sync model with database

# Developing the controller
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # get a json body that were sent as dictionary
        description = request.get_json()['description']
        todo = Todo(description=description, completed=False)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    #if not error:
        # return to a json object
        # return jsonify(body)
    if error:
      abort(400)
    else:
      return jsonify(body)

# set up a route that listen to set-completed
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

# take user's input and notify models to delete the to-do item
@app.route('/todos/<todo_id>/', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  return redirect(url_for('index'))

# set up a route that listen to home page
@app.route('/')

# create route handler
def index():
    # return a template html file
    # 4. replace dummy data with database
    return render_template(
        'index.html', todos=Todo.query.order_by('id').all()
        )

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
