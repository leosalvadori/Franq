from django.db import models
  
class AuthModel(models.Model):
    access_token = models.CharField(max_length=2000)
    expires_in = models.IntegerField()
    refresh_token = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self) -> str:
        return self.access_token