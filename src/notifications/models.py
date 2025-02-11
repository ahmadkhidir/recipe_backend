from django.db import models


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        abstract = True


class GeneralNotification(Notification):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return self.title