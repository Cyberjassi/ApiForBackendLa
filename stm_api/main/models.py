from django.db import models
from django.core import serializers

class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    detail=models.TextField(null=True)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    skills=models.TextField()

    #for shows in panel Table name
    class Meta:
        verbose_name_plural = "1. Teachers"

    def __str__(self) -> str:
        return self.full_name
    
    def skill_list(self):
        skill_list=self.skills.split(',')
        return skill_list

class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    description=models.TextField()

    class Meta:
        verbose_name_plural = "2. Course Categories"
    
    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    #related name fatch all the courses which teacher have
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='teacher_courses')
    title=models.CharField(max_length=150)
    description=models.TextField()
    featured_img=models.ImageField(upload_to='course_imgs/',null=True)
    techs=models.TextField(null=True)
    
    class Meta:
        verbose_name_plural = "3. Course"
    
    def __str__(self) -> str:
        return self.title
    
        ########-
    def related_videos(self):
        related_videos=Course.objects.filter(techs__icontains=self.techs).exclude(id=self.id)
        return serializers.serialize('json',related_videos)
    #give skills -
    def tech_list(self):
        tech_list=self.techs.split(',')
        return tech_list
    
    def total_enrolled_student(self):
        total_enrolled_student=StudentCourseEnrollment.objects.filter(course=self).count()
        return total_enrolled_student
    
    def course_rating(self):
        course_rating=CourseRating.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return course_rating['avg_rating']

    

class Chapter(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_chapter")
    title=models.CharField(max_length=150)
    description=models.TextField()
    video=models.FileField(upload_to='chapter_videos/',null=True)
    remarks=models.TextField(null=True)
    
    class Meta:
        verbose_name_plural = "4. Chapter"
    
    def __str__(self) -> str:
        return self.title
    



class Student(models.Model):
    full_name=models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    username=models.CharField(max_length=200)
    interested_categories=models.TextField()
    class Meta:
        verbose_name_plural = "5. Student"

    def __str__(self) -> str:
        return self.full_name

class StudentCourseEnrollment(models.Model):
    student =models.ForeignKey(Student,on_delete=models.CASCADE,related_name='enrolled_student')
    course =models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrolled_courses')
    enrolled_time=models.DateTimeField(auto_now_add=True)
    depth = 1

    class Meta:
        verbose_name_plural = "6. Enrolled Courses"

    def __str__(self) -> str:
        return f"{self.course}-{self.student}"
    

class CourseRating(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    rating=models.PositiveIntegerField(default=0)
    reviews=models.TextField(null=True)
    review_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.course}-{self.student}-{self.rating}"
    
    class Meta:
        verbose_name_plural = "7. Course Ratings"