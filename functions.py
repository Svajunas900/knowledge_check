from SqliteDbConnection import Singleton


def check_answers(user_answers):
  db = Singleton()
  user_answers = cleanup_answers(user_answers)
  points = 0
  for answer in user_answers:
    if len(answer) == 3:
      question_id = answer[0]
      question = db.select_question_by_id(question_id)
      real_answer = question[-1]
      user_answer = answer[-1]
      if real_answer == user_answer:
        points += 1
  score = calculate_score(points)
  return score


def cleanup_answers(user_answers):
  result = []
  for answer in user_answers:
    new_list = filter(lambda x: x != None, list(answer))
    result.append(list(new_list))
  return result


def calculate_score(points):
  return f"{100*points/40}%"
