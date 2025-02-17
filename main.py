from flask import Flask, render_template, request, redirect, url_for
import bcrypt
from SqliteDbConnection import Singleton
from dotenv import load_dotenv
import os 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User
import json

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
  sqlite_db = Singleton()
  print(sqlite_db.select_all_users())
  print(sqlite_db.select_all_logs())
  print(sqlite_db.select_all_user_answers())
  print(sqlite_db.select_all_questions())
  if request.method == "POST":
    print("Yes")
    email = request.form["user_email"]
    password = request.form["user_password"]
    password_bytes = password.encode("utf-8")
    user = User.get_by_email(email)
    print(user)
    if user:
      hashed_password = user.password
      result = bcrypt.checkpw(password_bytes, hashed_password)
      if result:
        print("Trying to Logged In")
        login_user(user)
        sqlite_db.insert_login_user_to_logs(user.id)
        print("logged In")
        return redirect(url_for("qualifications"))
  return render_template("index.html")


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
    print("Trying")
    user = sqlite_db.select_user_by_email(email)
    if not user:
      sqlite_db.insert_user_query(username, email, hashed_password)

      print("Success")
    print("Tried")
    return redirect(url_for("login"))
  return render_template("register.html")


@app.route("/qualifications", methods=["GET"])
@login_required
def qualifications():
  return render_template("qualifications.html", user_name="Svajunas", message="Hello world")


@app.route("/qualifications_1", methods=["GET"])
@login_required
def qualifications_1():
  return render_template("qualifications.html", user_name="Still_Svajunas", message="Still hello")


@app.route("/logout")
def logout():
  db = Singleton()
  db.update_login_user_to_logs(current_user.id)
  logout_user()
  return redirect(url_for("login"))


if __name__ == "__main__": 
  app.run(debug=True)