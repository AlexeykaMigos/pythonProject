from models import UsersAnswers
from tinydb import TinyDB, Query
from datetime import datetime

# db.drop_table('Users')


class DbConnection:
    def __init__(self):
        self.db = TinyDB('db.json', indent=4, separators=(',', ': '), ensure_ascii=False)
        self.questions = self.db.table('Questions')
        self.users_data = self.db.table('Users')
        self.query = Query()

    def insert_user(self, name: str, chat_id: int):

        new_user = UsersAnswers(
            LoadDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            Name=name,
            ChatId=chat_id,
            A_1=None,
            A_2=None,
            A_3=None,
            A_4=None,
            A_5=None,
            A_6=None,
            A_7=None,
            A_8=None,
            A_9=None,
            A_10=None,
            )

        self.users_data.insert(new_user)


    def add_answer(self, chat_id: int, question_id: int, answer: str):
        self.users_data.update({"A_" + str(question_id): answer}, self.query.ChatId == chat_id)

    def get_text_by_id(self, qid: int):
        text = self.questions.all()[qid]['text']
        return text
    def get_options_by_id(self, qid: int):
        options = self.questions.all()[qid]['options']
        return options
    def get_type_by_id(self, qid: int):
        type = self.questions.all()[qid]['type']
        return type

    def get_user_answers(self, chat_id: int):
        return self.users_data.search(self.query.ChatId == chat_id)


db = DbConnection()

print(len(db.questions.all()))
