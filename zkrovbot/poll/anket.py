from .config import questions
from dto.base import db
class Anket:
    def __init__(self, config):
        self.config = config
        self.length = len(config)
        self.answers = None
        self.scores = 0

    def add_answers(self, answers: list):
        print(f"Add_answers {answers}")
        self.scores = 0
        self.answers = answers
        self._counter()
        return self.scores

    def get_question(self, k):
      return db.get_text_by_id(k)




    def _counter(self):
        for i in range(self.length):
            qtype = db.get_type_by_id(i)
            qoptions =  db.get_options_by_id(i)
            qanswer = self.answers[i]
            print(f"i={i} {qanswer} {qtype}")
            if qtype == 'closed':
                if qanswer == 'Да':
                    self.scores += 1
                else:
                    self.scores += 0

            if qtype == 'multiple_choice':
                print(db.get_options_by_id(i).index(qanswer))
                self.scores += db.get_options_by_id(i).index(qanswer)
            if qtype == 'number':
                pass
            if qtype == 'opened':
                pass
        print(self.scores)

anket = Anket(questions)
