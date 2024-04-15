from . import models
from rest_framework import serializers

class TecherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields =  ['id','full_name','email','password','qualification','mobile_no','skills','profile_img','teacher_courses','skill_list']
        # depth 1 for teacher_courses
    def __init__(self,*args, **kwargs):
       super(TecherSerializer,self).__init__(*args,**kwargs)
       request = self.context.get('request')
       self.Meta.depth = 0
       if request and request.method == 'GET':
           self.Meta.depth = 1


class TeacherDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['total_teacher_courses','total_teacher_students','total_teacher_chapters']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields =  ['id','title','description']

class CourseSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Course
        fields = ['id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs', 'course_chapter', 'related_videos', 'tech_list', 'total_enrolled_student', 'course_rating']
    
    def __init__(self,*args,**kwargs):
        super(CourseSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth = 2

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id','course','title','description','video','remarks']

    def __init__(self,*args,**kwargs):
        super(ChapterSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields =  ['id','full_name','email','profile_img','password','username','interested_categories']

# class CourseEnrollSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.StudentCourseEnrollment
#         fields =  ['id','course','student','enrolled_time']
class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCourseEnrollment
        fields =  ['id','course','student','teacher','enrolled_time']
    
    def __init__(self, *args,  **kwargs):
        super(StudentCourseEnrollSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1


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
            self.Meta.depth=1


class StudentAssignmentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.StudentAssignment
        fields = ['id','teacher','student', 'title', 'detail','student_status','add_time']
    
    def __init__(self,*args,**kwargs):
        super(StudentAssignmentSerializer,self).__init__(*args,**kwargs)
        request = self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth = 2


class StudentDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['enrolled_courses','favorite_courses','complete_assignments','pending_assignments']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ['teacher','student','notif_subject','notif_for','notif_created_time','notifiread_status']
