class GoogleBookResponse:
    def __init__(self, response):
        self.response = response

    def json(self):
        return self.response
