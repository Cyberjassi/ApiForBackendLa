from django.shortcuts import render
from django.contrib.flatpages.models import FlatPage

from django.http import Http404, JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from . import models
from .serializers import TecherSerializer,CategorySerializer,StudentSerializer,CourseSerializer,ChapterSerializer,StudentCourseEnrollSerializer,CourseRatingSerializer,TeacherDashboardSerializer,StudentFavoriteCourseSerializer,StudentAssignmentSerializer,StudentDashboardSerializer,NotificationSerializer,QuizSerializer,QuestionSerializer,CourseQuizSerializer,AttempQuizSerializer,StudyMaterialSerializer,FaqSerializer,FlatPagesSerializer,ContactSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
import json
from rest_framework.exceptions import AuthenticationFailed


from json.decoder import JSONDecodeError


from rest_framework import status
from django.db.models import Q



class TeacherList(APIView):
    def get(self, request):
        queryset = models.Teacher.objects.all()
        serializer = TecherSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        print("this is data from forntend",request.data)
        serializer = TecherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# change-
# class TeacherList(generics.ListCreateAPIView):
#    queryset=models.Teacher.objects.all()
#    serializer_class=TecherSerializer
   #withour authenticate we can'nt able to see and do operations
   # permission_classes = [permissions.IsAuthenticated]
   
   #Will---
   # def get_queryset(self):
   #    if 'popular' in self.request.GET:
   #       sql="SELECT *,COUNT(c.id) as total_course FROM main_teacher as t INNER JOIN main_course as c ON c.teacher_id=t.id GROUP BY t.id ORDER BY total_course desc"
   #       return models.Teacher.objects.raw(sql)
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer
   # permission_classes = [permissions.IsAuthenticated]


class TeacherDashboard(generics.RetrieveAPIView):
   queryset = models.Teacher.objects.all()
   serializer_class=TeacherDashboardSerializer


class TeacherCourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
   #  it is use for overide course so that we car retriewe specific course according to teacher id
    def get_queryset(self):
        # Retrieve teacher ID from URL kwargs
        teacher_id = self.kwargs['teacher_id']
        
        # Retrieve teacher object based on ID
        teacher = models.Teacher.objects.get(pk=teacher_id)
        
        # Filter courses by teacher
        return models.Course.objects.filter(teacher=teacher)

#through that teacher can do curd

class TeacherCourseDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Course.objects.get(pk=pk)
        except models.Course.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# will-
# class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Course.objects.all()
#     serializer_class = CourseSerializer
   


# it responsible for handle frontened request means if login information is match then it response True otherwise False

@csrf_exempt
def teacher_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print(request.body)
            print(email, password)
            
            try:
                teacher_data = models.Teacher.objects.filter(email=email, password=password).first()
            except models.Teacher.DoesNotExist:
                teacher_data = None

            if teacher_data:
                return JsonResponse({'bool': True,'teacher_id':teacher_data.id})
            else:
                return JsonResponse({'bool': False})
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


# will---
      #   email = request.POST.get('email')
      #   password = request.POST.get('password')
        # Filter teachers with matching email and password
      #   try:
      #       teacherData = models.Teacher.objects.filter(email=email, password=password,verify_status=True).first()
      #   except models.Teacher.DoesNotExist:
      #      teacherData=None
      #   if teacherData:
      #       if not teacherData.verify_status:
      #          return JsonResponse({'bool': False,'teacher_id':teacherData.id,'msg':'Account is not verified!!'})
      #       else:
      #          return JsonResponse({'bool': True,'teacher_id':teacherData.id})
      #   else:
      #       return JsonResponse({'bool':False,'msg':'Invalid Email or Password!!!'})
        
@csrf_exempt       
def verify_teacher_via_otp(request,teacher_id):
   otp_digit=request.POST.get('otp_digit')
   verify = models.Teacher.objects.filter(id=teacher_id,otp_digit=otp_digit).first()
   if verify:
      models.Teacher.objects.filter(id=teacher_id,otp_digit=otp_digit).update(verify_status=True)
      return JsonResponse({'bool':True,'teacher_id':verify.id})
   else:
      return JsonResponse({'bool':False})
    

@csrf_exempt
def teacher_change_password(request,teacher_id):
 
    password=request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(id=teacher_id)
    except models.Teacher.DoesNotExist:
       teacherData=None
    if teacherData:
       models.Teacher.objects.filter(id=teacher_id).update(password=password)
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})

class TeacherQuizList(generics.ListCreateAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        # Retrieve teacher ID from URL kwargs
        teacher_id = self.kwargs['teacher_id']
        
        # Retrieve teacher object based on ID
        teacher = models.Teacher.objects.get(pk=teacher_id)
        
        # Filter courses by teacher
        return models.Quiz.objects.filter(teacher=teacher)


class TeacherQuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer