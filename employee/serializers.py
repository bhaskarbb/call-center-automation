from rest_framework import serializers
from .models import Employee
from call.serializers import CallListSerializer


class EmployeeListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = ('id', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
	calls = CallListSerializer(read_only=True, many=True)

	class Meta:
		model = Employee
		fields = ('id', 'name', 'gender', 'age', 'calls')

