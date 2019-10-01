from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254)
    image = models.TextField(max_length=200)
    score = models.IntegerField(default=0)
    current_hints = models.CharField(max_length=200, blank=True)
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def getHints(self):
        if self.current_hints == '':
            return []
        else:
            return self.current_hints.split(',')

    def putClues(self, value):
        hints_arr = self.getHints()
        hints_arr.append(value)
        hints_str = [str(val) for val in hints_arr]
        self.current_hints = ','.join(hints_str)

    def checkClue(self, value):
        hints_arr = self.getHints()
        for hint in hints_arr:
            if value == int(hint):
                return 1
        return 0
