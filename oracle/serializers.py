from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import JobApplication, Position, Feedback, ApplicantList

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'position')

class ApplicantAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantList
        fields = '__all__'

class ApplicantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantList
        fields = '__all__'
        depth = 1

class ApplicantStatusSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ApplicantList
        fields = ('id', 'name', 'status', 'applicant_email')

class ApplicantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantList
        fields = ('id', 'name', 'unique_id', 'status', 'submitted_date')



class JobApplicationSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    
    class Meta:
        model = JobApplication
        fields = ('id', 'name', 'position', 'status', 'applied_date')

class JobApplicationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('id', 'resume_copy', 'passport_ic_copy', 'highest_education_cert_copy', 'payslip_or_graduation_letter', 'recommendation_letter', 'portfolio_url')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'