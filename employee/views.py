from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import EmployeeListSerializer, EmployeeSerializer
from call.serializers import ScoreSerializer
from .models import Employee
from call.models import Call

# Create your views here.


class GetEmployeeList(APIView):
	''' Get list of all employees '''

	def get(self, request):		

		employees = Employee.objects.all()
		employee_serializer = EmployeeListSerializer(employees, many=True)
		return Response(employee_serializer.data)

	def post(self, request):
		pass


class GetEmployee(APIView):
	''' Get details of an employee.'''

	def get(self, request):		

		employee_id = request.query_params.get('employee-id')
		employee = get_object_or_404(Employee, id=employee_id)
		employee_serializer = EmployeeSerializer(employee)
		return Response(employee_serializer.data)

	def post(self, request):
		pass


class GetScore(APIView):

	def get(self, request):		

		employee_id = request.query_params.get('employee-id')
		scope = request.query_params.get('scope')
		scores = Call.objects.filter(employee_id=employee_id)

		if scope == 'today':
			scores = scroes.filter(timestamp__date=date.today())
		elif scope == 'month':
			scores = scroes.filter(timestamp__month=date.today().month)
		elif scope == 'year':
			scores = scroes.filter(timestamp__year=date.today().year)

		score_serializer = ScoreSerializer(scores, many=True)
		return Response(score_serializer.data)

	def post(self, request):
		pass

