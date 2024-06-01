class TecherSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = models.Teacher
        fields =  ['id','full_name','email','password','qualification','mobile_no','skills','profile_img','skill_list','teacher_courses','total_teacher_courses','otp_digit','verify_status']
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

        
    def create(self, validated_data):
        email = validated_data.get('email')
        otp_digit = validated_data.get('otp_digit')
        instance = super(TecherSerializer, self).create(validated_data)
        send_mail(
            "Verify Account",
            "Please Verify Your Account",
            "settings.EMAIL_HOST_USER",
            [email],  # Use 'email' instead of 'self.email'
            fail_silently=False,
            html_message=f"<p>Your OTP is </p><p>{otp_digit}</p>"  # Use 'otp_digit' instead of 'self.otp_digit'
        )
        return instance

    
class TeacherLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = models.Teacher
    fields = ['email', 'password']

class TeacherDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['total_teacher_courses','total_teacher_students','total_teacher_chapters']

class TeacherStudentChatSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.TeacherStudentChat
        fields = ['id','teacher','student','msg_from','msg_text','msg_time']
    
    def to_representation(self, instance):
        representation = super(TeacherStudentChatSerializer,self).to_representation(instance)
        representation['msg_time'] = instance.msg_time.strftime('%Y-%m-%d %H:%M')
        return representation
