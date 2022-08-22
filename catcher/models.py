from django.db import models

class LogModel(models.Model): 
    typewh     = models.CharField(max_length=20)  
    origin     = models.CharField(max_length=30)
    operation  = models.CharField(max_length=40)
    payload    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
  
    def __str__(self) -> str:
        return self.operation