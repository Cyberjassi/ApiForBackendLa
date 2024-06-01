from django.db import models


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100,blank=True,null=True)
    qualification=models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20,unique=True)
    profile_img=models.ImageField(upload_to='teahcer_profile_imgs/',null=True)
    skills=models.TextField()
    verify_status=models.BooleanField(default=False)
    otp_digit=models.CharField(max_length=20,null=True)

    facebook_url=models.URLField(null=True)
    twitter_url=models.URLField(null=True)
    instagram_url=models.URLField(null=True)


    #for shows in panel Table name
    class Meta:
        verbose_name_plural = "1. Teachers"

    def __str__(self) -> str:
        return self.full_name
    # becuse want to show all skill in ui
    def skill_list(self):
        skill_list=self.skills.split(',')
        return skill_list
    
    def total_teacher_courses(self):
        total_courses = models.Course.objects.filter(teacher=self).count()
        return total_courses
    
    def total_teacher_chapters(self):
        total_chapters = models.Chapter.objects.filter(course__teacher=self).count()
        return total_chapters
    
    def total_teacher_students(self):
        total_students = models.StudentCourseEnrollment.objects.filter(course__teacher=self).count()
        return total_students