from django.db import models

# Create your models here.

class ProblemReport(models.Model):
    reporter_id = models.CharField(max_length=50, default='0', null=False)
    locate = models.CharField(max_length=20, null=False)
    equipment = models.CharField(max_length=50, null=False)
    equipment_location=models.CharField(max_length=10, null=False)
    problem_descript = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.user_id
