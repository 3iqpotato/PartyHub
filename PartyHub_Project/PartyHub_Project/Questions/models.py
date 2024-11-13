from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
# Ако създадете нов ап 'questions'

class Question(models.Model):
    party = models.ForeignKey('Party.Party', on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user} for {self.party}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.user}"
