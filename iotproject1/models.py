from django.db import models


class Professor(models.Model):
    professor = models.CharField(max_length =200)
    email = models.EmailField()
    in_office = models.BooleanField()

class Student(models.Model):
    email = models.EmailField()
    date_time = models.DateTimeField()
    professor = models.ForeignKey(Professor,on_delete=models.CASCADE)

class ApptRequests(models.Model):
    professor= models.ForeignKey(Professor,on_delete=models.CASCADE)
    student= models.ForeignKey(Student,on_delete=models.CASCADE)
    def get_time(self):
        return self.student.date_time
