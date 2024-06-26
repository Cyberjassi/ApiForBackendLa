from django.shortcuts import render
from django.contrib.flatpages.models import FlatPage
from django.http import Http404, JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from . import models
from .serializers import TecherSerializer,CategorySerializer,StudentSerializer,CourseSerializer,ChapterSerializer,StudentCourseEnrollSerializer,CourseRatingSerializer,TeacherDashboardSerializer,StudentFavoriteCourseSerializer,StudentAssignmentSerializer,StudentDashboardSerializer,NotificationSerializer,StudyMaterialSerializer,FaqSerializer,FlatPagesSerializer,ContactSerializer,TeacherStudentChatSerializer
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
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .permission import Teacher,Student


#Get Token-
def get_tokens_for_user(user, role):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token.payload['role'] = role

    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }

# pagination class-
class MyPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4



# Teacher-
class TeacherList(APIView):
    pagination_class = MyPagination 
    def get(self, request):
        if 'popular' in request.GET:
            sql = "SELECT t.id, t.full_name, t.email, t.password, t.qualification, t.mobile_no, t.profile_img, t.skills, t.verify_status, t.otp_digit, t.facebook_url, t.twitter_url, t.instagram_url, COUNT(c.id) AS total_course FROM main_teacher AS t INNER JOIN main_course AS c ON c.teacher_id = t.id GROUP BY t.id, t.full_name, t.email, t.password, t.qualification, t.mobile_no, t.profile_img, t.skills, t.verify_status, t.otp_digit, t.facebook_url, t.twitter_url, t.instagram_url ORDER BY total_course DESC"
            queryset = models.Teacher.objects.raw(sql)
        else:
            queryset = models.Teacher.objects.all()
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
  
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Teacher.objects.all()
   serializer_class=TecherSerializer

class TeacherDashboard(generics.RetrieveAPIView):
   permission_classes=[Teacher]
   queryset = models.Teacher.objects.all()
   serializer_class=TeacherDashboardSerializer

class TeacherCourseList(generics.ListCreateAPIView):
    permission_classes = [Teacher]
    serializer_class = CourseSerializer
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        print('teacher id -> ',teacher_id)
        teacher = models.Teacher.objects.get(pk=teacher_id)
        print('teacher ',teacher)
        return models.Course.objects.filter(teacher=teacher)

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

class teacher_login(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print("this is teacher data",request.body)
            try:
                teacher_data = models.Teacher.objects.filter(email=email, password=password).first()
            except ObjectDoesNotExist:
                teacher_data = None
            if teacher_data:   
                token = get_tokens_for_user(teacher_data,'teacher')
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
        print(otp_digit)
        verify = models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).first()
        if verify:
            models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).update(verify_status=True)
            token = get_tokens_for_user(verify,'student')
            return JsonResponse({'token':token,'bool': True, 'teacher_id': verify.id})
        else:
            return JsonResponse({'bool': False})
        
class teacher_forgot_password(APIView):
    def post(self, request):
        email = request.data.get('email')
        verify = models.Teacher.objects.filter(email=email).first()
        if verify:
            link=f"http://localhost:3000/teacher-change-password/{verify.id}/"
            send_mail(
                "Change Password",
                "Please Verify Your Account",
                "settings.EMAIL_HOST_USER",
                [email],
                fail_silently=False,
                html_message=f"<p>Your Password Reset Link is</p><p>{link}</p>"  
        )
            return JsonResponse({'bool': True, 'msg': 'please check your email'})
        else:
            return JsonResponse({'bool': False,'msg':'Invalid Email!!'})
        
class teacher_change_password(APIView):
    permission_classes=[Teacher]
    def get(self, request, teacher_id):
            return JsonResponse({'bool': False, 'msg': 'Get Method not Allowed!'})
    def post(self, request, teacher_id):
        try:
            password = request.data.get('password')
            if password is None:
                return JsonResponse({'bool': False, 'msg': 'Password field is missing from the request!'}, status=status.HTTP_400_BAD_REQUEST)
            teacher_data = models.Teacher.objects.get(id=teacher_id)
            teacher_data.password = password
            teacher_data.save()
            return JsonResponse({'bool': True, 'msg': 'Password has been changed!'})
        except models.Teacher.DoesNotExist:
            return JsonResponse({'bool': False, 'msg': 'Teacher not found!'}, status=status.HTTP_404_NOT_FOUND)
        
class MyTeacherList(generics.ListAPIView):
   permission_classes = [Student]
   queryset = models.Course.objects.all()
   serializer_class = CourseSerializer
   def get_queryset(self):
    if 'student_id' in self.kwargs: 
       student_id=self.kwargs['student_id']
       sql = f"SELECT DISTINCT ON (t.full_name) c.id, t.full_name FROM main_course AS c JOIN main_studentcourseenrollment AS e ON e.course_id = c.id JOIN main_teacher AS t ON c.teacher_id = t.id WHERE e.student_id = {student_id} ORDER BY t.full_name, c.id"
       qs=models.Course.objects.raw(sql)
       return qs
    
#teacher end

# Course-
class CategoryList(generics.ListCreateAPIView):
   queryset=models.CourseCategory.objects.all()
   serializer_class=CategorySerializer

class CourseList(APIView):
    pagination_class = MyPagination
    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = CourseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def get_queryset(self):
        queryset = models.Course.objects.all()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            queryset = queryset.order_by('-id')[:limit]
        elif 'category' in self.request.GET:
            print("this is link",self.request)
            category = self.request.GET['category']
            queryset = models.Course.objects.filter(techs__icontains=category)
            return queryset
        elif 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name = self.request.GET['skill_name']
            teacher = self.request.GET['teacher']
            teacher = models.Teacher.objects.filter(id=teacher).first()
            print(teacher)
            queryset = models.Course.objects.filter(techs__icontains=skill_name,teacher=teacher) 
        elif 'searchString' in self.request.GET:
            search = self.request.GET['searchString']
            queryset = models.Course.objects.filter(Q(techs__icontains=search)|Q(title__icontains=search))
        elif 'studentId' in self.request.GET:
            student_id = self.request.GET['studentId']
            print("this is my student id  ",student_id , "type of student id",type(student_id))
            student = models.Student.objects.get(pk=student_id)
            queries = [Q(techs__iendswith=value) for value in student.interested_categories]
            query = queries.pop()
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

class CourseDetailView(generics.RetrieveAPIView):
   queryset = models.Course.objects.all()
   serializer_class = CourseSerializer

class CourseRatingList(generics.ListCreateAPIView):
   pagination_class= MyPagination
   queryset=models.CourseRating.objects.all()
   serializer_class=CourseRatingSerializer
   def get_queryset(self):
      if 'popular' in self.request.GET:
        sql = """
    WITH ranked_courses AS (
        SELECT cr.id, 
               cr.course_id, 
               cr.student_id, 
               cr.rating, 
               cr.reviews, 
               cr.review_time,
               SUM(cr.rating) OVER (PARTITION BY cr.course_id) AS calculate_total_rating,
               ROW_NUMBER() OVER (PARTITION BY cr.course_id ORDER BY cr.rating DESC) AS row_num
        FROM main_courserating AS cr
    )
    SELECT id, course_id, student_id, rating, reviews, review_time, calculate_total_rating
    FROM ranked_courses
    WHERE row_num = 1
    ORDER BY calculate_total_rating DESC
    LIMIT 4
"""
        return models.CourseRating.objects.raw(sql)
      if 'all' in self.request.GET:
         sql = "SELECT * ,AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
         return models.CourseRating.objects.raw(sql)
      return models.CourseRating.objects.filter(course__isnull=False).order_by('-rating')
   
#course end

#student---
class student_login(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print("this is student data",request.body)
            try:
                student_data = models.Student.objects.filter(email=email, password=password).first()
            except ObjectDoesNotExist:
                student_data = None
            if student_data: 
                token = get_tokens_for_user(student_data,'student')
                return JsonResponse({'token':token,'bool': True, 'student_id': student_data.id})
            else:
                return JsonResponse({'bool': False,'msg':'Invalied Email or password'})
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    def get(self, request):
        return JsonResponse({'error': 'GET method not allowed'}, status=405)

class verify_student_via_otp(APIView):
    def post(self, request, student_id):
        otp_digit = request.data.get('otp_digit')
        print(otp_digit,student_id)  # Using request.data for POST data
        verify = models.Student.objects.filter(id=student_id, otp_digit=otp_digit).first()
        if verify:
            models.Student.objects.filter(id=student_id, otp_digit=otp_digit).update(verify_status=True)
            token = get_tokens_for_user(verify,'student')
            return JsonResponse({'token':token,'bool': True, 'student_id': verify.id})
        else:
            return JsonResponse({'bool': False})
             
class student_forgot_password(APIView):
    def post(self, request):
        email = request.data.get('email')
        verify = models.Student.objects.filter(email=email).first()
        if verify:
            link=f"http://localhost:3000/student-change-password/{verify.id}/"
            send_mail(
                "Change Password",
                "Please Verify Your Account",
                "settings.EMAIL_HOST_USER",
                [email], 
                fail_silently=False,
                html_message=f"<p>Your Password Reset Link is</p><p>{link}</p>" 
        )
            return JsonResponse({'bool': True, 'msg': 'please check your email'})
        else:
            return JsonResponse({'bool': False,'msg':'Invalid Email!!'})
    
class student_changne_password(APIView):
    def get(self, request, student_id):
            return JsonResponse({'bool': False, 'msg': 'Get Method not Allowed!'})
    def post(self, request, student_id):
        try:
            password = request.data.get('password')
            print(password)
            if password is None:
                return JsonResponse({'bool': False, 'msg': 'Password field is missing from the request!'}, status=status.HTTP_400_BAD_REQUEST)
            student_data = models.Student.objects.get(id=student_id)
            student_data.password = password
            student_data.save()
            return JsonResponse({'bool': True, 'msg': 'Password has been changed!'})
        except models.Student.DoesNotExist:
            return JsonResponse({'bool': False, 'msg': 'Student not found!'}, status=status.HTTP_404_NOT_FOUND)

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
   permission_classes = [Student]
   queryset = models.Student.objects.all()
   serializer_class=StudentDashboardSerializer
    
class StudentEnrollCourseList(generics.ListCreateAPIView):
   queryset=models.StudentCourseEnrollment.objects.all()
   serializer_class=StudentCourseEnrollSerializer

class StudentFavoriteCourseList(generics.ListCreateAPIView):
   permission_classes=[Student]
   queryset = models.StudentFavoriteCourse.objects.all()
   serializer_class = StudentFavoriteCourseSerializer
   def get_queryset(self):
    if 'student_id' in self.kwargs: 
       student_id=self.kwargs['student_id']
       student = models.Student.objects.get(pk=student_id)
       return models.StudentFavoriteCourse.objects.filter(student=student).distinct()
    
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
       return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct('student')
    elif 'student_id' in self.kwargs: 
       student_id=self.kwargs['student_id']
       student = models.Student.objects.get(pk=student_id)
       return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
    
#end student
   

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

#fatch-
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
    
@csrf_exempt
def remove_favorite_course(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    favoriteStatus=models.StudentFavoriteCourse.objects.filter(course=course,student=student).delete()
    if favoriteStatus:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})   
    
def fatch_rating_status(request,student_id,course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    ratingStatus=models.CourseRating.objects.filter(course=course,student=student).count()
    if ratingStatus:
       return JsonResponse({'bool':True})
    else:
       return JsonResponse({'bool':False})
    
#Assignment-
class AssignmentList(generics.ListCreateAPIView):
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer
   def get_queryset(self):
        student_id = self.kwargs['student_id']
        teacher_id = self.kwargs['teacher_id'] 
        student = models.Student.objects.get(pk=student_id)
        teacher = models.Teacher.objects.get(pk=teacher_id)  
        return models.StudentAssignment.objects.filter(student=student,teacher=teacher)
     
class MyAssignmentList(generics.ListCreateAPIView):
   permission_classes = [Student]
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer
   def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = models.Student.objects.get(pk=student_id)
        models.Notification.objects.filter(student=student,notif_for='student',notif_subject='assignment').update(notifiread_status=True)
        return models.StudentAssignment.objects.filter(student=student)
    
class UpdateAssignmentList(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = [Student]
   queryset=models.StudentAssignment.objects.all()
   serializer_class=StudentAssignmentSerializer

#Assignment End

# Other-
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

# send massage functionality-
class save_teacher_student_msg(APIView):
    def post(self, request, teacher_id, student_id):
        try:
            teacher = models.Teacher.objects.get(id=teacher_id)
            student = models.Student.objects.get(id=student_id)
            msg_text = request.data.get('msg_text')  # Using request.data instead of request.POST for DRF
            msg_from = request.data.get('msg_from')
            print("teacher",teacher,"student",student,"msg_text",msg_text,"msg_from",msg_from)
            msg_instance = models.TeacherStudentChat.objects.create(
                teacher=teacher,
                student=student,
                msg_text=msg_text,
                msg_from=msg_from,
            )
            return JsonResponse({'bool': True, 'msg': 'Message has been Send'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occurred!', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
         
class MessageList(generics.ListAPIView):
   queryset=models.TeacherStudentChat.objects.all()
   serializer_class=TeacherStudentChatSerializer
   def get_queryset(self):
      teacher_id = self.kwargs['teacher_id']
      student_id = self.kwargs['student_id']
      teacher = models.Teacher.objects.get(pk=teacher_id)
      student = models.Student.objects.get(pk=student_id)
      return models.TeacherStudentChat.objects.filter(teacher=teacher,student=student).exclude(msg_text='')

class save_teacher_student_group_msg(APIView):
    def post(self, request, teacher_id):
        try:
            teacher = models.Teacher.objects.get(id=teacher_id)
            msg_text = request.data.get('msg_text')  # Using request.data instead of request.POST for DRF
            msg_from = request.data.get('msg_from')
            enrolledList=models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
            for enrolled in enrolledList:
                msg_instance = models.TeacherStudentChat.objects.create(
                    teacher=teacher,
                    student=enrolled.student,
                    msg_text=msg_text,
                    msg_from=msg_from,
                )
            return JsonResponse({'bool': True, 'msg': 'Message has been Send'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occurred!', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



