from django.db import models
from quiz.models.Round import Round


class Clue(models.Model):
    question = models.CharField(max_length=750)
    answer = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True)
    round = models.ForeignKey('Round', on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def transformAnswer(self):
        answer_array = self.answer.split(",")
        for index, answer in enumerate(answer_array):
            temp = answer.lower()
            temp = temp.strip()
            answer_array[index] = temp
        return answer_array

    def checkAnswer(self, answer):
        answers = self.transformAnswer()
        for a in answers:
            if a == answer:
                return True
        return False

    def getPosition(self):
        pos_arr = self.position.split(",")
        new_arr = [float(val) for val in pos_arr]
        return new_arr
