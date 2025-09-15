import random


class Envelope:
    def __init__(self):
        self.amount = self._calc_money()

    money = []

    def _calc_money(self):
        while True:
            random_amount = random.randint(0, 1001)
            if random_amount not in self.money:
                self.money.append(random_amount)
                return random_amount

    def reveal(self):
        return self.amount
