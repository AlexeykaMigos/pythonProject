from .config import questions
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

    def get_question(self,k):
      return self.config[k].get('text')

    def _counter(self):
        for i in range(self.length):
            qtype = self.config[i].get('type')
            qoptions =  self.config[i].get('options')
            qanswer = self.answers[i]
            print(f"i={i} {qanswer} {qtype}")
            if qtype == 'closed':
                self.scores += 1 if qanswer == 'Да' else 0
            if qtype == 'multiple_choice':
                # print("Score for q: ", questions[i]['options'].index(qanswer))
                self.scores += questions[i]['options'].index(qanswer)
            if qtype == 'number':

                pass
            if qtype == 'opened':

                pass
        print(self.scores)

anket = Anket(questions)
