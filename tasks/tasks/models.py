from django.db import models

class Task(models.Model):
    user_id = models.IntegerField()  # or UUIDField, depending on the user ID type in the users project
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
