from flask_login import UserMixin
from SqliteDbConnection import Singleton

class User(UserMixin):
  def __init__(self, id, username, email, password):
    self.id = id
    self.username = username
    self.email = email
    self.password = password
  
  @classmethod
  def get(cls, user_id):
    db = Singleton()
    user = db.select_user_by_id(user_id)
    if user:
      return cls(user[0], user[1], user[2], user[3])
    return None
  
  @classmethod
  def get_by_username(cls, username):
    db = Singleton()
    user = db.select_user_by_username(username)
    if user:
        return cls(user[0], user[1], user[2], user[3])
    return None
  
  @classmethod
  def get_by_email(cls, email):
    db = Singleton()
    user = db.select_user_by_email(email)
    if user:
        return cls(user[0], user[1], user[2], user[3])
    return None