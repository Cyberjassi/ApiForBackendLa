class Student(models.Model):
    id = models.AutoField(primary_key=True)
    full_name=models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100,null=True,blank=True)
    username=models.CharField(max_length=200)
    interested_categories=models.TextField()
    profile_img=models.ImageField(upload_to='student_profile_imgs/',null=True)
    verify_status=models.BooleanField(default=False)
    otp_digit=models.CharField(max_length=20,null=True)
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
    # will-
    # teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
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
    
