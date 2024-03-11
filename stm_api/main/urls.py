from django.urls import path
from . import views

urlpatterns = [
    path('teacher/',views.TeacherList.as_view()),
    path('teacher/<int:pk>/',views.TeacherDetail.as_view()),
    # path('techer-login',views.teacher_login),#
    path('category/',views.CategoryList.as_view()),
    path('course/',views.CourseList.as_view()),
    path('chapter/',views.ChapterList.as_view()),
    path('course-chapters/<int:course_id>',views.CourseChapterList.as_view()),
    path('teacher-courses/<int:teacher_id>',views.TeacherCourseList.as_view()),

    path('teacher-courses-detail/<int:pk>',views.TeacherCourseDetail.as_view()),

 
]