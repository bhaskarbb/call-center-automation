from django.shortcuts import render
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response

from call.models import Call


class GetStats(APIView):

	def get(self, request):		

		scope = request.query_params.get('scope')
		employee_id = request.query_params.get('employee-id')
		print(employee_id)

		if employee_id:
			calls = Call.objects.filter(employee_id=employee_id)
		else:
			calls = Call.objects.all()

		if scope == 'today':
			calls = calls.filter(timestamp__date=date.today())
		elif scope == 'month':
			calls = calls.filter(timestamp__month=date.today().month)
		elif scope == 'year':
			calls = calls.filter(timestamp__year=date.today().year)

		response = {}
		response['total'] = calls.count()
		response['satisfied'] = calls.filter(satisfaction=True).count()
		response['unsatisfied'] = response['total'] - response['satisfied']
		response['score'] = Call.objects.all().aggregate(Avg('score'))['score__avg']		

		return Response(response)

	def post(self, request):
		pass