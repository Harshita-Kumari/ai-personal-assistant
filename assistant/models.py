# from django.db import models

# class ChatHistory(models.Model):
#     user_message = models.TextField()
#     ai_response = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user_message[:50]
    

# from django.db import models
# from django.contrib.auth.models import User

# class Conversation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255, default="New Chat")
#     created_at = models.DateTimeField(auto_now_add=True)

# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
#     role = models.CharField(max_length=10)  # user / assistant
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role}: {self.content[:30]}"