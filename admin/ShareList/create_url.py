class Url:
    def __init__(self):
        self.user_name = None
        self.question_id = None
        self.right_answer = None
        self.answer = None
        self.question = None
        self.url = None

    def link_component(self) -> str:
        # self.url = f'https://{self.user_name}/question={self.question}/answer={self.answer}/rightAnswer={self.right_answer}/question_id={self.question_id}'
        self.url = f'https://{self.user_name}/question={self.question}/answer={self.answer}/right_answer={self.right_answer}/question_id={self.question_id}'
        return self.url

    def create_url(self, question: str, answer: str | list[str], right_answer: str | list[str],
                   question_id: int, user_name: str = "default") -> str:
        self.user_name = user_name
        self.question = question
        self.answer = answer
        self.right_answer = right_answer

        self.question_id = question_id

        return self.link_component()
