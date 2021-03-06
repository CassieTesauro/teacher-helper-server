"""View module for handling requests about students"""

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

#get single student
    def retrieve(self, request, pk=None):
        """Handle GET requests for single student
        Returns:
            Response -- JSON serialized student instance
        """
        try:
            #get current student using pk
            requested_student = Student.objects.get(pk=pk)

            #translate to JSON and respond to the client side
            serializer = StudentsSerializer(requested_student, context={'request': request})
            return Response(serializer.data)
       
        except Exception as ex:  
            return HttpResponseServerError(ex)

#add new student
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized student instance
        """
        #specify current user
        current_user = request.auth.user 

       #set up new student object with user inputs
        try:
            new_student = Student.objects.create( 
                name=request.data["name"],  
                user=current_user,
            )
         
            #translate to JSON and respond to the client side
            serializer = StudentsSerializer(new_student, context={'request': request})  
            
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

#delete single student
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single student
        Returns:
            Response -- 200, 404, or 500 status code
        """
        #identify student to delete by pk and call orm
        try:
            student_to_delete = Student.objects.get(pk=pk)
            student_to_delete.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        #send error statuses if method fails
        except student_to_delete.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#edit single student
    def update(self, request, pk=None):
        """Handle PUT requests for a student
        Returns:
            Response -- Empty body with 204 status code
        """

        #specify student to edit
        student_to_update = Student.objects.get(pk=pk)

        #update student info
        student_to_update.name = request.data["name"] 
        student_to_update.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


#make serializer for students
class StudentsSerializer(serializers.ModelSerializer):
    """JSON serializer for students
    Arguments:
        serializer type
    """
    class Meta:
        model = Student
        fields = ('id', 'name', 'user_id')
        depth = 1