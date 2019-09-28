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
            temp = answer.lower().strip()
            answer_array[index] = temp
        return answer_array

    def checkAnswer(self, answer):
        answers = self.transformAnswer()
        answer = answer.lower()
        for a in answers:
            if a == answer:
                return 1
        return 0
