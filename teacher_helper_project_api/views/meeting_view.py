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

    #get list of all meetings 
    def list(self, request):
        """Handle GET requests to meetings resource
        Returns:
            Response -- JSON serialized list of meetings
        """

        #get current user
        current_user = request.auth.user


        #get all Meetings 
        meetings = Meeting.objects.all()   
            


        #get all meetings with current user's pk as a foreign key
        if meetings is not None:
            current_user_meetings = meetings.filter(user_id=current_user)  # section in filter is (column in sql table :: what we're matching to in filter)


        #translate to JSON and respond to client side
        meetings_serializer = MeetingsSerializer(
            current_user_meetings, many=True, context={'request': request}) 

        return Response(meetings_serializer.data) 
    


    #get single meeting with students assigned to meeting
    def retrieve(self, request, pk=None):
        """Handle GET requests for single meeting
        Returns:
            Response -- JSON serialized meeting instance
        """
        try:
            #get current meeting using pk
            requested_meeting = Meeting.objects.get(pk=pk)

            #translate meeting JSON 
            meeting_serializer = MeetingsSerializer(
                requested_meeting, context={'request': request})

            
        
  

            return Response(meeting_serializer.data)
       
       
       
        except Exception as ex:  
            return HttpResponseServerError(ex)


#make serializer for students
class StudentsSerializer(serializers.ModelSerializer):
    """JSON serializer for students
    Arguments:
        serializer type
    """
    class Meta:
        model = Student
        fields = ('id', 'name')
        depth = 1


#make serializer for meetings
class MeetingsSerializer(serializers.ModelSerializer):
    """JSON serializer for meetings
    Arguments:
        serializer type
    """
  

    class Meta:
        model = Meeting
        fields = ('id', 'name', 'description', 'date', 'time', 'learners')
        depth = 1

