from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    # flag = db.Column(db.String(100), nullable=False)
    # date_created = db.Column(db.Time, default=time.ctime())
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
     
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        # todo = Todo(title=title, desc=desc, flag="NotDone")
        # print(title)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    allTodo = Todo.query.all()
    # print(allTodo)
    return render_template("index.html", allTodo=allTodo)

# @app.route("/add", methods=['POST'])
# def submit():
#     if request.method == "POST":
#         print("Ya")
#         title = request.form['title']
#         desc = request.form['desc']
#         todo = Todo(title=title, desc=desc)
#         print(title)
#         db.session.add(todo)
#         db.session.commit()
#         return redirect("/")

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>This is products page</p>"

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        # print(title)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# @app.route("/done")

if __name__ == "__main__":
    app.run(debug=True)