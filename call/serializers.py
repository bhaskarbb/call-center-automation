from rest_framework import serializers
from .models import Call, Transcript, Tone


class CallListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Call
		fields = ('id', 'timestamp', 'category', 'score')


class TranscriptSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transcript
		fields = ('text', 'is_employee')


class ToneSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tone
		fields = ('tone', 'score')


class CallSerializer(serializers.ModelSerializer):
	transcript = TranscriptSerializer(read_only=True, many=True)
	tones = ToneSerializer(read_only=True, many=True)

	class Meta:
		model = Call
		fields = ('id', 'timestamp', 'category', 'violations', 'sentiment', 'satisfaction', 'score', 'tones', 'transcript')


class ScoreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Call
		fields = ('timestamp', 'score')
