from django.shortcuts import render,  HttpResponse, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Call, Transcript, Tone
from .serializers import CallSerializer

from watson_developer_cloud import ToneAnalyzerV3
from textblob import TextBlob
import apiai
import requests 
import json
import re

ai = apiai.ApiAI("5024b204fe004def95ee70793929c0f0")


class GetCall(APIView):

	def get(self, request):	

		call_id = request.query_params.get('call-id')
		call = get_object_or_404(Call, id=call_id)
		call_serializer = CallSerializer(call)
		return Response(call_serializer.data)

	def post(self, request):
		pass


# Create your views here.

def upload_call(request):
	audio_path = 'media/audio.mp3'
	employee_id = 1

	response = speech_to_text(audio_path)
	employee_text, caller_text, transcript = seperate_speakers(response)

	call_id = analyse_call(employee_id, employee_text, caller_text)

	save_transcript(transcript, call_id)
	analyse_tone(employee_text, call_id)

	return HttpResponse('Hello')


def speech_to_text(audio_path):
	''' converts audio file to text using ibm watsom api '''

	url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_NarrowbandModel&speaker_labels=true' 
	username = "dfa46e5a-c8d9-4de7-bff7-1354b80ae0e7"
	password = "bJbZkjlXAMFm"

	headers={'Content-Type': 'audio/mp3'} 
	audio = open(audio_path, 'rb') 

	response = requests.post(url, data=audio, headers=headers, auth=(username, password)).text
	return json.loads(response)


def seperate_speakers(response):
	''' seperates employee and speaker text and creates the transcript of the conversation '''

	speaker1 = []
	speaker2 = []
	transcript = []

	index = 0
	employee_num = 0
	for sent in response['results']:
	    text = sent['alternatives'][0]['transcript']
	    temp = {'text': text}

	    if response['speaker_labels'][index]['speaker'] == 1:
	        speaker1.append(text)
	        if employee_num == 0:
	            employee_num = 1

	        temp['is_employee'] = employee_num == 1

	    else:
	        speaker2.append(text)
	        if employee_num == 0:
	            employee_num = 2

	        temp['is_employee'] = employee_num != 1
	    
	    transcript.append(temp)

	    index += len(sent['alternatives'][0]['timestamps'])

	if employee_num == 1:
		return speaker1, speaker2, transcript
	else:
		return speaker2, speaker1, transcript


def save_transcript(transcript, call_id):
	''' saves the entire transcript of a call '''
	transcript_rows = (Transcript(call_id=call_id, text=i['text'], is_employee=i['is_employee']) for i in transcript)
	Transcript.objects.bulk_create(transcript_rows)


def analyse_call(employee_id, employee_text, caller_text):
	''' analyses violations, sentiment, category, satisfaction, score, tone and saves the result in db '''
	violations = count_violations(employee_text)
	sentiment = detect_sentiment(employee_text, caller_text)

	intents = get_intents(caller_text)
	category = get_category(intents)
	satisfaction = check_satisfaction(intents[-5:])

	score = calculate_score(violations, sentiment, satisfaction)

	call = Call.objects.create(
		employee_id=employee_id, 
		violations=violations, 
		sentiment=sentiment, 
		category=category, 
		satisfaction=satisfaction, 
		score=score
	)
	return call.id


def analyse_tone(employee_text, call_id):
	''' Finds out overall employee tone in the call and stores it in the db'''
	tone_analyzer = ToneAnalyzerV3(
	  version='2017-09-21',
	  username= "623777be-d95a-4ed5-9a62-376d03213f94",
	  password="qDmTyItpqd5v"
	)
	response = tone_analyzer.tone({'text' : '. '.join(employee_text)})

	tone_rows = (Tone(call_id=call_id, tone=i['tone_id'], score=i['score']) for i in response['document_tone']['tones'])
	Tone.objects.bulk_create(tone_rows)



def count_violations(employee_text):
	''' Counts number of curse words in the conversation '''

	curse_words = ('some', 'one')
	violations = 0
	text = ' '.join(employee_text)

	for word in curse_words:
 		violations += sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), text))

	return violations



def get_intents(caller_text):
    ''' Returns list of intents '''

    intents = []
    for text in caller_text:
        request = ai.text_request()
        request.query = text
        response = json.loads(request.getresponse().read().decode('utf-8'))
        try:
            intent = response['result']['metadata']['intentName']
            intents.append(intent)
        except:
            continue
    return intents


def get_category(intents):
	''' Returns the intent/category of the call '''
	categories = ('Schedule Meeting', 'Dance')
	for intent in intents:
		if intent in categories:
			return intent

	return 'unknown'


def check_satisfaction(intents):
	''' Checks if the user is satisfied from the last 3 intents'''

	return 'satisfaction' in intents


def detect_sentiment(employee_text, caller_text):
	''' Returns the overall sentiment of the conversation '''

	conversation = employee_text + caller_text
	sentiment = 0 

	for text in conversation:
		sentiment += TextBlob(text).sentiment.polarity

	return sentiment/len(conversation)


######### INCOMPLETE #############
def calculate_score(violations, sentiment, satisfaction):
	''' Calculates and returns overall score out of 100 of the call '''

	score = 0
	return score




'''

call to text
seperate voices
detect category
detect sentiment
overall score
violations
'''