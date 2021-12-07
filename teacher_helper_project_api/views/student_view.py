"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from teacher_helper_project_api.models import Student
from django.contrib.auth.models import User



class StudentView(ViewSet):  
    """Teacher Helper students on rosters"""

#get list of all students 
    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """

        #get current user
        current_user = request.auth.user


        #get all students, then get all students with current user's pk as a foreign key
        students = Student.objects.all()   
        if students is not None:
            current_user_students = students.filter(user_id=current_user)  # section in filter is (column in student table :: what we're matching to in filter)


        #translate to JSON and respond to client side
        students_serializer = StudentsSerializer(
            current_user_students, many=True, context={'request': request}) 

        return Response(students_serializer.data) 


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