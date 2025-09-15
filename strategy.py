import random
from abc import ABC, abstractmethod
from envelope import Envelope


class Strategy(ABC):
    @abstractmethod
    def __init__(self, envelopes):
        self.envelopes = envelopes

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    #  לא מצויין בתרשים המחלקות אבל משתמשים בו בקוד הנתון
    def display(self):
        print("The strategy method: ")


class RandomStrategy(Strategy):
    def __init__(self, envelopes):
        self.envelopes = envelopes
        self.rng = random.randrange(len(envelopes))

    def play(self):
        """

        :return: מכיוון והמשתמש בוחר את המעטפות בסדר זהה ואין לו דרך לחזור אחורה, נחזיר רק את המעטפה האחרונה שיפתח וכמה מעטפות כביכול נפתחו
        """
        return self.envelopes[self.rng - 1], self.rng

    def display(self):
        super().display()
        print("random envelope to open")

    pass


class StopAfterNOpensStrategy(Strategy):
    def __init__(self, envelopes):
        self.envelopes = envelopes
        self.N = 1

    def play(self):
        """

        :return: נפתח מעטפות ברנדומליות N פעמים ונחזיר את המעטפה האחרונה
        """
        # נסמן את המעטפות שנפתחו ב-1 כדי לדעת לא לפתוח אותן שוב
        open_envelopes = [0]*len(self.envelopes)
        for i in range(self.N):
            env_number = random.randint(0, len(self.envelopes))
            if open_envelopes[env_number] == 1:
                i -= 1
            else:
                open_envelopes[env_number] = 1
        return self.envelopes[env_number], self.N

    def display(self):
        super().display()
        print("stop after n open envelopes")


class BetterThanPercentStrategy(Strategy):
    def __init__(self, envelopes, percent):
        self.envelopes = envelopes
        self.percent = percent

    def play(self):
        """
        הפונקציה תעבור על האחוזים הראשונים ומוצאת את המקסימום בניהם.
        :return: המעטפה הראשונה עם הסכום שגדול מסכום המקסימום של המעטפות הראשונות. אם אין, נחזיר את המעטפה האחרונה.
        """
        amount_of_envelopes_to_open = int(len(self.envelopes) / self.percent)
        maximum = self.envelopes[0].reveal()
        percent_index = 0
        # מציאת המקסימום באחוזים הראשונים
        for i in range(amount_of_envelopes_to_open):
            if self.envelopes[i].reveal() > maximum:
                maximum = self.envelopes[i].reveal()
            percent_index = i
        max_index = 0
        for i in range(amount_of_envelopes_to_open, len(self.envelopes)):
            if self.envelopes[i].reveal() > maximum:
                return self.envelopes[i]
            max_index = i
        # אם הגענו לאחרון וגם הוא לא עקף את המקסימום
        return self.envelopes[len(self.envelopes)-1], percent_index + max_index + 1

    def display(self):
        super().display()
        print("better than n percent")
    pass


class MaxAfterNStrategy(Strategy):
    def __init__(self, envelopes, n=3):
        self.envelopes = envelopes
        self.N = n

    def play(self):
        """
        נעבור על המעטפות ונחפש כל פעם מקסימום עד שנגיע ל-N מקסימום שמצאנו.
        :return: המעטפה עם סכום הכסף המקסימלי ה-N
        """
        maximum = self.envelopes.reveal()
        amount_of_max = 1
        open_envelopes = 0
        for i in range(len(self.envelopes)):
            money = self.envelopes[i].reveal()
            if money >= maximum:
                amount_of_max += 1
                maximum = money
                if amount_of_max == self.N:
                    return self.envelopes[i]
            open_envelopes = i
        return self.envelopes[len(self.envelopes) - 1], open_envelopes + 1

    def display(self):
        super().display()
        print("max after n")
