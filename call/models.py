from django.db import models
from employee.models import Employee

# Create your models here.

class Call(models.Model):

	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='calls')
	category = models.CharField(max_length=32)
	score = models.IntegerField()
	violations = models.IntegerField()
	sentiment = models.FloatField()
	satisfaction = models.BooleanField()
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} - {}'.format(self.id, self.employee)


class Transcript(models.Model):

	call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='transcript')
	text = models.CharField(max_length=512)
	is_employee = models.BooleanField()

	def __str__(self):
		return '{} - {}'.format(self.call, self.text)


class Tone(models.Model):

	call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='tones')
	tone = models.CharField(max_length=32)
	score = models.FloatField()

	def __str__(self):
		return '{} - {}'.format(self.tone, self.call)

