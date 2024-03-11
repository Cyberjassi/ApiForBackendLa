from django.db import models

class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
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

class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    description=models.TextField()

    class Meta:
        verbose_name_plural = "2. Course Categories"
    
    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.TextField()
    featured_img=models.ImageField(upload_to='course_imgs/',null=True)
    techs=models.TextField(null=True)
    
    class Meta:
        verbose_name_plural = "3. Course"
    
    def __str__(self) -> str:
        return self.title
    

class Chapter(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
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
    qualification=models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    address=models.TextField()
    interested_categories=models.TextField()
    class Meta:
        verbose_name_plural = "5. Student"

