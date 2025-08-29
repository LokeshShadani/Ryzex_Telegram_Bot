import requests
import html
import random

user_scores = {}

def get_trivia_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    data = requests.get(url).json()
    question_data = data["results"][0]
    question = html.unescape(question_data["question"])
    correct = html.unescape(question_data["correct_answer"])
    options = [html.unescape(opt) for opt in question_data["incorrect_answers"]] + [correct]
    random.shuffle(options)
    return {"question": question, "options": options, "correct": correct}
