from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    done = db.Column(db.Boolean)


db.create_all()


@app.route("/")
def index():
    # show all todo item
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route("/add", methods=['POST'])
def add():
    # add new to do item
    title = request.form.get("title")
    new_todo = Todo(title=title, done=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new to do item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # add new to do item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
