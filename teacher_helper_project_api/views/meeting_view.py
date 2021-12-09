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

        #filter meetings to get all meetings belonging to current user
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


    #add new meeting
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized meeting instance
        """
        #specify current user
        current_user = request.auth.user 

       #set up new student object with user inputs
        try:
            new_meeting = Meeting.objects.create( 
                name=request.data["name"],  
                description=request.data["description"],  
                date=request.data["date"],  
                time=request.data["time"],  
                user=current_user
            )

            new_meeting.learners.set(request.data["learners"])  #hints- must be outside of the above because object must be made after look @ fixtures as syntax guide for building test object in postman


            #translate to JSON and respond to the client side
            meeting_serializer = MeetingsSerializer(new_meeting, context={'request': request})  
            
            return Response(meeting_serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


#delete single meeting
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single meeting
        Returns:
            Response -- 200, 404, or 500 status code
        """
        #identify meeting to delete by pk and call orm
        try:
            meeting_to_delete = Meeting.objects.get(pk=pk)
            meeting_to_delete.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        #send error statuses if method fails
        except student_to_delete.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#make serializer for students because meeting includes students (refer to meetings model 'learners')
class StudentsSerializer(serializers.ModelSerializer):
    """JSON serializer for students
    Arguments:
        serializer type
    """
    class Meta:
        model = Student
        fields = ('id', 'name')
        depth = 1



#make serializer for meetings and include the learners
class MeetingsSerializer(serializers.ModelSerializer):
    """JSON serializer for meetings
    Arguments:
        serializer type
    """
  
    class Meta:
        model = Meeting
        fields = ('id', 'name', 'description', 'date', 'time', 'learners')
        depth = 1

