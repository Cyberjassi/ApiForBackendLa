from django.contrib import admin
from .models import Teacher, CourseCategory, Course, Chapter, Student, StudentCourseEnrollment, StudentFavoriteCourse, CourseRating, StudentAssignment, Notification,Quiz,QuizQuestions,CourseQuiz,AttempQuiz,StudyMaterial,FAQ,TeacherStudentChat,Transaction

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ['full_name','email','password','qualification','mobile_no','profile_img','skills','verify_status','otp_digit']

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentCourseEnrollment)
class StudentCourseEnrollmentAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentFavoriteCourse)
class StudentFavoriteCourseAdmin(admin.ModelAdmin):
    pass

@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    pass

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display=['id','notif_subject','notif_for','notifiread_status']

admin.site.register(Notification)



admin.site.register(Quiz)
admin.site.register(QuizQuestions)
admin.site.register(CourseQuiz)
admin.site.register(AttempQuiz)
admin.site.register(StudyMaterial)
admin.site.register(FAQ)
admin.site.register(TeacherStudentChat)
admin.site.register(Transaction)