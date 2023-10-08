from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db.init_app(app)

class Todo(db.Model):
    sno : Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title : Mapped[str] = mapped_column(db.String(50), nullable=False)
    desc : Mapped[str] = mapped_column(db.String(500), nullable=False)
    dateCreated : Mapped[str] = mapped_column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo = Todo(title = request.form["title"], desc = request.form["desc"])
        db.session.add(todo)
        db.session.commit()
        
    allTodos = Todo.query.all()
    return render_template('index.html', allTodos = allTodos)


@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).one()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=8000)