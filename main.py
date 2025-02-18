from flask import Flask, render_template, request, redirect, url_for
import bcrypt
from SqliteDbConnection import Singleton
from dotenv import load_dotenv
import os 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User
import random
from functions import check_answers


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_db.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(user_id):
    return User.get(user_id)


@app.route("/", methods=["GET", "POST"])
def login():
  score = request.args.get('score')
  sqlite_db = Singleton()
  if request.method == "POST":
    email = request.form["user_email"]
    password = request.form["user_password"]
    password_bytes = password.encode("utf-8")
    user = User.get_by_email(email)
    if user:
      hashed_password = user.password
      result = bcrypt.checkpw(password_bytes, hashed_password)
      if result:
        login_user(user)
        sqlite_db.insert_login_user_to_logs(user.id)
        return redirect(url_for("qualifications"))
  return render_template("index.html", score=score)


@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    sqlite_db = Singleton()
    username = request.form["user_username"]
    email = request.form["user_email"]
    password = request.form["user_password"]
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    user = sqlite_db.select_user_by_email(email)
    if not user:
      sqlite_db.insert_user_query(username, email, hashed_password)
    return redirect(url_for("login"))
  return render_template("register.html")


@app.route("/qualifications", methods=["GET", "POST"])
@login_required
def qualifications():
  sqlite_db = Singleton()
  if request.method == "POST":
    user_answers = []
    for i in range(1,41):
      question_id = i
      question = request.form.get(f"question-{i}", None)
      answer_1 = request.form.get(f"answer-1-{i}", None)
      answer_2 = request.form.get(f"answer-2-{i}", None)
      answer_3 = request.form.get(f"answer-3-{i}", None)
      answer_4 = request.form.get(f"answer-4-{i}", None)
      if answer_1:
        answer_1 = 1
      if answer_2:
        answer_2 = 2
      if answer_3:
        answer_3 = 3
      if answer_4:
        answer_4 = 4
      user_answers.append((question_id, int(question), answer_1, answer_2, answer_3, answer_4))
    score = check_answers(user_answers)
    print(score)
    return redirect(url_for("login", score=score))
  all_questions = sqlite_db.select_all_questions()
  random.shuffle(all_questions)
  return render_template("qualifications.html", user_name="Svajunas", message="Hello world", questions=all_questions)


@app.route("/logout")
def logout():
  db = Singleton()
  db.update_login_user_to_logs(current_user.id)
  logout_user()
  return redirect(url_for("login"))


if __name__ == "__main__": 
  app.run(debug=True)