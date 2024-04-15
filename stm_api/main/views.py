from django.shortcuts import render

from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from . import models
from .serializers import TecherSerializer,CategorySerializer,StudentSerializer,CourseSerializer,ChapterSerializer,StudentCourseEnrollSerializer,CourseRatingSerializer,TeacherDashboardSerializer,StudentFavoriteCourseSerializer,StudentAssignmentSerializer,StudentDashboardSerializer,NotificationSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from rest_framework import status
from django.db.models import Q


class TeacherList(generics.ListCreateAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer
   #withour authenticate we can'nt able to see and do operations
   # permission_classes = [permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer
   # permission_classes = [permissions.IsAuthenticated]


class TeacherDashboard(generics.RetrieveAPIView):
   queryset = models.Teacher.objects.all()
   serializer_class=TeacherDashboardSerializer


class CategoryList(generics.ListCreateAPIView):
   queryset=models.CourseCategory.objects.all()
   serializer_class=CategorySerializer
   # permission_classes = [permissions.IsAuthenticated]

class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = models.Course.objects.all().order_by('-id')[:limit]

        elif 'category' in self.request.GET:
            category = self.request.GET['category']
            qs = models.Course.objects.filter(tech__icontains=category)

        elif 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name = self.request.GET['skill_name']
            teacher = self.request.GET['teacher']
            teacher = models.Teacher.objects.filter(id=teacher).first()
            qs = models.Course.objects.filter(techs__icontains=skill_name, teacher=teacher)

        elif 'studentId' in self.kwargs:
            student_id = self.kwargs['studentId']
            student = models.Student.objects.get(pk=student_id)
            queries = [Q(techs__icontains=value) for value in student.interested_categories]
            query = queries.pop()
            for item in queries:
                query |= item
            qs = models.Course.objects.filter(query)

        return qs
   # permission_classes = [permissions.IsAuthenticated]


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
# it responsible for handle frontened request means if login information is match then it response True otherwise False
def teacher_login(request):
   
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Filter teachers with matching email and password
        teacher_data = models.Teacher.objects.filter(email=email, password=password).first()

        if teacher_data:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})
   
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


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Student.objects.all()
   serializer_class=StudentSerializer


class TeacherDashboard(generics.RetrieveAPIView):
   queryset = models.Student.objects.all()
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
    
@csrf_exempt
def student_change_password(request,student_id):
 
    password=request.POST['password']
    try:
        studentData = models.Teacher.objects.get(id=student_id)
    except models.Student.DoesNotExist:
       studentData=None
    if studentData:
       models.Student.objects.filter(id=student_id).update(password=password)
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})
    

class StudentDashboard(generics.RetrieveAPIView):
   queryset = models.Student.objects.all()
   serializer_class=StudentDashboardSerializer
    
class StudentEnrollCourseList(generics.ListCreateAPIView):
   queryset=models.StudentCourseEnrollment.objects.all()
   serializer_class=StudentCourseEnrollSerializer


class StudentFavoriteCourseList(generics.ListCreateAPIView):
   queryset = models.StudentFavoriteCourse.objects.all()
   serializer_class = StudentFavoriteCourseSerializer

   def get_queryset(self):
    if 'student_id' in self.kwargs: 
       student_id=self.kwargs['student_id']
       student = models.Student.objects.get(pk=student_id)
       return models.StudentFavoriteCourse.objects.filter(student=student).distinct()

def fatch_enroll_status(request,student_id,course_id):
   student = models.Student.objects.filter(id=student_id).first()
   course = models.Course.objects.filter(id=course_id).first()
   enrollStatus = models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()
   if  enrollStatus:
      return JsonResponse({'bool':True})
   else:
      return JsonResponse({'bool':False})
   
def fatch_favorite_status(request,student_id,course_id):
   student=models.Student.objects.filter(id=student_id).first()
   course=models.Course.objects.filter(id=course_id).first()
   favoriteStatus=models.StudentFavoriteCourse.objects.filter(course=course,student=student).first()
   if favoriteStatus and favoriteStatus.status == True:
      return JsonResponse({'bool':True})
   else:
      return JsonResponse({'bool':False})
   
def fatch_favorite_status(request,student_id,course_id):
   student=models.Student.objects.filter(id=student_id).first()
   course=models.Course.objects.filter(id=course_id).first()
   favoriteStatus=models.StudentFavoriteCourse.objects.filter(course=course,student=student).first()
   if favoriteStatus and favoriteStatus.status == True:
      return JsonResponse({'bool':True})
   else:
      return JsonResponse({'bool':False})
  
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
def remove_favorite_course(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    favoriteStatus=models.StudentFavoriteCourse.objects.filter(course=course,student=student).delete()
    if favoriteStatus:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})
    

class EnrolledStudentList(generics.ListCreateAPIView):
   queryset=models.StudentCourseEnrollment.objects.all()
   serializer_class=StudentCourseEnrollSerializer

   def get_queryset(self):
    if 'course_id' in self.kwargs:   
        course_id = self.kwargs['course_id']
        course = models.Course.objects.get(pk=course_id)
        return models.StudentCourseEnrollment.objects.filter(course=course)
    elif 'teacher_id' in self.kwargs: 
       teacher_id=self.kwargs['teacher_id']
       teacher = models.Teacher.objects.get(pk=teacher_id)
       return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
    elif 'student_id' in self.kwargs: 
       student_id=self.kwargs['student_id']
       student = models.Student.objects.get(pk=student_id)
       return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
    
  

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
    


# it return us particular teacher and student assignment
class AssignmentList(generics.ListCreateAPIView):
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer

   def get_queryset(self):
        # Retrieve teacher ID from URL kwargs
    student_id = self.kwargs['student_id']
    teacher_id = self.kwargs['teacher_id']

        
        # Retrieve teacher object based on ID
    student = models.Student.objects.get(pk=student_id)
    teacher = models.Teacher.objects.get(pk=teacher_id)
        
        # Filter courses by teacher
    return models.StudentAssignment.objects.filter(student=student,teacher=teacher)
   
   
class MyAssignmentList(generics.ListCreateAPIView):
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer

   def get_queryset(self):
    student_id = self.kwargs['student_id']
    student = models.Student.objects.get(pk=student_id)
    return models.StudentAssignment.objects.filter(student=student)
   
class UpdateAssignmentList(generics.RetrieveDestroyAPIView):
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer

class NotificationList(generics.ListCreateAPIView):
   queryset=models.Notification.objects.all()
   serializer_class=NotificationSerializer

   def get_queryset(self):
      student_id=self.kwargs['student_id']
      student = models.Student.objects.get(pk=student_id)
      return models.Notification.objects.filter(student=student,notif_for='student',notif_subject='assignement',notifiread_status=False)