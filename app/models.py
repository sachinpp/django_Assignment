
from django.db import models

class Contact(models.Model):
    FirstName=models.CharField(max_length=80)
    LastName=models.CharField(max_length=80)
    Email=models.CharField(max_length=100)
    Mobile=models.CharField(max_length=100)
    #Dob =models.DateTimeField()

    def __str__(self):
        return self.FirstName+" "+self.LastName
