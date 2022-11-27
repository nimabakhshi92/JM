from django.db import models


class Narration(models.Model):
    narration_text = models.CharField(max_length=20000)
    # date = models.DateTimeField('date')


