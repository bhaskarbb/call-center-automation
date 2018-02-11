from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response

from call.models import Call
from call.serializers import ScoreSerializer


class GetStats(APIView):

	def get(self, request):		

		scope = request.query_params.get('scope')
		employee_id = request.query_params.get('employee-id')

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


class GetTopEmployees(APIView):

	def get(self, request):		
		calls = Call.objects.values('employee_id').annotate(avg_score=Avg('score')).order_by('-avg_score')[:5]
		response = list(calls)
		return JsonResponse(response, safe=False)

	def post(self, request):
		pass



class GetScore(APIView):
	
	def get(self, request):		

		scope = request.query_params.get('scope')
		scores = Call.objects.all()

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
