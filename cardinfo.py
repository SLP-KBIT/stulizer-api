class CardInfo:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.balance = ""

    def get(self):
        return {
            "id": self.id,
            "name": self.name,
            "balance": self.balance,
        }

    def update(self, id, name, balance):
        self.id = id
        self.name = name
        self.balance = balance
