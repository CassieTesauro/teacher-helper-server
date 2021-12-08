"""View module for handling requests about meetings"""

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

    #get list of all students 
    def list(self, request):
        """Handle GET requests to meetings resource
        Returns:
            Response -- JSON serialized list of meetings
        """

        #get current user
        current_user = request.auth.user


        #get all Meetings, then get all meetings with current user's pk as a foreign key
        meetings = Meeting.objects.all()   
        if meetings is not None:
            current_user_meetings = meetings.filter(user_id=current_user)  # section in filter is (column in student table :: what we're matching to in filter)


        #translate to JSON and respond to client side
        meetings_serializer = MeetingsSerializer(
            current_user_meetings, many=True, context={'request': request}) 

        return Response(meetings_serializer.data) 


#make serializer for meetings
class MeetingsSerializer(serializers.ModelSerializer):
    """JSON serializer for meetings
    Arguments:
        serializer type
    """
    class Meta:
        model = Meeting
        fields = ('id', 'name', 'description', 'date', 'time')
        depth = 1