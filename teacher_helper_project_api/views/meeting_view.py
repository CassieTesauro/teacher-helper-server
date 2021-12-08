from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from teacher_helper_project_api.models import Student
from teacher_helper_project_api.models import Meeting
from django.contrib.auth.models import User



class MeetingView(ViewSet):  
    """current user's meetings"""
    