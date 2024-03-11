from django.shortcuts import render

from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from . import models
from .serializers import TecherSerializer,CategorySerializer,CourseSerializer,ChapterSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

class TeacherList(generics.ListCreateAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer
   #withour authenticate we can'nt able to see and do operations
   permission_classes = [permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer
   permission_classes = [permissions.IsAuthenticated]


class CategoryList(generics.ListCreateAPIView):
   queryset=models.CourseCategory.objects.all()
   serializer_class=CourseSerializer
   permission_classes = [permissions.IsAuthenticated]

class CourseList(generics.ListCreateAPIView):
   queryset=models.Course.objects.all()
   serializer_class=CourseSerializer
   permission_classes = [permissions.IsAuthenticated]


#specific techer course-
class TeacherCourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        # Retrieve teacher ID from URL kwargs
        teacher_id = self.kwargs['teacher_id']
        
        # Retrieve teacher object based on ID
        teacher = models.Teacher.objects.get(pk=teacher_id)
        
        # Filter courses by teacher
        return models.Course.objects.filter(teacher=teacher)

#through that teacher can do curd
class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
   

@csrf_exempt
def teacher_login(request):
    email=request.POST['email']
    password=request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(email=email,password=password)
    except models.Teacher.DoesNotExist:
       teacherData=None
    if teacherData:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})
   
class ChapterList(generics.ListCreateAPIView):
   queryset = models.Chapter.objects.all()
   serializer_class = ChapterSerializer


class CourseChapterList(generics.ListCreateAPIView):
   serializer_class = ChapterSerializer

   def get_queryset(self):
        # Retrieve teacher ID from URL kwargs
    course_id = self.kwargs['course_id']
        
        # Retrieve teacher object based on ID
    course = models.Course.objects.get(pk=course_id)
        
        # Filter courses by teacher
    return models.Chapter.objects.filter(course=course)