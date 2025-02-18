import sqlite3
import datetime
import json

class MetaSingleton(type):
  _instances = {}

  def __call__(cls, *args, **kwds):
    if cls not in cls._instances:
      instance = super().__call__(*args, **kwds) 
      cls._instances[cls] = instance
    return cls._instances[cls]
  

class Singleton(metaclass=MetaSingleton):
  def __init__(self):
    self.connection = sqlite3.connect("quiz_db.db", check_same_thread=False)
    self.cursor = self.connection.cursor()
  

  def create_tables(self):
    self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
                      id INTEGER PRIMARY KEY,
                      username TEXT,
                      email TEXT,
                      password TEXT)
  """)
    self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
                        id INTEGER PRIMARY KEY,
                        user_id INT NOT NULL,
                        login INTEGER,
                        logged_in_time TEXT,
                        logged_out_time TEXT,
                        activity TEXT,
                        FOREIGN KEY (user_id) 
                        REFERENCES users (id) 
                            ON DELETE CASCADE 
                            ON UPDATE CASCADE);
    """)
    self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        option_1,
                        option_2,
                        option_3,
                        option_4,
                        correct_answer INTEGER)
""")
    self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_answers(
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        question_id INTEGER,
                        answer INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        FOREIGN KEY (question_id) REFERENCES questions(id))""")
    self.connection.commit()
  
  def insert_user_query(self, username, email, password):
    self.cursor.execute(f"INSERT INTO users(username, email, password) VALUES(?, ?, ?)", (username, email, password))
    self.connection.commit()

  def insert_login_user_to_logs(self, user_id):
    self.cursor.execute(f"INSERT INTO logs(user_id, login, logged_in_time, logged_out_time, activity) VALUES(?, ?, ?, ?, ?)", 
                        (user_id, 0, str(datetime.datetime.now().time()), "", "Played Quiz"))
    self.connection.commit()

  def insert_question(self, question, option_1, option_2, option_3, option_4, correct_answer):
    self.cursor.execute("INSERT INTO questions(question, option_1, option_2, option_3, option_4, correct_answer) VALUES(?, ?, ?, ?, ?, ?)",
                        (question, option_1, option_2, option_3, option_4, correct_answer))
    self.connection.commit()

  def update_login_user_to_logs(self, user_id):
    self.cursor.execute(f"SELECT * FROM logs WHERE user_id = ? ORDER BY logged_in_time DESC LIMIT 1", (user_id,))
    row = self.cursor.fetchone()
    logged_in_time = row[3]
    if row:
      logged_in_time = datetime.datetime.strptime(logged_in_time, '%H:%M:%S.%f').time()
      time_now = datetime.datetime.now().time()
      datetime1 = datetime.datetime.combine(datetime.datetime.today(), logged_in_time)
      datetime2 = datetime.datetime.combine(datetime.datetime.today(), time_now)
      time_spend = datetime2-datetime1
      self.cursor.execute(f"UPDATE logs SET logged_out_time = ?, login = ? WHERE id=?", (str(time_spend), 1, row[0]))
      self.connection.commit()

  def select_user_by_email(self, email):
    self.cursor.execute(f"SELECT * FROM users WHERE email =?", (email,))
    result = self.cursor.fetchone()
    return result
  
  def select_user_by_id(self, id):
    self.cursor.execute(f"SELECT * FROM users WHERE id =?", (id,))
    result = self.cursor.fetchone()
    return result
  
  def select_user_by_username(self, username):
    self.cursor.execute(f"SELECT * FROM users WHERE username =?", (username,))
    result = self.cursor.fetchone()
    return result

  def select_question_by_id(self, id):
    self.cursor.execute(f"SELECT * FROM questions WHERE id =?", (id,))
    result = self.cursor.fetchone()
    return result

  def select_question_by_question(self, question):
    self.cursor.execute(f"SELECT * FROM questions where question =?", (question,))
    result = self.cursor.fetchone()
    return result

  def select_all_users(self):
    self.cursor.execute("SELECT * FROM users")
    result = self.cursor.fetchall()
    return result
  
  def select_all_logs(self):
    self.cursor.execute("SELECT * FROM logs")
    result = self.cursor.fetchall()
    return result
  
  def select_all_questions(self):
    self.cursor.execute("SELECT * FROM questions")
    result = self.cursor.fetchall()
    return result

  def select_all_user_answers(self):
    self.cursor.execute("SELECT * FROM user_answers")
    result = self.cursor.fetchall()
    return result
  
db = Singleton()
db.create_tables()
questions = db.select_all_questions()
if len(questions) < 1:
  with open("questions.json") as file:
    questions = json.load(file)
    for question in questions["questions"]:
      quiz_question = questions["questions"][question]["question"]
      option_1 = questions["questions"][question]["option_1"]
      option_2 = questions["questions"][question]["option_2"]
      option_3 = questions["questions"][question]["option_3"]
      option_4 = questions["questions"][question]["option_4"]
      correct_answer = questions["questions"][question]["correct_answer"]
      db.insert_question(quiz_question, option_1, option_2, option_3, option_4, correct_answer)
    print("Success")
  