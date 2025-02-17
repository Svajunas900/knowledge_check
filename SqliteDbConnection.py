import sqlite3


class MetaSingleton(type):
  _instances = {}

  def __call__(cls, *args, **kwds):
    if cls not in cls._instances:
      instance = super().__call__(*args, **kwds) 
      cls._instances[cls] = instance
    return cls._instances[cls]
  

class Singleton(metaclass=MetaSingleton):
  def __init__(self):
    self.connection = sqlite3.connect("quiz_db.db")
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
                        login INTEGER,
                        time_spend TEXT,
                        activity TEXT)
    """)
    self.connection.commit()


# db = Singleton()
# db.create_tables()