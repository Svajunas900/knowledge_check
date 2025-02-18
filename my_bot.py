from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from SqliteDbConnection import Singleton
import time
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os 
import random


load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def solve_quiz():
  answers = random.randrange(32, 38)
  list_ans = [True] * answers
  list_false = [False] * (40 - answers)
  combined_list = list_ans + list_false
  random.shuffle(combined_list)

  url = "http://127.0.0.1:5000/"
  driver = Chrome()
  db = Singleton()
  actions = ActionChains(driver)

  driver.get(url)

  email_element = driver.find_element(by=By.XPATH, value="/html/body/div/div/form/div[1]/input")
  password_element = driver.find_element(by=By.XPATH, value="/html/body/div/div/form/div[2]/input")

  email_element.send_keys(EMAIL)
  password_element.send_keys(PASSWORD)

  button = driver.find_element(by=By.XPATH, value="/html/body/div/div/form/button")
  button.click()

  for i in range(1,41):
    question = driver.find_element(by=By.XPATH, value=f"/html/body/div/form/div/div[{i}]/p")

    question_text = question.text
    if i < 10:
      question_text = question_text[2:]
    if i >= 10:
      question_text = question_text[3:]
    db_question = db.select_question_by_question(question_text)
    correct_answer_option = db_question[-1]
    possible_answers = db_question[2:]
    correct_answer = possible_answers[correct_answer_option-1]
    for x in range(1,5):
      answer = driver.find_element(by=By.XPATH, value=f"/html/body/div/form/div/div[{i}]/label[{x}]")
      actions.move_to_element(answer).perform()
      answer_text = answer.text[3:]
      if correct_answer == answer_text:
        check = combined_list.pop()
        if check:
          answer.click()
  submit_button = driver.find_element(by=By.XPATH, value="/html/body/div/form/button")
  actions.move_to_element(submit_button).perform()
  submit_button.click()
  time.sleep(5)
  driver.quit()

# 32-38
solve_quiz()
