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

from django.utils.decorators import method_decorator
from json.decoder import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from django.db.models import Q

# jwt--
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# import coustom permisttion
from .permission import TeacherStudent

# pagination class for pagination

# main
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class MyPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4



# Teacher-

# old-
# class TeacherList(APIView):
#     def get(self, request):
#         queryset = models.Teacher.objects.all()
#         serializer = TecherSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
        
#         print("this is data from forntend",request.data)
#         serializer = TecherSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#mt
class TeacherList(APIView):
    pagination_class = MyPagination  # Assuming MyPagination is your custom pagination class

    def get(self, request):
        if 'popular' in request.GET:
            # Custom SQL query to get teachers ordered by the popularity of their courses
            # main is our app name in that query
            sql = "SELECT *, COUNT(c.id) as total_course FROM main_teacher as t INNER JOIN main_course as c ON c.teacher_id=t.id GROUP BY t.id ORDER BY total_course desc"
            queryset = models.Teacher.objects.raw(sql)
        else:
            queryset = models.Teacher.objects.all()

        # Pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        
        serializer = TecherSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TecherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # change-
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

#mt
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

# @method_decorator(csrf_exempt, name='dispatch')

# change and will itself-
class teacher_login(APIView):
    def post(self, request):
     
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print("this is teacher data",request.body)
            # print(email, password)
            
            try:
                teacher_data = models.Teacher.objects.filter(email=email, password=password).first()
            except ObjectDoesNotExist:
                teacher_data = None

            if teacher_data:
                if not teacher_data.verify_status:
                    return JsonResponse({'bool': False, 'msg': 'Accuount is not verified'})
                else:
                    token = get_tokens_for_user(teacher_data)
                    return JsonResponse({'token':token,'bool': True, 'teacher_id': teacher_data.id})
            else:
                return JsonResponse({'bool': False,'msg':'Invalied Email or password'})
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    def get(self, request):
        return JsonResponse({'error': 'GET method not allowed'}, status=405)
    
     
class verify_teacher_via_otp(APIView):
    def post(self, request, teacher_id):
        otp_digit = request.data.get('otp_digit')
        print(otp_digit)  # Using request.data for POST data
        verify = models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).first()
        if verify:
            models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).update(verify_status=True)
            return JsonResponse({'bool': True, 'teacher_id': verify.id})
        else:
            return JsonResponse({'bool': False})

class CategoryList(generics.ListCreateAPIView):
   queryset=models.CourseCategory.objects.all()
   serializer_class=CategorySerializer
#    pagination_class = MyPagination
   # permission_classes = [permissions.IsAuthenticated]

class CourseList(APIView):
   #  permission_classes=[TeacherStudent]
    pagination_class = MyPagination
    def get(self, request):
        print("This is kwargs",request.GET.get('role'))
        queryset = self.get_queryset()
        # new update-
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        #
        serializer = CourseSerializer(page, many=True)
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    def get_queryset(self):
        queryset = models.Course.objects.all()
        # Filter by 'result' query parameter
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            queryset = queryset.order_by('-id')[:limit]
        # Filter by 'category' query parameter
        elif 'category' in self.request.GET:
            print("this is link",self.request)
            category = self.request.GET['category']
            queryset = models.Course.objects.filter(techs__icontains=category)
            return queryset
        elif 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name = self.request.GET['skill_name']
            teacher = self.request.GET['teacher']
            teacher = models.Teacher.objects.filter(id=teacher).first()
            queryset = models.Course.objects.filter(techs__icontains=skill_name,teacher=teacher)
        elif 'searchString' in self.request.GET:
            search = self.request.GET['searchString']
            queryset = models.Course.objects.filter(Q(techs__icontains=search)|Q(title__icontains=search))
        elif 'studentId' in self.request.GET:
           student_id=self.request.GET['studentId']
           student = models.Student.objects.get(pk=student_id)
           print("this is student id ;;;;;;;",student)
           queries=[Q(techs__iendwith=value) for value in student.interested_categories]
           query=queries.pop()
           for item in queries:
              query |= item
           qs = models.Course.objects.filter(query)
           return qs
        return queryset   
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CourseList(APIView):
#     def get(self, request):
#         queryset = models.Course.objects.all()
#         serializer = CourseSerializer(queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#       #   print("this is data from forntend",request.data)
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def get_queryset(self):
#         qs = super().get_queryset()
#         if 'result' in self.request.GET:
#             limit = int(self.request.GET['result'])
#             qs = models.Course.objects.all().order_by('-id')[:limit]
#             # if category exits in our url then we will filter the data and return the data ---
#         elif 'category' in self.request.GET:
#             category = self.request.GET['category']
#             category = models.CourseCategory.objects.filter(id=category).first()
#             qs = models.Course.objects.filter(category=category)
# change---
# class CourseList(generics.ListCreateAPIView):
#     queryset = models.Course.objects.all()
#     serializer_class = CourseSerializer

   ##  for pagination-
#     pagination_class=StandardResultsSetPagination

#     def get_queryset(self):
#         qs = super().get_queryset()
#         if 'result' in self.request.GET:
#             limit = int(self.request.GET['result'])
#             qs = models.Course.objects.all().order_by('-id')[:limit]



#         elif 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
#             skill_name = self.request.GET['skill_name']
#             teacher = self.request.GET['teacher']
#             teacher = models.Teacher.objects.filter(id=teacher).first()
#             qs = models.Course.objects.filter(techs__icontains=skill_name, teacher=teacher)
# # search according title in serach bar
#         elif 'searchstring' in self.kwargs:
#             search = self.kwargs['searchstring']
#             qs = models.Course.objects.filter(Q(title__icontains=search)|Q(techs__icontains=search))

#         elif 'studentId' in self.kwargs:
#             student_id = self.kwargs['studentId']
#             student = models.Student.objects.get(pk=student_id)
#             queries = [Q(techs__icontains=value) for value in student.interested_categories]
#             query = queries.pop()
#             for item in queries:
#                 query |= item
#             qs = models.Course.objects.filter(query)

#         return qs
   ##permission_classes = [permissions.IsAuthenticated]

class CourseDetailView(generics.RetrieveAPIView):
   queryset = models.Course.objects.all()
   serializer_class = CourseSerializer
#specific techer course-



class student_login(APIView):
    def post(self, request):

        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print("this is student data ",request.body)
         
            
            try:
                student_data = models.Student.objects.filter(email=email, password=password).first()
            except ObjectDoesNotExist:
                student_data = None

            if student_data:
                token = get_tokens_for_user(student_data)
                return JsonResponse({'token':token,'bool': True, 'student_id': student_data.id})
            else:
                return JsonResponse({'bool': False})
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    def get(self, request):
        return JsonResponse({'error': 'GET method not allowed'}, status=405)

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
    
#end Teacher
   

#Chapter -
class ChapterList(APIView):
    def get(self, request):
        queryset = models.Chapter.objects.all()
        serializer = ChapterSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        print("this is data from forntend",request.data)
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChapterDetailView(APIView):
    def get_object(self, pk):
        try:
            return models.Chapter.objects.get(pk=pk)
        except models.Chapter.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        chapter = self.get_object(pk)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        chapter = self.get_object(pk)
        serializer = ChapterSerializer(chapter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        print("this is my dat................................................................",request.body)
        chapter = self.get_object(pk)
        serializer = ChapterSerializer(chapter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        chapter = self.get_object(pk)
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   # def get_serializer_context(self):
   #    context=super().get_serializer_context()
   #    context['chapter_duration']=self.chapter_duration
   #    print('context__________')
   #    print(context)
   #    return context

class CourseChapterList(APIView):
    def get(self, request, course_id):
        try:
            chapters = models.Chapter.objects.filter(course_id=course_id)
            serializer = ChapterSerializer(chapters, many=True)
            return Response(serializer.data)
        except models.Chapter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, course_id):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course_id=course_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
# chapter end


# Student-
# class StudentList(generics.ListCreateAPIView):
#    queryset=models.Student.objects.all()
#    serializer_class=StudentSerializer
class StudentList(APIView):
    def get(self, request):
        queryset = models.Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("this is data from forntend",request.data)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Student.objects.all()
   serializer_class=StudentSerializer


# will-
# @csrf_exempt
# def student_login(request):
#     email=request.POST['email']
#     password=request.POST['password']
#     try:
#         studentData = models.Student.objects.get(email=email,password=password)
#     except models.Student.DoesNotExist:
#        studentData=None
#     if studentData:
#        return JsonResponse({'bool':True,'student_id':studentData.id})
#     else:
#        return JsonResponse({'bool':False})

#mt 
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

# end Student


#study material
class StudyMaterialList(generics.ListCreateAPIView):
   serializer_class = StudyMaterialSerializer

   def get_queryset(self):
    course_id = self.kwargs['course_id']
    course = models.Course.objects.get(pk=course_id)
    return models.StudyMaterial.objects.filter(course=course)
   
class StudyMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = models.StudyMaterial.objects.all()
   serializer_class = StudyMaterialSerializer

#end study material


# instead below-
# def fatch_enroll_status(request,student_id,course_id):
#    student = models.Student.objects.filter(id=student_id).first()
#    course = models.Course.objects.filter(id=course_id).first()
#    enrollStatus = models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()
#    if  enrollStatus:
#       return JsonResponse({'bool':True})
#    else:
#       return JsonResponse({'bool':False})
   
class fatch_enroll_status(APIView):
    def get(self, request, student_id, course_id, *args, **kwargs):
        student = models.Student.objects.filter(id=student_id).first()
        course = models.Course.objects.filter(id=course_id).first()
        enroll_status = models.StudentCourseEnrollment.objects.filter(course=course, student=student).count()
        
        if enroll_status:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
        
class fatch_rating_status(APIView):
    def get(self, request, student_id, course_id, *args, **kwargs):
        student = models.Student.objects.filter(id=student_id).first()
        course = models.Course.objects.filter(id=course_id).first()
        ratingStatus = models.CourseRating.objects.filter(course=course, student=student).count()
        
        if ratingStatus:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
   
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
  
# @csrf_exempt
# def fatch_enroll_status(request,student_id,course_id):
#     student = models.Student.objects.filter(id=student_id).first()
#     course = models.Course.objects.filter(id=course_id).first()
#     enrollStatus=models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()
#     if enrollStatus:
#        return JsonResponse({'bool':True})
#     else:
#        return JsonResponse({'bool':False})
    
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
   pagination_class= MyPagination
   queryset=models.CourseRating.objects.all()
   serializer_class=CourseRatingSerializer

   # def get_queryset(self):
   #    course_id = self.kwargs['course_id']
   #    course = models.Course.objects.get(pk=course_id)
   #    return models.CourseRating.objects.filter(course=course)

   def get_queryset(self):
      if 'popular' in self.request.GET:
         sql = "SELECT * ,AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc LIMIT 4"
         return models.CourseRating.objects.raw(sql)
      if 'all' in self.request.GET:
         sql = "SELECT * ,AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
         return models.CourseRating.objects.raw(sql)
      return models.CourseRating.objects.filter(course__isnull=False).order_by('-rating')

   
def fatch_rating_status(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    ratingStatus=models.CourseRating.objects.filter(course=course,student=student).count()
    if ratingStatus:
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
    # Update notification-
    models.Notification.objects.filter(student=student,notif_for='student',notif_subject='assignment').update(notifiread_status=True)
    return models.StudentAssignment.objects.filter(student=student)
   
class UpdateAssignmentList(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer

class NotificationList(generics.ListCreateAPIView):
   queryset=models.Notification.objects.all()
   serializer_class=NotificationSerializer

   def get_queryset(self):
      student_id=self.kwargs['student_id']
      student = models.Student.objects.get(pk=student_id)
      return models.Notification.objects.filter(student=student,notif_for='student',notif_subject='assignment',notifiread_status=False)
   
   

def update_view(request,course_id):
   queryset=models.Course.objects.filter(pk=course_id).first()
   queryset.course_views+=1
   queryset.save()
   return JsonResponse({'views':queryset.course_views})

class FaqList(generics.ListAPIView):
   queryset=models.FAQ.objects.all()
   serializer_class=FaqSerializer

class FlatePageList(generics.ListAPIView):
   queryset = FlatPage.objects.all()
   serializer_class=FlatPagesSerializer

class FlatePageDetail(generics.RetrieveAPIView):
   queryset = FlatPage.objects.all()
   serializer_class=FlatPagesSerializer
   
class ContactList(generics.ListCreateAPIView):
   queryset=models.Contact.objects.all()
   serializer_class=ContactSerializer


# quiz-
class Quizlist(generics.ListCreateAPIView):
   queryset = models.Quiz.objects.all()
   serializer_class = QuizSerializer

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
   
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = models.Quiz.objects.all()
   serializer_class = QuizSerializer

class QuizQuestionList(generics.ListCreateAPIView):
   serializer_class = QuestionSerializer

   def get_queryset(self):
    quiz_id = self.kwargs['quiz_id']
    quiz = models.Quiz.objects.get(pk=quiz_id)
    if 'limit' in self.kwargs:
       return models.QuizQuestions.objects.filter(quiz=quiz).order_by('id')[:1]
    elif 'question_id' in self.kwargs:
      current_question=self.kwargs['question_id']
      return models.QuizQuestions.objects.filter(quiz=quiz,id__gt=current_question).order_by('id')[:1]
    else:
       return models.QuizQuestions.objects.filter(quiz=quiz)
   
class CourseQuizList(generics.ListCreateAPIView):
   queryset=models.CourseQuiz.objects.all()
   serializer_class=CourseQuizSerializer

   def get_queryset(self):
      if 'course_id' in self.kwargs:
         course_id = self.kwargs['course_id']
         course = models.Course.objects.get(pk=course_id)
         return models.CourseQuiz.objects.filter(course=course)

def fetch_quiz_assign_status(request,quiz_id,course_id):
   quiz = models.Quiz.objects.filter(id=quiz_id).first()
   course=models.Course.objects.filter(id=course_id).first()
   assignStatus = models.CourseQuiz.objects.filter(course=course,quiz=quiz).count()
   if assignStatus:
      return JsonResponse({'bool':True})
   else:
      return JsonResponse({'bool':False})
   
def fetch_quiz_result(request,quiz_id,student_id):
   quiz=models.Quiz.objects.filter(id=quiz_id).first()
   student=models.Student.objects.filter(id=student_id).first()
   total_questions=models.QuizQuestions.objects.filter(quiz=quiz).count()
   total_attempted_questions=models.AttempQuiz.objects.filter(quiz=quiz,student=student).values('student').count()
   attempted_questions=models.AttempQuiz.objects.filter(quiz=quiz,student=student)

   total_correct_questions=0
   for attempt in attempted_questions:
      if attempt.right_ans==attempt.question.right_ans:
         total_correct_questions+=1

   return JsonResponse({'total_questions':total_questions,'total_attempted_questions':total_attempted_questions,'total_correct_questions':total_correct_questions})
   
class AttemptQuizList(generics.ListCreateAPIView):
   queryset=models.AttempQuiz.objects.all()
   serializer_class=AttempQuizSerializer

   def get_queryset(self):
      if 'quiz_id' in self.kwargs:
         quiz_id = self.kwargs['quiz_id']
         quiz = models.Quiz.objects.get(pk=quiz_id)
         return models.AttempQuiz.objects.raw(f'SELECT * FROM main_attempquiz WHERE quiz_id={int(quiz_id)} GROUP by student_id')
      
def fetch_quiz_attempt_status(request,quiz_id,student_id):
   quiz=models.Quiz.objects.filter(id=quiz_id).first()
   student=models.Student.objects.filter(id=student_id).first()
   attemptStaus=models.AttempQuiz.objects.filter(student=student,question__quiz=quiz).count()
   if attemptStaus>0:
      return JsonResponse({'bool':True})
   else:
      return JsonResponse({'bool':False})
      
def fetch_quiz_attempt_status(request,quiz_id,student_id):
   quiz = models.Quiz.objects.filter(id=quiz_id).first()
   student=models.Student.objects.filter(id=student_id).first()
   attemptStatus = models.AttempQuiz.objects.filter(student=student,question__quiz=quiz).count()
   if attemptStatus > 0:
      return JsonResponse({'bool':True})
   else:
      return JsonResponse({'bool':False})
