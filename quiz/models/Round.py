from django.db import models


class Round(models.Model):
    round_number = models.IntegerField(default=1)
    question = models.CharField(max_length=750)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return str(self.round_number)

    def transformAnswer(self):
        answer_array = self.answer.split(",")
        for index, answer in enumerate(answer_array):
            temp = answer.lower()
            temp = temp.strip()
            answer_array[index] = temp
        return answer_array

    def checkAnswer(self, answer):
        answer = answer.lower()
        answers = self.transformAnswer()
        for a in answers:
            if a == answer:
                return True
        return False
