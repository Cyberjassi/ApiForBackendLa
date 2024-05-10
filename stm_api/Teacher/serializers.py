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






    



