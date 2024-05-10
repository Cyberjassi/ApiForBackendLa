from . import models
from rest_framework import serializers
from django.contrib.flatpages.models import FlatPage

from django.core.mail import send_mail




class TecherSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = models.Teacher
        fields =  ['id','full_name','email','password','qualification','mobile_no','skills','profile_img','skill_list','teacher_courses']
        # 'teacher_courses'
        # will-
        # fields =  ['id','full_name','email','password','qualification','mobile_no','skills','otp_digit','profile_img','teacher_courses','skill_list','total_teacher_courses','verify_status']
        # depth 1 for teacher_courses
    def __init__(self,*args, **kwargs):
       super(TecherSerializer,self).__init__(*args,**kwargs)
       request = self.context.get('request')
       self.Meta.depth = 0
       if request and request.method == 'GET':
           self.Meta.depth = 1

        
    # def create(self,validate_data):
    #     email=self.validated_data['email']
    #     otp_digit=self.validated_data['otp_digit']
    #     instance=super(TecherSerializer,self).create(validate_data)
    #     send_mail(
    #        "Verify Account",
    #         "Please Verify your account",
    #         "jaswantkhatri30@gmail.com",
    #         [email],
    #         fail_silently=False,
    #         html_message=f"<p>Your otp is </p><p>{otp_digit}</p>"
    #     )
     
    #     return instance
    
class TeacherLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = models.Teacher
    fields = ['email', 'password']


class TeacherDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['total_teacher_courses','total_teacher_students','total_teacher_chapters']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        # will---
        # fields =  ['id','title','description','total_courses']
        fields = ['id','title','description']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs','course_chapter','related_videos','tech_list','total_enrolled_students','course_rating']

    def __init__(self,*args,**kwargs):
        super(CourseSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth = 1
    

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id','course','title','description','video','video_duration','remarks']

    def __init__(self,*args,**kwargs):
        super(ChapterSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=1
            # will-
            # self.Meta.depth=1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields =  ['id','full_name','email','password','username','interested_categories']
        # will---
        # fields =  ['id','full_name','email','profile_img','password','username','interested_categories']
    def __init__(self, *args, **kwargs):
        super(StudentSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=2

# class CourseEnrollSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.StudentCourseEnrollment
#         fields =  ['id','course','student','enrolled_time']
class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCourseEnrollment
        # will-
        # fields =  ['id','course','student','teacher','enrolled_time']
        fields =  ['id','course','student','enrolled_time']
        depth=1
    
    def __init__(self, *args,  **kwargs):
        super(StudentCourseEnrollSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2


class StudentFavoriteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentFavoriteCourse
        fields=['id','course','student','status']
    def __init__(self, *args, **kwargs):
        super(StudentFavoriteCourseSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2

class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseRating
        fields =  ['id','course','student','rating','reviews','review_time']
    #if we only want to see data that is get then we assgin depth =1 but we need post request then we need depth 1
    def __init__(self,*args,**kwargs):
        super(CourseRatingSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=2


class StudentAssignmentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.StudentAssignment
        fields = ['id','teacher','student', 'title', 'detail','student_status','add_time']
    
    def __init__(self,*args,**kwargs):
        super(StudentAssignmentSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth = 1


class StudentDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['enrolled_courses','favorite_courses','complete_assignments','pending_assignments']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ['teacher','student','notif_subject','notif_for']
        # 'notif_created_time','notifiread_status' (that is serilaizer field perhaps)



class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ['id', 'teacher', 'title', 'detail', 'add_time']
    
    def __init__(self,*args,**kwargs):
        super(QuizSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth = 2



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizQuestions
        fields = ['id','quiz','questions','ans1','ans2','ans3','ans4','right_ans','add_time']

    def __init__(self,*args,**kwargs):
        super(QuestionSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=1


class CourseQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseQuiz
        fields =  ['id','teacher','course','quiz','add_time']
    
    def __init__(self, *args,  **kwargs):
        super(CourseQuizSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
class AttempQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttempQuiz
        fields =  ['id','student','question','right_ans','add_time']
    
    def __init__(self, *args,  **kwargs):
        super(AttempQuizSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudyMaterial
        fields = ['id','course','title','description','upload','remarks']

    def __init__(self,*args,**kwargs):
        super(StudyMaterialSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=1


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields =  ['question','answer']


# serializer for flate page in django-
class FlatPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=FlatPage
        fields=['id','title','content','url']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Contact
        fields=['id','full_name','email','query_txt']