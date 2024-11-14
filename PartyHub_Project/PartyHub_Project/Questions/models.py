from django.db import models
from django.contrib.auth import get_user_model


class Question(models.Model):
    party = models.ForeignKey('Party.Party', on_delete=models.CASCADE, related_name='questions')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.author} for {self.party}"


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')  # One-to-one relationship
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.author}"
