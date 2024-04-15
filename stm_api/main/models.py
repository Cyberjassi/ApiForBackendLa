from django.db import models
from django.core import serializers

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    profile_img=models.ImageField(upload_to='teahcer_profile_imgs/',null=True)
    skills=models.TextField()

    #for shows in panel Table name
    class Meta:
        verbose_name_plural = "1. Teachers"

    def __str__(self) -> str:
        return self.full_name
    
    def skill_list(self):
        skill_list=self.skills.split(',')
        return skill_list
    
    def total_teacher_courses(self):
        total_courses = Course.objects.filter(teacher=self).count()
        return total_courses
    
    def total_teacher_chapters(self):
        total_chapters = Chapter.objects.filter(course__teacher=self).count()
        return total_chapters
    
    def total_teacher_students(self):
        total_students = StudentCourseEnrollment.objects.filter(course__teacher=self).count()
        return total_students
    


class CourseCategory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description=models.TextField()


    class Meta:
        verbose_name_plural = "2. Course Categories"
    
    # that is show on CourseCategory data when we put the data
    def __str__(self) -> str:
        return self.title
    

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    #related name fatch all the courses which teacher have through id 
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
    id = models.AutoField(primary_key=True)
    # realted name paraticular course have particular chapter
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
    id = models.AutoField(primary_key=True)
    full_name=models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    username=models.CharField(max_length=200)
    interested_categories=models.TextField()
    profile_img=models.ImageField(upload_to='student_profile_imgs/',null=True)
    class Meta:
        verbose_name_plural = "5. Student"

    def __str__(self) -> str:
        return self.full_name
    
    def enrolled_courses(self):
        enrolled_courses = StudentCourseEnrollment.objects.filter(student=self).count()
        return enrolled_courses
    
    def favorite_courses(self):
        favorite_courses = StudentFavoriteCourse.objects.filter(student=self).count()
        return favorite_courses
    
    def complete_assignments(self):
        complete_assignments = StudentAssignment.objects.filter(student=self,student_status=True).count()
        return complete_assignments
    
    def pending_assignments(self):
        pending_assignments = StudentAssignment.objects.filter(student=self,student_status=False).count()
        return pending_assignments

class StudentCourseEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    student =models.ForeignKey(Student,on_delete=models.CASCADE,related_name='enrolled_student')
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    course =models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrolled_courses')
    enrolled_time=models.DateTimeField(auto_now_add=True)
    # depth = 1

    class Meta:
        verbose_name_plural = "6. Enrolled Courses"

    def __str__(self) -> str:
        return f"{self.course}-{self.student}"
    
class StudentFavoriteCourse(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '7. Student Favorite Courses'

    def __str__(self) -> str:
        return f"{self.course}-{self.student}"
    

class CourseRating(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    rating=models.PositiveBigIntegerField(default=0)
    reviews=models.TextField(null=True)
    review_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.course}-{self.student}-{self.rating}"
    
    class Meta:
        verbose_name_plural = "8. Course Ratings"
class StudentAssignment(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=200)
    detail=models.TextField(null=True)
    student_status = models.BooleanField(default=False,null=True)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = "9. Student Assignments"


class Notification(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    notif_subject = models.CharField(max_length=200,verbose_name='Notification Subject',null=True)
    notif_for = models.CharField(max_length=200,verbose_name='Notification For')
    notif_created_time=models.DateTimeField(auto_now_add=True)
    notifiread_status=models.BooleanField(default=False,verbose_name='Notification Status')

    class Meta:
        verbose_name_plural = "10. Notification"


class Quiz(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=200)
    detail = models.TextField()
    add_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "11. Quiz"

    def __str__(self):
        return f"{self.title}"

class QuizQuestions(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,null=True)
    questions=models.CharField(max_length=200)
    ans1=models.CharField(max_length=200)
    ans2=models.CharField(max_length=200)
    ans3=models.CharField(max_length=200)
    ans4=models.CharField(max_length=200)
    right_ans=models.CharField(max_length=200)
    add_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "12. Quiz Questions"
    
    def __str__(self):
        return f"{self.questions}"


class CourseQuiz(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,null=True)
    add_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "13. Course Quiz"

    def __str__(self):
        return f"{self.course}-{self.quiz}"