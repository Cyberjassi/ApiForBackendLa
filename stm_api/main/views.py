from django.shortcuts import render

from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from . import models
from .serializers import TecherSerializer,CategorySerializer,StudentSerializer,CourseSerializer,ChapterSerializer,CourseEnrollSerializer,CourseRatingSerializer
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
       return JsonResponse({'bool':True,'teacher_id':teacherData.id})
    else:
       return JsonResponse({'bool':False})
   
# class ChapterList(generics.ListCreateAPIView):
#    queryset = models.Chapter.objects.all()
#    serializer_class = ChapterSerializer

class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
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
   

class StudentList(generics.ListCreateAPIView):
   queryset=models.Student.objects.all()
   serializer_class=StudentSerializer


@csrf_exempt
def student_login(request):
    email=request.POST['email']
    password=request.POST['password']
    try:
        studentData = models.Student.objects.get(email=email,password=password)
    except models.Student.DoesNotExist:
       studentData=None
    if studentData:
       return JsonResponse({'bool':True,'student_id':studentData.id})
    else:
       return JsonResponse({'bool':False})
    
class StudentEnrollCourseList(generics.ListCreateAPIView):
   queryset=models.StudentCourseEnrollment.objects.all()
   serializer_class=CourseEnrollSerializer
  
@csrf_exempt
def fatch_enroll_status(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    enrollStatus=models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()
    if enrollStatus:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})
    
@csrf_exempt
def fatch_enrolled_students(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    enrollStatus=models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()
    if enrollStatus:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})
    

class EnrollStudentList(generics.ListCreateAPIView):
   queryset=models.StudentCourseEnrollment.objects.all()
   serializer_class=CourseEnrollSerializer

   def get_queryset(self):
       
    course_id = self.kwargs['course_id']
    course = models.Course.objects.get(pk=course_id)
    return models.StudentCourseEnrollment.objects.filter(course=course)
   

class CourseRatingList(generics.ListCreateAPIView):
   queryset=models.CourseRating.objects.all()
   serializer_class=CourseRatingSerializer

   
def fatch_rating_status(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    ratingStatus=models.CourseRating.objects.filter(course=course,student=student).count()
    if ratingStatus:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})