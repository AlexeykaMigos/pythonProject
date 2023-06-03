from models import UsersAnswers
from tinydb import TinyDB, Query
from datetime import datetime
from poll.anket import *
# db.drop_table('Users')


class DbConnection:
    def __init__(self):
        self.db = TinyDB('db.json', indent=4, separators=(',', ': '), ensure_ascii=False)
        self.db = TinyDB('db.json')
        self.questions = self.db.table('Questions')
        self.users_data = self.db.table('Users')
        self.query = Query()

    def insert_user(self, name: str, chat_id: int,
                     answers: list ):
        new_user = UsersAnswers(
            LoadDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            Name=name,
            ChatId=chat_id,
            A_0=answers[1],
            A_1=answers[2],
            A_2=answers[3],
            A_3=answers[4],
            A_4=answers[5],
            A_5=answers[6],
            A_6=answers[7],
            A_7=answers[8],
            A_8=answers[9],
            A_9=answers[10],
            A_10=None,)

        self.users_data.insert(new_user)


    def add_answer(self, chat_id: int, question_id: int, answer: str):
        self.users_data.update({"A_" + str(question_id): answer}, self.query.ChatId == chat_id)

    def get_question_by_id(self, qid: int):
        text = self.questions.all()[qid]['text']
        options = self.questions.all()[qid]['options']
        return text, options

    def get_user_answers(self, chat_id: int):
        return self.users_data.search(self.query.ChatId == chat_id)


db = DbConnection()

print(len(db.questions.all()))

# users_data
# add_answer(chat_id=1232, question_id=1, answer='sometext')

# print(get_user_answers(1232))
# print(users_data.all())
# print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))