from django.db import models
   
class States(models.Model):
    name = models.CharField(max_length=100)
    abv = models.CharField(max_length=100, default='default')
    
    def __str__(self):
        return self.name

class Activities(models.Model):
    name = models.CharField(max_length=100)
    abv = models.CharField(max_length=100, default='default')
    
    def __str__(self):
        return self.name