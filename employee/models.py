from django.db import models

# Create your models here.
class Employee(models.Model):
	genders = (
		('M', 'male'),
		('F', 'female')
	)
	name = models.CharField(max_length=64)
	gender = models.CharField(max_length=1, choices=genders)
	age = models.IntegerField()

	def __str__(self):
		return self.name



