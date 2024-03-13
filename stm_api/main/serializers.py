from . import models
from rest_framework import serializers

class TecherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields =  ['id','detail','full_name','email','password','qualification','mobile_no','skills','teacher_courses','skill_list']
        # depth 1 for teacher_courses
        depth=1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields =  ['id','title','description']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        #course chapter in chapter foreign key (coursse) we define realted name course chapter then it give us chapter according to course
        #######related_videos
        fields =  ['id','category','teacher','title','description','featured_img','techs','course_chapter','related_videos','tech_list','total_enrolled_student','course_rating']
        # depth 1 menas it go in this model and fatch also his parent data 
        depth = 1

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id','course','title','description','video','chapter_duration','remarks']

    def __init__(self,*args,**kwargs):
        super(ChapterSerializer,self).__init__(*args,**kwargs)
        request=self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields =  ['id','full_name','email','password','username','interested_categories']

class CourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCourseEnrollment
        fields =  ['id','course','student','enrolled_time']


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